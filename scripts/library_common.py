"""
论文知识库脚本的公共基础模块。

本文件集中定义八个主分类、阅读与复现状态枚举，并负责扫描
``papers/Pxxxx-short-name/README.md``、读取 YAML front matter 和规范化日期。
索引构建器与校验器共用这里的实现，避免两个脚本对字段含义产生漂移。

输入是仓库根目录或单个 Markdown 路径；输出是保持原始字段的 Python 字典。
该模块不会修改仓库文件。YAML 解析依赖 requirements.txt 中固定范围的 PyYAML；
缺少依赖时会给出明确的安装命令，而不会降级成可能误读嵌套字段的简易解析器。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - 仅在依赖缺失环境触发
    raise SystemExit("缺少 PyYAML，请先运行：python3 -m pip install -r requirements.txt") from exc


CATEGORIES: dict[str, str] = {
    "datasets": "数据集",
    "retargeting": "重定向",
    "motion-generation": "动作生成",
    "locomotion-prior": "Locomotion 与运动先验",
    "tracking-wbc": "动作跟踪与全身控制",
    "locomanip": "LocoManip",
    "world-model-vla-agent": "世界模型 / VLA / Agent",
    "engineering": "工程与实机部署",
}

READ_STATUSES = {"unread", "skimmed", "read", "deep-read"}
REPRODUCE_STATUSES = {
    "not-started",
    "environment-ready",
    "demo-tested",
    "training-tested",
    "sim2sim-tested",
    "real-robot-tested",
}
OPEN_SOURCE_STATUSES = {"full", "partial", "no", "unknown"}
PAPER_DIR_PATTERN = re.compile(r"^(P\d{4})-[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class PaperRecord:
    """表示一个论文目录、README 路径及其已解析元数据。"""

    directory: Path
    readme: Path
    metadata: dict[str, Any]


def repository_root(script_file: str) -> Path:
    """根据 scripts 目录中的脚本位置稳定推导仓库根目录。"""

    return Path(script_file).resolve().parents[1]


def read_front_matter(path: Path) -> dict[str, Any]:
    """读取 Markdown 文件开头的 YAML front matter。"""

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} 缺少起始 YAML 分隔符 ---")
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path} 缺少结束 YAML 分隔符 ---") from exc
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValueError(f"{path} 的 YAML front matter 必须是映射")
    return data


def iter_papers(root: Path) -> Iterable[PaperRecord]:
    """按目录名排序遍历全部符合永久 ID 约定的论文档案。"""

    papers_root = root / "papers"
    for directory in sorted(papers_root.iterdir() if papers_root.exists() else []):
        if not directory.is_dir() or not PAPER_DIR_PATTERN.fullmatch(directory.name):
            continue
        readme = directory / "README.md"
        if not readme.is_file():
            raise ValueError(f"论文目录缺少 README.md：{directory}")
        yield PaperRecord(directory=directory, readme=readme, metadata=read_front_matter(readme))


def display_date(value: Any) -> str:
    """将 YAML 日期或普通字符串统一为索引中的显示文本。"""

    if value is None:
        return "待核验"
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)


def markdown_escape(value: Any) -> str:
    """转义表格单元格中会破坏 Markdown 结构的字符。"""

    return str(value).replace("|", "\\|").replace("\n", " ").strip()
