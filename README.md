# Paper Organization

面向人形机器人运动智能的个人论文、项目与数据集知识库。仓库采用“实体固定、索引生成”的组织方式：论文档案拥有永久 ID，分类变化不会导致路径迁移；分类页和统计信息由元数据自动生成。

> 信息维护原则：准确性 > 完整性 > 结构一致性 > 更新速度。未知信息使用 `null` 或明确的“待核验”，不得猜测。

## 馆藏概览

<!-- AUTO-STATS:START -->
- 论文：39 篇
- 项目：0 个
- 数据集：0 个
- 精读：14 篇
- 已进入复现流程：0 篇
<!-- AUTO-STATS:END -->

## 导航

- [论文总索引](papers/README.md)
- [分类导航](index/README.md)
- [项目档案](projects/README.md)
- [数据集档案](datasets/README.md)
- [横向对比](comparisons/README.md)
- [主题笔记](topics/README.md)
- [标签词表](TAGS.md)
- [维护流程](docs/maintenance-workflow.md)
- [元数据规范](docs/metadata-schema.md)
- [飞书阅读清单覆盖表](docs/feishu-reading-lists.md)

## 核心分类

<!-- AUTO-CORE-CATEGORIES:START -->
| 分类 ID | 主分类 | 当前收录 | 入口 | 关注内容 |
|---|---|---:|---|---|
| C1 | 数据集 | **1 篇** | [datasets](index/datasets.md) | 人体动作、机器人动作、视频、音乐、交互数据 |
| C2 | 重定向 | **1 篇** | [retargeting](index/retargeting.md) | Human/SMPL/SMPL-X 到机器人、IK、神经重定向 |
| C3 | 动作生成 | **28 篇** | [motion-generation](index/motion-generation.md) | Text/Music/Audio/Video 到 Motion |
| C4 | Locomotion 与运动先验 | **3 篇** | [locomotion-prior](index/locomotion-prior.md) | Locomotion、AMP、ASE、Skill/Motion Prior |
| C5 | 动作跟踪与全身控制 | **4 篇** | [tracking-wbc](index/tracking-wbc.md) | Mimic、Tracking、WBC、RL Control |
| C6 | LocoManip | **0 篇** | [locomanip](index/locomanip.md) | Locomotion + Manipulation、HOI |
| C7 | 世界模型 / VLA / Agent | **2 篇** | [world-model-vla-agent](index/world-model-vla-agent.md) | World Model、VLA、VLM、Agent |
| C8 | 工程与实机部署 | **0 篇** | [engineering](index/engineering.md) | Isaac Lab、MuJoCo、Sim2Real、推理与通信 |
<!-- AUTO-CORE-CATEGORIES:END -->

## 最近更新

<!-- AUTO-RECENT:START -->
- 2026-09-04 [P0039 — ADAPT：面向鲁棒、可操控在线文本驱动人形机器人控制的敏捷扩散动作先验](papers/P0039-adapt/README.md)
- 2026-09-04 [P0012 — SONIC：扩展运动跟踪以实现自然的人形机器人全身控制](papers/P0012-sonic/README.md)
- 2026-09-04 [P0011 — 你会即兴表演吗？通过音频控制实现富有表现力的人形机器人运动](papers/P0011-roboperform/README.md)
- 2026-09-04 [P0010 — 基于物理反馈的强化学习：让大动作模型与人形机器人控制对齐](papers/P0010-rlpf/README.md)
- 2026-09-04 [P0009 — PhyGile：物理前缀引导的敏捷通用人形机器人动作生成与跟踪](papers/P0009-phygile/README.md)
- 2026-09-04 [P0008 — OMG：面向通用人形机器人控制的全模态动作生成](papers/P0008-omg/README.md)
- 2026-09-04 [P0007 — InfiniteDance：面向野外泛化的可扩展三维舞蹈生成](papers/P0007-infinitedance/README.md)
- 2026-09-04 [P0006 — HumanoidArena：第一视角层级式全身学习基准](papers/P0006-humanoidarena/README.md)
- 2026-09-04 [P0005 — HIL：面向动态运动控制的混合模仿学习](papers/P0005-hil/README.md)
- 2026-09-04 [P0004 — GigaBrain-WBC-0.5：用于环境交互鲁棒全身控制的行为世界模型](papers/P0004-gigabrain-wbc-0-5/README.md)
<!-- AUTO-RECENT:END -->

## 使用方式

```bash
python3 -m pip install -r requirements.txt
python3 scripts/sync_paper_info.py
python3 scripts/validate_library.py --strict-local
python3 scripts/build_index.py
python3 scripts/sync_paper_info.py --check
python3 scripts/build_index.py --check
```

新增论文时先复制 [论文模板](templates/paper-template.md)，编辑隐藏 YAML 元数据与正文，再运行基本信息同步、校验和索引构建。作者、机构、论文时间、期刊/会议、分类、标签及状态会从 YAML 自动生成到正文的无表格信息卡。方法详解与个人翻译放入论文目录的 `attachments/`，原论文备份仍放在不受 Git 跟踪的 `local_archive/`。

## 内容边界

- 公开仓库保存结构化元数据、深度阅读笔记、原论文重点图、用户指定的方法详解与个人翻译附件及公开链接。
- 出版社原始 PDF 和私人实验材料只存本地档案；论文重点图注明原始图号和出处。
- “静态阅读”“代码可运行”“仿真复现”“实机验证”是不同证据等级，必须分别记录。
