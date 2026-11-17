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

2. **Full Coding Toolset, Level Playing Field**:
   - Each harness runs with its standard coding tools: file creation, multi-pass editing, inspection, and terminal execution.
   - Tools that only some harnesses offer are switched off for all of them: web search and web fetch, account-linked connectors, and cloud tool catalogues. Where a tool cannot be switched off, it is noted and audited (see [`PROTOCOL.md`](PROTOCOL.md)).
   - This measures how effectively each agent plans, implements, inspects, and refines code on its own.

3. **Zero-Intervention Attempts**:
   - Each attempt receives exactly one prompt.
   - No human in the loop: no follow-up corrections, no hints, and no relayed error messages.
   - The agent works until it declares completion on its own.
   - **Current policy (protocol v1.x): first passing attempt.** The published result is the model's first attempt that passes verification. While the isolation setup was still being developed, some attempts failed for reasons that had nothing to do with the model, such as sandbox restrictions that blocked a harness. For that reason, failed attempts are re-run rather than published.
   - **Attempts are recorded from protocol v1.1 on.** [`PROTOCOL.md`](PROTOCOL.md) lists how many attempts each published v1.1 result took. Protocol v1.0, used for the first two benchmarks, did not record failed attempts.
   - **Planned (protocol v2.0): single attempt.** Once the setup is final, each model gets exactly one attempt, and that attempt is published whether it passes or fails.

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
| **Vehicle Dynamics** | **[F1 Night Duel](vehicle-dynamics/f1-night-duel/)** | Spline-Track Night Race, F1 Car Detail & Synthesized SFX | [`prompt.md`](vehicle-dynamics/f1-night-duel/prompt.md) | Active Cohort Testing (Protocol v1.1) |

---

## 🛡️ Reproducibility Standard

> **Protocol versions:** results are only directly comparable within one protocol version. See [`PROTOCOL.md`](PROTOCOL.md) for the version history and lessons learned from running benchmarks in parallel on a shared host.

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
| **Claude Sonnet 5.5 (Max)** | Claude Code | **PASS (100%)** | 4205.5s | [`ballistics/water-balloon/claude-sonnet-5.5/`](ballistics/water-balloon/claude-sonnet-5.5/) |
| **Qwen 4 Max (Max)** | Qwen Code | **PASS (100%)** | 2833.9s | [`ballistics/water-balloon/qwen-4-max/`](ballistics/water-balloon/qwen-4-max/) |
| **Codex GPT 6.1 Terra (Max)** | Codex CLI | **PASS (100%)** | 858.8s | [`ballistics/water-balloon/codex-gpt-6.1-terra/`](ballistics/water-balloon/codex-gpt-6.1-terra/) |

*Showing the 3 most recent benchmark deliverables. See [`TELEMETRY.md`](ballistics/water-balloon/TELEMETRY.md) for the complete multi-model leaderboard, full token metrics, cache ratios, and runtime verification logs.*
