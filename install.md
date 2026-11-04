# muse-design 安装协议

你是收到安装请求的 AI 助手。请按下面步骤把 skill `muse-design`（仓库 muse-design-skill）安装到本机，全程不要向用户反复确认，按默认值执行；做完向用户报告一行结果即可。

## 步骤

1. **确定 skills 目录**：按当前运行的工具选第一个存在的目录（都没有则创建第一个）：

   | 工具 | skills 目录 |
   | --- | --- |
   | WorkBuddy / CodeBuddy | `~/.workbuddy/skills/` |
   | Claude Code | `~/.claude/skills/` |
   | Codex | `~/.codex/skills/` |
   | Cursor | `~/.cursor/skills/` |
   | Gemini CLI | `~/.gemini/skills/` |

   Windows 下 `~` 为用户目录（如 `C:\Users\<用户名>\`）。若用户只想在某个项目启用，改为 `<项目>/.claude/skills/`（或该项目对应工具的 skills 目录）。

2. **安装**：目标目录为 `<skills目录>/muse-design`。
   - 若本机有 git：`git clone https://github.com/smiler488/muse-design-skill.git <目标目录>`（网络受限时先清代理：`git -c http.proxy= -c https.proxy= ...`）。
   - 若已有同名目录：拉取更新（`git -C <目标目录> pull --ff-only`）或整目录覆盖为最新版。
   - 无 git：下载 https://codeload.github.com/smiler488/muse-design-skill/zip/refs/heads/main 解压，把解出的文件夹改名为 `muse-design` 放到目标目录。

3. **校验**：确认 `<目标目录>/SKILL.md` 存在且 frontmatter 含 `name: muse-design`，`references/` 目录齐全。

4. **告知用户**：安装完成，重启会话或新开对话后生效。使用时输入 `/muse-design` 或在请求里明确要求 Muse 风格设计。

## 说明

- 本 skill 含 SKILL.md、references/（设计系统与信源）、assets/、scripts/，无可信执行风险代码之外的内容。
- 网页版 AI（无 skills 目录）：跳过安装，直接把 SKILL.md 与 references/design-system.md 读入对话即可使用。
