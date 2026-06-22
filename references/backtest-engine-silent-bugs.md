# Backtest Engine Silent Bugs — Fund Strategy Session 2026-05-29

## Overview

Quantitative backtest engines are prone to **silent bugs** that produce plausible-looking results but are fundamentally wrong. These bugs don't crash — they silently degrade or invalidate results. The Fund Strategy project discovered 6 such bugs via agy-review, 3 of which were CRITICAL.

## Bug Catalog

### B001: datetime.date vs DatetimeIndex silent fallback (CRITICAL)

**Symptom**: Adaptive allocation strategy appeared to have near-zero advantage over fixed allocation (Δ=+0.002), leading to months of "7-stage has no alpha" conclusions.

**Root cause**: `build_adaptive_equity()` used `d.date()` to convert `pd.Timestamp` to `datetime.date`, but looked up values in a `DatetimeIndex`. `datetime.date` objects NEVER match `DatetimeIndex` entries, so all lookups silently returned `NaN`, falling back to a default of 0.70.

**Detection**: agy-review audit discovered it. Match rate was 0% (should be ~90%).

**Fix**: Normalize stage_df dates to `pd.Timestamp` before lookup.

**Impact**: After fix, Δ jumped from +0.002 to +0.075 — the adaptive strategy was actually highly significant.

**Pattern**: `pandas` type coercion between `datetime.date` and `pd.Timestamp` is SILENT — no error, no warning. This is a general pandas pitfall.

### B005: future_return_7d look-ahead bias (CRITICAL)

**Symptom**: All strategy Sharpe ratios appeared higher than reality.

**Root cause**: `generate_signals()` included `future_return_7d` in the `required` list for `dropna()`. This meant funds that would be delisted/suspended in the next 7 days were excluded from the signal universe — giving the strategy advance knowledge of fund survival.

**Detection**: agy-review audit.

**Fix**: Remove `future_return_7d` from the `required` list. Signal generation should only depend on historical features.

**Impact**: Systematic overestimation of all strategy Sharpe ratios, especially for equity-heavy strategies in bear markets (where suspensions cluster).

### B006: hold_days=7 hardcoded vs config h=14 (HIGH)

**Symptom**: Grid search over holding period (h=7,14,21) produced identical results for all h values. The h dimension was completely wasted.

**Root cause**: `attach_future_returns(panel, hold_days=7)` was called once outside the grid loop with hardcoded 7. The `exit_date` column was fixed at T+8 for all configurations. The `h` parameter only affected `max_positions` calculation, not actual holding period.

**Detection**: Discovered when MR v2 grid search showed h=7/14/21 giving identical SharpeNet values.

**Fix**: Change all `hold_days=7` to `hold_days=14` (matching strategy configs). For grid search over h, recompute exit_date per configuration from pre-computed fund date maps.

**Impact**: ShpNet jumped from 0.736 to 1.074 (+0.338) after fix — the single largest performance driver.

**Pattern**: When a parameter appears in config but is overridden by a hardcoded value elsewhere, the config parameter is effectively dead. Grid search over that parameter produces flat results (identical across all values), which can be misinterpreted as "robustness" when it's actually a bug.

### B007: T+0 instant settlement (MEDIUM)

**Symptom**: MaxDD appeared unrealistically low (-3.5%).

**Root cause**: `engine.py` allowed redeemed cash to be immediately reused for buying. Real fund redemption takes T+1 to T+4 days.

**Fix**: Added `settlement_queue` with 2-day delay.

**Impact**: MaxDD increased from -3.5% to -6.7% (more realistic).

### B008: IC descending sign flip (HIGH)

**Symptom**: Signal IC was reported as negative (-0.008 to -0.033), leading to "alpha comes from portfolio construction, not signal" conclusion.

**Root cause**: `signal_decay_analysis.py` applied `ic_p[sig_col] = -ic_p[sig_col]` for descending signals, incorrectly flipping the sign. True IC ≈ +0.049.

**Impact**: Misleading interpretation of signal quality. The signal actually has modest positive predictive power.

### B010: Survivorship bias (CRITICAL, UNRESOLVED)

**Symptom**: All strategy Sharpe ratios systematically inflated.

**Root cause**: Fund pool based on 2026 currently-surviving funds. Funds delisted/merged during 2020-2025 are excluded.

**Impact**: Cannot be fixed without point-in-time fund data. Estimated SharpeNet overestimation: 0.1-0.3.

## General Patterns

1. **Silent fallback is the most dangerous bug class** — No crash, no error, plausible results. Always verify that dynamic logic is actually executing (check match rates, value distributions, per-group counts).

2. **Look-ahead bias is endemic in financial backtests** — Any use of future data in filtering, sorting, or required columns is a look-ahead. Audit every `dropna(subset=[...])` list.

3. **Hardcoded parameters kill grid search validity** — If a grid search produces flat results across a parameter, suspect the parameter isn't actually being used. Verify by checking that different parameter values produce different intermediate results (not just different final outputs).

4. **Settlement timing affects risk metrics more than returns** — T+0 vs T+2 barely changes Sharpe but significantly changes MaxDD and drawdown duration.

5. **agy-review is essential for catching these bugs** — 3 of 6 bugs were discovered by agy-review, not by manual testing. The datetime bug was invisible to all previous analysis because it produced plausible results.

## Prevention Checklist

For any backtest engine:

- [ ] Verify dynamic allocation match rates (should be >80%)
- [ ] Audit all `dropna(subset=[...])` lists for look-ahead columns
- [ ] Verify grid search parameters actually vary intermediate results
- [ ] Add settlement delay (minimum T+2)
- [ ] Check IC sign conventions for ascending/descending signals
- [ ] Document survivorship bias limitations explicitly
- [ ] Run agy-review before publishing any results
- [ ] Verify equity DataFrame has all required columns (`cash`, `total_equity`, `date`) before calling `portfolio_metrics()`
- [ ] Verify import names match actual module exports (e.g., `build_stage_series()` vs `MarketStageEstimator` class)

## Additional Session-Specific Pitfalls

### P001: portfolio_metrics requires `cash` column

**Symptom**: `KeyError: 'cash'` when calling `portfolio_metrics()` on manually-constructed equity DataFrames.

**Root cause**: `simulate_strategy()` automatically generates `cash` and `total_equity` columns, but `build_adaptive_equity_v2()` and manual equity construction only output `date` + `total_equity`. `portfolio_metrics()` accesses `df["cash"]` unconditionally.

**Fix**: Add `"cash": 0.0` to every row when constructing equity DataFrames manually.

**Session**: 2026-05-29, `mr_v2_candidate_test.py`

### P002: Module import name mismatch

**Symptom**: `ImportError: cannot import name 'MarketStageEstimator'` from `market_stage_estimator`.

**Root cause**: The module exports `build_stage_series()` (a function), not `MarketStageEstimator` (a class). The import was written based on assumed API rather than actual exports.

**Fix**: Use `from backtest.market_stage_estimator import build_stage_series`.

**Session**: 2026-05-29, `mr_v2_candidate_test.py`

### P003: hold_days grid parameter must recompute exit_date

**Symptom**: Grid search over h=7/14/21 produces identical results for all h.

**Root cause**: `attach_future_returns(panel, hold_days=14)` is called once with fixed hold_days. The `exit_date` column is computed at load time. If the grid loop varies h but doesn't recompute exit_date, h has no effect on actual holding period.

**Fix**: Pre-compute `fund_dates[fc] = sorted(panel[panel["基金代码"]==fc]["净值日期"].tolist())`. For h≠default, recompute `exit_date = fund_dates[fc][entry_idx + h]` per row.

**Session**: 2026-05-29, `mr_v2_grid.py`