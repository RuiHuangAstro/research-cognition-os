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

ScienceAgent_cstat_v2 is a fully automated multi-agent research platform investigating the **goodness-of-fit distribution of the Cash (C) statistic in the low-count Poisson regime**, where Wilks' theorem breaks down. The target quantity is `ΔC = C_data − C_best`, with primary objective accurate prediction of `E[ΔC]` and secondary objective a usable `Std[ΔC]`. The active scientific layer (L0) is bounded to `norm+shape` polynomial families (`linear`/`quadratic`, `p=2/3`) operating in the low-count regime, with the explicit charter that **a strong local result is preferred over a weak universal theory**. The system runs 24/7 via `main.sh` orchestrating five agents (Analyst, Verifier, Generator, Librarian, Simulator) plus Manager/Architect; as of round 1493 (2026-05-13) it is stalled in `planning_admission_exhausted` — the generator has no admissible families to propose into.

## Current focus

**Unblock the research loop from the admission-exhausted deadlock** (round 1493) by running the architect phase plan that the manager reflection memo prescribed: (1) open a bounded admissible search space, (2) prioritize high-information pending/cheap downsampled slices that separate total-count from channel-count effects, (3) route the simulator to populate that slice backlog before resuming generator. The 2026-05-13 manual intervention already added `custom/experiment_driven_p2_v1` to `allowed_families`; the next operational step is to actually consume that family with concrete experiment designs.

## Methodology invariants

These are project-specific rules. They are NOT the DET_ML defaults from the template — they are the cstat-program methodology derived from `docs/VERIFIER_RULES.md`, `docs/PHENOMENA.md`, and `docs/RESEARCH_CHARTER.md`.

1. **Axiom P1-Exact (reduction contract).** Any p≥2 theory MUST reduce to `E[ΔC] = C_e(Σμᵢ)` for p=1, where `C_e` is the exact per-bin deviance. This is the only universally trusted anchor. Violation → automatic `rejected` by verifier.
2. **Wilks high-count limit.** Any theory MUST converge to `ΔC ≈ p` (or `C_best ≈ N−p`) as total counts → ∞. This is the asymptotic anchor.
3. **Shape-curvature dependence (PHENOMENA-001).** A pure `p`-count correction is refuted for the bounded regime. Linear vs quadratic shape at matched (N, p, μ̄, φ) shifts `E[ΔC]` by ~0.25 — theories must include shape-curvature / heterogeneity terms (RelVar, leverage, curvature κ).
4. **Total counts ≠ N.** The empirical phenomenology distinguishes `total_counts` (Σμᵢ) from channel count `N`. Theories that conflate them are refuted on `Fixed-total binning` slices.
5. **Weak-shape activation is partial.** Slices with `phi < 1` (shape parameter variance) do not fully activate the shape degrees of freedom — generators must model partial activation, not binary on/off.
6. **Local strength > forced unification.** A theory with strong predictive success on the bounded target regime is scientifically meaningful even without global unification. Verifier must not over-penalize this.
7. **Cross-dimensional stress test for L3 maturity.** Any theory claiming L3 maturity MUST be jointly evaluated on p=2 (SHAPE) AND p=3 (EXTENDED) slices.
8. **RAI scoring.** New theories are scored by `RAI = RMSE_Ref / RMSE_New` against REF-AIC and REF-BIC baselines. RAI > 1 means improvement.
9. **Placeholders are not validated survivors.** Adapters still flagged as `safe_active_placeholder` or carrying TODO/placeholder fit notes are routed to `unsupported_family_queue` — they cannot count as validated survivors.

## Cognitive history in 5 stages

1. **S01 — IBA baseline era (Mar 2026).** Established C-statistic moments under the Independent Bin Approximation. `T-BASELINE-IBA-p1` is the exact p=1 anchor. Kaastra 2017 single-bin deviance moments are the foundation.
2. **S02 — Wilks-asymptotic baseline (Mar–Apr 2026).** Added `T-BASELINE-WILKS-p2` to anchor the high-count limit. Established that IBA fails for p≥2.
3. **S03 — PHENOMENA-001 discovery (Mar 26, 2026).** Empirical confirmation that linear vs quadratic shape shifts `E[ΔC]` by ~0.2553 at matched (N=20, p=2, μ̄=1.5, φ=0.9) — Z-score > 50. Pure p-correction is refuted.
4. **S04 — L0 bounded-regime focus (Apr–May 2026).** Charter narrowed to `norm+shape`, `linear/quadratic`, `p=2/3`, low-count regime. Strong local result > universal theory.
5. **S05 — P1 anchor repair + admission deadlock (May 11–13, 2026).** `core/exact_p1.py` corrected to return `C_e(Σμᵢ)` instead of `E[C_best]`. Z-score wall (>19,000) for p≥2 theories removed. But generator admission exhausted: all known p=2 families rejected. Manual intervention (round 1485 memo) added `custom/experiment_driven_p2_v1`. Loop still stalled as of round 1493.

## Currently trusted

- **Axiom P1-Exact reduction contract** (see Methodology invariant 1) — High trust; mathematically proven.
- **Wilks high-count limit** — High trust; asymptotic theorem.
- **PHENOMENA-001 shape-curvature deviation** — High trust; Z>50 empirical significance.
- **Kaastra (2017) single-bin deviance moments** — High trust; exact Poisson series.
- **Core simulator pipeline** (`core/simulator_common.py`, `core/control_loop.py`) — High trust; deterministic and reproducible.
- **`docs/RESEARCH_CHARTER.md` L0 scope definition** — High trust; explicit operator-mandated charter.

## Currently questioned

- **`T-BASELINE-IBA-p1` for p≥2** — Refuted; IBA fails with parameter coupling.
- **Pure p-count corrections (no shape term)** — Refuted by PHENOMENA-001.
- **All `T-20260511-006` through `T-20260512-002`** — Catastrophic Z-scores (>19,000) before P1 anchor repair; re-evaluation pending against corrected baseline.
- **Placeholder adapters (`safe_active_placeholder`)** — Not validated; cannot count as survivors.
- **Universal closed-form theory across all model families** — Explicitly de-prioritized by charter; not the current objective.

## Open questions

1. **Why is the generator admission gate exhausted?** All known p=2 families have been registered and rejected. Is this a finite-family exhaustion or a quality-control over-rejection?
2. **What is the smallest experiment that separates total-count effects from channel-count effects?** Manager reflection memo flagged this as the highest-information pending slice.
3. **Does `LeverageCurvatureCouplingTheory v1` (T-20260511-002) actually beat REF-AIC/BIC on the bounded target regime?** Adapter promoted but not yet validated on full benchmark.
4. **How does `Std[ΔC]` scale with N and total counts independently?** Secondary target, currently under-characterized.
5. **What is the role of weak-shape activation (`phi < 1`)?** Partial activation is empirically observed but no theory yet captures it cleanly.
6. **Will the round-1493 deadlock resolve via the architect phase plan, or does the loop need deeper restructuring?**

## AI instruction

Before giving suggestions, classify any proposed conclusion as:
- **Trusted** — backed by axiom, asymptotic theorem, or Z>50 empirical evidence.
- **Provisional** — has empirical support but not yet independently verified.
- **Questioned** — affected by known bugs (e.g., pre-repair P1 anchor), or contradicted by PHENOMENA-001.
- **Deprecated** — explicitly rejected by verifier or superseded by a newer theory.

When proposing a new theory or experiment, ALWAYS cite:
- Which `PHENOMENA-xxx` it addresses (or explain why it doesn't need to).
- Which `Axiom` it preserves (especially P1-Exact and Wilks limit).
- Which slice it targets (`linear/quadratic`, `p=2/3`, total-count range).
- What RAI it expects to achieve vs REF-AIC and REF-BIC.

## Related

- [[03_TRUST_TABLE]] — constrains
- [[02_CURRENT_QUESTION]] — anchors
- [[05_PROJECT_DAG]] — visualizes
- [[04_DECISION_LOG]] — records
- [[S01_stage]] — preceded-by
- [[S05_stage]] — current
