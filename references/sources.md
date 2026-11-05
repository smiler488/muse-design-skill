# 来源、采样与边界

版本：1.2 · 整理日期：2026-11-05（1.1：2026-11-02）。

## 一手来源

- [Muse 团队：How We Designed Muse](https://introducing.muse.ai/) — 主聊天、消息气泡、角色、活动入口、Goals、Ideas 与结构化操作的设计背景。
- [Alex Cornell 访谈](https://www.lennysnewsletter.com/p/how-meta-designed-muse-an-ai-agent) — 设计方向、界面结构、个性化、主聊与侧聊的取舍。
- [Emil Kowalski：Good vs Great Animations](https://emilkowal.ski/ui/good-vs-great-animations) — 学习动画起点、缓动与协调；不是 Muse 技术实现的证明。
- [Apple：Animate with springs](https://developer.apple.com/videos/play/wwdc2023/10158/) — 学习位置与速度连续性；不是 Muse 使用某套动画库的证明。

## 官方产品页实测（v1.2）

- [Muse 官方产品页](https://ai.meta.com/muse/) — 2026-11-05 用无头 Chrome 在 1440×900 与 390×844 视口打开，逐段滚动后读取 `getComputedStyle`（字号、行高、字重、颜色、圆角、内边距）与元素尺寸，并逐屏截图核对版式。结果整理在 [product-page.md](product-page.md)。只记录渲染结果；不下载字体文件、视频或图片，不提取源码。页面使用的 Optimistic 字体为 Meta 专有，本技能不附带也不建议使用。

## 颜色采样（应用层）

取 Muse 官方文章链接的原始 PNG，读取其 RGB 像素，结合图中区域识别用途。没有采集源码或私有设计文件，没有把浏览器截图的色彩管理结果当作官方 token。

| 原始图片 | 尺寸 | 可复查的像素颜色与用途 |
|---|---|---|
| [Ideas](https://introducing.muse.ai/_next/static/immutable/media/ideas.03w1vqmflzqox.png) | 1536 × 960 | `#FCFCFC` 占约 91.62%，为画布；`#67696C` 为摘要；`#111112` 为标题；`#E3E3E3` 出现在边缘 |
| [Activity](https://introducing.muse.ai/_next/static/immutable/media/status.38zbywac8-xmc.png) | 786 × 1254 | `#FCFCFC` 为背景；`#F3F4F5` 为控件/活动区域；`#FFFFFF` 为选中浮层 |
| [批准卡](https://introducing.muse.ai/_next/static/immutable/media/checkout.0nx6hmfxq6ara.png) | 786 × 1050 | `#FFFFFF` 为卡片；`#F3F4F5` 为次级区域；`#111112` 为正文；`#0064D4` 为 Allow 按钮 |

复核主蓝色的一个区域：批准卡图片 `(x=420..709, y=955..999)`，其中主色为 RGB `(0,100,212)`。只分析批准卡本身的控件，不从其中嵌入的商家网页提取应用主题色。频率统计只用于采样确认，不是要求网页必须采用相同比例。

## 本机观察

同日查看 Muse 桌面版的主聊天、Feed、Ideas、Goals、头像活动面板和活动详情，确认了浅色背景、浮动控件、逐层信息展开、聊天与内容分屏等模式。未逐帧测量动效，未提取字体文件，未检查内部 CSS；本仓库不包含任何私人对话、账号资料或本机界面截图。

## 推导项

用户补充观察（2026-11-02）：紧凑按键以图标呈现，鼠标悬停/手指操作时图标图案变化并出现功能文字，界面主要采用圆角矩形或胶囊。v1.1 将此提升为明确的组件规则并加入原创示例。示例触摸事件与时长是参考约定，没有宣称已实测 Muse 的触控实现。

`--muse-*` 名称、字体栈、尺寸、间距、圆角、阴影、悬停色、状态色、焦点样式、时长、曲线、响应式规则均为本项目建议。准确的图片像素值也不代表官方对外发布的设计规范；截图版本更新可能产生差异。

本项目包含原创文本、CSS 和演示页面，不附带 Muse 的图片、角色、商标或产品源码。公开来源用于可追溯学习。不要把本技能称为官方、内部提取或像素级复刻。

## 技能格式

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Agent Skills specification](https://agentskills.io/specification)

采用通用 `name` 与 `description` 前置字段，入口位于仓库根 `SKILL.md`，其余文件用相对路径引用。Claude Code 可将整个仓库放入单个技能目录。
