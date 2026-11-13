# Autonomous Pass@1 Benchmark Telemetry: ballistics/water-balloon

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.167.1 | `Max` | **PASS (100.0%)** | 861.6s | 38 | 32 | 1,483,498 | 1,444,352 | 11,157 | 35,564 | 40,291 B | 1,068 | `d72c7f93f657...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.167.1 | `Max` | **PASS (100.0%)** | 1250.4s | 26 | 20 | 1,247,049 | 1,204,480 | 21,468 | 49,066 | 46,100 B | 1,168 | `3a0695baa191...` |
| **Claude Fable 5.1 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 4423.1s | 51 | 48 | 746 | 3,495,006 | 213,245 | 255,903 | 45,889 B | 1,066 | `48744707d064...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 5835.3s | 282 | 281 | 254 | 59,948,939 | 323,212 | 491,384 | 100,339 B | 2,178 | `e181ef5272d3...` |
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **FAIL (94.4%)** | 3409.5s | 90 | 86 | 144 | 23,507,688 | 270,021 | 365,946 | 81,549 B | 1,972 | `4418fbabf13b...` |
| **Gemini 4 Argon (High)** | Antigravity CLI 1.5.6 | `High` | **PASS (100.0%)** | 1661.1s | 16 | 13 | 123,554 | 775,088 | 35,359 | 88,002 | 85,916 B | 2,249 | `5b41d39000c0...` |
| **Gemini 4 Carbon (High)** | Antigravity CLI 1.5.7 | `High` | **FAIL (94.4%)** | 2226.9s | 21 | 17 | 447,277 | 1,650,969 | 75,690 | 126,437 | 95,714 B | 2,338 | `48f8fb525f1d...` |
| **Gemini 4 Hydrogen (XHigh)** | Antigravity CLI 1.5.7 | `Xhigh` | **PASS (100.0%)** | 497.3s | 29 | 28 | 226,568 | 3,285,041 | 52,137 | 132,647 | 67,716 B | 1,913 | `761076827c34...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.5.3 | `Max` | **PASS (100.0%)** | 785.5s | 1 | 44 | 77,938 | 2,216,448 | 0 | 61,117 | 39,695 B | 1,161 | `6d07fd066dfb...` |
| **GLM 5.3 (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 1058.0s | 15 | 19 | 161,910 | 1,559,032 | 87,427 | 22,220 | 49,724 B | 1,306 | `234fb540e146...` |
| **GLM 5.3 Flash (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 613.2s | 7 | 7 | 201,999 | 385,024 | 65,654 | 18,456 | 46,714 B | 1,309 | `2f8ef44c5fc9...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `ballistics/water-balloon`
- **Protocol**: Autonomous Pass@1 (Zero human-in-the-loop, isolated ephemeral sandbox).
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
