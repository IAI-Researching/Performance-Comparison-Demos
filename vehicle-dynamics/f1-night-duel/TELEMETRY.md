# Autonomous Pass@1 Benchmark Telemetry: vehicle-dynamics/f1-night-duel

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1700.9s | 57 | 47 | 3,611,866 | 3,535,104 | 21,746 | 58,096 | 67,948 B | 982 | `3a6326f67f83...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 2515.6s | 55 | 47 | 4,454,013 | 4,379,008 | 41,303 | 90,983 | 67,200 B | 993 | `95682d93e65c...` |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1578.3s | 63 | 55 | 5,936,135 | 5,874,176 | 37,348 | 77,000 | 57,478 B | 824 | `eed7eee0cf3a...` |
| **Claude Fable 5.1 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 3718.2s | 65 | 64 | 1,026 | 6,861,599 | 163,289 | 263,518 | 114,109 B | 2,050 | `f6b86c6b7a29...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.325 | `Max` | **PASS (100.0%)** | 5767.2s | 173 | 171 | 198 | 37,161,080 | 365,577 | 506,672 | 137,419 B | 2,109 | `6d68fc6a4d59...` |
| **DeepSeek v4.1 Flash (Max)** | DeepSeek CLI 0.2.2-rc.3 | `Max` | **PASS (100.0%)** | 3055.7s | 252 | 252 | 131,472 | 67,322,880 | 0 | 308,909 | 116,586 B | 3,017 | `bd810b1fbcf2...` |
| **Gemini 4 Argon (High)** | Antigravity CLI 1.5.9 | `High` | **PASS (100.0%)** | 1483.4s | 42 | 41 | 244,023 | 4,426,165 | 29,379 | 107,814 | 125,910 B | 3,318 | `b59092f31fa8...` |
| **Gemini 4 Carbon (High)** | Antigravity CLI 1.5.9 | `High` | **PASS (100.0%)** | 2252.6s | 45 | 48 | 282,754 | 5,627,182 | 47,524 | 142,638 | 171,836 B | 4,490 | `80e2c6aad4a0...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.6.0 | `Max` | **PASS (100.0%)** | 3999.3s | 2 | 110 | 174,270 | 9,900,965 | 0 | 105,792 | 86,347 B | 2,087 | `84a7708256ca...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `vehicle-dynamics/f1-night-duel`
- **Protocol**: Autonomous Pass@1 (Zero human-in-the-loop, isolated ephemeral sandbox).
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
