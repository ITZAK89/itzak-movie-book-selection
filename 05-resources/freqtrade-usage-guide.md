---
title: Freqtrade 使用指南
type: reference
tags: [freqtrade, 回测, 量化交易, BTC, docker]
created: 2026-05-18
---

# Freqtrade 使用指南

## 前置条件

Docker Desktop 保持运行状态（菜单栏有鲸鱼图标，左下角显示绿色 Running）。

## 文件结构

```
~/freqtrade/
├── config.json                         ← 入口配置（docker compose 自动读取）
├── docker-compose.yml                 ← 简化命令配置
└── user_data/
    ├── config/config.json              ← 主配置文件
    ├── data/binance/                   ← 下载的 K 线数据
    ├── strategies/sample_btc.py        ← 交易策略
    ├── strategies/sample_btc.json      ← Hyperopt 优化结果（存在时会自动加载）
    ├── backtest_results/               ← 回测结果
    └── hyperopt_results/               ← Hyperopt 结果
```

## 短命令 (docker compose)

在 `~/freqtrade/` 目录下执行：

### 回测

```bash
cd ~/freqtrade
docker compose run --rm freqtrade backtesting --strategy SampleBTC --timerange 20170817-20260518
```

### Hyperopt (优化止损和出场规则)

```bash
cd ~/freqtrade
docker compose run --rm freqtrade hyperopt --strategy SampleBTC --hyperopt-loss SharpeHyperOptLoss --epochs 500 --timerange 20170817-20240101 --spaces roi stoploss
```

### 下载数据

```bash
cd ~/freqtrade
docker compose run --rm freqtrade download-data --exchange binance --pairs BTC/USDT --timeframes 5m --timerange 20240101-20260518
```

### 查看可用交易所

```bash
cd ~/freqtrade
docker compose run --rm freqtrade list-exchanges
```

### 查看已下载数据

```bash
cd ~/freqtrade
docker compose run --rm freqtrade list-data --exchange binance
```

### 绘制 K 线图（含指标）

```bash
cd ~/freqtrade
docker compose run --rm freqtrade plot-dataframe --strategy SampleBTC --pairs BTC/USDT --timerange 20260101-20260518
```

---

## 新建策略与回测

### 1. 创建策略文件

在 `~/freqtrade/user_data/strategies/` 下创建 `.py` 文件，文件名与类名一致。

```python
# ~/freqtrade/user_data/strategies/my_new_strategy.py
from pandas import DataFrame
import talib.abstract as ta
from freqtrade.strategy import IStrategy

class MyNewStrategy(IStrategy):
    timeframe = "1d"
    minimal_roi = {"0": 100}
    stoploss = -0.10

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 在此计算所需的技术指标
        dataframe["ema10"] = ta.EMA(dataframe, timeperiod=10)
        dataframe["sma50"] = ta.SMA(dataframe, timeperiod=50)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 入场条件
        dataframe.loc[
            (dataframe["rsi"] < 30),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 离场条件
        dataframe.loc[
            (dataframe["rsi"] > 70),
            "exit_long",
        ] = 1
        return dataframe
```

### 2. 回测

```bash
cd ~/freqtrade
docker compose run --rm freqtrade backtesting --strategy MyNewStrategy --timerange 20170817-20260518
```

`--strategy` 填类名即可（与 `.py` 文件名去掉后缀一致），Freqtrade 自动从 `strategies/` 目录找到对应文件。

### 3. Hyperopt 优化

策略中如有可优化参数（如 `buy_rsi = IntParameter(20, 40, default=30)`），可用 `--spaces buy sell` 优化。如果只想优化止损和出场规则，用 `--spaces roi stoploss`。

```bash
cd ~/freqtrade
docker compose run --rm freqtrade hyperopt --strategy MyNewStrategy --hyperopt-loss SharpeHyperOptLoss --epochs 500 --timerange 20170817-20240101 --spaces roi stoploss
```

### 4. 多策略并存

`strategies/` 目录下可以有任意多个 `.py` 文件，互不影响：

```
strategies/
├── sample_btc.py          ← 均线交叉策略
├── my_new_strategy.py     ← RSI 超卖策略
└── agent_seil_strategy.py ← 多智能体分析策略
```

通过 `--strategy` 指定要回测哪一个即可。

> **注意**：Hyperopt 优化结果会保存为与策略同名的 `.json` 文件（如 `MyNewStrategy.json`）。下次回测同策略时 Freqtrade 会自动加载该优化参数。如需使用策略原始参数，删除对应的 `.json` 文件即可。

---

## 原始命令 (docker run)

不依赖 docker-compose.yml，可以在任意目录执行：

### 回测

```bash
docker run --rm \
  -v ~/freqtrade/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable \
  backtesting \
  --config /freqtrade/user_data/config/config.json \
  --strategy SampleBTC \
  --timerange 20170817-20260518
```

### Hyperopt (优化止损和出场规则)

```bash
docker run --rm \
  -v ~/freqtrade/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable \
  hyperopt \
  --config /freqtrade/user_data/config/config.json \
  --strategy SampleBTC \
  --hyperopt-loss SharpeHyperOptLoss \
  --epochs 500 \
  --timerange 20170817-20240101 \
  --spaces roi stoploss
```

### 下载数据

```bash
docker run --rm \
  -v ~/freqtrade/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable \
  download-data \
  --exchange binance \
  --pairs BTC/USDT \
  --timeframes 5m \
  --timerange 20240101-20260518
```

### 查看可用交易所

```bash
docker run --rm \
  -v ~/freqtrade/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable \
  list-exchanges
```

### 查看已下载数据

```bash
docker run --rm \
  -v ~/freqtrade/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable \
  list-data \
  --exchange binance
```

### 绘制 K 线图（含指标）

```bash
docker run --rm \
  -v ~/freqtrade/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable \
  plot-dataframe \
  --config /freqtrade/user_data/config/config.json \
  --strategy SampleBTC \
  --pairs BTC/USDT \
  --timerange 20260101-20260518
```

---

## 可用指标库与文档

Freqtrade 内置两个指标库，策略中可直接导入使用。

### TA-Lib（150+ 指标）

```python
import talib.abstract as ta

dataframe["sma"] = ta.SMA(dataframe, timeperiod=50)
dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
```

官网函数列表：https://ta-lib.org/functions/

常用指标速查：

| 类别 | 指标 | 用法 |
|------|------|------|
| 趋势 | SMA, EMA, WMA, DEMA, TEMA, KAMA | `ta.EMA(dataframe, timeperiod=10)` |
| 趋势 | MACD | `ta.MACD(dataframe)` 返回 macd/signal/hist 三列 |
| 趋势 | ADX (趋势强度) | `ta.ADX(dataframe, timeperiod=14)` |
| 动量 | RSI | `ta.RSI(dataframe, timeperiod=14)` |
| 动量 | MFI, CCI, WILLR, STOCH, MOM, ROC | `ta.MFI(dataframe, timeperiod=14)` |
| 波动率 | BBANDS (布林带) | `ta.BBANDS(dataframe)` 返回 upper/middle/lower |
| 波动率 | ATR (真实波幅) | `ta.ATR(dataframe, timeperiod=14)` |
| 成交量 | OBV (能量潮) | `ta.OBV(dataframe)` |
| 成交量 | ADOSC (Chaikin) | `ta.ADOSC(dataframe)` |
| 形态 | CDLDOJI, CDLENGULFING 等 50+ 种 | `ta.CDLDOJI(dataframe)` |

### Pandas-TA（200+ 指标）

TA-Lib 未覆盖的指标（如 Supertrend, Ichimoku 等）可用 pandas-ta：

```python
import pandas_ta as pta

dataframe["supertrend"] = pta.supertrend(dataframe["high"], dataframe["low"], dataframe["close"])
```

文档：https://github.com/twopirllc/pandas-ta

### 命令行查询 TA-Lib 全部指标

```bash
cd ~/freqtrade
docker compose run --rm freqtrade python3 -c "import talib; print(sorted([f for f in dir(talib) if f.isupper()]))"
```

---

## 关键参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--strategy` | 策略类名（对应 strategies 目录下的 .py 文件名去掉后缀） | `SampleBTC` |
| `--timerange` | 回测时间范围 | `20170817-20260518` |
| `--epochs` | Hyperopt 迭代轮数，越大越充分但越慢 | `500` |
| `--spaces` | Hyperopt 优化空间 | `roi stoploss` |
| `--timeframes` | 下载的 K 线周期 | `1d 4h 1h 5m` |
| `--pairs` | 交易对 | `BTC/USDT` |

## 常用时间范围

- 全量 BTC 数据：`20170817-20260518`
- 最近一年：`20250501-20260518`
- Hyperopt 训练用（需要在回测时间之后留验证期）：`20170817-20240101`

## 当前配置

- 交易所：Binance (公开接口，无 API Key)
- 交易对：BTC/USDT
- K 线周期：日线 (1d)
- 初始资金：10,000 USDT
- 每笔投入：1,000 USDT
- 手续费：0.1%
- 模式：现货 (Spot)
