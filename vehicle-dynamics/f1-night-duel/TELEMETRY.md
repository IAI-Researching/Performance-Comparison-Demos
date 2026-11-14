# Autonomous Pass@1 Benchmark Telemetry: vehicle-dynamics/f1-night-duel

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1700.9s | 57 | 47 | 3,611,866 | 3,535,104 | 21,746 | 58,096 | 67,948 B | 982 | `3a6326f67f83...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 2515.6s | 55 | 47 | 4,454,013 | 4,379,008 | 41,303 | 90,983 | 67,200 B | 993 | `95682d93e65c...` |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI 0.169.0 | `Max` | **PASS (100.0%)** | 1578.3s | 63 | 55 | 5,936,135 | 5,874,176 | 37,348 | 77,000 | 57,478 B | 824 | `eed7eee0cf3a...` |
| **DeepSeek v4.1 Flash (Max)** | DeepSeek CLI 0.2.2-rc.3 | `Max` | **PASS (100.0%)** | 3055.7s | 252 | 252 | 131,472 | 67,322,880 | 0 | 308,909 | 116,586 B | 3,017 | `bd810b1fbcf2...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.6.0 | `Max` | **PASS (100.0%)** | 3999.3s | 2 | 110 | 174,270 | 9,900,965 | 0 | 105,792 | 86,347 B | 2,087 | `84a7708256ca...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `vehicle-dynamics/f1-night-duel`
- **Protocol**: Autonomous Pass@1 (Zero human-in-the-loop, isolated ephemeral sandbox).
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
