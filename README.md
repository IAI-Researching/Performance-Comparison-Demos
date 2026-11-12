# Performance Comparison Demos

> Standardized autonomous benchmarks of frontier AI models across developer harnesses on complex code generation—evaluated under strict zero-context isolation with full performance telemetry.

---

## 🎯 Purpose & Methodology

This repository houses reproducible evaluations comparing frontier AI models across their native developer harnesses—or dedicated agentic orchestrators when no first-party CLI exists—on demanding single-file 3D applications and physics simulations. Specific harness versions and runtime environments are dynamically captured at execution time and preserved in the benchmark telemetry.

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

---

## 🏆 Benchmark Deliverables

| Model | Developer Harness | Verification | Wall-Clock | Deliverable |
| :--- | :--- | :---: | :---: | :---: |
| **GLM 5.3 Flash** | OpenCode | **PASS (100%)** | 613.2s | [`glm-5.3-flash/`](glm-5.3-flash/) |
| **Kimi Code K3.1 Pro** | Kimi Code | **PASS (100%)** | 785.5s | [`kimi-k3.1-pro/`](kimi-k3.1-pro/) |
| **Codex GPT 6 Astra** | Codex CLI | **PASS (100%)** | 861.6s | [`codex-gpt-6-astra/`](codex-gpt-6-astra/) |
| **GLM 5.3** (Flagship) | OpenCode | **PASS (100%)** | 1058.0s | [`glm-5.3/`](glm-5.3/) |
| **Codex GPT 6.1 Sol** | Codex CLI | **PASS (100%)** | 1250.4s | [`codex-gpt-6.1-sol/`](codex-gpt-6.1-sol/) |
| **Gemini 4 Carbon** | Antigravity CLI | **PASS (100%)** | 1559.0s | [`gemini-4-carbon/`](gemini-4-carbon/) |
| **Gemini 4 Argon** | Antigravity CLI | **PASS (100%)** | 1661.1s | [`gemini-4-argon/`](gemini-4-argon/) |
| **Claude Fable 5.1** | Claude Code | **PASS (100%)** | 4423.1s | [`claude-fable-5.1/`](claude-fable-5.1/) |
| **Claude Fable 5.2** | Claude Code | **PASS (100%)** | 5835.3s | [`claude-fable-5.2/`](claude-fable-5.2/) |

*See [`TELEMETRY.md`](TELEMETRY.md) for full token metrics, cache ratios, and runtime verification logs.*
