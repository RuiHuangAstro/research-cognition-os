# Orchestrator + Subagent Research Workflow

Tested: 2026-05-14 on DET_ML_Uncertainty project (5 subagent deployments, 3 parallel).

## Architecture

```
You (orchestrator) → maintain cognition OS + plan DAG
 ├── delegate_task → subagent executes analysis
 │ ├── Mode A: Read + synthesize (100-300s, HIGH reliability)
 │ ├── Mode B: Compute + interpret (1000-3000s, NEEDS verification)
 │ └── Mode C: Derive + prove (NOT suitable for subagents)
 └── Background terminal → long simulations (unlimited time)
```

## Task Type → Reliability Mapping

| Task Type | Example | Reliability | Verification Needed |
|-----------|---------|-------------|---------------------|
| Read + synthesize | Audit assumptions, write procedure | HIGH | Spot-check key claims |
| Compute + interpret | Error budget, decomposition | MEDIUM | Cross-validate formulas + numbers |
| Derive + prove | First-principles derivation | LOW | Do NOT delegate — circular reasoning risk |

**Rule**: Delegate "what to find" and "how to organize", NOT "what to conclude".

## Subagent Capabilities

| Capability | Status | Notes |
|-----------|--------|-------|
| File read/write | ✅ | cognition OS, wiki, results, code |
| Python execution | ✅ | numpy, scipy, pandas available |
| Conversation context | ❌ | Must pass ALL info via `context` parameter |
| Skill auto-loading | ❌ | Must explicitly instruct to read key files |
| `clarify` (ask user) | ❌ | Leaf subagents cannot ask questions |
| `memory` (persistent) | ❌ | Only orchestrator can save memories |
| `delegate_task` | ❌ (leaf) / ✅ (orchestrator) | max_spawn_depth=2 allows nesting |

## Context Parameter Best Practices

The `context` parameter is the ONLY way to convey information to a subagent. It must include:

1. **Data paths** with explicit file formats and key column/array names
2. **Variable definitions** (what each column/array means, units, conventions)
3. **Formulas** with conventions (e.g., "SAS convention: ML = -log(gammaincc(2.5, DeltaC/2))")
4. **Known pitfalls** (e.g., "exp(-ML) underflows for ML > 50")
5. **Expected answer or sanity check** (e.g., "RMSE should be ~0.045 based on prior analysis")
6. **Output format** (structured, verifiable — e.g., "CSV with columns X, Y, Z")
7. **Language preference** (e.g., "Chinese for natural language, English for technical terms")

Example minimal context:
```
Project: DET_ML_Uncertainty at ~/program/DET_ML_Uncertainty/

Data file: results/cash_components_S20_b0.1.npz
  Keys: S_hat(5000,), x_hat(5000,), y_hat(5000,), DET_ML(5000,)
  center = 15 (grid is 31x31)

Model: k = 1/sqrt(1 + alpha * r^2 * W), alpha=0.325
ML convention: SAS shape=2.5 for 3-param
WARNING: exp(-ML) underflows for ML > 50

Expected: RMSE ~ 0.045, bias < 0.01
Output: CSV with columns Source, Magnitude, Direction, Confidence
```

## Deployment Statistics (Round 1)

| # | Task | Type | Duration | API Calls | Tokens (in/out) | Quality |
|---|------|------|----------|-----------|-----------------|---------|
| 1 | Read AI_BRIEFING + summarize | A | 134s | ~8 | small | Good |
| 2 | c' decomposition analysis | B | 2249s | 31 | 1.83M/24.8K | **Partially wrong** |
| 3 | Theory assumption audit | A | 1175s | 24 | 1.14M/7.5K | Excellent |
| 4 | Error budget decomposition | B | 1684s | 20 | 0.67M/16.6K | Excellent |
| 5 | Catalog application procedure | A | 1226s | 17 | 0.89M/10.1K | Good (formula error) |

Averages: 1294s, 1.13M input tokens, 14.8K output tokens.
60-80% of API calls are `read_file` — pre-packaging context can reduce this.

## Cross-Validation Protocol (MANDATORY)

After subagent returns results, perform these checks BEFORE recording as insight:

### Level 1: Formula Check (5 min)
- Every formula in subagent output must be checked against first principles or data
- Pay special attention to scaling relations (1/S vs 1/sqrt(S), linear vs quadratic)
- **Red flag**: unfamiliar scaling or large inflation factors (>3x) without physical justification

### Level 2: Number Check (10 min)
- Re-run the analysis script if subagent created one
- Verify key numbers against independent data
- Check that subagent's "dominant contribution" claims have quantitative comparison

### Level 3: Logic Check (5 min)
- If subagent claims "X causes Y", test what happens when X is removed
- Check for circular reasoning (subagent derives result that assumes the conclusion)
- Verify physical assumptions (e.g., "position error inflates variance" vs "position error is a consequence")

### Case Study 1: f² Inflation Error (Subagent #2)

Subagent analyzed position errors and concluded:
> "RMS_pos / sigma_Fisher = 1.95, so c' is inflated by f² = 3.81 (98% of excess)"

Cross-validation: replaced Fisher sigma_pos with 2x actual sigma_pos in the winginess model → RMSE worsened by 2.6x. The f²=3.81 logic was wrong.

Root cause: Position error (RMS_pos) is a CONSEQUENCE of optimizer inefficiency (finding local maxima), not a noise inflation. The winginess model correctly uses Fisher sigma_pos because compression depends on the search range (set by Fisher information), not on the position precision.

Lesson: Subagent's reasoning was internally consistent but based on a wrong physical assumption.

### Case Study 2: sigma_pos Formula Error (Subagent #5)

Subagent wrote: `sigma_pos ≈ FWHM / sqrt(S)` which is incorrect.
Correct: `sigma_pos ≈ sigma_PSF / S` (1/S scaling from Fisher information, not 1/sqrt(S)).

Root cause: Subagent confused the scaling of position uncertainty with that of flux uncertainty. Position uncertainty scales as 1/S (Fisher information), while flux uncertainty scales as 1/sqrt(S) (Poisson statistics).

Lesson: Formula errors are the most common subagent failure mode. Always cross-check scaling relations.

## Red Flags in Subagent Output

- **"Dominant contribution" without quantitative comparison** → VERIFY with independent method
- **Unfamiliar scaling** (e.g., 1/sqrt(S) instead of 1/S) → CHECK against first principles
- **Large inflation factors (>3x)** without physical justification → CROSS-VALIDATE
- **Results that seem "too clean"** (exact integers, perfect agreement) → SUSPECT
- **Circular reasoning** (result assumes what it's trying to prove) → REJECT

## child_timeout Tuning

```bash
# Check current value
grep child_timeout ~/.hermes/config.yaml

# Increase for research tasks
hermes config set delegation.child_timeout_seconds 14400  # 4 hours
```

Empirical timing:
- Simple read + summarize: 134s
- Data analysis with Python: 1000-2300s
- Token consumption: ~0.7-1.8M input + ~8-25K output

## Orchestrator Workflow

```
1. Read cognition OS (AI_BRIEFING + relevant insights)
2. Identify open questions that can be parallelized
3. Write detailed task specs with:
   a. Goal (what to produce)
   b. Context (key files, formulas, data paths, variable definitions)
   c. Expected answer / sanity check (for audit)
   d. Output format (structured, verifiable)
4. Deploy subagents (max 3 parallel)
5. As each completes:
   a. Level 1: Formula check
   b. Level 2: Number check (re-run script)
   c. Level 3: Logic check
   d. Update cognition OS with VERIFIED results only
   e. Deploy next subagent if needed
6. After all complete: write orchestrator experience insight
```

## Context Optimization

Subagents spend 60-80% of API calls reading project files. To reduce overhead:

1. **Pre-package key context** as a single summary file (reduce 15 read_file calls to 1-2)
2. **Include formulas directly** in context (don't make subagent derive them)
3. **Specify column names and units** (don't make subagent discover them)
4. **Set language preference** explicitly in every task

## Deployment Statistics (Round 2 — M104 CGM)

| # | Task | Type | Duration | Quality | Key Finding |
|---|------|------|----------|---------|-------------|
| 1 | v18 profile parameter extraction | B | ~300s | Good | 66/67 regions bg frozen; gradient is outer-hotter |
| 2 | Plan B v4 MCMC convergence fix | B | ~600s | Good | R-hat<1.005, but kT systematically low by ~0.15 keV |
| 3 | Band ratio map framework | B | ~400s | Partial | Event file PI filtering fails (H band 92% bg) |
| 4 | Fitting strategy comparison | B | ~500s | Partial | Code analysis done, but script NOT written (hit iteration limit) |
| 5 | Band ratio from PHA fix | A | ~200s | Good | Diagnosed: must use PHA not event file |
| 6 | Plan B bias investigation | B | ~400s | Good | Root cause: NPB ARF=1 inflates N_npb by ~302x |

### Key Lessons from Round 2

1. **Rolling deployment works well**: Deploy 3 → audit each as it completes → deploy replacement. Don't wait for all 3.

2. **Subagent-4 "diagnoses but doesn't fix" pattern**: Fitting strategy comparison analyzed v18 code correctly (identified LHB/CXB shared+thawed, SP handling, sky_bg_scale frozen) but ran out of iterations before writing the comparison script. Fix: dispatch a second subagent with the diagnosis as context and narrow "write the script" goal.

3. **Background process notifications**: Plan B v4 ran as a background process. The orchestrator got two notifications (one error from old version, one success from current version). Always check which version produced the result before acting on it.

4. **Cognition OS must be updated in real-time**: After each subagent audit, immediately update TRUST_TABLE, insights, and AI_BRIEFING. If you batch all OS updates to the end, you lose the "rolling" benefit — the next subagent you deploy should benefit from the latest understanding.

5. **Temperature gradient direction is a critical cognitive checkpoint**: The original user description said "30 kpc 0.75 → 10 kpc 0.6 keV" which IS outer-hotter, but the orchestrator initially misread this as "inner-hotter". This caused a false I007 "gradient direction correction" that had to be corrected again. **Rule**: When gradient direction matters, always verify with explicit numbers (inner kT = X, outer kT = Y) rather than relying on natural language descriptions like "从A下降到B".

## Deployment Statistics (Round 3-4 — M104 CGM, 4轮12 subagent)

| # | Task | Type | Duration | Quality | Key Finding |
|---|------|------|----------|---------|-------------|
| 7 | NPB ARF=1 fix + Plan B v4 rerun | B | 5693s | ✅ Good | Bias reduced 66% (-0.273→-0.091 keV). N_npb fixed=1.0 |
| 8 | Fitting strategy analysis | B | 3037s | ⚠️ Partial | Analysis done, script NOT written. Strategy C≡A for single obs |
| 9 | Band ratio from PHA | B | 4078s | ⚠️ Partial | Found 4B/3B data mismatch. CSV done, plots failed |
| 10 | Fitting strategy script creation | B | 4061s | ⚠️ Partial | Script created (~1100 lines), never executed (CIAO env blocked) |
| 11 | Response tables v2 rebuild | B | 1612s | ✅ Good | v2.npz from 3B data. obs_C +20-43% vs v1 |
| 12 | Band ratio S/M/H extraction | B | 4845s | ⚠️ Partial | CSV done. Negative v18 errors crashed plots |
| 13 | 5-band Plan B design | B | 2869s | ⚠️ Partial | Research done, code NOT created (hit limit) |
| 14 | S/M-only band ratio | B | 6526s | ✅ Key finding | NPB dominates S/M 73-80%. HR1 unusable. I014 |
| 15 | Fitting strategy execution | B | 4378s | ⚠️ Partial | Sherpa env verified. Script created, 1 fit done |
| 16 | 5-band Plan B implementation | B | 2237s | ✅ Good | Full pipeline: tables + MCMC + plots. 5b/3b error ratio=0.997 |
| 17 | BG robustness check | B | 3692s | ⚠️ Mixed | 24 fits done. Outer kT runaway (4-12 keV). But ±20% bg → kT stable |
| 18 | kT profile comparison plot | A | 576s | ✅ Good | 6 output files. 4 methods compared |

### Key Lessons from Round 3-4

1. **CIAO/Sherpa environment is the #1 subagent failure mode**: 5 of 12 subagents had CIAO-related issues. `source ciao.sh` is blocked by terminal tool restrictions. **Mitigation: provide a shell wrapper script that sources CIAO and runs Python in one command.** Example: `bash -c 'source /path/ciao.sh -o && python3 script.py'`. Or: pre-build the CIAO environment into a shell script and tell subagent to run it.

2. **"Research done, code not written" is the #2 failure mode**: Subagents 8, 13 both spent all iterations reading code and understanding structure but ran out before writing anything. **Mitigation: If the task involves both understanding AND implementing, split into two subagents — one for diagnosis/research, one for implementation with the diagnosis as context.** This was already a known pattern (pitfall #5) but the frequency in this session (3/12 = 25%) shows it's under-mitigated.

3. **Pre-package context aggressively**: Subagents 14 and 16 succeeded because they received extremely detailed context (exact file paths, column names, PI channel mappings, formulas). Subagents 8, 13, 15 struggled because they had to discover code structure by reading 2400+ line scripts. **Rule: If the source code is >500 lines, provide a pre-processed summary of the relevant functions and their signatures instead of making the subagent read the whole file.**

4. **Minimal models can produce misleading results**: Subagent 17's ultra-minimal Sherpa script (no SP, no sky_bg_scale, single instrument) gave physically meaningless kT values (4-12 keV) for outer regions, even though inner regions were fine. The "gradient robustness" conclusion was still valid (±20% bg → kT stable) but only because the test was about relative changes, not absolute values. **Rule: When using simplified models for robustness tests, ONLY trust relative comparisons between strategies, NOT absolute parameter values.**

5. **Negative error bars crash matplotlib**: v18 CSV has negative `kT_err_high` values for some regions. Always clip errors to >= 0 before plotting. **Rule: When reading external CSV data for plotting, sanitize numeric columns (clip errors, handle NaN/inf) before passing to matplotlib.**

6. **4.background vs 3B.background data quality**: User confirmed 4B data has better GTI (more soft proton removed). When multiple data processing versions exist, **always ask the user which version to use as primary** before investing subagent effort in the wrong one. We wasted Subagent-11 rebuilding response tables from 3B data that turned out to be inferior.

7. **Rolling deployment with cognition OS updates is effective but expensive**: 4 rounds × 3 parallel subagents × ~4000s average = ~48000s of subagent compute. But the orchestrator's context window degrades noticeably by round 4. **Rule: For sessions with >9 subagent deployments, consider writing an intermediate summary to cognition OS and starting a fresh session rather than continuing in a degraded context.**

## Deployment Statistics (Round 5 — M104 CGM 2D kT Map, 2轮6 subagent)

| # | Task | Type | Duration | Quality | Key Finding |
|---|------|------|----------|---------|-------------|
| 19 | 5-band Poisson MLE temperature map | B | ~600s | ✅ Good | kT consistent with v18 (+1.6% NE, -3.7% SE) |
| 20 | Band ratio HR→kT map | B | ~500s | ✅ Key finding | SP contamination ~9× source in H band. HR→kT NOT viable |
| 21 | Background systematics (3B vs 4B) | B | ~300s | ✅ Good | |ΔkT|=0.007 keV (0.9%). Not cause of poor rstat |
| 22 | Adaptive bin 5-band MLE (105 bins) | B | timeout | ❌ Failed | Count extraction too slow. Pre-extract needed |
| 23 | Color-color diagram | B | timeout | ⚠️ Partial | 3 figures created before timeout. Spatial info lost |
| 24 | Chandra 8-sector HR map | B | ~800s | ✅ Key finding | NE cooler 4.3σ. Matches XMM angular pattern |

### Key Lessons from Round 5

1. **5-band MLE validates v18 spectral kT**: The 5-band Poisson MLE approach
 (0.4-0.8, 0.8-1.2, 1.2-2.0, 2.0-3.2, 3.2-5.0 keV) gives kT within 2-4%
 of full v18 spectral fitting, but runs in ~0.1s per region vs ~8 min.
 This is the recommended fast-look tool for 2D temperature mapping.
 3-band MLE is degenerate for kT<0.8 keV — 5-band is the minimum.

2. **HR→kT is NOT viable for XMM EPIC**: SP H-band count rate is ~9× source
 H-band rate. Hardness ratio measures SP intensity, not temperature.
 S/M ratio is less affected but still has systematics. For absolute kT,
 use spectral fitting or 5-band MLE. HR is only useful for RELATIVE
 angular comparisons (e.g., Chandra HR showing NE cooler than SE).

3. **Data pre-extraction is critical for subagent success**: Subagent-22
 (adaptive bin MLE) timed out because it tried to extract counts from
 FITS event files AND run MLE in the same subagent. The count extraction
 took all the time. **Always pre-extract data into CSV/npz before
 delegating only the analysis/fitting/plotting step.**

4. **Partial results on timeout are still valuable**: Subagent-23 (color-color)
 timed out but produced 3 usable figures. Always check for partial output
 (figures, CSV, intermediate data) before re-dispatching.

5. **Pure-numpy tasks complete faster**: Subagent-21 (background comparison)
 used only numpy+pandas (no CIAO/Sherpa) and finished fastest with
 conclusive results. Prefer pure-numpy approaches when possible.

6. **Divergent parallel goals maximize value**: The 3-subagent triad
 (MLE / HR→kT / background systematics) had INDEPENDENT goals. If one
 fails, the others still produce unique value. Better than 3 subagents
 doing the same thing on different inputs.

7. **Old background processes create notification noise**: Batch fitting
 processes from previous sessions continued to deliver error notifications
 long after becoming irrelevant. **Rule**: Ignore background process
 notifications that reference old code/timestamps. Verify current results
 independently.

## When NOT to Use Subagents

- Derivations requiring mathematical judgment (circular reasoning risk)
- Tasks where the "correct answer" is unknown (no sanity check possible)
- Tasks requiring iterative user feedback (subagents cannot `clarify`)
- Tasks that touch the same files as other running subagents (race conditions)