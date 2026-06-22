# X-ray Imaging Extended Structure Analysis: Cognition OS Pattern

> Session: 2026-05-17, NGC 3079 superwind FXT analysis
> This is a worked example of building a cognition OS for an **imaging-based** X-ray project (as opposed to spectral or simulation projects).

---

## Project Type: Imaging Extended Structure

Unlike spectral analysis (M51/NGC891 pattern) or simulation studies (DET_ML pattern), imaging-based projects have these characteristics:

1. **Primary data**: Stacked count/rate/exposure maps (2D images), not spectra
2. **Goal**: Detect and characterize extended low-surface-brightness structures
3. **Challenge**: Dominant central emission + faint extended signal + PSF smearing
4. **Methods**: Image processing (filtering, subtraction, stacking), not spectral fitting
5. **Validation**: Morphological significance (azimuthal profiles, W/D ratios), not chi-squared

---

## Cognition OS Structure for Imaging Projects

### Stages

- **S01: Data stacking** — How were individual observations combined? What corrections (astrometric, exposure) were applied?
- **S02: Method development** — Which image processing methods were tested? Why? What are their assumptions?
- **S03: Quantitative analysis** — Azimuthal profiles, radial profiles, significance estimation
- **S04: Cross-validation** — Independent confirmation from other instruments/telescopes

### Insights (imaging-specific)

- Band selection rationale (soft band for thermal wind)
- PSF limitations on structure detection
- Method comparison results (which method is "best" and for what)
- Azimuthal asymmetry measurements (W/D ratios, wind excess)
- Point source subtraction completeness

### Experiments (imaging-specific)

Each method comparison is an experiment:
- Method name, principle, key parameters
- What it detected (or didn't)
- Assumptions and limitations
- Cross-method consistency check

### Trust Table (imaging-specific)

Key items to track:
| Item | Type | Trust criterion |
|------|------|-----------------|
| Stacked data quality | Data | Exposure time, number of observations, astrometric correction |
| Point source subtraction | Method | Detection threshold, mask growth, inpaint method |
| Energy band definition | Convention | Fraction of target signal in band |
| PSF FWHM | Constraint | Limits minimum detectable angular scale |
| Azimuthal asymmetry | Result | Significance level, consistency across methods |
| W/D ratio at specific radius | Result | Significance, systematic uncertainty |

---

## Key Method: Azimuthal-Median + 4-Fold Stacking

This is a general technique for detecting bipolar/asymmetric extended structures in X-ray images:

### Algorithm

1. **Point source removal**: Detect in hard band (where wind is faint), mask + inpaint
2. **Smooth**: Gaussian σ=3 pix (or instrument PSF-matched)
3. **Azimuthal-median subtraction**: At each radius, subtract the median count level. This removes the symmetric component (halo + CGM) while preserving azimuthal asymmetries.
4. **4-fold stacking**: Fold all 4 quadrants into Q1 by averaging. Boosts S/N by ~2x while preserving wind/disk asymmetry. **Critical**: must do az-median subtraction BEFORE 4-fold, otherwise the bright central emission floods all angles.
5. **Profile extraction**: Residual vs angle (0=disk, 90=wind) at fixed radii
6. **Wind excess**: (60-90° minus 0-30°) vs radius

### Why az-median first?

Raw 4-fold stacking averages the central bright emission across all angles, completely drowning the faint extended wind signal. Az-median subtraction removes this dominant symmetric component, so the 4-fold stacking operates on residuals where the wind signal is the dominant feature.

### Angle convention

For edge-on galaxies with bipolar wind:
- **Minor axis** (wind direction): angle = 90° from major axis
- **Major axis** (disk direction): angle = 0° from major axis
- **4-fold folding**: assumes bi-conical symmetry (N=S, E=W)

### Pitfalls

1. **Raw 4-fold fails for centrally concentrated sources** — always subtract az-median first
2. **Point sources near 0° (wind axis) artificially boost W/D** — mark on profiles
3. **PSF smearing limits minimum detectable scale** — FXT PSF ~1.4-2' FWHM
4. **Background/exposure edge effects at large radii** — W/D>1 may be systematic
5. **4-fold assumes axisymmetry** — real wind may be asymmetric; check with direct angle binning
6. **Az-median may over-subtract wide-angle winds** — if wind fills >60° from minor axis, median includes wind contribution

### Validation

- Cross-check with direct angle binning (no folding) — should show same trend
- Cross-check with independent instrument (XMM, Chandra)
- Bootstrap error estimation for significance claims
- Check for residual point source contamination at large radii

---

## NGC 3079 Worked Example

### Data
- Einstein Probe FXT stacked: 86.7h, 59 observations
- Soft band: 0.3-2.0 keV (89.5% of wind counts)
- Image: 600×600 pix, 9.67"/pix, 96.7' FOV
- 9 point sources removed (hard 5σ detection)

### Results
- Wind excess at r≈4' (~20 kpc): ~+0.6 counts, ~12σ
- W/D ratio >1 at r>7.8' (>40 kpc): peak ~1.5 at r≈9'
- W/D minimum at r≈5.5-6': cause unclear (interaction zone?)
- Best method: az-median (M6) for morphology, az-median+4fold for quantification

### Cognition OS files created
- 2 stages, 5 insights, 3 experiments, 1 session
- Key insight hierarchy: I001 (wind at 4') → I002 (W/D beyond 40kpc) → current question (cross-validation)