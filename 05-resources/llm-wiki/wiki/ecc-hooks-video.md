---
title: ECC 系列：Hook 系统详解
type: source-note
tags: [claude-code, hooks, automation, memory, ECC]
created: 2026-05-20
updated: 2026-05-20
sources: [raw/ECC助claude code自己管理自己-hook.md]
---

# ECC 系列：Hook 系统详解

B站 ECC 系列教程 Hook 专集，讲解 Claude Code 的 Hook 系统——六种生命周期事件，以及如何用它们实现自动化、质量保证和跨会话连续性。

## 六种 Hook 生命周期

| Hook | 触发时机 | 用途 |
|------|---------|------|
| **PreToolUse** | Claude 执行操作前 | 安全校验、操作拦截（如禁止删除受保护文件） |
| **PostToolUse** | 操作执行完成后 | 自动收尾（格式化、类型检查） |
| **UserPromptSubmit** | 用户敲回车提交 prompt 时 | 注入额外上下文，帮 Claude 更好理解意图 |
| **Stop** | 工作停止 / 会话结束时 | 格式化 + 类型检查 + 测试 + 经验记录 |
| **PreCompact** | 上下文即将压缩前 | 保存关键状态，防止压缩丢失信息 |
| **SessionStart** | 新会话启动时 | 加载偏好设置、记忆文件、项目配置 |

## Stop Hook：最实用的 Hook

视频重点推荐，自动执行四件事：
1. **代码格式化**：统一风格
2. **类型检查**：防止引入类型错误
3. **单元测试**：自动跑修改模块的测试
4. **经验记录**：分析刚才做的事，保存可复用模式（持续学习的底层触发机制）

## Memory Persistence：三 Hook 协作

PreCompact + Stop + SessionStart 组合实现跨会话连续性：
- PreCompact 在压缩前保存工作状态
- Stop 将经验写入记忆文件
- SessionStart 在下一次打开时自动加载

视频称这是"真正的连续性"——今天做到一半的工作，明天打开直接接上。

## Hookify：自然语言生成 Hook

用自然语言描述需求（如"每次写文件时检查 console.log"），自动生成对应 Hook 配置 JSON，覆盖 80% 日常需求，降低配置门槛。

## 与我们项目的对照

我们已在 `.claude/settings.json` 中配置了 SessionStart、Stop、PreCompact 三种 hook。但实际使用中发现：

- **Stop Hook 的"四件事"对纯 Markdown 项目不适用**——没有代码要格式化、没有类型要检查、没有测试要跑。唯一可适配的"经验记录"需要 AI 判断力，超出 shell hook 能力。
- **PreCompact "保存关键状态"被视频理想化**——shell hook 只能写时间戳，做不到智能提取重要上下文。这是我们之前讨论中确认的根本矛盾。
- **SessionStart 加载记忆**是我们唯一用上的功能，但当前 session-state.md 内容太弱。

视频的 Hook 设计模式对**代码项目**更实用；对本 vault（纯 Markdown 知识管理）需要做减法，而非照搬。

## 关键洞察

视频的 Memory Persistence 策略和我们在 [[agent-harness|Agent Harness]] 中讨论的 hooks 设计一脉相承。但视频避而不谈"shell hook 的能力边界"——这恰好是我们实践中最核心的限制。
