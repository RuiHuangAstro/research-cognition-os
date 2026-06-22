# Quantitative Self-Consistency Validation Method

Concrete method for testing whether a semi-analytical model (e.g., k(ML))
accurately describes simulation results from the same pipeline.

## Step 1: Compute residuals per bin

```
residual_i = sigma_ratio_observed_i - k(ML_predicted_i)
rel_residual_i = residual_i / k(ML_predicted_i)
```

## Step 2: Test for systematic structure

Three statistical tests (run all three):

| Test | Purpose | Method | Interpretation |
|------|---------|--------|---------------|
| ANOVA / Kruskal-Wallis | Grouped by physical variable | `scipy.stats.f_oneway(*groups)` or `kruskal(*groups)` | p<0.05 → missing dependence |
| Linear regression | Residual vs continuous variable | `scipy.stats.linregress(x, residual)` | p<0.05 → systematic trend |
| Mann-Whitney U | Two-group comparison | `scipy.stats.mannwhitneyu(a, b)` | p<0.05 → different distributions |

**If all three are non-significant**: residuals are consistent with noise.
**If any is significant**: the model has a missing dependence.

## Step 3: Build error budget table

Decompose total uncertainty into independent sources:

| Source | How to estimate | Typical magnitude |
|--------|---------------|-------------------|
| Statistical (N_sims/cell) | 1/√(2·N_eff) per bin | ~1.9% (N=50k) to ~4.6% (N=5k) |
| Model parameterization | Chi2/ndof of fit | ~1-2% |
| PSF shape mismatch | Controlled experiment (4-step vs 8-step) | <0.5% |
| Optimizer convergence | Benchmark with known truth | <0.1% |
| ML formula | Analytical derivation | <0.1% |
| **TOTAL** | **RSS of above** | **~2-5%** |

The dominant source is almost always statistical (finite N per bin).
To reduce: increase N_sims. Rule: N_eff > 1500 for 5% effect detection.

## Step 4: Identify missing dependencies

If ANOVA is significant, plot mean residual vs the grouping variable.
Look for patterns:

### U-shaped pattern (DET_ML E010b example)

| Off-axis range | Mean residual | Interpretation |
|----------------|--------------|---------------|
| 0-4' (near-axis) | +1.2% | Theory OK (PSF similar to calibration) |
| 4-8' (mid) | +7.5% | Theory over-predicts compression |
| 8-12' (mid-far) | +5.6% | Theory over-predicts compression |
| 12-16' (far) | +1.2% | Theory OK (PSF very different but effects cancel) |

**Working interpretation**: k(ML) was calibrated on on-axis ELLBETA. At mid off-axis,
PSF may be less wingy → less compression → sigma_ratio higher than predicted.
At far off-axis, PSF may be strongly elliptical but wide → effects partially cancel.

**Required verification**: compute W (and the relevant position-scale variable r) per position before calling this the settled root cause. The winginess model k = 1/√(1+α·r²·W) is the hypothesis to test, not the conclusion by default.

### Monotonic trend

If residual increases/decreases monotonically with a variable,
the model is missing a linear/quadratic term in that variable.

## Step 5: Determine required N_sims

To detect a Δ% effect with 80% power at α=0.05:

```
σ_required < Δ / 2.8
σ ~ 1 / √(2 · N_eff)
N_eff = N_sims / n_bins_per_cell

→ N_sims > n_bins · 2 · (2.8/Δ)²
```

Example: detect 5% effect with 12 bins/cell:
- N_eff > 2·(2.8/0.05)² = 6272
- N_sims > 12 × 6272 = 75,264

For DET_ML E010b (N=1000/cell, 12 bins): σ≈7.8% per bin.
This is too noisy for 5% effect detection → need ~18× more sims.

## Bootstrap error bars for summary statistics

For any derived statistic (mean residual, RMS, etc.):

```python
rng = np.random.default_rng(42)
boot_stats = []
for _ in range(2000):
    idx = rng.choice(len(data), size=len(data), replace=True)
    boot_stats.append(statistic(data[idx]))
ci_68 = np.percentile(boot_stats, [16, 84])
ci_95 = np.percentile(boot_stats, [2.5, 97.5])
```

Always report: point estimate ± 68% CI. If CI includes zero,
the effect is not significant at 1σ.

## Paper writing pattern

When self-consistency is established with a known systematic:

> "Our compression model k = 1/√(1+α·r²·W) with α=0.325 describes
> our pipeline's simulation results with RMS residual of 4.5% (242 data
> points). Residuals show no systematic structure (trend vs r: p=0.06,
> trend vs S: p=0.82, PSF-type difference: p=0.75). The dominant error
> source is statistical (finite N per bin). For real-data paths with
> off-axis PSF variation, the winginess model captures the position-
> dependent compression, reducing systematic uncertainty from ~5% to ~2%."