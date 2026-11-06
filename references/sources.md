# 来源、采样与边界

版本：1.5 · 整理日期：2026-11-06（1.4 同日）（1.3 / 1.2：2026-11-05；1.1：2026-11-02）。v1.4 重做排版，来源是 platform.muse.ai 自己提供的 CSS（见下）。v1.3 的组件来自在 smiler488.github.io 上的实际改造与截图核对（桌面 1280/1440、手机 390、深色模式），不是 Muse 官网测量。

## 一手来源

- [Muse 团队：How We Designed Muse](https://introducing.muse.ai/) — 主聊天、消息气泡、角色、活动入口、Goals、Ideas 与结构化操作的设计背景。
- [Alex Cornell 访谈](https://www.lennysnewsletter.com/p/how-meta-designed-muse-an-ai-agent) — 设计方向、界面结构、个性化、主聊与侧聊的取舍。
- [Emil Kowalski：Good vs Great Animations](https://emilkowal.ski/ui/good-vs-great-animations) — 学习动画起点、缓动与协调；不是 Muse 技术实现的证明。
- [Apple：Animate with springs](https://developer.apple.com/videos/play/wwdc2023/10158/) — 学习位置与速度连续性；不是 Muse 使用某套动画库的证明。

## 官方产品页实测（v1.2）

- [Muse 官方产品页](https://ai.meta.com/muse/) — 2026-11-05 用无头 Chrome 在 1440×900 与 390×844 视口打开，逐段滚动后读取 `getComputedStyle`（字号、行高、字重、颜色、圆角、内边距）与元素尺寸，并逐屏截图核对版式。结果整理在 [product-page.md](product-page.md)。只记录渲染结果；不下载字体文件、视频或图片，不提取源码。页面使用的 Optimistic 字体为 Meta 专有，本技能不附带也不建议使用。

## 产品页 token 实读（v1.4）

- [Muse 产品页](https://platform.muse.ai/) — 2026-11-06 用无头 Chromium 在 1440×900 打开，读取 `getComputedStyle`；并取该页自己通过 `<link rel=stylesheet>` 提供的三个 CSS chunk（`_next/static/immutable/chunks/*.css`），直接读出其中声明的 `--text-*`（字号与行高成对）、`--font-weight-*`、`--tracking-*`、`--ai-gray-*`、`--blue-*` 变量。结果整理在 [typography.md](typography.md)。

这一层的证据比截图采样强：数值是页面自己声明的 token，不是从像素反推。但仍然只证明该日期该页面的公开 CSS，不证明 Meta 内部的 token 名称、设计文件或其他页面。只读取浏览器正常加载的公开样式表；没有下载字体文件（`optimisticAI` 为 Meta 专有），没有提取页面图片、视频、JS 源码或任何账号数据。

交叉验证：产品页声明的次要文字 `--ai-gray-a650: #00040996` 叠在 `--ai-gray-025 / bg-primary #FCFCFC` 上合成为 `#68696B`，与 v1.1 从应用截图像素采样得到的 `#67696C` 一致。两条独立取证互相印证了同一个值。

同日用同样方法测了 `smiler488.github.io` 与 `www.dc-ppp.com`，用于定位这两个站点与产品页的具体差异（行高 1.6/1.65、逐级负字距、真 300 与 600/700 字重、实色灰次要文字、无网页字体）。这些是本仓库使用者的站点，不是 Muse 的资产。

## 动效与色彩系统实读（v1.5）

同日（2026-11-06）用同样方法补测了动效、色彩系统、阴影、模糊、圆角与密度：

- 取 `platform.muse.ai` 的三个 CSS chunk 与页面内联 `<style>`，以及 `ai.meta.com/muse` 的内联样式（该页没有外链样式表），读出其中声明的 `--fds-animation-*`（按意图命名的缓动曲线）、`--fds-duration-*`（成对进出时长）、`--shadow-elevation-*`、`--fill-*`、`--ai-gray-*` / 各色相 `*-650`、`--spacing-density` / `--radius-density`、`corner-shape: squircle` 规则。
- 在 1440×900 实际操作：悬停主按钮与导航链接、Tab 聚焦读聚焦环、逐屏滚动全页后统计 `position: sticky`、`animation-timeline`、`will-change` 与带 transition 的元素数量。**结果为 0 / 0 / 0 / 1**，据此写下"Muse 没有滚动视差与滚动驱动动画"这一条。
- 对比度是用 WCAG 2.x 相对亮度公式对实测色值计算的，半透明色先与背景合成；`scripts/check_tokens.py` 会复算并在回归时失败。

结果整理在 [motion.md](motion.md) 与 [color-surface.md](color-surface.md)。

**排除项**：`platform.muse.ai` 内联了第三方 toast 组件库（sonner）的样式表，其中的 `.4s ease`、`swipe-out-*` 关键帧等**不是 Muse 的设计**，没有收录。区分页面自有 token 与 vendored 库是这次取证的一部分。

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
