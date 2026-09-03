<!--
---
id: P0031
title_en: "MotionCraft: Crafting Whole-Body Motion with Plug-and-Play Multimodal Controls"
title_zh: "MotionCraft：使用即插即用多模态控制生成全身动作"
year: 2024
date: 2024-07-30
venue: "AAAI 2025"
primary_category: motion-generation
tags: [motion-generation, multimodal, diffusion, transformer, smplx, text, audio]
authors: [Yuxuan Bian, Ailing Zeng, Xuan Ju, Xian Liu, Zhaoyang Zhang, Wei Liu, Qiang Xu]
institutions: [The Chinese University of Hong Kong, Tencent]
paper_url: "https://arxiv.org/abs/2407.21136"
project_url: "https://cure-lab.github.io/MotionCraft"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, speech, motion controls]
outputs: [SMPL-X whole-body motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0031｜MotionCraft：使用即插即用多模态控制生成全身动作

*MotionCraft: Crafting Whole-Body Motion with Plug-and-Play Multimodal Controls*

[论文](https://arxiv.org/abs/2407.21136) · [项目页](https://cure-lab.github.io/MotionCraft)

## 本文贡献

- 建立统一 SMPL-X 的 MC-Bench，解决文本动作、音乐舞蹈和语音手势数据骨架/部位不一致的问题。
- 提出由文本语义预训练到多模态低层控制适配的 coarse-to-fine 两阶段训练，降低不同任务分布直接混合的冲突。
- 在 Diffusion Transformer 中加入 MC-Attn，同时建模静态人体拓扑与动态运动关系，并以即插即用控制分支接入音频等条件。

## 研究问题

文本提供全局语义，音乐/语音提供高频时间条件；各数据集又覆盖不同身体部位。若直接联合训练，模型会在动作分布和条件粒度上相互干扰。MotionCraft 先统一格式，再让文本主干提供动作先验，最后适配细粒度条件。

## 原论文重点图

![MotionCraft 框架](figures/key-figure.png)

**图 1：统一 SMPL-X 与即插即用多模态控制（原论文 Figure 1 所在页）。** 文本主干学习通用动作语义，控制分支读取音乐/语音等逐帧条件；MC-Attn 在身体拓扑与时间动态两条关系上交换信息。

## 研究方法详细解读

### MC-Bench 与统一 SMPL-X

各数据先转换到共同 SMPL-X 全身参数、FPS 和坐标系，再对缺失手/脸部位设定一致处理。统一格式让任务共享主干，但由拟合得到的部位不等同于原始高质量捕捉。

### 两阶段训练

第一阶段用文本动作数据训练语义强、分布广的 DiT 主干；第二阶段保留该先验，通过适配器/控制分支学习音乐和语音的帧级约束。训练顺序降低遗忘，但新任务仍需用旧任务回归测试。

### MC-Attn

静态分支依据骨架连接和身体拓扑组织注意力，动态分支捕捉跨帧运动。二者并行融合，避免纯时序 Transformer 把关节当无结构通道。

## 实验结果与结论

论文在多个标准生成任务上报告强结果，并通过统一 benchmark 展示一个模型处理文本、音乐和语音。结论是格式统一和分阶段适配同样重要；结果仍属于人体动作生成。

## 局限与复现提醒

- SMPL-X 转换误差、缺失部位填充和 FPS 统一会影响跨数据集比较。
- 插件式控制增加参数和训练阶段，不代表任意新模态零成本接入。
- 机器人应用仍需重定向与动力学验证。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：项目页已核验，完整代码/权重边界待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2407.21136)
- [项目页](https://cure-lab.github.io/MotionCraft)

## 更新记录

- 2026-09-03：新建条目，整理 MC-Bench、两阶段训练与 MC-Attn。
