---
name: muse-design
description: Design, implement, or review web and app interfaces in the Muse-inspired style — near-white pages, a fixed-px type ramp with weight-500 headings, translucent near-black secondary text, one accent per page, full-width hairline sections, soft borderless cards, capsule buttons, icon-first controls that change graphic and reveal labels, and progressive disclosure. Also carries the measured motion system (intent-named easing curves, paired in/out durations, hover wash, brightness press, 2px focus ring, and why Muse uses no scroll parallax), the color system with per-hue contrast limits, three-step tinted elevation, blur materials, and a density scale. Use when the user requests Muse-like design, 同款 Muse 风格, asks about typography, color, spacing, radius, shadow, blur, easing, duration or interaction polish in this style, or applies this skill to a website, personal site, research tools or an application.
---

# Muse-inspired interface design

把 Muse 的视觉与交互规则转化为适合当前产品的实现。默认采用浅色风格，尊重现有框架、内容、品牌约束和用户指定范围。

本技能是独立整理的参考实现，不是 Meta 官方设计系统。颜色部分来自公开图片采样；布局、尺寸、阴影、动效参数是经过整理的实现起点。不要把近似值说成 Muse 源码或内部规范。证据见 [references/sources.md](references/sources.md)。

## 先确定要做什么

1. 阅读当前项目的说明与相关页面，确认主任务、已有组件、样式入口、路由和响应式方式。修改已有网站时保留真实内容、链接、语言切换和功能，除非用户要求改变。
2. 按需要读实测参考（这四份是数值的单一来源，彼此不重复）：
   - **有文字 → [typography.md](references/typography.md)**：字号阶梯、行高、字重、字距、文字色。
   - **有颜色、阴影、圆角、留白 → [color-surface.md](references/color-surface.md)**：半透明中性色、每色相唯一可用档与对比度、三档阴影、模糊材质、密度与栅格。
   - **有过渡、入场、悬停、聚焦、加载 → [motion.md](references/motion.md)**：按意图命名的曲线、成对时长、交互状态，以及 Muse **没有**做的那些滚动效果。
   - 组件与模式见 [design-system.md](references/design-system.md)；图标按钮、展开、异步任务见 [interaction.md](references/interaction.md)；个人网站改造见 [website.md](references/website.md)。
3. **选层**：网页（个人网站、研究主页、产品介绍、工具页外壳）默认用**页面层**（`.muse-layer-page`：宽版面 + 落地页大标题）；应用内部界面（聊天、活动面板）用应用层。两层共用 typography.md 的同一套字号阶梯和文字色。[references/product-page.md](references/product-page.md) 记录的是另一个页面（营销页）的版式，排版数值已被 typography.md 取代。同一站点只用一种动作蓝。
4. 选一个能覆盖主要规则的页面或流程先实现，再复用到相关页面。不要为了套风格将普通个人网站变成聊天软件。

## 必须保留的风格特征

- **接近白色的底，清晰的黑灰文字。** 两层同一套：页面底 `#FCFCFC`，浮层 `#FFFFFF`，交替区段与柔和控件底 `#F3F4F5`，正文 `#111112`，次要文字 `#00040996`（**半透明**近黑，不是实色灰），分隔 `#000c1e17`。次要文字用半透明，是为了让同一个 token 落在白底、灰面板、淡蓝底上关系都不变。页面的温暖感来自少量人物、自然图片或物件，而不是全屏米黄。
- **一个页面只有一个主色。** 默认 `#0064D4`（悬停 `#0058BE`），通过 `data-muse-accent` 在根节点整体切换，而不是给每个区块分配一种颜色。每个色相只有一档可用（见 color-surface.md 的对比度表）：橙和黄**不能承载文字**，只能做点或色块，含义写在旁边的正文里。用户要求保留品牌色时，统一适配 primary、primary-hover、primary-soft、on-primary 及关联链接/焦点颜色，重新检查对比。次要动作使用浅灰底；状态另用语义色。不要给每个模块分配一种鲜艳颜色。
- **内容平静，操作有轻微悬浮感。** 文章、研究项目和条目靠对齐、留白、标题与摘要形成层级。输入框、浮动导航、菜单和活动面板可以使用柔和阴影。避免给所有内容套带阴影的卡片。
- **图标优先，交互时显露名称。** 紧凑导航、工具栏和次级操作默认只显示图标；鼠标悬停、键盘聚焦或触摸时，图标切换实际图形/轮廓并显露对应功能文字。只改颜色、阴影或整体缩放不算图案变化。保持图标语义与点击位置稳定；有效单次点击照常执行动作，不能变成“两次点击才执行”。主要提交、难辨认或高风险操作可保留文字。
- **圆角矩形与胶囊构成统一形状语言。** 小型图标控件用圆角方形或等宽高的胶囊，文字按钮用胶囊，菜单与面板用大圆角矩形；媒体和小块用较小圆角。纯内容条目可以没有外框，避免把所有内容都装进胶囊。
- **个性集中出现。** 可选一个原创或用户提供的头像、少量物件插图。功能图标仍保持统一的线性风格；保留名称或可访问标签。
- **按需展开，保持上下文。** 列表先呈现摘要，细节在当前对象附近或明确关联的面板展开。用户应知道内容从哪里打开、如何关闭、关闭后回哪里。
- **阅读体验来自排版，不来自装饰。** 排版细节全部按 [typography.md](references/typography.md)，其中四条最常被做错：
  - **行高是固定 px，而且字号越大越紧**：正文 16/22，区块标题 30/34，最大标题 48/52。长文阅读才放到 16/26。不要写 `line-height: 1.6`。
  - **字重只有 400 / 500 / 600**：标题 500，行内强调 600，正文 400。没有 300（Muse 的字体根本不含 300），没有 700/800。要更响就加大字号，不是加粗。
  - **34px 以下不收字距**：只有 40px+ 标题用 −0.015em。全大写眉标反过来要 +0.06em 正字距。
  - **层级只走阶梯**：11/12/13/14/15/16/17/18/22/30/34/40/48，中间不自创字号。
  另外：必须真的加载一个几何无衬线字体（默认 Hanken Grotesk），只写系统字体栈等于放弃一半风格；版面宽（约 1376px）而文字列窄（lead ~46rem、正文 ~68ch）；大区块之间用整宽 1px 细线和约 100px 留白分隔，而不是外框和阴影。去掉渐变光斑、彩色角标和层层套框。
- **动效服务操作，曲线按意图选。** 细节见 [motion.md](references/motion.md)：
  - 曲线按**发生了什么**选，不是全站一个 `ease`：用户发起的位移/展开用 `--muse-ease-move`，非用户发起的用 `-passive`，按下与换形用 `-quick`，进出用 `-enter`/`-exit`，**纯透明度用 linear**。
  - 时长成对，**出场不慢于入场**（200/150、280/200、400/350）。
  - 入场只写在 `prefers-reduced-motion: no-preference` 里，而不是先写好再关掉；位移 8px 级别，错峰 70ms 且封顶 5–6 个；淡入在 60% 就结束，位移继续跑完。
  - 悬停是一层 ~7.5% 的半透明 wash，按下是 `brightness(.95)`——**不是 `scale()`**；聚焦是 `outline: 2px` + `offset: 2px`。
  - **Muse 实测没有滚动视差、没有 sticky、没有滚动驱动动画、没有全局平滑滚动，整页只有一个元素带 transition。** 不要靠滚动特效制造"高级感"；真正需要动的是加载、进度、展开和浮层。

- **层级靠三档阴影和密度，不靠描边。** 内容卡片用 `#F3F4F5` 实底、无边框无阴影；只有真正浮起来的东西用 `--muse-elevation-1/2/3`（两层、染 `#111112`）。间距和圆角都乘一个密度系数，用 `data-muse-density="dense|airy"` 整块重调——数据界面更密更方，落地页更松更圆。

## 实现资产

- [assets/muse.css](assets/muse.css)：带 `--muse-*` 命名空间的颜色、字号阶梯、尺寸、动效变量和基础组件。字号/行高成对出现（`--muse-title-1` / `--muse-title-1-lh`），并有 `.muse-title-1`、`.muse-body-status`、`.muse-display` 等角色类——用角色类，不要在组件里手写 `font-size`。优先映射进现有设计变量；需要时复制采用的组件，避免引入冲突的全局样式。
- [assets/example.html](assets/example.html)：原创、无外部依赖的颜色与交互样例。用于理解层级和状态，不是个人主页模板，也不是真实 Muse 截图。
- [assets/page-example.html](assets/page-example.html)：产品页层样例（`muse-layer-page`）：眉标与区块头、手风琴配图、无边框特性卡片、问答、圆圈箭头链接。
- [assets/tool-example.html](assets/tool-example.html)：v1.3 两栏首屏、科研工具外壳、成对的「教程 / 打开工具」按钮、验证说明展开行、灰面板上的白色次级按钮。
- [assets/icon-controls.js](assets/icon-controls.js)：图标控件的文字显露、触摸反馈与 Escape 收起辅助行为；业务动作仍由具体按钮或链接实现。
- 动效与材质工具类：`.muse-reveal` / `.muse-reveal-group`（入场，仅存在于 `no-preference` 内）、`.muse-elevation-1/2/3`、`.muse-material`（玻璃层，`@supports` 渐进增强）、`.muse-squircle`（超椭圆圆角，需约两倍半径）。
- 修改变量后运行 `python3 scripts/check_tokens.py`：检查两层的关键色对（半透明色先与背景合成）、字号阶梯的 px 配对、400/500/600 字重范围、每个主色在三种页面底色上的双向对比度（并把橙/黄锁在"非文字"），以及时长的进出配对、意图曲线齐备、淡入为线性、三档阴影成立。它不替代实际页面检查。

没有指定技术栈时沿用项目现有技术。不要为了少量过渡新增庞大动效库。原生 app 可以把 token 映射到平台组件，但不要声称 CSS 资产是原生实现。

## 交付前检查

- 真实页面在宽屏和窄屏都保持清楚的主次关系；长中文、长标题、200% 缩放不裁切。
- 主要链接、导航、展开、关闭、表单等实际工作，键盘可达，焦点可见；关闭浮层后焦点回到触发入口。
- 普通文字与实际背景至少达到 4.5:1；有意义的控件边界/图标至少 3:1。浅色装饰边框不能成为识别输入框的唯一方式。
- 内容区域与操作区域有区别；没有把所有内容变成胶囊或卡片；蓝色、阴影和插图仍然节制。
- 同一工具/对象在卡片、页面、教程中只用一个名字。
- 排版（最容易退化，逐条核对渲染结果，不只看源码）：正文行高是 22px 而不是 1.6；标题字重 500、行内强调 600，页面上**没有** 300 或 700 的文字；34px 以下的标题字距为 0；所有字号都落在阶梯上；大写眉标有正字距；真的加载了几何无衬线字体（断网或字体 404 时页面不应退化成系统字体就交付）；中文段落行高已放宽到 1.6 左右且标题字距为 0。
- 页面层：每个大区块有眉标；区块之间是细线而不是外框；主按钮是蓝色胶囊（17/22、字重 500，不是黑色、不是粗体）；次级动作是圆圈箭头链接或灰底胶囊。
- 检查正常、悬停、按下、选中、禁用、加载、空和错误状态中实际存在的部分。没有后端时不伪造提交成功。
- 图标控件在悬停/聚焦/触摸时确实改变图形并显露功能文字；图标名称始终可被辅助技术读取。验证单次触控执行、触摸取消、真实选中状态和长标签，不让文字出现推走点击目标。
- 验证 `prefers-reduced-motion: reduce`：页面应是**静止的最终状态**，不是被截断的动画。移动端不能依赖悬停，内容展开不能挤出视口。
- 动效：每个过渡的曲线按意图选；出场时长 ≤ 入场；按下没有改变控件尺寸或位置；聚焦环 2px + 2px offset 且在深色区块上也可见；没有滚动视差、全局平滑滚动或整页渐入；没有为几个过渡引入动效库。
- 色彩与层级：页面只有一个主色；橙/黄没有承载文字；玻璃层在最坏背景下文字仍达 4.5:1；阴影只用三档之一；改一处密度属性，整块间距和圆角一起变（没有残留硬编码 px）；容器变宽时文字列没有跟着变宽。
- 按已有项目要求运行适当检查；有浏览器工具时实际操作页面并查看窄屏。明确说明未验证的部分。

最终说明修改了什么、怎样体现本风格、验证结果，以及仍需用户提供的内容。只对当前任务做必要改变。发布或部署按本次用户授权范围处理。
