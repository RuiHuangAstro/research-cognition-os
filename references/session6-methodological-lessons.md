# DET_ML_Uncertainty Session 6 Learnings (2026-05-13)

> Methodological lessons from winginess model validation + cross-session impact analysis.
> Extracted for the research-cognition-os skill reference.

---

## Lesson 1: σ_PSF Definition Changes Can Flip Model Parameter Signs

When model `k = 1/√(1 + α · r² · W^γ)` uses different r definitions:
- `r = σ_pos / (FWHM/2.355)` → γ = -0.482 (winginess "cancels" σ_PSF difference)
- `r = σ_pos / FWHM` → γ = +0.882 ≈ +1.0 (winginess "amplifies" compression)

This is NOT a numerical coincidence — it's a fundamental change in physical meaning.
The correct interpretation (γ=+1.0, W as positive amplifier) only becomes clear with
the more natural variable definition (r = σ_pos/FWHM).

**Rule**: When a model parameter's sign/magnitude changes dramatically after
redefining an operationalized variable, re-examine the physical meaning rather
than just comparing numbers.

## Lesson 2: Use Existing Data Before Running New Simulations

When validating a model under new conditions:
1. **First**: Check if existing simulation data covers the needed parameter space
2. **Second**: Do zero-cost analysis with existing data to confirm model viability
3. **Third**: Only then invest compute resources in new simulations

Real example: 179 Gaussian + 63 ELLBETA = 242 existing data points sufficed
to validate the winginess model (RMS=4.4%, BIC improvement Δ=37). New King PSF
simulations timed out at 300s with grid-search 3-param fitting, producing
sigma_ratio ≈ 1.0 (no compression detected) — wrong because the grid was too
coarse and S/N too high.

## Lesson 3: Cross-Session Impact Analysis Protocol

When another session reports a major finding (e.g., I025: 8-step vs 4-step <0.5%):

1. List ALL affected insights/experiments/bugs
2. Assess trust level change for each affected item
3. Check if the finding unblocks previously stuck work
4. Update AI_BRIEFING + TRUST_TABLE + relevant stage/insight files
5. Identify newly opened research directions
6. Don't do only local updates — a finding's ripples may reach seemingly
   unrelated cognitive nodes

Real example: I025 (spokes negligible for DET_ML) affected:
- B001 Bug4 severity: Medium → Low
- Spoke amplitude 2.7-2.9×: "unresolved" → "no impact on DET_ML"
- T11 (Python vs SAS off-axis): Medium → Medium-High
- Paper Section 2: can now state "4-step sufficient" with evidence

## Lesson 4: PSF Template Pre-computation vs On-the-fly Generation

Speed comparison for 3-param Cash fitting:
- `psf_model.build()` with 7×7 sub-pixel integration: ~5 ms/call
- Pre-computed template + `ndimage.shift(order=3)`: ~0.1 ms/call
- Speed ratio: **50x**

For 84,000 fits (E010): 8 hours → 10 minutes.

**Rule**: When PSF shape doesn't change during fitting (only position shifts),
ALWAYS pre-compute the template and use ndimage.shift. Only use on-the-fly
generation when PSF shape itself varies with position (e.g., off-axis ellipticity
requiring multiple templates for interpolation).

## Lesson 5: Bug Severity Should Reflect Impact on Core Scientific Conclusions

Spoke amplitude 2.7-2.9× too large sounds severe (PSF shape deviation),
but its impact on DET_ML is <0.5% (I025). Therefore B001 Bug4 should be
rated "Low", not "Medium".

**Rule**: Bug severity = max(impact on intermediate quantities,
impact on core conclusions), but final rating should be based on
core conclusions. A seemingly severe bug that doesn't affect the
scientific question being asked is low priority.

## Lesson 6: Winginess Model Validation — Combined Data Approach

The key insight for validating the winginess model was combining data from
two independent PSF types (Gaussian + ELLBETA) into a single dataset, then
fitting a universal model against a PSF-type-specific model.

Model comparison:
| Model | Params | RMS | BIC |
|-------|--------|-----|-----|
| Simple: k=1/√(1+α·r²) | 1 | 0.0485 | -1459 |
| Winginess: k=1/√(1+α·r²·W^γ) | 2 | 0.0444 | -1496 |
| Separate: α_G, α_E | 2 | 0.0444 | -1496 |

Winginess and Separate models are **mathematically equivalent** at γ=0.882
(α_eff matches to 10^-4). Fixing γ=1.0 costs only ΔRMS=0.0001.

**Pattern**: When two models with the same number of parameters give
identical BIC, they are equivalent reparameterizations. The one with
clearer physical meaning (winginess model) is preferred.