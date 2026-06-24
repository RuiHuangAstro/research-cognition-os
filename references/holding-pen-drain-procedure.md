# Holding-Pen Drain Procedure (Full 3-Round Pattern)

> Worked example: 2026-06-22, draining `_archived-leaked-project-pitfalls.md` (58 KB, 98 ⚠️ entries)
> into 11 project cognition OS directories.

## When to use

The user says "把 skill 里的项目特异内容分发到各项目" or "drain the holding pen" or
"继续寻找这样的内容，然后更新到项目里去". The goal: move project-specific knowledge
out of the shared skill and into each project's own `research-cognition-os/`.

## Constraint

The skill's `_archived-leaked-project-pitfalls.md` and `SKILL.md` are **read-only** — never
modify them during drain. All writes go to project directories only.

## 3-Round Procedure

### Round 1: Classify & create PITFALLS.md

1. **Read the archived file** — enumerate all ⚠️ entries
2. **Classify by target project** — look for project names (DET_ML, M104, M31CGM, NGC3079,
   Fund Strategy, 星上算法, …), instrument names (XMM/Chandra/FXT), and variable names
   (`DeltaC`, `S_hat`, PSF templates, …)
3. **Check existing project OS directories** — `find ~/program ~/Data -maxdepth 4 -type d
   -name 'research-cognition-os'` and count existing insights/stages to avoid ID collisions
4. **Create `PITFALLS.md` per project** via parallel `delegate_task` (4 subagents, one per
   project group). Use YAML frontmatter (`type: meta`, `tags: [cog/meta, project-specific]`).
5. **Deduplicate** — the archived file often has 2-3 copies of the same pitfall. Pick one
   canonical version per pitfall.

### Round 2: OS_MAINTENANCE.md + project-specific references

1. **Create `OS_MAINTENANCE.md` per project** — lightweight file with (a) one-line reference
   to `references/os-maintenance-lessons.md` listing the 10 generic lessons, and (b) a
   `## 项目特异补充` section for project-specific maintenance notes (DAG design, tool
   conflicts, session audit procedures)
2. **Copy project-specific references** from skill's `references/` to each project's
   `research-cognition-os/references/`. Criteria: the file names a specific project in its
   title or first 5 lines (e.g., `i044-catalog-bridge-session.md` → DET_ML,
   `m104-cgm-2d-kt-map-orchestrator-session.md` → M104)
3. **Do NOT copy generic references** — files like `os-maintenance-lessons.md`,
   `supersede-dont-overwrite-pattern.md`, `negative-result-insight-pattern.md` are
   domain-neutral and stay in the skill

### Round 3: Deep sweep for remaining project-specific content

1. **Re-read the skill's full `references/` directory listing** — identify any remaining
   project-specific files not yet distributed
2. **Check for projects with OS directories but no PITFALLS.md** — these may have been
   missed in round 1 (e.g., XARTATOMS had 38 insights but no PITFALLS.md)
3. **Check for projects WITHOUT OS directories** — some may need bootstrap (e.g., M82 had
   no `research-cognition-os/` but had a `references/` directory from a prior copy)
4. **Supplement existing PITFALLS.md** — if a project's reference file contains additional
   pitfalls not in the archived file (e.g., `xray-temperature-mapping-pattern.md` has
   M104-specific pitfalls beyond what was in `_archived-leaked-project-pitfalls.md`)
5. **Copy remaining project-specific references** (second pass)

## Categorization rules for references

| Category | Destination | Examples |
|----------|-------------|---------|
| Project-specific session detail | Project `references/` | `i044-catalog-bridge-session.md`, `m104-cgm-2d-kt-map-orchestrator-session.md` |
| Project-specific build log | Project `references/` | `det-ml-uncertainty-cognitive-history.md`, `xartatoms-cognition-os-build.md` |
| Domain-specific pattern (X-ray) | Project `references/` + skill stays as upstream | `xray-temperature-mapping-pattern.md`, `proposal-upgrade-workflow-pattern.md` |
| Generic OS methodology | Skill `references/` only (do NOT copy) | `os-maintenance-lessons.md`, `supersede-dont-overwrite-pattern.md`, `negative-result-insight-pattern.md` |
| Generic build methodology | Skill `references/` only | `deep-audit-methodology.md`, `young-research-project-os-build.md`, `routine-os-sync-pattern.md` |

## Pitfall: "The drain is never done in one round"

The first pass classifies obvious pitfalls by project name. But the archived file also contains
generic-sounding entries that are actually project-specific when you read the details (e.g.,
"OS internal consistency" sounds generic, but the real lesson mentions specific insight IDs
like I016-I019 and V53-V58 — that's DET_ML-specific). And the skill's `references/` directory
contains project-specific files that aren't in the archived pitfalls at all.

**Rule**: always do at least 3 rounds. Round 1 = obvious classification. Round 2 = OS
maintenance + references. Round 3 = deep sweep of remaining content + projects discovered
during rounds 1-2.

## Verification

After all rounds, verify:
```bash
# Count PITFALLS.md files
find ~/program ~/Data ~/research-cognition-os -name 'PITFALLS.md' 2>/dev/null | wc -l

# Count OS_MAINTENANCE.md files
find ~/program ~/Data ~/research-cognition-os -name 'OS_MAINTENANCE.md' 2>/dev/null | wc -l

# Count project references directories with content
for d in $(find ~/program ~/Data -maxdepth 4 -type d -name 'research-cognition-os'); do
  refs="$d/references"
  [ -d "$refs" ] && [ "$(ls "$refs" 2>/dev/null | wc -l)" -gt 0 ] && echo "$(basename $(dirname "$d")): $(ls "$refs" | wc -l) refs"
done
```
