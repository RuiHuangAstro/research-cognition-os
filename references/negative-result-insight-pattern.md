# Negative-Result Insight Pattern

## When to use
When a theoretical approach or hypothesis is systematically tested and definitively ruled out
(not just "didn't work" but "can't work because of X").

## Pattern

### 1. Write the insight immediately
Don't wait for a "better" result. The negative result IS the result.

```markdown
# Ixxx: X Cannot Explain Y (Negative Result)
Confidence: High

## Statement
X CANNOT explain Y because of Z [mathematical/logical reason].

## Evidence
1. [Quantitative falsification]
2. [Mathematical proof if applicable]
3. [Empirical measurement that rules it out]

## Implications
- [What this eliminates as an option]
- [What the correct direction likely is]
```

### 2. Key distinction: "didn't work" vs "can't work"
- "Didn't work" = implementation issue, might work with better code/params → experiment note
- "Can't work" = fundamental mathematical/logical reason → insight

Examples:
- Edgeworth CANNOT change variance (orthogonal polynomial property) → insight
- A specific hyperparameter value didn't converge → experiment note
- Extreme value theory overpredicts by 3-4x → insight (wrong mechanism)

### 3. Record in AI_BRIEFING
Add to "Currently trusted" section:
```
- [[I017_edgeworth_cannot_explain_variance_compression]] — Edgeworth/Bartlett/extreme-value cannot explain ~11% compression (High confidence, negative result)
```

### 4. Link from the parent stage
In the stage that explored the dead end:
```markdown
## Decision: 方案三 is dead end, focus on 方案二
```

### 5. Real examples from DET_ML_Uncertainty
- I017: Edgeworth/Gram-Charlier cannot explain variance compression
 - Mathematical proof: orthogonal polynomials preserve variance
 - Bartlett correction affects mean not variance
 - Extreme value theory overpredicts (0.30 vs 0.88 observed)
 - True mechanism: position-residual covariance (nonlinear selection bias)
- I023: Residual field Z_⊥ is white noise — compression is NOT from noise correlation
 - Constrained residual field has ξ=0.5 pix (= pixel scale), identical for Gaussian and ELLBETA
 - ΔC landscape also has same ξ≈2.54 pix for both PSF types
 - Decisive experiment: if noise were correlated, ξ_noise >> 1 pix; but ξ_noise = 1 pix
 - True mechanism: PSF gradient structure maps independent noise into correlated ΔC landscape

## Why this matters
Without recording dead ends, future sessions waste time re-exploring the same
theoretical avenues. A well-documented negative result is as valuable as a
positive one — it narrows the search space.