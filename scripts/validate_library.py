"""
校验论文知识库的目录、元数据、受控词表、链接和公开附件契约。

脚本逐个读取 ``papers/Pxxxx-short-name/README.md``，检查永久 ID 与目录一致、
ID/题名不重复、必填字段完整、主分类和状态枚举合法、标签来自 ``TAGS.md``、
URL 使用 HTTPS。若保留原论文的本机路径，则仅做本地档案契约检查；方法详解与
全文翻译应作为论文目录下的公开附件，由 Markdown 链接检查确保真实存在。
此外会遍历公开 Markdown，检查导航、模板和论文页中的相对链接是否指向现存目标。

输出为逐项中文诊断和最终错误/警告计数。脚本完全只读，不修改 Markdown、档案
或 Git 状态；结构通过只说明知识库契约一致，不代表论文结论、代码复现或实机安全。
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import unquote, urlparse

from library_common import (
    CATEGORIES,
    OPEN_SOURCE_STATUSES,
    PAPER_DIR_PATTERN,
    READ_STATUSES,
    REPRODUCE_STATUSES,
    iter_papers,
    repository_root,
)


REQUIRED_FIELDS = {
    "id",
    "title_en",
    "title_zh",
    "year",
    "date",
    "venue",
    "primary_category",
    "tags",
    "authors",
    "institutions",
    "read_status",
    "reproduce_status",
    "created",
    "updated",
}
OPEN_SOURCE_FIELDS = {
    "code",
    "training_code",
    "inference_code",
    "model_weights",
    "dataset",
    "robot_deployment",
}
URL_FIELDS = {"paper_url", "project_url", "github_url", "video_url"}
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def controlled_tags(path: Path) -> set[str]:
    """从 TAGS.md 的反引号列表项中提取规范标签。"""

    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^- `([a-z0-9][a-z0-9-]*)`$", text, flags=re.MULTILINE))


def valid_https_url(value: Any) -> bool:
    """判断非空值是否为带主机名的 HTTPS URL。"""

    if value is None:
        return True
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_internal_markdown_links(root: Path) -> list[str]:
    """检查全部公开 Markdown 中不含网络协议的相对文件链接。"""

    errors: list[str] = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if ".git" in relative.parts or (
            relative.parts and relative.parts[0] == "local_archive" and relative.name != "README.md"
        ):
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            raw_target = match.group(1).strip()
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1]
            if raw_target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target_without_anchor = unquote(raw_target.partition("#")[0])
            if not target_without_anchor:
                continue
            candidate = (path.parent / target_without_anchor).resolve()
            if not candidate.exists():
                errors.append(f"{relative} 包含失效的相对链接：{raw_target}")
    return errors


def main() -> int:
    """执行全部只读校验并返回适合 CI 使用的退出码。"""

    parser = argparse.ArgumentParser(description="校验论文知识库结构与元数据")
    parser.add_argument(
        "--strict-local",
        action="store_true",
        help="把 local_materials 路径缺失视为错误；公开 CI 不应启用",
    )
    args = parser.parse_args()
    root = repository_root(__file__)
    tags = controlled_tags(root / "TAGS.md")
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: dict[str, Path] = {}
    seen_titles: dict[str, Path] = {}

    try:
        records = list(iter_papers(root))
    except (OSError, ValueError) as exc:
        print(f"[错误] 无法读取论文档案：{exc}", file=sys.stderr)
        return 2

    for record in records:
        meta = record.metadata
        label = str(record.readme.relative_to(root))
        page_text = record.readme.read_text(encoding="utf-8")
        if not page_text.startswith("<!--\n---\n"):
            errors.append(f"{label} 必须使用 HTML 注释隐藏 YAML 元数据，避免 GitHub 渲染成表格")
        if "```mermaid" in page_text:
            errors.append(f"{label} 不应使用自绘 Mermaid 代替原论文重点图")
        if "## 本地材料" in page_text:
            errors.append(f"{label} 不应展示本机材料路径；请改为论文附件链接")
        if "## 本文贡献" not in page_text:
            errors.append(f"{label} 缺少“本文贡献”章节")
        if "## 研究方法详细解读" not in page_text:
            errors.append(f"{label} 缺少“研究方法详细解读”章节")
        directory_match = PAPER_DIR_PATTERN.fullmatch(record.directory.name)
        expected_id = directory_match.group(1) if directory_match else ""
        missing = sorted(REQUIRED_FIELDS - set(meta))
        if missing:
            errors.append(f"{label} 缺少字段：{', '.join(missing)}")

        paper_id = meta.get("id")
        if paper_id != expected_id:
            errors.append(f"{label} 的 id={paper_id!r} 与目录 ID {expected_id!r} 不一致")
        if paper_id in seen_ids:
            errors.append(f"{label} 与 {seen_ids[paper_id]} 使用重复 ID {paper_id}")
        elif isinstance(paper_id, str):
            seen_ids[paper_id] = record.readme

        normalized_title = str(meta.get("title_en", "")).strip().casefold()
        if not normalized_title:
            errors.append(f"{label} 的 title_en 为空")
        elif normalized_title in seen_titles:
            errors.append(f"{label} 与 {seen_titles[normalized_title]} 的英文题名重复")
        else:
            seen_titles[normalized_title] = record.readme

        if meta.get("primary_category") not in CATEGORIES:
            errors.append(f"{label} 的 primary_category 不合法：{meta.get('primary_category')!r}")
        if meta.get("read_status") not in READ_STATUSES:
            errors.append(f"{label} 的 read_status 不合法：{meta.get('read_status')!r}")
        if meta.get("reproduce_status") not in REPRODUCE_STATUSES:
            errors.append(f"{label} 的 reproduce_status 不合法：{meta.get('reproduce_status')!r}")

        paper_tags = meta.get("tags")
        if not isinstance(paper_tags, list):
            errors.append(f"{label} 的 tags 必须是列表")
        else:
            unknown_tags = sorted(set(paper_tags) - tags)
            if unknown_tags:
                errors.append(f"{label} 使用了未登记标签：{', '.join(unknown_tags)}")

        for list_field in ("authors", "institutions"):
            if not isinstance(meta.get(list_field), list) or not meta.get(list_field):
                errors.append(f"{label} 的 {list_field} 必须是非空列表")

        for field in URL_FIELDS:
            if not valid_https_url(meta.get(field)):
                errors.append(f"{label} 的 {field} 必须为 HTTPS URL 或 null")

        open_source = meta.get("open_source")
        if not isinstance(open_source, dict):
            errors.append(f"{label} 的 open_source 必须是映射")
        else:
            missing_open = sorted(OPEN_SOURCE_FIELDS - set(open_source))
            if missing_open:
                errors.append(f"{label} 的 open_source 缺少：{', '.join(missing_open)}")
            for field in OPEN_SOURCE_FIELDS & set(open_source):
                if open_source[field] not in OPEN_SOURCE_STATUSES:
                    errors.append(f"{label} 的 open_source.{field} 状态不合法：{open_source[field]!r}")

        local_materials = meta.get("local_materials", [])
        if not isinstance(local_materials, list):
            errors.append(f"{label} 的 local_materials 必须是列表")
        else:
            expected_prefix = f"local_archive/{paper_id}/"
            for item in local_materials:
                if not isinstance(item, str) or not item.startswith(expected_prefix):
                    errors.append(f"{label} 的本地材料必须位于 {expected_prefix}：{item!r}")
                    continue
                candidate = (root / item).resolve()
                archive_root = (root / "local_archive").resolve()
                if archive_root not in candidate.parents:
                    errors.append(f"{label} 的本地材料路径越出 local_archive：{item}")
                elif not candidate.is_file():
                    message = f"{label} 登记的本地材料不存在：{item}"
                    (errors if args.strict_local else warnings).append(message)

    errors.extend(validate_internal_markdown_links(root))

    for warning in warnings:
        print(f"[警告] {warning}")
    for error in errors:
        print(f"[错误] {error}", file=sys.stderr)
    print(f"校验完成：{len(records)} 篇论文，{len(errors)} 个错误，{len(warnings)} 个警告。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
