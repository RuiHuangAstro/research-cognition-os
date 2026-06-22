# M104 CGM 2D kT Map — Orchestrator Session (2026-05-19)

## Session Summary

Two rounds of subagent deployment (7 tasks total, 5 completed, 2 timed out but produced partial results) to characterize M104's CGM 2D temperature structure.

## Round 1: Three Subagents (All Completed)

### Subagent A: 5-band Poisson MLE Temperature Map
- **Goal**: Produce 2D kT map using 5-band Poisson MLE on angular sector data
- **Result**: SUCCESS. 34 data points across 5 radial bins × 2-8 angular sectors
- **Key finding**: R4-6 NE=0.680 keV (+1.6% vs v18 0.669), SE=0.780 keV (-3.7% vs v18 0.810)
- **3-band vs 5-band**: 3-band MLE is degenerate for kT<0.8 keV; 5-band required
- **Files**: `grid_temperature_map.py`, `kT_2d_map_cartesian.png`, `kT_map_5band_mle.csv`

### Subagent B: XMM Band Ratio HR→kT
- **Goal**: Create band ratio temperature map from XMM event files
- **Result**: SUCCESS (but negative finding)
- **Key finding**: HR→kT is NOT viable. SP contamination ~9× source in hard band
- **Implication**: Must use spectral fitting or 5-band MLE, not simple HR
- **Files**: `band_ratio_temperature_map.py`, HR maps

### Subagent C: Background Cross-Validation (3B vs 4.background)
- **Goal**: Compare kT from different background datasets
- **Result**: SUCCESS. Fast and conclusive.
- **Key finding**: mean |ΔkT| = 0.007 keV (0.9%). Poor rstat from 3B is NOT kT bias.
- **Files**: `run_v18_fit_bkgtype.sh`, comparison CSV

## Round 2: Three Subagents (1 Completed, 2 Timed Out)

### Subagent D: Adaptive Bin 5-band MLE
- **Goal**: Run 5-band MLE on all 105 adaptive bins
- **Result**: TIMEOUT. No partial results.
- **Root cause**: Count extraction from event files per bin was too slow
- **Lesson**: Pre-extract all counts to JSON before running MLE

### Subagent E: Color-Color Diagnostic Diagram
- **Goal**: Create multi-band color-color plot for M104 CGM
- **Result**: TIMEOUT but produced useful partial results
- **Key finding**: Global C-C plot loses spatial information — must bin by quadrant
- **Files**: `color_color_diagnostic_3band.png`, `kT_map_color_color_3band_v2.png`, `comprehensive_color_diagnostic_MOS2.png`

### Subagent F: Chandra 8-sector HR Map
- **Goal**: Refined Chandra HR map at 8 sectors × 4 radial bins
- **Result**: SUCCESS. 32 regions extracted.
- **Key finding**: N+NE cooler than S+SE at R4-6: ΔHR = -0.077 ± 0.018 (4.3σ)
- **HR→kT calibration**: Weak Spearman r=0.11 (not significant). Absolute calibration unreliable; relative angular variations robust.
- **Files**: `chandra_8sector_hr_map_final.py`, `chandra_8sector_hr_results_final.csv`, `chandra_xmm_combined_polar.png`

## Key Scientific Conclusions

1. **NE cool gas confirmed by 3 independent methods**: v18 spectral (0.669 keV), 5-band MLE (0.680 keV), Chandra HR (4.3σ softer)
2. **HR→kT direct calibration is NOT viable**: SP contamination dominates
3. **Background systematics <0.02 keV**: 3B vs 4.background difference is negligible
4. **Color-color needs spatial binning**: Global C-C plot loses azimuthal info
5. **Adaptive bin MLE needs pre-extraction**: Too slow to extract counts on-the-fly

## Orchestrator Performance Lessons

- Subagent timeout is #1 failure mode (2/7 timed out)
- Tasks needing CIAO/Sherpa are 3-5× slower than pure-numpy tasks
- Pre-extract data before delegating (count extraction > MLE fitting)
- Provide environment setup as shell wrapper, not inline commands
- Color-color subagent: useful partial results even on timeout
- Background comparison subagent: fast and conclusive (0.007 keV)
- Chandra HR subagent: completed with 4.3σ result

## Stale Background Process Issue

15+ stale background processes from pre-APEC-fix v18.py continued firing notifications for 2+ hours after the fix. Each produced ValueError or broken-APEC output, but none overwrote the correct CSV files. Prevention: kill old processes and clean up old wrapper scripts before deploying fixes.

## Files Created This Session

### Cognition OS
- `insights/I028_4sector_kt_northern_cool_gas.md`
- `insights/I029_subagent_triad_5band_mle_hr_unreliable_bkg_systematics.md`
- `insights/I030_orchestrator_round2_chandra_colorcolor.md`

### Scripts
- `grid_temperature_map.py` (subagent A)
- `band_ratio_temperature_map.py` (subagent B)
- `chandra_8sector_hr_map_final.py` (subagent F)
- `color_diagram.py` (subagent E, partial)

### Figures
- `figure/kT_2d_map_cartesian.png/pdf` (5-band MLE Cartesian)
- `figure/kT_profile_5band_mle_1col/2col.png/pdf` (5-band MLE profiles)
- `figure/chandra_8sector_hr_map_polar_final.png/pdf` (Chandra HR)
- `figure/chandra_xmm_combined_polar.png/pdf` (combined 3-panel)
- `figure/kT_map_color_color_3band_v2.png` (color-color kT map)
- `figure/comprehensive_color_diagnostic_MOS2.png` (MOS2 color diagnostic)