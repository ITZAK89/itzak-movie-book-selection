---
title: Everything Claude Code (ECC)
type: source-note
tags: [claude-code, agent-harness, hooks, skills, token-optimization]
created: 2026-05-20
updated: 2026-05-20
sources: [raw/affaan-meverything-claude-code The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond..md]
---

# Everything Claude Code (ECC)

182K+ star 的 Claude Code 插件，Anthropic Hackathon 获奖项目。定位为 **[[agent-harness|Agent harness]] 性能优化系统**，而非简单的配置文件合集。

## 四维架构

| 维度 | 数量 | 说明 |
|------|------|------|
| Skills | 231 | **主要工作流入口**，slash commands 正在向 skills 迁移 |
| Agents | 60 | 子代理委托，处理特定领域任务（code review、安全审计、build fix 等） |
| Hooks | 20+ 脚本 | 事件触发自动化：SessionStart、PreToolUse、PostToolUse、Stop 等 |
| Rules | 34 | 始终遵循的编码准则，分 common + 各语言（TypeScript、Python、Go 等） |

## 对我们有价值的部分

### Hooks 架构参考

ECC 的 hooks 分为几个关键事件类型，可以作为设计自己 hooks 的模板：

- **SessionStart**：加载上下文，注入项目状态（默认上限 8000 chars）
- **Stop**：保存会话状态，触发 pattern extraction
- **PreToolUse**：操作前检查（如 secrets 检测、tmux 提醒）
- **PostToolUse**：操作后自动处理（格式化、类型检查）
- **持续学习**：Stop hook 自动从会话中提取 pattern，保存为 instinct

Hook 运行时有分级控制：`ECC_HOOK_PROFILE=minimal|standard|strict`，可按需开关。

### Token 优化策略

```
model: sonnet (默认，60% 成本节省)
MAX_THINKING_TOKENS: 10000 (从 31999 降下来)
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: 50 (更早压缩，更好的长会话质量)
```

Opus 仅在复杂架构设计、深度调试时切换。

### Memory Persistence

通过 hooks 实现跨会话记忆：SessionStart 加载上次保存的上下文 → Stop 时保存新状态。这套机制和我们的 [[llm-wiki-building-guide|LLM Wiki]] 记忆系统互补。

## 架构决策

- Skills 是未来：新 workflow 开发优先放在 `skills/`，slash commands 仅维护兼容
- DRY adapter 模式：跨平台（Cursor、Codex、OpenCode）复用同一套 hook 脚本
- Plugin 安装 vs 手动安装：二选一，不要叠加

## 与我们项目的关联

ECC 的 hooks 架构直接指导我们设计自己的 Claude Code hooks（SessionStart → 展示 wiki 状态，Stop → 提示收录知识）。但不建议全量安装——太重，按需取用设计模式即可。
