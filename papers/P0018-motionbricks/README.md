<!--
---
id: P0018
title_en: "MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives"
title_zh: "MotionBricks：基于模块化潜变量生成模型与智能原语的可扩展实时动作"
year: 2026
date: 2026-04-27
venue: "ACM Transactions on Graphics 45(4), SIGGRAPH 2026"
primary_category: motion-generation
tags: [motion-generation, real-time, latent-motion, multimodal, human-object-interaction, g1]
authors: [Tingwu Wang, Olivier Dionne, Michael De Ruyter, David Minor, Davis Rempe, Kaifeng Zhao, Mathis Petrovich, Ye Yuan, Chenran Li, Zhengyi Luo, Brian Robison, Xavier Blackwell, Bernardo Antoniazzi, Xue Bin Peng, Yuke Zhu, Simon Yuen]
institutions: [NVIDIA, ETH Zürich, Simon Fraser University, The University of Texas at Austin]
paper_url: "https://arxiv.org/abs/2604.24833"
project_url: "https://nvlabs.github.io/motionbricks/"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: partial}
open_source_checked: 2026-09-03
robots: [Unitree G1]
inputs: [velocity command, style, keyframes, object constraints]
outputs: [real-time latent motion, humanoid reference motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0018｜MotionBricks：基于模块化潜变量生成模型与智能原语的可扩展实时动作

*MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives*

[论文](https://arxiv.org/abs/2604.24833) · [项目页](https://nvlabs.github.io/motionbricks/)

## 本文贡献

- 面向生产级实时交互，在单一模块化潜变量主干中建模超过 35 万动作片段，报告约 2 ms 延迟与 15,000 FPS 批吞吐。
- 提出 Smart Primitives，把速度、风格、关键帧和物体交互统一为可组合动作接口，让应用像搭积木一样组织导航与交互。
- 在 UE5 应用和 Unitree G1 上展示同一生成框架从动画到机器人控制的迁移，强调生成层与低层执行层的组合边界。

## 研究问题

离线扩散模型通常质量高但交互延迟大，传统 motion matching/状态机实时却难扩展到海量技能和多模态控制。MotionBricks 试图把大数据生成先验压入低延迟 latent transition，并用显式原语接口解决产品逻辑如何稳定调用生成模型。

## 原论文重点图

![MotionBricks 总览](figures/key-figure.png)

**图 1：动画与 G1 的统一实时动作接口（原论文 Figure 1 所在页）。** 上半部分展示 UE5 中导航、风格、杂技和物体交互，下半部分展示 G1 执行；共同点是 Smart Primitive 只描述约束，模块化潜变量主干生成连续动作，机器人端仍需跟踪控制器。

## 研究方法详细解读

### 模块化潜变量主干

模型在紧凑动作 latent 中预测短时未来，把昂贵高维去噪转为低维、少步生成。模块化设计让新增动作数据与能力不必重新手写状态转移，同时把共享时序先验与任务专用条件分开。

### Smart Primitives

原语不是固定动画片段，而是对未来动作施加的速度、方向、风格、关键帧、接触或物体关系约束。应用层组合原语，生成器解决约束间的时序过渡；冲突时的优先级和可满足性仍由训练分布与接口实现决定。

### 机器人控制链

G1 演示将生成的人体/机器人参考交给低层全身控制。2 ms 指生成模型推理，不包括感知、重定向、控制和通信总延迟；复现必须分开测端到端控制周期。

## 实验结果与结论

论文在不同规模开源/私有动作集上比较质量与吞吐，并展示生产级长时交互。核心结论是潜变量模块化和原语接口可兼顾规模、质量与实时性；G1 演示说明可连接机器人，但不是完整硬件安全或任意技能泛化证明。

## 局限与复现提醒

- 35 万片段含私有数据，公开资源边界会影响规模复现。
- 吞吐与单实例端到端延迟口径不同，不能直接把 15,000 FPS 当控制频率。
- 机器人链路需要核对 MotionBricks 输出表示、跟踪器、50 Hz 重采样和关节映射。

## 阅读与复现状态

- 阅读：已阅读原论文与飞书方法整理。
- 资源：项目页已核验，代码/权重发布状态保守记为待核验。
- 运行：未执行 UE5 或 G1 演示。

## 参考资料

- [arXiv](https://arxiv.org/abs/2604.24833)
- [项目页](https://nvlabs.github.io/motionbricks/)
- [ACM DOI](https://doi.org/10.1145/3811334)

## 更新记录

- 2026-09-03：新建条目，整理模块化 latent、Smart Primitives、实时性口径与 G1 接口。
