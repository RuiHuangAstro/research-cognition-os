# Cron Pipeline → Cognition OS Integration

When a project runs automated cron jobs as a pipeline (data refresh → feedback → detection → recommendation → reflection → discovery → optimization), each job must write its results to the cognition OS. Without this, the OS drifts from project reality (see OS drift audit pitfall).

## General Pattern

Every cron job in a pipeline must include a "Cognition OS 更新（强制）" section in its prompt. The specific OS artifacts written depend on the job's role in the pipeline.

### Mandatory for ALL cron jobs

1. **Session record**: Append Did/Found/Next to `sessions/YYYY-MM-DD.md` (never overwrite existing content — append or create new)
2. **AI_BRIEFING**: Update "Last updated" date and relevant sections

### Conditional by job type

| Job type | OS artifacts | Trigger condition |
|----------|-------------|-------------------|
| Data refresh | Insight (anomaly) | NAV missing, signal failure, data gap |
| Feedback collector | Insight (credit change) + TRUST_TABLE | Credit score change > threshold |
| State detector | Insight (state change) + TRUST_TABLE + AI_BRIEFING | Regime/state switch detected |
| Recommendation | Insight (shift) + AI_BRIEFING | Strategy composition change > 20% |
| Weekly reflection | Insight (weekly, mandatory) + TRUST_TABLE + CURRENT_QUESTION | Always (this IS the reflection) |
| Strategy discovery | Insight (new/negative) + TRUST_TABLE + CURRENT_QUESTION | New strategy found or hypothesis rejected |
| Parameter optimization | Insight (param change) + TRUST_TABLE + DECISION_LOG | Parameters updated |

### Insight naming convention for cron-generated insights

- Feedback: `I0xxx_feedback_YYYYMMDD.md`
- Regime switch: `I0xxx_regime_switch_YYYYMMDD.md`
- Recommendation shift: `I0xxx_recommend_shift_YYYYMMDD.md`
- Weekly reflection: `I_weekly_reflection_YYYYMMDD.md`
- Strategy discovery: `I0xxx_strategy_discovery_YYYYMMDD.md`
- Negative result: `I0xxx_no_alpha_YYYYMMDD.md` (Statement: "X CANNOT work because Y", Confidence=High)
- Param update: `I0xxx_param_update_YYYYMMDD.md`

### Cron job setup requirements

1. **Load `research-cognition-os` skill**: Add to `skills` list so the agent knows OS conventions (YAML frontmatter, wikilinks, trust classification)
2. **Include `file` toolset**: Agent needs `file` tool to write OS .md files (terminal-only jobs cannot write files)
3. **Specify OS path explicitly**: `Cognition OS 路径: <project-root>/research-cognition-os/`
4. **ID collision prevention**: Before creating any insight, check `ls insights/ | sort -t_ -k1 -n | tail -3` for highest existing number

### Confidence assignment for cron-generated insights

| Source | Default confidence | Upgrade condition |
|--------|-------------------|-------------------|
| New strategy from discovery | Low | Upgrade to Medium after 2 weeks positive feedback |
| Negative result (hypothesis rejected) | High | — |
| Parameter change from optimization | Low | Upgrade to Medium after OOS validation |
| Regime switch observation | Medium | — |
| Weekly reflection summary | Medium | — |
| Anomaly from data refresh | Low | Upgrade to Medium if persistent across sessions |

## Fund Strategy Worked Example (C1-C7)

7-cron feedback-driven pipeline with cognition OS integration:

| Cron | Name | Schedule | OS writes |
|------|------|----------|-----------|
| C1 | NAV+market refresh | EDT 14:00 | session + anomaly insight + AI_BRIEFING |
| C2 | Feedback collector | EDT 18:00 | session + credit-change insight + TRUST_TABLE upgrade/downgrade + AI_BRIEFING |
| C3 | Regime detector | EDT 21:30 | session + regime-switch insight + TRUST_TABLE + AI_BRIEFING |
| C4 | Live recommend | EDT 23:30 | session + recommend-shift insight + AI_BRIEFING |
| C5 | Weekly reflection | Sun 23:30 | session + **mandatory** weekly insight + TRUST_TABLE + AI_BRIEFING + CURRENT_QUESTION |
| C6 | Strategy discovery | Sat 06:30 | session + new/negative insight + TRUST_TABLE + AI_BRIEFING + CURRENT_QUESTION |
| C7 | Param optimization | Sun 07:00 | session + param-change insight + TRUST_TABLE + DECISION_LOG + AI_BRIEFING |

Key design decisions:
- C5 (weekly reflection) must always produce an insight — this IS the structured reflection
- C6 (discovery) new strategies start at Low confidence, need feedback validation to upgrade
- C6 negative results get High confidence — prevents future re-exploration
- C7 parameter changes go to DECISION_LOG (not just insights) — parameter decisions are project-level
- C2 credit score changes > 0.1 trigger TRUST_TABLE updates — significant enough to change strategy trust
- C3 regime switches update CURRENT_QUESTION focus — regime changes are project-level attention shifts

## Pitfalls

1. **Cron without `file` toolset cannot write OS** — Terminal-only cron jobs can run scripts but cannot write .md files. Always include `file` in `enabled_toolsets`.
2. **Session record append, not overwrite** — Multiple crons may run on the same day. Each appends its Did/Found/Next, never overwrites the existing session file.
3. **Insight ID collision across concurrent crons** — If C5 and C6 both run on Sunday and both create insights, they may collide on I0xx numbering. Always `ls insights/ | tail -3` before creating.
4. **Don't create insights for routine operations** — NAV refresh that succeeds normally → session record only. Insight only for anomalies. Otherwise the OS gets flooded with trivial entries.
5. **Weekly reflection insight is non-optional** — Unlike daily crons where insights are conditional on anomalies, the weekly reflection MUST produce an insight. This is the cognitive checkpoint.
