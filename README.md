# Muse Design Skill

给 Claude Code 等支持 Agent Skills 的工具使用的 **Muse 风格网页与 app 设计技能**。重点是可复用的颜色、排版、空间、组件状态与交互规则，适用于个人网站改造和应用界面设计。

v1.3 补充在研究网站上验证过的组件：两栏首屏、科研工具外壳、成对的教程/打开工具按钮（书本图标悬停翻开）、验证说明展开行、灰面板上的白色次级按钮，以及命名一致与深色图标规则，见 [tool-example.html](assets/tool-example.html)。

v1.2 新增**产品页层**：在 Muse 官方产品页实测排版与版式（字号阶梯、500 字重标题、蓝色眉标、冷灰蓝说明文字、整宽细线分区、无边框灰底卡片、手风琴配图、问答），用于个人网站与科研工具页；应用层保持不变，见 [product-page.md](references/product-page.md) 与 [page-example.html](assets/page-example.html)。

v1.1 明确加入：**默认图标优先 → 悬停/聚焦/触摸时图案变化并显露功能文字**；圆角方形、圆角矩形与胶囊组成一致的形状语言。示例中的收藏和稍后阅读支持一次点击切换，并区分悬停反馈和真实开启状态。

独立整理，非 Meta 官方项目。核心颜色从官方公开图片采样；其他实现参数是参考值。包含原创样例，不包含 Muse 角色素材、私人截图或产品源码。

## 配色

产品页层（网站默认，官网实测）：页面底 `#FFFFFF` · 标题 `#0A1317` · 说明 `#5D6C7B` · 动作 `#0457CB` · 分隔 `#DADDE1` · 卡片 `#F1F4F7`。

应用层（应用截图采样）：

| 用途 | 色值 |
|---|---|
| 页面背景 | `#FCFCFC` |
| 浮层、菜单、输入区域 | `#FFFFFF` |
| 柔和控件底色 | `#F3F4F5` |
| 主要文字 | `#111112` |
| 次要文字 | `#67696C` |
| 装饰边界 | `#E3E3E3` |
| 主要动作与链接 | `#0064D4` |

具体证据和用途见 [design-system.md](references/design-system.md) 与 [sources.md](references/sources.md)。

## 安装

**一句话安装**：复制下面这句发给你在用的 AI 助手（WorkBuddy、Claude Code、Codex 等），它会自动完成安装：

```text
请根据 https://raw.githubusercontent.com/smiler488/muse-design-skill/main/install.md，安装 muse-design。
```

手动安装（以 Claude Code 为例）：这是单技能仓库，根目录就是 `SKILL.md`。个人级安装：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/smiler488/muse-design-skill.git ~/.claude/skills/muse-design
```

只在某个项目启用时，在项目根目录运行：

```bash
mkdir -p .claude/skills
git clone https://github.com/smiler488/muse-design-skill.git .claude/skills/muse-design
```

二选一即可。已有同名目录时先检查内容，不要覆盖；已安装副本可用 `git -C ~/.claude/skills/muse-design pull --ff-only` 更新。

在 Claude Code 中输入 `/muse-design`，或在请求里明确使用 Muse 风格。若技能列表尚未刷新，重启当前会话。安装路径与使用方式依据 [Claude Code 官方文档](https://code.claude.com/docs/en/skills)。

## 改造个人网站的提示词

```text
/muse-design 改造当前个人网站。

先检查项目结构、现有页面和样式系统，保留技术框架、真实内容、路由、
中英文切换与已有功能。以 Muse 的接近白色背景、黑灰文字层级、克制蓝色
动作、柔和浮层和渐进展开为参考；不要把网站改成聊天软件。

先实现主页和一个项目详情页，把颜色、字体、间距、圆角和动效整理成可复用
变量。若现有品牌色必须保留，使用该色作为动作色并重新检查对比度。
验证移动端、键盘操作、长标题、减少动态效果和现有项目检查。
完成后说明改动与未验证项，先保留本地结果。
```

这段提示词默认本地改造。需要部署时，另外写明目标与授权。

## 内容

- [SKILL.md](SKILL.md)：智能体入口与工作流程。
- [视觉规范](references/design-system.md)：配色、字号、间距、圆角、阴影、图片与深色扩展边界。
- [交互规范](references/interaction.md)：信息展开、分屏、动效、键盘和焦点行为。
- [个人网站适配](references/website.md)：把规则用于已有网站。
- [CSS 资产](assets/muse.css)：有命名空间的 token 与基础组件，可映射到已有框架。
- [交互样例](assets/example.html)：下载后在浏览器打开，查看色板、条目、展开与弹层。无需安装依赖。
- [产品页层规范](references/product-page.md) 与 [产品页样例](assets/page-example.html)：网站排版、区块、卡片、手风琴与问答。
- [图标反馈辅助代码](assets/icon-controls.js)：文字显露、触摸反馈、取消与 Escape 收起；与实际业务动作分离。
- [来源与边界](references/sources.md)：采样方法与公开参考。

CSS 为浅色参考实现。深色主题需要另行适配与验证；原生 app 可借用设计变量和行为规则，CSS 本身并非原生组件。

## 检查

```bash
python3 scripts/check_tokens.py
```

检查应用层与产品页层的关键文字、状态、控件和焦点颜色对比，修改 token 后可以重复运行。实际项目仍需检查布局、真实交互、浏览器兼容与内容。

本版已检查：技能格式、相对引用、15 组关键色对及对比度失败检出；浏览器桌面与 390/320px 窄屏布局；展开、弹层、Escape 关闭与焦点返回。独立智能体完成了保留品牌色、双语路由和原有框架的方案测试。尚未直接在 Claude Code 中运行网站改造，也未进行全部浏览器或原生 app 验证。

v1.1 另外检查了图标默认/悬停/键盘聚焦的图形与名称、单击开启、Escape 隐藏名称但保留选中态，以及 320px 窄屏标签位置。触摸开始/松开/取消、点外部与混合输入切换经过事件逻辑模拟；未在真实触屏设备上实测。

许可证：MIT，覆盖本仓库原创内容；不授予任何第三方商标或素材权利。
