# Benchmark Protocol & Changelog

This file records which version of the execution protocol produced each set of results, what changed between versions, and why. Results are only directly comparable when they were produced under the same protocol version.

| Version | Name | Status | Applies to |
| :--- | :--- | :--- | :--- |
| **v1.0** | Shared-Host Seatbelt | Retired | [`ballistics/water-balloon`](ballistics/water-balloon/), [`materials/prince-ruperts-drop`](materials/prince-ruperts-drop/) (runs from 2026-11-11 to 2026-11-14) |
| **v1.1** | Shared-Host Seatbelt, all harnesses enforced | Current | [`vehicle-dynamics/f1-night-duel`](vehicle-dynamics/f1-night-duel/) |
| **v2.0** | Isolated, one run per environment | Planned | Future benchmarks |

---

## v1.0: Shared-Host Seatbelt

**How runs were executed**

- Every run started stateless, received a byte-identical prompt, and had exactly one attempt with no human intervention (Pass@1).
- Each harness ran under a macOS Seatbelt (`sandbox-exec`) profile. The profile blocked file reads and writes to the repository, other runs' scratch folders and personal folders, and confined writes to the run's own scratch folder.
- All runs shared one physical Mac and one user account. To save time, several runs were often executed **in parallel**.

**What we found** (review of all published raw logs, 2026-11-14)

The Seatbelt profile controlled *files*, but not *processes* or some *shared temporary space*. Because runs shared one machine and one user account, they were not fully separated from each other:

1. **One harness was not sandboxed.** The orchestrator exempted the DeepSeek Harness from `sandbox-exec`, because its own built-in sandbox cannot run inside another one. A run made with it outside the orchestrator worked directly inside the repository. That run was never published, and it has been removed from the repository history.
2. **Runs could see and stop each other's processes.** Agents can list every process on the machine, with full command lines, and can stop any process owned by the same user. In practice:
   - One run listed processes and saw another agent rendering its own deliverable from inside the repository. It did not open or use that file.
   - The same run stopped a browser process it had not started, assuming it was left over. We could not determine whose process it was.
   - One run stopped *every* headless browser on the machine (`pkill -f "firefox --headless"`). No other recorded run was active at those moments, but this command can interrupt another run's self-testing.
3. **Overlapping runs.** In v1.0, 11 pairs of recorded runs overlapped in time, by 1 to 33 minutes each. Overlapping runs shared the CPU, GPU and network, which can affect wall-clock time, and they shared the risks above.
4. **A shared temporary folder stayed open.** One temporary folder (`/private/tmp/claude-*`) had to stay readable and writable for Claude Code to work. It is shared by every Claude Code session on the machine, sandboxed or not. We found no run that read another run's files there.
5. **Host details in public logs.** Agents commonly inspect their environment, such as installed applications and browser caches. These details are now part of the published raw logs.

**Impact on published results**

- We found **no evidence that any published deliverable used another model's output**. Every published v1.0 deliverable was produced inside its own sandbox and passed the same automated verification.
- Overlapping runs make **wall-clock times less reliable** as a measure of speed. Treat v1.0 durations as approximate.
- v1.0 results remain published unchanged, with this note, so the record stays complete and verifiable against its checksums.

---

## v1.1: Shared-Host Seatbelt, all harnesses enforced (current)

Changes from v1.0, applied 2026-11-14:

- **Every harness now runs inside the same Seatbelt profile.** The DeepSeek Harness runs with its built-in sandbox switched off and the outer profile as the boundary. This matches how the Claude Code, Codex CLI and Antigravity CLI runs are configured.
- **The DeepSeek Harness gets a fresh, empty home folder per run.** It receives only login credentials and its base configuration, with no past sessions, attachments, cache or user instructions. This matches how Codex CLI and Kimi Code are isolated.
- **The real DeepSeek Harness state folder is unreadable from inside a run**, like the Codex and Kimi folders.
- **Runs are executed one at a time.**

Still shared with v1.0: one machine and one user account, so process visibility and the shared Claude Code temporary folder remain. These are addressed in v2.0.

---

## v2.0: Isolated, one run per environment (planned)

Goal: every run is physically or virtually separated, so no run can observe or affect another.

- Each run executes in its **own virtual machine or dedicated macOS user account**, reset between runs.
- **No parallel runs on a shared host.** Parallelism only across fully separate environments.
- Each run gets a **private temporary folder**; nothing temporary is shared between runs.
- Agents **cannot list, signal or stop processes** outside their own run.
- Published raw logs are checked for **host-specific details**, such as installed apps and user paths, before release.
- Each `metrics.json` records the **protocol version** it was produced under.
