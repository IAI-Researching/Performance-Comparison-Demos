# Autonomous Benchmark Telemetry (first passing attempt): ballistics/water-balloon

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1111.8s | 26 | 19 | 1,663,208 | 1,616,768 | 17,883 | 45,051 | 46,398 B | 1,196 | `aa4368f83241...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1203.9s | 36 | 30 | 1,344,955 | 1,294,080 | 20,799 | 46,759 | 42,890 B | 1,082 | `1306ebbea3fb...` |
| **Codex GPT 6.2 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 2318.8s | 63 | 58 | 4,256,635 | 4,120,576 | 37,197 | 75,595 | 55,957 B | 1,340 | `4973e8703eab...` |
| **Codex GPT 6.2 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1535.8s | 79 | 74 | 3,992,941 | 3,884,032 | 29,022 | 65,175 | 59,350 B | 1,520 | `703f1793997a...` |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 858.8s | 36 | 31 | 2,963,555 | 2,917,376 | 19,777 | 41,342 | 33,417 B | 904 | `b6f6b35f923e...` |
| **Claude Fable 5.1 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 4423.1s | 51 | 48 | 746 | 3,495,006 | 213,245 | 255,903 | 45,889 B | 1,066 | `48744707d064...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 5835.3s | 282 | 281 | 254 | 59,948,939 | 323,212 | 491,384 | 100,339 B | 2,178 | `e181ef5272d3...` |
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 3667.2s | 85 | 83 | 134 | 16,652,522 | 307,141 | 374,424 | 63,304 B | 1,564 | `caa99f3c7e84...` |
| **Claude Sonnet 5.5 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 4205.5s | 264 | 262 | 272 | 55,872,855 | 319,122 | 459,573 | 70,372 B | 1,759 | `edcfc82d8a12...` |
| **Gemini 4 Argon (High)** | Antigravity CLI 1.5.6 | `High` | **PASS (100.0%)** | 1661.1s | 16 | 13 | 123,554 | 775,088 | 35,359 | 88,002 | 85,916 B | 2,249 | `5b41d39000c0...` |
| **Gemini 4 Carbon (High)** | Antigravity CLI 1.5.6 | `High` | **PASS (100.0%)** | 1559.0s | 26 | 25 | 210,534 | 2,795,612 | 52,814 | 107,376 | 99,631 B | 2,557 | `076115f2e6ec...` |
| **Gemini 4 Hydrogen (XHigh)** | Antigravity CLI 1.5.7 | `Xhigh` | **PASS (100.0%)** | 497.3s | 29 | 28 | 226,568 | 3,285,041 | 52,137 | 132,647 | 67,716 B | 1,913 | `761076827c34...` |
| **Qwen 4 Max (Max)** | Qwen Code 1.0.0-preview.1 | `Max` | **PASS (100.0%)** | 2833.9s | 94 | 95 | 6,834,634 | 6,632,704 | 0 | 112,709 | 35,565 B | 1,050 | `f7dd3716235f...` |
| **Qwen 4 Max (XHigh) via OpenCode** | OpenCode 2.3.0 | `Xhigh` | **PASS (100.0%)** | 1528.3s | 21 | 30 | 149 | 1,624,153 | 53,790 | 34,979 | 51,640 B | 1,388 | `1fcd1ce74e80...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.5.3 | `Max` | **PASS (100.0%)** | 785.5s | 1 | 44 | 77,938 | 2,216,448 | 0 | 61,117 | 39,695 B | 1,161 | `6d07fd066dfb...` |
| **GLM 5.3 (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 1058.0s | 15 | 19 | 161,910 | 1,559,032 | 87,427 | 22,220 | 49,724 B | 1,306 | `234fb540e146...` |
| **GLM 5.3 Flash (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 613.2s | 7 | 7 | 201,999 | 385,024 | 65,654 | 18,456 | 46,714 B | 1,309 | `2f8ef44c5fc9...` |
| **MiniMax M3.1 Flash (Max)** | MiniMax Code 0.7.4 | `Max` | **PASS (100.0%)** | 4078.6s | 1 | 294 | 595,313 | 51,247,363 | 0 | 230,859 | 52,182 B | 1,427 | `b4b36c70aa57...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `ballistics/water-balloon`
- **Protocol**: Autonomous, first passing attempt, protocol v1.1 (zero human-in-the-loop, sandboxed). See PROTOCOL.md; failed attempts are re-run, not published.
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
- **Mixed protocol versions**: this table contains v1.0 and v1.1 rows. v1.1 rows: Codex GPT 6 Astra (Max), Codex GPT 6.1 Sol (Max), Codex GPT 6.2 Astra (Max), Codex GPT 6.2 Sol (Max), Codex GPT 6.1 Terra (Max), Claude Sonnet 5.5 (Max), Qwen 4 Max (Max), Qwen 4 Max (XHigh) via OpenCode. All other rows are v1.0 (shared host, some runs overlapped; wall-clock approximate). Harness versions and effort levels vary between rows; see ../../PROTOCOL.md.
