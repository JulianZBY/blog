---
title: "smart_parking_system 编译失败（JDK 过新）"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

smart_parking_system 后端 `./mvnw spring-boot:run` 编译必崩，报 `EndPosTable` 相关错误（另有一次 `./mvnw: /bin/sh^M: bad interpreter`，是 Windows 换行符，`dos2unix` 类处理解决）。

# 结论

不是项目坏了：Spring Boot 3.4.5 托管的 Lombok 版本不支持太新的 JDK，本机全局 JDK 27 编译时崩出 `EndPosTable`。项目本身就是 target Java 21。

# 解决方案

用 mise 装 Temurin JDK 21，并在 `Java/backend/mise.toml` 把该目录固定到 21——全局的 JDK 27 其他项目照常用，不受影响：

```bash
mise use -i temurin@21   # 在 Java/backend 目录下
```

之后直接重跑 `./mvnw spring-boot:run -Dspring-boot.run.profiles=h2local`，shell 里的 mise 会自动切到 21。mise 提示 untrusted config 就 `mise trust`。

# 相关笔记

- mise 任务秒退（端口残留进程）（Context），同一个项目的运行问题。
