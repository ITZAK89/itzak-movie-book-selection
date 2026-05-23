---
title: Freqtrade - 开源加密货币交易机器人
type: source-note
tags: [加密货币, 交易机器人, 开源, Python, 量化交易, 回测, 机器学习]
created: 2026-05-18
updated: 2026-05-18
sources: [raw/freqtradefreqtrade Free, open source crypto trading bot.md]
---

# Freqtrade - 开源加密货币交易机器人

## 概况

Freqtrade 是用 Python 编写的免费开源加密货币交易机器人。支持主流交易所，通过 Telegram 或 WebUI 操控，内置回测、图表和资金管理工具，以及基于机器学习的策略优化。

- **语言**：Python 3.11+
- **许可证**：AGPLv3（推测，未在原文中明确）
- **协议**：Telegram RPC + REST API + WebUI

## 核心功能

| 功能 | 说明 |
|------|------|
| **持久化** | 通过 SQLite 实现交易数据持久化 |
| **Dry-run** | 模拟交易模式，无需真实资金 |
| **回测 (Backtesting)** | 用历史数据模拟买卖策略表现 |
| **策略优化 (Hyperopt)** | 用机器学习在真实交易数据上优化策略参数 |
| **自适应建模 (FreqAI)** | 通过自适应机器学习方法，让策略自我训练以适应市场变化 |
| **白名单/黑名单** | 选择要交易的加密货币，或避开不想交易的币种 |
| **WebUI** | 内置 Web 管理界面 |
| **Telegram 控制** | 通过 Telegram Bot 远程管理 |
| **法币盈亏显示** | 以法币展示盈亏 |
| **性能报告** | 提供当前交易的状态报告 |

## 支持的交易所

### 现货
Binance、BingX、Bitget、Bitmart、Bybit、Gate.io、HTX、Hyperliquid (DEX)、Kraken、OKX 等。

### 合约
Binance、Bitget、Gate.io、Hyperliquid (DEX)、OKX、Bybit、Kraken。

社区已验证可用：Bitvavo、Kucoin。

## 快速开始

推荐 Docker 方式启动，详见 [Docker Quickstart](https://www.freqtrade.io/en/stable/docker_quickstart/)。

原生安装：

```
pip install freqtrade
```

最小硬件要求：2GB RAM、1GB 磁盘、2vCPU。依赖 Python >= 3.11、TA-Lib。推荐使用 Docker 部署。

## 核心命令

| 命令 | 用途 |
|------|------|
| `trade` | 启动实盘/模拟交易 |
| `backtesting` | 运行回测 |
| `backtesting-analysis` | 回测结果分析 |
| `hyperopt` | 机器学习策略参数优化 |
| `download-data` | 下载回测数据 |
| `plot-dataframe` | 绘制 K 线图与指标 |
| `plot-profit` | 生成盈亏图表 |
| `webserver` | 启动 Web 管理服务 |
| `list-strategies` | 列出可用策略 |
| `list-exchanges` | 列出可用交易所 |

## Telegram 远程命令

通过 Telegram Bot 控制机器人：

- `/start` / `/stop` — 启动/停止交易
- `/status` — 查看当前持仓
- `/profit [n]` — 查看近 n 天累计盈亏
- `/forceexit <trade_id>` — 强制平仓
- `/performance` — 按交易对分组展示表现
- `/balance` — 查看账户余额
- `/daily <n>` — 近 n 天每日盈亏

## 开发分支

- `stable` — 最新稳定版，经过充分测试
- `develop` — 新功能分支，可能有破坏性变更
- `feat/*` — 特定功能开发分支，请勿用于生产

提交 PR 需指向 `develop` 分支。

## 对 BTC 交易的可能用途

1. **策略回测**：在历史数据上验证 BTC 交易策略的可行性
2. **参数优化**：用 Hyperopt 自动优化策略的买入/卖出参数
3. **自适应策略**：用 FreqAI 训练能随市场变化的 ML 模型
4. **自动化执行**：策略验证后，通过 Telegram 或 WebUI 监控实盘运行

Freqtrade 可与 [[multi-agent-trading-framework|多智能体交易框架]] 配合：框架产出交易决策，Freqtrade 负责回测验证和实盘执行。如需整合多源数据（链上、宏观、情绪），可与 [[openbb|OpenBB]] 的数据层对接。
