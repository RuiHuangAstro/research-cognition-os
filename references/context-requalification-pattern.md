# Context Re-Qualification Pattern (认知语境重定位)

## When to use

An old insight's conclusion is **correct within its original scope** but the overall
understanding has evolved because a new method, data, or framing changed the context.
This is NOT a full supersede (old conclusion is not wrong) — it's a **scope re-qualification**:
the old claim is still true, but its implications have changed.

## Distinction from other patterns

| Pattern | Old insight | Relationship | Example |
|---------|------------|--------------|---------|
| **Supersede** | Wrong / invalidated | New replaces old | I028 ML offset = PSF → I029 = background gradient |
| **Negative result** | Hypothesis ruled out | Dead end recorded | Edgeworth cannot explain variance |
| **Context re-qualification** | Correct, but scope narrowed | Old still true in original domain; new insight expands the picture | I015 "Kβ drift uncorrectable" → I019 D1 "Kα drift correctable for slow component" |

## Pattern

### 1. Update old insight — add "认知演进" section

Do NOT change the original Statement/Evidence. Add a new section:

```markdown
## 认知演进

| 阶段 | 方法 | 结论 |
|------|------|------|
| I0xx (old) | [old method] | [old conclusion — still correct in scope] |
| I0yy (new) | [new method] | [new conclusion — broader context] |

**关键突破：** [One sentence explaining why the picture changed.]
```

### 2. Add YAML `updated` field

```yaml
updated: 2026-06-20
tags: [..., context-requalified-by/I021]
```

### 3. Update TRUST_TABLE — annotate, don't overwrite

```markdown
| I0xx | Observation | **Trusted (context updated)** | ... | Kβ 统计不足; **Kα 方法已成功校正慢分量（I0yy）** |
```

Note the `(context updated)` tag in Status column — this signals that the trust
level hasn't changed but the implications have.

### 4. Create new insight with explicit link

The new insight should reference the old one in its `## Supersedes` or `## Related` section,
and explain *why* the picture changed without claiming the old insight was wrong:

```markdown
## Related

- [[I0xx_old_insight]] — Kβ 统计不足的结论正确; 本 insight 用 Kα 统计量突破此限制
```

### 5. Update AI_BRIEFING — add evolution summary table

Add a dedicated section (not just inline annotation):

```markdown
## ⚠️ 漂移认知演进（I015 → I019 → I021）

| 阶段 | 方法 | 统计量 | 结论 |
|------|------|--------|------|
| I015 | Kβ 单线追踪 | ~100/file | 统计不足，无法校正 |
| I019 D1 | Kα 固定形状双峰质心 | ~800/file | **慢漂移可校** |
| I021 | 三分类框架 | — | A:慢可校 B:快不可校 C:增益不稳不可校 |
```

### 6. Update affected downstream files

Same propagation checklist as supersede pattern, but with lighter touch:
- S12 stage: add "认知演进" note, change status to `Superseded (by S13)`
- CURRENT_QUESTION: add refined exclusion (e.g., "Kβ 排除但 Kα 可校慢分量")
- DAG: add new node + link from old insight to new classification

## Why this pattern matters

Without context re-qualification, old insights that say "X is impossible" become
landmines — future sessions read them and don't attempt the now-possible approach.
The key is making the *scope* of the old claim explicit: "X is impossible **with method Y**"
is very different from "X is impossible **in general**".

The evolution summary table in AI_BRIEFING is critical: it lets future sessions
see the cognitive trajectory at a glance, rather than having to reconstruct it
by reading multiple insight files.

## Worked example: I015 → I019 → I021

| What changed | I015 (old) | I019 D1 (new) | I021 (classification) |
|---|---|---|---|
| Tracer | Kβ single-line centroid | Kα fixed-shape doublet centroid | N/A (meta) |
| Statistics | ~100 events/file | ~800 events/file | N/A |
| Conclusion | "Drift uncorrectable" | "Slow drift correctable" | "Three classes with different correctability" |
| Scope | Kβ-based correction only | Kα-based slow-drift correction | Full drift taxonomy |

I015 was never wrong — Kβ statistics ARE insufficient. But the broader claim
"文件内漂移无法可靠校正" was scope-creep: it generalized from one method to all methods.
I019 showed a different method works for a subset. I021 made the subset explicit.
