---
title: "Hermes 的技能加载先按 platforms 声明过滤"
date: 2026-10-20
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 背景

Hermes 加载技能时，会先按 SKILL.md 里的 platforms 声明过一道筛。磁盘上有这个技能、桌面技能列表里却没有，不代表装坏了，这一步是自动的，和手动禁用是两回事。

# 机制

SKILL.md 的 frontmatter 里可以写 platforms。比如 apple-notes 标了 platforms: [macos]，在这台 Linux 机器上照样躺在技能目录里，Hermes 加载时按当前系统比对，不匹配就不加载，桌面端的技能列表里也看不到它。

skills.disabled 是另一道开关，写在配置里，靠人工列名单。两道都放行的技能才真正可用，所以磁盘上的技能数和实际加载数对不上，是正常的。

工具是另一条线，开关在 agent.disabled_toolsets，和技能文件无关。

# 相关笔记

- Hermes 的技能按目录层级分组，DESCRIPTION.md 只是分类卡片（Context），同一套加载规则的另一半，讲技能放在哪一层。
- 六个 bot 在 Hermes 里各占一个 profile（Context），那篇记每个 bot 的目录与工具集裁剪。
