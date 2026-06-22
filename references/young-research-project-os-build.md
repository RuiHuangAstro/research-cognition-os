# Young Research Project OS Build Pattern

When a research project has few prior AI sessions but already has a complete pipeline + products,
the deep-audit procedure (8-phase, subagent decomposition) is overkill. This pattern replaces it.

## When to use

- Project has < 3 prior AI sessions
- Project already has scripts, data products, fit results, plots
- No complex session history to reconstruct
- External documents (proposal, reviews) provide key context

## Procedure

### 1. File tree scan (not session extraction)

```bash
find <root> -type f -printf '%T+ %p\n' | sort
```

This gives the chronological timeline of all products. No session search needed.

### 2. Read key docs first

Read AGENTS.md, README.md, any BUGREPORT — these contain the project narrative.
For X-ray projects, also read fit reports (`.txt` files under `fits/`).

### 3. Map scripts → experiments, outputs → products

Each script = one experiment. Each output directory = one product.
Create E001, E002, ... by reading each script's docstring + outputs.

### 4. Build stages from pipeline order

For pipeline projects, stages = pipeline steps, not direction changes:
- S01: data acquisition/extraction
- S02: baseline model fitting
- S03: simulation/validation
- S04: proposal upgrade (if applicable)

### 5. Insights from data, not sessions

Read fit reports, CSV summaries, plots. Extract quantitative conclusions.
Do NOT try to reconstruct reasoning from absent session logs.

### 6. External documents as insight sources

**This is the key differentiator from the deep-audit pattern.**

- Proposal PDFs reveal: what the project claims, what it needs to prove
- Reviewer feedback reveals: weaknesses, missing analyses, priorities
- Internal notes reveal: draft status, TODO items, authorship

Each reviewer concern → one insight (especially if multiple reviewers converge).
Each draft note → one insight (things to fix before submission).

### 7. Goal prompt as artifact

If the user writes a detailed execution plan (e.g., a `/goal` prompt for Hermes),
save it under `artifacts/` and reference it from the active stage file.
This preserves the user's intent and constraints for future sessions.

## PDF extraction with SAS environment conflict

**Pitfall**: When SAS (XMM-Newton Scientific Analysis System) is initialized,
its bundled `libstdc++.so.6` shadows the system library, breaking `pdftotext`:

```
pdftotext: .../sas/.../libstdc++.so.6: version `GLIBCXX_3.4.29' not found
```

**Fix**: Temporarily clear LD_LIBRARY_PATH:

```bash
LD_LIBRARY_PATH="" pdftotext -layout file.pdf -
```

## docx extraction pattern

```python
from docx import Document
doc = Document('file.docx')
# Paragraphs
for p in doc.paragraphs:
    if p.text.strip():
        print(p.text)
# Tables (separate iteration required!)
for table in doc.tables:
    for row in table.rows:
        cells = [c.text.strip() for c in row.cells]
        print(' | '.join(cells))
```

Note: `doc.paragraphs` does NOT include table content. Must iterate `doc.tables` separately.

## Worked Example: M82 SQUDE

- **Project**: M82 SQUDE feasibility simulation for proposal
- **Pipeline**: Chandra extraction → Sherpa fit → SQUDE fake_pha → re-fit
- **Prior sessions**: 1 (slide deck creation, not data analysis)
- **OS files created**: 20 (6 core + 4 stages + 4 insights + 3 experiments + 1 decision log + 1 session + 1 artifact)
- **Key insights from external docs**:
  - I003: Two reviewers converge on same 3 weaknesses (spatial mixing, background, subgrid)
  - I004: Proposal has "yi" draft notes + overstated precision claims
- **Goal prompt**: `artifacts/hermes_m82_proposal_goal_prompt.md` — 8-phase revision plan
- **Build time**: ~30 minutes (single session, no subagents needed)

## Worked Example: M31-τX

- **Project**: Map τ_hot(v_esc) in M31 + M33 using PHAT/PHATTER resolved SFH + Chandra/XMM diffuse X-ray
- **Pipeline**: Phase 0 (feasibility) → Phase 1 (data inventory) → Phase 2 (X-ray reduction) → Phase 3 (cross-match + K(t) fitting)
- **Prior sessions**: 2 (feasibility + methodology design)
- **OS files created**: 6 (AI_BRIEFING + CURRENT_QUESTION + TRUST_TABLE + S02 + I001-I003 + session)
- **Key pattern**: **Literature research during methodology stage can force strategy revision**
 - Discovered M33 has no hot halo (Tüllmann+2011) → M33 cannot serve as "second M31" for quantitative τ_hot(v_esc) profile
 - But "no halo" is itself a qualitative constraint → revised M33 role from "quantitative cross-validation" to "low-v_esc anchor"
 - This insight (I002) was written BEFORE any data reduction — saving the project from wasted M33 halo analysis effort
- **Build time**: ~15 minutes (single session, no subagents for OS build; subagent used for M33 literature search)
- **Key lesson**: When dual-galaxy strategy depends on both galaxies having detectable emission, verify detection status in BOTH galaxies before committing to symmetric reduction pipelines

## Worked Example: M31Center RGS (Data-Only Project)

- **Project**: Reproduce Zhang+2019 (ApJ 887, 63) M31 bulge RGS spectral fitting
- **Pipeline**: Not a pipeline — iterative XSPEC fitting (v1-v21) with convention fixes, image comparisons, and blocker discovery
- **Prior sessions**: 5+ (multiple fitting iterations, convention corrections, stack reprocessing)
- **OS files created**: 18 (6 core + 3 stages + 3 insights + 3 experiments + 1 bug + 1 session + 1 artifact)
- **Data-only pattern**: No `~/program/M31Center/` directory — all code, data, and products under `~/Data/M31Center/`
- **Key pattern**: **Pre-existing audit document as artifact source**
 - CODEX_AUDIT_PROMPT.md already existed at `~/Data/M31Center/combined/xspec_fits_rgsxsrc/`
 - Symlinked into `research-cognition-os/artifacts/` rather than duplicating content
 - The audit prompt served as the primary source for stages, insights, and experiments
- **Key pattern**: **Stages track fitting iteration phases, not pipeline steps**
 - S01: Initial fitting (wrong conventions: wilm/C-stat/Fe=1.6)
 - S02: Convention fix (angr/χ²/Fe=0.57 — confirmed correct, archived)
 - S03: rgsxsrc blocker (multi-image limitation — active, unresolved)
- **Key pattern**: **Trust table includes both confirmed conventions and open blockers**
 - Trusted: angr abundances, χ² statistic, Fe=0.57
 - Questioned: rgsxsrc single-image constraint, vapec norm 35× discrepancy
- **Build time**: ~20 minutes (single session, execute_code for bulk discovery, no subagents)
- **Key lesson**: For iterative fitting projects, stages = paradigm shifts (convention fix, blocker discovery), NOT pipeline steps. Each stage should have a clear "what changed" and "what's still wrong" summary