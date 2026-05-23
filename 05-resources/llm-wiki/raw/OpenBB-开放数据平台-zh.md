---
title: "OpenBB 开放数据平台：面向分析师、量化交易员和 AI 智能体的金融数据平台"
source: "https://github.com/OpenBB-finance/OpenBB"
created: 2026-05-18
description: "面向分析师、量化交易员和 AI 智能体的金融数据平台"
tags:
  - "clippings"
  - "金融数据"
  - "开源"
  - "AI智能体"
---

[![Open Data Platform by OpenBB logo](https://github.com/OpenBB-finance/OpenBB/raw/develop/images/odp-dark.svg?raw=true#gh-dark-mode-only)](https://github.com/OpenBB-finance/OpenBB/blob/develop/images/odp-dark.svg?raw=true#gh-dark-mode-only)

OpenBB 开放数据平台（ODP）是一套开源工具集，帮助数据工程师将自有数据、授权数据和公共数据源整合到下游应用中，如 AI 智能助手和研究仪表盘。

ODP 充当"一次接入，随处消费"的基础设施层，将数据统一整合并同时暴露到多个终端：面向量化交易员的 Python 环境、面向分析师的 OpenBB Workspace 和 Excel、面向 AI 智能体的 MCP 服务器，以及面向其他应用的 REST API。

[![Logo](https://camo.githubusercontent.com/a3fd1d9d5a13e0dcb0d83b89dcbfbfab38371622bd86c0e9629e6145ada8cb13/68747470733a2f2f6f70656e62622d636d732e64697265637475732e6170702f6173736574732f37306239373165662d376137652d343836652d623561652d3163633630326632313632632e706e67)](https://pro.openbb.co/)

快速开始：`pip install openbb`

```
from openbb import obb
output = obb.equity.price.historical("AAPL")
df = output.to_dataframe()
```

可用的数据集成详见：[https://docs.openbb.co/python/reference](https://docs.openbb.co/python/reference)

---

## OpenBB Workspace

开放数据平台提供开源的数据集成基础，而 **OpenBB Workspace** 则提供面向分析师的企业级 UI，用于可视化数据集并利用 AI 智能体。平台"一次接入，随处消费"的架构实现了两者之间的无缝集成。

你可以在 [https://pro.openbb.co](https://pro.openbb.co/) 访问 OpenBB Workspace。

数据集成：

- 有关向 OpenBB Workspace 添加数据的更多信息，请参阅[文档](https://docs.openbb.co/workspace)或[此后端开源仓库](https://github.com/OpenBB-finance/backends-for-openbb)。

AI 智能体集成：

- 有关向 OpenBB Workspace 添加 AI 智能体的更多信息，请参阅[此智能体开源仓库](https://github.com/OpenBB-finance/agents-for-openbb)。

### 将开放数据平台接入 OpenBB Workspace

在 Python（3.9.21 - 3.12）环境中，通过几个简单命令即可将此库连接到 OpenBB Workspace。

#### 运行 ODP 后端

- 安装依赖包。
```
pip install "openbb[all]"
```
- 在本地启动 API 服务器。
```
openbb-api
```

这将通过 Uvicorn 在 `127.0.0.1:6900` 启动一个 FastAPI 服务器。

你可以访问 [http://127.0.0.1:6900](http://127.0.0.1:6900/) 验证是否运行成功。

#### 将 ODP 后端接入 OpenBB Workspace

登录 [OpenBB Workspace](https://pro.openbb.co/)，按以下步骤操作：

1. 进入 "Apps" 标签页
2. 点击 "Connect backend"
3. 填写表单：名称填写 Open Data Platform，URL 填写 [http://127.0.0.1:6900](http://127.0.0.1:6900/)
4. 点击 "Test"，应显示 "Test successful" 并显示发现的 app 数量
5. 点击 "Add"

完成。

---

## 目录

1. [安装](#1-安装)
2. [贡献](#2-贡献)
3. [许可证](#3-许可证)
4. [免责声明](#4-免责声明)
5. [联系方式](#5-联系方式)
6. [Star 历史](#6-star-历史)
7. [贡献者](#7-贡献者)

## 1. 安装

ODP Python 包可以从 [PyPI](https://pypi.org/project/openbb/) 安装：

```
pip install openbb
```

或直接从仓库克隆：

```
git clone https://github.com/OpenBB-finance/OpenBB.git
```

更多安装信息请参阅 [OpenBB 文档](https://docs.openbb.co/python/installation)。

### ODP CLI 安装

ODP CLI 是一个命令行工具，可直接从命令行访问 ODP。

安装方式：

```
pip install openbb-cli
```

或直接从仓库克隆：

```
git clone https://github.com/OpenBB-finance/OpenBB.git
```

更多安装信息请参阅 [OpenBB 文档](https://docs.openbb.co/cli/installation)。

## 2. 贡献

参与该项目有三种主要方式（希望你已给项目点了 Star ⭐️）。

### 成为贡献者

- 更多信息见[开发者文档](https://docs.openbb.co/python/developer)。

### 创建 GitHub 工单

创建工单前，请确认你要提交的问题在[已有 issues](https://github.com/OpenBB-finance/OpenBB/issues) 中不存在。

- [报告 Bug](https://github.com/OpenBB-finance/OpenBB/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBug%5D)
- [建议改进](https://github.com/OpenBB-finance/OpenBB/issues/new?assignees=&labels=enhancement&template=enhancement.md&title=%5BIMPROVE%5D)
- [请求新功能](https://github.com/OpenBB-finance/OpenBB/issues/new?assignees=&labels=new+feature&template=feature_request.md&title=%5BFR%5D)

### 提供反馈

我们在 [Discord](https://openbb.co/discord) 上最活跃，也欢迎通过[其他社交平台](https://openbb.co/links)与我们联系。

## 3. 许可证

基于 AGPLv3 许可证分发。详见 [LICENSE](https://github.com/OpenBB-finance/OpenBB/blob/main/LICENSE)。

## 4. 免责声明

金融工具交易涉及高风险，包括可能损失部分或全部投资金额的风险，并非适合所有投资者。

在决定交易金融工具之前，应充分了解金融市场交易相关的风险和成本，仔细考虑你的投资目标、经验水平和风险承受能力，并在必要时寻求专业建议。

开放数据平台中包含的数据未必准确。

OpenBB 及本网站所含数据的任何提供方，均不对因你的交易或依赖所展示信息而产生的任何损失或损害承担责任。

本网站、产品或文档中可能引用的第三方名称、标志和品牌均为其各自所有者的商标。除非另有说明，OpenBB 及其产品和服务未获这些第三方认可、赞助或关联。

我们使用这些名称、标志和品牌仅出于识别目的，并不暗示任何此类认可、赞助或关联。

## 5. 联系方式

如有关于平台或 OpenBB 的任何问题，欢迎发送邮件至 `support@openbb.co`

如需问候或有意与我们合作，欢迎联系 `hello@openbb.co`

任何社交媒体平台：[openbb.co/links](https://openbb.co/links)

## 6. Star 历史

这是我们增长的见证，一切才刚刚开始。

更多我们关注的数据指标，请访问 [openbb.co/open](https://openbb.co/open)。

[![Star History Chart](https://camo.githubusercontent.com/17bcc77a81b74e439926d82e406fa1602742219e72ff0e3c34f89f339345d359/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d6f70656e62622d66696e616e63652f4f70656e424226747970653d44617465267468656d653d6461726b)](https://api.star-history.com/svg?repos=openbb-finance/OpenBB&type=Date&theme=dark)

## 7. 贡献者

没有你们就没有 OpenBB。如果我们想要颠覆金融行业，每一份贡献都至关重要。感谢你们成为这段旅程的一部分。

[![](https://camo.githubusercontent.com/5a28c87a8563a6db7157ecd2524d570dda419452ba66711de174914125bf8eb4/68747470733a2f2f636f6e7472696275746f72732d696d672e7765622e6170702f696d6167653f7265706f3d4f70656e42422d66696e616e63652f4f70656e4242)](https://github.com/OpenBB-finance/OpenBB/graphs/contributors)
