# X-ray temperature-mapping pattern (domain-specific)

> Extracted from `SKILL.md` to keep the skill domain-neutral. This is an **X-ray astronomy**
> analysis pattern, not a general cognition-OS rule. It is kept as a reference for X-ray
> projects; the general skill body does not need it.

### Multi-Method Temperature Mapping Pattern

When characterizing 2D temperature structure in extended X-ray sources (galaxy halos, cluster outskirts), use multiple independent methods with cross-validation:

**Method hierarchy (by S/N requirement)**:
1. **Full spectral fitting** (Sherpa/XSPEC APEC): Gold standard, needs ~2000 counts/region. Produces kT ± confidence. Slow (~5-10 min/region).
2. **5-band Poisson MLE**: Fits APEC model to counts in 5 energy bands simultaneously. Needs ~500 counts. Fast (~1s/region after pre-extraction). ~2% systematic vs spectral fitting.
3. **3-band color-color diagram**: C1=M/S, C2=H/M compared to APEC model track. Needs ~200 counts. Loses spatial information in global C-C plot — must bin spatially to show azimuthal variations.
4. **Hardness ratio (HR)**: HR=(H-S)/(H+S). Needs ~100 counts. **NOT reliable for direct kT calibration** — soft proton contamination dominates (SP flux ~9× source flux in hard band). Relative angular variations may be robust if SP is spatially uniform.

**Key pitfalls**:
- **HR→kT is NOT viable**: SP contamination in 2-5 keV band makes absolute HR→kT calibration unreliable. Only use HR for relative comparisons (e.g., N vs S at same radius).
- **3-band MLE is degenerate**: Need ≥5 bands to break kT-Z degeneracy. 3-band gives wrong kT for Z≠0.3 solar.
- **Background systematics are small**: Comparing 3B.background_20240601 vs 4.background for same regions: mean |ΔkT| = 0.007 keV (0.9%). Poor fit quality (rstat>2) is NOT caused by background choice.
- **Color-color diagram needs spatial binning**: A global C-C plot with all regions overlaid loses azimuthal information. Must label points by quadrant or create separate C-C plots per angular sector.
- **Adaptive bin MLE requires pre-extraction**: Extracting counts from event files per adaptive bin is too slow for subagent. Pre-extract all counts to JSON, then run MLE in pure Python.

**Cross-validation protocol**:
1. Compare 5-band MLE kT vs spectral fitting kT at overlapping regions (expect <5% difference)
2. Compare Chandra HR angular pattern vs XMM kT angular pattern (expect same sign, not same magnitude)
3. Compare different background datasets for same regions (expect <2% difference)
4. If methods disagree, diagnose: is it S/N, systematic, or physics?

**Real example (M104 CGM)**: 5-band MLE R4-6 NE=0.680 keV vs v18 spectral 0.669 keV (+1.6%); SE=0.780 vs 0.810 (-3.7%). Chandra HR confirms N+NE cooler than S+SE (4.3σ). Background systematics <0.02 keV.
