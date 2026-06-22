# Self-Consistency vs External Consistency: Validation Strategy for Scientific Pipelines

## Problem

When validating a theory against a reference implementation (e.g., our Python pipeline vs SAS emldetect), a systematic offset appears. The question is: is the theory wrong, or is the implementation different?

## Two-Question Framework

Split validation into two independent questions:

### 1. Self-Consistency (PRIMARY)
**Does the theory accurately describe our own pipeline's results?**

- Compares theory predictions to simulation results from our own pipeline
- The theory must pass this test before external validation matters
- Residual structure tests: trend vs parameters, chi2/ndof, bootstrap CIs
- If residuals are noise (no systematic structure), the theory is self-consistent
- **For the concrete quantitative method (ANOVA, bootstrap, error budget table), see [[self-consistency-validation-method]]**

**Example (DET_ML):**
- k(ML) model: RMS 1.9% (Gaussian), 4.6% (ELLBETA)
- Winginess model: RMS 4.5% (242 pts)
- Residuals: no trend vs r (p=0.06), no trend vs S (p=0.82)
- → **Theory is self-consistent at ~5%**
- E010b real-data path: 4% mean offset with significant off-axis dependence (ANOVA p<0.001) → winginess model needed

### 2. External Consistency (SECONDARY)
**Does our pipeline match the reference implementation?**

- Compares our pipeline to an external ground truth (e.g., emldetect)
- Systematic offset is a calibration constant, not a theory failure
- Decompose the offset into known sources (implementation details)
- If the theory is self-consistent, the offset can be calibrated away

**Example (DET_ML):**
- Our pipeline vs emldetect: ~3% ML offset (median ML_ratio ≈ 0.97)
- **Background gradient** (dominant, I029): emldetect uses `bkgimagesets` (spatially-varying map), Python uses flat `BG_MAP` value. Bkg relative std within 15px mask: 3.85% median. ML_ratio is strongly b-dependent: 0.79 (S=2.5, b=0.4) → 0.999 (S=320, b=0.025). Fix: use bkg map cutout instead of flat value.
- 4-step vs 8-step PSF: <0.5% (I025)
- CCF interpolation: <0.1%
- ~~Sub-pixel integration: ~2-5%~~ (SUPERSEDED by I029 — main pipeline already has sub-pixel precision via `build_psf(dx,dy)`)
- → **Offset is fixable (background treatment), not intrinsic**

## Error Budget Decomposition

When self-consistent, decompose the error budget:

| Source | How to estimate |
|--------|---------------|
| Statistical (finite N) | Bootstrap / jackknife per bin |
| Model parameterization | Chi2/ndof, cross-validation |
| PSF shape | Compare different PSF implementations |
| Optimizer | Benchmark with known truth (E023) |
| ML formula | Compare to analytical derivation |
| **TOTAL** | **RSS of above** |

For a concrete example with numbers, see [[self-consistency-validation-method]] Step 3.

## When to proceed to external consistency

Only after self-consistency is established:

1. Self-consistency established → put external consistency on Parking Lot
2. External consistency needed → calibrate the offset, don't fix the theory
3. If theory fails self-consistency → fix the theory first, then re-check

## Writing for papers

"Our theory is validated on our own pipeline with systematic uncertainty of ±5%. The ~3% median offset between our pipeline and SAS emldetect is primarily attributed to background treatment differences (spatially-varying map vs flat value) and can be corrected by using the background map directly."

## Key lesson: verify which pipeline the hypothesis applies to

When a hypothesis about a systematic offset comes from one session, verify it
applies to the main pipeline before implementing a fix. The "PSF sub-pixel
misalignment ~4%" hypothesis (I028) came from `fft_psf_wrapper.py` (which uses
`int(round(x))` integer placement), but the main pipeline `run_sb_grid_1k.py`
already uses `build_psf(x0+dx, y0+dy)` with sub-pixel precision. The FFT phase
shift module was implemented and verified but turned out to be unnecessary for
the main pipeline. The real offset source was background gradient (I029).

**Rule**: Before implementing a fix, `grep -rl` to check which code references
the buggy module. If no production code depends on it, the fix is lower priority.