---
title: "Mise 的使用"
date: 2026-10-12
tags:
  - "开发环境"
  - "版本管理"
  - "Mise"
categories:
  - "编程基础"
---

# 背景

曾经只需要全局安装包的某个特定版本就能正常进行开发，现在遇到了当前版本的python太新无法下载特定的包的问题，我曾经依赖于scoop这个包管理器，用于快速的安装各种开发环境，但是在版本管理这方面不足

于是我了解到了各种包的管理工具，比如nodejs有nvm等等，但是管理不同的包需要不同的管理工具，十分麻烦，于是了解到了Mise

# 使用

安装教程详见官网

## 配置相关问题

### Shell

- 对于bash，添加```eval "$(mise activate bash)"```到~/.bashrc
- 对于Powershell虽然也能添加```(&mise activate pwsh) | Out-String | Invoke-Expression```到$PROFILE 但是会导致powershell启动很慢
## Path

- 对于bash，`mise activate --shims YOUR_SHELL` 将shims添加到环境变量，但是这个命令不支持Windows
- 对于Windows手动添加`%LOCALAPPDATA%\mise\shims`到环境变量的PATH下，这是比较推荐的方式，因为不会拖慢powershell启动

## 临时调用

使用`mise exec 包@版本 -- 命令`的方式临时运行命令，比如

```
mise exec node@24 -- node --version
```

> 可以不指定@版本号，默认使用最新版本
## 安装

### 项目下

```
mise use 包@版本
```

这会在项目目录下自动创建mise.toml

### 全局

```
mise use 包@版本 -g
```

这会在~/.config/mise/ 下创建config.toml


## 配置文件

```toml
[tools]
node = "24"

[env]
NODE_ENV = "development"

[tasks.hello]
run = "node --eval 'console.log(process.env.NODE_ENV)'"
```

或者

```toml
[tasks]
build = "cargo build"
test = "cargo test"
lint = "cargo clippy"
```

其中tasks非常好用，task.后自定义名称，批量执行命令只需要mise run 自定义名称即可
