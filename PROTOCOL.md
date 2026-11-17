# Benchmark Protocol & Changelog

This file records which version of the execution protocol produced each set of results, what changed between versions, and why. Results are only directly comparable when they were produced under the same protocol version.

| Version | Name | Status | Applies to |
| :--- | :--- | :--- | :--- |
| **v1.0** | Shared-Host Seatbelt | Retired | [`ballistics/water-balloon`](ballistics/water-balloon/), [`materials/prince-ruperts-drop`](materials/prince-ruperts-drop/): runs started before 2026-11-14 06:31 UTC (12 and 11 published rows) |
| **v1.1** | Shared-Host Seatbelt, all harnesses enforced | Current | [`vehicle-dynamics/f1-night-duel`](vehicle-dynamics/f1-night-duel/) (introduced in stages during the first round; see below), plus every water-balloon and prince-ruperts-drop run started on or after 2026-11-14 06:31 UTC (5 and 4 rows) |
| **v2.0** | Isolated, one run per environment | Planned | Future benchmarks |

**Mixed tables.** Water Balloon and Prince Rupert's Drop therefore contain both v1.0 and v1.1 rows. Each row's `protocol_version` is recorded in `telemetry.json` (backfilled 2026-11-17 from `started_at`; the v1.0/v1.1 boundary is the start of the first F1 run). Compare only rows with the same `protocol_version`, and read wall-clock across versions as approximate. The v1.0 rows have not been re-run under v1.1.

**Known confounds inside a benchmark** (not protocol differences, but they limit head-to-head reading):

- *Reasoning effort differs by model.* Gemini 4 Argon/Carbon and ERNIE ran at High; Gemini 4 Hydrogen and Qwen 4 Max (OpenCode) at XHigh; all others at Max. Effort is recorded per row (`reasoning_effort`).
- *Harness versions differ within a benchmark* for rows produced before the "same version per round" rule: Water Balloon has Claude Code 2.1.322 and 2.1.325, Codex CLI 0.167.1 and 0.169.0, Antigravity CLI 1.5.6 and 1.5.7; Prince Rupert's Drop has Codex CLI 0.167.1 and 0.168.0. Versions are recorded per row (`harness_version`).
- *Telemetry columns are only comparable within one harness.* Harnesses count turns, uncached input and cache reads differently (e.g. Kimi Code reports 2 turns; MiniMax Code reports none).
- *The grader checks the page and player, not the scene.* All 18 checks cover structure, countdown, dock, determinism, network and errors; none verifies scene content (for F1: car colours, finish margin, exposure limits, DRS). 100% means "meets the shell contract". Scene quality is judged by review.
- *One run per model per benchmark.* Run-to-run variance is not measured.

---

## v1.0: Shared-Host Seatbelt

**How runs were executed**

- Every run started stateless and received a byte-identical prompt, with no human intervention during the run.
- **Attempt policy: first passing attempt.** Attempts that failed were re-run, and only a passing attempt was published. Some failures came from the isolation setup itself while it was being adjusted, not from the model.
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

v1.1 was introduced during the first F1 Night Duel round on 2026-11-14. Its changes were made in three stages as each gap was found, so the table at the end of this section lists the conditions each run actually had. Runs from the earlier stages were kept rather than re-run: the remaining differences (a reachable shared temporary folder, and web tools available to one harness) were not used by any run, as the logs show. Every later round starts on the full v1.1 setup from its first run.

**Every harness**

- **Same boundary.** Every harness runs inside the same Seatbelt profile and uses its own built-in sandbox switched off (`--dangerously-skip-permissions`, `--dangerously-bypass-approvals-and-sandbox`, `danger-full-access`).
- **Clean, login-only home per run.** Each harness gets a home or config folder that contains only its login credentials and base configuration. It has no past sessions, conversations, history, memory, plans, attachments, caches or user instructions. The host's real state folders (`~/.claude`, `~/.codex`, `~/.gemini`, `~/.kimi`, `~/.kimi-code`, `~/.dsh`, `~/.minimax`) are unreadable from inside a run.
  - Codex CLI, Kimi Code, DeepSeek Harness and Antigravity CLI receive a fresh copy of their login in the run's own folder.
  - Claude Code and MiniMax Code tie their login to a fixed folder, so each uses a dedicated benchmark-only folder (`~/.pcd-harness/claude`, `~/.pcd-harness/minimax`). It was signed in once, and everything in it except the login is deleted before every run.
- **No web tools.** Web search and web fetch tools are disabled for every harness, by flag or configuration, and checked with a test call. The one exception is below.
- **Private temporary folder.** Each run has its own temporary folder. The shared `/private/tmp/claude-*` area is no longer reachable from any run.
- **No extra tool catalogues.** Account-level connectors (Claude Code) and cloud connector tools (MiniMax Code) are disabled, because other harnesses have no equivalent.
- **Same stop rule, no time limit.** A run ends only when the agent exits. Runs up to and including Claude Fable 5.2 had a 2-hour timeout; it never triggered (the longest run took 96 minutes), and it was removed for all later runs. An Antigravity-only rule that stopped runs after 6 minutes without file changes was also removed; it had never triggered.
- **Same version per round.** Within a round, every model on the same harness uses the identical harness version, which is checked before each run (for example, Codex CLI 0.169.0 for all Codex models in F1 Night Duel). Auto-update is disabled during runs where the harness supports it.
- **Attempt policy: first passing attempt (unchanged).** Failed attempts are archived outside the repository and the model is re-run; only the first passing attempt is published.
- **One run at a time.** Benchmark runs never overlap. Short sandboxed setup tests (under two minutes each) ran alongside some runs while these changes were being made.

**Known exception: Antigravity web search.** Antigravity CLI's `search_web` tool runs on Google's side and could not be disabled by any available setting. Gemini runs therefore have search available. To keep this auditable, each Gemini run's full step-by-step transcript is appended to its `raw_output.json`, and every `search_web` call is counted and noted in the run's commit message.

**Attempts are recorded from v1.1 on, with gaps.** The table below has "not recorded" for runs whose attempt count was not written down when they were published; going forward, record the count in each run's commit message and in `metrics.json`. Every attempt on a benchmark's final prompt is counted, including ones that failed or were discarded because of the setup, and the table below lists how many attempts each published result took. v1.0 did not record failed attempts, so v1.0 results have no attempt count.

**F1 Night Duel round, conditions and attempts per published run**

| Run | Started (UTC) | Attempts | Conditions |
| :--- | :--- | :---: | :--- |
| Codex GPT 6.1 Terra | 06:31 | 1 | Stage A. Codex isolation unchanged from v1.0 (fresh login-only home, web search off). The shared Claude temp area was still reachable. An earlier run used a draft of the prompt and is not counted. |
| DeepSeek v4.1 Flash | 12:52 | 2 | Stage A. First sandboxed DeepSeek run with a fresh home. Its web tools were still available; the log shows no web calls. Attempt 1 was discarded because the orchestrator had run DeepSeek without the sandbox. |
| Codex GPT 6.1 Sol, Codex GPT 6 Astra | 13:50, 14:32 | 1, 1 | Stage A, as Terra. |
| Kimi Code K3.1 Pro | 15:30 | 2 | Stage B. Clean homes and web tools off for Kimi, DeepSeek and Antigravity. The shared Claude temp area was still reachable. Attempt 1 was cut off when the orchestrating session ended. |
| Gemini 4 Argon | 16:53 | 1 | Stage B. Transcript appended; `search_web` calls: 0. |
| Gemini 4 Carbon | 17:18 | 1 | Stage C, full v1.1. `search_web` calls: 0. |
| Claude Fable 5.1 | 18:07 | not recorded | Stage C, full v1.1. |
| Claude Fable 5.2 | 19:09 | not recorded | Stage C. Longest run before the timeout was removed (96 min; never triggered). |
| Gemini 4 Hydrogen | 21:55 | 2 | Stage C. Attempt 1 (16:38, Stage B) failed verification: a page error stopped playback. Attempt 2 published. |
| MiniMax M3.1 Flash | 23:42 | not recorded | Stage C. |
| Claude Haiku 5.5, Claude Opus 5.5, Claude Sonnet 5.5, ERNIE 5.5 Flash Preview, Qwen 4 Max | 01:56, 04:10, 05:34, 08:53, 20:45 | not recorded | Full v1.1. Published after this table was last updated; attempt counts were not written down at the time and cannot be reconstructed from the repository. |

Still shared with v1.0: one machine and one user account. Agents can still list and stop other processes on the machine. That is addressed in v2.0.

---

## v2.0: Isolated, one run per environment (planned)

Goal: every run is physically or virtually separated, so no run can observe or affect another.

- Each run executes in its **own virtual machine or dedicated macOS user account**, reset between runs.
- **No parallel runs on a shared host.** Parallelism only across fully separate environments.
- Each run gets a **private temporary folder**; nothing temporary is shared between runs.
- Agents **cannot list, signal or stop processes** outside their own run.
- Published raw logs are checked for **host-specific details**, such as installed apps and user paths, before release.
- **Attempt policy: single attempt.** Each model gets exactly one attempt per round, and that attempt is published whether it passes or fails.
- Each `metrics.json` records the **protocol version** it was produced under.
