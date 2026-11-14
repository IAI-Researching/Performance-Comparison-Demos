# Autonomous Pass@1 Benchmark Telemetry: materials/prince-ruperts-drop

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6 Astra (Max)** | Codex CLI 0.167.1 | `Max` | **PASS (100.0%)** | 1167.0s | 42 | 36 | 2,164,542 | 2,096,640 | 16,225 | 39,692 | 40,026 B | 866 | `514d1885fcd4...` |
| **Codex GPT 6.1 Sol (Max)** | Codex CLI 0.167.1 | `Max` | **PASS (100.0%)** | 1361.0s | 42 | 36 | 1,566,423 | 1,519,616 | 22,008 | 47,774 | 42,794 B | 975 | `9d51a8bf90ca...` |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI 0.168.0 | `Max` | **PASS (100.0%)** | 1332.9s | 68 | 60 | 5,951,186 | 5,884,288 | 23,253 | 66,234 | 35,965 B | 918 | `bc6cff6d4450...` |
| **Claude Fable 5.1 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 4621.9s | 134 | 128 | 3,966 | 31,492,245 | 235,618 | 311,156 | 59,459 B | 1,409 | `1c7840fe83e2...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 5467.3s | 166 | 164 | 226 | 43,091,373 | 295,012 | 461,119 | 88,714 B | 2,052 | `4f5d87a87d07...` |
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 2981.1s | 92 | 90 | 168 | 19,687,839 | 207,139 | 296,913 | 81,607 B | 1,983 | `9efdd728f9d4...` |
| **Claude Sonnet 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 5065.9s | 233 | 303 | 254 | 46,347,751 | 302,857 | 426,529 | 73,155 B | 1,726 | `a95c8d7de175...` |
| **Claude Haiku 5.5 (Max)** | Claude Code 2.1.322 | `Max` | **PASS (100.0%)** | 1942.2s | 99 | 98 | 198 | 33,062,889 | 276,287 | 340,656 | 44,138 B | 1,117 | `50420c443b2c...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `materials/prince-ruperts-drop`
- **Protocol**: Autonomous Pass@1 (Zero human-in-the-loop, isolated ephemeral sandbox).
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
