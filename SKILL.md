---
name: research-cognition-os
description: >
  科研认知操作系统 (Research Cognition OS): 结构化管理研究项目的
  认知状态、可信度、依赖关系与注意力分配。核心文件：AI_BRIEFING.md,
  TRUST_TABLE.md, CURRENT_QUESTION.md, 以及 stages/ insights/ experiments/
  bug_impacts/ sessions/ 目录体系。配套 Mermaid 研究 DAG 可视化。
  包含一键初始化流程 (cognition-os-init 已合并)。
category: note-taking
---

# 科研认知操作系统 (Research Cognition OS)

管理科研项目的认知状态、可信度、依赖关系与注意力分配。

## 核心理念

> 每一个研究分支都必须说明：它想回答什么问题、用了什么方法、产生了什么证据、现在还能不能信、导致了什么决策、相关材料在哪里。

这不是任务管理，而是**认知状态管理**。

**项目范围规则**: 学习性子任务不单独建项目，必须归属到主项目的 cognition OS 下。详见 `references/project-scoping-rules.md`。

## Scope & contribution rules (read before adding anything to this skill)

This skill is a **project-agnostic** method for building and maintaining a cognition OS. It must
stay that way. The single most common failure mode is **pollution**: while working on a concrete
project, an agent learns a useful pitfall and writes it back into *this* `SKILL.md` instead of into
the project's own OS. Over time the skill fills with one project's physics/quant conventions, bug
catalogs, and numeric results — bloating the always-loaded context and confusing every other project.

**Litmus test before writing anything into this skill or its `references/`:**

> *"Would this exact sentence help someone building a cognition OS for a completely unrelated
> project?"*

If the lesson names a specific dataset, instrument, variable (`DeltaC`, `S_hat`, a PSF template),
file name, optimizer, numeric result, or bug — the answer is **no**. It is project knowledge, and
it belongs in **that project's** `research-cognition-os/`:

| The lesson is about… | Write it here (inside the project, never in this skill) |
|---|---|
| a result / convention / formula | `insights/Ixxx_*.md` (+ a `03_TRUST_TABLE.md` row) |
| a bug and its blast radius | `bug_impacts/Bxxx_*.md` |
| a recurring project-local gotcha | a project-local `PITFALLS.md` or the active stage |

Only genuinely domain-neutral lessons about *running an OS* (consistency checks, drift, ID
numbering, supersede-don't-overwrite, …) belong here — collected in
`references/os-maintenance-lessons.md`.

Pitfalls that already leaked in (DET_ML, M104, X-ray, backtest, …) have been moved out of context
to `references/_archived-leaked-project-pitfalls.md` — that file is a read-only holding pen; do not
extend it and do not copy from it.

### ⚠️ Draining the holding pen (when the user asks to redistribute leaked pitfalls)

The holding pen is "read-only" in the sense of *don't add to it and don't copy from it back into
the skill*. But the user may legitimately ask to **drain** it — move the archived pitfalls into
their target project OS directories. When that happens:

1. **Read the archived file** to enumerate all pitfalls.
2. **Classify each pitfall by target project** — look for project names (DET_ML, M104, M31CGM,
   NGC3079, Fund Strategy, …), instrument names (XMM/Chandra/FXT), and variable names
   (`DeltaC`, `S_hat`, PSF templates, …).
3. **Create a `PITFALLS.md` per target project** at `<project>/research-cognition-os/PITFALLS.md`
   with YAML frontmatter (`type: meta`, `tags: [cog/meta, project-specific]`). Do NOT create one
   `insights/Ixxx_*.md` per pitfall — that floods the insight namespace. A single consolidated
   `PITFALLS.md` is the right format for bulk-migrated content.
4. **Cross-reference existing insights** when writing — subagents should read each project's
   existing `insights/` and `03_TRUST_TABLE.md` first, then cite specific IDs (e.g., "I043",
   "T03") in the new PITFALLS.md so the migrated content is anchored to the project's own OS.
5. **Deduplicate** — the archived file often contains duplicated entries from copy-paste. Pick
   one canonical version per pitfall.
6. **Use parallel `delegate_task` subagents** — one per target project, each with the full list
   of pitfalls for that project plus the project's existing insight IDs for cross-referencing.
7. **Create `OS_MAINTENANCE.md` per project** — a lightweight file at
   `<project>/research-cognition-os/OS_MAINTENANCE.md` with (a) a one-line reference to
   `references/os-maintenance-lessons.md` listing the 10 generic lessons, and (b) a
   `## 项目特异补充` section for project-specific maintenance notes (e.g., DAG design
   lessons, tool conflicts, session audit procedures). This avoids repeating the full
   generic text in every project while giving each project a local copy of its own additions.
8. **Copy project-specific references** — some files in the skill's `references/` directory
   are session-specific to a particular project (e.g., `i044-catalog-bridge-session.md` →
   DET_ML, `m104-cgm-2d-kt-map-orchestrator-session.md` → M104). Copy these into the
   target project's `research-cognition-os/references/` so the project OS is self-contained.
   The skill's copy stays as the upstream reference; the project copy is for local use.
9. **Do NOT modify the holding pen** after draining — leave it as-is so future sessions can
   verify what was migrated.

For the full 3-round drain procedure with categorization rules and verification commands, see
`references/holding-pen-drain-procedure.md`.

**Worked example (2026-06-22, 3 rounds)**:

| Round | Action | Files created |
|-------|--------|--------------|
| 1 | Classify ~90 archived pitfalls by project, create `PITFALLS.md` per project | 10 PITFALLS.md (DET_ML: 61, M104: 4, M31CGM: 4, M31-τX: 2, M31Center: 4, Fund_strategy_X: 5, fxt_data_reduction: 4, NGC3079: 3, 星上算法: 5, N132D: 3) |
| 2 | Create `OS_MAINTENANCE.md` per project, copy project-specific references from skill | 10 OS_MAINTENANCE.md + 9 references to 6 projects |
| 3 | Distribute remaining project-specific references, create PITFALLS.md for newly discovered projects (XARTATOMS, M82, ScienceAgent_cstat_v2), supplement NGC3079 | 3 more PITFALLS.md + 3 OS_MAINTENANCE.md + 17 references to 7 projects |

**Final totals**: 13 PITFALLS.md, 13 OS_MAINTENANCE.md, 26 reference files distributed across 11 projects. 4 parallel `delegate_task` subagents handled round 1 bulk writes. The skill's `_archived-leaked-project-pitfalls.md` was left untouched (read-only holding pen). None of the 14 generic references in the skill were distributed — only project-specific ones.

## 一句话方法论

```text
Question → Attempt → Evidence → Trust Level → Decision → Artifact Index
```

## Methodology invariants are project-specific — promote them, don't hardcode them

Every project has a few **methodology invariants** (conventions, the optimizer/statistic it
uses, what variable to condition on, abundance tables, …). These are high-value, but they are
**per-project** — they belong in *that project's* `00_AI_BRIEFING.md` / `02_CURRENT_QUESTION.md` /
`03_TRUST_TABLE.md` (as a first-class trust row so downstream agents see them before the detailed
insights), **not** in this shared skill.

The meta-rule for any project: when it studies conditional distributions or simulation/catalog
statistics, condition on observables (not simulation truth), analyze residuals of the primary
statistic (not cuts on a nonlinear transform of it), and make the methodology a named trust item.
Fill in the concrete variable names in the project's own OS. Do **not** copy another project's
invariants here — see "Scope & contribution rules" below.

## 项目文件结构

```text
<project-root>/
  00_AI_BRIEFING.md          # AI 入口导航摘要
  01_PROJECT_INDEX.md        # 项目全局索引
  02_CURRENT_QUESTION.md     # 当前注意力锚
  03_TRUST_TABLE.md          # 项目可信度总表
  04_DECISION_LOG.md         # 重大决策记录
  05_PROJECT_DAG.md          # 研究 DAG (Mermaid)

  stages/                    # 认知演化阶段
    S01_xxx.md

  insights/                  # 沉淀知识
    I001_xxx.md

 experiments/ # 可重复实验 (FLAT: Exxx_name.md + Exxx_name_manifest.yaml)
 Exxx_name.md
 Exxx_name_manifest.yaml

 bug_impacts/ # Bug 影响审计
 B001_xxx.md

  sessions/                  # 每日最低成本记录
    YYYY-MM-DD.md

  artifacts/
    derivations/
    figures/
    scripts/
    configs/

  PITFALLS.md              # 项目专属 pitfall 清单 (bulk-migrated from skill)
  OS_MAINTENANCE.md         # OS 维护手册 (通用引用 + 项目特异补充)
  references/               # 项目特异 session 细节 (从 skill references/ 复制)
```

## 核心文件规范

### 00_AI_BRIEFING.md

AI 进入项目的入口文件，100–200 行以内。

```markdown
# AI Briefing: <Project Name>

Last updated: YYYY-MM-DD

## One-paragraph project summary
...

## Current focus
...

## Cognitive history in <N> stages
1. ...

## Currently trusted
- ...

## Currently questioned
- ...

## Open questions
1. ...

## AI instruction
Before giving suggestions, classify any proposed conclusion as:
Trusted / Provisional / Questioned / Deprecated.
```

### 02_CURRENT_QUESTION.md

强制规定本周/当前只回答一个主问题。

```markdown
# Current Question

Updated: YYYY-MM-DD

## Main question this week
...

## Not the current question
- Do not ...

## Success criterion
...

## Next concrete action
...

## Parking Lot
- ...
```

### 03_TRUST_TABLE.md

项目最需要的文件：回答"过去哪些东西还能信"。

```markdown
# Trust Table

| Item | Type | Status | Depends on ...? | Current trust | Notes |
|---|---|---|---|---|---|
```

状态分类：Trusted / Provisional / Questioned / Deprecated

### stages/Sxx_xxx.md

记录认知演化，不是 daily log。

```markdown
# Sxx: Stage Name

Status: Active | Archived
Started: YYYY-MM-DD
Current trust: High / Medium / Low

## Why this stage started
## Core idea
## What this stage produced
## What remains valid
## What remains open
## Links
```

### insights/Ixxx_xxx.md

每个重要结论单独抽离。

```markdown
# Ixxx: Insight Title

Status: Active
Confidence: High / Medium / Low
Created: YYYY-MM-DD
Last reviewed: YYYY-MM-DD

## Statement
## Assumptions
## Evidence
## Dependencies
## Limitations
## Used by
```

### experiments/ (Flat format: Exxx_name.md + Exxx_name_manifest.yaml)

每次实验都有 manifest + summary（两个文件，平铺在同一目录下）。

```yaml
# Exxx_name_manifest.yaml
experiment_id: Exxx_name
date: YYYY-MM-DD
status: active | questioned | deprecated
trust_level: high | medium | low
question: >
  ...
code_commit: abc1234
inputs:
  ...
outputs:
  ...
main_result: >
  ...
known_issues:
  ...
linked_bug: [B001_xxx]
linked_insights: [I001_xxx]
```

### bug_impacts/Bxxx_xxx.md

Bug 不是一句"之前错了"，而是一次审计。

**⚠️ 必须与项目 BUGREPORT 交叉验证** — 如果项目有 `BUGREPORT_*.md`，B001 的 bug 列表必须与 BUGREPORT 完全一致。遗漏 bug 会导致污染范围低估。

```markdown
# Bxxx: Bug Name

Discovered: YYYY-MM-DD
Status: Active audit

## Bug summary
## Bug details (per bug: description, severity, affected code, impact)
## Affected code versions
## Affected outputs
## Not affected
## Conclusion audit (table)
## Recovery plan

## Cross-reference
- BUGREPORT_xxx.md: [link] — verified all bugs accounted for? Y/N
```

### sessions/YYYY-MM-DD.md

每天只写三行：Did / Found / Next。必须包含 YAML frontmatter，且每个 section 内容必须为 bullet points 格式。

```markdown
---
type: session
status: active
created: YYYY-MM-DD
tags: [cog/session]
---

# Session YYYY-MM-DD

## Did
- ... (bullet points starting with '- ')

## Found
- ... (bullet points starting with '- ')

## Next
- ... (bullet points starting with '- ')

## Related (optional, but encouraged)
- [[Sxx_stage]] — worked-on
- [[Exxx_experiment]] — ran
- [[Ixxx_insight]] — discovered
```

**详见**：[references/session-formalization-pitfalls.md] 包含完整的 linting 脚本、Pitfall 分析和使用指南。

## 研究 DAG 可视化

三类图，多格式输出：

- **Cognitive DAG**: 认知演化路径
- **Trust DAG**: 可信度依赖与污染链
- **Frontier DAG**: 当前注意力前沿 (5–10 节点)

节点分类：Q (Question), H (Hypothesis), D (Derivation), E (Experiment), I (Insight), B (Bug/Blocker)

边类型：supports, depends_on, invalidates, supersedes, motivates, contaminates

状态颜色：
- Trusted (绿), Provisional (黄), Questioned (红), Deprecated (灰), Current (蓝)

### 多格式输出 (Mandatory)

每个 DAG 必须输出 5 种格式：

| Format | Location | Best for |
|--------|----------|----------|
| Mermaid | 嵌入 `05_PROJECT_DAG.md` | GitHub / Obsidian markdown preview |
| Canvas | `PROJECT_DAG.canvas` | Obsidian interactive drag-zoom-click |
| PDF | `dag/<name>.pdf` | Print / high-res vector |
| PNG | `dag/<name>.png` | Quick preview (200 dpi) |
| SVG | `dag/<name>.svg` | Web embed / Obsidian inline |

**Regenerate all**: `cd dag/ && python generate_dags.py`

### Canvas 规范

- **优先用 `type: "file"` 节点** — 直接指向 .md 文件，点击跳转
- 仅 Questions (Q 节点) 用 `type: "text"` — 因为 Q 不对应独立文件
- 颜色编码：4=Trusted, 3=Provisional, 5=Questioned, 6=Current, 2=Deprecated
- 布局：5 行 — Q(y=-600) → Stage(y=-300) → Exp(y=0) → Insight(y=300) → Bug(y=600)
- X 间距 350px，左到右按认知流
- 污染边用 `color: "5"` (红)

### ⚠️ Mermaid / Graphviz 布局限制 (general)

Mermaid `flowchart LR`/`flowchart TB` 使用 Dagre 自动布局，**不保证 parent 在 child 上方/左方**。常见问题：箭头向下但 child 出现在 parent 上方（箭头拐 180°）；`subgraph` 内 `direction LR` 与外层 `TB` 冲突导致错位；多条 cross-layer 边导致布局"爆炸"。

解决方案：

- **Mermaid 用 compact summary 节点**（一个 phase 一个节点），同时生成 Graphviz PDF 保证精确布局。
- **Graphviz 不用 cluster**（cluster 与 `rank=same` 冲突），改用 `plaintext` 节点做 section label + invisible edge 强制层序。
- **Cross-layer 边（污染/回溯箭头）加 `constraint=false`**，否则会干扰主布局的垂直排序。
- **DAG 不能有回边** — 每次回滚生成新节点（S04 → S04b），保持 acyclic。
- **不要一开始就自动化 DAG** — 先手动画 20 个节点，再考虑 Graphviz/脚本生成。
- **不要完美主义** — `00_AI_BRIEFING.md` 先写 100 行，不要等"完整"。

### OS 维护通用经验

跨项目通用的 OS 维护经验（内部一致性检查、drift 审计、routine sync、ID 编号冲突、原子传播、supersede-不覆盖、负结果当一等公民、session 记录优先、subagent 交叉验证、长任务不轮询）已统一收录到 **`references/os-maintenance-lessons.md`**。这些是 domain-neutral 的；**项目特有的 pitfall 不要写进本 skill**（见上方 "Scope & contribution rules"）。

## Templates

All starter files are in `templates/` — copy and customize per project:

| Template | Purpose |
|----------|---------|
| `ai-briefing-template.md` | 00_AI_BRIEFING.md starter |
| `current-question-template.md` | 02_CURRENT_QUESTION.md starter |
| `trust-table-template.md` | 03_TRUST_TABLE.md starter |
| `decision-log-template.md` | 04_DECISION_LOG.md starter |
| `project-dag-template.md` | 05_PROJECT_DAG.md Mermaid starter (with classDef colors) |
| `stage-template.md` | stages/Sxx_xxx.md starter |
| `insight-template.md` | insights/Ixxx_xxx.md starter |
| `experiment-manifest-template.yaml` | experiments/Exxx/manifest.yaml starter |
| `experiment-summary-template.md` | experiments/Exxx/summary.md starter |
| `bug-impact-template.md` | bug_impacts/Bxxx_xxx.md starter |
| `session-template.md` | sessions/YYYY-MM-DD.md starter |
| `pitfalls-template.md` | PITFALLS.md starter (bulk-migrated project pitfalls) |
| `os-maintenance-template.md` | OS_MAINTENANCE.md starter (generic ref + project-specific) |

## Learning-Project Initialization

Not every cognition OS is built for an established research project. When the user's goal is **"learn to use X"** (e.g., a new instrument pipeline, a new analysis framework), the OS serves a different purpose: tracking **learning progress** rather than reconstructing cognitive history.

### When to use this pattern

- User says "学会使用 X 的数据处理方法" or "learn X pipeline"
- Project is new or the user is new to the domain
- No complex session history to reconstruct
- Stages reflect learning milestones, not research breakthroughs

### Steps

1. **Determine project type**: Is this a learning project or a research project?
   - Learning: stages = learning milestones (setup → pipeline → advanced)
   - Research: stages = direction changes (use the deep-audit procedure below)

2. **Initialize OS with forward-looking structure**:
   - `00_AI_BRIEFING.md`: State what the user wants to learn, current knowledge level, open questions
   - `02_CURRENT_QUESTION.md`: The specific skill/pipeline being learned this week
   - `03_TRUST_TABLE.md`: Tools and concepts the user has verified vs. not-yet-tried
   - `04_DECISION_LOG.md`: Key decisions about learning approach (e.g., environment setup choices)

3. **Use delegate_task for codebase audit**: Even for learning projects, the existing codebase contains transferable knowledge. Send a subagent to read all scripts and return structured summaries (purpose, functions, parameters, pitfalls per module). This takes ~5 min and provides the raw material for wiki pages.

4. **Create stages as learning milestones**: Each stage represents a level of mastery:
   - S01: Environment setup + first successful pipeline run
   - S02: Batch processing capability
   - S03: Understanding coordinate systems / response files / advanced topics
   - Stages are **forward-looking** (what to learn next), not backward-looking (what happened)

5. **Create insights as "things that work differently than expected"**: For learning projects, insights capture:
   - Tool quirks (e.g., a CLI returning a misleading exit code)
   - Environment conflicts (e.g., two toolchains whose libraries clash)
   - Domain-specific conventions (e.g., a coordinate-system or unit convention that differs from what you expected)
   - NOT research conclusions (there are none yet)

6. **TRUST_TABLE tracks tool reliability**: For learning projects, the trust table answers "which tools have I verified work?" rather than "which conclusions can I still believe?"
   - Trusted: tools the user has run successfully
   - Provisional: tools the user has read about but not run
   - Questioned: tools where the user hit failures or unknowns

7. **Co-build wiki simultaneously**: Learning projects benefit from a parallel wiki that captures transferable knowledge (tool parameters, pipeline flows, comparison tables). The wiki is the "textbook"; the cognition OS is the "learning journal".

### Key difference from research-project OS

| Dimension | Research project | Learning project |
|---|---|---|
| Stages | Direction changes, breakthroughs | Learning milestones, skill levels |
| Insights | Scientific conclusions | Tool/convention discoveries |
| Trust Table | Which conclusions are reliable | Which tools are verified working |
| Experiments | Hypothesis tests | "Did this tool work?" trials |
| Bug impacts | Contamination audits | Setup/configuration failures |
| Build procedure | Deep audit of session history | Forward-looking initialization |

### Verified example

A "learn tool X" project (live OS at `~/program/fxt_data_reduction/research-cognition-os/`): goal was to learn a data-reduction pipeline. OS initialized with stages as learning milestones (environment → batch pipeline → source detection), insights capturing tool quirks and environment conflicts (not research conclusions), and a parallel wiki as the "textbook". Built in one session with a subagent codebase audit.

### Young research project pattern

When a research project has **few prior sessions** (< 3) but **already has a complete pipeline + products** (scripts, spectra, fits, plots), the deep-audit procedure is overkill. Instead:

1. **File tree scan** (not session extraction): `find <root> -type f -printf '%T+ %p\n' | sort` gives the timeline
2. **Read key docs first**: AGENTS.md, README.md, any fit reports — these contain the project narrative
3. **Read scripts + outputs**: Each script = one experiment; each output dir = one product. Map them 1:1
4. **Build stages from pipeline order**: For a pipeline project, stages = pipeline steps (extract → fit → simulate → validate), not direction changes
5. **Insights from data, not sessions**: Read fit reports, CSV summaries, and plots to extract quantitative conclusions
6. **External documents as insight sources**: Proposal PDFs, reviewer feedback, and internal notes are first-class insight generators — they reveal what the project needs to address
7. **Goal prompt as artifact**: If the user writes a detailed execution plan (e.g., a `/goal` prompt), save it under `artifacts/` and reference it from the active stage

**Key difference from deep-audit**: No session-search step needed. The project is young enough that all context is in the files, not in AI session logs.

**Worked examples**: see `references/young-research-project-os-build.md` (file-tree + proposal/reviewer reconstruction, ~20 files in one session) and the live OS at `~/program/M104_TwoPhaseGas/research-cognition-os/` (subagent codebase audit; insights include both positive and negative results).

### New direction within existing project pattern

When a project **already has a complete pipeline + products** (scripts, spectra, fits, plots) but the user identifies a **new scientific question** that reuses the existing infrastructure, the OS build differs from both the young-project and deep-audit patterns:

**Key characteristics**:
- Existing pipeline is mature (v16, v18, etc.) with established model components
- New question repurposes existing data products rather than requiring new data reduction
- The pivot is a *scientific* direction change, not a *technical* one
- Existing TRUST_TABLE items remain valid; new items are additive

**Build procedure** (lighter than deep audit, more targeted than young-project):

1. **Read existing project docs** (AGENTS.md, README.md) to understand current pipeline and model
2. **Identify reusable assets**: Which existing products (spectra, fits, maps) serve the new question? Which need modification?
3. **Define new regions/methods**: The new question likely requires different spatial or spectral decomposition (e.g., disk vs halo instead of radial bins)
4. **Build OS forward-looking**: Stages = new analysis phases, NOT reconstruction of existing work
5. **Inherit existing trust**: Existing pipeline trust items carry over; new items start at Provisional/Questioned
6. **TRUST_TABLE is additive**: Keep existing rows, add new rows for new assumptions and their dependencies
7. **DECISION_LOG records the pivot**: The direction change itself is a decision (why the new question, what it supersedes or extends)

**OS structure** (leaner than deep-audit):
- 1 active stage (forward-looking phases within it)
- 2-3 insights (foundational observation + key methodological assumption)
- 0-1 experiments (first experiment not yet run)
- 1-3 decisions (pivot rationale + method choices)

**Key difference from other patterns**:

| Dimension | Young project | New direction | Deep audit |
|---|---|---|---|
| Existing pipeline | New/learning | Mature, reusable | Mature, under audit |
| Stages | Pipeline steps | New analysis phases | Historical reconstruction |
| Trust items | Tool reliability | Inherited + new assumptions | All under review |
| Build time | 15-30 min | 20-30 min | 3-5 hours |
| Session search | Minimal | Check for related context | Exhaustive |

**Worked example**: live OS at `~/program/M31CGM/research-cognition-os/` — a mature pipeline reused for a new scientific question; the new stage is forward-looking and the trust table inherits existing pipeline trust while adding the new assumptions at Provisional/Questioned. See also `references/n132d-rgs-cognition-os-build.md` for a spectral-pipeline build where all insights come from data products (no proposal/reviewers).

### Data-only project pattern

Some projects have no separate `~/program/<Proj>/` code directory — all data, scripts, and products live under `~/Data/<Proj>/`. The cognition OS should still be created under the data directory: `~/Data/<Proj>/research-cognition-os/`.

**Key characteristics**:
- No code-data separation (no `data` symlink needed)
- Scripts may be scattered across per-dataset subdirectories or a `combined/` directory
- No AGENTS.md or README.md at project root — look for CLAUDE.md or fit report files instead
- XCM scripts and logs serve as the primary "experiment" records

**Build procedure** (same as young-project streamlined audit, but):
1. Use `execute_code` for bulk file discovery (XCM/log file listing, directory structure) — faster than subagents
2. Read the latest XCM scripts + their logs to extract fitting parameters and results
3. If a detailed audit document already exists (e.g., CODEX_AUDIT_PROMPT.md), symlink it into `artifacts/` rather than duplicating content
4. Stages = fitting iteration phases (convention fixes, image comparison, blocker discovery), not pipeline steps

**Worked example**: live OS at `~/Data/M31Center/research-cognition-os/` — a data-only project (no separate code dir) built from a pre-existing audit prompt + script-log scanning; the audit doc is symlinked into `artifacts/` and stages track analysis-iteration phases, not pipeline steps.

---

## Build Procedure: Right-Sizing the OS to Project Scale

Before starting a cognition OS build, **assess the project scale** to choose the right procedure:

| Scale | Key indicators | Build procedure |
|-------|---------------|-----------------|
| **Small-medium** | ≤30 key products, ≤5 sessions, clear file tree, AGENTS.md/README.md exist | Streamlined audit (below) |
| **Large** | 50+ summary files, months of multi-tool sessions, complex branching | Deep audit (8-phase, below) |
| **Learning** | New project, user learning a tool/pipeline | Learning-Project Initialization (above) |

### Streamlined Audit for Small-Medium Research Projects

When the project is research-grade but small enough to read directly:

1. **Read project docs first**: AGENTS.md, README.md, any GOAL.md or BUGREPORT — these contain the project narrative and conventions. Feed them directly into AI_BRIEFING + TRUST_TABLE.
2. **Scan file tree with timestamps**: `find <root> -type f -printf '%T+ %p\n' | sort -r | head -60` — identify chronological order and latest products.
3. **Read key outputs**: Fit results (.txt), summaries (.csv), simulation reports. Extract parameters, statistics, and conclusions directly.
4. **Search session history**: `session_search` for project-relevant keywords. If ≤3 sessions found, read summaries directly — no need for Codex/Claude JSONL extraction.
5. **Build all OS files in one pass**: You have enough context from steps 1-4 to write AI_BRIEFING, TRUST_TABLE, CURRENT_QUESTION, DECISION_LOG, DAG, stages, insights, experiments, and session record.
6. **Skip**: Subagent decomposition, multi-tool session extraction (Codex/Claude/Gemini JSONL), 8-phase deep audit, 100+ file batch reading.

**Time budget**: 15-30 minutes for a small-medium project. The deep audit can take 3-5 hours.

**When to upgrade to deep audit**: If step 4 reveals ≥10 sessions across multiple AI tools, or if the file tree shows >50 summary/result files with unclear relationships, switch to the full deep audit procedure.

---

## Build Procedure: Extracting Cognitive History from File Trees (Large Projects)

When building a cognition OS for an existing research project (not a learning project), the first task is **reconstructing cognitive history**. This is the hardest part — the project already has months of work but no structured record.

### ⚠️ CRITICAL LESSON: Session records FIRST, file tree SECOND

The biggest mistake in three audits of DET_ML_Uncertainty was treating the file tree as the primary information source. File trees show *what was produced*, not *why* or *what was tried and abandoned*. Session records (Codex JSONL, Claude Code JSONL) contain the actual cognitive process: user feedback, rejected approaches, reasoning chains, and accidental discoveries.

**Correct priority order**:

1. **Session record extraction** — Codex/Claude/Gemini JSONL → extract `final_answer` + `user_message` timeline. Tools: `codex_search.py`, `claude_search.py`, `gemini_search.py`
2. **Identify cognitive turning points** — direction changes, bug discoveries, rejected approaches
3. **Cross-reference with file tree** — verify session claims against actual files
4. **Read key docs and code** — fill gaps, verify PSF dependencies
5. **Write OS files** — stages/insights/experiments from session narrative, not file timestamps

**Real example**: DR14 effective mask calibration (scut≈0.74, ecut≈14px) and SAS ecut semantics (ecut=0.68 = PSF enclosed fraction) were only in Claude Code session records. No results/ summary or wiki file contained them. Three file-tree-based audits completely missed these.

### Step-by-step (revised)

1. **Extract session records across ALL AI tools**: Search Codex, Claude Code, and Hermes sessions for the project. Use the session-search skills:
   - `codex-session-search` → `scripts/codex_search.py` — searches `~/.codex/sessions/` JSONL rollouts
   - `claude-session-search` → `scripts/claude_search.py` — searches `~/.claude/projects/<project>/` JSONL sessions
   - `gemini-session-search` — searches `~/.gemini/tmp/<project>/chats/` JSONL
   - Hermes: use `session_search` tool (built-in)
   - Also check `~/.codex/state_5.sqlite` threads table for CWD matching (find sessions by project directory)
   - Extract all `final_answer` + `user_message` entries. Build a chronological timeline of conclusions and direction changes.
2. **Identify turning points**: Mark every moment where "we realized our previous understanding was wrong" or "user said they weren't satisfied and direction changed". These define stage boundaries.
3. **Cross-reference file tree**: `find <project-root> -type f -printf '%T+ %p\n' | sort` — verify that files mentioned in sessions actually exist, and find files not mentioned in sessions.
4. **Read key docs first**: GOAL.md, AGENTS.md, any BUGREPORT*.md, theory/*.md — these contain the project narrative.
5. **Read code entry points**: config.py, lib/*.py, scripts/*.py (by timestamp order) — verify PSF dependencies.
6. **Build stages from session turning points**: Each direction change → one `stages/Sxx_*.md`. The narrative comes from sessions + docs + code triangulation.
7. **Extract insights from sessions + code**: Key formulas, empirical findings, bug discoveries → `insights/Ixxx_*.md`. Check each insight's dependency chain.
8. **Build TRUST_TABLE first**: Before writing anything else substantial, enumerate all conclusions and classify them.
9. **Use execute_code for bulk reading**: For 100+ summary files, use Python loops with read_file (not delegate_task — subagents timeout at 600s).
10. **Triangulate sessions × files × code**: No single source tells the full story.

### Key principle

> Session records ARE the cognitive history — they capture reasoning, rejections, and turning points. The file tree is the product catalog. Your job is to extract the narrative from sessions first, then cross-reference with files.

### ⚠️ When filename scanning is not enough

For established projects with 50+ summary files in `results/`, the basic timeline approach will miss experiments AND the cognitive reasoning behind them. Use the **deep audit methodology** instead (see `references/deep-audit-methodology.md`):

1. **Extract session records FIRST** — Codex/Claude JSONL → chronological timeline of conclusions, rejections, and direction changes
2. Read every `_summary.md` file completely (use execute_code + read_file loops, 10-15 per batch)
3. Audit key scripts for PSF dependency verification
4. Reconstruct theory derivation chains
5. Cross-validate: sessions × wiki log × theory × results × code

**Real lesson**: Two audits of DET_ML_Uncertainty failed because they only scanned filenames. A third audit plan now uses 8 phases and 5 parallel subagents to achieve 100% summary coverage.

## Obsidian Canvas Generation

The Mermaid DAG in `05_PROJECT_DAG.md` is for Git/AI readability. The `.canvas` file is for **interactive visual exploration** in Obsidian.

### Canvas format

Obsidian Canvas is a JSON file with `nodes` and `edges` arrays:

```json
{
  "nodes": [
    {"id": "0", "type": "text", "x": 0, "y": 0, "width": 300, "height": 80, "color": "4", "text": "Q1: Question"},
    {"id": "1", "type": "file", "x": 0, "y": 200, "width": 300, "height": 60, "color": "4", "file": "stages/S01_toy_world.md"}
  ],
  "edges": [
    {"id": "e0", "fromNode": "0", "toNode": "1", "color": "4"}
  ]
}
```

### Color codes (Obsidian Canvas)

| Color number | Meaning | Matches Mermaid |
|-------------|---------|-----------------|
| 1 | Default | — |
| 2 | Gray / Deprecated | `fill:#e5e5e5` |
| 3 | Yellow / Provisional | `fill:#fff3bf` |
| 4 | Green / Trusted | `fill:#d8f5d0` |
| 5 | Red / Questioned | `fill:#ffd6d6` |
| 6 | Blue / Current | `fill:#d6e8ff` |

### Layout strategy

- **Row 1 (y=-400)**: Questions (Q nodes)
- **Row 2 (y=-200)**: Hypotheses/Derivations (H/D nodes)
- **Row 3 (y=0)**: Experiments (E nodes)
- **Row 4 (y=200)**: Insights (I nodes)
- **Row 5 (y=400)**: Bugs/Blockers (B nodes)
- **Row 6 (y=600)**: File links (type="file" nodes pointing to stage .md files)
- **X spacing**: 600px between columns, left-to-right follows cognitive flow
- Contamination edges use dashed style in Mermaid, red color in Canvas

### Generation script pattern

```python
import json
canvas = {"nodes": [], "edges": []}
nid = [0]
def add_node(text, x, y, w=300, h=80, color="4", file=None):
    n = {"id": str(nid[0]), "x": x, "y": y, "width": w, "height": h, "color": color}
    n["type"] = "file" if file else "text"
    if file: n["file"] = file
    else: n["text"] = text
    canvas["nodes"].append(n)
    nid[0] += 1; return n["id"]
# ... build nodes and edges, then json.dump(canvas, f, indent=2)
```

## Obsidian 双链规范 (Mandatory)

The cognition OS is designed for Obsidian. All files MUST use `[[wikilinks]]` and YAML frontmatter to leverage Obsidian's graph view, backlink panel, and Dataview queries.

### YAML Frontmatter (every .md file)

```yaml
---
type: stage | insight | experiment | bug | session | meta
status: active | archived | deprecated | active-audit | in-progress
confidence: high | medium | low   # optional, not for meta/session
created: YYYY-MM-DD               # auto-extracted from content
tags: [cog/<type>, trust/<level>, psf-dependent]
---
```

### Tag Taxonomy

| Tag | Meaning | Usage |
|-----|---------|-------|
| `#cog/stage` | Research stage | All stages/Sxx files |
| `#cog/insight` | Knowledge claim | All insights/Ixxx files |
| `#cog/experiment` | Experiment record | All experiments/Exxx files |
| `#cog/bug` | Bug impact audit | All bug_impacts/Bxxx files |
| `#cog/session` | Daily session log | All sessions/ files |
| `#cog/meta` | Core OS file | 00-05 numbered files, SCHEMA, log |
| `#trust/high` | Trusted | Confidence = High |
| `#trust/medium` | Provisional | Confidence = Medium/Medium-High |
| `#trust/low` | Questioned | Confidence = Low |
| `#<dep>-dependent` | Depends on a known-risky component | Optional project-specific tag for items contaminated by a specific bug/tool (e.g. a particular pipeline module). Define per project |

### Wikilink Rules

1. **All cross-references use `[[NoteName]]`** — never plain paths like `stages/S01_xxx.md`
2. **Every file must have ≥2 outbound wikilinks** (except AUDIT_LOG, AUDIT_PLAN, SCHEMA)
3. **Use `## Related` section** at end of each file for semantic links with relation type:
   - `[[S04_projection_formula]] — discovered-in`
   - `[[E010_ml10_forward_calibration]] — produces`
   - `[[B001_analytic-ellbeta-psf-bugs]] — contaminated-by`
4. **Relation types**: `part-of`, `produces`, `supports`, `evidence-from`, `discovered-in`, `contaminated-by`, `questions`, `triggers-rollback`, `extends`, `uses`, `feeds-into`, `anchors`, `preceded-by`
5. **Experiment files are flat**: `experiments/E010_xxx.md` (NOT `experiments/E010_xxx/summary.md`). Manifest files: `experiments/E010_xxx_manifest.yaml`

### Dataview Queries (for Obsidian)

```dataview
TABLE status, confidence, tags
FROM "research-cognition-os"
WHERE type = "insight"
SORT confidence ASC
```

```dataview
TABLE status
FROM "research-cognition-os"
WHERE contains(tags, "psf-dependent")
```

### Graph View

With frontmatter + wikilinks + tags, Obsidian graph view will:
- Color-code by trust level (via Tags plugin or CSS snippets)
- Show cognitive flow: stages → insights → experiments
- Highlight contamination chains: bugs → experiments → insights
- Filter by `#cog/insight` or `#trust/low` to focus attention

## Integration with Subagent Orchestrator (Rolling Deployment)

When using `delegate_task` subagents with cognition OS, follow the rolling deployment pattern:

1. **Deploy up to 3 subagents in parallel** with clear, independent goals
2. **When one completes → audit immediately** → update cognition OS → deploy replacement
3. **Audit checklist per completed subagent**:
 - Extract quantitative results (CSV, figures)
 - Cross-validate with existing trust table entries
 - Write new insights (Ixxx) for non-obvious findings
 - Write experiment manifests (Exxx) for what was done
 - Update TRUST_TABLE with new findings or status changes
 - Update AI_BRIEFING if trusted/questioned lists changed
 - Update current stage (Sxx) with new results
4. **Don't wait for all 3 to finish** — alternate between "deploy new" and "audit completed"
5. **Record each subagent's performance** — did it hit iteration limit? Diagnose problem but not fix? Produce wrong results?

**Common subagent failure modes in research**:
- **Hit iteration limit (100 API calls)**: Common for tasks requiring reading 2000+ line scripts or complex environment setup. Mitigation: pre-process long scripts into summaries before delegating.
- **Diagnoses but doesn't fix**: Subagent identifies root cause correctly but runs out of iterations before implementing fix. Mitigation: treat diagnosis and fix as separate subagent tasks.
- **Framework built but not executed**: Subagent creates code structure but doesn't run it. Mitigation: explicitly require "run the script and show results" in the task context.

**Cognition OS update priority after each subagent**:
1. Trust table (most critical — what can we still believe?)
2. Insights (non-obvious discoveries that prevent future mistakes)
3. Stage file (current results and open questions)
4. AI Briefing (keeps future sessions aligned)
5. Experiment manifests (what was tried)

## External AI Audit Prompt Generation Pattern

The cognition OS serves not only as internal state management but also as a **structured context source for external AI audits**. When the project reaches a critical midpoint, you can synthesize an audit prompt by reading the OS files in sequence:

### When to use

- Project has completed a major phase (e.g., batch fitting running, results partially available)
- User wants an independent review before committing to the next phase
- User explicitly asks for a Codex/external AI audit

### Procedure

1. **Read OS files in sequence**: AI_BRIEFING → TRUST_TABLE → DECISION_LOG → active stage → CURRENT_QUESTION
2. **Read latest experimental data**: batch fitting log tail, CSV results, anomaly notes
3. **Synthesize audit prompt with 5 question categories**:
   - **Scientific logic** — assumptions, alternative explanations, logical gaps
   - **Methodology** — fitting strategy, optimizer, statistic choice, error propagation
   - **Data quality** — outliers, detection thresholds, systematic biases
   - **Statistical approach** — multiple testing, upper limit handling, sample size
   - **Physical interpretation** — degenerate explanations, confounders
4. **Save to `artifacts/codex_audit_prompt_YYYY-MM-DD.md`** — preserves the snapshot of project state at audit time
5. **Include 15-20 specific numbered questions** — makes it easy for the auditor to address each one

### Key structural elements of the prompt

- **Goal section**: 1-paragraph summary of what the project is trying to prove
- **Model structure**: Full model definition with frozen/free parameters clearly marked
- **Current results table**: Quantitative summary with detection rates, anomalies flagged
- **Critical questions**: Numbered, categorized, with enough context for an independent reviewer
- **Instructions**: What files to read, what to produce (structured report with traffic-light assessment)

### Difference from "audit prompt as input" pattern

| Direction | Pattern | Example |
|-----------|---------|---------|
| **OS → audit prompt** (output) | Synthesize OS state into external review document | M31CGM Codex audit (this session) |
| **Audit prompt → OS** (input) | Consume existing audit document to build OS | a pre-existing `CODEX_AUDIT_PROMPT.md` becomes the OS seed |

Both patterns are valid. The OS is bidirectional — it can both consume and produce audit artifacts.

**Worked example**: see `references/m31cgm-external-audit-pattern.md` — reading the OS (AI_BRIEFING + TRUST_TABLE + DECISION_LOG + active stage) and synthesizing it into a ~20-question, 5-category audit prompt saved under `artifacts/`, including model structure, current statistics, and flagged anomalies.

## Integration with llm-wiki

The cognition OS IS a wiki — it follows the same `SCHEMA.md + index.md + log.md` pattern as `llm-wiki`. When building a cognition OS:

1. Create `SCHEMA.md` with domain-specific tag taxonomy and trust classification rules
2. Create `index.md` listing all pages with trust status
3. Create `log.md` for action tracking
4. Use `[[wikilinks]]` between stages, insights, experiments, and bug_impacts for bidirectional navigation
5. The cognition OS should live at `<project-root>/research-cognition-os/`, NOT in `~/wiki/` (domain separation)

See also: [[llm-wiki]] for the full wiki maintenance workflow.

## References

| File | Content |
|------|---------|
| `references/os-maintenance-lessons.md` | **Project-agnostic** OS-maintenance lessons: internal-consistency check, drift audit, routine sync vs deep audit, ID-numbering conflicts, atomic propagation, supersede-don't-overwrite, negative-result insights, session-records-first, subagent cross-validation, don't-poll-long-tasks. Start here for general OS hygiene |
| `references/context-requalification-pattern.md` | Re-qualifying an old insight whose conclusion is still correct in its original scope but whose context evolved — without overwriting it (companion to supersede-don't-overwrite) |
| `references/supersede-dont-overwrite-pattern.md` | How to mark a superseded insight/decision, link forward to its replacement, and downgrade the trust row — research history as a DAG, not a mutable array |
| `references/session-linter-and-drift-detection.md` | Using `scripts/session_linter.py` and the drift-detection scripts: session frontmatter/format linting and cross-deployment OS-drift scanning |
| `references/orchestrator-deployment.md` | Orchestrator + subagent deployment protocol: task planning, context packaging, deployment, cross-validation, and the cognition-OS update workflow |
| `references/tes-os-drift-audit-example.md` | Worked example of a routine OS drift audit + sync (TES 星上算法, 2026-06-05) — concrete application of the drift/sync procedure |
| `references/_archived-leaked-project-pitfalls.md` | **Read-only holding pen.** Project-specific pitfalls that leaked into SKILL.md and were moved out of context. Do not extend; do not copy from. See "Scope & contribution rules" and "Draining the holding pen" for the migration procedure |
| `references/m82-squade-cognition-os-build.md` | M82 SQUDE cognition OS build: streamlined audit worked example for a small-medium research project (16 files, ~20 min). Shows right-sizing, template adjustments, and what file-tree-only reconstruction misses |
| `references/n132d-rgs-cognition-os-build.md` | N132D RGS cognition OS build: spectral-analysis pipeline pattern (no proposal/reviewers, insights from data products only, forward-looking current stage). 26 files in ~15 min |
| `references/xray-imaging-extended-structure-pattern.md` | Imaging-based project OS pattern (domain-specific): az-median+4fold method, stage/insight structure, trust table items, NGC 3079 worked example |
| `references/xray-temperature-mapping-pattern.md` | Domain-specific (X-ray): multi-method 2D temperature mapping — spectral fit / 5-band MLE / color-color / HR hierarchy, cross-validation protocol, M104 example. Not a general OS rule |
| `references/proposal-upgrade-workflow-pattern.md` | Domain-specific (X-ray): 7-phase observation-proposal upgrade workflow for reviewer responses (SQUDE/XRISM/Chandra AO), language rules, M82 example. Not a general OS rule |
| `references/young-research-project-os-build.md` | Young research project OS build pattern: file-tree reconstruction when sessions are sparse, proposal+reviewer as insight sources, goal-prompt artifact pattern, M82 SQUDE worked example |
| `references/dag-design-principles.md` | Three DAG views, node/edge types, trust-state colors, acyclicity rule, attention investment formula, five diagnostic questions, tool progression |
| `references/file-timestamp-extraction.md` | How to reconstruct cognitive history from file trees: timeline extraction, date clustering, pivot detection, delegate_task pattern |
| `references/deep-audit-methodology.md` | Full-content audit methodology for existing projects: 8-phase deep audit, subagent decomposition, PSF dependency classification, cross-validation checklist. Required when filename-only scans miss experiments |
| `references/det-ml-uncertainty-cognitive-history.md` | Complete cognitive history of DET_ML_Uncertainty project, reconstructed from full-content audit of 105 summary files, 32 theory files, 8 wiki phase logs, Codex research log, and BUGREPORT. Serves as worked example of deep cognition OS reconstruction |
| `references/xartatoms-cognition-os-build.md` | XARTATOMS (M104 Sombrero) cognition OS build: session search across Codex+Claude+Hermes, VERSION_CHANGELOG as primary source, SZ/X-ray tension as core question. Pattern: different AI tools carry different research weight per project |
| `references/m31cgm-external-audit-pattern.md` | External AI audit prompt generation: using cognition OS as structured context source for Codex/external review. Bidirectional pattern (OS→audit vs audit→OS). M31CGM worked example with 20-question 5-category template |
| `references/m104-cgm-2d-kt-map-orchestrator-session.md` | M104 CGM 2D kT map orchestrator session (2026-05-19): 7 subagents, 5-band MLE vs spectral fitting, HR→kT unreliability, background cross-validation, Chandra 8-sector HR, stale process management |
| `references/m104-high-snr-bin-kt-mapping-workflow.md` | M104 high-SNR bin kT mapping workflow (2026-05-31): 16-bin pie extraction with SAS evselect, BACKSCAL manual calculation, Wstat+group_counts Sherpa fitting, bulge contamination diagnosis, reliability classification, three-version kT map generation |
| `references/negative-result-insight-pattern.md` | How to record dead-end theoretical approaches as first-class insights: "can't work" vs "didn't work" distinction, confidence=High for mathematical proofs of impossibility, AI_BRIEFING inclusion pattern |
| `references/semi-analytical-model-discovery-pattern.md` | After ruling out dead ends, how to find the right physical variable and build the simplest parametric model: boundary conditions, cross-validation, variance decomposition. DET_ML k=1/sqrt(1+alpha*r^2) as worked example |
| `references/session6-methodological-lessons.md` | 6 lessons from winginess model validation: σ_PSF definition sign-flip, existing-data-first strategy, cross-session impact protocol, PSF template pre-computation 50x speedup, bug severity by core-conclusion impact, equivalent reparameterization identification |
| `references/session-formalization-pitfalls.md` | Session 记录形式化 Pitfalls: linter 使用指南、大小写陷阱、frontmatter 重建 bug、审计发现汇总 |
| `references/self-consistency-validation-method.md` | Concrete ANOVA + bootstrap + error-budget method for testing whether a model is self-consistent on its own pipeline. Includes U-shaped off-axis dependence diagnosis from DET_ML E010b |
| `references/first-principles-derivation-pattern.md` | EVT decomposition pattern for empirical constants: map to generic random field class → numerical "bare" coefficient → landscape correction factor → decomposition verification. α=0.325 = c·c'/W_ref as worked example |
| `references/self-consistency-vs-external-consistency.md` | Two-question validation framework: self-consistency (PRIMARY, does theory match our pipeline?) before external consistency (SECONDARY, does our pipeline match reference?). Error budget decomposition. Paper writing pattern. For the concrete quantitative method (ANOVA, bootstrap, error budget table), see self-consistency-validation-method.md |
| `references/verification-audit-methodology.md` | Systematic re-verification of TRUST_TABLE High-confidence claims: subagent grouping, bootstrap protocol (rel err < 20%), R² definition pitfall, stale data detection, OS propagation checklist. Includes DET_ML_Uncertainty worked example (15 claims, 4 issues: κ R² misleading, α ratio confusion, 8/4 text error, invalid CSV) |
| `references/orchestrator-subagent-research-workflow.md` | Orchestrator + subagent pattern for research: architecture, subagent capabilities, context parameter best practices, cross-validation protocol, child_timeout tuning, f² inflation error case study |
| `references/catalog-only-ml-prediction-pattern.md` | "Shortcut path" evaluation: when theory needs full simulation data but user only has catalog params, quantify accuracy at each correction level. Includes ablation study method, kappa calibration constant check, r(OFFAXIS) vs W(OFFAXIS) insight from DET_ML |
| `references/variance-conditioning-trap.md` | Var(X | conditioned_on_what) determines physical meaning. ML binning is selection bias, not physics. For inference/catalog applications prefer observable-conditioned residual moments such as `(S_hat,b,psf)`; `S_true` is only a simulation bookkeeping label unless explicitly discussing repeated-generation variance. |
| `references/cron-pipeline-os-integration.md` | Cron pipeline → cognition OS integration: which OS artifacts each cron job type must write, insight naming conventions, confidence defaults, Fund Strategy C1-C7 worked example, setup requirements (skills list, file toolset), pitfalls (session append, ID collision, routine-vs-anomaly threshold) |
| `references/fund-strategy-cognition-os-build.md` | Fund Strategy cognition OS build: non-X-ray quantitative research project, 31→46 files, bug-invalidated branch pattern (S03/S04 deprecated by B001), agy-review as OS validation, strategy reclassification insights, cross-cutting bug tracking |
| `references/routine-os-sync-pattern.md` | Routine OS sync with latest AI tool sessions: lighter procedure than deep audit (15-30 min), diff-based gap filling, Claude Code --project flag workaround with leading-dash names, TES 星上算法 worked example |
| `references/large-project-streamlined-bootstrap.md` | OS bootstrap for Large existing projects (~1 hour): when user asks "建立 cognition OS" for a 50+ product project, not full deep audit. ScienceAgent_cstat_v2 worked example (1493 rounds, 387 theories, 469 experiments, 8→22 files in one session). Covers ssh-based remote OS, subagent parallel file creation, template-collision pitfall, deep supplement phase (insight extraction, stage backfill, cross-doc propagation), heredoc+backtick collision, subagent directory drift, remote Python quoting. |
| `references/cross-project-os-health-audit.md` | Cross-project OS health audit methodology: 6-minute fleet scan, health scoring matrix, remediation priorities, zero-OS project discovery, automation opportunities. 14-project empirical baseline from 2026-06-18 audit |
| `references/methodology-trust-negativity.md` | Empirical finding: methodology trust items are severely neglected across OS deployments (8/14 projects <5% coverage). Root cause analysis, fix patterns, automation check, and session-record evidence |
| `references/backtest-engine-silent-bugs.md` | Backtest engine silent bugs: 6 bugs found by agy-review in Fund Strategy project (datetime.date silent fallback, look-ahead bias, hardcoded hold_days, T+0 settlement, IC sign flip, survivorship bias). Prevention checklist. Applicable to any quantitative backtest engine |
| `references/holding-pen-drain-procedure.md` | Full 3-round procedure for draining the `_archived-leaked-project-pitfalls.md` holding pen into project OS directories. Includes categorization rules for references, the "never done in one round" pitfall, and verification commands |
| `references/skill-repo-sync-pattern.md` | Skill-to-repo sync pattern: keeping the GitHub mirror in sync with the Hermes skill (upstream). Drift detection, common pollution patterns, update procedure. 2026-06-22 worked example |
| `references/i044-catalog-bridge-session.md` | I044 PSF-template catalog bridge session detail: convention bridge verification, MASKFRAC filtering, position-dependent PSF assignment, corrupted PSF diagnosis pattern, beyond-Fisher correction, catalog pilot results. **v2 update (2026-05-17)**: scut=0.9 effect negligible (dZ=-0.020), azimuth PSF mismatch is dominant blocker (1.46σ at same off-axis), 1000 reps needed for per-position low-S SE, S<5 degenerate outliers from near-zero var_3p, 31×31 template truncation 11% at 14'. DET_ML_Uncertainty project 2026-05-16/17 |

## Cron Pipeline → Cognition OS Integration

When a project runs automated cron jobs as a pipeline (data refresh → feedback → detection → recommendation → reflection → discovery → optimization), each job must write its results to the cognition OS. Without this, the OS drifts from project reality (see OS drift audit pitfall).

**Core rule**: Every cron job prompt must include a "Cognition OS 更新（强制）" section specifying which OS artifacts to write after the job runs. The artifacts vary by job type:

| Job type | Mandatory OS writes | Conditional OS writes |
|----------|-------------------|----------------------|
| Data refresh | session + AI_BRIEFING date | Insight (anomaly only) |
| Feedback collector | session + AI_BRIEFING | Insight (credit change) + TRUST_TABLE upgrade/downgrade |
| State detector | session + AI_BRIEFING | Insight (state switch) + TRUST_TABLE + CURRENT_QUESTION |
| Recommendation | session + AI_BRIEFING | Insight (composition shift) |
| Weekly reflection | session + **mandatory insight** + TRUST_TABLE + AI_BRIEFING | CURRENT_QUESTION |
| Discovery | session + TRUST_TABLE + AI_BRIEFING | Insight (new/negative) + CURRENT_QUESTION |
| Optimization | session + TRUST_TABLE + DECISION_LOG + AI_BRIEFING | Insight (param change) |

**Setup requirements for cron jobs that write OS**:
1. Add `research-cognition-os` to `skills` list
2. Include `file` in `enabled_toolsets` (terminal-only cannot write .md)
3. Specify OS path explicitly in prompt
4. Check `ls insights/ | sort -t_ -k1 -n | tail -3` before creating any insight to avoid ID collision

**Confidence defaults**: New strategy = Low (upgrade after 2w feedback), Negative result = High, Param change = Low (upgrade after OOS), Regime switch = Medium, Weekly reflection = Medium.

See `references/cron-pipeline-os-integration.md` for full pattern, naming conventions, Fund Strategy C1-C7 worked example, and pitfalls (session append not overwrite, don't create insights for routine ops, weekly reflection insight is non-optional).

## Cross-Project OS Health Audit (Multi-OS Fleet Management)

当你有 10+ 个 cognition OS 部署在多个项目上时，**单项目 drift audit 不够**。需要定期做**跨项目健康审计**，发现系统性退化模式。

### 触发条件

- 用户说"检查所有 OS 项目的健康状况"
- 超过 3 个月未做跨项目审计
- 新代码项目增长到 5+ Python 文件但无 OS
- 发现一个项目 OS 严重 drift（>7 天）→ 触发全舰队检查

### 审计步骤 (15 分钟)

1. **发现所有 OS 部署**:
   ```bash
   find ~/program ~/Data -maxdepth 4 -type d -name 'research-cognition-os' 2>/dev/null
   ```

2. **统计每个 OS 的文件组成**:
   ```bash
   for d in <all_os_dirs>; do
     name=$(basename $(dirname "$d"))
     files=$(find "$d" -name '*.md' -o -name '*.yaml' | wc -l)
     stages=$(find "$d/stages" -name '*.md' 2>/dev/null | wc -l)
     insights=$(find "$d/insights" -name '*.md' 2>/dev/null | wc -l)
     experiments=$(find "$d/experiments" -name '*.md' -o -name '*.yaml' 2>/dev/null | wc -l)
     bugs=$(find "$d/bug_impacts" -name '*.md' 2>/dev/null | wc -l)
     sessions=$(find "$d/sessions" -name '*.md' 2>/dev/null | wc -l)
     last_session=$(ls -t "$d/sessions/" 2>/dev/null | head -1)
     briefing_date=$(head -5 "$d/00_AI_BRIEFING.md" 2>/dev/null | grep -oP 'Last updated: \K.*' || echo "N/A")
     echo "$name | files=$files stages=$stages insights=$insights exp=$experiments bugs=$bugs sessions=$sessions | last_session=$last_session | briefing=$briefing_date"
   done
   ```

3. **量化 OS drift**（代码 vs session 时间差）:
   ```bash
   last_sess=$(ls -t "$d/sessions/"* 2>/dev/null | head -1 | xargs -I{} stat -c '%Y' {} 2>/dev/null || echo "0")
   last_code=$(find "$proj" -name '*.py' -printf '%T@\n' 2>/dev/null | sort -rn | head -1 || echo "0")
   gap=$(( ($last_code - $last_sess) / 86400 ))
   ```

4. **评估方法论条目覆盖率**（TRUST_TABLE 中的 method/methodology/pipeline 行数）:
   ```bash
   tt=$(find "$d" -maxdepth 1 -name '03_TRUST_TABLE.md')
   method=$(grep -ci 'method\|methodology\|pipeline\|approach\|workflow' "$tt" 2>/dev/null)
   ```

5. **检查 DAG 多格式输出完整性**（Mermaid + Canvas + PNG 均需存在）

6. **发现零 OS 项目**（有大量 Python 文件但无 OS 的代码目录）:
   ```bash
   for d in ~/program/*/; do
     [ -d "$d/research-cognition-os" ] && continue
     pycount=$(find "$d" -maxdepth 2 -name '*.py' 2>/dev/null | wc -l)
     [ "$pycount" -gt 5 ] && echo "$name: ${pycount} Python files, no OS"
   done
   ```

### 审计结果解读

| 指标 | 健康 | 警告 | 危险 |
|------|------|------|------|
| OS drift (代码 vs session) | < 3 天 | 3-14 天 | > 14 天 |
| Session 频率 | 每周 ≥ 1 | 每月 ≥ 1 | 无 session |
| TRUST_TABLE 方法论条目 | ≥ 总行数 20% | 5-20% | < 5% |
| DAG 多格式输出 | 3+ 格式 | 1 格式 | 无 |
| 零 OS 项目 | 0 | 1-3 | > 3 |

### 修复优先级

1. **严重 drift (>14d)**：先做 routine OS sync（15-30 min），不要全量 deep audit
2. **方法论条目缺失**：为每个主要 pipeline 步骤添加 TRUST_TABLE 行（如 `PSF-template generation | Methodology | Provisional`）
3. **零 OS 项目**：执行 15 分钟 streamlined audit 建立最小可用 OS
4. **DAG 缺失**：从现有 stages/insights 生成至少 Mermaid 版本

### 实证基准（2026-06-18 审计）

14 个部署 OS 的健康状况：
- **最佳**: 星上算法（13 sessions, 0d drift, 7/64 方法论条目）
- **最差**: DET_ML_Uncertainty（33d drift, 5 sessions, 3/92 方法论条目）
- **典型**: M31CGM（17d drift, 2 sessions, 3/18 方法论条目）
- **零 OS 警告**: 11 个项目（astro_evo_mvp 61py, cstat 86py, playground 87py 等）
- **DAG 完成度**: 仅 1/14 项目达成 5 格式输出

### ⚠️ 常见陷阱

- **方法论条目是系统性盲区** — 实证发现大多数项目 TRUST_TABLE 中 0-3 条方法论条目（占总量 <5%）。方法论（我们用什么 pipeline、什么优化器、什么统计量）是 OS 的核心资产但最容易被忽略。**规则**：每次跨项目审计必须检查方法论条目覆盖率，<10% 即标记为警告。
- **DAG 不完整是常态** — 14 个项目中仅 DET_ML 有完整 5 格式输出。Canvas 交互图几乎为零。**规则**：新 OS 初始化时至少生成 Mermaid + Canvas 两个格式，PDF/PNG/SVG 可选。
- **Session 记录形式化不足** — 大多数项目只有 1-2 个 session（初始化时），之后无更新。**规则**：session 频率 < 每周 1 次 = OS 已死亡。必须强制每日 Did/Found/Next 3 行记录。
- **零 OS 项目比 drift 更严重** — 有代码但无 OS = 认知状态完全丢失。**规则**：任何有 >5 个 Python 文件的科研项目必须在 1 周内建立最小 OS（AI_BRIEFING + TRUST_TABLE + CURRENT_QUESTION + session）。
- **不要对 drift 项目做全量 deep audit** — 严重 drift 时，先做 15 分钟 routine sync，不要启动 3-5 小时的 deep audit。Deep audit 只在首次 OS 构建或项目有重大方向变化时执行。

## 相关技能

- [[xray-wiki-maintenance]] — Wiki 维护流程
- [[rollback-logic-design]] — 回退逻辑设计 (4-level rollback)
- [[xray-project-scaffolding]] — 项目脚手架 (可集成 cognition OS 初始化)

---

## § 一键初始化流程 (cognition-os-init 已合并)

为新/现有研究项目创建 cognition OS 目录结构和核心文件。自动判断项目类型并选择对应构建流程。

### 触发条件

- 用户说"给这个项目建 cognition OS"或"初始化 OS"
- 新项目开始，需要认知状态管理
- 现有项目需要结构化知识管理

### 项目类型判断

| 类型 | 特征 | 构建流程 |
|------|------|---------|
| Learning | 新工具/管线学习 | Forward-looking init |
| Young | ≤5 sessions, 有完整 pipeline | Streamlined audit |
| Large | 50+ products, 多月多工具 | Deep audit (8-phase) |
| New direction | 成熟项目新问题 | Forward-looking + inherit trust |

### 初始化步骤

1. **创建目录结构**: `mkdir -p "$OS_DIR"/{stages,insights,experiments,bug_impacts,sessions,artifacts,figures,scripts,configs,dag}`
2. **判断项目类型**: 统计已有产物和 session 数量
3. **从模板创建核心文件**: 复制 00-05 模板 (AI_BRIEFING, CURRENT_QUESTION, TRUST_TABLE, DECISION_LOG, PROJECT_DAG)
4. **填充项目信息**: 根据类型自动填充 (Young: 读已有文件; Learning: 用户目标; Large: 只创建骨架标注"待审计")
5. **创建首日 session**: `cp session-template.md sessions/$DATE.md`
6. **YAML frontmatter + wikilinks**: 每个文件添加 type/status/created/tags

### 验证清单

- [ ] 目录结构完整 (stages/, insights/, experiments/, bug_impacts/, sessions/)
- [ ] 5 个核心文件存在 (00-05)
- [ ] AI_BRIEFING 有项目摘要
- [ ] TRUST_TABLE 至少有 1 行
- [ ] CURRENT_QUESTION 有主问题
- [ ] 首日 session 已创建
- [ ] 所有文件有 YAML frontmatter

### 初始化 Pitfalls

- **不要对大型项目做一键初始化** — 需要完整 deep audit
- **不要覆盖已有 OS** — 如果 `research-cognition-os/` 已存在，先检查
- **模板中的 methodology invariants 是项目特异的** — DET_ML 的规则不能复制到其他项目
- **⚠️ NEVER write_file OS content to the skill's own template directory** — When building an OS, always write to the target project path (`<project-root>/research-cognition-os/`), NEVER to `~/.hermes/skills/note-taking/research-cognition-os/templates/`. The template files are shared across all projects; overwriting them with project-specific content destroys the templates for future use. If you accidentally overwrite a template, restore it immediately from the skill's git history or by re-reading the original content from the skill_view output. Root cause: `write_file` with a path under `~/.hermes/skills/` silently overwrites skill files. Prevention: always verify the target path starts with the project root, not the skill directory.
- **⚠️ Large-project streamlined bootstrap workflow** — When a project is classified as Large (50+ products, multi-month, multi-tool) but the user asks to "建立 cognition OS" (not "deep audit"), the correct workflow is NOT full deep audit (8-phase, 3-5hr) NOR one-click init. It is a **streamlined bootstrap**: (1) Read existing project docs (GOAL.md, RESEARCH_CHARTER.md, PHENOMENA.md, CHANGELOG.md, latest round log) — 15-20 min; (2) Write core OS files (00_AI_BRIEFING, 02_CURRENT_QUESTION, 03_TRUST_TABLE, 04_DECISION_LOG, 05_PROJECT_DAG) with project-specific methodology invariants — 20-30 min; (3) Write current stage file + bug_impact file for any active blockers — 10 min; (4) Write first session record — 5 min; (5) Cross-doc consistency check — 5 min. Total: ~1 hour. This produces a **minimally viable OS** that can be maintained via routine sync. Deep audit is reserved for when the project has a major direction change or when the user explicitly requests it. Real example: ScienceAgent_cstat_v2 (1493 rounds, 387 theories, 469 experiments) — streamlined bootstrap produced 8 files (108KB) in one session.
- **⚠️ Subagent pattern for parallel OS file creation** — When creating 3+ OS files simultaneously, delegate to a subagent with full project context (project summary, key docs content, methodology invariants, ID numbering). The subagent writes files locally then scp's to the target. This avoids 15+ sequential ssh+write round-trips. Key: pass the AI_BRIEFING content as context so the subagent can derive TRUST_TABLE/CURRENT_QUESTION/DECISION_LOG/DAG consistently. Real example: 4 OS files created in one delegate_task call (~16 min) vs estimated 25+ min sequential.
- **⚠️ Cross-doc consistency verification recipe** — After creating all OS files, run this concrete check:
  ```bash
  cd <project-root>/research-cognition-os
  # Check that key IDs appear in all core files
  for f in *.md; do
    echo "== $f =="; grep -oE '(S0[0-9]|D0[0-9]|M0[0-9]|I0[0-9]|B00[0-9]|PHENOMENA-[0-9])' "$f" | sort -u
  done
  # Check YAML frontmatter exists in all .md files
  for f in *.md stages/*.md bug_impacts/*.md sessions/*.md; do
    head -1 "$f" | grep -q '^---' || echo "MISSING FRONTMATTER: $f"
  done
  ```
  This catches missing cross-references and missing frontmatter that would break Obsidian/wiki tooling.
- **⚠️ Heredoc + backtick collision via remote ssh** — When appending Mermaid or code-block content to OS files over ssh, `cat >> file << 'HEREDOC'` will still execute backtick-enclosed text as shell commands (e.g., `I001[...]` gets executed). **Fix**: write the content to a local temp file with `write_file`, then `scp` it to the remote and `cat /tmp/append.md >> target.md`. Never use heredoc for content containing backticks, square brackets, or Mermaid syntax.
- **⚠️ Subagent directory naming drift** — When delegating OS file creation to subagents, explicitly specify the target directory name (e.g., `bug_impacts/`, NOT `bugs/`). Subagents will invent plausible-but-wrong directory names if not given the exact path. After subagent completion, verify file placement with `find . -type f | sort` and move any misplaced files before doing cross-doc checks.
- **⚠️ Remote ssh Python validation — use `%` formatting, not f-strings** — Validating JSON files over ssh with Python one-liners fails when f-strings contain dict key access (`c["nodes"]`) because shell quoting and Python quoting collide across 3 layers (shell → ssh → python). Use `print("N nodes" % len(c["nodes"]))` instead. This applies to any remote Python one-liner that accesses dict keys.
