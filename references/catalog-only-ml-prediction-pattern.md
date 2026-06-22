# Catalog-Only ML Prediction Pattern

Source: DET_ML_Uncertainty session 7 (2026-05-13), corrected 2026-05-15

## Problem Pattern

When a theory requires full simulation data (PSF model, background map, etc.) but the user only has catalog-level parameters (S_det, b, OFFAXIS, MASKFRAC), can the theory still predict the key output (ML distribution) with useful accuracy?

This is the "shortcut path" vs "full replication path" problem.

## Critical Correction (2026-05-15)

**Previous version** claimed sigma(deltaC) needs G(x) empirical correction — **WRONG**.

`deltac_moments_3param(S_hat, b, psf)` gives Var(deltaC) that is validated
accurate (z-score std ≈ 1.0). Only E[deltaC] needs correction (~2-5% bias).
The "4 correction levels" table below applies to E[ML] only, not sigma(ML).

## Method

### 1. Separate mean from variance

Before listing correction levels, first establish:
- **E[deltaC]**: from theory, needs empirical correction for ~2-5% bias
- **Var(deltaC)**: from theory, **already accurate** (z-score std ≈ 1.0)

This separation is essential. Do NOT apply empirical dispersion corrections
(G(x), H_var) to sigma(deltaC) — they are artifacts of mixing conditional
and marginal variances.

### 2. Decompose E[deltaC] corrections into levels

List every correction the theory needs, in order of importance:
- Level 1: Core mean prediction (e.g., sigma_eff for factorized proxy)
- Level 2: Physical corrections (e.g., k(ML) 3-param compression)
- Level 3: Empirical corrections (e.g., r(OFFAXIS) lookup table)
- Level 4: External calibration (e.g., emldetect constant)

### 3. Ablation study

For each level, compute:
- Bias after adding this level
- Uncertainty after adding this level
- Marginal contribution (how much this level improved over previous)

### 4. Identify calibration constants

Check whether external calibration constants (like kappa for deltaC scaling) are:
- **Constant** across the parameter space → absorbed into single fitted parameter
- **Parameter-dependent** → need a lookup table or parametric form

Real example: kappa = 2.28 ± 0.01 is OFFAXIS-independent across 3 bins (0-5', 5-10', 10-15'), meaning it's already absorbed by sigma_eff fitting.

### 5. Identify the bottleneck correction

The correction that reduces bias the most but requires the most effort to calibrate.

Real example: r(OFFAXIS) reduces bias from 5% to 2% but requires simulation or empirical calibration at each off-axis angle.

## Key Results from DET_ML

### E[ML] correction levels (applies to mean only)

| Correction | Bias (E[ML]) | Uncertainty | Needs |
|-----------|------|-------------|-------|
| sigma_eff (1p mean) | ~3% | ~15% | 1 fitted parameter |
| +k(ML) | ~5% | ~10% | alpha, beta (2 params) |
| +r(OFFAXIS) | ~2% | ~8% | lookup table (5 bins) |

### sigma(ML) — reporting transform, not primary statistic

Primary statistics should be computed in `DeltaC` residual space. For reporting,
`sigma(ML) = |dML/d(deltaC)| * sqrt(Var(deltaC))`, where `Var(deltaC)` comes from
`deltac_moments_3param(S_hat, b, psf)`. This is a local delta-method propagation,
not a license to treat ML itself as Gaussian or to perform ML cuts.

### Final at ML~10

ML = 10.0 ± sigma(ML) (theory-accurate) with ~2% mean bias (correctable)

## Critical Insight: r(OFFAXIS) is the key, not W(OFFAXIS)

The winginess model k = 1/sqrt(1 + alpha * r^2 * W) has two OFFAXIS-dependent variables:
- W (PSF shape second-moment/FWHM): varies 0.48-0.68 (modest)
- r (sigma_pos/sigma_PSF): varies 0.71-1.29 (dominant!)

U-shaped r(OFFAXIS): near-axis r large (PSF narrow → large sigma_pos/sigma_PSF), mid off-axis r small (PSF wide), far off-axis r large (PSF elliptical → harder to locate).

## When to use this pattern

- User says "I want to use the theory on catalog data directly"
- User distinguishes between "full replication" and "shortcut" approaches
- User asks "how well can we do without X?" (where X is expensive simulation data)
- The theory has multiple correction levels that can be evaluated independently

## Pitfall: Don't invent empirical corrections for already-accurate theory

When the exact theory formula (e.g., `deltac_moments_3param`) already gives
accurate variance, do NOT add empirical overdispersion factors (G(x)) based
on comparing marginal catalog scatter with conditional theory variance. The
marginal scatter includes population mixing (different S_true in same bin),
which is NOT a theory failure. See `references/variance-conditioning-trap.md`.