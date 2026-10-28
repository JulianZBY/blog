#!/usr/bin/env python3
"""把 Vault 里标记「发布: true」的笔记同步到 Hexo 并构建。

用法: python3 publish.py [--no-build] [--no-push]
流程: 扫描 /mnt/Data/Vault 根目录笔记 → 挑出 发布:true 的 →
      转换 wikilink/属性后写入 source/_posts/（只清理自己上次生成的文件）→
      hexo generate → 有远端时 git commit+push。
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

VAULT = Path("/mnt/Data/Vault")
POSTS = Path(__file__).resolve().parent / "source" / "_posts"
MANIFEST = Path(__file__).resolve().parent / ".publish-manifest.json"

def parse_frontmatter(text):
    """解析《仓库笔记规范》格式的 frontmatter；返回 (props, body)。
    支持 key: value 和 key: + 缩进列表项；值保留原始字符串（含引号/[[..]]）。"""
    if not text.startswith("---"):
        return {}, text
    m = re.search(r"\n---\s*(\n|$)", text[3:])
    if not m:
        print(f"  警告: frontmatter 未闭合，属性被忽略", file=sys.stderr)
        return {}, text
    props, last_key = {}, None
    for line in text[3:3 + m.start()].splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and last_key:
            props.setdefault(last_key, []).append(item.group(1).strip())
            continue
        kv = re.match(r"^([^:\s][^:]*):\s*(.*)$", line)
        if kv:
            last_key, val = kv.group(1).strip(), kv.group(2).strip()
            props[last_key] = val if val else []
        else:
            print(f"  警告: 无法解析行 {line!r}", file=sys.stderr)
    return props, text[3 + m.end():]

def unquote(v):
    return v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'" else v

def is_true(v):
    return isinstance(v, str) and unquote(v).lower() == "true"

def strip_wikilinks(props_value):
    """'[[规范]]' → '规范'；列表递归处理。"""
    def one(v):
        m = re.match(r"^\[\[([^]|#]+)(?:#[^|]+)?(?:\|(.+))?\]\]$", unquote(v))
        return (m.group(2) or m.group(1)).strip() if m else unquote(v)
    if isinstance(props_value, list):
        return [one(v) for v in props_value]
    return one(props_value)

def convert_body(body):
    """正文 wikilink 转纯文本；图片嵌入 ![[x]] 留占位注释。代码块内不动。"""
    out, in_fence = [], False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        line = re.sub(r"!\[\[([^\]]+)\]\]",
                      r"<!-- 附件图片 \1 未随发布迁移，请手动处理 -->", line)
        line = re.sub(r"\[\[([^]|#]+)(?:#[^|]+)?(?:\|([^\]]+))?\]\]",
                      lambda m: (m.group(2) or m.group(1)).strip(), line)
        out.append(line)
    return "\n".join(out) + "\n"

def main():
    build = "--no-build" not in sys.argv
    push = "--no-push" not in sys.argv
    selected = {}
    for note in sorted(VAULT.glob("*.md")):
        props, body = parse_frontmatter(note.read_text(encoding="utf-8"))
        if "发布" in props and not is_true(props["发布"] if isinstance(props["发布"], str) else props["发布"][0] if props["发布"] else ""):
            continue
        if is_true(props.get("发布", "")):
            selected[note.stem] = (props, body)
    print(f"选中 {len(selected)} 篇: {', '.join(selected) or '（无）'}")

    # 只删上次由本脚本生成的文章，手写文章（hexo new post）不受影响
    prev = set(json.loads(MANIFEST.read_text(encoding="utf-8"))) if MANIFEST.exists() else set()
    for name in prev:
        (POSTS / name).unlink(missing_ok=True)
    for stem, (props, body) in selected.items():
        fm = ["---", f"title: \"{stem.replace(chr(34), '')}\""]
        date = unquote(str(props.get("创建时间", "")))
        if date:
            fm.append(f"date: {date}")
        tags = strip_wikilinks(props.get("标签", []))
        if tags:
            fm.append("tags:")
            fm += [f"  - \"{t}\"" for t in tags]
        cats = strip_wikilinks(props.get("分类", []))
        if cats:
            fm.append("categories:")
            fm += [f"  - \"{c}\"" for c in (cats if isinstance(cats, list) else [cats])]
        fm.append("---")
        (POSTS / f"{stem}.md").write_text("\n".join(fm) + "\n\n" + convert_body(body),
                                          encoding="utf-8")
        print(f"  已转换: {stem}")

    MANIFEST.write_text(json.dumps(sorted(f"{s}.md" for s in selected), ensure_ascii=False),
                        encoding="utf-8")

    if build:
        hexo = Path(__file__).resolve().parent / "node_modules" / "hexo" / "bin" / "hexo"
        r = subprocess.run(["node", str(hexo), "clean"], cwd=Path(__file__).resolve().parent,
                           capture_output=True)
        r = subprocess.run(["node", str(hexo), "generate"], cwd=Path(__file__).resolve().parent)
        if r.returncode:
            sys.exit("hexo generate 失败")

    if push:
        blog = Path(__file__).resolve().parent
        if subprocess.run(["git", "-C", str(blog), "remote"], capture_output=True, text=True).stdout.strip():
            for cmd in (["add", "-A"], ["commit", "-m", "publish: sync from vault"],
                        ["push"]):
                r = subprocess.run(["git", "-C", str(blog)] + cmd, capture_output=True, text=True)
                if r.returncode and "nothing to commit" not in r.stdout + r.stderr:
                    sys.exit(f"git {cmd[0]} 失败: {r.stderr}")
            print("已 commit+push，GitHub Actions 会自动部署")
        else:
            print("（无 git 远端，跳过 push）")

if __name__ == "__main__":
    main()
