# First-Principles Derivation of Empirical Constants: EVT Decomposition and Its Limits

> Pattern from DET_ML_Uncertainty direction C (2026-05-13, revised 2026-05-13):
> decomposing an empirically calibrated constant into physically interpretable
> components using extreme value theory of random fields. **CRITICAL UPDATE**:
> the original decomposition was found circular — this file documents both the
> valid pattern and the circularity pitfall.

---

## The Pattern (Valid Parts)

When a semi-analytical model has an empirically calibrated parameter (e.g., α ≈ 0.325
in k = 1/√(1 + α·r²·W)), the EVT framework provides:

1. **Identify the mathematical class** — What class of problem is this?
   (e.g., "finding the max of a correlated random field over a search region")
2. **Compute the "bare" coefficient from generic theory** — Use numerical
   simulation of the generic class (e.g., 2D Gaussian random field maxima
   → c = 0.74 from k = 1/√(1 + c·η²))
3. **Match models** — The EVT formula k = 1/√(1 + c·η²) and the winginess
   model k = 1/√(1 + α·r²·W) must give the same k. This defines:
   η² = (α/c)·r²·W = c'·r²·W, where c' = α/c = 0.439
4. **Interpret c' physically** — c' is the "effective search efficiency":
   the ratio of the real optimizer's variance reduction to the idealized
   EVT prediction. c' < 1 because the real optimizer is less efficient
   than the global-maximum EVT search.

## The Circularity Pitfall (CRITICAL)

### What went wrong

The original decomposition claimed:

```
α = c · c' / W_ref
```

with c = 0.74 (EVT), c' ≈ 0.5 (geometric), W_ref = 1.126 (Gaussian PSF).
This gave α = 0.74 × 0.5 / 1.126 = 0.329 ≈ 0.325 (1% match).

**But c' was NOT independently derived.** Setting c' = α/c:

```
α = c · (α/c) / W_ref = α / W_ref
```

This requires W_ref = 1, contradicting W_ref = 1.126. The "1% match"
was coincidental, not a derivation.

### The back-substitution test

**Mandatory check for any parameter decomposition**: substitute the
decomposition back into the original equation. If you get a tautology
or contradiction, the decomposition is circular.

Example:
- Decomposition: α = c · c' / W_ref
- Claim: c' is independently derived ≈ 0.5
- Back-substitution: c' = α/c → α = α/W_ref (contradiction if W_ref ≠ 1)
- Verdict: CIRCULAR — c' is not independent of α

### Why the 1% match was coincidental

The apparent match comes from choosing c' ≈ 0.5 ≈ α/c = 0.439, which
is close but not exact. The residual error (0.5 vs 0.439) is absorbed
by the W_ref factor, making the decomposition look like a derivation
when it's actually a reparametrization.

## What IS valid: c' as effective search efficiency

The decomposition α = c · c' is valid as an INTERPRETATION, not a
DERIVATION. It tells us:

- c = 0.74: the shape of k(η) from EVT (well-determined numerically)
- c' = α/c = 0.439: the effective search efficiency (derived from data)
- c' < 1 means the real optimizer achieves 44% of the idealized compression

The reasons c' < 1 (each reducing the effective N_eff):
1. Nelder-Mead finds local maxima, not the global maximum
2. The ΔC landscape has quadratic drift (signal peak), limiting search
3. Amplitude S is re-optimized at each position, changing the landscape
4. Poisson noise has non-Gaussian structure

## Key Result: Gaussian Field + Drift Model

Direct numerical simulation of F(x,y) = -κ/2·(x²+y²) + Z(x,y) where
Z is a 2D Gaussian random field confirms:

- The model DOES produce compression (k < 1) — purely geometric effect
- But it OVERPREDICTS compression by ~6× compared to real data
- With R_eff ≈ 1.5σ_pos, the Gaussian model matches c' ≈ 0.3
- The real optimizer has R_eff ≈ 0.6σ_pos (from winginess model matching)
- The 2nd-order Taylor expansion predicts Var_3p > Var_1p (wrong direction!)
  → compression is a beyond-Fisher, nonlinear effect

| R/σ_pos | k (sim) | c_eff |
|---------|---------|-------|
| 0.5     | 0.998   | 4.41  |
| 1.0     | 0.987   | 0.70  |
| 1.5     | 0.971   | 0.31  |
| 2.0     | 0.957   | 0.20  |
| 3.0     | 0.935   | 0.13  |
| 5.0     | 0.925   | 0.11  |

The c_eff ≈ 0.31 at R = 1.5σ_pos is closest to the empirical c' = 0.44.

## Pitfalls

1. **⚠️ Back-substitution test is MANDATORY** — For any decomposition
   α = f(x₁, x₂, ...), substitute back and verify it doesn't reduce to
   α = α or a contradiction. If it does, the decomposition is circular.
2. **Don't claim a "derivation" from a reparametrization** — α = c·c'
   with c' = α/c is a reparametrization, not a derivation. It provides
   physical interpretation but doesn't reduce the number of free parameters.
3. **The correction factor c' is NOT universal** — It depends on the
   optimizer, noise structure, and landscape shape. Don't transfer c'
   between problems.
4. **2nd-order Taylor expansion can predict the WRONG direction** — For
   nonlinear statistics like ΔC at the optimizer's position, the 2nd-order
   expansion gives ΔC(x̂) = ΔC(0) + (κ/2)·dr², predicting Var_3p > Var_1p.
   But the actual observation is Var_3p < Var_1p (compression). The linear
   approximation breaks down because the optimizer's position choice is
   correlated with the noise in a way that 2nd-order terms miss.
5. **Numerical simulation of generic class is cheap** — 3000 simulations of
   128×128 fields takes ~30 seconds. Do this FIRST before any analytical work.
6. **Gaussian field + drift overpredicts** — The simple model captures the
   qualitative mechanism but overpredicts by ~6×. The real ΔC landscape
   has Poisson structure, amplitude coupling, and optimizer-specific behavior.

## Related

- Adler & Taylor 2007, "Random Fields and Geometry" — theoretical foundation
- I026 in DET_ML_Uncertainty cognition OS — the specific derivation (revised)
- `theory/first_principles_alpha_derivation.md` in the project — full writeup (revised)
- Session 8 (2026-05-13) — where the circularity was discovered