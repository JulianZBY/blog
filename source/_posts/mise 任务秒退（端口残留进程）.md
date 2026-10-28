---
title: "mise 任务秒退（端口残留进程）"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

`mise run dev`（并行起 web / backend / ocr 三个任务）里 backend 4.5 秒秒退，Maven 报一堆 ERROR；加"自动清端口"的加固后反而一行输出都没有直接退出。

# 结论

两个问题叠着：

1. **秒退真因**：8080 上有之前没死干净的 JVM，占着端口还锁着 H2 库，新 backend 绑端口失败直接退。
2. **加固反坑**：给任务加的 `fuser -k 8080/tcp;` 在端口没人占时返回 1，mise 任务脚本按 `-e` 语义执行，一个非零返回值把整个脚本带走。

# 解决方案

三处任务（backend / backend-mysql / web）启动前都写成：

```toml
fuser -k 8080/tcp || true
```

`|| true` 吞掉"端口本来就没人"的正常情况，从此端口残留自愈。验证过 `mise run backend` 起来后 `/v3/api-docs` 返回 200。

风险一条：`fuser -k` 不认进程是谁，哪天别的服务占 8080 也会被杀——本机 8080 专用，实际影响小。

# 相关笔记

- smart_parking_system 编译失败（JDK 过新）（Context），同项目的 mise 固定 JDK。
