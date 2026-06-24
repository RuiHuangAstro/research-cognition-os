# Research Cognition OS

[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-blue)](https://github.com/NousResearch/hermes-agent)

A **Hermes Agent skill** for structured management of cognitive states, trust levels, dependencies, and attention allocation in scientific research projects.

## What It Does

Every research branch must answer: *What question does it ask? What method? What evidence? Can we still trust it? What decisions did it drive? Where are the artifacts?*

This is not task management — it's **cognitive state management**.

### Core Files (per project)

| File | Purpose |
|------|---------|
| `00_AI_BRIEFING.md` | Machine-readable project summary |
| `01_PROJECT_INDEX.md` | Project global index |
| `02_CURRENT_QUESTION.md` | Active question + sub-questions |
| `03_TRUST_TABLE.md` | Evidence → trust → decision ledger |
| `04_DECISION_LOG.md` | Major decision records |
| `05_PROJECT_DAG.md` | Research DAG (Mermaid) |
| `stages/` | Research stage progression |
| `insights/` | Key findings with confidence levels |
| `experiments/` | Experiment manifests + results |
| `bug_impacts/` | Bug impact assessments |
| `sessions/` | Per-session formalization |

### Key Concepts

- **Trust Level**: Every claim has a trust level (high/medium/low/refuted) that evolves with evidence
- **Research DAG**: Mermaid-based dependency graph showing how questions, methods, and evidence connect
- **Supersede, Don't Overwrite**: New evidence supersedes old; history is preserved
- **Methodology Invariants**: Statistical research rules promoted to cognition OS files, not buried in session logs

## Install as Hermes Skill

```bash
hermes skills install https://raw.githubusercontent.com/RuiHuangAstro/research-cognition-os/main/SKILL.md
```

Or manually:

```bash
# Copy to your Hermes skills directory
cp -r . ~/.hermes/skills/note-taking/research-cognition-os/
```

## Directory Structure

```
research-cognition-os/
├── SKILL.md              # Skill definition (YAML frontmatter + full methodology)
├── README.md             # This file
├── .gitignore
├── references/           # 42 reference documents
│   ├── dag-design-principles.md
│   ├── deep-audit-methodology.md
│   ├── orchestrator-deployment.md
│   ├── variance-conditioning-trap.md
│   └── ...
├── scripts/              # Automation scripts
│   ├── cog_os_cron.sh         # Cron sync
│   ├── cog_os_drift_detect.sh # Drift detection
│   └── session_linter.py      # Session formalization linter
└── templates/            # 13 project templates
    ├── ai-briefing-template.md
    ├── trust-table-template.md
    ├── insight-template.md
    └── ...
```

## One-Line Methodology

```
Question → Attempt → Evidence → Trust Level → Decision → Artifact Index
```

## License

MIT
