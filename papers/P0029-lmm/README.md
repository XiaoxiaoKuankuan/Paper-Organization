<!--
---
id: P0029
title_en: "Large Motion Model for Unified Multi-Modal Motion Generation"
title_zh: "LMM：用于统一多模态动作生成的大动作模型"
year: 2024
date: 2024-04-01
venue: "ECCV 2024"
primary_category: motion-generation
tags: [motion-generation, multimodal, diffusion, transformer, large-scale-data, human-motion]
authors: [Mingyuan Zhang, Daisheng Jin, Chenyang Gu, Fangzhou Hong, Zhongang Cai, Jingfang Huang, Chongzhi Zhang, Xinying Guo, Lei Yang, Ying He, Ziwei Liu]
institutions: [S-Lab Nanyang Technological University, SenseTime Research]
paper_url: "https://arxiv.org/abs/2404.01284"
project_url: "https://mingyuan-zhang.github.io/projects/LMM.html"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, speech, motion constraints]
outputs: [human motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0029｜LMM：用于统一多模态动作生成的大动作模型

*Large Motion Model for Unified Multi-Modal Motion Generation*

[论文](https://arxiv.org/abs/2404.01284) · [项目页](https://mingyuan-zhang.github.io/projects/LMM.html)

## 本文贡献

- 构建 MotionVerse：统一 16 个数据集、10 类任务、约 32 万序列和 1 亿帧，建立多模态动作预训练底座。
- 在 Diffusion Transformer 中提出 ArtAttention，将身体划为 10 个区域并显式建模部位内与部位间关系。
- 采用可变 FPS 与多种掩码的预训练策略吸收异构数据，使单一 generalist 在已见任务上接近专家，并对未见条件组合出现迁移能力。

## 研究问题

不同动作数据集使用不同骨架、FPS、任务和条件，简单混合会使模型学习到数据源标识而非通用动作规律。LMM 从数据、骨架结构注意力和预训练采样三方面统一异构性。

## 原论文重点图

![LMM 与 MotionVerse](figures/key-figure.png)

**图 1：MotionVerse 与通用 LMM（原论文 Figure 1 所在页）。** 多个文本、音乐、语音、姿态任务统一到动作条件生成；ArtAttention 在同一 DiT 内按身体区域组织 token，使共享模型仍保留人体拓扑归纳偏置。

## 研究方法详细解读

### MotionVerse 统一

数据先映射到公共动作格式并规范 FPS、坐标、长度和条件。10 个任务通过条件类型与掩码定义，而不是维护 10 套输出头；采样需平衡大数据集，避免长尾任务被帧数淹没。

### ArtAttention

关节按 10 个身体区域分组，注意力先捕捉局部协同，再交换跨部位信息。相较全连接时空注意力，它强调肢体结构并降低无关交互，但区域划分是人工先验。

### 可变 FPS 与掩码预训练

随机帧率让模型学习时间尺度不变性，不同掩码对应预测、补全、条件生成等任务。预训练目标共享，任务在推理时由可见条件和 mask 形式确定。

## 实验结果与结论

LMM 在多项标准任务上与专用模型竞争，并展示未见任务/条件的 emergent transfer；消融支持数据、ArtAttention 和预训练策略均有贡献。结果不代表所有任务都超过专家，也不含机器人动力学。

## 局限与复现提醒

- MotionVerse 的 16 数据集许可、预处理和采样权重需分别追踪。
- 可变 FPS 必须保持速度/接触定义一致，否则只是改变数值尺度。
- 统一人体动作输出仍需机器人重定向与跟踪。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：项目页已核验，完整代码/数据边界待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2404.01284)
- [项目页](https://mingyuan-zhang.github.io/projects/LMM.html)

## 更新记录

- 2026-09-03：新建条目，整理 MotionVerse、ArtAttention 与多任务预训练策略。
