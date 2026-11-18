# Autonomous Benchmark Telemetry (first passing attempt): character-action/storm-titan

> Autonomous evaluation under hardened Unobstructed Viewport specification enforcement.

---

## 📊 Leaderboard & Telemetry Matrix

| Model | Developer Harness | Effort | Protocol | Attempts | Verification | Wall-Clock | Turns | Tool Calls | Input Tokens | Cached Tokens | Thinking Tokens | Output Tokens | Code Size | LOC | SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6.2 Sol (Max)** | Codex CLI 0.170.0 | `Max` | v1.1 | 1 | **PASS (100.0%)** | 2570.8s | 44 | 39 | 6,094,254 | 5,905,152 | 37,254 | 106,754 | 129,810 B | 2,982 | `e66eb5775e8a...` |
| **Claude Fable 5.2 (Max)** | Claude Code 2.1.325 | `Max` | v1.1 | 1 | **PASS (100.0%)** | 7666.2s | 117 | 114 | 154 | 27,385,762 | 541,019 | 697,996 | 176,035 B | 2,552 | `fefa9dac5220...` |
| **Claude Opus 5.5 (Max)** | Claude Code 2.1.325 | `Max` | v1.1 | 1 | **PASS (100.0%)** | 6208.8s | 142 | 140 | 252 | 53,068,313 | 448,229 | 624,354 | 200,568 B | 3,954 | `08729dbd34a9...` |

---

## 🔬 Methodology & Enforced Constraints

- **Benchmark ID**: `character-action/storm-titan`
- **Protocol**: Autonomous, first passing attempt (zero human-in-the-loop, sandboxed). Each row lists the protocol version it ran under; compare only rows with the same version. See PROTOCOL.md; failed attempts are re-run, not published, and **Attempts** counts every launch including failed ones.
- **Effort**: reasoning effort is not equal across models (see PROTOCOL.md, Known confounds).
- **Token and turn columns** are counted differently by each harness; compare them only within one harness.
- **Unobstructed Viewport Constraint**: Strict negative constraint forbidding extraneous headers, mastheads, annotation overlays, and phase description panels. Viewport contains exclusively Three.js canvas, center countdown, and bottom dock.
