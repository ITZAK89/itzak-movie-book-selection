---
title: OpenBB 开放数据平台
type: source-note
tags: [金融数据, 开源, Python, AI智能体, MCP, 量化交易]
created: 2026-05-18
updated: 2026-05-18
sources: [raw/OpenBB-开放数据平台-zh.md]
---

# OpenBB 开放数据平台

## 概况

OpenBB ODP（Open Data Platform）是一套开源工具集，解决金融数据工程的核心问题：如何把自有的、授权的、公共的数据源整合起来，统一喂给下游应用。

- **许可证**：AGPLv3
- **安装**：`pip install openbb`
- **架构理念**："接一次，到处用"

## 四类消费终端

| 终端 | 面向用户 | 用途 |
|------|----------|------|
| **Python SDK** | 量化交易员 | `from openbb import obb` → 直接调数据 |
| **OpenBB Workspace** | 分析师 | 企业级 UI，可视化数据 + AI Agent |
| **MCP 服务器** | AI 智能体 | 让 Claude/GPT 直接调用金融数据 |
| **REST API** | 其他应用 | HTTP 接口，数据接入任意系统 |

## 快速开始

```python
from openbb import obb

# 拉取 Apple 历史价格
output = obb.equity.price.historical("AAPL")
df = output.to_dataframe()
```

## 与 [[freqtrade|Freqtrade]] 的关系

[[freqtrade|Freqtrade]] 是**策略执行**层，OpenBB 是**数据**层：

```
OpenBB (数据整合) → 多源数据 → Freqtrade (回测/执行)
```

当前你的 Freqtrade 通过 ccxt 直接从 Binance 拉数据，够用。但如果未来需要整合链上数据、宏观指标、情绪数据等多源信息，OpenBB 的"一次接入"架构就有意义了。

## MCP 集成

OpenBB 支持 MCP（Model Context Protocol），意味着 AI Agent 可以直连金融数据。这和 Claude Code 生态有潜在整合空间——未来你的 Claude Code [[agent-harness|Agent]] 可以直接调 OpenBB 拉数据跑分析。

## 本地部署到 Workspace

1. `pip install "openbb[all]"`
2. `openbb-api`（在 localhost:6900 启动 FastAPI 服务器）
3. 在 Workspace → Apps → Connect backend → 填入 URL → Test → Add
