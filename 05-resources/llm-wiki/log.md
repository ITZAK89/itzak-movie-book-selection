---
area: llm-wiki
type: log
created: 2026-05-15
---

# LLM Wiki 操作日志

## [2026-05-15] 重构 | 改为三步结构

- pages/ → wiki/，新增 outputs/
- 对齐博主 Martina 推荐的三步结构：raw → wiki → outputs
- 更新 schema.md、overview.md、llm-wiki-building-guide.md

## [2026-05-15] 初始化 | LLM Wiki 知识库创建

- 创建 Wiki 目录结构
- 编写 overview.md（LLM Wiki 概念说明）
- 编写 schema.md（LLM 维护规范）
- 编写 index.md（页面索引模板）
- 编写 log.md（本文件，操作日志）

## [2026-05-15] 收录 | AI个人知识库搭建教程 (Bilibili)

- 来源：B站 Martina在进化，Karpathy LLM Wiki 搭建教程
- 创建 [[llm-wiki-building-guide]] 笔记页
- 更新 index.md
- 注意：视频类剪辑原始文件含大量 UI 噪音，后续建议手动补充视频要点笔记

## [2026-05-18] 收录 | BTC report_20260518

- 来源：raw/BTC report_20260518.md
- 创建 [[btc-multi-agent-trading-analysis-20260518]] source-note 页面
- 内容：多智能体 BTC 交易分析报告，涵盖技术面/情绪面/新闻面/基本面四维分析、5 轮牛熊辩论、三方风控博弈、组合经理裁决 SELL
- 更新 index.md

## [2026-05-18] 新建 | 概念页面

- 创建 [[multi-agent-trading-framework]] 概念页：多智能体交易决策框架
- 从 [[btc-multi-agent-trading-analysis-20260518]] 衍生
- 更新 index.md

## [2026-05-18] 收录 | Freqtrade 开源加密货币交易机器人

- 来源：raw/freqtradefreqtrade Free, open source crypto trading bot.md
- 创建 [[freqtrade]] source-note 页面
- 内容：Python 开源交易机器人，支持多交易所、回测、ML 策略优化、FreqAI 自适应建模
- 更新 index.md

## [2026-05-18] 收录 | 资本是如何引爆全球金融危机的？

- 来源：B站 BV1hN596zEas（小Lin说），AI 字幕由用户通过 dubbing 下载
- 字幕转存为 raw/资本是如何引爆全球金融危机的-字幕.md
- 创建 [[asian-financial-crisis-1997]] source-note 页面
- 内容：1994-98 年全球金融危机链，墨西哥→东南亚→韩国→香港保卫战→俄罗斯，索罗斯做空策略，IMF 道德风险
- 更新 index.md

## [2026-05-18] 收录 | OpenBB 开放数据平台

- 来源：raw/OpenBB-开放数据平台-zh.md（GitHub README 中文翻译）
- 创建 [[openbb]] source-note 页面
- 内容：ODP 架构、四类消费终端（Python/Workspace/MCP/REST）、与 Freqtrade 的互补关系
- 更新 index.md

## [2026-05-20] 收录 | ECC (Everything Claude Code)

- 来源：raw/affaan-meverything-claude-code...md（GitHub README 全文）
- 创建 [[everything-claude-code]] source-note 页面
- 内容：182K+ star 的 Agent harness 性能优化系统，Skills/Hooks/Agents/Rules 四维架构，hooks 设计模式，token 优化策略
- 衍生创建 [[agent-harness]] 概念页：Agent 运行时系统的四组件架构
- 更新 index.md

## [2026-05-20] 收录 | awesome-gpt-image-2 (Prompt as Code)

- 来源：raw/freestyleflyawesome-gpt-image-2...md（GitHub README 全文）
- 创建 [[prompt-as-code]] source-note 页面
- 内容：GPT-Image2 工业级提示词引擎，"散文式提示词→结构化协议"方法论，370+ 案例 12 大类，20+ 工业模板
- 核心洞察：Prompt as Code 与 LLM Wiki 共享"编译一次，持续使用"的复利理念
- 更新 index.md

## [2026-05-20] 收录 | ECC 系列 Hook 专集视频

- 来源：raw/ECC助claude code自己管理自己-hook.md（B站视频字幕）
- 创建 [[ecc-hooks-video]] source-note 页面
- 内容：六种 Hook 生命周期枚举、Stop Hook 四件套设计、Memory Persistence 三件组合、Hookify 自然语言配置工具
- 对照本 vault：视频 Hook 模式更适合代码项目，纯 Markdown 项目需做减法；PreCompact "保存关键状态"被视频理想化，shell hook 能力边界是实践核心限制
- 更新 index.md

## [2026-05-20] 产出 | 跨机器 Hook 部署方案

- Source: 对话产出，总结为 outputs/对话总结-2026-05-20.md（第二次会话，覆盖同一文件）
- 梳理完整 Hook 配置文件结构：settings.json + commands/ + CLAUDE.md
- 设计自然语言指令方案：让另一台 Mac 的 Claude 自动探测 vault 结构并生成等价 hook 配置
- 核心机制：Stop 提示 /summary → SessionStart 展示 outputs 文件列表 → 用户让 Claude 读最新 output 继续工作
- 确认 M 芯片对 osascript 通知无影响

## [2026-05-20] 改进 | /summary 命令优化

- 增加保存前三选一逻辑（合并/新建/覆盖），避免直接覆盖已有文件
- 增加主题名询问步骤，文件名从 `对话总结-{{date}}.md` 改为 `{主题名}-{{date}}.md`
- 解决多项目并行时 outputs/ 文件名撞车问题
- 测试通过：主题名询问 → 文件冲突检查 → 保存成功

## [2026-05-21] 开发 | 韩语学习网站词汇体系搭建

- Source: 对话产出，总结为 outputs/韩语学习网站-2026-05-21.md
- 构建「AI种子词表 → KRDict API → AI中文翻译」词汇生产管道，100词测试成功率87%
- 设计多义词数据结构(senses字段)并实现UI义项分组渲染
- 词汇量从100词扩充到459词（6级占71%），覆盖14个分类
- 因KRDict对6级术语命中率低，切换为AI全生成策略（韩文释义+中文翻译+实战例句）
- UI优化：复习按钮移至卡片右上角、标题改为Vocabulary、列表默认折叠

## [2026-05-21] 开发 | 韩语学习网站语法板块

- Source: 对话产出，合并至 outputs/韩语学习网站-2026-05-21.md
- 设计学测分离模式：Study（分类浏览82条语法卡片）+ Quiz（79道近义辨析选择题）
- Quiz选项从同一功能类别抽取（如全为「原因」类），模拟TOPIK阅读题实际考法
- 以Korean Grammar in Use为主骨架，覆盖14个语法分类
- Grammar面板功能对齐Vocabulary：等级/分类筛选、每日数量、复习按钮

## [2026-05-21] 开发 | Grammar 复习功能完善

- Source: 对话产出，合并至 outputs/韩语学习网站-2026-05-21.md
- Grammar卡片添加复习标记按钮（今日复习/强化复习），localStorage持久化
- 实现复习模式筛选：点击复习入口按钮过滤已标记语法，再次点击退出
- 切换等级/分类/每日数量时自动退出复习模式
- Vocabulary + Grammar 功能完全对齐：筛选、每日数量、复习标记、复习模式

## [2026-05-21] 开发 | Shadowing 板块搭建（Echo Method）

- Source: 对话产出，合并至 outputs/韩语学习网站-2026-05-21.md
- 模仿 Miraa app Echo Method 跟读模式：Listen → Reveal → Shadow → Next
- 通过 yt-dlp 提取 YouTube 韩语字幕（VTT格式），解析为逐句时间戳
- 内置 10 个 TEDx 韩语视频（5,191 句字幕 + 音频），视频选择器切换
- 音频 timeupdate 跟踪同步字幕；字幕数据拆分独立 JS 文件（953KB→327KB）

## [2026-05-22] 重构 | Shadowing 板块重建与排错

- Source: 对话产出，合并至 outputs/韩语学习网站-2026-05-21.md
- 大范围代码丢失后，用 regenerate_html.py 从 JSON 数据源全新生成 index.html
- 经验教训固化到 memory：大 HTML 文件不反复 Edit，用脚本从数据源重新生成
- Shadowing 重建为用户自供内容模式（粘贴 YouTube + VTT 字幕）
- 编写 server.py（自定义 HTTP 服务器，/api/download 端点 + Range 请求支持）
- 修复音频 seek：Range 206 Partial Content 解决浏览器无法跳转问题
- 提供 file:// 和 http://localhost:8766 双访问链接
