"""
从论文 YAML 元数据生成知识库首页统计、最近更新、分类数量和论文索引。

脚本扫描 ``papers/Pxxxx-short-name/README.md``，把每篇论文分配到唯一主分类，
生成 ``papers/README.md`` 与八个 ``index/*.md``，并替换根 README 中带标记的
自动区块。默认模式会原子式覆盖生成结果；``--check`` 模式只比较内存结果与磁盘，
适合本地验收和 GitHub Actions，发现索引过期时返回非零退出码。

输入：论文档案 YAML front matter、根 README 的自动区块标记。
输出：按创建日期与永久 ID 倒序排列的 Markdown 索引，最新入库论文显示在最前；
总索引和分类索引均在 ID 前显示页内序号，分类导航与分类页标题同步显示当前篇数。
相同输入会得到相同输出。脚本不读取或复制 ``local_archive`` 中的受版权约束材料，
也不会执行任何 Git 操作。
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Iterable

from library_common import (
    CATEGORIES,
    PaperRecord,
    display_date,
    display_tag,
    iter_papers,
    markdown_escape,
    repository_root,
)


GENERATED_NOTICE = "<!-- 本文件由 scripts/build_index.py 自动生成，请勿手工修改。 -->"
CATEGORY_FOCUS = {
    "datasets": "人体动作、机器人动作、视频、音乐、交互数据",
    "retargeting": "Human/SMPL/SMPL-X 到机器人、IK、神经重定向",
    "motion-generation": "Text/Music/Audio/Video 到 Motion",
    "locomotion-prior": "Locomotion、AMP、ASE、Skill/Motion Prior",
    "tracking-wbc": "Mimic、Tracking、WBC、RL Control",
    "locomanip": "Locomotion + Manipulation、HOI",
    "world-model-vla-agent": "World Model、VLA、VLM、Agent",
    "engineering": "Isaac Lab、MuJoCo、Sim2Real、推理与通信",
}


def paper_link(root: Path, record: PaperRecord, from_dir: Path) -> str:
    """生成从索引目录指向论文 README 的 POSIX 相对链接。"""

    relative = record.readme.relative_to(root)
    if from_dir == root:
        return relative.as_posix()
    return (Path("..") / relative).as_posix()


def paper_table(root: Path, records: Iterable[PaperRecord], from_dir: Path) -> str:
    """渲染带页内序号的统一论文表格；空分类也给出明确文本。"""

    rows = list(records)
    if not rows:
        return "暂无论文记录。"
    lines = [
        "| 序号 | ID | 中文题目 | 英文题目 | 年份 | 出版信息 | 重点标签 |",
        "|---:|---|---|---|---:|---|---|",
    ]
    for sequence, record in enumerate(rows, start=1):
        meta = record.metadata
        paper_id = markdown_escape(meta.get("id", ""))
        title_zh = markdown_escape(meta.get("title_zh", "待补充"))
        title_en = markdown_escape(meta.get("title_en", "待补充"))
        venue = markdown_escape(meta.get("venue", "待核验"))
        year = markdown_escape(meta.get("year", "待核验"))
        tags = meta.get("tags", [])[:3]
        tag_text = " · ".join(f"**{markdown_escape(display_tag(tag))}**" for tag in tags) or "-"
        link = paper_link(root, record, from_dir)
        lines.append(
            f"| {sequence} | {paper_id} | **[{title_zh}]({link})** | {title_en} | "
            f"{year} | {venue} | {tag_text} |"
        )
    return "\n".join(lines)


def paper_added_sort_key(record: PaperRecord) -> tuple[str, str]:
    """返回入库倒序键；同一天创建时以更大的永久 ID 代表更新入库。"""

    meta = record.metadata
    return display_date(meta.get("created")), str(meta.get("id", record.directory.name))


def category_navigation(records: Iterable[PaperRecord]) -> str:
    """渲染带实时论文数量的八类导航表。"""

    rows = list(records)
    lines = [
        "| 分类 ID | `primary_category` | 中文名称 | 当前收录 | 入口 |",
        "|---|---|---|---:|---|",
    ]
    for sequence, (slug, title) in enumerate(CATEGORIES.items(), start=1):
        count = sum(item.metadata.get("primary_category") == slug for item in rows)
        lines.append(
            f"| C{sequence} | `{slug}` | {title} | **{count} 篇** | [查看]({slug}.md) |"
        )
    return "\n".join(lines)


def core_category_navigation(records: Iterable[PaperRecord]) -> str:
    """渲染仓库首页的核心分类、实时数量和关注内容。"""

    rows = list(records)
    lines = [
        "| 分类 ID | 主分类 | 当前收录 | 入口 | 关注内容 |",
        "|---|---|---:|---|---|",
    ]
    for sequence, (slug, title) in enumerate(CATEGORIES.items(), start=1):
        count = sum(item.metadata.get("primary_category") == slug for item in rows)
        lines.append(
            f"| C{sequence} | {title} | **{count} 篇** | [{slug}](index/{slug}.md) | "
            f"{CATEGORY_FOCUS[slug]} |"
        )
    return "\n".join(lines)


def replace_block(text: str, name: str, body: str) -> str:
    """替换 README 中一个成对标记包围的自动区块。"""

    start = f"<!-- AUTO-{name}:START -->"
    end = f"<!-- AUTO-{name}:END -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"README.md 中必须且只能有一组 {start} / {end}")
    prefix, remainder = text.split(start, 1)
    _, suffix = remainder.split(end, 1)
    return f"{prefix}{start}\n{body.rstrip()}\n{end}{suffix}"


def build_outputs(root: Path, records: list[PaperRecord]) -> dict[Path, str]:
    """在内存中构造全部应生成的文件内容。"""

    outputs: dict[Path, str] = {}
    ordered = sorted(records, key=paper_added_sort_key, reverse=True)
    papers_index = "\n\n".join(
        ["# 论文总索引", GENERATED_NOTICE, paper_table(root, ordered, root / "papers")]
    ) + "\n"
    outputs[root / "papers" / "README.md"] = papers_index

    for slug, title in CATEGORIES.items():
        selected = [item for item in ordered if item.metadata.get("primary_category") == slug]
        category_text = "\n\n".join(
            [
                f"# {title}（{len(selected)} 篇）",
                GENERATED_NOTICE,
                paper_table(root, selected, root / "index"),
            ]
        ) + "\n"
        outputs[root / "index" / f"{slug}.md"] = category_text

    category_readme_path = root / "index" / "README.md"
    category_readme = category_readme_path.read_text(encoding="utf-8")
    category_readme = replace_block(
        category_readme,
        "CATEGORIES",
        category_navigation(ordered),
    )
    outputs[category_readme_path] = category_readme.rstrip() + "\n"

    project_count = len(list((root / "projects").glob("J[0-9][0-9][0-9][0-9]-*/README.md")))
    dataset_count = len(list((root / "datasets").glob("D[0-9][0-9][0-9][0-9]-*.md")))
    deep_read_count = sum(item.metadata.get("read_status") == "deep-read" for item in ordered)
    reproduced_count = sum(item.metadata.get("reproduce_status") != "not-started" for item in ordered)
    stats = "\n".join(
        [
            f"- 论文：{len(ordered)} 篇",
            f"- 项目：{project_count} 个",
            f"- 数据集：{dataset_count} 个",
            f"- 精读：{deep_read_count} 篇",
            f"- 已进入复现流程：{reproduced_count} 篇",
        ]
    )

    recent = sorted(
        ordered,
        key=lambda item: (display_date(item.metadata.get("updated")), str(item.metadata.get("id", ""))),
        reverse=True,
    )[:10]
    if recent:
        recent_lines = []
        for item in recent:
            meta = item.metadata
            link = paper_link(root, item, root)
            recent_lines.append(
                f"- {display_date(meta.get('updated'))} [{markdown_escape(meta.get('id'))} — "
                f"{markdown_escape(meta.get('title_zh'))}]({link})"
            )
        recent_text = "\n".join(recent_lines)
    else:
        recent_text = "暂无论文记录。"

    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_block(readme, "STATS", stats)
    readme = replace_block(readme, "CORE-CATEGORIES", core_category_navigation(ordered))
    readme = replace_block(readme, "RECENT", recent_text)
    outputs[readme_path] = readme.rstrip() + "\n"
    return outputs


def apply_or_check(outputs: dict[Path, str], check: bool) -> int:
    """写入生成结果，或检查磁盘内容是否已经最新。"""

    stale: list[Path] = []
    for path, expected in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == expected:
            continue
        if check:
            stale.append(path)
        else:
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(expected, encoding="utf-8")
            temporary.replace(path)
            print(f"已生成：{path}")
    if stale:
        for path in stale:
            print(f"索引已过期：{path}", file=sys.stderr)
        print("请运行：python3 scripts/build_index.py", file=sys.stderr)
        return 1
    if check:
        print("索引检查通过：所有自动生成内容均为最新。")
    return 0


def main() -> int:
    """解析命令行参数并执行索引生成或只读检查。"""

    parser = argparse.ArgumentParser(description="构建或检查论文知识库索引")
    parser.add_argument("--check", action="store_true", help="只检查索引是否最新，不写文件")
    args = parser.parse_args()
    root = repository_root(__file__)
    try:
        records = list(iter_papers(root))
        outputs = build_outputs(root, records)
    except (OSError, ValueError) as exc:
        print(f"索引构建失败：{exc}", file=sys.stderr)
        return 2
    return apply_or_check(outputs, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
