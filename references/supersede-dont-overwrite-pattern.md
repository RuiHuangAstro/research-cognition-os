# Supersede, Don't Overwrite: Cognition OS Revision Pattern

## User Preference (2026-05-13)

> "不要修改之前的结果, 而是标注不再可靠, 这样以后就像把他们剪切掉了,
> 我们重新做新的版本. 这样不会使得我的研究历史发生混乱."

Translation: Don't modify previous results — mark them as no longer reliable.
Treat it like cutting the wire to old conclusions and routing through new ones.
This prevents research history confusion.

## Pattern

When a new discovery invalidates an old conclusion:

### 1. Old insight → mark superseded

```yaml
# YAML frontmatter changes:
status: superseded                          # was: active
confidence: medium                          # was: high (downgrade)
tags: [..., superseded-by/I029]             # add superseded-by tag
```

```markdown
# Title: add ⚠️ SUPERSEDED

> **Superseded by [[I029_new_insight]]**.
> Brief reason why old conclusion is no longer valid.

Status: **Superseded** by I029
```

**Do NOT**:
- Delete the old insight file
- Overwrite the old Statement/Evidence sections
- Remove the old insight from AI_BRIEFING (add superseded annotation instead)

### 2. Decision Log → add superseded annotation

```markdown
## 2026-05-13 Decision: ... ⚠️ SUPERSEDED

> **Superseded by [[I029_new_insight]]**.
> Why the decision is outdated.
> Original context preserved below.

**Context**: (original text preserved verbatim)
```

### 3. TRUST_TABLE → downgrade + annotate

```markdown
| T11 | ... | **Medium** ⚠️ | Old value; superseded by I029: new value |
```

### 4. Create new insight with full evidence

New insight gets a `## Supersedes` section:

```markdown
## Supersedes

- [[I028_old_insight]] — "old claim" is not applicable because [reason]
- I013 Critical Update (date) — "old number" was from different pipeline
```

### 4b. Downstream propagation checklist

Before considering the supersede complete, scan all downstream files that mention the old insight or depend on it:

```bash
rg "I0xx_old|old_claim_keyword" research-cognition-os
```

For each downstream page, decide whether to mark it `questioned`, `provisional`, or unchanged. Update:
- YAML frontmatter `status`, `confidence`, and tags
- visible `Status:` / `Confidence:` lines
- `03_TRUST_TABLE.md`
- `00_AI_BRIEFING.md` trusted/questioned lists
- DAG/current-question files if they expose the stale claim

A bug or supersede is not fully recorded until its downstream trust state has propagated.

### 5. AI_BRIEFING → add new, annotate old

```markdown
- [[I028_old]] — ⚠️ SUPERSEDED by I029; only applies to [specific context]
- [[I029_new]] — Corrected conclusion (High).
```

### 6. DAG → update current cycle, add to DONE

```text
CUR["Current Cycle\n1. New priority from I029..."]
DONE1["Done\nI029: supersedes I028\nI028: superseded by I029\n..."]
```

## Why This Matters

Research history is a **directed acyclic graph** (DAG), not a mutable array.
Overwriting old conclusions creates orphan reasoning chains — downstream
decisions that depended on the old conclusion become untraceable.

With supersede annotations:
- Old conclusion + evidence preserved → can audit "what did we know when"
- Supersede link → can trace "why did we change our mind"
- New insight → can see "what we believe now and why"
- Research history integrity maintained

## Worked Example: I028 → I029

| What changed | Old (I028) | New (I029) |
|---|---|---|
| ML offset source | PSF sub-pixel misalignment ~4% | Background gradient (flat vs map) |
| ML_ratio | 0.961 (from fft_psf_wrapper pipeline) | 0.970 (from sb_grid_1k, 763k pts) |
| Fix needed | FFT phase shift | Use bkg map instead of flat BG_MAP |
| Applies to | fft_psf_wrapper.py only | Main run_sb_grid_1k.py pipeline |

I028 was not "wrong" — it correctly identified a bug in fft_psf_wrapper.py.
But the bug didn't affect the main pipeline. The supersede pattern preserves
this nuance rather than erasing it.