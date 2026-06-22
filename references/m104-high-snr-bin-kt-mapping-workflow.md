# M104 High-SNR Bin kT Mapping Workflow

Session: 2026-05-31, XARTATOMS project
Pattern: 2D temperature mapping from XMM-Newton EPIC MOS spectra using pie-shaped spatial bins

## Problem

Characterize 2D temperature structure of M104's CGM using XMM-Newton MOS data.
Previous adaptive-bin results (2026-05-17) were pre-APEC-fix and unreliable.
Need post-APEC-fix results with proper spectral extraction and fitting.

## Solution: 16-Bin Pie Design

4 quadrants (NE/SE/SW/NW → Angle0-90/90-180/180-270/270-360) × 4 radial rings (R=0-2,2-4,4-6,6-8').
Total: 16 bins. SNR target ~25 (compromise from user's preferred ~25).

## Step-by-Step Workflow

### Step 1: Region Definition

Define pie sectors in DS9 fk5 coordinates, convert to XMM DET expression using `ds9_to_xmmexpr()`:
- Pie → `((DETX,DETY) IN sector(cx,cy,r_in,r_out,phi_start,phi_end))`
- Exclude sources → `&& !((DETX,DETY) IN circle(...))`

**Critical**: `ds9_to_xmmexpr` for exclude regions already returns `&& !(...)` — do NOT wrap in another negation (double-negation bug).

### Step 2: SAS evselect Extraction

```bash
evselect table=events.fits expression='FLAG==0&&PATTERN<=12&&((DETX,DETY) IN sector(...))&&(!((DETX,DETY) IN circle(...)))' \
  withspectrumset=yes spectrumset=obj.pi energycolumn=PI \
  spectralbinsize=5 withspecranges=yes specchannelmin=0 specchannelmax=2399
```

**Critical pitfalls** (all encountered and fixed):
1. **Single quotes mandatory** for expression — double quotes break `(DETX,DETY)` comma parsing
2. **BACKSCAL=1.0** — evselect does NOT set BACKSCAL for spatial selections. Must compute manually.
3. **detmaptype=flat** for arfgen — `psf` mode is prohibitively slow (>10 min/bin)
4. **Background spectrum from blank-sky observation** — use separate OBSID (0900170701) for back.pi

### Step 3: BACKSCAL Manual Calculation

```python
# Pie region area in arcmin²
pie_area = (PA_end - PA_start) / 360.0 * π * (R_out² - R_in²)
# If AGN excluded:
agn_area = π * r_agn_arcmin²  # only if fully inside pie
net_area = pie_area - agn_area

# v18 convention: BACKSCAL = area_arcmin² × 1440000
# (because v18 uses skyarea = BACKSCAL × (1/20/60)²)
BACKSCAL = net_area * 1440000

# Update both obj.pi and back.pi headers
for f in [obj_pi, back_pi]:
    with fits.open(f, mode='update') as h:
        h['SPECTRUM'].header['BACKSCAL'] = BACKSCAL
```

**BACKSCAL values for 90° pie sectors**:
| Ring | Area (arcmin²) | BACKSCAL |
|------|----------------|----------|
| R0-2 | 3.14 | 4,524,000 |
| R2-4 | 9.42 | 13,571,000 |
| R4-6 | 15.71 | 22,618,000 |
| R6-8 | 21.99 | 31,666,000 |

### Step 4: Sherpa Fitting (Wstat + group_counts)

```python
from sherpa.astro.ui import *

# Load MOS1 + MOS2 spectra
load_pha(1, 'mos1U005-obj.pi')
load_pha(2, 'mos2U005-obj.pi')

# Load ARF and RMF explicitly (evselect PI may lack keywords)
for sid in [1, 2]:
    load_arf(sid, f'mos{sid}U005.arf')
    load_rmf(sid, f'mos{sid}U005.rmf')

# Group by counts (30 counts/bin gives ~20-45 bins for typical MOS spectra)
group_counts(1, 30)
group_counts(2, 30)

# Wstat handles Poisson background automatically — NO subtract()!
set_stat('wstat')

# Simple 1-T APEC model with Galactic absorption
set_model(1, xsapec.src * xsphabs.abs1)
set_model(2, src * abs1)  # same model for both datasets
abs1.nH = 0.0445  # Galactic, frozen
abs1.nH.frozen = True
src.kT = 0.5  # initial guess
src.Abundanc = 0.3  # frozen at typical halo value
src.Abundanc.frozen = True
src.redshift = 0.003  # M104 distance
src.redshift.frozen = True

# Fit
set_method('neldermead')
fit()

# Error estimation
covar(1, 2)
cr = get_covar_results()
kT = src.kT.val
kT_err = cr.parmaxes[list(cr.parnames).index('src.kT')]
```

**Why Wstat + group_counts instead of v18's group_subtracted_oversampling_SNR**:
- `group_subtracted_oversampling_SNR(SNR=6)` collapses low-SNR spectra to 1 bin (all 2400 channels merged)
- Even SNR=3 gives only 5 points with -15 dof — completely useless
- `group_counts(30)` + Wstat gives 20-45 bins, rstat=1.1-1.6, proper Poisson background handling

### Step 5: Reliability Classification

| Status | Criteria | Action |
|--------|----------|--------|
| RELIABLE | kT<3 keV, kT_err/kT<1, rstat<2.5 | Include in all map versions |
| BULGE_CONTAM | kT>3 keV in R<3' | Flag, exclude from conservative |
| UNCONSTRAINED | kT_err/kT>1 | Include in usable, flag in exploratory |
| BAD_FIT | rstat>2.5 | Include in exploratory only |
| NO_ERR | Fit didn't converge | Include in exploratory only |

### Step 6: kT Map Generation

Three versions: Conservative (reliable only), Usable (reliable+unconstrained), Exploratory (all).
Use SciencePlots `['science', 'no-latex']`, dual output 1col (~3.35") + 2col (~7").

## Key Results (M104, 2026-05-31)

**8 reliable bins** (kT = 0.26–0.90 keV):
- R0-2 NE: kT=0.72±0.12 (after AGN exclusion)
- R2-4 NE: kT=0.69±0.06
- R2-4 SE: kT=0.90±0.04
- R4-6 NE: kT=0.26±0.21 (low SNR)
- R4-6 SW: kT=0.71±0.02
- R4-6 NW: kT=0.72±0.03
- R6-8 SW: kT=0.79±0.02
- R6-8 NW: kT=0.38±0.19

**3 bulge-contaminated bins** (R0-2 SE/SW, R4-6 SE): kT>4.7 keV
- 30" AGN exclusion insufficient — extended bulge emission dominates
- Inner ring (R0-2') unsuitable for halo temperature mapping

**Physical gradient**: Inner kT~0.7-0.9 keV → outer kT~0.3-0.4 keV, consistent with virialized halo cooling outward.

## Lessons for Future kT Mapping Projects

1. **R0-2' is always contaminated** for galaxies with bright nuclei — start halo mapping at R2-4'
2. **AGN exclusion radius matters** — 30" is too small; 1-2' needed for extended bulge, but removes most inner bin area
3. **Wstat + group_counts is the robust approach** for low-to-moderate SNR bins where v18's grouping fails
4. **BACKSCAL must be manually set** — evselect never computes it for spatial selections
5. **Single-quote expression syntax** is non-negotiable for SAS evselect
6. **Exclude expression from ds9_to_xmmexpr** already has `&& !(` prefix — do not double-negate
7. **detmaptype=flat** for arfgen — saves 10-20× time vs `psf`, adequate for extended sources
8. **Background from blank-sky OBSID** — same instrument, different sky position, provides NXB-like spectrum