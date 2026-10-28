---
title: "kitty 关闭窗口免确认"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

kitty 关闭窗口时总弹确认框。

# 结论与解决方案

`~/.config/kitty/kitty.conf` 加一行：

```
confirm_os_window_close 0
```

按 `ctrl+shift+f5` 重载配置生效。注意这同时关掉了"该窗口有运行中程序"的提示，误关会直接终止里面的进程。
