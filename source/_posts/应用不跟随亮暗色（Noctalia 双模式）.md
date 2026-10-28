---
title: "应用不跟随亮暗色（Noctalia 双模式）"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

Noctalia Shell 里切了亮暗色，部分应用不跟随变化。

# 结论

Noctalia 有两套亮暗概念，别搞混（官方文档 docs.noctalia.dev/theming）：

| 配置 | 控制什么 |
|---|---|
| `[theme].mode` | **应用的亮暗**——写模板并同步 gsettings 的 `color-scheme` |
| `[theme].shell_mode` | 只改 **Noctalia 自己**的外观（顶栏、面板、启动器） |

只动 `shell_mode` 应用不会跟随；`sync_color_scheme`（默认 `true`）被关掉也会断掉同步。

# 解决方案

```bash
noctalia msg theme-mode-get        # 看当前模式
noctalia msg color-scheme-get      # 看 color-scheme 同步状态
gsettings get org.gnome.desktop.interface color-scheme
noctalia msg theme-mode-set dark   # dark | light | auto（持久化并同步应用）
```

配置文件 `~/.config/noctalia/`（v5 为 TOML）：`mode`、`shell_mode = "follow"`、`sync_color_scheme = true`。个别应用还不变就重启它（很多应用只读一次主题），并确认装了 `xdg-desktop-portal-gtk`——见下篇。

# 相关笔记

- Flatpak 应用不跟随亮暗色（缺 portal 后端）（后续），gsettings 有了还得有 portal 才能到达沙盒应用。
