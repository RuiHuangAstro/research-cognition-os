# I044 PSF-Template Catalog Bridge Session Detail

**Date**: 2026-05-16 (v1) + 2026-05-17 (v2) + 2026-05-18 (v3)
**Project**: DET_ML_Uncertainty (XMM-Newton source detection statistics)

## v1 Session (2026-05-16)

See the original summary below. Key results:
- 408k rows, 500 reps/cell
- On-axis PASS, off-axis partial (±0.8σ scatter)
- scut=1.0 used in pilot
- Beyond-Fisher m0 sufficient

## v2 Session (2026-05-17)

### What changed from v1

| Parameter | v1 | v2 |
|-----------|-----|-----|
| Reps/cell | 500 | 1000 |
| Total rows | 408,000 | 816,000 |
| Clean rows | 405,641 | 811,194 |
| Pilot scut | 1.0 | 0.9 |
| Pilot S_fit filter | >0.1 | ≥5 |
| Beyond-Fisher model | m0 sufficient | m2 best (LOPO 0.095) |

### Critical new findings

1. **scut=0.9 effect is negligible**: dZ = -0.020 ± 0.009 (95% CI: [-0.038, -0.002]).
   - When theory and fit use the same mask, Z is invariant to mask size.
   - The v1→v2 on-axis shift of +0.24 was NOT scut — it was filter/sample changes.
   - **Implication**: scut convention mismatch is NOT the off-axis root cause.

2. **Azimuth-dependent PSF mismatch is the dominant catalog blocker**:
   - At same off-axis, Z varies by 1.46σ depending on azimuth.
   - Root cause: 31×31 template truncation + XMM mirror asymmetry.
   - At 6.26': Z ranges from -0.79 (az=+90°) to +0.67 (az=-90°).
   - At 8.85': Z ranges from -0.78 (az=-45°) to +0.69 (az=+45°).

3. **1000 reps fixes per-position low-S SE**:
   - v1: ALL 17 per-position S_fit<5 SE FAIL (0.05-0.53 vs target 0.05)
   - v2: ALL 17 per-position S_fit<5 SE PASS (0.009-0.010)
   - The threshold is sharp: need ~8000 samples per position×S_bin

4. **S<5 degenerate outliers identified**:
   - 0.17% of mask stress test samples have S_fit≈0.01, var_3p≈1.9e-8
   - Z values reach -2294 to -100
   - Clean cut: S_fit > 0.5 AND var_3p > 0.01

5. **Beyond-Fisher m2 now beats m0**:
   - m0(S_fit): LOPO worst 0.144
   - m2(S_fit, b, A2, W_eff): LOPO worst 0.095
   - 1000 reps reveals b and PSF shape contributions that 500 reps missed

6. **31×31 PSF template truncation**:
   - On-axis: 95.7% flux in 31×31
   - 12.5' off-axis: 89.1% flux
   - 14.0' off-axis: 88.7% flux
   - 401×401 templates exist but not yet used in pilot

7. **Simulation vs catalog gap**:
   - Simulation (scut=0.9): mean Z ≈ +0.32
   - Catalog (AT-template): mean Z = +0.16
   - Gap = -0.16σ, attributed to PSF model differences (emldetect vs psfgen)

### v2 Key Numbers

| Metric | v1 | v2 |
|--------|-----|-----|
| Global mean(Z) | +0.354 | +0.356 |
| Global std(Z) | 0.973 | 0.972 |
| S_fit>20 mean(Z) | +0.069 | +0.068 |
| S_fit>20 std(Z) | 0.979 | 0.978 |
| Per-position S<5 SE | FAIL | PASS |
| Beyond-Fisher LOPO | m0=0.144 | m2=0.095 |

### Updated remaining blockers

| Blocker | Severity | v1 assessment | v2 assessment |
|---------|---------|---------------|---------------|
| Azimuth PSF mismatch | HIGH | ±0.8σ scatter (unknown cause) | 1.46σ at same off-axis (root cause: 31×31 truncation + mirror asymmetry) |
| scut convention | HIGH | Suspected cause of off-axis offset | **RULED OUT** — effect is negligible |
| 31×31 truncation | MEDIUM | Not quantified | 11% flux loss at 14' — confirmed contributor |
| M2 templates | MEDIUM | Missing | Still missing |
| Per-source PSF | LOW | Not considered | Needed for precision off-axis work |
| Energy weight mismatch | LOW | Not considered | psfgen vs emldetect weights may differ |

## v3 Session (2026-05-18): Publication PSF Closure

### What changed from v2

Focus shifted from "run more simulations" to "isolate catalog PSF mismatch mechanism for publication".
Used multi-phase audit workflow with explicit GATE criteria per phase.

### Phase results

| Phase | Gate | Key Finding |
|-------|------|-------------|
| P0: V2 audit from CSV | PASS | All v2 numbers confirmed; S<5 raw mean(Z)=+0.920 |
| P1: 31x31 truncation | FAIL | s31 = exact crop of rebinned s401 (max diff=0.0). dZ<0.003σ, r=-0.24 wrong sign |
| P2: Per-source ratio | PASS | DC_obs/mu_3p ratio [0.905,1.105]. Azimuth 1.46σ→0.19σ at 8.85'. 97.3% variance reduction |
| P3: Convention matrix | FAIL | 9 variants, none explains 1.46σ azimuth spread. Normalization -4.1% to +4.8% position-dependent |
| P4: Matched cells | PARTIAL | 83.6% significant, S>20 mean |residual|=0.72σ |
| P5: Decision table | PASS | 9-row table with allowed paper wording per claim |
| P6: Figures | PASS | 4 figures (1col+2col each): ratio correction, matched cells, truncation, beyond-Fisher |

### Updated blocker assessment

| Blocker | v2 assessment | v3 assessment |
|---------|---------------|---------------|
| 31x31 truncation | 11% flux loss at 14' — contributor | **RULED OUT** — s31 is exact crop, dZ<0.003σ |
| Azimuth PSF mismatch | 1.46σ, cause unknown | **MECHANISM IDENTIFIED** — psfgen vs ELLBETA model difference, ratio correction reduces to 0.19σ |
| scut convention | Ruled out | Confirmed ruled out |
| Per-source PSF | Needed | Ratio correction works but needs per-position calibration |
| Convention mismatch | Under investigation | No single convention explains spread |

### Publication claims

CAN claim: theory validated at 0.07σ (S>20), beyond-Fisher m2 correction, 31×31 truncation ruled out, PSF model mismatch identified and empirically correctable.

CANNOT claim: catalog closure, off-axis production validation, any ML-bin evidence.

### Key technique: DC_obs/mu_3p ratio as PSF mismatch diagnostic

The per-position DC_obs/mu_3p ratio directly measures the net effect of all PSF model differences between psfgen and emldetect:
- ratio > 1: emldetect gives larger DeltaC than psfgen predicts (PSF too narrow in template)
- ratio < 1: emldetect gives smaller DeltaC (PSF too wide in template)
- Position-level ratio range [0.905, 1.105] = ±10% systematic
- 14/15 positions show S_hat-dependent ratio → PSF shape mismatch, not just normalization
- After correction: azimuth spread drops from 1.46σ to 0.19σ at 8.85'

### Key technique: Convention matrix for ruling out systematic explanations

When a systematic residual is observed, build a convention matrix varying ONE factor at a time:
1. scut (0.9 vs 1.0): dZ < 0.02σ, spread < 0.01σ
2. ecut (10-22 px): dZ < 0.003σ
3. Sub-pixel shift (0.0-0.5 px): dZ < 0.01σ
4. Normalization (±5%): large dZ but wrong direction
5. Energy weight: would need emldetect source code access

If no single factor explains the spread, the root cause is a position-dependent model difference (not a convention choice).

---

## v1 Session Summary (original, 2026-05-16)

This session executed a comprehensive I044 PSF-template catalog bridge run with 8 phases:

1. **Gate 0**: E025 reproduction from CSV (61,200 rows) — confirmed user audit numbers
2. **Phase 1**: P6 diagnosis — corrupted psfgen file, NOT detector boundary
3. **Phase 2**: High-stat simulation (408k rows, 17 positions, 8 S × 6 b, 500 reps/cell)
4. **Phase 3**: Beyond-Fisher correction modeling (m0-m3 comparison, LOPO validation)
5. **Phase 4**: Mask stress test (1.68M tasks, running at session end)
6. **Phase 5**: SAS catalog convention bridge (DET_ML, BG, S_hat, position conventions resolved)
7. **Phase 6**: Catalog pilot (19,452 sources, on-axis PASS, off-axis partial)
8. **Phase 7**: OS updates (AI_BRIEFING, TRUST_TABLE T43+T49 updated, T54-T58 added, I044 insight, log)

### v1 Key Numbers

- Raw: 408,000 rows → Clean: 405,641 (99.4%)
- Global: mean(Z)=+0.354, std(Z)=0.973
- S_fit>20: mean(Z)=+0.069, std(Z)=0.979
- S_fit>50: mean(Z)=+0.024, std(Z)=0.999

### Convention Bridge (confirmed in both v1 and v2)

- DET_ML = -ln(gammaincc(1.5, DeltaC/2)), nu=3
- PN_4_BG = counts/pixel (direct)
- S_hat = PN_4_RATE × PN_4_EXP
- IMPIX = round(FITS_pixel) - 1
- MASKFRAC > 0.8 required
- Sum(PN_4_DC + M1_4_DC + M2_4_DC) / (2 × EP_4_DET_half_DELTAC) = 0.9998

### Coding Pitfall

- `lib/fit_mask_3param.py` exports `weighted_deltac_moments_3param` (lowercase 'c' in 'deltac')
- Import with capital 'C' causes ImportError only at runtime (multiprocessing pool lazy loading)