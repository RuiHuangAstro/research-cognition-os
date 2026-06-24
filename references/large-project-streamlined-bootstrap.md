# Large-Project Streamlined Bootstrap: ScienceAgent_cstat_v2

## Context

User asked to build a cognition OS for an existing large project (ScienceAgent_cstat_v2) on a remote server (lang2). The project is a fully automated multi-agent research platform with 1493 rounds, 387 theories, 469 experiments, running 24/7 since March 2026. It was stalled in `planning_admission_exhausted` deadlock for 40+ days.

## Project-type classification

- **NOT New** — project has extensive history
- **NOT Young** — far more than 5 sessions, 50+ products
- **Large** — but user asked "建立 cognition OS", not "deep audit"
- **Decision**: Streamlined bootstrap (1 hour) → minimally viable OS → maintain via routine sync

## Workflow executed

### Step 1: Project reconnaissance (15 min)

- `session_search` to find 3 prior sessions about this project
- `ssh lang2` to inspect file tree: `ls -la ~/program/ScienceAgent_cstat_v2/{core,scripts,docs,index,logs}`
- Read key docs via ssh: `docs/GOAL.md`, `docs/RESEARCH_CHARTER.md`, `docs/PHENOMENA.md`, `docs/VERIFIER_RULES.md`, `CHANGELOG.md`
- Read latest round log: `logs/round-1493.json` → identified deadlock state

### Step 2: Core OS file creation (35 min)

- **00_AI_BRIEFING.md** (8.2 KB): Written directly with project-specific methodology invariants (9 rules derived from VERIFIER_RULES.md, PHENOMENA.md, RESEARCH_CHARTER.md). NOT copied from DET_ML template.
- **02_CURRENT_QUESTION.md, 03_TRUST_TABLE.md, 04_DECISION_LOG.md, 05_PROJECT_DAG.md**: Delegated to subagent with full project context. Subagent wrote locally then scp'd to lang2. Total: ~16 min for 4 files.
- **PITFALL**: Accidentally wrote AI_BRIEFING content to `~/.hermes/skills/.../templates/ai-briefing-template.md` instead of the project directory. Had to restore template and re-target.
- **stages/S05_p1-repair-deadlock.md** (3.7 KB): Current active stage
- **bug_impacts/B002_admission_deadlock.md** (4.5 KB): Active blocker audit

### Step 3: First session record (5 min)

- `sessions/2026-06-22.md`: Did/Found/Next format with YAML frontmatter

### Step 4: Cross-doc consistency check (5 min)

- Grep for key IDs (S01-S05, D01-D04, M01-M09, B002, PHENOMENA-001) across all files
- Verify YAML frontmatter in all .md files
- Result: all consistent

## Key decisions

1. **Methodology invariants are project-specific** — The cstat project has 9 invariants (P1-Exact axiom, Wilks limit, PHENOMENA-001 shape dependence, total≠N, weak-shape activation, local>universal, cross-dimensional stress test, RAI scoring, placeholder policy). These are completely different from the DET_ML defaults (S_hat conditioning, DeltaC residuals, ML truncation). **Never copy template defaults into a project that doesn't need them.**

2. **Only S05 stage created, not S01-S04** — S05 is the current active stage. S01-S04 can be backfilled from CHANGELOG.md as time permits. Prioritizing the current stage over historical completeness is correct for streamlined bootstrap.

3. **B002 bug_impact created for active blocker** — The admission deadlock is the primary blocker. Recording it as a bug_impact (not just a session note) ensures future sessions see it in the TRUST_TABLE and DAG.

4. **Insights directory left empty** — Key insights (shape-curvature deviation, total≠N, weak-shape activation) are currently captured as TRUST_TABLE M-entries (M01-M09). They can be extracted to I001-I003 insight files during a routine sync when the project resumes.

5. **Remote project via ssh** — All file operations went through `ssh lang2` + `scp`. The OS directory lives on the remote server alongside the project code. No local copy needed.

## Output

8 files, 108 KB total at `lang2:~/program/ScienceAgent_cstat_v2/research-cognition-os/`

| File | Size |
|:---|:---|
| 00_AI_BRIEFING.md | 8.2 KB |
| 02_CURRENT_QUESTION.md | 4.5 KB |
| 03_TRUST_TABLE.md | 5.5 KB |
| 04_DECISION_LOG.md | 6.4 KB |
| 05_PROJECT_DAG.md | 4.8 KB |
| stages/S05_p1-repair-deadlock.md | 3.7 KB |
| bug_impacts/B002_admission_deadlock.md | 4.5 KB |
| sessions/2026-06-22.md | 3.9 KB |

## Deep supplement phase (same session, +14 files)

After the initial 8-file bootstrap, the user requested a deeper exploration with the updated skill. This phase added:

### Insight extraction from M-entries → I-files (6 files)

The TRUST_TABLE M01–M09 methodology invariants contained embedded scientific conclusions. These were extracted into standalone insight files (I001–I006) so Obsidian can track them independently. Key pattern: **M-entries are methodology rules; I-entries are the scientific conclusions those rules produce.** They are different objects and should not stay merged.

One insight (I006) is a **negative result** — "no universal closed-form theory exists in bounded regime" — recorded as `confidence: High` per the negative-result-insight pattern.

### Bug backfill: B001 (1 file)

The P1 anchor bug was only referenced in the CHANGELOG and D03 decision. Extracting it into `bug_impacts/B001_p1-anchor-bug.md` makes it visible in the DAG and trust table independently of the decision log. Pattern: **every resolved critical bug should have its own B-file**, not just a decision entry.

### Stage backfill: S01–S04 (4 files)

Historical stages were reconstructed from CHANGELOG.md + project docs (GOAL.md, RESEARCH_CHARTER.md, PHENOMENA.md). S05 (current) already existed. Pattern: **only backfill stages when the user asks for deeper exploration** — the initial bootstrap correctly prioritizes S05 only.

### Meta files (3 files)

- `SCHEMA.md`: Tag taxonomy, trust classification rules, naming conventions
- `01_PROJECT_INDEX.md`: Global index with wikilinks to all OS files
- `PROJECT_DAG.canvas`: Obsidian Canvas JSON (16 nodes, 19 edges, color-coded)

### Cross-doc propagation after bulk additions

Adding 14 files broke the cross-doc consistency that was verified in the initial bootstrap. The fix required:

1. **AI_BRIEFING**: Add `[[I001]]`–`[[I006]]` and `[[B001]]` under Currently trusted / Currently questioned
2. **TRUST_TABLE**: Add I001–I006 insight rows + B001–B002 bug rows
3. **PROJECT_DAG**: Add Mermaid subgraphs for insights and bugs
4. **Session**: Update Did/Found/Next to reflect the supplement

Pattern: **After any bulk OS addition, do a full propagation pass: B/I files → TRUST_TABLE → AI_BRIEFING → DAG → session.** The atomic propagation rule from `os-maintenance-lessons.md` applies especially after subagent-created files.

### Pitfalls encountered

1. **Heredoc + backtick collision**: `cat >> file << 'HEREDOC'` with Mermaid content (triple backticks) caused bash to execute bracket-enclosed text as commands. Fix: write to local temp file, scp, then `cat /tmp/append.md >> target.md`.
2. **Subagent directory drift**: Subagent created `bugs/B001_*.md` instead of `bug_impacts/B001_*.md`. Fix: `mv` after completion + `rmdir` the spurious directory.
3. **Remote Python quoting**: `ssh lang2 "python3 -c '...f\"Canvas: {len(c[\"nodes\"])}...\"'"` fails across 3 quoting layers. Fix: use `%` formatting: `print("Canvas: %d nodes" % len(c["nodes"]))`.

## What NOT to do (lessons from mistakes)

1. **Don't write_file to skill template paths** — Always verify target path starts with project root.
2. **Don't do full deep audit for "建立 OS" requests** — User wants a working OS, not a 3-5 hour archaeological dig.
3. **Don't copy DET_ML methodology invariants** — Every project has its own methodology rules. Read the project's own docs (GOAL.md, CHARTER, VERIFIER_RULES, PHENOMENA) and derive invariants from those.
4. **Don't leave M-entries and I-entries merged** — M-entries are methodology rules (what the system enforces). I-entries are scientific conclusions (what the research found). Extract insights into I-files when doing deep supplement.
5. **Don't use heredoc for Mermaid/code-block content over ssh** — Write locally, scp, then append.
