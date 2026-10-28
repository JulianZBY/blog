---
title: "Noctalia Greeter 无法记住上一次的会话选择的原因"
date: 2026-10-25
categories:
  - "问题排查"
---

Greeter 尝试保存 `sync.toml` 时，被 SELinux 拒绝了。 即使普通 Unix 文件权限看起来正常，SELinux 仍然可以单独阻止这个操作。

## 修复方法：为 Greeter 状态目录设置合适的 SELinux 标签

Fedora 的 SELinux 策略中有 `xdm_var_lib_t` 类型，用于显示管理器在 `/var/lib` 下的数据。

可以先将 Noctalia Greeter 的状态目录单独标记为这个类型，而不是关闭 SELinux 或放宽整个系统的权限。

### 1. 添加持久化标签规则

```
sudo semanage fcontext -a -t xdm_var_lib_t \
  '/var/lib/noctalia-greeter(/.*)?'
```

### 2. 应用标签

```
sudo restorecon -RFv /var/lib/noctalia-greeter
```
