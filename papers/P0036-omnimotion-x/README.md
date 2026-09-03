<!--
---
id: P0036
title_en: "OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation"
title_zh: "OmniMotion-X：多用途多模态全身动作生成"
year: 2025
date: 2025-10-22
venue: "CVPR 2026 Findings"
primary_category: motion-generation
tags: [motion-generation, multimodal, diffusion, autoregressive, smplx, large-scale-data, motion-editing]
authors: [Guowei Xu, Yuxuan Bian, Ailing Zeng, Zhuo Chen, Mingyi Shi, Shaoli Huang, Wen Li, Lixin Duan, Qiang Xu]
institutions: [University of Electronic Science and Technology of China, The Chinese University of Hong Kong, The University of Hong Kong, Tencent]
paper_url: "https://arxiv.org/abs/2510.19789"
project_url: null
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, speech, reference motion, keypoints, trajectory]
outputs: [SMPL-X whole-body motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0036｜OmniMotion-X：多用途多模态全身动作生成

*OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation*

[论文](https://arxiv.org/abs/2510.19789)

## 本文贡献

- 以统一 sequence-to-sequence 自回归 Diffusion Transformer 支持文本动作、音乐舞蹈、语音手势、预测、插值、补全和关节/轨迹控制及其组合。
- 将参考动作作为显式条件，增强内容、风格和时间动态一致性；提出从弱条件到强条件的渐进混合训练缓解模态冲突。
- 构建 OmniMoCap-X：统一 28 个 MoCap 来源、10 类任务为 30 FPS SMPL-X，并以渲染视频 + GPT-4o 生成层级描述。

## 研究问题

多任务模型既要处理全局文本，又要处理逐帧音频和稀疏几何约束；强条件过早加入会让模型忽略弱语义。OmniMotion-X 通过自回归块生成和 weak-to-strong 课程，先学通用动作，再逐步增加精确约束。

## 原论文重点图

![OmniMotion-X 自回归生成](figures/key-figure.png)

**图 1：OmniMotion-X 分块自回归 DiT（原论文 Figure 1 所在页）。** 动作以约 150 帧块连续生成，每块可接收文本、音乐、语音和控制条件；先前块成为下一块上下文，从而支持交互式长动作和条件切换。

## 研究方法详细解读

### OmniMoCap-X

28 个来源先转换为 SMPL-X/30 FPS，共约 6430 万帧、286.2 小时；渲染后由视觉语言模型生成低层动作与高层语义描述。统一格式扩大任务覆盖，也引入人体拟合和自动描述误差。

### 自回归 Diffusion Transformer

单个 DiT 对当前块做扩散生成，已生成块作为因果上下文。相比整段一次扩散，分块可延伸长度和在线修改；代价是边界与长期漂移累积，需要训练时模拟历史误差。

### 渐进混合条件

训练先使用弱/全局条件建立自然动作先验，再逐步加入关键点、轨迹和参考动作等强约束。参考动作提供风格和节奏模板；当多个条件冲突时，课程顺序隐含优先级，而非显式求解。

## 实验结果与结论

论文在多个文本、音乐、语音和空间控制基准上取得领先或有竞争力结果，并展示长时组合控制。统一能力来自数据和训练协议共同作用，不应只归因于 DiT 结构。

## 局限与复现提醒

- 30 FPS、SMPL-X 参数、150 帧块和历史长度是关键接口。
- VLM 自动描述需抽样审计；28 数据集许可与可下载性不等同。
- 机器人部署仍需重定向与低层控制。

## 阅读与复现状态

- 阅读：已阅读论文与飞书详细整理。
- 资源：论文入口已核验，代码/完整数据状态待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2510.19789)

## 更新记录

- 2026-09-03：新建条目，整理 OmniMoCap-X、分块自回归扩散和渐进混合条件。
