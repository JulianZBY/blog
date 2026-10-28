---
title: "家目录缺 Pictures Videos 等用户目录"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

家目录里没有 Pictures、Videos、Documents 等常用目录。

# 结论

不是什么包缺失得玄乎，就是 `xdg-user-dirs` 没装：`xdg-user-dirs-update` 和 `~/.config/user-dirs.dirs` 都不存在。

# 解决方案

```bash
sudo dnf install xdg-user-dirs
xdg-user-dirs-update
```

自动按 locale 创建全套目录并写入 `~/.config/user-dirs.dirs`。想要中文目录名，装完后配中文 locale 跑 `xdg-user-dirs-update --force` 或手改该文件。
