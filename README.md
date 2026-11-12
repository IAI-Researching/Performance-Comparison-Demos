# Performance Comparison Demos

> Standardized autonomous benchmarks of frontier AI models across developer harnesses on complex code generation—evaluated under strict zero-context isolation with full performance telemetry.

---

## 🎯 Purpose & Methodology

This repository houses head-to-head, reproducible evaluations comparing frontier AI models and their native developer harnesses (Claude Code `2.1.322`, Antigravity CLI `1.5.6`, Codex CLI `0.167.1`, Kimi Code `2.5.3`, OpenCode `2.2.7`) on demanding single-file 3D applications, physics simulations, and complex interactive systems.

### The Autonomous Pass@1 Benchmark Protocol

To measure real-world engineering utility without artificial constraints or human bias:

1. **Zero-Context Isolation**:
   - Every session starts completely stateless with zero previous conversation history, no memory persistence, and no carried-over project settings.
   - All agents receive the exact same byte-identical prompt.

2. **Full Native Toolsets**:
   - Rather than stripping tools from coding agents, each harness is invoked with its full native capability (file creation, multi-pass editing, reading, and bash execution).
   - This measures how effectively each agent harness plans, implements, inspects, and refines code autonomously.

3. **Strict Zero-Intervention (Pass@1)**:
   - Exactly one initial prompt is sent.
   - No human in the loop: no follow-up corrections, no hints, and no relayed error messages.
   - The agent works until it autonomously declares completion.

4. **Automated Post-Run Verification**:
   - Once an agent declares completion, the deliverable is audited via an automated 18-point CDP runtime verification suite checking for WebGL rendering, draw calls, countdown sequence, dock geometry, canvas freeze, determinism across scrubbing, and clean workdir.

5. **Universal Telemetry**:
   - Every run logs exact wall-clock duration, Time to First Token (TTFT), thinking/reasoning tokens, total output tokens, tool call counts, prompt cache hit ratios, and cryptographic SHA-256 integrity hashes.

---

## 🔬 Benchmark Specification: `ballistics/water-balloon`

- **Task**: Interactive single-file 3D physics demonstration modeling an elastomeric thin-shell water balloon impacting a rigid barrier.
- **Specification Enforcement**: Hardened **Unobstructed Viewport** constraint—the viewport contains exclusively the Three.js canvas, center countdown, and bottom dock (all extraneous headers, mastheads, annotation overlays, and phase description panels are strictly forbidden).
- **Duration**: Exactly 8.000-second timeline scrubbing with sub-millisecond precision.

### 🛡️ Reproducibility Standard

- [`prompt.md`](prompt.md): Canonical, immutable prompt specification.
- [`parameters.txt`](parameters.txt): Ground-truth CLI execution flags per harness.
- [`evaluate.py`](evaluate.py): Automated 18-point verification suite.
- [`TELEMETRY.md`](TELEMETRY.md): Comprehensive executive comparison matrix and compliance audit.
- [`telemetry.json`](telemetry.json): Machine-readable telemetry array.
- [`CHECKSUMS.sha256`](CHECKSUMS.sha256): Cryptographic signatures for all deliverables.
