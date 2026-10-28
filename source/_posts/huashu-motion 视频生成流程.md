---
title: "huashu-motion 视频生成流程"
date: 2026-10-27
tags:
  - "AI Agent"
categories:
  - "工作流"
---

# huashu-motion 视频生成流程

**触发场景**：需要一段动效/解说/发布视频，且希望产物是「可编辑的代码」而不是黑盒渲染文件时，想起这篇。

## 环境要求

- 本机只有 helium（Chromium 分支）没装 Chrome：`om doctor` 报错时 `export OM_CHROME=/usr/bin/helium-browser-bin`，`headless=new` 正常。

## 流程（2026-10-27 端到端跑通，「视频即代码」12.5s 1080p30 测试片）

1. `om new` 建项目
2. 写 `index.html`（合同：变量 / `data-om-id` / scene 标签 / 暂停 GSAP 时间线 / `OM.sfx` + `OM.music`）
3. `om check` → `om still` 逐帧看 → `om sound`（内置 devtool 方向 = synthwave）→ `om render`（约 30s）→ `om qa`
4. 交付 `out/*-v1.mp4`（实测 12.5s ≈ 2MB）

## 坑

- `index.html` 必须显式 `<script src="vendor/om.js">`——模板脚手架不带这行，漏了运行时报 `OM.music is not a function`。
- 堆叠场景的 section 要打 `data-layout-allow-occlusion`，否则 `om check` 一堆 text-overlap 误报（隐藏场景被当静止元素比对）。

## 遗留优化点

motion contrast 1.23 偏稳；结尾静止约 3s 略长；`--blur`、60fps 未用；studio 互动循环在聊天回合里不可用。

# 相关笔记

- 路径官 —— Context：「工作流」分类与「触发场景」字段的体系出处。
