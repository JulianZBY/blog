---
title: "Hyprland 键位对齐 DMS 默认"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

用 Noctalia Shell + Hyprland，想要 DankMaterialShell（DMS）风格的完整窗口/工作区键位。

# 结论

不用自己凭感觉编，DMS 官方默认键位就在它仓库的 `hypr-binds.lua` 里（现在官方就是 Lua 格式），直接抓下来逐条映射最可靠。最终 112 条绑定、零重复，全部经 `hyprctl binds` 注册验证。

# 解决方案

键位写进 `~/.config/hypr/conf/` 的绑定文件，要点：

- 窗口：`SUPER+F/Shift+F` 最大化/全屏，`SUPER+T` 浮动，`SUPER+W` 分组
- 移动：`SUPER+Shift+方向` 扔窗口，`SUPER+Ctrl+↑/↓` 扔工作区，`SUPER+Ctrl+←/→` 切显示器
- 工作区：`SUPER+U/I` 前后切，`SUPER+Shift+U/I` 交换顺序
- 分工：`SUPER+S` scratchpad、`SUPER+A` 控制中心、`SUPER+Alt+L` 锁屏、`SUPER+Shift+P` DPMS

两个注意：`SUPER+Shift+E` 会不弹窗直接退出会话，小心误触；DMS 有而 Noctalia 没有的功能（总览、取色器、键位速查表等）没法映射。
