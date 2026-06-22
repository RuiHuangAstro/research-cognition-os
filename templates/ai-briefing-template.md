---
title: AI Briefing
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
tags: [research-management, cognition, trust]
---

# AI Briefing: <Project Name>

Last updated: YYYY-MM-DD

## One-paragraph project summary
...

## Current focus
...

## Methodology invariants

- Theory is conditional on observable inputs such as `(S_hat, b, psf)`, not `S_true`; `S_true` is only a simulation-generation label.
- Analyze primary-statistic residuals, not transformed-statistic cuts. For DET_ML-like work, analyze `DeltaC - E_theory[DeltaC]`; do not use ML-truncated samples to infer intrinsic conditional shape or variance.
- Reconstruct sample moments from residuals plus theory: `mean(DeltaC)=mean(R)+mean(mu_theory)` and `Var(DeltaC)=Var(R+mu_theory)`. Use `Var(R)` alone only for residual width or narrow bins where `mu_theory` is nearly constant.

## Cognitive history in <N> stages
1. ...

## Currently trusted
- ...

## Currently questioned
- ...

## Open questions
1. ...

## AI instruction
Before giving suggestions, classify any proposed conclusion as:
Trusted / Provisional / Questioned / Deprecated.