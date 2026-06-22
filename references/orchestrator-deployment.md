---
name: orchestrator-deployment
description: >
  Orchestrator + Subagent deployment protocol for research automation.
  Defines task planning, context packaging, deployment, cross-validation,
  and cognition OS update workflow.
---

# Orchestrator Deployment Protocol

## When to Use

When you need to parallelize research tasks across subagents while maintaining
a single cognition OS as the source of truth.

## Core Principle

**You are the Orchestrator. You think, plan, verify, and update cognition OS.
Subagents execute. Their results are NOT trusted until cross-validated.**

## Task Categories & Verification Levels

| Category | Examples | Verification Level | Reliability |
|----------|----------|-------------------|-------------|
| Read + Synthesize | Literature review, assumption audit, summarization | Light (spot-check key claims) | High |
| Compute + Report | Error budget, statistical tests, data extraction | Medium (verify key numbers) | Medium |
| Compute + Interpret | Decomposition, contribution analysis, model comparison | Heavy (cross-validate conclusions) | Low-Medium |
| Derive + Prove | First-principles derivation, formula proof | DO NOT DELEGATE | N/A |

**Rule**: "Read + Synthesize" → reliable. "Compute + Interpret" → must cross-validate.
"Derive + Prove" → do yourself.

## Task Spec Template

```markdown
## Goal
[One sentence: what to produce]

## Context
[Key files with absolute paths, formulas, data paths, variable definitions]

## Method
[EXPLICIT analysis method: what to condition on, what to bin by, what to subtract.
 E.g., "Bin by S_hat (NOT by ML). Subtract theoretical mean DeltaC. Analyze residual."]
This prevents subagent from choosing a plausible-but-wrong method.

## What to Compute/Produce
[Numbered list of SPECIFIC deliverables with file paths]

## Output Format
[Structured format: tables, CSV, markdown sections]

## Sanity Checks
[Expected approximate values, known constraints, physical limits]

## MANDATORY: Output Files
[List of files that MUST be created. If not created, task is FAILED.]
```

**Critical addition from Round 2**: Always specify output files explicitly.
Subagent D failed because no output file was required in the spec.

## Context Packaging Rules

1. **Absolute paths only** — subagent has no session context
2. **Include formulas explicitly** — subagent won't derive them correctly
3. **Define all variables** — don't assume domain knowledge
4. **Provide sanity checks** — "sigma_pos should be ~1-3 pixels for S=20"
5. **Specify output file location** — so you can verify the file exists

## Deployment Workflow

1. Read cognition OS (AI_BRIEFING + relevant insights)
2. Identify parallelizable tasks from open questions
3. Write task specs with context + sanity checks
4. Deploy max 3 subagents in parallel
5. **Alternating deployment** (critical for throughput):
 As EACH subagent completes (not all), immediately:
 a. Cross-validate its result
 b. Update cognition OS
 c. Deploy a NEW subagent from the queue
 This means you always have up to 3 running, but the specific
 tasks rotate. Do NOT wait for all 3 to finish before deploying
 the next batch — that wastes time. Example timeline:
 - T0: deploy A, B, C
 - T1: A finishes → audit A → deploy D (B, C still running)
 - T2: B finishes → audit B → deploy E (C, D still running)
 This "交替发车" pattern maximizes throughput.
 
 **Important**: The user has explicitly asked for this alternating
 pattern. Do NOT fall into the trap of waiting for all 3 to complete
 before deploying the next batch. As soon as ONE finishes, audit
 it, update cognition OS, and immediately deploy the next task.
 The remaining 2 subagents continue running — you don't lose any
 parallelism, you just rotate which tasks are active.
   a. Check output file exists and is non-empty
   b. Cross-validate key claims against existing data
   c. Check formulas against first principles
   d. Compare with your expected result
   e. Update cognition OS with verified results
   f. Deploy next subagent if queue not empty
6. After all complete: write orchestrator experience

## Cross-Validation Checklist

For each subagent result, verify:

- [ ] Output file exists and has expected size
- [ ] Key numbers match known data (within tolerance)
- [ ] Formulas are correct (compare with first principles or known results)
- [ ] **Analysis method is correct** — did the subagent use the right conditioning variable? (e.g., bin by S_hat, NOT by ML; condition on observables, not derived statistics)
- [ ] **Library functions are verified** — never trust a helper function without round-trip test or external data cross-check. A single missing `/2` in gammaincc caused a 2x error in dC_thresh, making all downstream P(ML>=6) analyses wrong.
- [ ] No "dominant contribution" claims without quantitative comparison
- [ ] No inflation factors > 2x without physical justification
- [ ] No circular reasoning (result assumes what it proves)
- [ ] Consistency with existing insights (check I0xx references)

## Red Flags in Subagent Output

| Red Flag | Example | Action |
|----------|---------|--------|
| Large inflation factor | f^2 = 3.81 | Cross-validate with independent method |
| Unfamiliar scaling | 1/sqrt(S) instead of 1/S | Check against first principles |
| "Dominant contribution" | "optimizer explains 98%" | Verify with alternative decomposition |
| Perfect agreement | RMSE = 0.0000 | Suspect overfitting or error |
| Formula without derivation | sigma_pos = FWHM/sqrt(S) | Derive from first principles yourself |
| No output files produced | 100 API calls, 0 writes | Task too exploratory; restructure |
| Physics sign error | "corrected > uncorrected" | Re-derive from first principles |
| Many read_file, few write_file | 80/20 read/write ratio | Add explicit output requirements |
| Analysis uses derived stat for binning | Binning by ML instead of S_hat | **CRITICAL**: reject method; specify correct conditioning variable in task spec |

## Known Failure Modes (from I035 + Round 2 + Round 3)

1. **Plausible but wrong reasoning**: f^2=3.81 inflation (subagent #2, 2026-05-14)
2. **Formula errors**: sigma_pos = FWHM/sqrt(S) instead of sigma_PSF/S (subagent #5)
3. **Over-claiming**: "optimizer efficiency explains 98%" without cross-validation
4. **Circular reasoning**: α = c·c'/W_ref → W_ref = 1 (not subagent, but same pattern)
5. **Exploration without production**: subagent reads 100 files but produces no output (Subagent D, 2770s)
6. **Sign error in physics reasoning**: "S_limit_corrected > S_limit_uncorrected" when it should be < (Subagent F, corrected by Orchestrator)
7. **Wrong analysis method applied to correct data**: Subagent E analyzed ML=5-10 conditional distributions by truncating on ML range, producing plausible-looking but methodologically wrong results (skew from truncation, not intrinsic). The correct method is binning by S_hat (the observable), not by ML (the derived statistic). This is the most dangerous failure mode — the numbers are real, the method is wrong, so the conclusion seems solid. **Mitigation**: specify the analysis method explicitly in the task spec; if the subagent proposes ML-binning, reject it.
8. **Library function bug silently corrupts downstream analysis**: `lib/detml.py` had `gammaincc(a, delta_c)` instead of `gammaincc(a, delta_c/2)`, causing dC_thresh to be 2x too small. All P(ML>=6) calculations appeared correct (~1.0) because the threshold was trivially easy to exceed. The bug was only discovered when the Orchestrator manually verified the function against external benchmark data. **Mitigation**: always round-trip test critical functions; cross-check against known physical values; never trust a function you haven't verified against external data.
9. **Data extraction + analysis in same subagent**: When a subagent needs to (a) extract counts from event files AND (b) run MLE fitting, the extraction alone can consume all API calls/timeout budget. **Mitigation**: pre-extract all data into CSV/npz files BEFORE delegating, then delegate only the analysis step. The subagent should read pre-extracted data, not raw event files.
10. **Partial results on timeout are still valuable**: A subagent that times out may have produced figures/CSV files before the timeout. Always check the output directory for partial results before re-dispatching. **Mitigation**: require subagents to write output incrementally (save figures/data as they're created, not all at the end).

## Performance Benchmarks (from 8 deployments)

| Metric | Round 1 (5) | Round 2 (3) | Total |
|--------|-------------|-------------|-------|
| Average duration | 1294s | 2793s | 1883s |
| Average input tokens | 1.13M | 3.19M | 1.90M |
| Average output tokens | 14.8K | 16.4K | 15.4K |
| Average API calls | 20 | 68 | 38 |
| Completed with output | 4/5 (80%) | 2/3 (67%) | 6/8 (75%) |
| Formula/reasoning errors | 2/5 (40%) | 1/3 (33%) | 3/8 (38%) |
| Exploration-only (no output) | 0/5 (0%) | 1/3 (33%) | 1/8 (13%) |

### Key Round 2 Findings

- **Complex tasks take 2x longer**: D (2770s), E (2890s), F (2718s) vs Round 1 avg 1294s
- **Exploration trap**: Subagent D spent all 100 API calls reading files, never wrote analysis
- **Sign errors in physics**: Subagent F derived correct formula but wrong physical interpretation
| High-quality output when focused | Subagent E produced excellent non-Gaussianity analysis |
| **Pre-packaged context helps** | Subagent E had the best context (explicit data paths + formulas) |

### M104 CGM Session (2026-05-19): 7 subagents, 2 rounds

**Round 1** (3 subagents, all completed):
| Subagent | Goal | Duration | Result | Key Finding |
|----------|------|----------|--------|-------------|
| A | 5-band Poisson MLE kT map | ~15 min | ✅ Complete | R4-6 NE=0.680 (+1.6% vs v18), SE=0.780 (-3.7%) |
| B | Band ratio HR→kT map | ~15 min | ✅ Complete | **HR→kT unreliable**: SP contaminates H band 9× |
| C | Background systematics | ~5 min | ✅ Complete | |ΔkT|=0.007 keV (0.9%) between 3B/4.background |

**Round 2** (3 subagents, 2 completed + 1 partial):
| Subagent | Goal | Duration | Result | Key Finding |
|----------|------|----------|--------|-------------|
| D | Adaptive bin 5-band MLE | timeout | ❌ No output | Count extraction too slow; needs pre-extraction |
| E | Color-color diagram | timeout | ⚠️ Partial | 3 figures created; global C-C loses spatial info |
| F | Chandra 8-sector HR | ~20 min | ✅ Complete | **4.3σ**: N+NE cooler than S+SE at R4-6 |

**Key lessons**:
- **Pre-extract data**: Subagent D failed because count extraction + MLE in one
  subagent exceeded timeout. Pre-extract counts to CSV/npz, THEN delegate analysis.
- **Partial results are valuable**: Subagent E timed out but produced 3 usable
  figures. Always check for partial output before re-dispatching.
- **Pure-numpy > CIAO/Sherpa**: Subagent C (numpy+pandas) finished in ~5 min;
  CIAO-dependent tasks take 3-5× longer.
- **Divergent parallel goals**: The triad (MLE / HR / background) had independent
  goals. If one fails, the others still produce unique value.
- **Rolling deployment works**: After C completed fast, audited + deployed F
  while A/B were still running. No wasted time.

## Cognition OS Update Protocol

After each subagent completes:

1. Create insight (I0xx) with: Statement, Evidence, Confidence, Dependencies
2. Update AI_BRIEFING: add to "Currently trusted" or "Currently questioned"
3. Update session log: add to "Did", "Found", "Next"
4. If subagent result was wrong: add correction to the insight + reference the correction
5. If new open question emerged: add to "Open questions" in AI_BRIEFING

**Key principle**: The cognition OS is the SINGLE SOURCE OF TRUTH.
Every subagent result must be written back to cognition OS before
deploying the next subagent. This ensures that downstream tasks
always have the latest verified state. The user treats cognition OS
updates as MANDATORY — skipping them means the next subagent works
with stale context.

**Also update wiki** (`~/wiki/`) when the subagent discovers a new
technique, pitfall, or domain knowledge that would benefit future
sessions beyond the current project.

## Session Continuity: Resuming Past Work

When a user says "resume that session", "continue from where we left off",
or references a past session by name/topic, Hermes has no native session-resume
feature. Instead, reconstruct project state from multiple sources:

### Reconstruction Sequence (in order of cost)

| Step | Source | Tool | What to Extract |
|------|--------|------|-----------------|
| 1 | Past session | `session_search(query)` | Session summary, key decisions, unresolved items |
| 2 | Persistent memory | Auto-injected | User preferences, project facts, conventions |
| 3 | Filesystem state | `terminal` + `search_files` + `read_file` | What files exist, what's been completed, latest timestamps |
| 4 | Plan files | `read_file` on `.hermes/plans/*.md` | Project plan, phase status, pending tasks |
| 5 | Cognition OS | `read_file` on project AI_BRIEFING | Current beliefs, open questions, confidence levels |

### Key Principle

**Trust filesystem state over session summaries.** Session summaries describe
intentions; filesystem shows what actually happened. A session summary may say
"8-sector fitting planned" but the fitting directory shows only 2-sector results
exist — the plan wasn't executed yet.

### Monitoring Unfinished Work

If the blocking task is running in another session/terminal (not in current
Hermes context), set up a cronjob to monitor for output files:

```
cronjob(action='create', schedule='every 30m', prompt='Check if <expected files> exist...')
```

The cronjob should:
- Check for specific output file patterns (e.g., `*Angle[0-7]*_model_parameters.txt`)
- Count progress (e.g., "12/24 regions completed")
- Report ONLY when new results appear (silent otherwise)
- Deliver to current thread so the user can continue here

### What to Tell the User

After reconstruction, present a concise status table:
- What's done (with evidence: file counts, timestamps)
- What's pending (with blockers if known)
- What you've set up to monitor (cronjob details)

This replaces the impossible "session resume" with a verifiable state reconstruction.

## Cross-Session State Investigation

When the user asks "what is that other session doing?" or "does session X have
a plan for Y?", you need to reconstruct ANOTHER session's state — not resume
your own. This is a distinct pattern from session resumption.

### Use Cases

- User has a CLI session and a Discord session running in parallel
- Cron jobs are monitoring long-running tasks
- User wants to know if another session already planned/started a specific task
- Avoiding duplicate work across concurrent sessions

### Investigation Protocol (5 layers, low to high cost)

| Layer | Method | What It Reveals | Cost |
|-------|--------|-----------------|------|
| 1 | `session_search(query)` with OR terms | Session titles, summaries, timestamps | Free |
| 2 | Cognition OS files (`00_AI_BRIEFING.md`, `02_CURRENT_QUESTION.md`, `stages/Sxx.md`) | Current beliefs, open questions, stage status | Low (3-5 read_file) |
| 3 | Plan files (`<project>/.hermes/plans/*.md`) | Detailed phase plans, task breakdowns | Low |
| 4 | Filesystem state (output directories, result files) | What actually exists vs what was planned | Medium |
| 5 | Raw session JSON parsing (`~/.hermes/sessions/session_*.json`) | Todo lists, delegate_task results, tool outputs | High |

### Layer 5: Raw Session JSON Parsing

When `session_search` summaries are truncated or missing key detail, read the
raw session JSON directly. Key extraction patterns:

```python
import json
with open(session_path) as f:
    data = json.load(f)
msgs = data.get('messages', [])

# Extract todo lists (from tool responses containing "todos")
for msg in msgs:
    content = str(msg.get('content', ''))
    if '"todos"' in content and '"status"' in content:
        parsed = json.loads(content)
        for todo in parsed.get('todos', []):
            print(f"{todo['id']}: {todo['content']} [{todo['status']}]")

# Extract delegate_task results (from tool responses containing "results")
for msg in msgs:
    content = str(msg.get('content', ''))
    if '"results"' in content and '"summary"' in content:
        parsed = json.loads(content)
        for r in parsed.get('results', []):
            print(r.get('summary', '')[:500])
```

### Pitfalls

- **session_search uses FTS5 default AND** — use OR between keywords for broad
  recall: `session_search(query="M104 OR spectrum OR extraction")`
- **Multiple sessions share the same initial prompt** — Hermes resumes sessions
  by re-injecting the original user message. Many sessions start with identical
  text. Distinguish them by checking message count, last-active timestamp, and
  the assistant's unique response content.
- **Todo status may be stale** — a todo item may show `in_progress` even after
  the blocking issue was resolved by a subagent. Always cross-check with
  filesystem state (do the output files exist?).
- **Cron sessions are lightweight** — cron session JSONs are small (monitoring
  only). For the full plan, find the parent CLI session that created the cron.
- **Session JSON files can be large** (500KB+) — don't read the full content
  into context. Use `execute_code` + Python to extract only the fields you need.

### Worked Example

For a concrete cross-session investigation (XARTATOMS M104 project, checking
whether a CLI session had spectrum extraction plans), see
`references/cross-session-investigation-xartatoms-example.md`.

## Optimization: Pre-package Context

To reduce file-reading overhead (60-80% of API calls):

1. Create a `context/` directory with pre-extracted key information
2. For each task type, maintain a context bundle:
   - Key formulas (copy from theory/)
   - Key data summary (copy from results/)
   - Key insights (copy from cognition OS)
3. Subagent reads 1-2 files instead of 15+

## Subagent Configuration

```yaml
delegation:
  child_timeout_seconds: 14400  # 4 hours
  max_spawn_depth: 2
  max_concurrent_children: 3
```

Toolsets: ["terminal", "file"] for most tasks. Add "web" if web search needed.