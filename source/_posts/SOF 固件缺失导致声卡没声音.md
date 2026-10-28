---
title: "SOF 固件缺失导致声卡没声音"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

Fedora 装完后没有声音，音频设备不可用，像是驱动/固件没装。

# 结论

内核日志直接点名：`sof-audio-pci-intel-tgl: SOF firmware and/or topology file not found`（要找的是 `intel/sof/sof-rpl.ri`）。这台 Raptor Lake 机器的声卡 DSP 需要 SOF 固件，而 `sof-firmware` 包没装。

# 解决方案

```bash
sudo dnf install sof-firmware
sudo systemctl reboot
```

重启让驱动重试加载固件即可。
