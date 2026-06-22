# Session Linter & OS Drift Detection

## Session Linter (`scripts/session_linter.py`)

Checks and auto-fixes session files under `research-cognition-os/sessions/`:
- Missing YAML frontmatter (adds `type/status/created/tags`)
- Missing DID/FOUND/NEXT sections (adds `- ...` placeholder)
- Non-bullet content (converts to `- ` prefix)

Usage:
```bash
# Dry-run (check only)
python3 scripts/session_linter.py --path /home/huangrui/program/<Proj>/research-cognition-os

# Auto-fix
python3 scripts/session_linter.py --fix --path /home/huangrui/program/<Proj>/research-cognition-os
```

### Critical Pitfall: Section Header Case

Session files use ALL-CAPS headers: `## DID`, `## FOUND`, `## NEXT`. The regex must match `(DID|FOUND|NEXT|Related)`, NOT `(Did|Found|Next|Related)`. A case-mismatch silently returns zero matches, causing the linter to treat existing sections as missing and rebuild the file with empty `- ...` placeholders — **destroying original content**.

This bug was responsible for corrupting multiple session files. The fix: always match the actual case used in files.

### Frontmatter Reconstruction

When extracting existing frontmatter (between `---` delimiters), the `extract_frontmatter_and_body` function returns the content between delimiters. When reconstructing the file, you must re-add the closing `---` delimiter:
```python
# CORRECT:
new_content = f'---\n{fm}\n---\n\n{body}'
# WRONG (missing closing ---):
new_content = f'---\n{fm}\n\n{body}'  # Missing closing delimiter
```

Missing the closing `---` causes the linter to detect the file as "changed" on every run (infinite fix loop), because the regenerated file always differs from the original.

## OS Drift Detection (`scripts/cog_os_drift_detect.sh`)

Compares latest code modification time vs latest session date for all projects with `research-cognition-os/`. Threshold: >1 day = drift.

```bash
bash scripts/cog_os_drift_detect.sh
# Exit 0 + output = drift detected
# Exit 1 + silent = all projects synced
```

Cron job `cognition-os-drift-check` (7b2ed733aaac) runs this daily at 09:00, with an LLM agent that reads drifted projects' AI_BRIEFING + latest code + latest session, then generates a drift report with specific OS update suggestions.

### Drift Detection Logic

1. For each project with `research-cognition-os/`:
   - Get latest session date from `sessions/YYYY-MM-DD.md` filenames
   - Get latest `.py/.ipynb/.sh` modification time (excluding `research-cognition-os/`, `.git/`, `__pycache__/`, `venv/`)
   - If code newer than session by >1 day → drift
2. Projects with no `sessions/` dir or no session files are also flagged
