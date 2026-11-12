#!/usr/bin/env python3
"""
Universal Benchmark Evaluation Suite (`evaluate_template.py`).
Performs:
  1. Strict structural HTML/CSS/JS parsing (via `html.parser`, zero host JS execution).
  2. Static dependency & zero-external-asset enforcement (rejects HTTP/HTTPS, relative
     assets, CSS `@import` / external `url()`, `<link rel="stylesheet">`, `<script type="importmap">`).
  3. Canonical DOM contract verification (`#stage`, `#countdown`, `#dock`, child controls,
     unobstructed viewport with zero visible text outside `#dock` and `#countdown`).
  4. Mandatory Headless Browser Runtime, Network & Behavioral Verification via
     `baseline/verify_runtime.py` (fail-closed unless `--static-only` is explicitly passed
     for offline syntax debugging).
"""

import argparse
from html.parser import HTMLParser
import json
import os
import re
import signal
import subprocess
import sys

PINNED_THREEJS_URL = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"

CANONICAL_IDS = (
    "stage",
    "countdown",
    "dock",
    "btn-refire",
    "btn-toggle",
    "icon-pause",
    "icon-play",
    "speed-group",
    "scrubber",
)


class SingleFileHTMLAuditor(HTMLParser):
    """Parses HTML structure without executing any submitted code."""

    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.has_doctype = False
        self.has_html_open = False
        self.has_html_close = False
        self.style_blocks = []
        self.inline_scripts = []
        self.external_scripts = []
        self.importmaps = 0
        self.forbidden_resource_tags = []
        self.ids = []
        self.tag_stack = []
        self.allowed_text_depth = 0
        self.raw_text_tag = None
        self.current_buf = []
        self.stray_visible_text = []
        self.speed_pills = []
        self.scrubber_attrs = None

    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype html"):
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        attr_map = {k.lower(): (v if v is not None else "") for k, v in attrs}

        if t == "html":
            self.has_html_open = True

        el_id = attr_map.get("id", "").strip()
        if el_id:
            self.ids.append(el_id)

        cls_tokens = set(attr_map.get("class", "").split())
        if "speed-pill" in cls_tokens and "data-speed" in attr_map:
            self.speed_pills.append(attr_map["data-speed"].strip())

        if el_id == "scrubber" and t == "input":
            self.scrubber_attrs = attr_map

        # Resource & external asset inspection on real parsed attributes
        if t == "script":
            stype = attr_map.get("type", "").strip().lower()
            if stype == "importmap":
                self.importmaps += 1
            if "src" in attr_map:
                self.external_scripts.append(attr_map["src"].strip())
            else:
                self.raw_text_tag = "script"
                self.current_buf = []
        elif t == "style":
            self.raw_text_tag = "style"
            self.current_buf = []
        elif t == "link":
            rel = attr_map.get("rel", "").lower()
            href = attr_map.get("href", "").strip()
            if href and not href.startswith("data:"):
                self.forbidden_resource_tags.append(f"<link rel={rel!r} href={href!r}>")
        elif t in ("img", "audio", "video", "source", "iframe", "embed", "object", "track"):
            src = (attr_map.get("src") or attr_map.get("data") or attr_map.get("srcset") or "").strip()
            if src and not src.startswith(("data:", "blob:")):
                self.forbidden_resource_tags.append(f"<{t} src={src!r}>")

        # Track whether we are inside #dock or #countdown for visible text auditing
        entering_allowed = el_id in ("dock", "countdown")
        if t not in self.VOID_ELEMENTS:
            self.tag_stack.append((t, entering_allowed))
            if entering_allowed:
                self.allowed_text_depth += 1

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == "html":
            self.has_html_close = True

        if self.raw_text_tag == t:
            body_text = "".join(self.current_buf)
            if t == "style":
                self.style_blocks.append(body_text)
            elif t == "script":
                self.inline_scripts.append(body_text)
            self.raw_text_tag = None
            self.current_buf = []

        # Pop matching tag from stack
        for idx in range(len(self.tag_stack) - 1, -1, -1):
            open_t, entered_allowed = self.tag_stack[idx]
            if open_t == t:
                popped = self.tag_stack[idx:]
                del self.tag_stack[idx:]
                for _, flag in popped:
                    if flag:
                        self.allowed_text_depth = max(0, self.allowed_text_depth - 1)
                break

    def handle_data(self, data):
        if self.raw_text_tag in ("style", "script"):
            self.current_buf.append(data)
            return

        active_tags = {t for t, _ in self.tag_stack}
        if active_tags & {"head", "title", "script", "style", "noscript", "template"}:
            return
        if "body" in active_tags and self.allowed_text_depth == 0:
            txt = data.strip()
            if txt:
                self.stray_visible_text.append(txt[:40])


def find_runtime_verifier():
    env_override = os.environ.get("PCD_RUNTIME_VERIFIER")
    if env_override and os.path.isfile(env_override):
        return env_override

    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "verify_runtime.py"),
        os.path.abspath(os.path.join(here, "..", "..", "baseline", "verify_runtime.py")),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def evaluate(html_path, expected_duration=None, require_runtime=True, lenient_ui=False):
    results = {
        "file": os.path.abspath(html_path),
        "checks": [],
        "passed_checks": 0,
        "total_checks": 0,
        "score_pct": 0.0,
        "verdict": "FAIL",
    }

    def check(name, passed, detail=""):
        results["checks"].append({
            "name": name,
            "passed": bool(passed),
            "detail": detail,
        })
        results["total_checks"] += 1
        if passed:
            results["passed_checks"] += 1

    if not os.path.isfile(html_path) or os.path.islink(html_path):
        check("Regular Deliverable File", False, f"Missing or non-regular file: {html_path}")
        return results

    raw_bytes = open(html_path, "rb").read()
    try:
        content = raw_bytes.decode("utf-8")
        utf8_ok = True
    except UnicodeDecodeError as exc:
        content = raw_bytes.decode("utf-8", errors="replace")
        utf8_ok = False
        utf8_err = str(exc)

    check(
        "Valid UTF-8 Non-Empty Deliverable",
        utf8_ok and len(raw_bytes) > 0,
        f"Size: {len(raw_bytes):,} bytes, {len(content.splitlines())} LOC"
        if utf8_ok
        else f"Invalid UTF-8 encoding: {utf8_err}",
    )

    auditor = SingleFileHTMLAuditor()
    try:
        auditor.feed(content)
        auditor.close()
        parse_ok = True
    except Exception as exc:
        parse_ok = False
        parse_err = str(exc)

    check(
        "Parsed Single-File HTML Structure",
        parse_ok and auditor.has_doctype and auditor.has_html_open and auditor.has_html_close,
        "Valid <!DOCTYPE html> and <html>...</html> document"
        if parse_ok
        else f"HTML parse error: {parse_err}",
    )

    has_inline_css = any(s.strip() for s in auditor.style_blocks)
    has_inline_js = any(j.strip() for j in auditor.inline_scripts)
    check(
        "Non-Empty Inline <style> & <script>",
        has_inline_css and has_inline_js,
        f"style_blocks={len(auditor.style_blocks)}, inline_scripts={len(auditor.inline_scripts)}",
    )

    # Dependency & Zero External Assets Audit (HTML + CSS)
    css_combined = "\n".join(auditor.style_blocks)
    css_imports = re.findall(r"@import\b", css_combined, flags=re.IGNORECASE)
    css_urls = [
        u.strip(" '\"")
        for u in re.findall(r"url\(\s*([^)]+?)\s*\)", css_combined, flags=re.IGNORECASE)
        if not u.strip(" '\"").startswith(("data:", "#"))
    ]

    exact_three_cdn = auditor.external_scripts == [PINNED_THREEJS_URL] and auditor.importmaps == 0
    check(
        "Pinned Three.js r128 Single Script Tag",
        exact_three_cdn,
        f"external_scripts={auditor.external_scripts}, importmaps={auditor.importmaps}",
    )

    zero_static_ext = (
        len(auditor.forbidden_resource_tags) == 0
        and len(css_imports) == 0
        and len(css_urls) == 0
    )
    check(
        "Zero External HTML/CSS Asset References",
        zero_static_ext,
        "Zero forbidden external tags, @import rules, or external CSS url() references"
        if zero_static_ext
        else f"tags={auditor.forbidden_resource_tags[:2]}, imports={len(css_imports)}, css_urls={css_urls[:2]}",
    )

    # Canonical DOM IDs & Unobstructed Static Text Audit
    if not lenient_ui:
        missing_ids = [cid for cid in CANONICAL_IDS if cid not in auditor.ids]
        dup_ids = [cid for cid in CANONICAL_IDS if auditor.ids.count(cid) > 1]
        dom_contract_ok = (
            len(missing_ids) == 0
            and len(dup_ids) == 0
            and auditor.speed_pills == ["0.25", "0.5", "1.0", "2.0"]
            and auditor.scrubber_attrs is not None
        )
        check(
            "Canonical UI DOM Skeleton & IDs",
            dom_contract_ok,
            f"missing={missing_ids}, duplicates={dup_ids}, speed_pills={auditor.speed_pills}",
        )

    check(
        "Static Unobstructed Viewport (Zero Stray Body Text)",
        len(auditor.stray_visible_text) == 0,
        "Zero text nodes outside #dock and #countdown"
        if not auditor.stray_visible_text
        else f"Stray text: {auditor.stray_visible_text[:3]}",
    )

    # Mandatory Headless Browser Runtime, Network & Behavioral Grading (Fail-Closed!)
    if require_runtime:
        verifier = find_runtime_verifier()
        if not verifier:
            check(
                "[Runtime] Verifier Available",
                False,
                "Fail-closed: verify_runtime.py not found",
            )
        else:
            cmd = [sys.executable, verifier, html_path]
            if expected_duration is not None:
                cmd.extend(["--duration", str(expected_duration)])
            if lenient_ui:
                cmd.append("--lenient-ui")
            p_rt = None
            rt_pgid = None
            try:
                p_rt = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True,
                )
                rt_pgid = os.getpgid(p_rt.pid)
                rt_stdout, rt_stderr = p_rt.communicate(timeout=60)
                rt_data = json.loads(rt_stdout)
                rt_checks = rt_data.get("runtime_checks")
                if not isinstance(rt_checks, list) or len(rt_checks) == 0:
                    check(
                        "[Runtime] Valid Runtime Report",
                        False,
                        f"Missing runtime_checks (rc={p_rt.returncode}, stderr={rt_stderr[:160]})",
                    )
                else:
                    for rc in rt_checks:
                        check(
                            f"[Runtime] {rc.get('name', 'Check')}",
                            bool(rc.get("passed")),
                            rc.get("detail", ""),
                        )
                    if rt_data.get("verdict") != "PASS" or p_rt.returncode != 0:
                        if all(c["passed"] for c in results["checks"]):
                            check("[Runtime] Overall Verdict", False, "Runtime verifier returned non-PASS")
            except subprocess.TimeoutExpired:
                check("[Runtime] Headless Execution Timeout", False, "verify_runtime.py exceeded 60s timeout")
            except Exception as exc:
                check("[Runtime] Headless Execution Output", False, f"Failed to parse verify_runtime.py JSON: {exc}")
            finally:
                if rt_pgid is not None:
                    try:
                        os.killpg(rt_pgid, signal.SIGTERM)
                    except Exception:
                        pass
                    if p_rt is not None:
                        try:
                            p_rt.wait(timeout=2)
                        except Exception:
                            pass
                    try:
                        os.killpg(rt_pgid, signal.SIGKILL)
                    except Exception:
                        pass

    if results["total_checks"] > 0:
        results["score_pct"] = round(
            (results["passed_checks"] / results["total_checks"]) * 100.0, 1
        )
        results["verdict"] = (
            "PASS" if results["passed_checks"] == results["total_checks"] else "FAIL"
        )
    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate single-file benchmark deliverable.")
    parser.add_argument("html_path", help="Path to candidate index.html")
    parser.add_argument("--duration", type=float, default=None, help="Expected exact simulation duration in seconds")
    parser.add_argument("--static-only", action="store_true", help="Skip headless browser runtime checks (debug only)")
    parser.add_argument("--lenient-ui", action="store_true", help="Use legacy UI tolerances for pre-baseline runs")
    args = parser.parse_args()

    res = evaluate(
        args.html_path,
        expected_duration=args.duration,
        require_runtime=not args.static_only,
        lenient_ui=args.lenient_ui,
    )
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
