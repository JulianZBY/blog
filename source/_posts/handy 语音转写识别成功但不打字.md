---
title: "handy 语音转写识别成功但不打字"
date: 2026-10-27
categories:
  - "问题排查"
---

# 问题现象

handy（语音转写工具）识别成功，但不往光标处打字。

# 排查过程（三层修复链，全部保留，勿还原）

1. **全局快捷键失效**：handy 0.9.8 的 HandyKeys 要读 `/dev/input` → 用户加入 `input` 组（`sudo usermod -aG input`）+ 重新登录。
2. **麦克风无可用输入**：系统缺 `alsa-ucm`（Fedora 44 包名，Arch 才叫 alsa-ucm-conf）→ sof-hda-dsp 只剩 stereo-fallback profile、WirePlumber 激活失败（Object activation aborted）→ `sudo dnf install -y alsaucm` + 重启 wireplumber；默认输入从扩展坞 USB mono 切回内置麦。
3. **打字丢字**：ydotool 走实体按键映射，只能打 ASCII，中文静默丢弃 → Wayland 中文转写必须走剪贴板粘贴：用户级 ydotool 服务（`~/.config/systemd/user/ydotool.service`，socket=`%t/.ydotool_socket`）+ handy `paste_method: ctrl_v`（wl-copy + ydotool 模拟 Ctrl+V）。

# 最终根因（用户自己发现）

handy 的转写弹窗弹出时把自己的 dock 顶起，光标焦点变了，粘贴打去了别处。关掉弹窗即好。

# 教训

- 三层都是真故障，修复链值得保留；但「修了三层症状还在」本身是重要信号——应回到原始症状做回归验证，而不是继续修下一层。规矩见 排障规范。
- Wayland 输入事实：wtype 在 GNOME/Mutter 上不可用（无 zwp_virtual_keyboard_manager）；uinput 系（ydotool）可用但只认 ASCII；中文输入走剪贴板是正路。
- handy 退出时会用内存设置整体覆写 `settings_store.json`——外部改配置必须在 handy 停止时改。
- ydotool 系统级服务（Fedora 包）socket 在 `/tmp/.ydotool_socket` 且 root:root 0600，CLI 默认找 `$XDG_RUNTIME_DIR/.ydotool_socket` → 必须用用户级服务。
- 排障手法：`strings` 挖二进制枚举（TypingTool=wtype/ktype/dotool/ydotool/xdotool）、`ps` 高频轮询抓 argv、`~/.local/bin` 放同名 wrapper 拦截、`journalctl --user --unit handy-app.service`（handy 用 systemd-run 常驻，nohup 启动日志会被吞）。

# 相关笔记

- 排障规范 —— Applies：本案例催生的排障纪律，每修一层回归验证原始症状。
- 疑难杂症索引 —— 同类：排障笔记的检索入口，本篇已补入。
- SOF 固件缺失导致声卡没声音 —— 同类：同属音频链路排障。
