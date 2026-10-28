---
title: "hyprland-uwsm 警告 failed units（nvidia-settings 自启失败）"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

进 hyprland-uwsm 时每次都警告 "failed units detected"。

# 结论

user 会话里有个失败的单元 `app-nvidia\x2dsettings\x2duser@autostart.service`：`/etc/xdg/autostart/nvidia-settings-user.desktop` 开机自启 nvidia-settings 然后失败。uwsm 启动会话前会检查 failed units，检测到就报这个警告，不是 Hyprland 的问题。

在 Wayland 下 nvidia-settings 的显示器类设置（如 SyncToVBlank）会静默无效或报错，这个自启本来就没用；建个空 `~/.nvidia-settings-rc` 虽能让报错消失，但等于每次开机空跑一个无意义进程。

# 解决方案

用 XDG 规范的用户级覆盖禁用（不需要 sudo，同名文件覆盖系统目录的）：

```bash
mkdir -p ~/.config/autostart
printf '[Desktop Entry]\nType=Application\nExec=nvidia-settings -l\nHidden=true\n' > ~/.config/autostart/nvidia-settings-user.desktop
```

`Hidden=true` 即全局禁用，failed unit 消失。哪天回 X11 想自动加载 nvidia 设置，删掉这个覆盖文件即可，原文件完好。Wayland 下等效需求的替代工具：nvibrant（饱和度）、hyprsunset（色温）、LACT（风扇/功耗）。
