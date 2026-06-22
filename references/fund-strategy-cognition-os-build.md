# Fund Strategy Cognition OS Build (Updated 2026-05-29)

## Project Overview
Non-X-ray quantitative research project: 中国公募基金 C 份额短周期策略回测系统.
46 files across 5 core + 7 stages + 21 insights + 10 bug impacts + 2 experiments + 1 session.

## Key Pattern: Bug-Invalidated Branch
S03 (7-stage bugged v3) and S04 (Fixed optimization v4) were entirely invalidated by B001
(datetime.date ≠ DatetimeIndex silent bug). This is the canonical example of how a single
silent bug can invalidate months of conclusions — all "7-stage has no alpha" results were
artifacts of the bug causing silent fallback to 0.70 default allocation.

## Build History

### Session 1 (2026-05-29 morning): Initial build
- 31 files: 5 core + 6 stages + 15 insights + 4 bugs + 1 session
- S01-S06 covering v1→v2→v3(bugged)→v4(misdirected)→v5(bug fix)
- B001 datetime silent bug as CRITICAL
- Agy-review as validation mechanism

### Session 2 (2026-05-29 afternoon): agy audit + 6bug fix + MR v2
- Updated to 46 files: +1 stage (S07), +6 bugs (B005-B010), +6 insights (I016-I021)
- S07: agy全策略审计 + 6bug修复重建
- 6 common bugs found by agy: look-ahead, IC sign, hardcoded h, T+0, survivorship, Sharpe avg
- Post-fix v5: ShpNet=1.074 (↑0.338), MaxDD=-6.7%, W2=-0.028
- MR v2 grid search (288 configs): 0 new signals beat DD_ac_rank
- RSI-20 as regime-conditional candidate (Bear=+0.641)
- mr_composite+above_ma60 as low-risk variant (MaxDD=-15.1%)
- h parameter exit_date recompute pitfall discovered

## Cognitive Arc
```
S01(Foundation v1v2)
  → S02(Regime Exploration)
  → S03(7-stage BUGGED) ← DEPRECATED by B001
  → S04(Fixed Optimization v4) ← DEPRECATED by B001
  → S05(Bug Discovery → v5) ← TURNING POINT
  → S06(Audit Remediation)
  → S07(agy Audit + 6bug Fix + MR v2) ← CURRENT
```

## Lessons for OS Building

1. **Bug-invalidated branches must be marked deprecated, not deleted** — S03/S04 content
   preserved for historical reference but clearly marked as unreliable

2. **agy-review as OS validation mechanism** — External audit found bugs that internal
   testing missed. Always run agy-review before marking conclusions as Trusted.

3. **Cross-cutting bug tracking** — 6 common bugs affected ALL strategies, not just one.
   B005-B010 track each bug's impact across the entire project.

4. **Strategy reclassification as insights** — agy audit revealed DP=债券Carry, FR=趋势动量,
   ZA=多头陷阱, MR=纯均值回归. These reclassifications are high-confidence insights
   that change how strategies should be combined.

5. **Grid search parameter verification** — When h=7/14/21 produce identical results,
   the parameter isn't being applied. Always verify intermediate values differ, not
   just final outputs. This is a general backtest engine pitfall.

## File Structure
```
research-cognition-os/
├── 00_AI_BRIEFING.md
├── 02_CURRENT_QUESTION.md
├── 03_TRUST_TABLE.md (21 insights + 6 decisions + 10 bugs)
├── 04_DECISION_LOG.md (6 decisions)
├── 05_PROJECT_DAG.md
├── stages/ (S01-S07, S03/S04 deprecated)
├── insights/ (I001-I021, 14 Trusted + 7 Provisional)
├── bug_impacts/ (B001-B010, 6 Resolved + 4 Active)
├── experiments/ (E001 full audit, E002 post-fix rebuild)
└── sessions/ (2026-05-29)
```