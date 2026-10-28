---
title: "Hyprland 全局模糊没效果"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

Hyprland 开了模糊，但窗口看起来完全没有模糊效果。

# 结论

直觉正确：模糊一直开着，但所有窗口都是全不透明（opacity 1.0），模糊没有可见的半透明表面可作用。要出磨砂玻璃效果，模糊 + 透明度缺一不可。

# 解决方案

`~/.config/hypr/conf/settings.lua`（按官方 0.56 文档核对过变量）：

```lua
-- 全局微微透明
active_opacity = 0.95
inactive_opacity = 0.90
-- 磨砂玻璃预设
blur: size 8, passes 3, noise 0.05, contrast 0.9, xray true（浮动窗口省 GPU）, popups true（右键菜单也模糊）
```

`~/.config/kitty/kitty.conf` 加 `background_opacity 0.85`，只有终端背景半透明，文字依然清晰。

微调：更糊/更清动 `size`（4 轻 ~ 16 重）和 `passes` 同步升降；嫌全局透明发虚就把 `active_opacity` 调回 1.0 只留 kitty 透明。
