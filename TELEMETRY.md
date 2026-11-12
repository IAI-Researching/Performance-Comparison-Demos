# Autonomous Pass@1 Benchmark Telemetry: ballistics/water-balloon

> Head-to-head evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **GLM 5.3 (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 1058.0s | 15 | 19 | 161,910 | 1,559,032 | 87,427 | 22,220 | 49,724 B | 1,306 | `234fb540e146...` |
| **GLM 5.3 Flash (Max)** | OpenCode 2.2.7 | `Max` | **PASS (100.0%)** | 613.2s | 7 | 7 | 201,999 | 385,024 | 65,654 | 18,456 | 46,714 B | 1,309 | `2f8ef44c5fc9...` |
| **Kimi Code K3.1 Pro (Max)** | Kimi Code 2.5.3 | `Max` | **PASS (100.0%)** | 785.5s | 1 | 44 | 77,938 | 2,216,448 | 0 | 61,117 | 39,695 B | 1,161 | `6d07fd066dfb...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `ballistics/water-balloon`
- **Protocol**: Autonomous Pass@1 (Zero human-in-the-loop, isolated ephemeral sandbox).
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
