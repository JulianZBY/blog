---
title: "Flatpak 应用不跟随亮暗色（缺 portal 后端）"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

Noctalia 切亮暗色时，Flatpak 应用纹丝不动，原生应用却正常。

# 结论

链条断在 portal：沙盒应用不能直接读 dconf，唯一途径是 D-Bus 接口 `org.freedesktop.portal.Settings` 读 `org.freedesktop.appearance` → `color-scheme`。本机实测这个接口根本不存在——装了 portal 调度器（xdg-desktop-portal），但**一个后端都没装**，`portals.conf` 里指向的 `hyprland;gtk` 两个后端都不存在。Noctalia 没问题（`prefer-dark` 确实写进了 gsettings），但没有任何后端把它广播给沙盒应用。且 `xdg-desktop-portal-hyprland` 只实现 ScreenCast/Screenshot/GlobalShortcuts，**不实现 Settings**，必须搭配 gtk 后端。

# 解决方案

```bash
sudo dnf install xdg-desktop-portal-gtk xdg-desktop-portal-hyprland
systemctl --user restart xdg-desktop-portal
```

验证：

```bash
gdbus call --session --dest org.freedesktop.portal.Desktop \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.portal.Settings.ReadOne \
  org.freedesktop.appearance color-scheme
# 暗色应返回 (<uint32 1>,)，切亮色后变 2
```

已装的 `adw-gtk3` Flatpak 主题负责 GTK3 应用的"涂装"，和这条偏好通道互补，不用动。

# 相关笔记

- 应用不跟随亮暗色（Noctalia 双模式）（前因），上游写 gsettings 的那半边。
