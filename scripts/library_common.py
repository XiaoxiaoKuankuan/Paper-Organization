"""
论文知识库脚本的公共基础模块。

本文件集中定义八个主分类、中文标签显示名、阅读与复现状态枚举，并负责扫描
``papers/Pxxxx-short-name/README.md``、读取隐藏式 YAML front matter 和规范化日期。
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

# 元数据继续使用稳定的英文 slug，面向读者的索引统一显示中文名称。
TAG_LABELS: dict[str, str] = {
    "reinforcement-learning": "强化学习",
    "imitation-learning": "模仿学习",
    "adversarial-learning": "对抗学习",
    "diffusion": "扩散模型",
    "flow-matching": "流匹配",
    "transformer": "Transformer",
    "world-model": "世界模型",
    "motion-prior": "运动先验",
    "physics-guidance": "物理引导",
    "physics-feedback": "物理反馈",
    "curriculum-learning": "课程学习",
    "distillation": "蒸馏",
    "autoregressive": "自回归",
    "inverse-kinematics": "逆运动学",
    "optimization": "优化",
    "multimodal": "多模态",
    "masked-modeling": "掩码建模",
    "mixture-of-experts": "混合专家",
    "contrastive-learning": "对比学习",
    "reinforcement-fine-tuning": "强化学习微调",
    "continual-learning": "持续学习",
    "dataset": "数据集",
    "benchmark": "基准",
    "motion-generation": "动作生成",
    "retargeting": "重定向",
    "motion-tracking": "动作跟踪",
    "locomotion": "运动控制",
    "whole-body-control": "全身控制",
    "loco-manipulation": "移动操作",
    "human-object-interaction": "人-物交互",
    "navigation": "导航",
    "pose-estimation": "姿态估计",
    "dance-generation": "舞蹈生成",
    "motion-editing": "动作编辑",
    "teleoperation": "遥操作",
    "force-control": "力控制",
    "fall-recovery": "跌倒恢复",
    "dexterous-hand": "灵巧手",
    "text": "文本",
    "audio": "音频",
    "music": "音乐",
    "video": "视频",
    "image": "图像",
    "speech": "语音",
    "smpl": "SMPL",
    "smplx": "SMPL-X",
    "keypoints": "关键点",
    "robot-state": "机器人状态",
    "velocity-command": "速度指令",
    "latent-motion": "动作潜变量",
    "vr": "虚拟现实",
    "humanoid": "人形机器人",
    "g1": "Unitree G1",
    "h1": "Unitree H1",
    "h1-2": "Unitree H1-2",
    "biped": "双足机器人",
    "human-motion": "人体动作",
    "isaac-lab": "Isaac Lab",
    "isaac-gym": "Isaac Gym",
    "mujoco": "MuJoCo",
    "genesis": "Genesis",
    "sim2sim": "Sim2Sim",
    "sim2real": "Sim2Real",
    "real-time": "实时",
    "onnx": "ONNX",
    "tensorrt": "TensorRT",
    "ros2": "ROS 2",
    "motion-capture": "动作捕捉",
    "synthetic-data": "合成数据",
    "large-scale-data": "大规模数据",
    "physical-plausibility": "物理合理性",
    "diversity": "多样性",
    "generalization": "泛化",
    "zero-shot": "零样本",
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

READ_STATUS_LABELS: dict[str, str] = {
    "unread": "待读",
    "skimmed": "已初读",
    "read": "已阅读",
    "deep-read": "已精读",
}

REPRODUCE_STATUS_LABELS: dict[str, str] = {
    "not-started": "未开始",
    "environment-ready": "环境已准备",
    "demo-tested": "Demo 已验证",
    "training-tested": "训练已验证",
    "sim2sim-tested": "Sim2Sim 已验证",
    "real-robot-tested": "实机已验证",
}


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
    """读取 Markdown 文件开头的隐藏式或传统 YAML front matter。

    论文页把 YAML 包在 HTML 注释内，避免 GitHub 把元数据渲染成难读的表格；
    模板与其他旧文件仍可使用传统的首行 ``---``，从而保持向后兼容。
    """

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        raise ValueError(f"{path} 为空，无法读取 YAML 元数据")
    start = 0
    if lines[0].strip() == "<!--":
        if len(lines) < 2 or lines[1].strip() != "---":
            raise ValueError(f"{path} 的隐藏元数据缺少起始 YAML 分隔符 ---")
        start = 1
    elif lines[0].strip() != "---":
        raise ValueError(f"{path} 缺少起始 YAML 分隔符 ---")
    try:
        end = next(
            index for index, line in enumerate(lines[start + 1 :], start=start + 1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ValueError(f"{path} 缺少结束 YAML 分隔符 ---") from exc
    if start == 1 and (end + 1 >= len(lines) or lines[end + 1].strip() != "-->"):
        raise ValueError(f"{path} 的隐藏 YAML 元数据缺少 HTML 注释结束符 -->")
    data = yaml.safe_load("\n".join(lines[start + 1 : end]))
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


def display_tag(tag: Any) -> str:
    """把规范标签转换为中文显示名，未登记映射时保留原 slug。"""

    normalized = str(tag).strip()
    return TAG_LABELS.get(normalized, normalized)


def display_list(values: Any) -> str:
    """把作者、机构等列表渲染成适合中文正文的顿号分隔文本。"""

    if not isinstance(values, list) or not values:
        return "待核验"
    return "、".join(str(value).strip() for value in values if str(value).strip()) or "待核验"


def render_basic_info(metadata: dict[str, Any]) -> str:
    """从唯一元数据源生成论文页开头的无表格中文书目信息卡。

    信息卡故意使用 Markdown 引用块而不是表格：作者或机构较多时可以自然换行，
    也不会重新引入 GitHub 页面顶部密集方框的问题。作者、机构、发表时间、出版
    信息是固定必显字段；分类、标签和状态一并展示，方便浏览时快速判断论文位置。
    """

    publication_date = display_date(metadata.get("date"))
    if publication_date == "待核验" and metadata.get("year"):
        publication_date = f"{metadata['year']}（具体日期待核验）"
    category = CATEGORIES.get(str(metadata.get("primary_category", "")), "待核验")
    tags = metadata.get("tags")
    if isinstance(tags, list) and tags:
        tag_text = " · ".join(f"**{display_tag(tag)}**" for tag in tags)
    else:
        tag_text = "待补充"
    read_status = READ_STATUS_LABELS.get(str(metadata.get("read_status", "")), "待核验")
    reproduce_status = REPRODUCE_STATUS_LABELS.get(
        str(metadata.get("reproduce_status", "")), "待核验"
    )

    return "\n".join(
        [
            "## 基本信息",
            "",
            "<!-- AUTO-BASIC-INFO:START -->",
            f"> **作者**：{display_list(metadata.get('authors'))}",
            ">",
            f"> **机构**：{display_list(metadata.get('institutions'))}",
            ">",
            f"> **论文时间**：{publication_date}",
            ">",
            f"> **期刊 / 会议**：{metadata.get('venue') or '待核验'}",
            ">",
            f"> **主分类**：{category}",
            ">",
            f"> **重点标签**：{tag_text}",
            ">",
            f"> **阅读状态**：{read_status}　·　**复现状态**：{reproduce_status}",
            "<!-- AUTO-BASIC-INFO:END -->",
        ]
    )
