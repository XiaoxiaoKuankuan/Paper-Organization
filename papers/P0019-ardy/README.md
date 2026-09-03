<!--
---
id: P0019
title_en: "ARDY: Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation"
title_zh: "ARDY：用于交互式人体动作生成的混合表示自回归扩散模型"
year: 2026
date: 2026-07-09
venue: "arXiv preprint arXiv:2607.08741"
primary_category: motion-generation
tags: [motion-generation, diffusion, autoregressive, real-time, text, keypoints, human-motion]
authors: [Kaifeng Zhao, Mathis Petrovich, Haotian Zhang, Tingwu Wang, Siyu Tang, Davis Rempe]
institutions: [NVIDIA, ETH Zürich]
paper_url: "https://arxiv.org/abs/2607.08741"
project_url: "https://research.nvidia.com/labs/sil/projects/ardy/"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [online text, keyframes, paths, motion history]
outputs: [streaming human motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0019｜ARDY：用于交互式人体动作生成的混合表示自回归扩散模型

*ARDY: Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation*

[论文](https://arxiv.org/abs/2607.08741) · [项目页](https://research.nvidia.com/labs/sil/projects/ardy/)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Kaifeng Zhao、Mathis Petrovich、Haotian Zhang、Tingwu Wang、Siyu Tang、Davis Rempe
>
> **机构**：NVIDIA、ETH Zürich
>
> **论文时间**：2026-07-09
>
> **期刊 / 会议**：arXiv preprint arXiv:2607.08741
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **扩散模型** · **自回归** · **实时** · **文本** · **关键点** · **人体动作**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 提出流式自回归扩散框架，在在线文本提示、关键帧、路径与交互式 locomotion 指令下持续生成动作。
- 用“显式根特征 + 身体潜变量”混合表示兼顾全局轨迹精确控制与局部姿态压缩，降低纯高维动作扩散的实时成本。
- 设计两阶段自回归 Transformer 去噪器和可变历史上下文，以 4 步扩散实现约 33 ms 一段的交互生成。

## 研究问题

离线动作生成可使用完整未来条件，但无法响应运行中变化的提示；既有在线模型速度快却常只有短历史或弱文本控制。ARDY 要在因果流式约束下同时保留文本语义、长时目标和几何可控性。

## 原论文重点图

![ARDY 交互式生成](figures/key-figure.png)

**图 1：ARDY 交互控制能力与总体结构（原论文 Figure 1 所在页）。** 系统把已生成历史与当前在线条件组成自回归上下文，显式根通道承担路径/朝向，latent body 通道承担姿态细节；每次只生成下一块，再把结果接回历史。

## 研究方法详细解读

### 混合动作表示

根平移、朝向和速度直接保留，使鼠标/键盘或路径条件能对全局运动施加硬度更高的控制；身体姿态经编码器压缩为 latent，减少扩散维度。若全部隐式化，轨迹误差难纠正；若全部显式化，实时去噪成本和冗余过高。

### 两阶段自回归去噪

第一阶段聚合可变长度历史、文本和长期运动学约束，第二阶段细化当前生成块。训练从真值随机采样文本、关键帧与路径条件，并随机化历史长度，使模型适应运行时上下文逐步增长及提示切换。

### 流式推理

每块通过 4 个去噪步生成，约 33 ms 延迟满足交互动画；边界连续性依赖历史条件和重叠设计。该延迟不含人体到机器人的重定向与控制，因此机器人系统仍需要另行测量闭环预算。

## 实验结果与结论

论文在 HumanML3D 与大规模 Bones Rigplay 上比较质量、约束遵循和实时性，并展示动态文本切换、关键帧、路径与键鼠控制。ARDY 的优势是在线可控生成，不以物理执行为训练目标。

## 局限与复现提醒

- 自回归长序列仍可能累积 root/接触漂移，提示突变时需要过渡策略。
- 复现需固定动作编码器、显式/隐式维度、块长、历史采样和 4 步 sampler。
- 本知识库尚未运行交互 Demo 或机器人链路。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法解读。
- 资源：项目页已核验，代码/权重状态待正式发布确认。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2607.08741)
- [项目页](https://research.nvidia.com/labs/sil/projects/ardy/)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理混合表示、两阶段流式扩散和实时性边界。
