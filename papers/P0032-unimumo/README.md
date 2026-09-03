<!--
---
id: P0032
title_en: "UniMuMo: Unified Text, Music and Motion Generation"
title_zh: "UniMuMo：统一文本、音乐与动作生成"
year: 2024
date: 2024-10-06
venue: "AAAI 2025"
primary_category: motion-generation
tags: [motion-generation, multimodal, autoregressive, transformer, text, music, dance-generation]
authors: [Han Yang, Kun Su, Yutong Zhang, Jiaben Chen, Kaizhi Qian, Gaowen Liu, Chuang Gan]
institutions: [The Chinese University of Hong Kong, University of Washington, University of British Columbia, UMass Amherst, MIT-IBM Watson AI Lab, Cisco Research]
paper_url: "https://arxiv.org/abs/2410.04534"
project_url: "https://hanyangclarence.github.io/unimumo_demo/"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, motion]
outputs: [text, music, motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0032｜UniMuMo：统一文本、音乐与动作生成

*UniMuMo: Unified Text, Music and Motion Generation*

[论文](https://arxiv.org/abs/2410.04534) · [项目页](https://hanyangclarence.github.io/unimumo_demo/)

## 本文贡献

- 在缺少大规模配对数据时，通过节拍检测与动态时间规整将独立音乐、舞蹈对齐，利用音乐-only 与动作-only 数据。
- 将动作映射到音乐模型的残差码本空间，并行自回归生成音乐与动作，使任意一方可作为另一方条件。
- 以跨模态因果注意力和混合专家组合预训练单模态模型，在一个 encoder–decoder Transformer 中支持文本、音乐、动作多向生成。

## 研究问题

音乐和动作虽共享节奏结构，却缺少成对数据；分别量化后 token 时间率也不同。UniMuMo 通过节拍对齐构造弱配对，再在共享声学/动作 token 时间轴上联合生成，降低从头训练多模态模型的成本。

## 原论文重点图

![UniMuMo 统一生成](figures/key-figure.png)

**图 1：文本、音乐和动作的统一输入输出（原论文 Figure 1 所在页）。** 音乐与动作先在节拍层对齐并 token 化，模型沿共同时间步并行预测两条序列；文本可描述或控制任一/两者。

## 研究方法详细解读

### 弱配对数据构建

系统从独立音乐和动作中提取视觉/声学 beat，再用 DTW 拉伸时间轴使节拍对齐。该过程扩展数据量，但“节拍相同”并不保证风格/语义匹配，因此属于带噪弱监督。

### 共享码本与并行生成

动作 encoder 把运动映射到预训练音乐 codec 的多层残差码本特征空间；decoder 恢复动作。音乐和动作 token 在每个时间块并行预测，而非把完整音乐序列放在动作之前，减少单向偏置。

### 跨模态注意力与专家

各模态保留自身因果流，同时允许同步位置交换信息；MoE 为音乐/动作分配专门容量。文本 encoder 提供全局语义，模型通过掩码决定执行 music↔motion、text→music/motion 等任务。

## 实验结果与结论

论文在各单向生成 benchmark 上达到有竞争力结果，并展示音乐—舞蹈双向生成和文本控制。贡献在数据利用和统一结构；弱配对噪声仍限制精确编舞对应。

## 局限与复现提醒

- DTW 需记录 beat detector、允许拉伸范围和重采样策略，否则音频/动作时长会漂移。
- 用音乐码本承载动作需单独验证重建，不应只看最终 FID。
- 人体动作输出不含机器人接触或力矩约束。

## 阅读与复现状态

- 阅读：已阅读论文与飞书整理。
- 资源：项目页已核验，代码/模型状态待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2410.04534)
- [项目页](https://hanyangclarence.github.io/unimumo_demo/)

## 更新记录

- 2026-09-03：新建条目，解析节拍弱配对、共享残差码本和并行生成。
