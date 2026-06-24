# Skill-to-Repo Sync Pattern

When a Hermes skill has a public GitHub mirror (e.g., `~/program/playground/research-cognition-os/`), the Hermes skill version is the **upstream** — it is the cleaned, project-neutral version. The repo may drift behind or accumulate project-specific content that violates the skill's own Scope rules.

## Sync direction

**Hermes skill → GitHub repo** (one-way). Never edit the repo SKILL.md independently and expect the skill to follow.

## Sync checklist

1. **Compare SKILL.md sizes** — repo larger than skill = likely pollution
2. **Compare section headers** — `diff <(grep '^## ' repo/SKILL.md) <(grep '^## ' skill/SKILL.md)`
3. **Compare references/** — `comm -23 <(ls skill/references/ | sort) <(ls repo/references/ | sort)` for files only in skill
4. **Check for duplicate ⚠️ entries** — `grep -c '⚠️' repo/SKILL.md` should be close to skill version
5. **Check README.md accuracy** — verify file numbering matches SKILL.md conventions

## Common drift patterns

| Drift type | Detection | Fix |
|-----------|-----------|-----|
| Project-specific pitfalls leaked into SKILL.md | ⚠️ count >> skill version | Move to `references/_archived-leaked-project-pitfalls.md` |
| Duplicate pitfall entries | `grep '⚠️ <same title>' repo/SKILL.md | wc -l > 1` | Deduplicate |
| Domain-specific sections inlined | Section exists in repo but not in skill (moved to references/) | Move to `references/<topic>-pattern.md` |
| Missing references files | Files in `skill/references/` but not in `repo/references/` | Copy from skill to repo |
| README.md numbering wrong | e.g., `01_CURRENT_QUESTION` vs `02_CURRENT_QUESTION` | Fix to match SKILL.md |

## Update procedure

```bash
# From the repo directory
cd ~/program/playground/research-cognition-os

# 1. Copy cleaned SKILL.md from skill
cp ~/.hermes/skills/note-taking/research-cognition-os/SKILL.md ./SKILL.md

# 2. Copy missing references
for f in _archived-leaked-project-pitfalls.md large-project-streamlined-bootstrap.md os-maintenance-lessons.md proposal-upgrade-workflow-pattern.md xray-temperature-mapping-pattern.md; do
  cp ~/.hermes/skills/note-taking/research-cognition-os/references/$f ./references/
done

# 3. Fix README.md numbering if needed
# 4. git add + commit + push
```

## Trigger

- After any skill patch that adds/renames references
- User asks "sync the repo"
- Periodic (monthly) check

## Worked example

2026-06-22 comparison found:
- Repo SKILL.md: 120 KB, 101 ⚠️ entries (vs skill 62 KB, 9 ⚠️ entries)
- 3 duplicate pitfall entries in repo
- ~90 DET_ML-specific pitfalls in repo (violates Scope rules)
- 5 missing references in repo
- README.md had wrong file numbering (01/02 instead of 02/03)
