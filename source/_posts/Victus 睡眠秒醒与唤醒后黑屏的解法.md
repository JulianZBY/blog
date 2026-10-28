---
title: "Victus 睡眠秒醒与唤醒后黑屏的解法"
date: 2026-10-20
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 背景

这台机器是 HP Victus，Fedora 上挂起有两个毛病。一是进 s2idle 的瞬间就被踢出来，等于没睡；二是真睡下去以后唤醒，内屏不亮，只能靠外接屏。

# 分析

秒醒的根因是 EC GPE 风暴。gpe6E 以约 3.7 次每秒持续触发，实测一次失败的挂起期间计数到 1663，把 ACPI 唤醒中断（IRQ 9）不停打响。日志里那句 "ACPI: PM: ACPI non-EC GPE wakeup" 只是唤醒通知，不是源头，照它去查会查错方向。

黑屏的根因在 i915 的 PSR、FBC 节能机制和这台机器的幽灵 eDP 打架。HP 的 VBT 在 DDI B 上多挂了一个并不存在的面板，恢复时 eDP 链路训练失败，日志里是 `[DPRX] Failed to enable link training`，内屏于是不亮。

# 解决方案

秒醒：自建一个 acpi-mask-ec-gpe.service，把 gpe6E 屏蔽掉。这套机器上一版的 Fedora 里就是这么修的，本次重装后丢了，需要重建。

黑屏：加内核参数 `i915.enable_psr=0 i915.enable_fbc=0 i915.psr_safest_params=1`，在上一套系统上验证有效。

更彻底的两条路，记下来备用。一是 VBT 覆盖：改三个字节，再用 `i915.vbt_firmware=` 加载，CachyOS issue 1043 里有做法，同型号在七次尝试中七次验证通过。二是等上游：内核 7.4 已合入正式修复（drm/i915/dp: wake DPRx on DPCD init）。

排查过程有六份报告，放在诊断师 profile 的 `reports/2026-10-20-suspend-failure*.md`。

# 相关笔记

- Linux和Windows双系统时钟问题（Context），同一次排障里发现的时间问题，RTC 走本地时间，与 Windows 双系统是同一条线索。
