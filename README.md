# Muse Design Skill

English | [中文](README.zh-CN.md)

[![CI](https://github.com/smiler488/muse-design-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/smiler488/muse-design-skill/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![Agent Skill](https://img.shields.io/badge/Agent_Skill-informational)
An Agent Skill for designing, building or reviewing web and app interfaces in the style of Meta's Muse app. It covers near-white pages, weight-500 headings with blue uppercase eyebrows, slate-grey body text and full-width hairline sections. It also covers soft borderless cards, capsule buttons, icon-first controls that change shape and reveal their label on hover or focus, and details that open next to the item they belong to.

I put it together while redesigning my personal and research-tool pages. I wanted the calm, readable feel of the Muse product page without copying any of its assets. The colours were sampled from public images. Sizes, spacing, shadows and motion are my own reference values, not Meta's internal specification. This is an independent project and is not affiliated with Meta.

There are two layers:

- **Product-page layer** (default for websites): white `#FFFFFF`, headings `#0A1317`, body `#5D6C7B`, action `#0457CB`, dividers `#DADDE1`, cards `#F1F4F7`, a 64/48/36/28/24/18/16/14 type scale, wide layout (~1376 px) with a narrow text column (~52 rem).
- **App layer** (chat, activity panels): page `#FCFCFC`, surface `#FFFFFF`, soft controls `#F3F4F5`, text `#111112`, secondary `#67696C`, action `#0064D4`.

## Install

Tell your assistant (Claude Code, Codex, WorkBuddy, …):

```text
Install muse-design following https://raw.githubusercontent.com/smiler488/muse-design-skill/main/install.md
```

Or by hand. The skill folder must be called `muse-design`:

```bash
git clone --depth 1 https://github.com/smiler488/muse-design-skill.git ~/.claude/skills/muse-design
```

For one project only, clone into `<project>/.claude/skills/muse-design`. Update with `git -C ~/.claude/skills/muse-design pull --ff-only`. `muse-design.skill` is the same content as an importable package.

## Use

Type `/muse-design` in Claude Code or ask for a Muse-style design. A prompt I use for personal websites:

```text
/muse-design Restyle the current personal website.

Inspect the project structure, pages and styling first. Keep the framework, the real
content, routes, the language switch and existing features. Use Muse's near-white
background, black/grey text hierarchy, restrained blue actions, soft floating layers
and progressive disclosure as reference; do not turn the site into a chat app.

Start with the home page and one project page, and collect colours, type, spacing,
radii and motion into reusable variables. If the brand colour must stay, use it as the
action colour and recheck contrast. Check mobile, keyboard use, long titles and reduced
motion. Report changes and anything not verified; keep the result local.
```

## Contents

| Path | What it is |
| --- | --- |
| `SKILL.md` | entry point and workflow for the assistant |
| `references/design-system.md` | colour, type, spacing, radii, shadows, images |
| `references/interaction.md` | disclosure, split views, motion, keyboard and focus |
| `references/product-page.md` | product-page layer measured on the official page |
| `references/website.md` | applying the rules to an existing website |
| `references/sources.md` | sampling method and public references |
| `assets/muse.css` | `--muse-*` tokens and base components |
| `assets/example.html`, `assets/page-example.html` | original, dependency-free demos of both layers (open in a browser) |
| `assets/icon-controls.js` | label reveal, touch feedback and Escape handling for icon controls |
| `scripts/check_tokens.py` | WCAG contrast check of the key colour pairs of both layers |

The CSS is a light-theme reference. A dark theme needs its own adaptation and testing. Native apps can reuse the tokens and behaviour rules, but the CSS itself is not a native component.

## Check

```bash
python3 scripts/check_tokens.py
```

All 34 colour pairs of both layers pass (text ≥ 4.5:1, control borders ≥ 3:1). Layout, real interaction and browser support still need checking in the actual project.

## License

MIT, see [LICENSE](LICENSE). It covers the original content of this repository only and grants no rights to third-party trademarks or assets. Liangchao Deng (邓良超).
