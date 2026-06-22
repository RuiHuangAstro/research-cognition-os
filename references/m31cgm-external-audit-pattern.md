# External AI Audit Prompt Generation Pattern

## When to use

- Project has completed a major phase and needs independent review before proceeding
- User wants Codex or another AI tool to audit current results
- Key decisions need external validation (e.g., model choices, parameter freezing, detection thresholds)

## Procedure

### 1. Read OS files in dependency order

```
00_AI_BRIEFING.md → 03_TRUST_TABLE.md → 04_DECISION_LOG.md → stages/Sxx.md → 02_CURRENT_QUESTION.md
```

Each file provides a different layer:
- **AI_BRIEFING**: Project summary, trusted/questioned lists, methodology invariants
- **TRUST_TABLE**: What can be believed and what's uncertain — the auditor needs to know which claims are fragile
- **DECISION_LOG**: Why choices were made — the auditor needs to evaluate whether alternatives were adequately considered
- **Stage file**: Current execution plan, progress, script inventory — the auditor needs to know what's been done
- **CURRENT_QUESTION**: What the project is trying to answer right now — focuses the audit

### 2. Read latest experimental data

- Batch fitting log: `tail -500` to see current completion state and anomalies
- CSV results: detection rates, outlier flagging
- Key scripts: read the fitting sequence to understand methodological choices

### 3. Synthesize audit prompt structure

```markdown
# Codex Audit Prompt: <Project Name>

## Your Task
[Independent auditor role, 6-point review checklist]

## Scientific Goal
[1-paragraph from AI_BRIEFING]

## Key Observation
[The foundational observation/assumption]

## Project Structure
[File paths, key scripts, key data files, cognition OS location]

## Region/Model Definitions
[Full model with frozen/free params marked]

## Key Results So Far
[Quantitative table + detection statistics + anomalies]

## Fitting Sequence
[Step-by-step fitting procedure]

## Planned Next Steps
[What hasn't been done yet — auditor should evaluate feasibility]

## Critical Questions for the Auditor
[15-20 questions in 5 categories, numbered for easy reference]

## Instructions
[What to read, what to produce, output format]
```

### 4. Question categories (5 mandatory)

| Category | Typical count | Focus |
|----------|--------------|-------|
| Scientific logic | 3-5 | Foundational assumptions, alternative explanations |
| Methodology | 4-6 | Statistic, optimizer, parameter freezing, error propagation |
| Data quality | 3-4 | Outliers, detection thresholds, systematic biases |
| Statistical approach | 2-3 | Multiple testing, upper limits, sample size |
| Physical interpretation | 2-3 | Degenerate explanations, confounders |

### 5. Save to artifacts/

```
research-cognition-os/artifacts/codex_audit_prompt_YYYY-MM-DD.md
```

This preserves the project state snapshot at audit time. Future sessions can compare audit findings against the state that was audited.

## Bidirectional pattern

The cognition OS can both **produce** and **consume** audit artifacts:

| Direction | Pattern | When | Example |
|-----------|---------|------|---------|
| OS → audit prompt | Synthesize OS state for external review | Mid-project checkpoint | M31CGM 2026-05-31 |
| Audit prompt → OS | Ingest existing audit into OS structure | Building OS for existing project | M31Center RGS |

## M31CGM Worked Example (2026-05-31)

### Context
- M31 disk 0.7 keV APEC component vs stellar mass correlation study
- 21 halo OBSIDs fitted → averaged sky background
- 101 disk OBSIDs batch fitting running (48/101 complete)
- Key decision: M31HotISM.kT=0.7 + SrcPo.Γ=1.7 frozen (D07)

### Prompt structure
- 9.5 KB markdown document
- 20 questions across 5 categories:
  - Scientific logic (4): halo truly lacks 0.7 keV? MW foreground spatial variation? kT=0.7 assumption? coronal/virial mix?
  - Methodology (6): chi2gehrels vs C-stat? levmar vs moncar? MWhothalo error propagation? Srcabs.nH bound? SrcPo.Γ uniformity? sequential thaw bias?
  - Data quality (4): nH=0.05 detections real? extreme norm outliers? SP absorption of signal? MOS1/MOS2 systematics?
  - Statistical (3): false positive rate? expected scatter? upper limit handling?
  - Interpretation (3): norm∝M★ proof of coronal? non-correlation proof of virial? three-origin degeneracy?

### Key design decisions
- Included **anomaly flagging** in results section (2 extreme norms, Srcabs.nH boundary cases)
- Included **detection rate vs Srcabs.nH** breakdown — shows the fundamental S/N challenge
- Asked about **error propagation from frozen halo params** — critical methodological concern
- Asked about **degenerate physical interpretations** — not just "is the method right" but "even if right, what does it mean"

### Output location
`~/program/M31CGM/research-cognition-os/artifacts/codex_audit_prompt_2026-05-31.md`

### Post-audit response workflow

After receiving Codex audit results, the response follows a structured pattern:

1. **User triages audit findings** — accepts, rejects, or modifies each recommendation
2. **Rejected items become D-decisions** — e.g., "chi2gehrels is acceptable" (D21)
3. **Accepted items drive script versioning** — v1→v2→v3 with clear changelog
4. **Each version runs diagnostic subset first** — never jump to full batch
5. **Subset results validate/refute the fix** — e.g., nH ceiling fix (D24) confirmed by 0302320201 going from outlier→robust
6. **Cognition OS updated after each validated change** — Decision Log entries, AI_BRIEFING method invariants, S01 stage results table

**Key lesson**: Never do full batch re-run without subset validation. The v1→v2 (MWhothalo=0) and v2→v3 (nH max=0.1) transitions each revealed new issues that would have propagated to all 101 OBSIDs if run without subset testing first.