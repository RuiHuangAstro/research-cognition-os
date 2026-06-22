# Routine OS Sync with Latest AI Sessions (2026-06-12)

## Context

User asked: "read the latest cognition OS and the latest Claude session, update the missing part of the cognition OS." This is a routine maintenance task, not an initial build or deep audit.

## Worked example: TES 星上算法 OS sync

### Step 1: Read current OS state

Read AI_BRIEFING, TRUST_TABLE, active stage, latest session record. Note the highest insight/experiment numbers currently in use.

### Step 2: Extract latest AI session content

```bash
# Find Claude Code sessions for the project
python3 ~/.hermes/skills/data-science/codex-session-search/scripts/claude_search.py --list --project <name>

# If --project fails (leading-dash name), read JSONL directly:
ls -lt ~/.claude/projects/<project-dir>/*.jsonl | head -3

# Extract final answers
grep '"final_answer"' SESSION.jsonl | python3 -c "import sys,json; [print(json.loads(l).get('payload',{}).get('message','')[:2000]) for l in sys.stdin]"
```

### Step 3: Diff OS vs session

Compare session conclusions vs existing insights. Items in session but NOT in OS = missing items.

Found in this session:
- I009 naming conflict: two insight files (timing_jitter + V52_result) both using "I009"
- Missing I008 (gap in numbering)
- PROJECT_DAG not updated with latest nodes
- Cross-references stale (I016, I017, I018, I019, S13 still referenced old I009)

### Step 4: Fix conflicts and add missing items

1. Rename conflicting I009 → I020 (V52 result)
2. Fill missing I008
3. Update all cross-referencing files

### Step 5: Verify with grep

```bash
grep -r "I009" --include="*.md" research-cognition-os/
# Must return zero results for the old ID
```

### Step 6: Update session record

Write today's Did/Found/Next in sessions/YYYY-MM-DD.md.

## Key differences from deep audit

| Feature | Deep audit | Routine sync |
|---------|-----------|--------------|
| Session search | All tools, exhaustive | Latest session only |
| Time budget | 3-5 hours | 15-30 min |
| Subagent use | Yes (parallel) | No |
| Scope | Reconstruct full history | Fill gaps since last sync |
| Trigger | Initial OS build | User request or drift detection |

## Pitfall: --project flag with leading-dash names

Claude Code project directory names encode `/` as `-`, so they start with `-` (e.g., `-home-huangrui-program-tes-onboard-processing`). The `claude_search.py` argparse may interpret these as flags. Workaround: read JSONL files directly instead of using the CLI.
