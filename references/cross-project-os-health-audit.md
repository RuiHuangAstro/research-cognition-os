# Cross-Project OS Health Audit Methodology

This document captures the systematic procedure for auditing the health of multiple cognition OS deployments across different projects, as developed from the empirical audit of 14 active OS projects and 11 zero-OS projects on 2026-06-18.

## Why Cross-Project Audit?

Single-project OS drift audits (checking if code has outpaced session updates) are necessary but not sufficient. When managing a fleet of cognition OS deployments, you need to detect systemic patterns:

1. **Methodology neglect**: Most projects fail to audit their own methodology (pipeline steps, optimizer choices, statistic choices) as trust items
2. **Session abandonment**: After initial enthusiasm, daily session recording drops to zero
3. **DAG decay**: Multi-format DAG generation (Mermaid → Canvas → PDF/PNG/SVG) falls back to just Mermaid or nothing
4. **Zero-OS proliferation**: Active code projects grow without any cognition OS, losing cognitive history

## The 6-Minute Fleet Health Scan

Run these commands to get a rapid health overview:

```bash
# 1. Find all OS deployments
find ~/program ~/Data -maxdepth 4 -type d -name 'research-cognition-os' 2>/dev/null | tee /tmp/os_dirs.txt

# 2. For each, get key metrics (paste into terminal)
while read d; do
  name=$(basename $(dirname "$d"))
  files=$(find "$d" -name '*.md' -o -name '*.yaml' | wc -l)
  stages=$(find "$d/stages" -name '*.md' 2>/dev/null | wc -l)
  insights=$(find "$d/insights" -name '*.md' 2>/dev/null | wc -l)
  sessions=$(find "$d/sessions" -name '*.md' 2>/dev/null | wc -l)
  last_sess=$(ls -t "$d/sessions/"* 2>/dev/null | head -1 | xargs -I{} stat -c '%Y' {} 2>/dev/null || echo "0")
  last_code=$(find "$(dirname "$d")" -name '*.py' -printf '%T@\n' 2>/dev/null | sort -rn | head -1 || echo "0")
  gap=$(( ($last_code - $last_sess) / 86400 ))
  [ "$gap" -lt 0 ] && gap=0
  method=$(grep -ci 'method\|methodology\|pipeline\|approach\|workflow' "$d/03_TRUST_TABLE.md" 2>/dev/null || echo "0")
  total=$(grep -c '^|' "$d/03_TRUST_TABLE.md" 2>/dev/null | echo $(( $(grep -c '^|' "$d/03_TRUST_TABLE.md" 2>/dev/null) - 2 )) || echo "0")
  [ -z "$total" ] && total=0
  pct=$(( total > 0 ? (method * 100) / total : 0 ))
  briefing=$(head -5 "$d/00_AI_BRIEFING.md" 2>/dev/null | grep -oP 'Last updated: \K.*' || echo "N/A")
  echo "$name | F:$files S:$stages I:$insights Ses:$sessions Drift:${gap}d Method:$method/$total($pct%) Brief:$briefing"
done < /tmp/os_dirs.txt

# 3. Find zero-OS projects (code dirs with substantial Python but no OS)
echo "=== ZERO-OS PROJECTS ==="
for d in ~/program/*/; do
  [ -d "$d/research-cognition-os" ] && continue
  pycount=$(find "$d" -maxdepth 2 -name '*.py' 2>/dev/null | wc -l)
  [ "$pycount" -gt 5 ] && echo "$(basename "$d"): ${pycount} Python files, no OS"
done
for d in ~/Data/*/; do
  [ -d "$d/research-cognition-os" ] && continue
  pycount=$(find "$d" -maxdepth 2 -name '*.py' 2>/dev/null | wc -l)
  [ "$pycount" -gt 5 ] && echo "$(basename "$d"): ${pycount} Python files, no OS"
done
```

## Interpreting the Results

### Health Scoring Matrix

| Metric | Healthy | Warning | Critical | Weight |
|--------|---------|---------|----------|--------|
| **OS Drift** (code vs session age) | 0-2 days | 3-14 days | >14 days | 25% |
| **Session Frequency** | ≥ weekly | ≥ monthly | none | 20% |
| **Methodology Coverage** (method rows / total TRUST_TABLE) | ≥20% | 5-20% | <5% | 20% |
| **DAG Completeness** (formats: Mermaid+Canvas+PNG/SVG) | 3+ formats | 1-2 formats | 0 formats | 15% |
| **Zero-OS Projects** (count) | 0 | 1-3 | >3 | 20% |

### Priority Remediation Order

1. **Critical Drift (>14 days)**: Immediate routine OS sync (15-30 min)
   - Do NOT start deep audit—this wastes time when the OS is salvageable
   - Run: `Read current OS state → Extract latest AI session → Diff → Fill gaps`
   
2. **Zero Methodology (<5%)**: Add methodology trust items
   - For each major pipeline step: `PSF-template generation | Methodology | Provisional`
   - Target: Reach 20% coverage within 2 weeks
   
3. **Zero-OS Projects**: 15-minute streamlined audit per project
   - `mkdir -p OS_DIR/{stages,insights,experiments,bug_impacts,sessions,artifacts}`
   - Copy templates for 00-05 files
   - Write one-sentence AI_BRIEFING, CURRENT_QUESTION, TRUST_TABLE (3 rows)
   - Create session for today
   
4. **Incomplete DAG (<3 formats)**: Generate missing formats
   - Minimum: Mermaid (in 05_PROJECT_DAG.md) + Canvas (PROJECT_DAG.canvas)
   - Optional: PDF/PNG/SVG via `cd dag/ && python generate_dags.py`

## Empirical Baselines (from 2026-06-18 Audit)

### Deployment Health Distribution

| Project | Files | Stages | Insights | Sessions | Drift | Methodology Rows | Methodology Pct | DAG Formats |
|---------|-------|--------|----------|----------|-------|------------------|-----------------|-------------|
| DET_ML_Uncertainty | 257 | 10 | 46 | 5 | 33d | 3 | 92 | 3 (Mermaid+Canvas+PNG) |
| fxt_data_reduction | 15 | 3 | 3 | 1 | 0d | 2 | 14 | 1 (Mermaid only) |
| M104_TwoPhaseGas | 23 | 3 | 8 | 3 | 0d | 0 | 18 | 0 |
| M31Center (prog) | 37 | 5 | 15 | 2 | 17d | 8 | 23 | 2 |
| M31CGM | 14 | 1 | 4 | 2 | 17d | 3 | 18 | 2 |
| M31HotISM | 2 | 0 | 0 | 0 | 0d | 0 | 0 | 0 |
| M31-τX | 9 | 1 | 4 | 1 | 0d | 0 | 4 | 0 |
| N132D | 26 | 4 | 4 | 1 | 0d | 0 | 4 | 3 |
| NGC3079 | 65 | 7 | 11 | 2 | 1d | 0 | 15 | 3 |
| XARTATOMS | 68 | 6 | 38 | 10 | 8d | 12 | 95 | 0 |
| xmm_psf_ellbeta | 33 | 4 | 15 | 1 | 3d | 1 | 7 | 0 |
| 星上算法 | 53 | 10 | 16 | 13 | 0d | 7 | 64 | 1 |
| M31Center (data) | 18 | 3 | 3 | 1 | 0d | 0 | 3 | 1 |
| M82 | 21 | 4 | 4 | 2 | 0d | 0 | 4 | 1 |

### Zero-OS Projects Found

Projects with >5 Python files but zero cognition OS:
- astro_evo_mvp (61 py)
- cstat (86 py) 
- playground (87 py)
- ScienceAgent (8 py)
- xmm (53 py)
- Abell85 (6 py)
- astro_evo_mvp (61 py)
- astro_evo_v0.0.1 (50 py)
- ChandraClusterRepro (15 py)
- fxt-gui (6 py)
- M51 (6 py)
- M86 (6 py)
- NGC3221 (7 py)
- NGC891 (6 py)
- PDF2DOC (16 py)
- pipeline_demo (15 py)

## Automation Opportunities

### Health Check Cron Job
Create a weekly cron job that:
1. Runs the 6-minute fleet scan
2. Scores each deployment
3. Sends Bark notification if any project hits Critical in ≥2 categories
4. Auto-generates remediation tickets for:
   - Drift >14d → Routine OS sync task
   - Methodology <5% → Add methodology trust items task  
   - Zero-OS → Streamlined audit task

### DAG Generation Hook
Add to OS update workflow:
```bash
# After any change to AI_BRIEFING, TRUST_TABLE, stages/, insights/
if git diff --name-only HEAD~1 HEAD | grep -E '^(00_|03_|stages/|insights/)' ; then
  cd "$OS_DIR/dag" && python generate_dags.py
fi
```

## Common Failure Patterns Observed

### Pattern 1: Methodology Neglect (Systemic)
- **Symptom**: TRUST_TABLE has 0-3 methodology entries out of 15-95 total
- **Root Cause**: Teams treat OS as "conclusion audit" not "methodology audit"
- **Fix**: Make methodology items explicit in CURRENT_QUESTION: "This week we validate: [optimizer choice], [statistic choice], [PSF dependency]"

### Pattern 2: Session Abandonment 
- **Symptom**: 1-2 session files (initialization), then none for months
- **Root Cause**: Seen as optional documentation, not cognitive history
- **Fix**: Tie session commits to code commits: `git commit` requires updating sessions/TODAY.md

### Pattern 3: DAG Decay
- **Symptom**: Only Mermaid in 05_PROJECT_DAG.md, no Canvas/PDF/PNG
- **Root Cause**: Belief that "Mermaid is enough for GitHub"
- **Fix**: Treat DAG as multi-format deliverable like a paper (PDF+supplementary)

### Pattern 4: Zero-OS Drift
- **Symptom**: Growing codebase with zero OS, team says "we'll add it later"
- **Root Cause**: Perceived as heavyweight initiation
- **Fix**: 15-minute streamlined audit delivers 80% of value for 20% effort

## References

This methodology was validated against:
- DET_ML_Uncertainty deep audit (8-phase, 105 summary files)
- 13 other active cognition OS deployments  
- 11 zero-OS projects with substantial code
- Session records from Claude Code, Codex, and Hermes
- Cross-project consistency checks (AI_BRIEFING ↔ TRUST_TABLE ↔ DAG)

For single-project deep audit methodology, see `deep-audit-methodology.md`.
For routine OS sync procedure, see `routine-os-sync-pattern.md`.