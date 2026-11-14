# Benchmark Protocol & Changelog

This file records which version of the execution protocol produced each set of results, what changed between versions, and why. Results are only directly comparable when they were produced under the same protocol version.

| Version | Name | Status | Applies to |
| :--- | :--- | :--- | :--- |
| **v1.0** | Shared-Host Seatbelt | Retired | [`ballistics/water-balloon`](ballistics/water-balloon/), [`materials/prince-ruperts-drop`](materials/prince-ruperts-drop/) (runs from 2026-11-11 to 2026-11-14) |
| **v1.1** | Shared-Host Seatbelt, all harnesses enforced | Current | [`vehicle-dynamics/f1-night-duel`](vehicle-dynamics/f1-night-duel/) (introduced in stages during the first round; see below) |
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

v1.1 was introduced during the first F1 Night Duel round on 2026-11-14. Its changes were made in three stages as each gap was found, so the table at the end of this section lists the conditions each run actually had.

**Every harness**

- **Same boundary.** Every harness runs inside the same Seatbelt profile and uses its own built-in sandbox switched off (`--dangerously-skip-permissions`, `--dangerously-bypass-approvals-and-sandbox`, `danger-full-access`).
- **Clean, login-only home per run.** Each harness gets a home or config folder that contains only its login credentials and base configuration. It has no past sessions, conversations, history, memory, plans, attachments, caches or user instructions. The host's real state folders (`~/.claude`, `~/.codex`, `~/.gemini`, `~/.kimi`, `~/.kimi-code`, `~/.dsh`, `~/.minimax`) are unreadable from inside a run.
  - Codex CLI, Kimi Code, DeepSeek Harness and Antigravity CLI receive a fresh copy of their login in the run's own folder.
  - Claude Code and MiniMax Code tie their login to a fixed folder, so each uses a dedicated benchmark-only folder (`~/.pcd-harness/claude`, `~/.pcd-harness/minimax`). It was signed in once, and everything in it except the login is deleted before every run.
- **No web tools.** Web search and web fetch tools are disabled for every harness, by flag or configuration, and checked with a test call. The one exception is below.
- **Private temporary folder.** Each run has its own temporary folder. The shared `/private/tmp/claude-*` area is no longer reachable from any run.
- **No extra tool catalogues.** Account-level connectors (Claude Code) and cloud connector tools (MiniMax Code) are disabled, because other harnesses have no equivalent.
- **Same stop rule.** A run ends when the agent exits or after the 2-hour timeout. An Antigravity-only rule that stopped runs after 6 minutes without file changes was removed; it had never triggered.
- **Same version per round.** Within a round, every model on the same harness uses the identical harness version, which is checked before each run (for example, Codex CLI 0.169.0 for all Codex models in F1 Night Duel). Auto-update is disabled during runs where the harness supports it.
- **One run at a time.** Benchmark runs never overlap. Short sandboxed setup tests (under two minutes each) ran alongside some runs while these changes were being made.

**Known exception: Antigravity web search.** Antigravity CLI's `search_web` tool runs on Google's side and could not be disabled by any available setting. Gemini runs therefore have search available. To keep this auditable, each Gemini run's full step-by-step transcript is appended to its `raw_output.json`, and every `search_web` call is counted and noted in the run's commit message.

**F1 Night Duel round, conditions per run**

| Run | Started (UTC) | Conditions |
| :--- | :--- | :--- |
| Codex GPT 6.1 Terra | 06:31 | Stage A. Codex isolation unchanged from v1.0 (fresh login-only home, web search off). The shared Claude temp area was still reachable. |
| DeepSeek v4.1 Flash | 12:52 | Stage A. First sandboxed DeepSeek run with a fresh home. Its web tools were still available; the log shows no web calls. |
| Codex GPT 6.1 Sol, Codex GPT 6 Astra | 13:50, 14:32 | Stage A, as Terra. |
| Kimi Code K3.1 Pro | 15:30 | Stage B. Clean homes and web tools off for Kimi, DeepSeek and Antigravity. The shared Claude temp area was still reachable. |
| Gemini 4 Hydrogen, Gemini 4 Argon | 16:38, 16:53 | Stage B. Transcript appended; `search_web` calls: 0 and 0. |
| All later runs | from 17:03 | Stage C. Full v1.1 as described above. |

Still shared with v1.0: one machine and one user account. Agents can still list and stop other processes on the machine. That is addressed in v2.0.

---

## v2.0: Isolated, one run per environment (planned)

Goal: every run is physically or virtually separated, so no run can observe or affect another.

- Each run executes in its **own virtual machine or dedicated macOS user account**, reset between runs.
- **No parallel runs on a shared host.** Parallelism only across fully separate environments.
- Each run gets a **private temporary folder**; nothing temporary is shared between runs.
- Agents **cannot list, signal or stop processes** outside their own run.
- Published raw logs are checked for **host-specific details**, such as installed apps and user paths, before release.
- Each `metrics.json` records the **protocol version** it was produced under.
