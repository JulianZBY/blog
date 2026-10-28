---
title: "Noctalia 的 nvim 模板颜色不生效"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

在 Noctalia 设置中心勾了社区 nvim 模板（matugen），但 nvim 颜色没生效。

# 结论

两件事都没到位：模板只生成了 `lua/matugen.lua`，**没有 `init.lua` 调用它**（模板作者默认你自己有 init.lua 并 `require('matugen').setup()`）；而且模板依赖 `base16-colorscheme`，全新 nvim 里**插件根本没装**。

# 解决方案

写一个 16 行的 `~/.config/nvim/init.lua`：引导 lazy.nvim → 装 `RRethy/base16-nvim` → 插件加载后执行 `require("matugen").setup()`。验证方式：headless 启动 nvim 看 `Normal` 前景色是否等于模板里的 base05。

额外福利：模板自带 SIGUSR1 热更新——Noctalia 里换壁纸/主题色会重新生成 `matugen.lua` 并发信号，已打开的 nvim 自动换色。

# 相关笔记

- nvim 从零配置到 NvChad 迁移（后续），这套 matugen 配色后来在 NvChad 里也接上了。
