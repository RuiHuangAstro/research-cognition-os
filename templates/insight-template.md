---
type: insight
status: active
confidence: medium
created: YYYY-MM-DD
tags: [cog/insight, trust/medium]
---

# Ixxx: Insight Title

Status: Active | **Superseded** (if replaced by newer insight)
Confidence: Medium by default; upgrade to High only after independent verification, mathematical proof, or stable replicated evidence. Use Low/Questioned when affected by bugs or stale definitions.
Created: YYYY-MM-DD
Last reviewed: YYYY-MM-DD

<!-- WHEN SUPERSEDED: Add ⚠️ SUPERSEDED to title, add blockquote below,
     change status to "superseded", add tag "superseded-by/Iyyy",
     change confidence to reflect reliability of OLD claim.
     NEVER delete or overwrite the original content. -->

<!-- Example superseded annotation:
# Ixxx: Insight Title ⚠️ SUPERSEDED

> **Superseded by [[Iyyy_new_insight]]**.
> Brief reason why the old conclusion is no longer valid.
> The original content is preserved below for research history.

Status: **Superseded** by Iyyy
Confidence: Medium (original claim was correct for specific context, not general)
-->

## Statement
...

## Methodology status

If this insight changes analysis methodology, state the durable rule separately from numerical claims. Example:

```text
Durable rule: bin by S_hat, subtract E_theory[DeltaC], and analyze residuals.
Numerical claims: require rerun after bug/fix X.
```


## Assumptions
...

## Evidence
- [[Exxx_experiment_name]] — provides evidence
- results/... — data artifacts

## Dependencies
- Depends on: [[Iyyy_dependency]]
- Does not depend on: ...

## Limitations
...

## Moment accounting (if using residuals)

Define `R = DeltaC - mu_theory`. Distinguish residual width `Var(R)` from mixed-bin observed width `Var(R + mu_theory)`. Only use `Var(DeltaC) ≈ Var(R)` when `mu_theory` is nearly constant within the bin.

## Used by
- [[Izzz_downstream]] — uses this insight
- [[Sxx_stage]] — applied in this stage

## Related
- [[Sxx_stage_name]] — discovered-in
- [[Exxx_experiment]] — evidence-from