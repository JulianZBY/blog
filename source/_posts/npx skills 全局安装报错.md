---
title: "npx skills 全局安装报错"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

`npx skills add ... -g` 装到全局时总报 `PromptScript: PromptScript does not support global skill installation`。

# 结论

上游 bug：PromptScript 是 1.5.5 之后才加进注册表的 agent，它的检测逻辑有毛病；修复 PR #1571 已合入但**截至 2026-10 尚未发版**（npm 最新 1.7.4 仍带此 bug）。文件照常落进 `~/.agents/skills/`，工具照常能读到——报错无害。

# 解决方案

排序：**忽略红字**（最省）> 显式 `-a` 点名 agent > 固定旧版 `npx skills@1.5.5`（能用，但损失几个月的修复，下策）。用不固定版本的 `npx skills`，等 #1571 发版后自动就好了，零操作。
