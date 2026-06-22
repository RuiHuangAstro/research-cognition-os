# Semi-Analytical Model Discovery Pattern

## When to use
After ruling out multiple theoretical approaches (negative results), a simplified
parametric model based on physical intuition is derived and validated against
simulation data. This is the POSITIVE complement of the negative-result pattern.

## Pattern

### 1. Start from physical mechanism, not mathematical generality
After Edgeworth/Bartlett/extreme-value all failed, the key was identifying the
RIGHT physical variable: sigma_pos/sigma_PSF (position uncertainty / PSF width).

This ratio controls "how many effective independent positions the MLE optimizer
searches" — a concrete, measurable quantity, not an abstract expansion parameter.

### 2. Choose the simplest parametric form that respects boundary conditions
For k = sigma_obs / sigma_theory:
- k(0) = 1 (no compression when position is perfectly known)
- k → 0 as search freedom → infinity
- Monotonic decreasing

Simplest form: k = 1/sqrt(1 + alpha * r^2) where r = sigma_pos/sigma_PSF

### 3. Calibrate from simulation, then cross-validate
- Fit alpha on one dataset (b=0.1)
- Predict on independent dataset (b=0.4 → b=0.1)
- If alpha is stable across conditions → it's a physical parameter, not a fit artifact

### 4. Validate with variance decomposition
Law of total variance:
  Var(DC | S_hat) = E_x[Var(DC | S_hat, x)] + Var_x(E[DC | S_hat, x])
                   = intrinsic     + systematic

If systematic fraction is large → confirms position-residual covariance mechanism.

### 5. Compare with alternatives
| Approach | Params | RMS | Physical? |
|----------|--------|-----|-----------|
| k = 1/sqrt(1+alpha*r^2) | 1 | 3.8% | Yes |
| k = 1 - a*exp(-b*ML) | 2 | ~3% | No (phenomenological) |
| Edgeworth | 2+ | N/A | Wrong mechanism |
| Full simulation | 0 | exact | No formula |

### 6. Test on extended domain BEFORE declaring success
The semi-analytical model k=1/√(1+α·r²) with α=0.267 works for Gaussian PSFs (RMS 3.8%).
But when tested on ELLBETA (King+Gaussian) PSFs, it **predicts the wrong direction**:
- Model: wider PSF (σ_PSF=5.79 pix via 2nd moment) → smaller r → less compression → k closer to 1
- Data: ELLBETA shows MORE compression (k=0.806 vs Gaussian 0.906 at ML[2,5))

**Root cause**: σ_PSF defined as second moment is tail-dominated for King profiles.
The optimizer "sees" the PSF core, not the distant wings. The physical variable
(sigma_pos/sigma_PSF) is right, but the σ_PSF OPERATIONALIZATION is wrong for
non-Gaussian PSFs.

**Lesson**: A model that works on the calibration domain can fail catastrophically\non an extended domain — not just degrade, but predict the OPPOSITE of reality.\nAlways test on qualitatively different conditions (different PSF shape, not just\ndifferent S/b parameters).\n\n**Follow-up (2026-05-12)**: After 5 σ_PSF definitions all failed to unify α,\na winginess model was discovered: k = 1/√(1 + α · r² · (σ_2nd/FWHM)^γ).\nWith γ=-0.482, α=0.267 becomes universal across Gaussian and ELLBETA.\nThe winginess parameter (σ_2nd/FWHM) captures the core-vs-wing balance:\nGaussian = 1.0, ELLBETA = 2.89 → 2.89^(-0.482) ≈ 0.600 → α_eff = 0.160.\nThis needs validation on more PSF types before trusting.

### 7. Document limitations explicitly
- alpha calibrated from Gaussian PSF only — **ELLBETA validation FAILED**
- σ_PSF definition is ambiguous for non-Gaussian PSFs (2nd moment ≠ effective width)
- Not tested for off-center sources
- Not validated for high background
- Model may need PSF-dependent α or redefined σ_PSF_eff

### 8. Record in cognition OS
- New insight (I018): semi-analytical model
- Update parent insight (I016): add semi-analytical evidence
- Update stage (S09): record positive result AND extended-domain failure
- Update AI_BRIEFING: add to trusted insights BUT note ELLBETA limitation

## Why this matters
The negative-result pattern tells you what DOESN'T work. This pattern tells you
what to do AFTER ruling out dead ends: find the right physical variable, build
the simplest model, validate with cross-validation and variance decomposition.

## Real example from DET_ML_Uncertainty
- I017 (negative): Edgeworth/Bartlett/extreme-value cannot explain compression
- I018 (positive): k = 1/sqrt(1 + alpha*(sigma_pos/sigma_PSF)^2), alpha=0.267
- Key: the physical variable (sigma_pos/sigma_PSF) emerged from understanding
  the MECHANISM (position-residual covariance), not from trying more expansions.

## Key lesson
When mathematical generality fails (expansions, corrections), look for a
CONCRETE PHYSICAL QUANTITY that controls the effect. The right variable often
comes from understanding WHY the effect happens, not from formal mathematics.

**But**: finding the right variable is necessary but not sufficient. You must
also operationalize it correctly — sigma_pos/sigma_PSF works for Gaussian PSFs
where "PSF width" is unambiguous, but fails for King profiles where the
effective width for position search differs from the statistical second moment.
The PATTERN (physical variable → simplest model → validate) is sound; the\nEXECUTION (choosing the right operational definition of each variable) requires\ndomain-specific care.\n\n### 9. When the physical variable's operationalization fails, test the mechanism itself\n\nAfter 5 σ_PSF definitions all failed to unify α, the next question was:\nis the mechanism (noise spatial correlation → compression) even correct?\n\n**Test**: compute the correlation length of the constrained residual field Z_⊥.\n- If Z_⊥ has long-range correlation → mechanism confirmed, just need right ξ\n- If Z_⊥ is white noise → mechanism is WRONG, compression comes from elsewhere\n\n**Result**: Z_⊥ is white noise (ξ=0.5 pix = pixel scale) for both Gaussian and ELLBETA.\nThe ΔC landscape in position space also has the same correlation length (ξ≈2.54 pix).\n\n**Physical synthesis**: the compression is NOT about correlated noise — it's about\nhow the PSF gradient structure maps independent pixel noise into a correlated ΔC\nlandscape. The "σ_PSF" in the model is NOT a noise property but a PSF-shape property\nthat controls how many effective independent positions the optimizer can search.\n\n**Lesson**: when all operationalizations of a physical variable fail, question whether\nthe mechanism itself is correct. The residual-field correlation test is a decisive\nexperiment: if ξ_noise = ξ_pixel, then noise correlation cannot explain compression.