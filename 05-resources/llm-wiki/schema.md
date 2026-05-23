---
area: llm-wiki
type: schema
created: 2026-05-15
updated: 2026-05-22
---

# LLM Wiki 维护规范

本文档告诉 Claude Code 如何维护 `05-resources/llm-wiki/` 下的知识库。

## 目录结构

```
05-resources/llm-wiki/
├── schema.md          ← 本文件：LLM 维护规范
├── overview.md        ← LLM Wiki 概念说明
├── index.md           ← wiki 全部页面索引
├── log.md             ← 操作日志（按时间）
├── raw/               ← 第一步：原始资料（论文、文章、视频笔记等）
│   ├── papers/
│   └── articles/
├── wiki/              ← 第二步：AI 整理好的结构化知识文章
│   ├── transformer.md
│   ├── gpt-series.md
│   └── ...
└── outputs/           ← 第三步：AI 生成的报告、分析、草稿
```

## 页面命名规范

- 文件名使用英文小写 + 连字符，如 `attention-mechanism.md`、`gpt-4.md`
- 页面标题（H1）使用中文，如 `# 注意力机制`
- 每个页面开头必须有 YAML frontmatter：
  ```yaml
  ---
  title: 中文标题
  type: concept | entity | comparison | summary | source-note
  tags: [tag1, tag2]
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  sources: [引用 raw/ 中的源文件路径]
  ---
  ```

## 页面类型

| type | 用途 | 示例 |
|------|------|------|
| `concept` | 解释一个概念/技术 | 注意力机制、Transformer 架构、RLHF |
| `entity` | 描述一个具体模型/产品/人物 | GPT-4、Claude Sonnet、Andrej Karpathy |
| `comparison` | 对比多个事物 | GPT-4 vs Claude、RAG vs 微调 |
| `summary` | 某主题的综合综述 | LLM 发展简史、2024 AI 趋势 |
| `source-note` | 单篇原始资料的阅读笔记 | Attention Is All You Need 论文笔记 |

## 收录工作流 (Ingest)

当用户说"收录"或"把这篇文章加入 wiki"时：

1. 阅读 raw/ 中对应的原始资料
2. 和用户简短讨论关键收获（3-5 句）
3. 在 wiki/ 下创建或更新 `source-note` 页面（阅读笔记）
4. 识别资料涉及的概念和实体，创建或更新对应的 wiki 页面
5. 更新 index.md 中受影响的条目
6. 在 log.md 末尾追加操作记录，格式：`## [日期] 收录 | 资料名称`
7. 告知用户共更新了哪些页面

## 查询工作流 (Query)

当用户以 wiki 内容提问时：

1. 先读 index.md 定位相关页面
2. 读取相关页面内容
3. 综合回答，引用具体页面作为来源
4. 如果答案有价值，询问用户是否将其保存到 outputs/ 下

## 体检工作流 (Lint)

当用户说"体检"或"检查 wiki"时：

1. 扫描 wiki/ 下所有页面
2. 检查：矛盾论断、过时信息、孤儿页面（无入链）、缺失页面（提到但不存在）、交叉引用遗漏
3. **跨目录关联检查**：扫描 `03-projects/` 和 `05-resources/llm-wiki/outputs/`，识别主题相同或高度重叠但未通过 `[[wikilink]]` 互链的笔记对。主题匹配以标题关键词和正文核心术语为准，不要求精确标题一致
4. 列出问题清单，逐项询问是否修复

## 写作风格

- 所有内容使用中文，技术术语可中英对照
- 简洁直接，每个页面 200-800 字
- 善用表格和列表提高可读性
- 关键概念首次出现时标注英文原名，如"注意力机制（Attention Mechanism）"
- 页面之间使用 `[[页面文件名]]` 建立内部链接（Obsidian 兼容）
