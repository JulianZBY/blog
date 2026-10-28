---
title: "重启后进 TTY 不进桌面的解法"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

重启后默认进入 TTY 文字界面，不进桌面。hyprland-uwsm 入口选择时还报 "failed units detected"。

# 结论

默认启动目标是 `multi-user.target`（纯文字模式），greetd 装好了但开机没被拉起来。一条命令的事。

# 解决方案

```bash
sudo systemctl set-default graphical.target
# 本次开机立即生效（不重启）：
sudo systemctl isolate graphical.target
```

改完还是黑屏进 TTY 的话，说明图形会话启动失败，看 `journalctl -b -u greetd`。

uwsm 的 "failed units detected" 警告是另一件事：`/etc/xdg/autostart/nvidia-settings-user.desktop` 每次登录失败，uwsm 启动会话前检查到 failed unit 才提醒，见 hyprland-uwsm 警告 failed units（nvidia-settings 自启失败）。

# 相关笔记

- 浏览器每次启动弹钥匙环的解法（Context），greetd + noctalia-greeter 的配置在同一轮完成。
