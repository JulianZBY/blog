---
title: "dnf 下载提速与 Fedora 44 默认值"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

想优化 dnf：多线程下载、最快镜像、跳过弱依赖。照老教程写了一堆 `[main]` 配置项后被质疑冗余。

# 结论

质疑正确。Fedora 44 把发行版默认值放在 drop-in 文件 `/usr/share/dnf5/libdnf.conf.d/20-fedora-defaults.conf`（`best=False`、`pkg_gpgcheck=True`、`skip_if_unavailable=True`），加上 dnf5 上游默认（`installonly_limit=3`、`clean_requirements_on_remove=True`），老教程里那五行**全部多余**。drop-in 优先级高于 `dnf.conf`，系统升级改默认值也不会互相干扰。

# 解决方案

`/etc/dnf/dnf.conf` 最小正确版本，只写要的三个优化项：

```ini
[main]
max_parallel_downloads=10
fastestmirror=True
install_weak_deps=False
```

教训：改配置前先查这个 Fedora 版本的默认值来源，别抄老教程。
