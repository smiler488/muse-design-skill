# 动效与交互状态：实测（v1.5）

涉及任何过渡、入场、悬停、按下、聚焦、加载、展开时读这份。

## 证据等级

**实测值**：2026-11-06 用无头 Chromium 打开 <https://platform.muse.ai/> 与 <https://ai.meta.com/muse/>，取两站自己提供的样式表与内联 `<style>`，读出其中声明的动效 token；并在 1440×900 实际悬停、Tab 聚焦、逐屏滚动，读 `getComputedStyle` 比对前后状态。

**边界**：`platform.muse.ai` 内联了第三方 toast 库（sonner）的样式，里面的 `.4s ease` 之类**不是 Muse 的设计**，本文件不收。下表只收两站自己的 token 与页面自身的关键帧。

## 曲线按"意图"命名，不是按 ease-out

这是整套动效最值得抄的一点：曲线不是按形状（ease-in / ease-out）选，而是按**发生了什么、谁发起的**选。

| 意图 | 曲线 | 用在哪 |
|---|---|---|
| `move` / `expand-collapse` | `cubic-bezier(0.17, 0.17, 0, 1)` | 用户自己发起的位移、展开收起。强减速、零回弹 |
| `passive-move` | `cubic-bezier(0.5, 0, 0.1, 1)` | **不是**用户发起的位移（轮播自走、后台刷新）。两头都缓，不抢注意力 |
| `quick-move` | `cubic-bezier(0.1, 0.9, 0.2, 1)` | 开关、按下、图标换形。几乎瞬间起步 |
| `enter` | `cubic-bezier(0.14, 1, 0.34, 1)` | 东西出现 |
| `exit` | `cubic-bezier(0.45, 0.1, 0.2, 1)` | 东西离开 |
| `fade` | **linear**（`cubic-bezier(0, 0, 1, 1)`） | 纯透明度。**不要给 opacity 加缓动** |
| `soft` / `strong` | `cubic-bezier(.08,.52,.52,1)` / `cubic-bezier(.12,.8,.32,1)` | 通用备用档 |

两条推论：

- **进出用不同曲线。** `enter` 起步极快然后长时间沉降；`exit` 起步慢一点、收尾干脆。同一个元素进和出不是同一条曲线的正反放。
- **淡入淡出是线性的。** 透明度没有质量，给它加减速只会让它看起来"粘"。位移才需要曲线。

## 时长成对，而且出比进快

| 档 | in | out |
|---|---|---|
| xxs | 100ms | 100ms |
| xs | 200ms | 150ms |
| s | 280ms | 200ms |
| m | 400ms | 350ms |
| l | 500ms | 350ms |
| xl | 1000ms | 1000ms |

**出场永远不慢于入场**（只有 100ms 和 1000ms 两端相等）。原则：来可以花时间，走不能占用户时间。一个 300ms 进、300ms 出的弹窗，关的时候就是慢。

选档：按下/换形 xxs，悬停与提示 xs，菜单与展开 s，区块入场 m，首屏编排 l。

## 入场编排（实测关键帧）

`platform.muse.ai` 首屏：

```css
@media (prefers-reduced-motion: no-preference) {
  .platform-intro-icon  { animation: emerge .62s cubic-bezier(.65,0,.35,1) backwards; }
  .platform-intro-avatar{ animation: settle .42s cubic-bezier(.22,1,.36,1) backwards; }
}
@keyframes emerge {
  0%  { opacity: 0; transform: translate(dx, dy) scale(.16); }
  60% { opacity: 1; }                      /* 淡入在 60% 就结束 */
  to  { opacity: 1; transform: translate(0) scale(1); }
}
```

三个细节值得照抄：

1. **整段动画只存在于 `prefers-reduced-motion: no-preference` 里**，而不是先写好再在 `reduce` 里关掉。于是"不要动效"的用户拿到的是静止的最终状态，不是一个被纠正过的动画。
2. **淡入在 60% 就到 1，位移继续跑到 100%。** 内容在停稳之前就已经可读，入场不会显得卡。
3. **错峰 70ms**（实测 0.14 / 0.21 / 0.28 / 0.35 / 0.42s 五个延迟）。`animation-fill-mode: backwards` 保证元素在延迟期间是隐藏的，而不是先闪一下。

错峰要封顶：超过 5–6 个之后，最后一个是在等编排而不是在被阅读。本仓库的 `.muse-reveal-group` 到第 6 个就不再增加延迟。

## 交互状态（实测）

| 状态 | Muse 的做法 | 不要做 |
|---|---|---|
| 悬停 | 盖一层 **~7.5% 黑**（`#00000013`）的 wash，或 `opacity: .8 → 1` | 换一个手挑的灰色；加阴影抬起；放大 |
| 按下 | `filter: brightness(90–95%)` 或 `opacity: .6` | `transform: scale(.98)` ——缩放会把标签从手指底下挪走，每次点击都像在弹 |
| 聚焦 | `outline: 2px solid <accent>; outline-offset: 2px` | 3–4px 的粗框、box-shadow 光晕（不跟随真实形状）、`outline: none` |
| 禁用 | 更深一级的灰底 + 次要文字色 | 整体 `opacity`（会把文字对比度一起拖垮） |

wash 用半透明而不是实色的理由和次要文字一样：同一条规则在白底、`#F3F4F5` 面板、蓝色行上都成立。

落地页上的导航链接和主按钮**实测悬停没有过渡**（`transition-duration: 0s`）：wash 是立刻出现的。会动的东西用 `.15s` 的默认过渡。

## Muse 没有做的事（重要）

逐屏滚动 `platform.muse.ai` 全页后实测：

- `position: sticky` 元素：**0 个**
- `animation-timeline`（滚动驱动动画）：**0 个**
- `will-change` 非 auto：**0 个**
- `scroll-behavior`：`auto`（没有全局平滑滚动）
- 整页只有 **1 个**元素带 transition

**没有滚动视差，没有滚动进度联动，没有逐块飞入。** 那种"高级感"不是靠滚动效果堆出来的——它来自排版、留白、克制的色彩，以及**几乎不动**。页面上会动的东西只有三类：首屏一次性编排、用户自己触发的状态变化、真实的加载/进度反馈（骨架 shimmer、脉冲、活动指示）。

所以做"Muse 风格"时：

- 想加滚动视差 → 不加。
- 想给每个区块加滚动渐入 → 最多给首屏一次，或完全不加。整页依次飞入会让快速滚动的用户一直在看半透明的东西。
- 想加全局 `scroll-behavior: smooth` → 不加；锚点跳转交给浏览器，键盘用户和快速导航的人需要立刻到位。
- 想做滚动进度条 → 只有在进度本身是内容时才做（长文阅读），不要给落地页加。

真正需要动的地方是**异步与状态**：加载骨架（shimmer）、进行中（脉冲/活动指示）、展开收起、浮层进出、按下反馈。这些是本仓库 `muse.css` 里实现的部分。

## 本仓库的实现

```css
--muse-ease-move / -passive / -quick / -enter / -exit / -fade
--muse-duration-{xxs,xs,s,m,l,xl}-{in,out}
--muse-stagger: 70ms
--muse-wash-hover / --muse-wash-active / --muse-press-brightness
--muse-focus-width: 2px / --muse-focus-offset: 2px
.muse-reveal / .muse-reveal-group      /* 仅存在于 no-preference 内 */
```

`.muse-reveal` 的位移是 **8px**，不是半屏滑动：入场是提示"这里新出现了东西"，不是表演。

## 交付前检查

- 每个过渡的曲线是按意图选的，不是全站一个 `ease`。
- 出场时长 ≤ 入场时长。
- `prefers-reduced-motion: reduce` 下页面是**静止的最终状态**，不是被截断的动画；手动在 DevTools 里切一次验证。
- 聚焦环在键盘 Tab 下可见，2px、带 offset，且在深色区块上也能看见。
- 按下反馈没有改变控件尺寸或位置。
- 没有引入滚动视差、全局平滑滚动、整页渐入。
- 没有为了几个过渡引入动效库。
