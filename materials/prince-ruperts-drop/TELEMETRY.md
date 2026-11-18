# Autonomous Benchmark Telemetry (first passing attempt): materials/prince-ruperts-drop

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.167.1 | `Max` | **PASS (100.0%)** | 1167.0s | 42 | 36 | 2,164,542 | 2,096,640 | 16,225 | 39,692 | 40,026 B | 866 | `514d1885fcd4...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 909.1s | 28 | 23 | 1,108,395 | 1,004,672 | 17,824 | 39,823 | 42,169 B | 847 | `9ae9e53438d4...` |
| **Codex GPT 6.2 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 2054.5s | 51 | 47 | 4,014,546 | 3,791,744 | 35,000 | 68,632 | 58,174 B | 1,371 | `2f13657953bf...` |
| **Codex GPT 6.2 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1428.0s | 57 | 52 | 4,045,693 | 3,930,368 | 27,653 | 60,144 | 55,520 B | 1,370 | `d55bb76db7c5...` |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI 0.168.0 | `Max` | **PASS (100.0%)** | 1332.9s | 68 | 60 | 5,951,186 | 5,884,288 | 23,253 | 66,234 | 35,965 B | 918 | `bc6cff6d4450...` |
| **Claude Fable 5.1 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 4621.9s | 134 | 128 | 3,966 | 31,492,245 | 235,618 | 311,156 | 59,459 B | 1,409 | `1c7840fe83e2...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 5467.3s | 166 | 164 | 226 | 43,091,373 | 295,012 | 461,119 | 88,714 B | 2,052 | `4f5d87a87d07...` |
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 2981.1s | 92 | 90 | 168 | 19,687,839 | 207,139 | 296,913 | 81,607 B | 1,983 | `9efdd728f9d4...` |
| **Claude Sonnet 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 5065.9s | 233 | 303 | 254 | 46,347,751 | 302,857 | 426,529 | 73,155 B | 1,726 | `a95c8d7de175...` |
| **Claude Haiku 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 1942.2s | 99 | 98 | 198 | 33,062,889 | 276,287 | 340,656 | 44,138 B | 1,117 | `50420c443b2c...` |
| **Gemini 4 Argon (High)** | Antigravity CLI 1.5.8 | `High` | **PASS (100.0%)** | 997.9s | 17 | 16 | 135,106 | 1,321,407 | 19,564 | 95,263 | 85,195 B | 2,318 | `ded50d19cd8e...` |
| **Gemini 4 Carbon (High)** | Antigravity CLI 1.5.8 | `High` | **PASS (100.0%)** | 1999.5s | 45 | 44 | 533,849 | 5,309,450 | 58,294 | 136,271 | 103,857 B | 2,690 | `7e39ceef690f...` |
| **Gemini 4 Hydrogen (XHigh)** | Antigravity CLI 1.5.8 | `Xhigh` | **PASS (100.0%)** | 644.4s | 37 | 36 | 205,362 | 4,043,760 | 56,600 | 116,786 | 79,685 B | 2,186 | `09a3cf635ff7...` |
| **Qwen 4 Max (Max)** | Qwen Code 1.0.0-preview.1 | `Max` | **PASS (100.0%)** | 996.1s | 22 | 24 | 866,703 | 817,152 | 0 | 38,138 | 39,054 B | 1,118 | `fd98c069efc7...` |
| **Qwen 4 Max (XHigh) via OpenCode** | OpenCode 2.3.0 | `Xhigh` | **PASS (100.0%)** | 1593.9s | 29 | 34 | 205 | 2,279,419 | 65,481 | 26,167 | 47,190 B | 1,334 | `22a55f657b56...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.6.0 | `Max` | **PASS (100.0%)** | 2122.7s | 2 | 47 | 115,666 | 1,926,656 | 0 | 57,273 | 48,737 B | 1,325 | `b8ca6a4df257...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `materials/prince-ruperts-drop`
- **Protocol**: Autonomous, first passing attempt, protocol v1.1 (zero human-in-the-loop, sandboxed). See PROTOCOL.md; failed attempts are re-run, not published.
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
- **Mixed protocol versions**: this table contains v1.0 and v1.1 rows. v1.1 rows: Codex GPT 6.1 Sol (Max), Codex GPT 6.2 Astra (Max), Codex GPT 6.2 Sol (Max), Qwen 4 Max (Max), Qwen 4 Max (XHigh) via OpenCode, Kimi Code K3.1 Pro (Max). All other rows are v1.0 (shared host, some runs overlapped; wall-clock approximate). Harness versions and effort levels vary between rows; see ../../PROTOCOL.md.
