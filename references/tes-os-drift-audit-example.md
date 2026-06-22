# TES 星上算法 OS Drift Audit Example (2026-06-05)

## Context

Session was asked to read-only review the cognition OS for the TES 星上算法 project.
Discovered the OS was severely behind the actual code progress.

## Drift diagnosis pattern

1. `find ~/program/星上算法/code/ -name '*.py' -printf '%T+ %p\n' | sort -r | head -5`
   → Latest code: v51_kalpha_plot.py (2026-06-05)
2. `ls -lt research-cognition-os/sessions/ | head -3`
   → Latest session: 2026-06-01 (4 days behind)
3. AI_BRIEFING "Current focus" mentions V44 but code has v51
4. TRUST_TABLE last updated 2026-06-02, missing V44/V46 entries
5. CURRENT_QUESTION still targets "复现 4eV" — already achieved at 4.42 eV

## What was missing from OS

| Missing item | Code version | Date |
|---|---|---|
| 5 session records (6/2-6/5) | V39-V51 | 6/2-6/5 |
| D19-D24 decisions | V39-V46 | 6/2-6/4 |
| E004-E007 experiments | V39, V40, V44, V46 | 6/2-6/4 |
| S05-S10 stages | V39-V46 cognitive phases | 6/2-6/4 |
| I009+ insights | timing=jitter, phase-shifted OF, sigma bound | 6/2-6/4 |
| TRUST_TABLE V39-V46 entries | 8+ new rows | 6/2-6/4 |
| DAG update | V39-V46 nodes | 6/2-6/4 |

## Key breakthroughs not in OS

1. **V39**: Timing jitter is the 21eV system term (φ swing=52.5eV)
2. **V40**: G7 OFFICIAL = 5.34 eV (upsampled whitened φ + spline CV)
3. **V44**: Phase-shifted OF eliminates post-hoc spline → G7=5.58 eV, no overfitting risk
4. **V46**: Sigma lower bound artifact (4.71eV = 2.3548 × 0.002keV bound). Relaxed → 4.42 eV

## Root cause of drift

Between 6/1 and 6/5, the user drove the analysis via Claude Code (not Hermes),
so Hermes sessions didn't capture the work. The OS was only updated when
Hermes sessions were active (5/28, 6/1). Claude Code sessions leave traces
in `~/.claude/projects/` but these weren't harvested into the OS.

## Recovery technique: Extracting results from Claude Code JSONL

When OS is behind and you need the latest results, extract structured numerical
data from Claude Code session JSONL using targeted `grep` patterns on the
`toolUseResult.stdout` field (NOT assistant message text):

```bash
# Find the latest session for the project
ls -lt ~/.claude/projects/<project-dir>/*.jsonl | head -3

# Extract per-file FWHM results
grep -o 'File [0-9].*FWHM=[^ ]*' SESSION.jsonl | head -20

# Extract Kα median shifts (gain calibration)
grep -o 'File [0-9].*Ka median=[^ ]*' SESSION.jsonl | head -20

# Extract M4 fit results
grep -o 'M4.*FWHM=[^ ]*.*chi2=[^ ]*' SESSION.jsonl | head -10

# Extract version-to-version FWHM comparisons
grep -o 'V[0-9][0-9].*FWHM=[^ ]*' SESSION.jsonl | head -20
```

For multi-line structured output (tables, segment results), use Python JSONL
parsing to extract `toolUseResult.stdout` and process line by line.

See also: `codex-session-search` skill → "Extracting Quantitative Research Results from JSONL" section.

## Lesson

When multiple AI tools operate on the same project, the OS only gets updated
by the sessions that know about it. Claude Code / Codex sessions produce
code and output files but don't write to research-cognition-os/. The Hermes
agent must periodically audit the gap between code timestamps and OS timestamps.
When drift is detected, recover latest results from the other tool's session JSONL
before attempting OS updates.