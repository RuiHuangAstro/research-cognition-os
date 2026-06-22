# M82 SQUDE Cognition OS Build (2026-05-28)

## Project type

Small-medium research project. Existing pipeline (Chandra extraction → Sherpa fit → SQUDE simulation → re-fit), ~15 key products, 1 Hermes session found, no Codex/Claude sessions.

## Build procedure used

Streamlined audit (6 steps, ~20 minutes):

1. **Read project docs**: AGENTS.md + README.md → extracted project structure, CIAO workflow, Sherpa patterns, naming conventions
2. **Scan file tree**: `find -printf '%T+ %p\n' | sort -r | head -60` → identified 3 chronological phases (Apr 13 extraction → Apr 13 fit → Apr 15 vertical bins + SQUDE)
3. **Read key outputs**: fit .txt files (4×4' baseline, SQUDE 50ks re-fit), flux_summary.csv, simulation info.txt → extracted parameters, rstat, counts, deviations
4. **Session search**: `session_search("M82 SQUDE")` → 1 session (May 12 slide deck creation, not analysis)
5. **Build all OS files in one pass**: 16 files created
6. **No deep audit needed**: Project too small for 8-phase procedure

## Key decisions during build

- **3 stages** (not more): S01 extraction, S02 baseline fit, S03 SQUDE simulation. Each stage maps to a clear chronological phase.
- **2 insights** (not more): I001 (param recovery <5%) and I002 (center bin contamination). These are the two non-obvious findings.
- **6 decisions in DECISION_LOG**: D001-D006, covering ObsID selection, no-background, kT_hot fixed, abundances linked, 50ks exposure, vertical binning schemes.
- **Current question**: SQUDE line-resolution capability — chosen because it's the next logical step and the proposal's core selling point.

## What the file tree alone missed

The session search found only 1 session (a slide deck, not analysis). The actual analysis was done in a different session format or by the user directly. The AGENTS.md + README.md + file timestamps provided sufficient context to reconstruct the cognitive history without session records.

## Template adjustments

- AI_BRIEFING: Replaced DET_ML methodology invariants with project-specific ones (Wilms/Verner abundances, chi2gehrels, no-background)
- TRUST_TABLE: Added 12 items covering data, model, response, results, and methods
- DAG: Simple 3-stage flow, no contamination chains (no bugs yet)

## Output

`~/Data/M82/research-cognition-os/` — 16 files:
- 6 core files (00-05)
- 3 stages (S01-S03)
- 2 insights (I001-I002)
- 3 experiments (E001-E003) + 1 manifest
- 1 session record