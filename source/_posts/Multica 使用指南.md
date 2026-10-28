---
title: "Multica 使用指南"
date: 2026-10-27
tags:
  - "AI Agent"
categories:
  - "软件工具"
---

# Multica 使用指南

Multica 是「人与 AI 智能体一起工作的平台」：把 Claude Code、Codex、pi 等 CLI 智能体当成**同事**放进一个工作区——派活（issue）、执行（runtime）、留痕（评论）、自动化（autopilot）、沉淀（skill/知识库）。可以理解为 **AI Agent 界的 Linear + GitHub Actions**。

本篇按本工作区的实际配置写，读完就能上手。

## 核心概念（一分钟版）

| 概念 | 是什么 | 你工作区里的对应 |
|---|---|---|
| 工作区 Workspace | 一切发生的容器 | Self Improvement（SELF） |
| 成员 Member | 人类用户 | 你（julianzby） |
| 智能体 Agent | 有名字、指令、模型的 AI 同事 | Mika、复盘官、路径官 |
| Runtime | 智能体干活用的真机 | 你的 Fedora（Pi runtime） |
| Issue | 活儿的载体：目标、过程、结果都在这 | 每晚的「每日复盘」就是一个 issue |
| Autopilot | 定时/事件触发的自动化 | 复盘官的每天 22:30 |
| Squad | 一组智能体+一个 Lead，整组接活 | 还没建 |
| Project | 多个 issue 共享一个 outcome 时的绑定 | 还没建 |
| Mention | 评论里 @ 某智能体 = 给它排一次运行 | 见下文速查 |

## 日常就三件事

1. **聊天问 Mika**：一次对话能解决的事（解释、比较、读东西、小改动判断）直接说。Mika 是默认管家，会自己决定"答在聊天"还是"建 issue 派活"。
2. **Issue 派活**：需要工具、跨多轮、要留记录的活 → 建 issue 指派给某个智能体。**issue 是唯一带所有权的交付物**——过程评论、最终结果、附件都在上面，聊天窗口里说的话转身就没了。
3. **评论 @ 驱动**：活干到一半要换人/加人，在 issue 评论里 @ 对方智能体即可，它会被排队唤醒。

## 你的三位同事

| 智能 | 怎么叫 | 什么时候叫 |
|---|---|---|
| **Mika** | 聊天直接说；或 issue 指派 | 默认 everything：管家、编排、建智能体、查平台 |
| **复盘官** | 每晚 22:30 自动跑（autopilot）；也可手动指派 issue | 想复盘某一天、想立规矩、想改规范 |
| **路径官** | issue 指派 + 丢任务书 | 给一个模糊目标，要一条"真实走通"的可复现工作流 |

智能体之间可以互相委托：在 issue 评论里 @ 对方即排队交接，权限判定看委托链顶端的人类（= 你），所以现在怎么串都通。

## Mention 速查（重要）

- 只有 `@agent` 和 `@squad` 触发运行；**@人类成员只是链接，不触发任何东西**
- 纯文本 `@路径官` 无效，必须是标准提及链接（界面输入 @ 选人即可）
- 目标正忙 → 委托排队，等它跑完自动重放，不丢
- `@all` 是广播且会抑制 assignee 的自动触发——慎用
- 私有智能体：看得到 ≠ 叫得动，调用走权限门

## CLI 速查（智能体代劳，你了解即可）

```bash
multica issue list --output json          # 看所有 issue
multica issue get <id> --output json      # issue 详情
multica issue comment add <id> --content-file <path>  # 评论
multica issue status <id> in_review       # 改状态
multica agent list --output json          # 智能体名册
multica autopilot list --output json      # 自动化列表
```

## 学习资源

**官方文档**（最权威，支持中文）：
- 中文文档首页：https://multica.ai/docs/zh
- 完整教程（推荐第一个看，用一个个人网站项目串起全部概念）：https://multica.ai/docs/zh/tutorial
- 开源仓库：https://github.com/multica-ai/multica

**视频**（社区中文教程，来自搜索结果，未逐一验证有效性）：
- [Multica 零基础搭建 AI Agent 管理系统（B站）](https://www.bilibili.com/video/BV1DT5y6jEYA/)——分章节入门：是什么/安装/看板/autopilot
- [Multica 实战！用 Codex/Claude Code/Hermes/Opencode 构建 AI 编程闭环（B站，约1小时）](https://www.bilibili.com/video/BV1DpE16fEeY/)——最完整的实操系列
- [Multica 深度解读：把 AI 编程 Agent 变成真正的团队成员（B站）](https://www.bilibili.com/video/BV17PYp6yEjg/)——概念向，讲清它和 Jira/Actions 的关系
- 官方中文文档首页底部有「看一段演示」的官方视频入口
- 配套模板仓库：https://github.com/it235/multica-best-practices （可直接复制的 Agent/Squad 指令模板）

## 已知的坑（本工作区实测）

- 智能体回复投递到你**发起对话的界面**；不经过飞书，除非你的接入通道本身是飞书
- 定时任务（autopilot）深夜 @ 其他智能体也叫得动：权限回退到 autopilot 创建者
- 智能体的"记忆"不在它脑子里：短期在 pi 日志（可搜索），长期在 工作流笔记 和规范笔记——**改文件即改行为**

## 相关笔记

- 仓库笔记规范 — Context：本篇按它写；智能体行为准则的入口篇
- 复盘官 — Confirms：每晚自动把当天问题沉淀进本库的执行者
- 路径官 — Confirms：把模糊目标变成可复现工作流的执行者
