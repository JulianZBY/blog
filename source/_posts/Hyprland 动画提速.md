---
title: "Hyprland 动画提速"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

想让 Hyprland 所有动画整体变快；用嵌套表写法（`animation = { windows = ... }`）直接报错。

# 结论

两点：全局选项存在——新版动画系统是一棵树，`global` 是根节点，没单独设置的动画全部继承它；但 Lua 配置 API 不接受嵌套表，必须用 `hl.animation()` 逐条调用（报 `undefined-global hl` 是 lua-language-server 不认识运行时全局，无害）。

# 解决方案

`conf/settings.lua` 末尾一行：

```lua
hl.animation({ leaf = "global", enabled = true, speed = 2, bezier = "default" })
```

`speed` 单位是 0.1 秒：`2` = 0.2s，`1` = 极速，`3~4` = 比默认（8）略快。用 `hyprctl eval` 可以先在当前会话试效果再持久化。
