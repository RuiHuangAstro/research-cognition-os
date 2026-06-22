# XARTATOMS Cognition OS Build: Worked Example

> Built: 2026-05-11
> Project: XARTATOMS — X-ray Analysis of M104 (Sombrero Galaxy) Hot Gas Halo
> Project path: `~/program/XARTATOMS/`

## Session Search Results

| Tool | Sessions found | Data volume | Content quality |
|------|---------------|-------------|-----------------|
| Codex (`codex_search.py`) | 1 (019db73d, 2026-04-22) | 14MB, 1057 lines | **Core** — SZ/X-ray iteration, data audit, MCMC |
| Claude Code (`claude_search.py`) | 3 (893f219b, eaa7e5bf, ed5b5869) | 13KB total | Useless — only "hello?" test messages |
| Hermes (`session_search`) | 3 (2026-05-06) | Small | Minor — RGS exploration |
| File tree (VERSION_CHANGELOG.md) | — | — | **Core** — v1→v19 cognitive history |

## Key Finding: Session Records vs File Tree

The VERSION_CHANGELOG.md was the primary source for cognitive history (v1→v19 evolution). The Codex session provided the SZ/X-ray tension narrative. Claude Code and Hermes contributed nothing substantive. This is the opposite pattern from DET_ML_Uncertainty, where Claude Code sessions were the primary source.

**Lesson**: Always search ALL tools — you don't know which one has the real work until you check.

## Codex Session Extraction Notes

Codex JSONL format differs from Claude Code:
- `type='response_item'` with `payload.role='user'` and `payload.content[].type='input_text'`
- Not `type='user'` with `message.content` like Claude Code
- The `codex_search.py` script had an IndentationError and couldn't parse this session format
- Had to extract manually with Python one-liners

## Stages Identified

| Stage | Period | Key event |
|-------|--------|-----------|
| S01: Exploration | 2025-06 | v1→v6: energy range, background strategy, parameter freezing |
| S02: Stabilization | 2025-08 | v7→v12: output dirs, xspegpwrlw, background scaling |
| S03: Publication freeze | 2025-09 | v13→v15: fixed CXB, T/Z grid |
| S04: SZ/X-ray tension | 2026-04 | ~2× discrepancy discovered, data version audit |
| S05: Temperature refinement | 2025-11→2026-02 | v16→v19: temperature refit, SP freeze, module cleanup |

## Core Open Question

**Why is X-ray derived SZ ~2× higher than reference?**

Root cause hypothesis: beta model data files (v7.2.npz) were modified 2025-10-10, but reference figure was generated 2025-10-08. Data version mismatch.

## Trust Table Summary

- 22 items total
- Trusted: v15 fitting, 2T APEC, energy range, xspegpwrlw, upper limit handling, normalization fix
- Questioned: SZ derivation, isothermal assumption, v7 beta samples, SP freezing
- Provisional: background scaling, beta model deprojection, v13/v14/v15 samples, temperature profile

## Files Created

```
research-cognition-os/
  00_AI_BRIEFING.md
  02_CURRENT_QUESTION.md
  03_TRUST_TABLE.md
  04_DECISION_LOG.md
  05_PROJECT_DAG.md
  stages/S01_exploration.md through S05_temperature_background_refinement.md
  insights/I001_xspegpwrlw_for_CXB.md through I003_upper_limit_censored.md
  bug_impacts/B001_normalization_bug.md, B002_data_version_mismatch.md
  sessions/2026-04-22.md, 2026-05-06.md, 2026-05-11.md
```