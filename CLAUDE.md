# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Obsidian 个人知识管理 vault（第二大脑）。核心工作流围绕 LLM Wiki 知识库的持续建设（收录→体检→输出），投资追踪和项目管理为支撑模块。

## 权限约束

`.claude/settings.json` 限制了 Claude 可执行的操作：
- **允许的文件操作**：仅 `.md` 文件（Read, Write, Edit）
- **允许的 Bash 命令**：仅 `ls` 和 `find`
- 超出此范围的操作需要用户手动批准

## 目录结构

| 目录 | 用途 |
|------|------|
| `00-meta/` | 系统配置：用户档案 (`profile/`)、上下文提示词 (`system/context-prompt.md`) |
| `03-projects/` | 有明确截止日期的项目 |
| `04-areas/` | 持续维护的领域 |
| `04-areas/finance/` | 投资追踪：`btc-holdings.md`（持仓）、`cash-flow.md`（现金流）、`investment-plan.md`（投资计划） |
| `05-resources/` | 知识库，核心为 `llm-wiki/`（三步结构：raw → wiki → outputs） |
| `08-templates/` | 模板文件（仅 `daily-journal.md`，供 Obsidian 日记插件使用） |
| `临时/` | 临时工作目录（如 PPT 生成等一次性项目），含 `assets/` 子目录 |

## Obsidian 配置要点

- **附件路径**：`05-resources/llm-wiki/raw/assets`（所有粘贴的图片/文件存于此）
- **模板文件夹**：`08-templates/`
- **已启用的核心插件**：日记、模板、属性（Properties）、反向链接、标签面板、大纲、Canvas、书签、Sync
- **社区插件**：Marp Slides（将 Markdown 转为幻灯片）
- **Obsidian Sync**：已启用，笔记在多设备间同步

## 模板结构

创建新笔记时，必须匹配现有模板的 frontmatter 格式。

**日记** (`08-templates/daily-journal.md`)：
```yaml
---
date: {{date}}
---
```

## 笔记命名规范

**TIA（提阿非罗大人）视频笔记**：存放在 `04-areas/finance/`，命名格式 `TIA-YYYY-MM-DD-标题.md`。

当用户要求总结 author frontmatter 含"提阿非罗大人"的笔记时：
1. 总结内容追加到原笔记末尾（`## 总结` 分隔）
2. 若文件名尚未符合格式，重命名为 `TIA-{published日期}-原标题.md`

## 自定义命令

三个 slash 命令定义在 `.claude/commands/`：

- `/ingest` — 收录 raw/ 中新资料到 wiki：阅读 → 讨论要点 → 创建 wiki 页面 → 更新 index + log
- `/lint` — 体检 wiki 全库：扫描矛盾/过时/孤儿页面/缺失交叉引用，输出问题清单
- `/summary` — 总结当前对话，提取要点、概念、行动项，保存到 `05-resources/llm-wiki/outputs/`

## LLM Wiki 规范

`05-resources/llm-wiki/` 下的知识库由 AI 维护，完整规范见 `05-resources/llm-wiki/schema.md`。

核心工作流（由 `/ingest`、`/lint` 命令及日常对话驱动）：
- **收录** (`/ingest`)：阅读 `raw/` 中原始资料 → 讨论关键收获 → 创建 wiki 页面 → 更新索引和日志
- **查询** (对话中自然触发)：查 index.md → 读相关页面 → 综合回答 → 询问是否保存到 `outputs/`
- **体检** (`/lint`)：扫描 wiki 全部页面，检查矛盾、过时、孤儿页面、交叉引用缺失

页面命名英文小写+连字符，内容中文撰写，使用 Obsidian 兼容的 `[[wikilink]]` 语法。页面类型：`concept`、`entity`、`comparison`、`summary`、`source-note`。

## 用户背景

35岁+，韩国留学/经济管理专业，曾在京创业（IT/影院自助取票），有10年加密货币投资经历。当前无业，专注比特币投资和 AI 学习。年度目标：学习运用 AI、投资盈利 30-50 万 RMB。完整档案见 `00-meta/system/context-prompt.md`。

## Obsidian CLI

与 Obsidian vault 交互时，优先通过 `obsidian` CLI 命令操作（需 Obsidian 打开），而非直接读写文件。详见 skill `obsidian-cli`。

使用约定：
1. **优先使用 obsidian CLI**：所有笔记的读取、创建、搜索、属性修改、标签查询等操作，优先调用 `obsidian` 命令
2. **默认 silent**：所有命令默认加上 `silent` 参数（避免前台打开文件），除非用户明确要求在前台打开
3. **标签搜索优先 obsidian tags**：标签查找优先使用 `obsidian tags` 命令（直接命中 Obsidian 元数据），比全文 `grep` 更精确

## 编码行为准则

以下准则偏重谨慎而非速度。对简单任务可灵活判断。

### 1. 先思考再编码

**不要假设，不要隐藏困惑，主动暴露权衡。**

在实现之前：
- 明确陈述你的假设。如果不确定，询问。
- 如果存在多种理解，呈现它们——不要沉默地选择一种。
- 如果有更简单的方法，说出来。有理有据地推回不合理的需求。
- 如果有不清楚的地方，停下来。说出困惑之处。询问。

### 2. 提案先行

**任何会产生输出或副作用的操作，先给方案再动手。**

适用场景：修改文件、创建文件、生成内容（如 /summary 等命令的输出）、执行有副作用的 shell 命令、git 操作等。纯只读操作（搜索、读取、浏览）不需要。

- 先用简洁的语言描述你打算怎么做
- 说明为什么选择这个方案（尤其是存在替代方案时）
- 涉及多文件时，列出受影响文件及改动范围
- 等待用户确认后再实施

简单的单行修复（拼写错误、格式修正）可以跳过此步骤。

### 3. 简单优先

**用最少的代码解决问题。不要做推测性开发。**

- 不添加超出需求的功能。
- 不为单次使用的代码创建抽象。
- 不添加未被请求的"灵活性"或"可配置性"。
- 不为不可能发生的场景添加错误处理。
- 如果你写了 200 行而 50 行就能解决，重写。

问自己："资深工程师会说这过度复杂吗？" 如果是，简化。

### 4. 精准修改

**只动你必须改的。只清理你自己的烂摊子。**

编辑现有代码时：
- 不要"顺手改进"相邻代码、注释或格式。
- 不要重构没坏的东西。
- 匹配现有风格，即使你觉得它不好。
- 如果你注意到无关的死代码，提出来——不要直接删。

当你的修改产生孤儿代码时：
- 移除因你的修改而不再使用的导入/变量/函数。
- 不要删除修改之前就已存在的死代码，除非被要求。

### 5. 目标驱动执行

**定义成功标准。循环直到验证通过。**

将任务转化为可验证的目标：
- "添加验证" → "为无效输入编写测试，然后让测试通过"
- "修复 bug" → "编写复现 bug 的测试，然后让测试通过"
- "重构 X" → "确保重构前后测试全部通过"

对多步骤任务，先陈述简要计划，每一步配一个验证检查点。
