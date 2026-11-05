---
name: muse-design
description: Design, implement, or review web and app interfaces in the Muse-inspired style — white pages with weight-500 headings and blue uppercase eyebrows, slate-gray copy, full-width hairline sections, soft borderless cards, accordions with paired media, capsule buttons, icon-first controls that change graphic and reveal labels, and progressive disclosure. Covers both the app layer and the product-page layer measured on the official Muse page. Use when the user requests Muse-like design, 同款 Muse 风格, or applies this skill to a website, personal site, research tools or an application.
---

# Muse-inspired interface design

把 Muse 的视觉与交互规则转化为适合当前产品的实现。默认采用浅色风格，尊重现有框架、内容、品牌约束和用户指定范围。

本技能是独立整理的参考实现，不是 Meta 官方设计系统。颜色部分来自公开图片采样；布局、尺寸、阴影、动效参数是经过整理的实现起点。不要把近似值说成 Muse 源码或内部规范。证据见 [references/sources.md](references/sources.md)。

## 先确定要做什么

1. 阅读当前项目的说明与相关页面，确认主任务、已有组件、样式入口、路由和响应式方式。修改已有网站时保留真实内容、链接、语言切换和功能，除非用户要求改变。
2. 先读取 [references/design-system.md](references/design-system.md)。涉及图标按钮、状态反馈、展开、面板或异步任务时，再读 [references/interaction.md](references/interaction.md)。个人网站、作品集或首页改造时，再读 [references/website.md](references/website.md)。
3. **选层**：网页（个人网站、研究主页、产品介绍、工具页外壳）默认用**产品页层**，必读 [references/product-page.md](references/product-page.md)——它来自官方产品页的实测排版；应用内部界面（聊天、活动面板）用应用层。同一站点只用一种动作蓝。
4. 选一个能覆盖主要规则的页面或流程先实现，再复用到相关页面。不要为了套风格将普通个人网站变成聊天软件。

## 必须保留的风格特征

- **接近白色的底，清晰的黑灰文字。** 应用层：页面底 `#FCFCFC`，浮层 `#FFFFFF`，柔和控件底 `#F3F4F5`，正文 `#111112`，次要文字 `#67696C`。产品页层（网页默认）：白底 `#FFFFFF`，标题 `#0A1317`，说明 `#5D6C7B`，卡片 `#F1F4F7`，分隔 `#DADDE1`，动作 `#0457CB`。页面的温暖感来自少量人物、自然图片或物件，而不是全屏米黄。
- **动作色有明确用途。** 默认 `#0064D4` 用于主要动作和链接。用户要求保留品牌色时，统一适配 primary、primary-hover、primary-soft、on-primary 及关联链接/焦点颜色，重新检查对比。次要动作使用浅灰底；状态另用语义色。不要给每个模块分配一种鲜艳颜色。
- **内容平静，操作有轻微悬浮感。** 文章、研究项目和条目靠对齐、留白、标题与摘要形成层级。输入框、浮动导航、菜单和活动面板可以使用柔和阴影。避免给所有内容套带阴影的卡片。
- **图标优先，交互时显露名称。** 紧凑导航、工具栏和次级操作默认只显示图标；鼠标悬停、键盘聚焦或触摸时，图标切换实际图形/轮廓并显露对应功能文字。只改颜色、阴影或整体缩放不算图案变化。保持图标语义与点击位置稳定；有效单次点击照常执行动作，不能变成“两次点击才执行”。主要提交、难辨认或高风险操作可保留文字。
- **圆角矩形与胶囊构成统一形状语言。** 小型图标控件用圆角方形或等宽高的胶囊，文字按钮用胶囊，菜单与面板用大圆角矩形；媒体和小块用较小圆角。纯内容条目可以没有外框，避免把所有内容都装进胶囊。
- **个性集中出现。** 可选一个原创或用户提供的头像、少量物件插图。功能图标仍保持统一的线性风格；保留名称或可访问标签。
- **按需展开，保持上下文。** 列表先呈现摘要，细节在当前对象附近或明确关联的面板展开。用户应知道内容从哪里打开、如何关闭、关闭后回哪里。
- **阅读体验来自排版，不来自装饰。**（产品页层）标题用 500 字重、展开项标题 300，层级靠 64/48/36/28/24/18/16/14 的字号阶梯；说明文字用冷灰蓝 `#5D6C7B`；区块前有蓝色眉标；版面宽（约 1376px）而文字列窄（~52rem）；大区块之间用整宽 1px 细线和 80px 留白分隔，而不是外框和阴影。去掉渐变光斑、彩色角标和层层套框。
- **动效服务操作。** 即时反馈、短距离移动、自然减速，支持中断和减少动态效果。频繁操作不要等待装饰动画；不要强迫滚动、自动漂浮或整页依次飞入。

## 实现资产

- [assets/muse.css](assets/muse.css)：带 `--muse-*` 命名空间的颜色、尺寸、动效变量和基础组件。优先映射进现有设计变量；需要时复制采用的组件，避免引入冲突的全局样式。
- [assets/example.html](assets/example.html)：原创、无外部依赖的颜色与交互样例。用于理解层级和状态，不是个人主页模板，也不是真实 Muse 截图。
- [assets/page-example.html](assets/page-example.html)：产品页层样例（`muse-layer-page`）：眉标与区块头、手风琴配图、无边框特性卡片、问答、圆圈箭头链接。
- [assets/tool-example.html](assets/tool-example.html)：v1.3 两栏首屏、科研工具外壳、成对的「教程 / 打开工具」按钮、验证说明展开行、灰面板上的白色次级按钮。
- [assets/icon-controls.js](assets/icon-controls.js)：图标控件的文字显露、触摸反馈与 Escape 收起辅助行为；业务动作仍由具体按钮或链接实现。
- 修改变量后运行 `python3 scripts/check_tokens.py` 检查两层的关键色对。它不替代实际页面检查。

没有指定技术栈时沿用项目现有技术。不要为了少量过渡新增庞大动效库。原生 app 可以把 token 映射到平台组件，但不要声称 CSS 资产是原生实现。

## 交付前检查

- 真实页面在宽屏和窄屏都保持清楚的主次关系；长中文、长标题、200% 缩放不裁切。
- 主要链接、导航、展开、关闭、表单等实际工作，键盘可达，焦点可见；关闭浮层后焦点回到触发入口。
- 普通文字与实际背景至少达到 4.5:1；有意义的控件边界/图标至少 3:1。浅色装饰边框不能成为识别输入框的唯一方式。
- 内容区域与操作区域有区别；没有把所有内容变成胶囊或卡片；蓝色、阴影和插图仍然节制。
- 同一工具/对象在卡片、页面、教程中只用一个名字。
- 产品页层：标题不超过 500 字重；每个大区块有眉标；区块之间是细线而不是外框；主按钮是蓝色胶囊（不是黑色）；次级动作是圆圈箭头链接或灰底胶囊。
- 检查正常、悬停、按下、选中、禁用、加载、空和错误状态中实际存在的部分。没有后端时不伪造提交成功。
- 图标控件在悬停/聚焦/触摸时确实改变图形并显露功能文字；图标名称始终可被辅助技术读取。验证单次触控执行、触摸取消、真实选中状态和长标签，不让文字出现推走点击目标。
- 验证 `prefers-reduced-motion`；移动端不能依赖悬停，内容展开不能挤出视口。
- 按已有项目要求运行适当检查；有浏览器工具时实际操作页面并查看窄屏。明确说明未验证的部分。

最终说明修改了什么、怎样体现本风格、验证结果，以及仍需用户提供的内容。只对当前任务做必要改变。发布或部署按本次用户授权范围处理。
