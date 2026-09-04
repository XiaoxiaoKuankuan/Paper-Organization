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
- 2026-09-04 [P0025 — UDE-2：多模态、多身体部位人体动作合成统一框架](papers/P0025-ude-2/README.md)
- 2026-09-04 [P0024 — MotionGPT：将人体动作视为一种外语](papers/P0024-motiongpt/README.md)
- 2026-09-04 [P0023 — TM2D：通过音乐—文本融合进行双模态三维舞蹈生成](papers/P0023-tm2d/README.md)
- 2026-09-04 [P0022 — UDE：人体动作生成的统一驱动引擎](papers/P0022-ude/README.md)
- 2026-09-04 [P0021 — AnyMo：通过掩码建模扩展任意模态条件动作生成](papers/P0021-anymo/README.md)
- 2026-09-04 [P0020 — MACE-Dance：面向音乐驱动舞蹈视频生成的动作—外观级联专家](papers/P0020-mace-dance/README.md)
- 2026-09-04 [P0019 — ARDY：用于交互式人体动作生成的混合表示自回归扩散模型](papers/P0019-ardy/README.md)
- 2026-09-04 [P0018 — MotionBricks：基于模块化潜变量生成模型与智能原语的可扩展实时动作](papers/P0018-motionbricks/README.md)
- 2026-09-04 [P0017 — Kimodo：可控人体动作生成的规模化](papers/P0017-kimodo/README.md)
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
