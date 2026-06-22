# File Timestamp Extraction for Cognitive History Reconstruction

Source: DET_ML_Uncertainty project cognition OS build session (2026-05-11)

## Problem

You have an existing research project with months of work but no structured cognitive record. The file tree IS the research log — it's just unstructured. You need to reconstruct the narrative from timestamps and content.

## Method

### 1. Full Timeline

```bash
find <project-root> -type f \
  ! -path '*/.git/*' ! -path '*/__pycache__/*' ! -path '*/.claude/*' ! -path '*/.agents/*' \
  -printf '%T+ %p\n' | sort
```

This gives every file with its modification timestamp. The chronological order reveals the project's actual execution sequence.

### 2. Date Burst Clustering

Files created/modified within 2-3 days of each other usually belong to the same research stage. Group by date:

- 2026-03-28 to 03-29: Project initialization + Phase 0
- 2026-03-30 to 04-02: Phase 1-2 (benchmark, conditional analysis)
- 2026-04-05 to 04-09: Phase 3-4 (projection formula, catalog)
- etc.

### 3. Key Document Priority

Read in this order (most narrative value first):
1. `GOAL.md` / `PROJECT_README.md` — project definition
2. `AGENTS.md` — environment and conventions
3. `BUGREPORT_*.md` — known bugs and impacts
4. `theory/*.md` — analytical derivations
5. `CLAUDE.md` / `GEMINI.md` — AI agent instructions (reveal workflow)
6. `OFFICIAL_FITTING_CONVENTIONS.md` / domain-specific docs
7. `config.py` / `lib/*.py` — actual implementation

### 4. Pivot Detection from File Naming

Iterative debugging leaves traces in file naming:
```
replicate_emldetect.py → v2 → v3 → v4 → final → official
```
Each version = a sub-stage. The progression reveals what was wrong and what was tried.

### 5. Data-Code Cross-Reference

- `results/*.npz`, `*.h5`, `*.csv` → when experiments actually ran
- `batch_*/combined_results.json` → large-scale simulation data
- `figures/*.png` timestamps → when visualizations were produced
- Symlinks (e.g., `emldetect_simulation -> /path/to/data/`) → external data dependencies

### 6. delegate_task for Large Projects

For projects with 100+ files, use delegate_task to read all key files in parallel. Each subagent reads a subset and returns structured summary:
- Chronological timeline
- Key stages identified
- Major insights/conclusions
- Known bugs and impacts
- Current state

The main agent then synthesizes into cognition OS files.

## Triangulation Principle

No single source tells the full story. Triangulate from **four** sources (priority order):

1. **Session records** (Codex/Claude JSONL) — reveal *why* decisions were made, what was tried and rejected, user feedback, reasoning chains
2. **Docs** — say what was planned and concluded
3. **Code** — shows what was actually implemented
4. **Data timestamps** — show when it actually ran

**⚠️ Session records are the primary source for cognitive history.** File trees only show products, not process. Three audits of DET_ML_Uncertainty missed critical findings (DR14 effective mask, SAS ecut semantics) because they only scanned files.

## Real Example: DET_ML_Uncertainty

From file tree analysis of `~/program/DET_ML_Uncertainty/` and `~/Data/XMM/M31_data/emldetect/`:

| Date Range | Stage | Key Files |
|-----------|-------|-----------|
| 2026-03-28 | S01: Toy world | sim/phase0_toy_world/, results/phase0_sims.npz |
| 2026-03-31 | S02: Position fitting | lib/fit.py, tests/test_phase1.py |
| 2026-04-02 | S03: 44.6M benchmark | scripts/run_parallel_benchmark.py, results/parallel_benchmark.h5 |
| 2026-04-05 | S04: Projection formula | theory/likelihood_derivation.md, scripts/fit_factorized_kappa_model.py |
| 2026-04-08 | S05: Catalog + deboosting | lib/deboosting.py, draft.pdf |
| 2026-05-01 | S06: M31 emldetect replica | emldetect_simulation/replicate_emldetect_*.py (6 versions!) |
| 2026-05-11 | S07: PSF bug rollback | BUGREPORT_AnalyticEllbetaPSF.md |

**⚠️ This table is INCOMPLETE** — it was built from file-tree-only analysis. Session record extraction later revealed additional critical findings not in any file: DR14 effective mask calibration (scut≈0.74, ecut≈14px), SAS ecut semantics (ecut=0.68 = PSF enclosed fraction), and the full reasoning behind direction changes. The file tree gives the skeleton; session records give the flesh.