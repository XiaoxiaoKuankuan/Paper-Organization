"""
从隐藏 YAML 元数据同步每篇论文正文开头的中文基本信息卡。

作者、机构、发表时间和期刊/会议既是索引数据，也是读者打开论文页后必须立即
看到的信息。本脚本以隐藏 YAML 为唯一数据源，生成无边框的 Markdown 引用块，
避免手工维护两份内容产生漂移。默认模式会初始化或更新全部论文页；``--check``
只检查磁盘内容是否同步，适合本地验收和 GitHub Actions。

脚本只修改 ``papers/Pxxxx-*/README.md`` 中的自动基本信息区块。首次处理旧页面
时会保留原有的资料与开源说明；后续运行只替换成对标记之间的自动内容。
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from library_common import iter_papers, render_basic_info, repository_root


BASIC_INFO_PATTERN = re.compile(
    r"## 基本信息\n\n<!-- AUTO-BASIC-INFO:START -->.*?<!-- AUTO-BASIC-INFO:END -->",
    flags=re.DOTALL,
)
LEGACY_INFO_PATTERN = re.compile(
    r"## 1\. 基本信息\n\n(?P<body>.*?)\n\n(?=## 本文贡献)",
    flags=re.DOTALL,
)


def synchronized_text(text: str, basic_info: str) -> str:
    """返回同步后的页面文本，并兼容没有信息区或使用旧标题的页面。"""

    if BASIC_INFO_PATTERN.search(text):
        return BASIC_INFO_PATTERN.sub(lambda _: basic_info, text, count=1)

    legacy = LEGACY_INFO_PATTERN.search(text)
    if legacy:
        old_body = legacy.group("body").strip()
        preserved = f"\n\n### 资料与开源说明\n\n{old_body}" if old_body else ""
        return text[: legacy.start()] + basic_info + preserved + "\n\n" + text[legacy.end() :]

    contribution_heading = "\n## 本文贡献\n"
    if contribution_heading not in text:
        raise ValueError("缺少“本文贡献”章节，无法确定基本信息插入位置")
    return text.replace(contribution_heading, f"\n{basic_info}\n{contribution_heading}", 1)


def main() -> int:
    """同步全部论文页，或在检查模式报告尚未同步的文件。"""

    parser = argparse.ArgumentParser(description="同步论文页中文基本信息卡")
    parser.add_argument("--check", action="store_true", help="只检查，不修改文件")
    args = parser.parse_args()
    root = repository_root(__file__)
    stale: list[Path] = []

    try:
        records = list(iter_papers(root))
        for record in records:
            current = record.readme.read_text(encoding="utf-8")
            expected = synchronized_text(current, render_basic_info(record.metadata))
            if current == expected:
                continue
            if args.check:
                stale.append(record.readme)
            else:
                temporary = record.readme.with_suffix(".md.tmp")
                temporary.write_text(expected, encoding="utf-8")
                temporary.replace(record.readme)
                print(f"已同步：{record.readme.relative_to(root)}")
    except (OSError, ValueError) as exc:
        print(f"基本信息同步失败：{exc}", file=sys.stderr)
        return 2

    if stale:
        for path in stale:
            print(f"基本信息已过期：{path.relative_to(root)}", file=sys.stderr)
        print("请运行：python3 scripts/sync_paper_info.py", file=sys.stderr)
        return 1
    if args.check:
        print(f"基本信息检查通过：{len(records)} 篇论文均与元数据一致。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
