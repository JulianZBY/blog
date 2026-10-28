---
title: "Nous Portal 的设备登录失败"
date: 2026-10-20
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 背景

Hermes 桌面端登录 Nous Portal 时，点“继续”之后又退回“继续”，点多少遍都过不去。

# 分析

Portal 的登录和 CAPTCHA 先失败了，设备授权拿不到，这是已知问题 #20605。反复点继续，只是把同一条已经失败的路再走一遍。

# 解决方案

这台机器不登 Portal 也能用，本地功能不受影响，不必卡在这一步。要用 Portal 的话，等它那边的登录链路修好再试。

# 相关笔记

- 六个 bot 在 Hermes 里各占一个 profile（Context），同一段搬迁期间撞上的登录问题。
