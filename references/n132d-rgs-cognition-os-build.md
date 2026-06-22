# N132D RGS Cognition OS Build: Spectral-Analysis Pipeline Pattern

## When this pattern applies

- Project is a **spectral analysis pipeline** (not proposal, not simulation validation)
- Pipeline is complete (data → products) but no spectral fitting done yet
- Few prior AI sessions (< 3), all context is in files
- No external documents (proposals, reviews) — insights come purely from data products
- The "current question" is forward-looking (what to model next), not backward-looking (what went wrong)

## Procedure

### 1. Identify project scale → choose streamlined audit

N132D RGS: 5 OBSIDs, ~10 scripts, 1 combined spectrum, < 3 sessions.
→ Streamlined audit (15–30 min), NOT deep audit (3–5 hours).

### 2. Read project README first

`~/program/N132D/README.md` contained the full observation inventory (851 observations across 18 missions, XMM details with exposure breakdown). This provided:
- OBSID list (5 RGS observations)
- Exposure times (RGS1/RGS2 effective exposures)
- PA distribution context

### 3. Scan data directory structure

```bash
find /home/huangrui/Data/N132D/ -maxdepth 3 -type d
```

Revealed: `<OBSID>/odf/ + pps/ + rpc/rgs/` pattern + `combined/rgs/` for stacked products.

### 4. Identify pipeline scripts → map to experiments

| Script | Experiment | Stage |
|--------|-----------|-------|
| `process_rgs_all.sh` | E001: rgsproc | S01: Data acquisition |
| `screen_n132d_flare.py` | E002: Flare screening | S02: QC |
| `stack_rgs.sh` | E003: rgscombine | S03: Stacking |
| `rgs_emission_lines.py` + plot scripts | E004: Line annotation | S03: Stacking |

Key: each script = one experiment. No need to decompose further.

### 5. Read screening results → quality decisions

`flare_screening.json` was the single most important data product for the OS:
- 2/5 OBSIDs clean → Decision D02 (exclude 3 OBSIDs)
- 0811012401 "negative rate" → open question (not diagnosed)

### 6. Session search for context

`session_search("N132D RGS")` returned 1 session with detailed summary covering:
- RGS spatial resolution technical notes
- Emission line inventory from vision_analyze
- Interrupted wiki ingest

This session summary provided the cognitive history that file-tree-only analysis would miss (especially the RGS vs EPIC resolution comparison and the O VII triplet blending assessment).

### 7. Build all OS files in one pass

Since all context was gathered in steps 1–6, wrote all 26 files in 3 `execute_code` batches:
- Batch 1: Core files (00–04) + directory structure
- Batch 2: Stages (S01–S04) + DAG
- Batch 3: Insights (I001–I004) + Experiments (E001–E004 with manifests) + Session + SCHEMA + index + log

### 8. Key structural choices

**Stages = pipeline order** (acquisition → screening → stacking → modeling), NOT direction changes. This is the standard pattern for pipeline projects.

**Current stage (S04) is forward-looking**: it poses open questions (2T sufficient? O VII density? Fe XVII ratio?) rather than recording completed work.

**Trust table includes physical priors**: T08 (spatial broadening) and T09 (O-rich ejecta) are from literature/domain knowledge, not from project experiments. This is correct — the trust table should include ALL claims that downstream analysis depends on.

**No bug impacts yet**: Pipeline ran cleanly. Empty `bug_impacts/` directory is fine.

## Differences from M82 SQUDE pattern

| Dimension | M82 SQUDE (proposal) | N132D RGS (spectral pipeline) |
|-----------|---------------------|-------------------------------|
| External docs | Proposal + reviewer feedback → insights | None; insights from data products only |
| Goal prompt | Saved as artifact | Not applicable |
| Current question | "Upgrade proposal section" | "What spectral model fits best?" |
| Insight sources | Reviewer convergence, draft notes | Flare screening, line inventory |
| Stages | Pipeline + proposal upgrade | Pipeline only (modeling = next stage) |
| Decisions | Proposal strategy choices | Data quality exclusion decisions |

## File count

- 6 core files (00–05)
- 4 stages
- 4 insights
- 4 experiments × 2 files (md + yaml) = 8 files
- 1 session record
- 1 SCHEMA
- 1 index
- 1 log
- **Total: 26 files**

## Build time

~15 minutes (single session, no subagents, no deep audit needed).