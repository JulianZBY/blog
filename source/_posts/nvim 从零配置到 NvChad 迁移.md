---
title: "nvim 从零配置到 NvChad 迁移"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

nvim 从零开始配置，目标：极简、贴近实际开发场景（VSCode 使用习惯）。

# 结论

演进路径：lazy.nvim 手搓 → 参考三发行版出过 19 插件清单 → 最终**迁移到 NvChad starter**（内置插件 + 白送功能，比自己维护省心）。当前状态：

- 底座：NvChad starter，配色走 Noctalia 的 matugen 模板（生成到 NvChad 读取的 themes 目录，随壁纸动态变色）
- 文件：yazi（`leader+e`），配 zoxide/fzf
- LSP 五语言已验证：lua_ls / pyright / clangd / ts_ls / jdtls（pyright 类型诊断实测工作，`gd` 跳转、`K` 文档）
- 终端：toggleterm（`leader+t`），leap 跳转，mini.ai 文本对象

两个误判案例值得记住：打引号光标不进引号中间——**是 fcitx5 输入法的锅，不是 mini.pairs**；`jk` 当 Esc 在 visual 模式无效是方案已知限制。
