---
title: "pi 接入 b.ai 的工具名映射"
date: 2026-10-24
tags:
  - "工具配置"
categories:
  - "软件工具"
---

# 问题现象

把 b.ai 的 Claude 模型接入 pi（openai-completions 协议）后，模型返回的工具调用全失败——Claude 规范认的工具名是首字母大写的 `Bash`/`Read`，pi 内部是小写 `bash`/`read`。

# 结论

协议差异问题，靠一个 pi 扩展双向改名解决：`~/.pi/agent/extensions/claude-tool-names.ts`（约 60 行）。

| 方向 | 钩子 | 做什么 |
|---|---|---|
| 出站请求 | `before_provider_request` | `model` 以 `claude` 开头时，把工具声明和历史 tool_calls 里的名字按 CC 规范改名（`bash`→`Bash` 等 17 个，与 pi 内置 stealth 模式同一张表） |
| 入站响应 | `message_end` | 把模型回的 `Bash` 等映射回小写 `bash`，工具正常执行，历史记录保持小写 |

只动表内名字，MCP/自定义工具透传；对官方 Anthropic OAuth 路径幂等。

# 解决方案

环测通过（`echo` 经改名环路正常执行）。两个提醒：流式输出中 UI 可能短暂显示 `Bash`，`message_end` 后修正，无实际影响；**b.ai 网关有静默换模型的迹象**（自称 Windows 11、说法语）——回答质量异常是平台侧问题，别怀疑配置。
