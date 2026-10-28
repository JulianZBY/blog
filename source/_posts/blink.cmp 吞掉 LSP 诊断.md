---
title: "blink.cmp 吞掉 LSP 诊断"
date: 2026-10-24
tags:
  - "问题排查"
categories:
  - "软件工具"
---

# 问题现象

nvim 里 lua_ls 对明显的语法错误一条诊断都不报，补全却正常。

# 结论

不是 root_dir 问题，是 **blink.cmp 把 LSP 客户端能力声明改坏了**：`blink.cmp.get_lsp_capabilities()` 只声明了"我能补全"，没合并 Neovim 默认能力，丢掉了 `publishDiagnostics`——lua_ls 一看客户端说不能接收诊断，就一条都不发。决定性实验：绕开 blink、用默认 capabilities 直接启动 lua_ls，语法错误立刻报红。根因在 blink 源码：`plugin/blink-cmp.lua` 调 `get_lsp_capabilities(user_caps)` 时没传第二个参数 `include_nvim_defaults`。

# 解决方案

blink 的 config 里补一行，显式合并默认能力：

```lua
config = function(_, opts)
  require('blink.cmp').setup(opts)
  vim.lsp.config('*', { capabilities = require('blink.cmp').get_lsp_capabilities(vim.lsp.config['*'].capabilities, true) })
end,
```

另：`root_dir = nil` 是独立小问题——单文件分析不受影响，但真实项目里跨文件跳转不准，值得一起修。

# 相关笔记

- nvim 从零配置到 NvChad 迁移（Context），同期 nvim 配置工作。
