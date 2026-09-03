---
id: P0010
title_en: "RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control"
title_zh: "基于物理反馈的强化学习：让大动作模型与人形机器人控制对齐"
year: 2025
date: 2025-06-15
venue: "ECCV 2026"
primary_category: motion-generation
tags:
  - motion-generation
  - reinforcement-learning
  - physics-feedback
  - transformer
  - text
  - retargeting
  - motion-tracking
  - g1
  - sim2real
authors:
  - Junpeng Yue
  - Zepeng Wang
  - Yuxuan Wang
  - Weishuai Zeng
  - Jiangxing Wang
  - Xinrun Xu
  - Yu Zhang
  - Sipeng Zheng
  - Ziluo Ding
  - Zongqing Lu
institutions:
  - Peking University
  - BeingBeyond
  - Wuhan University
paper_url: "https://arxiv.org/abs/2506.12769"
project_url: "https://beingbeyond.github.io/RLPF/"
github_url: "https://github.com/BeingBeyond/RLPF"
video_url: null
open_source:
  code: "no"
  training_code: "no"
  inference_code: "no"
  model_weights: "no"
  dataset: "no"
  robot_deployment: "no"
open_source_checked: 2026-09-03
robots:
  - Unitree G1
inputs:
  - text instruction
outputs:
  - discrete human-motion tokens
  - retargeted robot reference motion
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0010/RL from Physical Feedback: Aligning Large Motion.pdf"
  - "local_archive/P0010/RLPF_方法框架详解与全文中文翻译.docx"
created: 2026-09-03
updated: 2026-09-03
---

# P0010 — 基于物理反馈的强化学习：让大动作模型与人形机器人控制对齐

## 1. 基本信息

- 论文：[arXiv:2506.12769](https://arxiv.org/abs/2506.12769)
- 项目页：[RLPF](https://beingbeyond.github.io/RLPF/)
- 代码入口：[BeingBeyond/RLPF](https://github.com/BeingBeyond/RLPF)。截至 2026-09-03，仓库仍仅说明代码将发布，故这里不把占位仓库记为已开源。

## 2. 一句话总结

RLPF 把机器人在物理仿真中的实际跟踪成败变成强化学习反馈，配合文本/动作语义对齐约束，以 GRPO 后训练大动作模型，使文本生成动作更适合 G1 执行。

## 3. 研究问题

传统文本到动作模型主要优化人体域的视觉质量和语义一致性，生成结果经重定向后仍可能脚滑、穿地或动态失稳。只优化“容易跟踪”又会产生站立等奖励投机，因此需要同时约束物理可执行性和语义忠实度。

## 4. 整体框架

```mermaid
flowchart LR
    A[文本] --> B[LLaMA2-7B 大动作模型]
    B --> C[离散动作 token]
    C --> D[动作解码器]
    D --> E[人体动作]
    E --> F[SMPL 到 G1 优化式重定向]
    F --> G[冻结的 Teacher-Student Tracker]
    G --> H[Isaac Gym 成功/失败物理反馈]
    D --> I[文本/动作对齐编码器]
    I --> J[语义对齐反馈]
    H --> K[GRPO]
    J --> K
    K --> B
```

## 5. 大动作模型

动作 tokenizer 把连续人体动作压缩为离散 token，LLaMA2-7B 作为因果解码器根据文本自回归生成 token，再还原为连续动作。该选择是论文实例，RLPF 的核心并不依赖特定生成骨干。

## 6. 物理反馈链路

生成动作先通过两阶段优化从 SMPL 形态映射到 G1，再由 ExBody2 风格的跟踪器执行。Teacher 在 PPO 训练中使用特权状态，Student 通过类似 DAgger 的蒸馏只保留可部署观测；RL 后训练时 tracker 冻结，以是否完成跟踪形成二值物理奖励。

## 7. GRPO 与语义约束

每条文本采样 20 个候选，组内标准化奖励后用 GRPO 更新生成器，避免额外训练 value 网络。文本—动作与参考动作—生成动作两个对齐距离用于防止“站着不动最安全”的奖励投机；附录给出 tracking、alignment、KL 权重分别为 10、2、1.0。

## 8. 主要结果

论文在 CMU/AMASS、Isaac Gym 与 MuJoCo 上报告更高跟踪成功率和较低动作误差，并给出真实 G1 动作展示。消融显示仅有物理奖励会损害语义和动作丰富性，加入对齐验证后才在可执行性与文本一致性之间取得平衡。

## 9. 优点与局限

- 优点：把实际控制器能力直接反馈给生成模型；GRPO 不依赖人工偏好标注；显式处理 reward hacking。
- 局限：物理奖励主要是固定 tracker 下的二值成败；人体生成、优化式重定向和控制仍是多阶段链路；当前没有可运行代码与权重可供复核。

## 10. 对个人研究的价值

RLPF 可作为“物理反馈后训练”路线，与 GENMO/OMG 的数据驱动生成和 PhyGile 的 physics-prefix 路线横向比较。迁移到自有机器人时，奖励必须基于实际 tracker、关节映射、仿真参数与失败判据重新校准。

## 11. 阅读与复现状态

- [x] 阅读原文和方法详解/全文翻译
- [x] 核验项目页与代码占位仓库
- [ ] 等待并核验正式代码发布
- [ ] 在统一 tracker 上复现实验
- [ ] 独立实机安全验证

## 12. 本地材料

- `local_archive/P0010/RL from Physical Feedback: Aligning Large Motion.pdf`：原论文。
- `local_archive/P0010/RLPF_方法框架详解与全文中文翻译.docx`：方法框架详解与全文中文翻译。

## 13. 来源

- [论文](https://arxiv.org/abs/2506.12769)
- [项目页](https://beingbeyond.github.io/RLPF/)
- [代码占位仓库](https://github.com/BeingBeyond/RLPF)

## 14. 更新日志

- 2026-09-03：创建精读档案；登记两份本地材料，并区分“已有仓库 URL”与“已有可运行代码”。
