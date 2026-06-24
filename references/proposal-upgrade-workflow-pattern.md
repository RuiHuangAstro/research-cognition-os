# Proposal-upgrade workflow pattern (domain-specific)

> Extracted from `SKILL.md` to keep the skill domain-neutral. This is an **X-ray observation-proposal**
> workflow (SQUDE / XRISM / Chandra AO reviewer responses), not a general cognition-OS rule. Kept as a
> reference for X-ray proposal projects.

## Proposal Upgrade Workflow Pattern

When a research project receives reviewer feedback on an observation proposal (SQUDE,XRISM AO, Chandra AO, etc.), use this systematic workflow to upgrade the proposal section:

### 7-Phase structure

1. **Phase 0 — Audit**: Locate proposal source (PDF/tex), reviewer documents, existing data products. Record trust levels for all current results.
2. **Phase 1 — Text cleanup**: Remove internal draft notes, fix false claims (frozen parameters ≠ measured, source-only ≠ realistic precision), restructure into reviewer-facing subsections.
3. **Phase 2 — Figure update**: Produce Chandra/high-res image with FoV overlay + PSF-smoothed panel + extraction regions. Dual output (1col + 2col).
4. **Phase 3 — PSF mixing quantification**: Compute leakage matrix from high-resolution image convolved with coarse PSF. Present as table in proposal.
5. **Phase 4 — Background/foreground robustness**: Design conservative bracket (Sim-0 source-only, Sim-1 nominal bg, Sim-2 high bg). Address O VII foreground for starburst/CGM targets.
6. **Phase 5 — Model-discrimination examples**: Prioritize: abundance pattern > DEM > kinematics > NEI. Each must map to a physical test, not just a measurement.
7. **Phase 6 — Feasibility table**: Region × purpose × counts × key lines × measurable params × dominant systematic.
8. **Phase 7 — Validation**: Syntax checks, plot inspection, cognition OS update (session + decisions + trust table).

### Key language rules

- **"baseline source-only statistical precision"** — never present simulation results without this label
- **"SQUDE can test CIE versus NEI"** — not "SQUDE will detect NEI"
- **"O/Fe, Ne/Fe, Mg/Fe"** — not He/C/N (those are frozen, not measured)
- **"phase-coupled vs phase-decoupled velocity"** — not absolute velocity (gain calibration floor)
- **O VII foreground caveat** — mandatory for any target with v < 500 km/s

### Reviewer-facing deliverables

- Revised proposal section with 7 subsections
- Updated figure with FoV overlay + HPD-smoothed panel + extraction regions
- PSF leakage matrix table
- Systematics paragraph (background, foreground O VII, PSF mixing, gain calibration)
- Feasibility matrix

### Verified example

M82 SQUDE proposal (2026-05-28): 7-phase upgrade completed in one session. Key corrections: removed 2 "yi" draft notes, fixed He/C/N overclaim, qualified kT precision, added leakage matrix (Central 82.7%, Wind ~67%), added O VII foreground caveat. See `~/Data/M82/SQUDE_response/M82_section_v2_draft.md` and `~/Data/M82/research-cognition-os/sessions/2026-05-28.md`.
