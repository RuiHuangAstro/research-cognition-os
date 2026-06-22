# Variance Conditioning Trap

## The Problem

When comparing Var(deltaC_3p) vs Var(deltaC_1p), the ratio H_var depends
**critically** on what variable you condition on. Three natural choices
give completely different numbers:

| Conditioning | H_var at ML~10 | Physical meaning | Selection bias? |
|---|---|---|---|
| **S_true, b** | ≈ 1.00 | Repeated-experiment variance (same source, many realizations) | No |
| **ML_bin** | ≈ 0.35 | Variance within a narrow ML range | **Yes** — ML is monotonic in deltaC |
| **S_hat_bin** | ≈ 0.3–0.9 (non-monotonic) | Variance for sources with similar detected counts | Partial |

## Why ML-binning gives misleading H_var

ML is a monotonic function of deltaC under the SAS/emldetect convention: `DET_ML = -ln(gammaincc(nu/2, DeltaC/2))`.
Binning by ML ≈ binning by deltaC. Within a narrow ML bin, deltaC has a narrow
range by construction → Var(deltaC | ML_bin) is artificially small.

This is NOT a physical effect of 3-param fitting reducing variance. It's
selection bias: you selected realizations with similar deltaC, then measured
that their deltaC values are similar. Tautology.

## Why S_hat-binning gives non-monotonic H_var

S_hat = S_true + noise. When S_hat ≈ S_true (typical realization), the
3-param fit effectively uses its extra degrees of freedom → compresses deltaC
variance relative to 1-param → H_var small (~0.3). When S_hat >> S_true
(lucky fluctuation), position is well-determined → 3p ≈ 1p → H_var → 1.
When S_hat << S_true (unlucky), noise dominates → H_var → 1.

The non-monotonic pattern reflects the mixture of typical and atypical
realizations within each S_hat bin.

## ⚠️ ML Truncation Trap (2026-05-14 addition)

An even more dangerous variant of ML-binning is **ML truncation**:
selecting samples where ML falls in some range (e.g., ML ∈ [5,10]) and
then analyzing the conditional distribution of deltaC or ML within that
truncated sample.

### Why it's wrong

Realized ML is a nonlinear monotonic transform of realized DeltaC. Typical/expected ML at fixed observable inputs is determined by `(S_hat, b, psf)`, not by `S_true`. Truncating on ML is therefore a DeltaC cut, and the resulting distribution is the TRUNCATION of the conditional DeltaC distribution, NOT the intrinsic `p(deltaC | S_hat, b, psf)`.

Consequences:
- **Artificial skew** at truncation boundaries: skew can reach 1.0+ at
  ML=5 or ML=10 boundaries (truncation of Gaussian tails), while intrinsic
  skew is <0.3
- **Compressed variance**: restricting ML range restricts deltaC range
- **Misleading non-Gaussianity**: the truncated distribution looks
  non-Gaussian, but the intrinsic distribution IS near-Gaussian

### The correct method: S_hat residual analysis

1. **Bin by S_hat** (the observable), NOT by ML (the derived statistic)
2. **Subtract theoretical mean DeltaC** from each sample: residual = DeltaC - mean_theory
3. **Analyze the residual distribution**: mean, std, skew, kurtosis
4. **Select bins of interest** by their typical ML value (e.g., "S_hat bins
   where median ML ≈ 6-10"), but do NOT truncate the data within each bin

### Concrete example (highstat_1p3p_comparison, 300K samples)

Using CORRECT method (S_hat binning, no ML truncation):
- residual skew: 0.01-0.15 (near-Gaussian)
- residual kurtosis: -0.3 to +0.1 (near-Gaussian)
- r_std / sigma_theory: 0.93-1.00 (variance correctly predicted)
- residual mean: +0.3 to +0.6 (theory mean underestimates — needs correction)

Using WRONG method (ML=[5,10] truncation):
- skew at ML=5 boundary: +1.28 (artificial, from truncation)
- skew at ML=10 boundary: -1.27 (artificial, from truncation)
- skew in center (ML~7): +0.06 (coincidentally correct, but method is wrong)
- **Conclusion appears correct ("near-Gaussian at ML~6") but for wrong reasons**
- Worse: misses the +0.3-0.6 mean bias because residual method wasn't used

### Key insight: mean bias is the real issue, not shape

The Gaussian SHAPE is correct (skew<0.3, kurt<0.5), but the Gaussian
LOCATION is wrong (theory mean DeltaC underestimates by +0.3-0.6).
Without correcting the mean, P(ML>=6) computed from Gaussian approximation
has ~10-15% error. With mean correction, error drops to <1%.

The ML truncation method missed this because it analyzed p(ML) directly
rather than p(DeltaC - mean_theory), so the mean bias was invisible.

## The correct theory (CORRECTED 2026-05-15)

**Previous (WRONG)**: "Use 1-param theory Var(deltaC) = B_proxy · Phi(x) and apply mean correction."

**Correct**: Use `deltac_moments_3param(S_hat, b, psf, fitposition=True)` directly.
This function computes both mean and variance of deltaC conditioned on
(S_hat, b, psf) — **completely independent of S_true**.

```python
from lib.fit_mask_3param import deltac_moments_3param
mean_dC, var_dC = deltac_moments_3param(S_hat, b, psf, fitposition=True)
sigma_dC = np.sqrt(var_dC) # ← accurate! z-score std ≈ 1.0
```

### Key finding: sigma(deltaC) theory is accurate

From E021 simulation (150k realizations, Gaussian PSF):
- z-score = (deltaC_obs - mean_theory) / sigma_theory
- std(z-score) ≈ 0.95–1.05 across all (S_true, b) cells
- **No empirical correction needed for sigma(deltaC)**

### What needs correction

Only **E[deltaC]** has a ~2-5% systematic bias (the self-consistency
finding from I027). This propagates to E[ML] but NOT to sigma(ML).

| Quantity | Source | Needs correction? | How |
|----------|--------|-------------------|-----|
| E[deltaC] | `deltac_moments_3param()[0]` | YES (~2-5%) | k(ML) winginess model + factorized proxy |
| Var(deltaC) | `deltac_moments_3param()[1]` | **NO** | Theory is accurate |
| E[ML] | `detml_from_delta_c(E[deltaC])` | YES | Same as E[deltaC] |
| sigma(ML) | `|dML/ddC| * sqrt(Var)` | **NO** | Accurate from theory |

### Why the previous advice was wrong

The previous version said "Use 1-param theory Var = B_proxy * Phi(x)".
But B_proxy and Phi(x) are from the factorized proxy approximation, which
introduces sigma_eff and other fitted parameters. The exact formula
`deltac_moments_3param` uses the real PSF directly and needs no such
approximation. The G(x) "overdispersion" factor was an artifact of
comparing marginal catalog variance (which includes population mixing)
with conditional theory variance — not a failure of the theory.

## Numerical example (E021, Gaussian PSF, 50000/cell)

| S_true | b | ML_mean | CV(deltaC_3p) | H_var | sigma(ML) |
|--------|-----|---------|---------------|-------|-----------|
| 10 | 0.10 | 8.4 | 0.532 | 1.007 | 4.9 |
| 10 | 0.40 | 3.8 | 0.629 | 1.086 | 2.7 |
| 20 | 0.10 | 22.9 | 0.365 | 1.003 | 7.7 |
| 20 | 0.40 | 10.4 | 0.457 | 1.012 | 5.1 |
| 40 | 0.10 | 34.5 | 0.243 | 1.000 | 0.7 |
| 40 | 0.40 | 29.0 | 0.300 | 1.006 | 6.2 |

H_var ≈ 1.00 across all conditions. The large CV comes from S_hat Poisson
scatter, not from 3-param fitting effects.

## Catalog route (CORRECTED)

For catalog-based prediction where only (S_hat, b, OFFAXIS) are available:

1. Lookup PSF from CCF ELLBETA_PARAMS(OFFAXIS)
2. `mean_dC, var_dC = deltac_moments_3param(S_hat, b, psf)`
3. E[ML] = `detml_from_delta_c(mean_dC, nu=3)` → has ~2-5% bias, needs correction
4. sigma(ML) = `|dML/ddC| * sqrt(var_dC)` → **accurate, no correction needed**
5. Correct E[ML] using factorized proxy calibration or k(ML) winginess model

## Rules

0. **Promote project-specific invariants into the OS entry files** — if this trap applies, add the rule to `00_AI_BRIEFING.md`, `02_CURRENT_QUESTION.md`, and `03_TRUST_TABLE.md`, not just to this reference.

1. **Always report "Var(X | conditioned_on_what)"** — never just "Var(X)".
   The conditioning variable determines the physical meaning of the variance,
   and different conditionings can give values that differ by 3×.

2. **Always use the exact theory formula first** — don't substitute rough
   approximations that introduce spurious parameter dependencies (like S_true
   dependence in `conditional_DET_ML_width` that doesn't exist in the exact
   `deltac_moments_3param`).

3. **Never truncate on ML when analyzing conditional distributions** — ML is
   a derived statistic, not an independent observable. Bin by S_hat, subtract
   theory mean, analyze residuals. Use bin-level ML only for selecting which
   bins are of interest (e.g., "bins where typical ML ≈ 6").

4. **Separate shape from location** — even when the distribution SHAPE is
   near-Gaussian, the LOCATION (mean) may have systematic bias. The residual
   method (subtract theory mean first) exposes both shape properties and
   mean bias independently.

## Residual moment accounting

For samples in a bin, define:

```text
R_i = DeltaC_i - E_theory[DeltaC_i | S_hat_i, b_i, psf_i]
```

Then:

```text
mean(DeltaC) = mean(R) + mean(E_theory[DeltaC])
Var(DeltaC) = Var(R + E_theory[DeltaC])
DeltaC = R + mu_theory
Var(DeltaC) = Var(R) + Var(mu_theory) + 2 Cov(R, mu_theory)
```

Use `Var(R)` for residual width. Use `Var(R + mu_theory)` for the observed DeltaC width of a mixed bin. The approximation `Var(DeltaC) ≈ Var(R)` is valid only for narrow bins where `mu_theory` is nearly constant.
