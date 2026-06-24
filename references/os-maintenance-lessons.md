# OS maintenance lessons (project-agnostic)

General lessons for keeping any cognition OS healthy. These are domain-neutral — they
mention no specific dataset, instrument, or result. (Project-specific findings do **not**
go here; they go into that project's own `research-cognition-os/`. See `SKILL.md` →
"Scope & contribution rules".)

## Internal consistency: DAG ≡ TRUST_TABLE ≡ AI_BRIEFING

After any multi-file OS update, every new `I`/`E`/`B`/`S` ID must appear in **all** of:
`00_AI_BRIEFING.md`, `03_TRUST_TABLE.md`, `05_PROJECT_DAG.md`, and the relevant stage file.
Missing IDs = incomplete update. Quick check:

```bash
grep -c 'I0[0-9][0-9]' 05_PROJECT_DAG.md 03_TRUST_TABLE.md 00_AI_BRIEFING.md
ls insights/ | sed 's/_.*//' | sort > /tmp/ids.txt
grep -oP 'I0[0-9]{2}' 05_PROJECT_DAG.md | sort -u > /tmp/dag_ids.txt
comm -23 /tmp/ids.txt /tmp/dag_ids.txt   # insights missing from the DAG
```

## OS drift audit (run at the start of every session)

Code/experiments routinely move faster than the OS. Diagnose lag:

1. `find <root> -name '*.py' -printf '%T+ %p\n' | sort -r | head -5` — newest code timestamp
2. `ls -lt research-cognition-os/sessions/ | head -3` — newest session timestamp
3. If code is >1 day newer than the latest session → the OS is lagging.

When lagging, don't rush a full rebuild: note "OS needs sync from <version>" in
`02_CURRENT_QUESTION.md`, then backfill at the next real milestone (new result, new
insight, bug discovery). The bundled `scripts/cog_os_drift_detect.sh` automates the scan
across all deployments.

## Routine sync vs deep audit

"Read the latest OS + the latest AI session, fill the gaps" is a *light* 15–30 min task,
not a deep audit: read current OS state → extract the latest session's conclusions →
diff against existing insights/experiments → add only the missing items (check
`ls insights/ | sort -t_ -k1 -n | tail -3` first to avoid ID collisions) → update all
cross-references → write today's session. No multi-tool exhaustive search, no subagent
decomposition. See `routine-os-sync-pattern.md`. The deep-audit procedure
(`deep-audit-methodology.md`) is only for first-time construction or major pivots.

## ID numbering conflicts

Before adding any numbered item, `ls {experiments,insights,bug_impacts}/ | sort -t_ -k1 -n | tail -3`
and use `max+1`. Concurrent sessions on the same OS are the common cause of collisions.
After any rename, `grep -r "old_ID" --include="*.md" .` must return **zero** before you
declare it done — ghost references break Obsidian's graph view and confuse future sessions.

## Atomic propagation of status changes

When a fact changes (bug count 3→5, an output becomes deprecated, a trust level drops),
propagate it through the **whole** chain in one pass: `Bxxx → 03_TRUST_TABLE → 00_AI_BRIEFING →
stages/Sxx → DAG → session log`. A partial update leaves the OS internally inconsistent.
Verify with e.g. `grep -r "3 bugs\|3 个 bug" research-cognition-os/` to confirm no stale value remains.

## Supersede, never overwrite

When a new finding overturns an old one, do **not** edit the old insight/decision in place.
Mark its status `superseded`, add a `⚠️ SUPERSEDED → [[Inew]]` banner, create a new insight
for the corrected conclusion, and downgrade the old row in the trust table. Research history
is a DAG, not a mutable array — overwriting orphans every reasoning chain that depended on the
old node. Full pattern + worked example: `supersede-dont-overwrite-pattern.md`.

## Negative results / dead ends are first-class insights

A disproven approach is a cognitive asset, not nothing. Record it as a `confidence=High`
insight: Statement = "X CANNOT explain Y because Z", Evidence = the disproving evidence.
List negative-result insights under "Currently trusted" in the briefing, and mark dead-end
experiments as "negative control" / "dead end" (dashed red in the DAG). This prevents future
sessions re-exploring the same dead road. See `negative-result-insight-pattern.md`.

## Session records are the primary cognitive source

File trees show *what was produced*; session records (Codex/Claude/Gemini JSONL) show *why*,
*what was tried and abandoned*, and *where direction changed*. When reconstructing history,
extract session `final_answer` + `user_message` timelines **first**, then cross-reference the
file tree — not the other way round.

## Trust Table is the core; Current Question is the gate

On any new bug, update the trust table *first* — don't spiral into "throw everything out".
Before opening a new branch, ask "is this the current question?"; if not, it goes in the
Parking Lot. Record dependencies and current trust, not just "what I did".

## Verify subagent / external output before recording it

Quantitative results returned by a subagent (or an external audit) are not insights until
checked. Run a 3-level check: formula (against first principles, watch scaling and large
inflation factors), numbers (re-run on independent data), logic (does "X causes Y" survive
removing X?). See `orchestrator-subagent-research-workflow.md`.

## Don't poll long-running tasks

For background tasks >30 min, don't loop `sleep N && ls`. Start a background monitor
(`while [ ! -f out.csv ]; do sleep 300; done && notify`), fire a push notification on
completion, and do other useful work meanwhile.
