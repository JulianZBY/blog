---
title: "六个 bot 在 Hermes 里各占一个 profile"
date: 2026-10-20
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 背景

六个 bot 原来挤在 openmausbot 一个应用里。2026-10-19 夜里搬进 Hermes 的 Bot Mode，到 20 日凌晨搬完。现在 curator、tutor、researcher、ghostwriter、diagnostician、toolsmith 各自是一个 profile。Chief of Staff 撤了，Hermes 自己派活，中间少一层。

# 名字

单字的职业英文名，显示名和 profile 名一样。旧应用里的角色名不用了，名字跟着职责走，不跟应用走，以后换工具不用改名。

# 目录

一个 bot 一个目录，`~/.hermes/profiles/<名字>/` 下面这几样：

- `SOUL.md` 人格
- `profile.yaml` 显示信息
- `config.yaml` 设置
- `memories/MEMORY.md` 记忆
- `skills/` 技能
- `cron/` 定时任务

SOUL、技能、状态文件手改没事。`config.yaml` 别直接改，走 `hermes -p <bot> config set`，直接改的话别处读到的还是旧值。

# 工具

用不着的技能全局关了：claude-code、codex、opencode、google-workspace、notion、teams-meeting-pipeline、airtable、box。

工具集按职责裁。curator、tutor、ghostwriter 没有 terminal；researcher 也没有，但留着 browser、web 和代码执行；diagnostician 和 toolsmith 留着 terminal 和 browser，他们的活要用。`message_agent` 互发消息不受影响。

# 例行

curator 每周日 20:00 盘一次库，库在 `/mnt/Data/Vault`。tutor 每天 21:00 推复习，这个时间写在 cron 里，不属于访谈该问的字段。tutor 的活也从背卡片扩到讲题、出题、排学习计划，牌组还没建，素材等用户给文章。ghostwriter 的写作样本和模板目录还空着，第一次派活时问一次。

# 相关笔记

- 2026-10-18 建队复盘（Context），那天记怎么设计和踩了哪些坑，这篇记它第二天变成了什么样。
- 理想中的Agent构思（Applies），里面提的按需启用，这次落在关技能和裁工具集上。
- Obsidian笔记指南（Applies），周日盘库照这份规范走。
- 搬迁时碰到的几个环境问题：连接中断导致的消息重投、Nous Portal 的设备登录失败、Linux和Windows双系统时钟问题、桌面端首次引导重复触发。
- 技能什么时候会被加载：Hermes 的技能加载先按 platforms 声明过滤、Hermes 的技能按目录层级分组，DESCRIPTION.md 只是分类卡片，那两篇讲加载规则，本篇只摆目录和裁剪结果。
