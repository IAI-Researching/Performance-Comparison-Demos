# Performance Comparison Demos

> Standardized autonomous benchmarks of frontier AI models across native developer harnesses (or dedicated agentic orchestrators) on demanding 3D physics applications with full performance telemetry.

---

## 🎯 Purpose & Methodology

This repository houses reproducible evaluations comparing frontier AI models across their native developer harnesses—or dedicated agentic orchestrators when no first-party CLI exists—on demanding single-file 3D applications and physics simulations. Specific harness versions and runtime environments are dynamically captured at execution time and preserved in the benchmark telemetry.

### The Autonomous Pass@1 Benchmark Protocol

To measure real-world engineering utility without artificial constraints or human bias:

1. **Zero-Context Isolation**:
   - Every session starts completely stateless with zero previous conversation history, no memory persistence, and no carried-over project settings.
   - All agents receive the exact same byte-identical prompt.

2. **Full Toolset Execution**:
   - Rather than stripping or restricting tools from coding agents, each harness is invoked with its complete capabilities (file creation, multi-pass editing, inspection, and terminal execution).
   - This measures how effectively each agent environment plans, implements, inspects, and refines code autonomously.

3. **Strict Zero-Intervention (Pass@1)**:
   - Exactly one initial prompt is sent.
   - No human in the loop: no follow-up corrections, no hints, and no relayed error messages.
   - The agent works until it autonomously declares completion.

4. **Automated Post-Run Verification**:
   - Once an agent declares completion, the deliverable is audited via an automated 18-point CDP runtime verification suite checking for WebGL rendering, draw calls, countdown sequence, dock geometry, canvas freeze, determinism across scrubbing, and clean workdir.

5. **Universal Telemetry**:
   - Every run logs exact wall-clock duration, Time to First Token (TTFT), thinking/reasoning tokens, total output tokens, tool call counts, prompt cache hit ratios, and cryptographic SHA-256 integrity hashes.

---

## 🔬 Benchmark Directory

| Category | Benchmark | Domain | Specification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Ballistics** | **[Water Balloon](ballistics/water-balloon/)** | 3D Ballistics Physics & High-Speed Fluid Dynamics | [`prompt.md`](ballistics/water-balloon/prompt.md) | Active Cohort Testing |
| **Materials** | **[Prince Rupert's Drop](materials/prince-ruperts-drop/)** | Glass Fracture Mechanics & Supersonic Crack Propagation | [`prompt.md`](materials/prince-ruperts-drop/prompt.md) | Active Cohort Testing |

---

## 🛡️ Reproducibility Standard

Each benchmark test directory (e.g. [`ballistics/water-balloon/`](ballistics/water-balloon/), [`materials/prince-ruperts-drop/`](materials/prince-ruperts-drop/)) contains:
- `prompt.md`: Canonical, immutable prompt specification.
- `parameters.txt`: Ground-truth CLI execution flags per harness.
- `evaluate.py`: Automated 18-point verification suite.
- `TELEMETRY.md`: Comprehensive executive comparison matrix and compliance audit.
- `telemetry.json`: Machine-readable telemetry array.
- `CHECKSUMS.sha256`: Cryptographic signatures for all deliverables.

---

## 🏆 Latest Benchmark Deliverables

| Model | Developer Harness | Verification | Wall-Clock | Deliverable |
| :--- | :--- | :---: | :---: | :---: |
| **Gemini 4 Hydrogen (XHigh)** | Antigravity CLI | **PASS (100%)** | 644.4s | [`materials/prince-ruperts-drop/gemini-4-hydrogen/`](materials/prince-ruperts-drop/gemini-4-hydrogen/) |
| **Gemini 4 Carbon (High)** | Antigravity CLI | **PASS (100%)** | 1999.5s | [`materials/prince-ruperts-drop/gemini-4-carbon/`](materials/prince-ruperts-drop/gemini-4-carbon/) |
| **Gemini 4 Argon (High)** | Antigravity CLI | **PASS (100%)** | 997.9s | [`materials/prince-ruperts-drop/gemini-4-argon/`](materials/prince-ruperts-drop/gemini-4-argon/) |

*Showing the 3 most recent benchmark deliverables. See [`TELEMETRY.md`](materials/prince-ruperts-drop/TELEMETRY.md) for the complete multi-model leaderboard, full token metrics, cache ratios, and runtime verification logs.*
