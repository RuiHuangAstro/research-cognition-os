---
type: bug
status: active-audit
created: YYYY-MM-DD
tags: [cog/bug, psf-dependent]
---

# Bxxx: Bug Name

Discovered: YYYY-MM-DD
Status: Active audit

## Bug summary

Brief description of the bug and its overall impact.

## Bug details

### Bug 1: [Short description] — [Severity: Fatal / Severe / Moderate / Minor]

**Code location**: ...
**Problem**: ...
**Impact**: ...

### Bug 2: [Short description] — [Severity]

**Code location**: ...
**Problem**: ...
**Impact**: ...

(Continue for each bug. Must match BUGREPORT_*.md if one exists.)

## Affected code versions
- `path/to/code.py` (Lxxx-Lyyy)
- All variants using the buggy class/function

## Affected outputs
- All figures/data generated from affected code
- Be specific: list experiment IDs, figure filenames, result files

## Not affected
- Code/results that do NOT depend on the buggy component
- This section is critical — it prevents "total project panic"

## Conclusion audit

| Conclusion | Status after bug | Action |
|---|---|---|
| ... | Survives / Questioned / Deprecated | Keep / Rerun / Re-evaluate |

## Recovery plan

1. Fix the bug (or use corrected replacement)
2. Create anchor test against ground truth
3. Rerun only experiments depending on affected outputs
4. Update [[03_TRUST_TABLE]]
5. Mark old figures as deprecated (not deleted)

## Cross-reference
- BUGREPORT_xxx.md: [link or N/A]
- Verified all bugs accounted for? Y/N

## Related
- [[Exxx_experiment]] — contaminates
- [[Ixxx_insight]] — questions
- [[Sxx_stage]] — triggers-rollback