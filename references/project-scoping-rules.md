# Project Scoping Rules for Cognition OS

## Learning Sub-Tasks Stay Under the Parent Project

When the user wants to learn a technique (e.g., RGS point-source processing with Capella) as preparation for the main project (e.g., N132D RGS extended-source analysis), do NOT create a standalone project. The learning materials go under the parent project, and the cognition OS tracks it as a new stage within the existing project.

- ✅ Correct: add S05 `rgs-point-source-tutorial` stage to `~/program/N132D/research-cognition-os/`; learning code in `~/program/N132D/rgs_tutorial/`; tutorial data in `~/Data/N132D/Capella/`
- ❌ Wrong: create `~/program/RGS_Capella/research-cognition-os/` as a separate project

**Rationale**: Cognition OS must track all cognitive state for a research objective in one place. Splitting learning into a separate project disconnects the tutorial insights from the main analysis they serve.

## Always Check Existing Projects Before Suggesting New Scaffolding

The user may have already initialized the project with cognition OS in a prior session. Before proposing `mkdir` or scaffolding:

1. Check `~/program/<Name>/` — does it exist? Does it have `research-cognition-os/`?
2. Check `~/Data/<Name>/` — does data already exist?
3. Check `data/` symlink — does `~/program/<Name>/data` exist and point correctly?
4. Read existing cognition OS files (AI_BRIEFING, CURRENT_QUESTION) to understand current state

Only if the project truly doesn't exist should you scaffold from scratch.

## data/ Symlink Is Optional

The `data/` symlink convention (`~/program/<Project>/data → ~/Data/<Project>/`) is a convenience, not a requirement. Some existing projects (e.g., N132D) use absolute `DATA_ROOT` paths in shell scripts and store scripts + products directly in `~/Data/<Project>/`. When working within such a project:

- Match the existing path convention
- Do NOT force a symlink if the project works fine without it
- If adding new scripts, prefer relative paths via `data/` if the symlink exists, or match the existing absolute-path style if it doesn't
