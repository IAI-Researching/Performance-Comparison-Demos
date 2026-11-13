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
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 3667.2s | 85 | 83 | 134 | 16,652,522 | 307,141 | 374,424 | 63,304 B | 1,564 | `caa99f3c7e84...` |
| **Gemini 4 Argon (High)** | Antigravity CLI 1.5.6 | `High` | **PASS (100.0%)** | 1661.1s | 16 | 13 | 123,554 | 775,088 | 35,359 | 88,002 | 85,916 B | 2,249 | `5b41d39000c0...` |
| **Gemini 4 Carbon (High)** | Antigravity CLI 1.5.6 | `High` | **PASS (100.0%)** | 1559.0s | 26 | 25 | 210,534 | 2,795,612 | 52,814 | 107,376 | 99,631 B | 2,557 | `076115f2e6ec...` |
| **Gemini 4 Hydrogen (XHigh)** | Antigravity CLI 1.5.7 | `Xhigh` | **PASS (100.0%)** | 497.3s | 29 | 28 | 226,568 | 3,285,041 | 52,137 | 132,647 | 67,716 B | 1,913 | `761076827c34...` |
| **Gemini 3.8 Flash (High)** | Antigravity CLI 1.5.7 | `High` | **PASS (100.0%)** | 366.9s | 28 | 27 | 239,563 | 2,193,931 | 61,155 | 100,050 | 44,842 B | 1,419 | `f5d06cabae72...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.5.3 | `Max` | **PASS (100.0%)** | 785.5s | 1 | 44 | 77,938 | 2,216,448 | 0 | 61,117 | 39,695 B | 1,161 | `6d07fd066dfb...` |
| **GLM 5.3 (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 1058.0s | 15 | 19 | 161,910 | 1,559,032 | 87,427 | 22,220 | 49,724 B | 1,306 | `234fb540e146...` |
| **GLM 5.3 Flash (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 613.2s | 7 | 7 | 201,999 | 385,024 | 65,654 | 18,456 | 46,714 B | 1,309 | `2f8ef44c5fc9...` |
| **MiniMax M3.1 Flash (Max)** | MiniMax Code 0.7.4 | `Max` | **PASS (100.0%)** | 4078.6s | 1 | 294 | 595,313 | 51,247,363 | 0 | 230,859 | 52,182 B | 1,427 | `b4b36c70aa57...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `ballistics/water-balloon`
- **Protocol**: Autonomous Pass@1 (Zero human-in-the-loop, isolated ephemeral sandbox).
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
