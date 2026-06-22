# Session 记录形式化 — Pitfalls & 经验教训

从 2026-06-18 对 14 个项目的 57 个 session 文件的审计与修复中总结。

## 审计发现

| 问题 | 数量 | 严重度 |
|------|------|--------|
| YAML frontmatter 缺失 | 50/57 | 高 |
| Section header 大小写不一致 | 全部 | 中 |
| Section 缺失（Found/Next） | 多个 | 中 |
| Bullet 格式不统一（编号列表 vs bullet） | 多个 | 低 |
| 无 Related 部分（wikilink 到 stages/experiments/insights） | 绝大多数 | 低 |

## Pitfall 1: Section header 大小写匹配导致 linter 清空文件内容

**根因**：实际 session 文件中使用 `## DID`/`## FOUND`/`## NEXT`（大写），但 linter 正则写为 `^## (Did|Found|Next|Related)`（首字母大写）。Python `re.MULTILINE` 下 `^` 锚点正确，但 `Did` 不匹配 `DID`，导致 `extract_sections` 返回空字典。

**后果**：`ensure_bullets` 收到空字符串 → 输出 `- ...` → 原内容被清空，所有 session 文件变成只有 placeholder 的空模板。

**修复**：正则改为 `^## (DID|FOUND|NEXT|Related)`，匹配实际文件中的大写 header。

**教训**：**任何解析 section header 的代码都必须兼容大小写**。不要假设用户会按模板的精确大小写写 header。在 extract_sections 中同时匹配大小写变体，或在匹配后统一 lower() 处理。

## Pitfall 2: Frontmatter 重建时丢失 `---` 分隔符

**根因**：`extract_frontmatter_and_body` 返回的是 frontmatter 的**内容**（不含 `---` 分隔符），但 `fix_session` 在重建时直接 `f'{fm}\n\n{body}'`，丢失了 `---` 包裹。

**修复**：区分两种情况：
- 新建 frontmatter（`make_frontmatter` 已包含 `---`）→ 直接拼接
- 提取的已有 frontmatter（不含 `---`）→ 用 `f'---\n{fm}\n---\n\n{body}'` 包裹

## Pitfall 3: `find` 命令的 maxdepth 限制

**根因**：`find /home/huangrui -type d -name 'research-cognition-os'` 在某些配置下可能受默认 maxdepth 限制，导致找不到深层目录（如 `program/DET_ML_Uncertainty/research-cognition-os`）。

**修复**：显式指定 `-maxdepth 6` 或更高，或使用 `find /home/huangrui/program/*/research-cognition-os` 的 glob 模式作为后备。

## Linter 使用指南

```bash
# 检查单个项目（不修复）
python scripts/session_linter.py --path /path/to/project/research-cognition-os

# 修复单个项目
python scripts/session_linter.py --fix --path /path/to/project/research-cognition-os

# 修复所有项目
for d in /home/huangrui/program/*/research-cognition-os /home/huangrui/Data/*/research-cognition-os; do
  [ -d "$d/sessions" ] && python scripts/session_linter.py --fix --path "$d"
done
```

## 强制规范

1. **YAML frontmatter 必需**：type, status, created, tags
2. **三个 section 必需**：Did, Found, Next
3. **Bullet 格式强制**：每个条目以 `- ` 开头
4. **Related 推荐**：链接到相关 stage/experiment/insight
5. **Section header 大小写**：推荐 `## Did`/`## Found`/`## Next`（首字母大写），但 linter 兼容大写变体