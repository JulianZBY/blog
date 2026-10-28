---
title: "NTFS 与 exFAT 分区挂载权限"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

`/mnt/Data`（exFAT）和 `/mnt/Windows`（NTFS）挂载后所有文件归 root，普通用户没法随便写。

# 结论

fstab 里两行都没写 `uid/gid`，挂载后文件自然全归 root。exFAT/NTFS 没有真正的 Unix 权限位，权限是挂载时"模拟"的，全靠挂载选项声明。

# 解决方案

fstab 中对应两行加上：

```
uid=1000,gid=1000,umask=000,nosuid,nodev,nofail,x-gvfs-show
```

NTFS 那行再加 `windows_names`，禁止创建 Windows 非法文件名（如带 `:`），避免 Windows 启动出问题。改完 `sudo systemctl daemon-reload && sudo mount -a` 生效。

两个坑：
- NTFS 挂载后只读，多半是 Windows 快速启动/休眠锁了盘，去 Windows 跑 `powercfg /h off` 或彻底关机。
- `umask=000` 是所有用户全权限，个人机无所谓；多用户机改 `umask=077`。

# 相关笔记

- Linux和Windows双系统时钟问题（Context），同为双系统共存的坑。
