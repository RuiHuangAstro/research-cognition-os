# Deep Audit Methodology for Cognition OS Reconstruction

Source: DET_ML_Uncertainty project deep audit plan (2026-05-11)

## Problem

When building a cognition OS for an existing project, the naive approach (filename scanning + timeline extraction) fails because:
1. File names don't reveal experimental conclusions
2. Summary file headers don't capture PSF dependencies or trust levels
3. Codex/Hermes session records contain cognitive turning points invisible in the file tree
4. Theory derivation chains require reading content, not just timestamps

The DET_ML_Uncertainty project had TWO failed audits before this methodology was developed:
- Audit 1: Only scanned filenames + timestamps. Missed E010 (ML~10 forward calibration).
- Audit 2: Read 71/86 summary file headers but still "scanned and wrote conclusions" without deep reading. Missed 90+ summary files.

## Methodology: 8-Phase Deep Audit (Session-First Revision)

### Phase 0: Session Record Extraction (NEW — DO THIS FIRST)

Before touching any file tree, extract session records:
1. Use `codex_search.py --list --cwd <project>` to find Codex sessions
2. Extract all `final_answer` and `user_message` entries chronologically
3. Use `claude_search.py --list --cwd <project>` to find Claude Code sessions
4. Extract key conclusions, rejected approaches, user feedback, and bug discoveries
5. Build a provisional timeline of cognitive turning points

**Why first**: Session records contain the "why" and "why not" that file trees cannot reveal. Three audits of DET_ML_Uncertainty missed DR14 effective mask calibration and SAS ecut semantics because these only existed in Claude Code session JSONL.

### Phase A: Full Summary Content Reading (CRITICAL)

Read EVERY `_summary.md` file in `results/` completely. Extract per file:
- Research question
- Key conclusion (with numbers)
- PSF dependency: yes/no/partial
- Trust level: high/medium/low
- Linked insight (if any)
- Linked stage (if any)

**Subagent decomposition**: Split ~85 files into 3 parallel subagents by date range:
- A1: Early period (project start ~ mid-catalog work)
- A2: Mid period (catalog calibration ~ proxy simplification)
- A3: Late period (SAS validation ~ forward calibration)

**Output**: CSV with columns: `file, date, question, conclusion, psf_dep, trust, insight_id, stage_id, notes`

### Phase B: Key Script Code Audit

Read the ~10 most critical scripts to verify:
1. PSF dependency claims from Phase A (does the code actually use AnalyticEllbetaPSF?)
2. Whether summary conclusions match what the code actually computes
3. Whether "no PSF dependency" claims are truly independent

Focus on scripts that interface between toy model and real SAS data.

### Phase C: Session Record Deep Analysis (expands Phase 0)

Phase 0 extracted the raw timeline. This phase digs deeper:
- Extract reasoning chains behind each conclusion (not just what, but why)
- Identify rejected approaches and why they were rejected
- Find user feedback moments that triggered direction changes
- Map session conclusions to specific files/artifacts for cross-validation

### Phase D: Theory Derivation Chain Reconstruction

For `theory/` directories:
1. Sort by file modification date
2. Read each file's core claim
3. Build a derivation dependency graph: which document extends or supersedes which
4. Identify dead-end derivations (started but abandoned)

### Phase E: Catalog/Application History Reconstruction

For `source_catalog/` and catalog-related scripts:
1. Trace the iteration path from first catalog contact to final calibration
2. Identify parallel exploration branches (e.g., theory-guided vs empirical vs cts-window)
3. Note which branches converged and which died

### Phase F: OS Reconstruction

Synthesize all phase outputs into the cognition OS:
1. Merge summary CSV into ~30-40 experiment groups
2. Define 10-17 stages based on cognitive turning points (not just date clusters)
3. Extract 20-25 independent insights from experiment conclusions
4. Build TRUST_TABLE with 50-60 entries covering all experiments
5. Write AI_BRIEFING, CURRENT_QUESTION, DECISION_LOG
6. Draw three DAG views (Cognitive, Trust, Frontier)
7. Generate Obsidian Canvas from DAG

### Phase G: Cross-Validation

Verify against 7 criteria:
1. Every summary file has an experiment record
2. Every insight points to specific experiment evidence
3. TRUST_TABLE entries match experiment manifest trust levels
4. PSF dependency annotations match code audit results
5. DAG has no back-edges
6. Stage timeline matches file modification dates
7. AI_BRIEFING trusted/questioned lists match TRUST_TABLE
8. No duplicate IDs in insights/experiments/TRUST_TABLE unless explicitly documented
9. No broken wikilinks, except intentional examples in SCHEMA/templates
10. YAML frontmatter status/confidence matches visible Status/Confidence text
11. Deprecated/questioned items are not listed as unqualified trusted entries in AI_BRIEFING
12. Methodology invariants are present in AI_BRIEFING, CURRENT_QUESTION, and TRUST_TABLE when conditional statistics are central to the project

### Phase H: Skill + Wiki Sync

1. Update research-cognition-os skill pitfalls
2. Sync to ~/wiki/ domain pages
3. Update project wiki current-status and next-experiments

## PSF Dependency Classification Rules

For X-ray projects using both toy-model and real PSF data:

| Code uses | PSF dependency | Examples |
|-----------|---------------|----------|
| Toy model Gaussian PSF only | `no` | Phase 0-2 simulations, 44M benchmark |
| psfgen-generated PSF arrays (read from FITS) | `partial` | M31 batch simulation analysis |
| AnalyticEllbetaPSF / analytic ELLBETA class | `yes` | Python detection theory, forward calibration |
| Real catalog data (4XMM-DR14) | `no` (for catalog itself) | Catalog statistics |
| Python Cash fitter with any PSF | `depends on PSF used` | Check which PSF was passed |

## Subagent Timeout vs Direct Batch Reading

For projects with 100+ summary files, delegate_task subagents timed out at 600s with only 19/85 API calls completed. The successful approach was **direct batch reading in execute_code**:

```python
# In execute_code: read 10-15 files per call
from hermes_tools import read_file
files = ["file1_summary.md", "file2_summary.md", ...]
base = "/path/to/results/"
for f in files:
    r = read_file(path=base + f, limit=60)  # limit lines
    content = r["content"][:600]             # truncate chars
    print(f"FILE: {f}\n{content}")
```

- 5 batches × 15 files ≈ 30 seconds total
- Each batch: ~5-10 seconds wall time
- Truncation to 600-1500 chars/file is sufficient for question/conclusion/PSF-dependency extraction
- For deeper files (theory derivations, Codex logs), use limit=100-200 lines

**Rule: Never delegate bulk file reading to subagents for audit tasks. Use execute_code with read_file loops.**

## Real Example: DET_ML_Uncertainty Audit Results

| Metric | Before deep audit | After deep audit (actual) |
|--------|-------------------|---------------------------|
| Summary files read (content) | 0/106 (0%) | ~85/106 (~80%) |
| Experiments recorded in OS | 16 | 20 |
| Experiments with summary.md | 12/20 | 16/20 (4 missing filled) |
| Insights | 15 | 15 |
| Stages | 8 | 8 |
| TRUST_TABLE entries | 38 | 15 (精简版) + 38 (原版) |
| PSF dependencies verified | ~5 | All 20 experiments |
| Cognitive turning points | 0 | 4 (T1-T4) |
| Negative results recorded | 0 | 5 |
| Codex session phases extracted | 0 | 4 (Phase 0-4) |
| Theory files read | 0 | 10/32 key files |
| Wiki phase logs read | 0 | 8/8 |

**Coverage gap**: ~21 files not read (mostly CSV summaries and duplicate/variant runs of same experiment). These are lower priority than the .md summaries.