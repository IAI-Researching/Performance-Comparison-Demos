# Autonomous Benchmark Telemetry (first passing attempt): vehicle-dynamics/f1-night-duel

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1700.9s | 57 | 47 | 3,611,866 | 3,535,104 | 21,746 | 58,096 | 67,948 B | 982 | `3a6326f67f83...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 2515.6s | 55 | 47 | 4,454,013 | 4,379,008 | 41,303 | 90,983 | 67,200 B | 993 | `95682d93e65c...` |
| **Codex GPT 6.2 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 3192.5s | 88 | 82 | 7,110,871 | 6,949,504 | 35,275 | 97,408 | 112,214 B | 2,009 | `08ace90dce84...` |
| **Codex GPT 6.2 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 2128.0s | 65 | 59 | 5,176,963 | 4,837,376 | 38,206 | 93,466 | 109,578 B | 2,469 | `8d425b02fb33...` |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1578.3s | 63 | 55 | 5,936,135 | 5,874,176 | 37,348 | 77,000 | 57,478 B | 824 | `eed7eee0cf3a...` |
| **Claude Fable 5.1 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 3718.2s | 65 | 64 | 1,026 | 6,861,599 | 163,289 | 263,518 | 114,109 B | 2,050 | `f6b86c6b7a29...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 5767.2s | 173 | 171 | 198 | 37,161,080 | 365,577 | 506,672 | 137,419 B | 2,109 | `6d68fc6a4d59...` |
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 5030.6s | 211 | 210 | 322 | 78,987,241 | 303,112 | 458,151 | 148,125 B | 2,664 | `871452b06c60...` |
| **Claude Sonnet 5.5 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 4637.9s | 252 | 251 | 270 | 56,408,994 | 342,241 | 539,874 | 161,444 B | 2,826 | `0bcb8d03c6de...` |
| **Claude Haiku 5.5 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 2286.7s | 74 | 72 | 102 | 15,475,235 | 404,089 | 478,995 | 78,656 B | 1,813 | `b49b161ddee8...` |
| **DeepSeek v4.1 Flash (Max)** | DeepSeek CLI 0.2.2-rc.3 | `Max` | **PASS (100.0%)** | 3055.7s | 252 | 252 | 131,472 | 67,322,880 | 0 | 308,909 | 116,586 B | 3,017 | `bd810b1fbcf2...` |
| **Gemini 4 Argon (High)** | Antigravity CLI 1.5.9 | `High` | **PASS (100.0%)** | 1483.4s | 42 | 41 | 244,023 | 4,426,165 | 29,379 | 107,814 | 125,910 B | 3,318 | `b59092f31fa8...` |
| **Gemini 4 Carbon (High)** | Antigravity CLI 1.5.9 | `High` | **PASS (100.0%)** | 2252.6s | 45 | 48 | 282,754 | 5,627,182 | 47,524 | 142,638 | 171,836 B | 4,490 | `80e2c6aad4a0...` |
| **Gemini 4 Hydrogen (XHigh)** | Antigravity CLI 1.5.9 | `Xhigh` | **PASS (100.0%)** | 1284.7s | 86 | 108 | 570,792 | 7,616,719 | 72,568 | 273,284 | 130,385 B | 3,662 | `477698fc345a...` |
| **Qwen 4 Max (Max)** | Qwen Code 1.0.0-preview.1 | `Max` | **PASS (100.0%)** | 2702.7s | 53 | 79 | 3,894,288 | 3,722,240 | 0 | 106,246 | 84,516 B | 2,108 | `079dd936fbd8...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.6.0 | `Max` | **PASS (100.0%)** | 3999.3s | 2 | 110 | 174,270 | 9,900,965 | 0 | 105,792 | 86,347 B | 2,087 | `84a7708256ca...` |
| **MiniMax M3.1 Flash (Max)** | MiniMax Code 0.7.7 | `Max` | **PASS (100.0%)** | 4047.7s | N/A | 286 | 356,026 | 44,401,280 | 0 | 334,059 | 109,931 B | 2,701 | `9e2bdf304e50...` |
| **ERNIE 5.5 Flash Preview (High)** | OpenCode 2.3.0 | `High` | **PASS (100.0%)** | 1100.7s | 57 | 56 | 247,005 | 10,892,032 | 187,399 | 35,987 | 81,783 B | 2,616 | `7a57afa1b673...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `vehicle-dynamics/f1-night-duel`
- **Protocol**: Autonomous, first passing attempt, protocol v1.1 (zero human-in-the-loop, sandboxed). See PROTOCOL.md; failed attempts are re-run, not published.
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
