---
title: Agent Harness（智能体运行时）
type: concept
tags: [agent, claude-code, hooks, skills, automation]
created: 2026-05-20
updated: 2026-05-20
sources: [wiki/everything-claude-code.md]
---

# Agent Harness（智能体运行时）

Agent Harness 是管理和优化 AI 编程助手（如 Claude Code）行为的**运行时系统**。它不是 Agent 本身，而是 Agent 运行在其中的"操作系统"——提供 Skills、Hooks、Rules、Memory 等基础设施。

## 四个核心组件

| 组件 | 角色 | 类比 |
|------|------|------|
| **Skills** | 可复用的工作流定义 | 函数库 |
| **Hooks** | 事件驱动的自动化触发器 | 生命周期回调 |
| **Rules** | 始终生效的行为准则 | 类型系统 / lint 规则 |
| **Agents** | 专门化的子任务处理单元 | 微服务 |

## 关键设计原则

### Skills 优先于 Commands

Skills 是声明式的、可被 Agent 自动发现和推荐的工作流定义。Commands 是命令式的、需要用户主动调用。趋势是 Skills 取代 Commands 成为主要交互入口。

我们的 `/ingest`、`/lint` 命令目前是 command 形式，未来可以演进为 skill。

### Hooks 作为自动化基础设施

Hooks 在工具调用生命周期中插入自动化逻辑：

```
SessionStart → 加载上下文、展示状态
PreToolUse  → 校验、提醒、拦截
PostToolUse → 格式化、同步、记录
Stop        → 保存状态、提取 pattern
```

### Token 预算意识

Agent harness 需要管理 token 消耗：默认用轻量模型、控制 thinking tokens、在合适的时机压缩上下文。这直接影响使用成本。

## 对我们的意义

我们的 Claude Code 配置（CLAUDE.md + settings.json + commands + hooks）本质上就是一个轻量级的 Agent Harness。理解这个框架有助于：

- 设计合理的 hooks 事件链
- 决定哪些流程用 skill、哪些用 command
- 管理上下文窗口和 token 预算
