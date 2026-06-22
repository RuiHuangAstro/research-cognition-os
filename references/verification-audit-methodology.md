# Verification Audit Methodology for Research Cognition OS

Systematic re-verification of solid conclusions from TRUST_TABLE using
subagent parallelism and bootstrap error estimation.

## When to Run

- Before paper submission
- After bug fixes that affect downstream results
- Periodically (quarterly) for long-running projects
- When a conclusion's trust level is about to be upgraded

## Workflow

### Step 1: Extract verifiable claims

From TRUST_TABLE and AI_BRIEFING, extract all items with confidence ≥ High
that have quantitative claims (numbers, ratios, percentages). For each claim,
identify:
- The specific number(s) to verify
- The data source (results/ file, simulation, mathematical proof)
- The tolerance (default: relative error < 20%)

### Step 2: Group into subagent tasks

Group related claims into batches of 3-5, keeping together claims that:
- Share the same data source
- Use the same simulation pipeline
- Are logically dependent (if one fails, the other is suspect)

Max 3 subagents concurrent (respect max_concurrent_children limit).

### Step 3: Define verification protocol per claim

For **simulation-based claims**:
```
1. Generate N≥5000 simulations (or load existing data)
2. Compute the claimed statistic
3. Bootstrap error: N_boot=200 chunk resamples
4. Report: value ± err, relative error, PASS/FAIL vs 20% threshold
```

For **data-file claims**:
```
1. Load the CSV/npz file
2. Recompute the statistic from raw data
3. Compare to the claimed value
4. Report: difference, relative difference, PASS/FAIL
```

For **mathematical claims** (negative results, proofs):
```
1. Reproduce the proof symbolically (sympy) or numerically
2. Verify the key step (e.g., orthogonality, identity)
3. Report: CONFIRMED/REJECTED with evidence
```

### Step 4: Run and synthesize

Collect all subagent results into a single table:

| Insight | Claim | Observed | Expected | Rel Err | Status |
|---------|-------|----------|----------|---------|--------|

Categories:
- **CONFIRMED**: rel_err < 20%, no issues
- **NEEDS ATTENTION**: rel_err < 20% but definition mismatch or caveat
- **FAILED**: rel_err ≥ 20% or data invalid
- **DEPRECATED FILE**: data source has known bugs

### Step 5: Update cognition OS

For each non-CONFIRMED result:
1. Add pitfall to the relevant insight file
2. Update TRUST_TABLE if trust level should change
3. Mark invalid data files as deprecated
4. Update AI_BRIEFING if a "Currently trusted" item needs qualification

## Lessons from DET_ML_Uncertainty Audit (2026-05-14)

### Pitfall: Invalid result files in results/

`conditional_variance_ratio_k_ml.csv` had two known bugs (gamma shape
parameter + incompatible variance comparison) but was never marked deprecated.
Subagents picked it up and got nonsensical results (k_observed ~0.001 vs
k_predicted ~0.99). **Always mark buggy output files immediately.**

### Pitfall: κ factor definition mismatch

κ_empirical (from Cash statistic q0) vs κ_formula (from 44.6M benchmark)
can differ by 38% at specific (S,b) points because the formula is a global
fit across a parameter grid, not exact at every point. When verifying
empirical formulas, check if the formula is meant to be exact or an
average fit.

### Pitfall: κ factor R² definition

The κ formula `κ = 1.31·S^0.234·b^(-0.235)` was claimed with R²=0.994, but this
R² refers to fitting κ values to a power law — NOT predicting q0. The actual q0
prediction has R²=0.845, MAPE=35%. **Rule**: any R² claim must specify "R² of X
fitted to Y" — never just "R²=0.994". In TRUST_TABLE, this distinction is critical
because an unqualified R²=0.994 in Notes misleads future users into thinking the
model has near-perfect predictive accuracy. T03 was downgraded from High to Medium.

### Pitfall: α ratio confusion between models

The "α ratio 1.55x" (I019/T33) comes from the k(ML) exponential model
(α=0.283/0.182 for ELLBETA/Gaussian), NOT from the winginess model's α.
The winginess model uses a single α=0.325 within the tested Gaussian+ELLBETA benchmark, with different W per PSF type. Treat broader PSF universality as provisional until tested. When reporting model parameters, always specify which model
formulation the parameter belongs to.

### Pitfall: I025 text conflation

"8-step vs 4-step ML ratio: 1.005-1.058" actually describes the 8/emldetect
range, not the 8/4 range. The true 8/4 range is 1.000-1.027 (even stronger
support). When writing insight statements, double-check that ratio descriptions
match the actual comparison being made.

### Success: Bootstrap chunk method

For simulation-based verification with N=5000 sims and N_boot=10 chunks
(not 200 — too few per chunk), relative errors of 2-9% are achievable.
For data-file analysis with N_boot=200, errors of 1-5% are typical.

### Success: Mathematical proof verification

Negative-result insights (I017: Edgeworth preserves variance, I026: α
decomposition is circular) can be verified with sympy symbolic computation.
This is more reliable than numerical spot-checks for mathematical claims.