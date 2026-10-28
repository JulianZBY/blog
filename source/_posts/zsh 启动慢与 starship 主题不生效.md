---
title: "zsh 启动慢与 starship 主题不生效"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

感觉 zsh 启动慢；另外 Noctalia 的 starship 主题切换后"没什么用"，颜色没变。

# 结论

两件事，两的结论：

**zsh 不慢。** 实测 `zsh -i` 完整启动 110–140ms（卡顿感一般从 300ms 起）。大头是 kitty 自身启动约 200ms 和开机后第一次开终端的磁盘冷缓存。唯一值得做的优化：compinit 改 24 小时缓存写法，省约 15ms。别再抠了。

**starship 主题真没生效，是竞态。** Noctalia 日志显示：切换主题瞬间它就去套用 starship 模板，但模板文件 1 秒后才下载完（`failed to open template input ... starship.toml`），失败后**不会自动重试**。

# 解决方案

```zsh
# ~/.zshrc 的 compinit 缓存写法
autoload -Uz compinit
if [[ -n ~/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi
```

starship：模板文件现已齐全，在 Noctalia 设置里重新触发一次（随便再换一次主题，或关掉再打开 starship 模板）即可写入 `~/.config/starship.toml`。

顺带两个小知识：主目录显示 `via 🐍 v3.15.0` 是因为家目录有个 `test.py`，starship 检测到 `.py` 文件就显示 Python 版本（删文件或 `[python] disabled = true`）；starship 的 `[!?]` 是 git 状态符号（`!` 已改未暂存、`?` 未跟踪）。
