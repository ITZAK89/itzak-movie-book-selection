# Itzak's Selection — 电影图书推荐

聚合 Wikipedia 权威奖项数据，一站式浏览全球获奖电影和图书。数据实时拉取，无需注册，打开即用。

## 使用

**直接访问（推荐）：**[itzak89.github.io/itzak-movie-book-selection](https://itzak89.github.io/itzak-movie-book-selection/)

本地使用：

```bash
git clone https://github.com/itzak89/itzak-movie-book-selection.git
open index.html
```

## 功能

**电影**
- 22 个国际奖项全覆盖：戛纳、威尼斯、柏林、奥斯卡（含最佳国际影片）
- 按奖项来源 / 年份筛选，关键词搜索
- 海报展示（Wikipedia + TMDb 兜底），详情弹窗
- 收藏夹 & 已看标记（localStorage 持久化）
- 随机盲盒模式

**图书**
- 8 个国际文学奖：布克奖、诺贝尔文学奖、普利策小说奖、国际布克奖等
- 按奖项 / 年份筛选，关键词搜索
- 中译本标注

## 技术

纯静态 HTML/CSS/JS，零依赖。fetch() 调用 Wikipedia REST API，增量缓存策略（日常刷新仅 1 次 API 请求）。
