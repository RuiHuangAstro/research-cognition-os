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

## 一句话方法论

```text
Question → Attempt → Evidence → Trust Level → Decision → Artifact Index
```

## Methodology Invariants for Statistical Research

When a project studies conditional distributions or simulation/catalog statistics, promote these rules into `00_AI_BRIEFING.md`, `02_CURRENT_QUESTION.md`, `03_TRUST_TABLE.md`, and the relevant insight pages. Do not leave them buried in session logs or references.

1. **Condition on observables, not simulation truth** — the core conditioning variable is observable space, such as `(S_hat, b, psf)`. `S_true` is only a simulation label used to generate samples; it is not an inference conditioning variable unless the page explicitly discusses repeated-generation experiments.
2. **Analyze primary statistic residuals, not transformed-statistic cuts** — for DET_ML-like projects, do statistics in `DeltaC` residual space. `ML` is a nonlinear incomplete-gamma transform of `DeltaC` and is not expected to be Gaussian. For a phrase like "three-parameter ML~6-10", convert that ML interval to its corresponding `DeltaC` interval, then analyze in `DeltaC` or `S_hat` bins. Do not impose ML cuts when estimating intrinsic conditional distributions.
3. **Use residual moment accounting** — define `R_i = DeltaC_i - E_theory[DeltaC_i | S_hat_i, b_i, psf_i]`. Then `mean(DeltaC) = mean(R) + mean(E_theory[DeltaC])` and `Var(DeltaC) = Var(R + E_theory[DeltaC])`. Only in narrow bins where the theory expectation is nearly constant can `Var(DeltaC) ≈ Var(R)`.
4. **Make methodology claims first-class trust items** — add rows such as `Conditional-analysis methodology` to the trust table, so downstream agents see the rule before reading detailed insights.

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

### ⚠️ Mermaid 布局限制

Mermaid `flowchart LR`/`flowchart TB` 使用 Dagre 自动布局，**不保证 parent 在 child 上方/左方**。

常见问题：
- 箭头向下，但 child 节点出现在 parent 上方 → 箭头拐 180°
- `subgraph` 内 `direction LR` 与外层 `TB` 冲突，导致节点错位
- 多个 cross-layer 边导致布局"爆炸"（Phase 6-7 被推到右侧很远）

解决方案：
- **⚠️ OS internal consistency: DAG ≠ TRUST_TABLE ≠ AI_BRIEFING** — After any multi-file OS update, run a cross-document consistency check: (1) `grep -c 'I0[0-9][0-9]' 05_PROJECT_DAG.md 03_TRUST_TABLE.md 00_AI_BRIEFING.md` — all IDs should appear in all three; (2) `ls insights/ | sed 's/_.*//' | sort > /tmp/ids.txt && grep -oP 'I0[0-9]{2}' 05_PROJECT_DAG.md | sort -u > /tmp/dag_ids.txt && comm -23 /tmp/ids.txt /tmp/dag_ids.txt` to find insights missing from DAG. Real lesson: after syncing V53-V58 results, S13 and I016-I019 existed in TRUST_TABLE and AI_BRIEFING but were absent from PROJECT_DAG — the DAG was still at the V31 era. **Rule**: after any batch OS update, verify that every new I/E/B/S ID appears in ALL of: AI_BRIEFING, TRUST_TABLE, PROJECT_DAG, and the relevant stage file. Missing IDs = incomplete update.
- **⚠️ OS drift audit — 每次 session 开始必须检查 OS 是否滞后** — 代码/实验进展快于 OS 更新是常态。快速诊断方法：(1) `find <root> -name '*.py' -printf '%T+ %p\n' | sort -r | head -5` 取最新代码时间戳；(2) `ls -lt research-cognition-os/sessions/ | head -3` 取最新 session 时间戳；(3) 若代码比 session 新 >1 天 → OS 滞后。另一个信号：AI_BRIEFING 的 "Current focus" 提到的版本号低于代码目录中最新的 v* 脚本编号。滞后时不应急于全量更新，先在 CURRENT_QUESTION 标注 "OS needs sync from Vxx"，然后在关键突破点（new FWHM record, new insight, bug discovery）逐项补。真实教训：星上算法项目 V46 达到 4.42 eV 但 OS 停在 V31 时代，5 个 session、4 个 decision、4 个 experiment、6 个 stage 未记录
- **⚠️ Routine OS sync with latest AI tool sessions (not just initial build)** — The deep-audit procedure covers initial OS construction. But OS sync is also a **routine maintenance task**: when the user says "read the latest cognition OS and the latest Claude session, update the missing part", use this lighter procedure: (1) **Read current OS state**: AI_BRIEFING + TRUST_TABLE + active stage + latest session record; (2) **Extract latest AI session content**: Use `claude_search.py --list --project <name>` to find the newest session, then `--type final` for conclusions and `--type user --human` for direction changes. For Codex: `codex_search.py --list --cwd <path>` + `--type final`; (3) **Diff OS vs session**: Compare session conclusions vs existing insights/experiments. Items in session but NOT in OS = missing items to add; (4) **Add missing items with correct numbering**: `ls insights/ | sort -t_ -k1 -n | tail -3` first to avoid ID conflicts; (5) **Update all cross-references**: AI_BRIEFING, TRUST_TABLE, stages, DAG, session log. After any rename, `grep -r "old_ID" --include="*.md" .` to verify zero ghost references; (6) **Update session record**: Write today's Did/Found/Next in `sessions/YYYY-MM-DD.md`. **Key difference from deep audit**: No multi-tool exhaustive search, no subagent decomposition. Just: read OS → read latest session → diff → fill gaps. Time budget: 15-30 min. Real example: TES 星上算法 OS sync found I009 naming conflict (two files sharing one ID), missing I008, and 6+ stale cross-references — all fixed in one pass. See `references/routine-os-sync-pattern.md`
- **⚠️ Claude Code session `--project` flag parsing bug** — When using `claude_search.py --project <name>`, if the project name starts with a dash (e.g., `-home-huangrui-program-tes-onboard-processing`), the `argparse` parser may interpret it as a flag, causing an error or wrong results. **Workaround**: (1) Use `--list-projects` to find the exact encoded name, (2) if it starts with `-`, bypass the CLI and read the JSONL files directly: `ls ~/.claude/projects/<project-dir>/*.jsonl | sort -t/ -k6 | tail -1` to find the latest session, then `grep` or Python-parse it. This is an `argparse` limitation, not a Claude Code bug.
- **⚠️ Fitting parameter hitting bound = artifact, not result**
- **⚠️ Paper-freeze integration after negative results — 6-phase pattern** — When a negative result must be integrated into a publication package with a positive result, use this workflow: (1) Update publication skeleton — add negative result as separate appendix section, state "does not supersede" explicitly; (2) Create claim matrix — claims with ALLOWED/ALLOWED-WITH-CAVEAT/FORBIDDEN status, include negative-result claims; (3) Update figure/table plan — main text keeps positive-result figures, negative tables in appendix; (4) Post-integration stale-claim audit — re-run pattern search on ALL new content, add new patterns specific to the negative result; (5) Reproducibility manifest — include both positive and negative data files with MD5; (6) OS update — TRUST_TABLE, experiment artifact, BRIEFING, log, index, lint. Key rule: negative result goes in appendix/future-work, NOT main text. Re-audit after integration — new content can introduce new stale phrases. See `xmm-epic-deltac-residual-validation` Pitfall 43 for the DET_ML v16 worked example.
- **⚠️ Subagent-generated publication content must be re-audited** — When a subagent produces figure plans, captions, or tables for a publication package, the output can reintroduce stale claims that the same session's stale-claim audit just removed. Root cause: subagents use available CSV data without cross-checking against the claim matrix. Rule: after any subagent generates publication content, run a SECOND stale-claim audit on the NEW content before accepting it. Cross-check each figure caption and table entry against the claim matrix.
- **不要一开始就自动化 DAG** — 先手动画 20 个节点，再考虑 Graphviz 自动生成
- **⚠️ Mermaid subgraph 布局不可靠** — `flowchart TB` + `subgraph` + `direction LR` 组合下，Dagre 引擎不保证 parent 在 child 上方。箭头可能拐 180°。解决方案：(1) Mermaid 用 compact summary 节点（一个 phase 一个节点），(2) 同时生成 Graphviz PDF 保证精确布局
- **⚠️ Graphviz cluster 与 rank 冲突** — `cluster` 子图会让 Graphviz 自动排列节点位置，与 `rank=same` 约束冲突，导致节点被推到错误位置。解决方案：不用 cluster，用 `plaintext` 节点做 section label + invisible edge (`SEC0→SEC1→SEC2→SEC3`) 强制层序
- **⚠️ Cross-layer 边用 constraint=false** — 污染/回溯箭头（如 BUG→PH6 "contaminates"）如果不加 `constraint=false`，会干扰主布局的垂直排序
- **DAG 不能有回边** — 每次回滚生成新节点 (S04 → S04b)，保持 acyclic
- **不要完美主义** — AI_BRIEFING.md 先写 100 行，不要等"完整"
- **⚠️ OS internal consistency: DAG ≠ TRUST_TABLE ≠ AI_BRIEFING** — After any multi-file OS update, run a cross-document consistency check: (1) `grep -c 'I0[0-9][0-9]' 05_PROJECT_DAG.md 03_TRUST_TABLE.md 00_AI_BRIEFING.md` — all IDs should appear in all three; (2) `ls insights/ | sed 's/_.*//' | sort > /tmp/ids.txt && grep -oP 'I0[0-9]{2}' 05_PROJECT_DAG.md | sort -u > /tmp/dag_ids.txt && comm -23 /tmp/ids.txt /tmp/dag_ids.txt` to find insights missing from DAG. Real lesson: after syncing V53-V58 results, S13 and I016-I019 existed in TRUST_TABLE and AI_BRIEFING but were absent from PROJECT_DAG — the DAG was still at the V31 era. **Rule**: after any batch OS update, verify that every new I/E/B/S ID appears in ALL of: AI_BRIEFING, TRUST_TABLE, PROJECT_DAG, and the relevant stage file. Missing IDs = incomplete update.
### ⚠️ OS drift audit — 每次 session 开始必须检查 OS 是否滞后

代码/实验进展快于 OS 更新是常态。快速诊断方法：(1) `find <root> -name '*.py' -printf '%T+ %p\n' | sort -r | head -5` 取最新代码时间戳；(2) `ls -lt research-cognition-os/sessions/ | head -3` 取最新 session 时间戳；(3) 若代码比 session 新 >1 天 → OS 滞后。另一个信号：AI_BRIEFING 的 "Current focus" 提到的版本号低于代码目录中最新的 v* 脚本编号。滞后时不应急于全量更新，先在 CURRENT_QUESTION 标注 "OS needs sync from Vxx"，然后在关键突破点（new FWHM record, new insight, bug discovery）逐项补。真实教训：星上算法项目 V46 达到 4.42 eV 但 OS 停在 V31 时代，5 个 session、4 个 decision、4 个 experiment、6 个 stage 未记录

### ⚠️ Routine OS sync with latest AI tool sessions (not just initial build)

The deep-audit procedure covers initial OS construction. But OS sync is also a **routine maintenance task**: when the user says "read the latest cognition OS and the latest Claude session, update the missing part", use this lighter procedure:

1. **Read current OS state**: AI_BRIEFING + TRUST_TABLE + active stage + latest session record
2. **Extract latest AI session content**: Use `claude_search.py --list --project <name>` to find the newest session, then `--type final` for conclusions and `--type user --human` for direction changes. For Codex: `codex_search.py --list --cwd <path>` + `--type final`
3. **Diff OS vs session**: Compare session conclusions vs existing insights/experiments. Items in session but NOT in OS = missing items to add
4. **Add missing items with correct numbering**: `ls insights/ | sort -t_ -k1 -n | tail -3` first to avoid ID conflicts
5. **Update all cross-references**: AI_BRIEFING, TRUST_TABLE, stages, DAG, session log. After any rename, `grep -r "old_ID" --include="*.md" .` to verify zero ghost references
6. **Update session record**: Write today's Did/Found/Next in `sessions/YYYY-MM-DD.md`

**Key difference from deep audit**: No multi-tool exhaustive search, no subagent decomposition. Just: read OS → read latest session → diff → fill gaps. Time budget: 15-30 min. Real example: TES 星上算法 OS sync found I009 naming conflict (two files sharing one ID), missing I008, and 6+ stale cross-references — all fixed in one pass.

### ⚠️ Claude Code session `--project` flag parsing bug
- **⚠️ Fitting parameter hitting bound = artifact, not result** — 当拟合器的某个参数恰好等于其约束边界（如 sigma_lo=0.002 keV → FWHM=4.71 eV = 2.3548 × 0.002），这是人为下限而非物理结果。诊断：FWHM/bound_constant 是否完全吻合（如 4.71/2.3548=2.000=bound in keV）。修复：放宽下界重测，真实值应在 bound 附近自由收敛。真实教训：V46 所有 "4.71 eV" 结果都是 M4 sigma 下界 0.002 keV 造成的 artifact，放宽到 0.0003 keV 后真实 FWHM=4.42 eV，chi2/dof 更好。**规则：任何恰好等于拟合 bound 的结果都要放宽 bound 重测**
- **⚠️ AI_BRIEFING template methodology invariants are project-specific** — The template's "Methodology invariants" section contains DET_ML-specific rules (S_hat conditioning, DeltaC residuals, ML truncation). For non-DET_ML projects, replace these with the project's own methodology rules. Examples: X-ray spectral fitting projects should list abundance conventions (Wilms/Verner) and statistic choices (chi2gehrels/C-stat); imaging projects should list PSF handling and background subtraction rules. Do NOT copy the DET_ML invariants into a project that doesn't need them — they clutter the briefing and confuse future sessions.
- **不要只记做了什么** — 记录"这个结论依赖什么""现在还能不能信"
- **Trust Table 是核心** — 每次 bug 先更新表，不要陷入"全盘推翻"情绪
- **Current Question 是防线** — 想开新分支时先问：这是不是 current question？不是就放进 Parking Lot
- **Don't mix domains** — `~/wiki/` is X-ray 专用；其他项目的 cognition OS 放在 `~/program/<project>/wiki/`
- **⚠️ Verify detection status in ALL galaxies before committing to symmetric pipelines** — When a dual-galaxy strategy assumes both targets have detectable emission (e.g., hot halos for τ_hot measurement), verify detection in BOTH before designing symmetric reduction. M31-τX assumed M33 could serve as "second M31" for quantitative τ_hot(v_esc) profiling, but literature (Tüllmann+2011) showed M33 has NO hot halo — only disk-confined diffuse emission 5-10× fainter. This forced strategy revision: M33 → low-v_esc qualitative anchor instead of quantitative cross-validation. The insight was captured as I002 BEFORE any data reduction, preventing wasted effort on a symmetric M33 halo pipeline. **Rule**: during methodology design, explicitly check each target's detection status for the specific emission component your measurement requires
- **⚠️ Fill-value discovery is a cognition-OS archetype** — When a pipeline produces unexplained extreme values across many versions (v4→v8), the root cause is often a data format convention (fill value, saturation flag, invalid-pixel marker) that was never documented. This follows the same pattern as "the biggest enemy in data is what you don't know about the format." Record these discoveries as high-confidence insights with the diagnostic path (how many versions failed, what was checked, what was missed). Example: M31 Hα mosaic v4-v8 all had ±1.7M extreme values; root cause was LGGS fill value = 50000 masked as `ha==0|cont==0` but never checked for `ha>=49000`. See `xray-profile-extraction` skill → Section 9 (M31 Optical Ancillary Data) for the full diagnostic.
- **⚠️ When project pivots, archive old OS and rebuild — don't patch** — When the research direction fundamentally changes (e.g., FXT imaging → HK2020 spectral reproduction), the old OS stages/insights/experiments become irrelevant noise. Patching creates a hybrid that confuses future sessions. Instead: (1) `mkdir archive_YYYYMMDD/` and move ALL old files there, (2) rebuild from scratch with new stage numbering (S01+), new insight numbering (continue from max existing + 1 to avoid ID conflicts), (3) keep archive for reference but mark as inactive. Real lesson: NGC3079 had 28 FXT-era OS files that were irrelevant to HK2020 reproduction; archiving + rebuilding with 21 new files took ~30 min but eliminated all context pollution. Key rule: new OS ID numbering must not conflict with archived IDs (start insights at I006 if archive goes to I005)
- **⚠️ 构建 OS 时必须做 results/ 内容分析** — 不能只做文件名扫描+时间线分析。results/ 中的 _summary.md 文件包含已完成的实验结论，必须读取并录入 OS。否则会遗漏已存在但未被文件名识别的重要结果（如 forward calibration、ecut truncation）
- **⚠️ Wiki 更新后必须同步 OS** — 当项目 wiki 被更新时（如 wiki/concepts/ 新增页面），cognition OS 的 stages/insights/experiments 必须同步更新。否则 OS 会与项目实际状态脱节
- **⚠️ 实验→wiki 传播后必须标记** — 当实验结果被传播到 wiki（如 E001 的发现写入了 6 个 wiki 页面），必须在实验 manifest 中记录 `propagated_to_wiki: true` 和具体更新的 wiki 页面列表。否则未来 session 会重复传播相同内容。方法：在 manifest.yaml 中添加 `wiki_updates: [fxt-chain-pipeline, fxt-response-files, ...]`
- **⚠️ 每次 session 开始时做 OS audit — 检查 wiki/ 和 results/ 是否有未录入 OS 的新内容。这应该是 session 启动流程的一部分。方法：`find results/ -name '*_summary.md' -newer research-cognition-os/log.md` 找出新增 summary
- **⚠️ 已知 bug 的结果文件必须标记 deprecated** — 当 results/ 中的 CSV/npz 文件由有 bug 的脚本生成时，不仅要在 DECISION_LOG 中记录 bug，还必须：(1) 在文件名旁加 `_DEPRECATED` 或创建 `.deprecated` 标记文件，(2) 在 TRUST_TABLE 中添加该文件的条目并标记为 Deprecated，(3) 在 AI_BRIEFING 的 Currently questioned 中列出。真实教训：`conditional_variance_ratio_k_ml.csv` 有两个已知 bug（gamma shape 参数错误 + 1p/3p 方差比较方式错误），所有 18 个 bin 数据严重偏离，但文件仍留在 results/ 中未标记，导致 subagent 验证时引用了无效数据。正确做法：bug 修复后立即废弃旧文件，新文件用新名字
- **⚠️ 结论验证审计 (verification audit) 工作流** — 对 TRUST_TABLE 中 High confidence 的定量结论，应定期用 subagent 并行验证：每个 subagent 负责一组相关结论，从原始数据/模拟重新计算，报告统计量 ± bootstrap 误差，检查相对误差 < 20%。方法详见 `references/verification-audit-methodology.md`
- **⚠️ R² 声称必须区分拟合对象** — 当项目声称某模型 R²=0.994 时，必须追问：R² 是对什么量的拟合？κ = 1.31·S^0.234·b^(-0.235) 的 R²=0.994 是 κ 对幂律的拟合优度，不是 q0 预测的 R²。实际 q0 预测 R²=0.845，MAPE=35%。**规则**：任何 R² 声称必须注明"R² of X fitted to Y"，不能只写"R²=0.994"。这在 TRUST_TABLE 中尤其重要——将 R²=0.994 写入 Notes 会误导后续使用者认为模型预测精度极高。真实教训：DET_ML T03 κ 因子因此从 High 降级为 Medium
- **⚠️ 废弃数据文件必须显式标记** — results/ 中的 CSV/npz 文件即使已知有 bug，如果没有在 OS 中标记为 Deprecated，后续审计仍会引用。`conditional_variance_ratio_k_ml.csv` 有两个已知 bug（gamma shape 1.5 vs 2.5 + 1p/3p 方差比较方式错误），所有 18 个 bin 的 k_observed 严重偏离 k_predicted，但因为未标记，三次审计都未发现。**规则**：发现 bug 后，必须在 TRUST_TABLE 新增条目标记对应输出文件为 Deprecated，并在 AI_BRIEFING 中注明。不能只在 DECISION_LOG 或代码注释中记录
- **⚠️ Todo 状态在 subagent 完成后可能过时** — 当 orchestrator session 通过 delegate_task 修复了一个 blocker（如 APEC env bug），subagent 返回成功结果，但 parent session 的 todo list 可能仍显示 `in_progress`。如果 session 在 subagent 返回后很快结束（或用户切换到另一个 session），todo 状态不会被更新，下游依赖项保持 `pending`。**规则**：subagent 完成后，在记录结果的同时必须显式更新 todo list（标记 completed、unblock 依赖项）。跨 session 检查时，不要只看 todo 状态——用 filesystem state 交叉验证（文件是否存在？产出是否已生成？）
- **⚠️ 定期验证审计：High-trust 结论必须独立交叉检验** — TRUST_TABLE 中标记 High 的定量结论随时间可能失效（代码 bug、定义漂移、数据文件损坏）。验证方法：用 subagent orchestrator 并行检验，每个结论要求 bootstrap 相对误差 < 20%。典型流程见 `references/verification-audit-methodology.md`。DET_ML 项目首次验证审计发现 4/15 项需修正（κ 因子 R² 误导、α 比例混淆、8/4 比例文字错误、1 个 CSV 文件无效）
- **⚠️ 定量方向描述必须用显式数值对** — 当讨论 gradient/direction/trend 时，"从A下降到B"这种自然语言描述容易产生歧义（"从A下降到B"可以是A>B或A<B取决于说话者的参照点）。**规则**：在 insight 和 TRUST_TABLE 中，gradient 方向必须写为 "inner kT = 0.6 keV, outer kT = 0.85 keV → outer-hotter" 而不是 "温度从30kpc下降到10kpc" 或 "外高内低" 等可能被误读的表述。真实教训：M104 CGM 项目中，用户说"30 kpc 0.75 keV → 10 kpc 0.6 keV"指的是外高内低，但 orchestrator 误读为内高外低，写了错误的 I007 "gradient direction correction"，后来不得不二次修正
- **⚠️ 批量文件阅读用 execute_code + read_file 循环，不要用 delegate_task** — 对 100+ 文件的大项目，delegate_task subagent 需要较长时间。正确做法：在 execute_code 中用 Python 循环调 read_file，每批 10-15 个文件，截断到 600-1500 字符/文件。这比 subagent 快 10 倍且更可控。实际验证：5 批 × 15 文件 ≈ 30 秒完成全部 85 个 summary 读取。注意：child_timeout 可调（`hermes config set delegation.child_timeout_seconds 14400`），调大后 subagent 也能完成复杂分析任务（验证：2249s 完成 31 API 调用的 c' 分解分析），但批量文件阅读仍建议用 execute_code 以减少 token 消耗
- **⚠️ 工具变更后必须审计全部下游脚本再启动长任务** — 当核心工具改变时（如优化器从 L-BFGS-B 改为 Nelder-Mead），必须先用 `grep -r` 扫描所有脚本确认变更范围，再启动任何长时间运行的模拟。否则可能运行数小时后发现仍在用旧工具，浪费计算资源。正确流程：(1) `grep -r "L-BFGS-B" scripts/` 找到所有引用 (2) 逐个修改 (3) `python -m py_compile` 验证语法 (4) 再启动长任务
- **⚠️ ProcessPoolExecutor + 大数据 → swap 灾难** — 使用 `ProcessPoolExecutor(initializer=...)` 共享大型 numpy 数组时，每个 worker 会 fork 一份数据副本。12 workers × 600MB = 7.2GB → 超出可用 RAM → 大量 swap → 1.6× 减速。规则：`max_workers × data_per_worker < 0.5 × total_RAM`
- **⚠️ 模拟结果的可信度取决于优化器选择** — 当模拟涉及 Cash statistic 拟合时，优化器选择直接影响 DeltaC/ML 值。L-BFGS-B 在宽 PSF (如 ELLBETA King) 下 2% 负 DeltaC，但在 Gaussian PSF 下仅 0.005%。构建 TRUST_TABLE 时必须标注每个实验使用的优化器，并在 Bug 影响审计中评估优化器失败对结论的污染
- **⚠️ 理论验证先做最简情形** — 当质疑"理论是否在有限统计量下失效"时，先在 1-param toy model (Gaussian PSF, 固定位置) 下验证，再逐步加复杂度 (3-param → 真实PSF → M31 path)。这样能分离每个因素的贡献。真实教训: 1-param sigma_ratio≈0.99 (无偏差), 3-param≈0.965 (nonlinear refit), M31 path≈0.956 (额外~1%)。如果跳过 1-param 直接做复杂路径，无法判断偏差来源
- **⚠️ 负控制也要记录** — 失败的实验（如 E017 psfgen-shift 给出 k>1）是重要的认知资产。不要只记录成功的实验。失败实验标记为 "dead end" 或 "negative control"，在 DAG 中用虚线红框表示
- **⚠️ 死胡同也要写 insight** — 当一个理论方案被证伪（如方案三：Edgeworth 展开不能解释方差压缩），必须写一个 confidence=High 的 negative-result insight（如 I017），明确记录：为什么这条路不通、什么证据否决了它、否决的数学/逻辑依据。这防止未来重复探索同一条死路。格式：Statement 写"X CANNOT explain Y because Z"，Evidence 写否决证据，Confidence=High（对否定结论的高置信度）。在 AI_BRIEFING 的 "Currently trusted" 中也要列出 negative-result insights
- **⚠️ 每个实验必须标注 PSF 依赖** — 在 manifest.yaml 中明确标注 `depends_on_psfgen_replica: yes/no/partial`。这是 TRUST_TABLE 的基础
- **⚠️ 文件名扫描不够，必须读内容** — 两个真实教训：第一次 OS 构建只用 `find -printf` 扫描文件名和时间线，遗漏了 E010 (ML~10 forward calibration) 等已完成的实验。第二次审计虽然读取了 71/86 个 summary 文件头部，但仍是"扫一眼就写结论"的模式，遗漏了 90+ 个 summary 文件。正确做法：每个 summary 文件必须完整读取，提取问题/结论/PSF依赖/信任级别，用 subagent 并行处理
- **⚠️ ID numbering conflicts (experiments, insights, bugs)** — When adding ANY numbered item (E/I/B), first check `ls {experiments,insights,bug_impacts}/ | sort -t_ -k1 -n | tail -3` for existing numbers. Creating I026 when I026 already exists causes confusion and requires renaming + reference updates. This is especially likely when multiple sessions operate on the same OS concurrently. Fix: (1) `ls insights/ | sort -t_ -k1 -n | tail -3` to find the highest number, (2) use `max(existing) + 1`, (3) if a conflict is discovered, rename with `mv` and update ALL references (AI_BRIEFING, TRUST_TABLE, stages, DAG, session log). **Backlink cleanup after rename is mandatory** — use `grep -r "old_name" --include="*.md" .` to find every reference, then update each one. Missing backlinks create ghost references that break Obsidian graph view and confuse future sessions. **Verification step**: after all renames, run `grep -r "I009" --include="*.md" .` (old ID) to confirm ZERO remaining references before declaring done. Real lesson: I026 was created by two sessions simultaneously — one for first-principles α, one for self-consistency analysis. Also: I009 was shared by "timing jitter" and "V52 result" files, requiring rename to I020 + updates across 6 files (I016, I017, I018, I019, S13, session log).
- **⚠️ Bug 影响审计必须完整** — AnalyticEllbetaPSF 最初被认为有 3 个 bug，但 BUGREPORT 记录了 5 个。OS 的 B001 必须与 BUGREPORT 一致，遗漏 bug 会导致污染范围低估。每次发现新 bug 时，必须回溯更新 B001 和 TRUST_TABLE
- **⚠️ Session records 是认知历史的主信息源，不是补充** — 三次审计的致命错误：先扫文件树，session 记录当补充。正确做法：先提取 Codex/Claude/Gemini session 中的 final_answer + user_message 时间线，识别认知转折点，再用文件树交叉验证。文件只记录"做了什么"，session 才记录"为什么这么做"和"为什么没那么做"。真实教训：DR14 effective mask 标定 (scut≈0.74, ecut≈14px) 和 SAS ecut 语义 (ecut=0.68 = PSF enclosed fraction) 只存在于 Claude Code session 中，三次文件树审计全部遗漏。**注意**：Gemini CLI session 可能不含科学内容（DET_ML 项目实际只用于 infra 任务），但仍需检查，且项目 GEMINI.md 可能包含有价值的 AI 生成项目概述。
- **⚠️ Bug 修复进展也要同步到 OS** — 当 bug 被部分修复时（如 spoke 角度偏移已修但振幅未解决），必须在 B001 中新增"修复进展"段落，在 TRUST_TABLE 中新增修复后代码的条目（如 T22b），在 AI_BRIEFING 中新增"partially resolved"段。否则 OS 会仍显示全面 Questioned，与实际状态不符
- **⚠️ Bug count 变更必须原子传播** — 当 bug 数量从 3 变为 5 时，必须同时更新 ALL 下游文件：B001 → TRUST_TABLE → AI_BRIEFING → stages/Sxx → wiki → skill reference → codex_research_log_summary。遗漏任何一个会导致不一致。检查清单：`grep -r "3 bugs\|3 个 bug\|3 critical bugs" research-cognition-os/` 确认无残留旧数字
- **⚠️ Convention parameter 定义错误的三层审计** — 当发现核心库函数的参数定义有误（如 gammaincc 漏 /2、shape 参数用错 convention），必须做三层审计：(1) **Code 层**: `grep -rn` 所有直接调用和间接引用，按风险分级（🔴直接错误/🟡内联正确但重复/🟢已正确），列出受影响脚本清单；(2) **Cognition-OS 层**: 搜索所有 insights/decisions/sessions 中的错误参数值（如 shape=2.5→1.5），逐个修正并标注修正原因；(3) **Wiki 层**: 交叉验证 wiki 公式与实际代码行为。真实教训：lib/detml.py 漏 /2 → dC_thresh 偏小 2x → 82 处代码引用 + 7 处文档错误 + 6 处 cognition-OS convention 错误。shape=2.5 vs 1.5 的 convention 混乱传播到 6 个文件。**规则**: 发现 convention bug 后，用 `grep -rn` 扫描三层（code + cognition-OS/*.md + wiki/），列出完整受影响清单，再逐个修复。不要只修发现 bug 的那个函数
- **⚠️ Convention 错误≠Bug 数量变更 — 两个独立的审计维度** — Bug 数量变更（如 3→5 bugs）和参数 convention 错误（如 shape=2.5→1.5）是两个独立的传播维度。前者沿 B001→TRUST_TABLE 链传播；后者沿 insights/decisions/sessions/wiki 链传播。两者可能同时发生（如 lib/detml.py 的 /2 bug 既增加了 bug count 又改变了 convention），但审计清单不同。**规则**: 每次发现核心函数错误时，同时做两个审计：(1) bug count 原子传播 (B001→TRUST_TABLE→AI_BRIEFING)，(2) convention 参数值三层审计 (code→cognition-OS→wiki)
- **⚠️ Var(deltaC) 完全独立于 S_true** — `deltac_moments_3param(S_hat, b, psf)` 的 Var 项不含 S_true。不要把 Var(deltaC|S_true) 和 Var(deltaC|S_hat) 混淆。前者是 Poisson 统计涨落（理论准确），后者包含 S_hat 测量误差导致的额外 scatter（population mixing）。混淆二者会导致无意义的 H_var 修正或 G(x) overdispersion 讨论
- **⚠️ 4XMM DET_ML = -ln(Q), 不是 -log10(Q)** — 因子 ln(10)=2.303。如果理论代码用 -log10 而比较对象是 4XMM DET_ML，所有 ML 值差 2.303×。delta_c_nu3 = deltaC/2（gammaincc 的 x 参数），不是 deltaC 本身。先用 catalog 验证 log base 再做任何定量比较
- **⚠️ 不同计算框架的参数不能混用** — factorized proxy 的 S_proxy=0.75×CTS 和 B_proxy=89.67×BG 是经验拟合参数，不是物理量。它们不能作为 deltac_moments_3param() 的输入。混用会导致 deltaC 偏差 8-50×。真实教训：用 B_proxy/N_eff 作为 b_per_pix 输入 deltac_moments_3param，得到 ratio≈8 (实际应是≈1)。**规则**：每个计算框架有自己封闭的参数定义，跨框架比较必须在输出层（deltaC/ML），不在输入层（S, b）
- **⚠️ Convention trap 连锁效应** — 三个 convention 陷阱（ln/log10、deltaC/2、proxy≠physical）不是独立的，它们会连锁放大：(1) 用 log10 而非 ln → ML 差 2.3× → 反推 deltaC 也差 → (2) 再搞错 delta_c_nu3 含义 → deltaC 又差 2× → (3) 再混用 proxy 和 physical 参数 → 又差 8×。累积偏差可达 2.3×2×8≈37×。**规则**：做任何 catalog 比较前，先做 round-trip 验证（从 delta_c_nu3 反推 ML vs DET_ML 列），确认 convention 正确后再做定量分析
- **⚠️ 先读理论代码再提方案** — 用户对自己的理论代码（如 `deltac_moments_3param`）非常熟悉。当用户问"能不能从 X 出发做 Y"时，必须先读相关理论代码（`inspect.getsource`），理解公式结构和参数依赖，再提出方案。跳过这步直接用近似公式或错误假设，会被严厉纠正。真实教训：用户问 Var(deltaC) 能否从 catalog 得到，AI 用了粗糙的 conditional_DET_ML_width（含 S_true 依赖）而不是正确的 deltac_moments_3param（Var 独立于 S_true），导致提出错误的 H_var 修正框架
- **⚠️ 关注 deltaC 而不是 ML** — 用户明确说"不要太纠结 ML, deltaC 才是我们关注的"。ML 只是 deltaC 的非线性变换。分析应在 deltaC 空间做，ML 只作为上下文参考。在 deltaC 空间验证理论（mean 和 variance），再转换到 ML 空间报告结果
- **⚠️ 不同计算框架的参数不能混用** — factorized proxy 的 S_proxy=0.75×CTS 和 B_proxy=89.67×BG 是经验拟合参数，不是物理量。它们不能作为 deltac_moments_3param() 的输入。混用会导致 deltaC 偏差 8-50×。真实教训：用 B_proxy/N_eff 作为 b_per_pix 输入 deltac_moments_3param，得到 ratio≈8 (实际应是≈1)。**规则**：每个计算框架有自己封闭的参数定义，跨框架比较必须在输出层（deltaC/ML），不在输入层（S, b）
- **⚠️ Convention trap 连锁效应** — 三个 convention 陷阱（ln/log10、deltaC/2、proxy≠physical）不是独立的，它们会连锁放大：(1) 用 log10 而非 ln → ML 差 2.3× → 反推 deltaC 也差 → (2) 再搞错 delta_c_nu3 含义 → deltaC 又差 2× → (3) 再混用 proxy 和 physical 参数 → 又差 8×。累积偏差可达 2.3×2×8≈37×。**规则**：做任何 catalog 比较前，先做 round-trip 验证（从 delta_c_nu3 反推 ML vs DET_ML 列），确认 convention 正确后再做定量分析
- **⚠️ Feature decomposition debugging** — 当模型与 ground truth 之间有系统性差异时，用特征分解法定位：逐个关闭模型组件（spokes, az_mod, ellipticity, smoothing），测量每步的 RMS 变化。如果"关闭某组件"与"开启全部"给出相同结果，说明该组件从未被应用（dict key mismatch / indentation bug / guard condition failure）。真实教训：AZIMUTH_MOD 键名 'MOS1' vs 'EMOS1' 导致 az_mod 从未被应用，但"No az_mod"和"Full"给出完全相同的 RMS，立刻暴露了问题
- **⚠️ 模拟实验必须报告派生统计量的误差** — 当报告 sigma_ratio、k(ML) 等从模拟中提取的统计量时，必须同时报告该统计量的不确定性。用户明确要求：误差 < 统计量的 1/5（相对误差 ≤ 20%）。方法：(1) 将样本分成 N_chunk≥10 等份，每份独立计算统计量，报告 std 作为误差（bootstrap chunk）；(2) 或用 bootstrap/jackknife 重采样；(3) 优先提高 N_sims 直到满足精度要求。**不报告误差 = 结果不可信**。真实教训：旧结果 "-6.1%, -1.3%, -11%" 趋势奇怪但无法判断是真实还是统计涨落，因为没误差棒
- **⚠️ Cash statistic DeltaC 计算要用直接公式** — 不要分别算 C_best 和 C_null 再相减。C_null = 2·sum(b - Y·ln(b)) 容易漏掉 `2·sum(b)` 项（只写了 `-2·sum(Y·ln(b))`）。正确做法：直接算 `DeltaC = 2·sum(b - mu_best + Y·ln(mu_best/b))`，避免拆分。真实教训：脚本第一版 C_null 漏了 `2·sum(b)` 项，导致所有 DeltaC 偏移
- **⚠️ L-BFGS-B 3-param 拟合速度强依赖 SNR** — 高 SNR (S=40, b=0.1): ~9 ms/fit；低 SNR (S=10, b=0.4): ~148 ms/fit，慢 16×。估算运行时间时必须用低 SNR 的速率，否则严重低估。用 `multiprocessing.Pool(16)` 可并行，但内存需 ~800MB/worker
- **⚠️ 物理模型在扩展域上可能反向失效** — 一个在标定域（如 Gaussian PSF）上验证通过的半解析模型，在扩展域（如 ELLBETA King PSF）上不仅可能退化，还可能预测与实际相反的方向（如 k=1/√(1+α·r²) 预测 ELLBETA 压缩更小，但实际更大）。根因常是物理变量的操作化定义（operationalization）有误——如 σ_PSF 用二阶矩而非核心宽度。**教训**：验证模型时，必须测试定性不同的条件（不同 PSF 形状，而非仅不同 S/b 参数），而不仅是参数空间的外推
- **⚠️ 当模型在扩展域失效时，穷举操作化定义** — 如果模型依赖一个可多种定义的物理量（如 σ_PSF），穷举所有合理定义并测试哪个能统一标定域和扩展域。如果所有定义都无法统一（如 σ_PSF 的 5 种定义都无法让 Gaussian/ELLBETA 共享同一个 α），说明该量不是真正的普适量——需要找到更底层的守恒量（如 C=α/σ_PSF²）。**真实教训**：5 种 σ_PSF 定义给出相同的 RMS（因为只是 r 的线性缩放），但 α 差异巨大；C=α/σ_PSF² 才是真正的物理量，Gaussian C=0.105 vs ELLBETA C=0.222 (2.1×) 说明 PSF 形状（不仅仅是宽度）决定了有效 C
- **⚠️ 当噪声相关长度是白噪声时，压缩机制在别处** — 如果残差场 Z_⊥ 的空间相关长度只是像素尺度（ξ=0.5 pix），那么压缩不是来自噪声的空间相关性。真实教训：对于 DET_ML，残差场是白噪声（Poisson 噪声逐像素独立，3 个约束从 709 像素中减去可忽略），而 ΔC 景观相关长度（ξ≈2.54 pix）对 Gaussian 和 ELLBETA 相同。压缩来自 PSF 梯度结构如何将独立噪声映射到相关的 ΔC 景观——这是 PSF 形状的属性，而不是噪声的属性
- **⚠️ 翼状参数统一 α (winginess model)** — 当所有 σ_PSF 定义都无法统一 α 时，用 winginess W = σ_2nd/FWHM 缩放 α。模型：k = 1/√(1 + α · r² · W)，γ=+1.0（W 是正乘数，放大压缩效应）。对于 DET_ML，α=0.325 统一 Gaussian (W≈1.13) 和 ELLBETA (W≈2.89)。**注意**：早期 γ=-0.482 是错的——用了 FWHM/2.355 作为 σ_PSF，混淆了 r 的定义。正确 r = σ_pos/FWHM（不是 σ_pos/(FWHM/2.355)），γ=+1.0。验证：242 数据点，RMS=0.0445，ΔBIC=37。见 emldetect skill pitfall #38d
- **⚠️ σ_PSF 定义变更会翻转模型参数的符号/含义** — 当模型中 r 的定义从 σ_pos/(FWHM/2.355) 改为 σ_pos/FWHM 时，γ 可从负变正。这不是数值巧合，是物理含义的根本变化。**教训**：参数符号剧变时必须重新审视物理含义，而非只做数值比较。详见 `references/session6-methodological-lessons.md` Lesson 1
- **⚠️ 利用已有数据验证 vs 重跑模拟** — 先检查是否已有可复用的模拟数据，做零成本分析确认模型可行后，再投入计算资源。DET_ML 中 242 点已有数据足以验证 winginess 模型，而新 King PSF 模拟 300s 超时且结果无效（grid 太粗 + S/N 太高）。详见 `references/session6-methodological-lessons.md` Lesson 2
- **⚠️ 跨 session 重大发现的影响梳理流程** — 另一个 session 报告重大发现时：(1) 列出所有受影响项 (2) 评估 trust level 变化 (3) 检查是否解除阻塞 (4) 更新 AI_BRIEFING + TRUST_TABLE + stage/insight (5) 识别新方向。不要只做局部更新。详见 `references/session6-methodological-lessons.md` Lesson 3
- **⚠️ PSF 模板预计算 vs 即时生成 — 速度差 50x** — `psf_model.build()` 7×7 子像素 ~5ms/call vs 预计算模板 + `ndimage.shift` ~0.1ms/call。当 PSF 形状在拟合中不变（只有位置偏移），必须预计算。例外：PSF 形状随位置变化时需多个模板插值。详见 `references/session6-methodological-lessons.md` Lesson 4
- **⚠️ Bug 严重度应以核心科学结论影响为准** — Spoke 振幅偏大 2.7-2.9× 对 PSF 形状影响大，但对 DET_ML 影响 <0.5%→ 严重度应从"中等"降为"低"。Bug 严重度 = max(中间量影响, 核心结论影响)，但最终评级以核心结论为准。详见 `references/session6-methodological-lessons.md` Lesson 5
- **⚠️ 等价重参数化模型的识别** — 当两个模型参数数量相同且 BIC 一致时，它们是等价重参数化。选择物理含义更清晰的那一个。例：winginess 模型 vs separate-α 模型 BIC 相同，但 winginess 有清晰的 W = σ_2nd/FWHM 物理含义。详见 `references/session6-methodological-lessons.md` Lesson 6
- **⚠️ 参数分解的循环论证陷阱** — 当半解析模型有经验参数 α，将其分解为 α = c·c'/W_ref 且声称 c' 是"独立推导的"，必须验证独立性。检验方法：将 c' = α/c 代回，看是否得到恒等式（如 α = α/W_ref → W_ref=1 矛盾）。真实教训：DET_ML 项目声称 α = 0.74×0.5/1.126 = 0.329 ≈ 0.325（1% 匹配），但 c' = 0.5 实际上是 α/c 的近似值，代入后得到 α = α/W_ref（矛盾）。1% 匹配是巧合而非推导。**规则**：任何参数分解必须通过"代回检验"——将分解式代回原式，确认不会产生矛盾。详见 `references/first-principles-derivation-pattern.md`
- **⚠️ 2 阶 Taylor 展开可能预测错误方向** — 对非线性统计量（如 ΔC 在优化位置处的值），2 阶展开可能给出与观测相反的预测。真实教训：ΔC(x̂) = ΔC(0) + (κ/2)·dr² 预测 3-param 方差 > 1-param 方差，但实际观测 3-param 方差 < 1-param 方差（~11% 压缩）。压缩是 beyond-Fisher 的非线性效应，2 阶展开无法捕捉。**规则**：当理论预测与观测方向相反时，不是理论公式有错，而是线性化假设失效——需要更高阶或完全不同的框架
- **⚠️ 自洽性优先于外部一致性** — 当理论验证涉及"我们的实现 vs 闭源参考实现"的系统性偏移时，将验证分成两个独立问题：(1) **自洽性 (PRIMARY)**: 理论能否描述自己的 pipeline 的结果？(2) **外部一致性 (SECONDARY)**: 我们的 pipeline 是否匹配参考实现？必须先通过自洽性，再追求外部一致性。系统性偏移（如 ~8% ML offset）是校准常数，不是理论失败。在 CURRENT_QUESTION 中明确写出两个层级，将外部一致性放入 Parking Lot 直到自洽性通过。真实教训：DET_ML 项目花大量时间追踪 emldetect 的 ~8% ML 偏移（闭源 fortran fftpsf.f90），后发现 4-step vs 8-step PSF 差异 <0.5%，偏移来自 sub-pixel integration 实现细节。论文可以写："理论在自有 pipeline 上验证至 ~5%；与 emldetect 的 ~8% 偏移归因于 PSF 构建差异"
- **⚠️ 旧结论标注 superseded，绝不覆盖** — 当新发现推翻旧结论时，不要修改旧 insight/decision 的内容，而是：(1) 将旧条目 status 改为 `superseded`，(2) 添加 `⚠️ SUPERSEDED` 标题标注 + 链接到新 insight，(3) 创建新 insight 记录修正后的结论，(4) 在 TRUST_TABLE 中标注旧条目降级。**绝不原地覆盖旧结论**——研究历史是有向图，不是可变数组。覆盖旧结论会让依赖它的推理链变成孤儿，未来无法追溯"当时为什么这么判断"。用户明确要求："不要修改之前的结果，而是标注不再可靠，这样以后就像把它们剪切掉了，我们重新做新的版本。这样不会使得我的研究历史发生混乱。"真实教训：I028 的"PSF sub-pixel misalignment ~4%"被 I029 推翻（真正原因是背景梯度），I013/D07/D08 全部标注 superseded+链接 I029，旧内容完整保留
- **⚠️ Subagent 结论必须交叉验证 (3-level protocol)** — 当 subagent 通过 `delegate_task` 返回定量分析结果时，不要直接记录为 insight。5 个 subagent 部署中 2 个有公式/逻辑错误。三级验证：(1) **Formula check**: 每个公式对照第一性原理检查，特别关注 scaling (1/S vs 1/sqrt(S)) 和大膨胀因子 (>3x)；(2) **Number check**: 重跑脚本验证数字，用独立数据集交叉检验；(3) **Logic check**: 检查物理假设是否正确，"X导致Y"是否在去掉X后仍然成立。真实教训 Round 1：subagent 声称 f²=3.81 inflation (逻辑错误) 和 sigma_pos≈FWHM/sqrt(S) (公式错误)。详见 `references/orchestrator-subagent-research-workflow.md`
- **⚠️ 假设的 pipeline 来源必须验证** — 当一个 session 报告"X 代码有 Y bug 导致 Z% 偏移"时，必须先验证：(1) 这个 bug 是否存在于主 pipeline（不只是辅助脚本）？(2) 主 pipeline 是否已经用其他方式处理了这个问题？(3) 偏移数据来自哪个 pipeline？不做验证就实现 fix = 浪费时间。真实教训：I028 说"PSF sub-pixel misalignment ~4%"来自 `fft_psf_wrapper.py`（用 `int(round(x))` 做整数位移），但主 pipeline `run_sb_grid_1k.py` 的 `build_psf(x0+dx, y0+dy)` 已经是 sub-pixel 精确的。实现 FFT phase shift 模块后发现它对主 pipeline 无用。正确做法：先 `grep -rl` 搜索哪些代码引用了有 bug 的模块，再决定是否实现 fix
- **⚠️ 不要轮询长任务 — 用后台监控 + Bark 通知** — 当启动长时间运行的后台任务（>30 min）时，不要反复执行 `sleep N && ls results/` 轮询。正确做法：(1) 启动后台监控脚本（`while ! -f output.csv; do sleep 300; done && echo DONE`），(2) 用 Bark 通知完成，(3) 在等待期间做其他有用工作（如自洽性分析、误差预算）。轮询不仅浪费时间，还因为 terminal timeout 限制导致大量无效调用。真实教训：E010 NM 重跑预计 8h，轮询了 3h 无产出；改为后台监控 + 并行做自洽性分析后，3h 内完成了完整的误差预算分解
- **⚠️ 实验 subdirectory 格式 vs flat 格式** — SKILL.md 定义了 flat 格式（`experiments/E010_xxx.md` + `E010_xxx_manifest.yaml`），但实际使用中 subdirectory 格式（`experiments/E010b_nm_rerun/manifest.yaml + summary.md`）也可接受。两种格式的选择：(1) flat 格式适合简单实验（1-2 个文件），(2) subdirectory 格式适合有多个产物的实验（figures/, data/ 等）。**无论选哪种，manifest.yaml 必须包含 `experiment_id`, `date`, `status`, `trust_level`, `question`, `main_result`, `linked_insights`**。真实教训：E010b 用了 subdirectory 格式，与 skill 定义不同但不影响功能
- **⚠️ 多方向并行研究用 execute_code，不用 delegate_task** — 当需要同时研究 N 个方向（如 5 种修正策略的 ablation study），不要用 `delegate_task` 并行派发 N 个 subagent。Subagent 有 600s child_timeout 限制，对需要读取多个 CSV + 运行 bootstrap 的定量分析来说太短（实际 3/3 全部超时）。正确做法：在 execute_code 中按方向顺序分析，每个方向一个 code block，结果直接写入 OS。这比 subagent 快 10×（30s vs 600s timeout）且结果更可控。只有在每个方向需要 >30 min 独立计算时才用 delegate_task（且需调大 child_timeout）。真实教训：DET_ML catalog-only ML 预测的 5 方向分析，3 个 subagent 全部 600s 超时，改为 execute_code 后 5 个方向全部在 ~2 min 内完成
- **⚠️ "捷径路"评估模式 (shortcut evaluation pattern)** — 当项目有两条路：(1) 完整复刻路（有完整数据，做大量模拟）和 (2) 捷径路（只有部分参数，经验化对齐），必须量化捷径路的精度极限。方法：(a) 列出所有修正级别（如 σ_eff → k(ML) → r(OFFAXIS) → G(x)），(b) 逐级计算 bias + uncertainty，(c) 量化每级修正的贡献（ablation study），(d) 判断精度是否满足应用需求。真实教训：DET_ML catalog-only ML~10 预测：2% bias + 5% uncertainty，对 sensitivity map 够用。关键发现：kappa 校准常数不随 OFFAXIS 变化（2.28 ± 0.01），已被 σ_eff 吸收
- **⚠️ 方差的条件化变量决定结论 (variance conditioning trap)** — Var(deltaC | S_true, b) ≈ Var(deltaC_1p) (H_var≈1.0, 3-param 不改变 variance), 但 Var(deltaC | ML_bin) 给出 H_var≈0.35 (看起来 3-param 大幅减小 variance), 而 Var(deltaC | S_hat_bin) 给出 H_var≈0.3-0.9 (非单调). **三个数字描述的是完全不同的物理量**。按 ML 分 bin = 按 deltaC 分 bin → 人为压缩了 bin 内 deltaC 范围 → H_var 偏小是 selection bias, 不是物理效应! **规则**: 报告任何 variance 比值时, 必须明确写出 "Var(X | conditioned_on_what)"。对于 inference/sensitivity/catalog 应用，默认需要 observable-conditioned moments，例如 `Var(deltaC | S_hat, b, psf)` 或对应 residual width；`S_true` 只能作为 simulation bookkeeping label。不要用 `Var(deltaC | ML_bin)` 推断 intrinsic conditional variance。详见 `references/variance-conditioning-trap.md`
- **⚠️ 绝不做 ML 截断来分析条件分布 (ML truncation trap)** — realized ML 是 realized DeltaC 的非线性单调变换；fixed observable inputs 下的 expected/typical ML 由 `(S_hat, b, psf)` 决定, 不由 `S_true` 决定。分析 p(DeltaC | conditions) 时, 必须按 S_hat/observable bins 分析, 而不是在 ML 范围上截断。ML 截断 = DeltaC 截断 = selection cut → 截断边界处产生虚假 skew (可达 1.0+), bin 内 variance 被人为压缩。**正确方法**: (1) 按 S_hat 分 bin, (2) 减去理论 mean DeltaC, (3) 分析 residual 的 mean/std/skew/kurtosis, (4) 用 bin 的典型 ML 值来选择感兴趣的 bin (如 "ML~6-10 的 S_hat bin")。真实教训: Subagent E 对 ML=[5,10] 截断后报告 skew=1.28 (边界效应), 但按 S_hat 分 bin 后 intrinsic skew<0.3。详见 `references/variance-conditioning-trap.md`
- **⚠️ 关键库函数必须做 round-trip 测试 + 外部数据交叉验证** — `lib/detml.py` 的 `gammaincc(a, delta_c)` 漏了 `/2`，导致 `delta_c_from_detml(6.0, nu=3)` 返回 7.17 而非正确的 14.34。下游所有 P(ML>=6) 分析都基于错误阈值，结果看似正确（~1.0）但完全无效。Bug 仅在手动验证 `detml_from_delta_c(30.35, nu=3)` vs highstat benchmark 时发现。**规则**：对任何 DeltaC↔ML 转换函数，(1) 做 round-trip test，(2) 用已知外部数据验证至少一个点，(3) 检查 dC_thresh 是否在物理合理范围内（如 dC_thresh(ML=6) 应 ~14 而非 ~7 for typical sources）。详见 `references/variance-conditioning-trap.md`
- **⚠️ "我们已经有理论" — 不要假设用户要从零获取** — 当用户问 "X 能否从 Y 得到?" 时, 不要自动假设用户没有 X 的理论。先确认用户已有的理论框架, 再讨论如何用数据标定/修正。真实教训: 用户问 "sigma(deltaC) 能否从 catalog 直接得到?", 我花大量分析论证 "catalog 只有 1 个 ML/源, 无法直接拿 variance", 但用户实际已有 3-param sigma(deltaC) 理论, 只是想用 catalog 做 out-of-sample 验证 + 经验修正。正确做法: 先问 "你已有的理论是什么?", 再对齐分析目标
- **⚠️ scut=0.9 fix is negligible — azimuth PSF mismatch is the real blocker** — When catalog Z shows systematic offsets, "fix scut from 1.0 to 0.9" is the first instinct. But simulation shows dZ = -0.020 ± 0.009 (95% CI: [-0.038, -0.002]). When theory and fit use the same mask, Z is invariant to mask size. The real off-axis problem is azimuth-dependent PSF template mismatch: at the same off-axis, Z varies by 1.46σ depending on azimuth, due to 31×31 template truncation + XMM mirror asymmetry. **Rule**: before chasing small convention fixes, run a simulation comparison to quantify the expected effect. If the expected effect << observed offset, the root cause is elsewhere. Real lesson: I044 v1→v2 on-axis shift of +0.24 was attributed to scut, but simulation showed scut effect is only -0.020. The real cause was filter/sample changes + PSF model differences.
- **⚠️ 1000 reps/cell needed for per-position low-S SE targets** — At 500 reps/cell, per-position S_fit<5 SE audits ALL FAIL (SE=0.05-0.53 vs target 0.05). At 1000 reps/cell, ALL PASS (SE=0.009-0.010). The threshold is sharp: 500 reps gives ~4000 samples per position×S_bin, 1000 reps gives ~8000. For SE(mean Z) < 0.05 with std(Z)~0.85, need N > (0.85/0.05)² ≈ 289 per bin. But per-position×b_true subdivision requires N_total > 17×6×289 ≈ 29,469. With 8 S values, that's ~3,700 per (position,S) cell, which 500 reps barely meets. **Rule**: for per-position low-S validation, budget 1000 reps/cell minimum.
- **⚠️ S<5 degenerate outliers from near-zero var_3p** — In mask stress test, 0.17% of samples (325/1,680,000) have S_fit≈0.01 and var_3p≈1.9e-8, giving Z values of -2294 to -100. These extreme values inflate SE and std for the entire S<5 bin. **Rule**: apply clean cuts S_fit > 0.5 AND var_3p > 0.01 before any statistical analysis. Do not use S_fit > 0.1 alone — the degenerate tail (0.1 < S_fit < 0.5) still contains extreme Z values.
- **⚠️ PSF template truncation at 31×31** — The 31×31 template captures only 89% of flux at 14' off-axis (vs 96% on-axis). This truncation makes the PSF appear narrower, causing mu_3p to be underestimated. The effect is azimuth-dependent because the PSF is elongated radially. **Rule**: for off-axis sources, use 401×401 templates with sub-extraction, or accept ~10% systematic bias in mu_3p.
- **⚠️ scut=0.9 vs 1.0 simulation comparison before declaring a fix** — When a convention mismatch is suspected, run a controlled simulation comparing the two conventions before modifying the production pipeline. The I044 scut comparison used 3 positions × 4 S × 3 b × 500 reps = 36,000 tasks and found dZ = -0.020 ± 0.009. This small effect ruled out scut as the root cause. **Rule**: always quantify before fixing. A 36k-task simulation is cheap compared to days of chasing the wrong root cause.
- **⚠️ PSF 模板文件可能损坏 — 重新生成验证** — 当 PSF 模板显示异常（如 peak 极低、PSF 看起来是 flat），不要假设是 detector boundary 或 coordinate error。先用 psfgen 在**相同坐标**重新生成 PSF。如果重新生成的 PSF 正常，则原始文件是损坏的。真实教训：P6 (x=330,y=330) 的 psfgen 输出 peak=0.006（应为 0.073），被误标为"detector-boundary outlier"数周，实际只是文件损坏。重新生成后 peak=0.073，与 on-axis P8 完全一致。**规则**：PSF 异常时，先重新生成再诊断
- **⚠️ Catalog bridge 必须用 position-dependent PSF 模板** — 对 catalog 源计算 Z-score 时，不能用单一 on-axis PSF 模板。On-axis PSF 用于所有源会产生 mean(Z)=-0.74 的系统性偏差（off-axis PSF 更宽，on-axis 模板高估 mu_3p）。必须为每个源分配最近位置的 PSF 模板。真实教训：M31 OBSID 0800732701 的 21k 源，用 on-axis PSF 给出 mean(Z)=-0.74，用 position-dependent 模板给出 mean(Z)=-0.04
- **⚠️ Catalog bridge 必须过滤 MASKFRAC < 0.8** — 不做 MASKFRAC 过滤时，detector edge 附近的源给出灾难性 Z 值（14' off-axis mean(Z)=-1.6）。这些源的 PSF footprint 被 detector boundary 截断，emldetect 的 PSF 模型与模板不匹配。**规则**：catalog Z-score 分析前必须 MASKFRAC > 0.8
- **⚠️ PSF 模板不要 renormalize** — 当 off-axis PSF 模板 sum < 1.0（因 31×31 crop 截断 wings），renormalize 到 sum=1.0 会让 Z 更负（mean(Z) 从 -0.75 变成 -1.99）。截断的 PSF sum 反映 detection cell 内的实际 enclosed energy，理论已通过 mask 考虑了部分覆盖。不要 renormalize
- **⚠️ PSF 模板文件名坐标精度** — psfgen 输出文件名使用传入的精确浮点坐标，如 `psf_PN_b4_x331.5_y519.167_s31.img`（不是 `y519.2`）。加载模板时用 `os.listdir()` + 解析文件名，不要硬编码坐标字符串
- **⚠️ 库函数名大小写必须与模块一致** — `lib/fit_mask_3param.py` 导出 `weighted_deltac_moments_3param`（小写 'c'），不是 `weighted_deltaC_moments_3param`。大小写不一致导致运行时 ImportError（不是 import 时，因为 multiprocessing pool 延迟加载）。**规则**：使用库函数前，用 `grep -n 'def ' module.py` 确认确切函数名
- **⚠️ SAS LD_LIBRARY_PATH 冲突导致 pdftotext 失败** — 当 SAS 环境已初始化时，其 `libstdc++.so.6` 覆盖系统库，导致 `pdftotext` 报 `GLIBCXX_3.4.29 not found`。**规则**：在 X-ray 项目中提取 PDF 文本时，用 `LD_LIBRARY_PATH="" pdftotext -layout file.pdf -` 临时清除 SAS 库路径。类似地，python-docx 的 `doc.paragraphs` 不包含表格内容，必须单独遍历 `doc.tables`
- **⚠️ Backtest engine silent bugs invalidate months of conclusions** — Quantitative backtest engines are prone to silent bugs: (1) `datetime.date` vs `DatetimeIndex` silent fallback to default (0% match rate, looked like "no alpha" for months); (2) look-ahead bias via `future_return_7d` in `dropna()` required list; (3) hardcoded `hold_days=7` overriding config `h=14` making grid search flat (identical results across h values misinterpreted as "robustness"); (4) T+0 settlement giving unrealistically low MaxDD; (5) IC sign flip from descending convention. **Detection rule**: if a grid search produces identical results across a parameter dimension, the parameter is likely hardcoded elsewhere — verify intermediate results differ, not just final outputs. **Prevention**: always verify dynamic allocation match rates (>80%), audit all `dropna(subset=[...])` for look-ahead columns, add settlement delay, run agy-review before publishing. See `references/backtest-engine-silent-bugs.md` for full catalog and prevention checklist
- **⚠️ Faithfulness audit for paper reproduction projects** — When a Cognition OS tracks paper reproduction (not original research), there is a systematic overclaim bias: engineering workarounds get recorded as successful reproductions. Four overclaim patterns: (1) **Workaround→reproduction**: MOS-only fit recorded as "reproduced Table 3" when paper used MOS+PN jointly (systematic kT offset 0.04-0.08 keV); (2) **Extension→main model**: 2-APEC diagnostic recorded as "final result" when paper only uses 1-APEC; (3) **Partial→complete**: FUV filament with one quadrant severely contaminated recorded as "reproduced"; (4) **Bug-blocked→resolved**: PN data recorded as "available" when EXPOSU* bug makes spectra unreliable. **Audit procedure**: (a) Read paper tables for exact target values, (b) Read actual result JSON files, (c) Build per-item comparison: claimed vs paper vs residual, (d) Classify: GOOD (Δ<1σ) / FAIR (1-2σ) / POOR (>2σ or blocked), (e) Update OS: downgrade overclaims in AI_BRIEFING, add blockers as Bxxx, update TRUST_TABLE. Save audit to `reviews/YYYY-MM-DD_faithfulness_audit.md`. **Real lesson**: NGC3079 HK2020 audit found hp0.0 kT incorrectly recorded as 0.27-0.30 (actual 0.416±0.070), Phase 6d 2-APEC incorrectly promoted to "final result" (actually an extension). See `xray-thermal-joint-fitting` → `references/pyxspec-api-pitfalls.md` Pitfall #38

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
   - Tool quirks (e.g., xselect exit code bug)
   - Environment conflicts (e.g., HEADAS vs CIAO)
   - Domain-specific conventions (e.g., FXT coordinate system vs XMM)
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

FXT data reduction project (`~/program/fxt_data_reduction/`): User goal was "学会使用 FXT 的数据处理方法". OS initialized with 3 stages (environment → batch pipeline → source detection), 3 insights (coordinate system, HEADAS/CIAO conflict, RA/DEC alignment), and a parallel wiki with 12 pages covering FXT tools and concepts. Total: 13 cognition OS files + 19 wiki files, created in one session with delegate_task audit.

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

**Verified example**: M82 SQUDE project (`~/Data/M82/`): Research project with complete Chandra→Sherpa→SQUDE pipeline but < 2 prior sessions. OS built from file tree + proposal PDF + 2 reviewer docx files in one session. 20 files: 4 stages (extraction → baseline fit → SQUDE simulation → proposal upgrade), 4 insights (param recovery, center bin contamination, reviewer convergent weaknesses, proposal draft notes), 3 experiments, 7 decisions. Proposal upgrade executed as 7-phase goal prompt workflow (see "Proposal Upgrade Workflow Pattern" section in SKILL.md). See `references/young-research-project-os-build.md` for details.

**Verified example (M104_TwoPhaseGas)**: Young research project with 2T APEC fitting pipeline + FAST_MODE screening results. OS built via subagent delegate_task in one session from AGENTS.md + FAST_MODE CSVs + key script sections. 14 files: 3 stages (1T baseline → 2T FAST screening → CXB-hot degeneracy Plan A/B/C), 4 insights (CXB-hot degeneracy, plt.show() blocking, SrcHotApec link bug, Plan A CXB marginalization result), 2 bug impacts, 1 session record. Key pattern: insights include both positive results (I004: Plan A verification) and negative results (I002: plt.show() blocking as pitfall insight). See `~/program/M104_TwoPhaseGas/research-cognition-os/` for the live OS.

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

**Verified example (M31CGM Disk 0.7keV)**: Existing M31 CGM project with 145 OBSIDs, v18 per-OBSID fitting pipeline, WISE stellar mass map. User identified that disk shows 0.7 keV component but halo does not → new question: does 0.7 keV norm scale with stellar mass? OS built in one session: 1 stage (5 phases: geometry → halo verification → per-OBSID disk fitting → M★ correlation → interpretation), 2 insights (disk/halo asymmetry, halo-as-sky-background), 3 decisions (halo as bg, per-OBSID approach, EPIC only). Key pattern: TRUST_TABLE inherits existing pipeline trust while adding new assumptions (halo=no M31 emission, per-OBSID S/N sufficient) at Provisional/Questioned. See `~/program/M31CGM/research-cognition-os/` for the live OS.

**Verified example (N132D RGS)**: Young research project — spectral-analysis pipeline (not proposal). XMM-Newton RGS data for LMC SNR N132D: 5 OBSIDs processed, 2 clean, stacked spectrum with 15+ emission lines identified. OS built from file tree + 1 session summary in ~15 min, no subagents. 26 files: 4 stages (acquisition → flare screening → stacking → spectral modeling), 4 insights (pipeline complete, clean OBSID selection, combined spectrum valid, emission line inventory), 4 experiments with manifests. Key pattern: no external documents (proposal/reviewers) — all insights from data products; current stage S04 is forward-looking (what model to fit); trust table includes physical priors (spatial broadening, O-rich ejecta) alongside experimental results. See `references/n132d-rgs-cognition-os-build.md` for the full build procedure.

### Data-only project pattern

Some projects have no separate `~/program/<Proj>/` code directory — all data, scripts, and products live under `~/Data/<Proj>/`. The cognition OS should still be created under the data directory: `~/Data/<Proj>/research-cognition-os/`.

**Key characteristics**:
- No code-data separation (no `data` symlink needed)
- Scripts may be scattered across OBSID subdirectories or a `combined/` directory
- No AGENTS.md or README.md at project root — look for CLAUDE.md or fit report files instead
- XCM scripts and logs serve as the primary "experiment" records

**Build procedure** (same as young-project streamlined audit, but):
1. Use `execute_code` for bulk file discovery (XCM/log file listing, directory structure) — faster than subagents
2. Read the latest XCM scripts + their logs to extract fitting parameters and results
3. If a detailed audit document already exists (e.g., CODEX_AUDIT_PROMPT.md), symlink it into `artifacts/` rather than duplicating content
4. Stages = fitting iteration phases (convention fixes, image comparison, blocker discovery), not pipeline steps

**Verified example (M31Center RGS)**: Data-only project under `~/Data/M31Center/` with 34+ XMM OBSIDs, Chandra images, and 21 XSPEC fitting script versions (v1-v21). OS built from CODEX_AUDIT_PROMPT.md + XCM log scanning in one session. 18 files: 3 stages (initial fitting → convention fix → rgsxsrc blocker), 3 insights (model convention, image→O abundance link, rgsxsrc multi-image limitation), 3 experiments (36 ObsID stack, image comparison, no-rgsxsrc baseline), 1 bug impact (convention errors). Key pattern: pre-existing audit document symlinked as artifact; stages track fitting iteration phases, not pipeline steps; trust table includes both confirmed conventions (angr/χ²/Fe=0.57) and open blockers (rgsxsrc multi-image). See `~/Data/M31Center/research-cognition-os/` for the live OS.

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
| `#psf-dependent` | Depends on PSF code | Items affected by AnalyticEllbetaPSF bugs |

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

### Multi-Method Temperature Mapping Pattern

When characterizing 2D temperature structure in extended X-ray sources (galaxy halos, cluster outskirts), use multiple independent methods with cross-validation:

**Method hierarchy (by S/N requirement)**:
1. **Full spectral fitting** (Sherpa/XSPEC APEC): Gold standard, needs ~2000 counts/region. Produces kT ± confidence. Slow (~5-10 min/region).
2. **5-band Poisson MLE**: Fits APEC model to counts in 5 energy bands simultaneously. Needs ~500 counts. Fast (~1s/region after pre-extraction). ~2% systematic vs spectral fitting.
3. **3-band color-color diagram**: C1=M/S, C2=H/M compared to APEC model track. Needs ~200 counts. Loses spatial information in global C-C plot — must bin spatially to show azimuthal variations.
4. **Hardness ratio (HR)**: HR=(H-S)/(H+S). Needs ~100 counts. **NOT reliable for direct kT calibration** — soft proton contamination dominates (SP flux ~9× source flux in hard band). Relative angular variations may be robust if SP is spatially uniform.

**Key pitfalls**:
- **HR→kT is NOT viable**: SP contamination in 2-5 keV band makes absolute HR→kT calibration unreliable. Only use HR for relative comparisons (e.g., N vs S at same radius).
- **3-band MLE is degenerate**: Need ≥5 bands to break kT-Z degeneracy. 3-band gives wrong kT for Z≠0.3 solar.
- **Background systematics are small**: Comparing 3B.background_20240601 vs 4.background for same regions: mean |ΔkT| = 0.007 keV (0.9%). Poor fit quality (rstat>2) is NOT caused by background choice.
- **Color-color diagram needs spatial binning**: A global C-C plot with all regions overlaid loses azimuthal information. Must label points by quadrant or create separate C-C plots per angular sector.
- **Adaptive bin MLE requires pre-extraction**: Extracting counts from event files per adaptive bin is too slow for subagent. Pre-extract all counts to JSON, then run MLE in pure Python.

**Cross-validation protocol**:
1. Compare 5-band MLE kT vs spectral fitting kT at overlapping regions (expect <5% difference)
2. Compare Chandra HR angular pattern vs XMM kT angular pattern (expect same sign, not same magnitude)
3. Compare different background datasets for same regions (expect <2% difference)
4. If methods disagree, diagnose: is it S/N, systematic, or physics?

**Real example (M104 CGM)**: 5-band MLE R4-6 NE=0.680 keV vs v18 spectral 0.669 keV (+1.6%); SE=0.780 vs 0.810 (-3.7%). Chandra HR confirms N+NE cooler than S+SE (4.3σ). Background systematics <0.02 keV.

## Proposal Upgrade Workflow Pattern

When a research project receives reviewer feedback on an observation proposal (SQUDE,XRISM AO, Chandra AO, etc.), use this systematic workflow to upgrade the proposal section:

### 7-Phase structure

1. **Phase 0 — Audit**: Locate proposal source (PDF/tex), reviewer documents, existing data products. Record trust levels for all current results.
2. **Phase 1 — Text cleanup**: Remove internal draft notes, fix false claims (frozen parameters ≠ measured, source-only ≠ realistic precision), restructure into reviewer-facing subsections.
3. **Phase 2 — Figure update**: Produce Chandra/high-res image with FoV overlay + PSF-smoothed panel + extraction regions. Dual output (1col + 2col).
4. **Phase 3 — PSF mixing quantification**: Compute leakage matrix from high-resolution image convolved with coarse PSF. Present as table in proposal.
5. **Phase 4 — Background/foreground robustness**: Design conservative bracket (Sim-0 source-only, Sim-1 nominal bg, Sim-2 high bg). Address O VII foreground for starburst/CGM targets.
6. **Phase 5 — Model-discrimination examples**: Prioritize: abundance pattern > DEM > kinematics > NEI. Each must map to a physical test, not just a measurement.
7. **Phase 6 — Feasibility table**: Region × purpose × counts × key lines × measurable params × dominant systematic.
8. **Phase 7 — Validation**: Syntax checks, plot inspection, cognition OS update (session + decisions + trust table).

### Key language rules

- **"baseline source-only statistical precision"** — never present simulation results without this label
- **"SQUDE can test CIE versus NEI"** — not "SQUDE will detect NEI"
- **"O/Fe, Ne/Fe, Mg/Fe"** — not He/C/N (those are frozen, not measured)
- **"phase-coupled vs phase-decoupled velocity"** — not absolute velocity (gain calibration floor)
- **O VII foreground caveat** — mandatory for any target with v < 500 km/s

### Reviewer-facing deliverables

- Revised proposal section with 7 subsections
- Updated figure with FoV overlay + HPD-smoothed panel + extraction regions
- PSF leakage matrix table
- Systematics paragraph (background, foreground O VII, PSF mixing, gain calibration)
- Feasibility matrix

### Verified example

M82 SQUDE proposal (2026-05-28): 7-phase upgrade completed in one session. Key corrections: removed 2 "yi" draft notes, fixed He/C/N overclaim, qualified kT precision, added leakage matrix (Central 82.7%, Wind ~67%), added O VII foreground caveat. See `~/Data/M82/SQUDE_response/M82_section_v2_draft.md` and `~/Data/M82/research-cognition-os/sessions/2026-05-28.md`.

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
| **Audit prompt → OS** (input) | Consume existing audit document to build OS | M31Center RGS CODEX_AUDIT_PROMPT.md |

Both patterns are valid. The OS is bidirectional — it can both consume and produce audit artifacts.

### Verified example

M31CGM Disk 0.7 keV study (2026-05-31): OS at `~/program/M31CGM/research-cognition-os/` was read (AI_BRIEFING + TRUST_TABLE + DECISION_LOG + S01 stage) and synthesized into a 9.5 KB audit prompt with 20 questions across 5 categories. The prompt included full model structure, current detection statistics (48/101 OBSIDs: 20 DET / 15 Weak / 13 UL), anomaly flagging (2 extreme norms, Srcabs.nH boundary issues), and specific methodological challenges (chi2gehrels vs C-stat, levmar convergence, error propagation from frozen halo params). Saved at `artifacts/codex_audit_prompt_2026-05-31.md`.

## Integration with llm-wiki

The cognition OS IS a wiki — it follows the same `SCHEMA.md + index.md + log.md` pattern as `llm-wiki`. When building a cognition OS:

1. Create `SCHEMA.md` with domain-specific tag taxonomy and trust classification rules
2. Create `index.md` listing all pages with trust status
3. Create `log.md` for action tracking
4. Use `[[wikilinks]]` between stages, insights, experiments, and bug_impacts for bidirectional navigation
5. The cognition OS should live at `<project-root>/research-cognition-os/`, NOT in `~/wiki/` (domain separation)

See also: [[llm-wiki]] for the full wiki maintenance workflow.

## Imaging-Based Project Pattern

When the project's primary data are **stacked X-ray images** (not spectra or simulations), the cognition OS structure differs from the spectral/simulation patterns above. Key differences:

- **Stages** track: data stacking → method development → quantitative analysis → cross-instrument validation
- **Insights** capture: band selection, PSF limits, method comparison, azimuthal asymmetry measurements
- **Experiments** are method comparisons (each image processing technique = one experiment)
- **Trust Table** tracks: stacked data quality, point source subtraction completeness, PSF FWHM constraint, azimuthal asymmetry significance

### Key Method: Azimuthal-Median + 4-Fold Stacking

For detecting bipolar extended structures (galactic winds, jets) in X-ray images:

1. Point source removal (detect in hard band, mask + inpaint)
2. Gaussian smooth (σ≈PSF)
3. **Azimuthal-median subtraction** at each radius (removes symmetric component)
4. **4-fold stacking** (fold 4 quadrants into Q1, boosts S/N ~2x)
5. Profile extraction: residual vs angle (0=disk, 90=wind)

**Critical pitfall**: Raw 4-fold stacking (without az-median subtraction) fails for centrally concentrated sources — the bright core floods all angles and drowns the extended signal. **Always subtract az-median first.**

See `references/xray-imaging-extended-structure-pattern.md` for the full algorithm, pitfalls, and NGC 3079 worked example.

## References

| File | Content |
|------|---------|
| `references/m82-squade-cognition-os-build.md` | M82 SQUDE cognition OS build: streamlined audit worked example for a small-medium research project (16 files, ~20 min). Shows right-sizing, template adjustments, and what file-tree-only reconstruction misses |
| `references/n132d-rgs-cognition-os-build.md` | N132D RGS cognition OS build: spectral-analysis pipeline pattern (no proposal/reviewers, insights from data products only, forward-looking current stage). 26 files in ~15 min |
| `references/xray-imaging-extended-structure-pattern.md` | Imaging-based project OS pattern: az-median+4fold method, stage/insight structure, trust table items, NGC 3079 worked example |
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
| `references/routine-os-sync-pattern.md` | Routine OS sync with latest AI sessions: lighter procedure than deep audit (15-30 min), diff-based gap filling, Claude Code --project flag workaround with leading-dash names, TES 星上算法 worked example |
| `references/cross-project-os-health-audit.md` | Cross-project OS health audit methodology: 6-minute fleet scan, health scoring matrix, remediation priorities, zero-OS project discovery, automation opportunities. 14-project empirical baseline from 2026-06-18 audit |
| `references/methodology-trust-negativity.md` | Empirical finding: methodology trust items are severely neglected across OS deployments (8/14 projects <5% coverage). Root cause analysis, fix patterns, automation check, and session-record evidence |
| `references/backtest-engine-silent-bugs.md` | Backtest engine silent bugs: 6 bugs found by agy-review in Fund Strategy project (datetime.date silent fallback, look-ahead bias, hardcoded hold_days, T+0 settlement, IC sign flip, survivorship bias). Prevention checklist. Applicable to any quantitative backtest engine |
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
