---
title: Prompt as Code（提示词工程化）
type: source-note
tags: [prompt-engineering, gpt-image, agent, structured-output]
created: 2026-05-20
updated: 2026-05-20
sources: [raw/freestyleflyawesome-gpt-image-2 Prompt as Code  GPT-Image2 工业级提示词引擎与模板库，370+ 个案例逆向工程，20+ 套工业级模板，并提炼出Skills，持续更新中.md]
---

# Prompt as Code（提示词工程化）

来自 awesome-gpt-image-2 项目的核心方法论：将"散文式提示词"压缩成"结构化协议"，面向 Agent 和自动化工作流而非人肉复制粘贴。

## 核心思想

AI 画图经历了从"能不能出图"到"能不能稳定、可控、可复用地出图"的转变。Prompt as Code 的答案是：**把散乱的自然语言提示词整理成结构化的、可版本控制、可组合的资产。**

## 三层架构

1. **原子化 Schema**：将视觉要素（主体、光影、材质、排版、色彩）拆成独立组件，像代码模块一样组合
2. **工业级模板**：20+ 套按场景分类的模板（UI、信息图、海报、电商、品牌、摄影等）
3. **Agent Skill**：同一份风格库数据同时服务于网站浏览和 Agent API 调用

## 370+ 案例分类

| 类别 | 案例数 | 典型场景 |
|------|--------|---------|
| UI 与界面 | 68 | App、网页、仪表盘、社媒截图 |
| 图表与信息可视化 | 55 | 信息图、知识图谱、技术图解 |
| 海报与排版 | 71 | 活动海报、封面、字体设计 |
| 商品与电商 | 24 | 商品图、详情页、卖点广告 |
| 摄影与写实 | 34 | 人像、纪实、胶片质感 |
| 其他（插画、建筑、角色、场景、古风等） | 126+ | 覆盖 7 个细分领域 |

## 三步使用法

1. 从案例画廊找到目标视觉类型
2. 抄结构，不抄风格词——理解模板的逻辑而非复制词汇
3. 把业务变量填入通用模板

## 与 LLM Wiki 的关联

Prompt as Code 和 LLM Wiki 共享同一理念：**把一次性产物变成持续复利的资产。** LLM Wiki 将对话中的知识结构化存储，Prompt as Code 将提示词从"每次重新想"变成"模板化调用"。两者都是"编译一次，持续使用"的模式。

该项目提供了可直接安装的 Claude Code Agent Skill：`npx skills add freestylefly/awesome-gpt-image-2`
