---
title: "Hexo 用法"
date: 2026-10-28
tags:
  - "Hexo"
  - "Obsidian"
categories:
  - "工具配置"
---

# Hexo 用法

本机博客的技术底账：Hexo 框架 + GitHub Pages 部署，Obsidian 笔记可一键发布。项目在 `/mnt/Data/Projects/blog`（home 下有软链接 `~/Projects/blog`），线上地址 `https://julianzby.github.io/blog/`，仓库 `JulianZBY/blog`（公开）。

## 目录结构

```
blog/
├── _config.yml          站点配置（标题、url、root、主题名）
├── _config.fluid.yml    Fluid 主题配置（覆盖默认值，改外观只动这个）
├── publish.py           发布脚本：Vault → 博客
├── hexo                 包装脚本（exFAT 专用，见下）
├── source/
│   ├── _posts/          正式文章（脚本生成的 + 手写的可以共存）
│   ├── _drafts/         草稿（已被 gitignore，不会公开）
│   └── about/           「关于」页
├── public/              构建产物（gitignore，不用管）
└── .github/workflows/pages.yml   push 后自动构建部署的 Actions
```

## 常用命令

`/mnt/Data` 是 exFAT，不支持符号链接，npm 装不了 `node_modules/.bin`，所以 `npx hexo` 不可用。两种替代：

```sh
./hexo server          # 本地预览 http://localhost:4000
./hexo new post "标题"  # 手写文章，落在 source/_posts/
./hexo new draft "标题" # 草稿，落在 source/_drafts/
./hexo generate        # 纯构建
python3 publish.py     # 完整发布（见下）
```

## 发布流程（Obsidian 笔记 → 线上）

1. 想发布的笔记加上属性 `发布: true`，不用挪动位置
2. 跑 `python3 publish.py`（在 `~/Projects/blog` 下），它会：
   - 扫描库根目录笔记，挑出 `发布: true` 的
   - 转换后写入 `source/_posts/`（只清理自己上次生成的文件，手写文章不受影响）
   - `hexo clean` + `generate` 构建
   - 有远端时自动 `git commit` + `push`
3. push 触发 GitHub Actions 自动构建并部署，约一分钟后线上生效

**下线文章**：删掉笔记里的 `发布` 属性（或改 false），重跑脚本即可。

**转换规则**：`链接` 和 `别名` 转成纯文本；代码块内不动；`<!-- 附件图片 图片 未随发布迁移，请手动处理 -->` 嵌入**不会**迁移，转成 HTML 注释占位，需要图就手动把图放进 `source/images/` 再改成 Markdown 图片语法。笔记的 `创建时间`→文章日期，`标签`/`分类` 去掉 wikilink 后原样带过去。

## 主题（Fluid）

改外观只动 `blog/_config.fluid.yml`（它是主题默认配置的完整覆盖副本），改完 `./hexo server` 实时预览。官方文档：https://hexo.fluid-dev.com/docs/ 。常见改动：首页 banner 背景图、导航栏、关于页内容（`source/about/index.md`）。

## 坑与注意

- **零文章时整站 404**：Hexo 在 `source/_posts/` 为空时不生成首页 `index.html`，部署后整站打不开（只剩 404 页）。所以务必保留至少一篇手写文章（现存 `source/_posts/welcome.md`），不要清空
- 构建时区：CI 跑在 UTC，会把文章日期往前推一天；已在工作流里固定 `TZ: Asia/Shanghai`，本地与线上路径一致
- exFAT 无符号链接：以后在这个目录装新依赖一律 `npm install --no-bin-links`
- 仓库必须公开（免费套餐限制），博客源码所有人可见；`source/_drafts/` 已 gitignore，草稿安全
- 换电脑迁移：clone 仓库后 `npm install --no-bin-links` 即可，publish.py 随仓库走

## 相关笔记

- 仓库笔记规范：本篇及 `发布` 属性的词汇都按它建，发布机制依赖其 frontmatter 约定
- Obsidian笔记指南：库的整体用法，发布机制的源头输入
- 工具配置：本篇所属分类
