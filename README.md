# Paper Organization

面向人形机器人运动智能的个人论文、项目与数据集知识库。仓库采用“实体固定、索引生成”的组织方式：论文档案拥有永久 ID，分类变化不会导致路径迁移；分类页和统计信息由元数据自动生成。

> 信息维护原则：准确性 > 完整性 > 结构一致性 > 更新速度。未知信息使用 `null` 或明确的“待核验”，不得猜测。

## 馆藏概览

<!-- AUTO-STATS:START -->
- 论文：12 篇
- 项目：0 个
- 数据集：0 个
- 精读：12 篇
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

## 核心分类

| ID | 主分类 | 入口 | 关注内容 |
|---|---|---|---|
| C1 | 数据集 | [datasets](index/datasets.md) | 人体动作、机器人动作、视频、音乐、交互数据 |
| C2 | 重定向 | [retargeting](index/retargeting.md) | Human/SMPL/SMPL-X 到机器人、IK、神经重定向 |
| C3 | 动作生成 | [motion-generation](index/motion-generation.md) | Text/Music/Audio/Video 到 Motion |
| C4 | Locomotion 与运动先验 | [locomotion-prior](index/locomotion-prior.md) | Locomotion、AMP、ASE、Skill/Motion Prior |
| C5 | 动作跟踪与全身控制 | [tracking-wbc](index/tracking-wbc.md) | Mimic、Tracking、WBC、RL Control |
| C6 | LocoManip | [locomanip](index/locomanip.md) | Locomotion + Manipulation、HOI |
| C7 | 世界模型 / VLA / Agent | [world-model-vla-agent](index/world-model-vla-agent.md) | World Model、VLA、VLM、Agent |
| C8 | 工程与实机部署 | [engineering](index/engineering.md) | Isaac Lab、MuJoCo、Sim2Real、推理与通信 |

## 最近更新

<!-- AUTO-RECENT:START -->
- 2026-09-03 [P0012 — SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](papers/P0012-sonic/README.md)
- 2026-09-03 [P0011 — Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control](papers/P0011-roboperform/README.md)
- 2026-09-03 [P0010 — RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control](papers/P0010-rlpf/README.md)
- 2026-09-03 [P0009 — PhyGile: Physics-Prefix Guided Motion Generation for Agile General Humanoid Motion Tracking](papers/P0009-phygile/README.md)
- 2026-09-03 [P0008 — OMG: Omni-Modal Motion Generation for Generalist Humanoid Control](papers/P0008-omg/README.md)
- 2026-09-03 [P0007 — InfiniteDance: Scalable 3D Dance Generation Towards in-the-wild Generalization](papers/P0007-infinitedance/README.md)
- 2026-09-03 [P0006 — HumanoidArena: Benchmarking Egocentric Hierarchical Whole-body Learning](papers/P0006-humanoidarena/README.md)
- 2026-09-03 [P0005 — HIL: Hybrid Imitation Learning for Dynamic Athletic Control](papers/P0005-hil/README.md)
- 2026-09-03 [P0004 — GigaBrain-WBC-0.5: A Behavior World Model for Robust Whole-Body Control with Environment Interaction](papers/P0004-gigabrain-wbc-0-5/README.md)
- 2026-09-03 [P0003 — GenTrack: Physical Alignment for Robot-Native Motion Generation and Zero-Shot Humanoid Tracking](papers/P0003-gentrack/README.md)
<!-- AUTO-RECENT:END -->

## 使用方式

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_library.py --strict-local
python3 scripts/build_index.py
python3 scripts/build_index.py --check
```

新增论文时先复制 [论文模板](templates/paper-template.md)，只编辑论文档案的 YAML 和正文，再运行校验与索引构建。`local_archive/` 中的原论文、全文翻译和方法详解默认不会被 Git 跟踪。

## 内容边界

- 公开仓库保存个人整理、结构化元数据、原创图解和公开链接。
- 出版社 PDF、论文原文、全文翻译及可能受版权约束的二进制材料只存本地档案。
- “静态阅读”“代码可运行”“仿真复现”“实机验证”是不同证据等级，必须分别记录。
