---
title: "Hermes 的技能按目录层级分组，DESCRIPTION.md 只是分类卡片"
date: 2026-10-20
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 背景

Hermes 的技能目录里带一层分类文件夹，很容易把其中的 DESCRIPTION.md 当成技能本身。它其实只是一张卡片。

# 机制

`skills/<分类>/DESCRIPTION.md` 是这个分类的简介，不跑流程，也不带能力。

真正的技能在 `<分类>/<技能名>/SKILL.md`。技能也可以不归分类，直接放在第一层，写成 `<技能名>/SKILL.md`。unslop 和 vault-note-taking 就是这样，分别在 `~/.hermes/profiles/curator/skills/unslop/` 和 `~/.hermes/profiles/curator/skills/vault-note-taking/`。

发现是递归的，放在哪一层都会被找到并生效。

# 相关笔记

- Hermes 的技能加载先按 platforms 声明过滤（Context），同一套加载规则的另一半，讲哪些技能会进桌面列表。
- 六个 bot 在 Hermes 里各占一个 profile（Context），那篇记每个 bot 的目录与工具集裁剪。
