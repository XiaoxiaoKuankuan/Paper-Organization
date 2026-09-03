<!--
---
id: P0037
title_en: "Odoriko: A Shape-Aware Multimodal Diffusion Framework for Human Motion"
title_zh: "Odoriko：形状感知的多模态人体动作扩散框架"
year: 2026
date: 2026-06-19
venue: "ECCV 2026"
primary_category: motion-generation
tags: [motion-generation, multimodal, diffusion, smpl, pose-estimation, text, music, video]
authors: [Dongseok Shim, Julian Tanke, Kengo Uchida, Christian Simon, Koichi Saito, Takashi Shibuya, Shusuke Takahashi, Yuki Mitsufuji]
institutions: [Sony Group Corporation, Sony AI]
paper_url: "https://arxiv.org/abs/2606.21135"
project_url: "https://dsshim0125.github.io/odoriko.github.io/"
github_url: "https://github.com/sony/creativeai"
video_url: null
open_source: {code: partial, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, video, 2D pose, body shape]
outputs: [shape-aware SMPL motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0037｜Odoriko：形状感知的多模态人体动作扩散框架

*Odoriko: A Shape-Aware Multimodal Diffusion Framework for Human Motion*

[论文](https://arxiv.org/abs/2606.21135) · [项目页](https://dsshim0125.github.io/odoriko.github.io/) · [Sony 研究入口](https://github.com/sony/creativeai)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Dongseok Shim、Julian Tanke、Kengo Uchida、Christian Simon、Koichi Saito、Takashi Shibuya、Shusuke Takahashi、Yuki Mitsufuji
>
> **机构**：Sony Group Corporation、Sony AI
>
> **论文时间**：2026-06-19
>
> **期刊 / 会议**：ECCV 2026
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **扩散模型** · **SMPL** · **姿态估计** · **文本** · **音乐** · **视频**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 在统一文本、音乐、视频、2D 姿态动作模型中显式加入性别与 SMPL 形状参数，使运动学输出与“谁在运动”一致。
- 当视频条件没有形状标签时，同时恢复人体形状与动作，将估计和生成放入同一扩散框架。
- 采用类似 GENMO 的 estimation/generation 双模式：强观测条件下直接估计，弱条件下多样生成，并以分层方式注入模态与形态条件。

## 研究问题

既有统一模型通常把不同体形的运动平均到同一分布，忽略腿长、体重分布和性别对步态/舞姿的系统影响。Odoriko 把 body shape 作为条件变量，避免模型仅根据动作语义生成“平均身体”的运动。

## 原论文重点图

![Odoriko 形状感知框架](figures/key-figure.png)

**图 1：Odoriko 多模态与形状条件框架（原论文 Figure 1 所在页）。** 文本/音乐驱动生成，视频/2D 姿态驱动估计；SMPL 形状和性别在网络不同层级调制动作。视频无显式形状时，网络还预测形状分支。

## 研究方法详细解读

### 动作与形状解耦

姿态、根运动和 body shape 分开编码，形状条件通过分层调制影响去噪表示，而不是简单复制到每帧。这样同一语义动作可在不同体形上表现出相应运动学差异，同时保持动作内容。

### 多模态双模式训练

文本/音乐属于一对多生成条件，使用扩散采样；视频/2D 姿态是强观测，增加最大噪声/回归式估计路径。共享主干学习通用运动先验，模态适配器保留条件粒度。

### 联合形状恢复

视频输入时形状未知，模型从视觉运动证据预测 SMPL 形状并用于动作解码。形状和姿态存在可辨识性耦合，衣服、相机与遮挡会使形状误差反过来影响运动。

## 实验结果与结论

论文在文本动作、音乐舞蹈、视频动作估计上达到或超过多种专用模型，并新增形态一致性评价。结果说明 shape conditioning 有价值，但 FID 等指标仍受表示转换与评估器影响。

## 局限与复现提醒

- SMPL shape 不等于真实质量/惯量，不能直接作为机器人物理参数。
- 视频形状估计受服装和视角偏差；多任务权重会造成生成/估计折中。
- Sony 汇总仓库存在项目入口，但完整训练代码与权重需进一步核验。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：项目页与 Sony 汇总入口已核验，完整开源边界待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2606.21135)
- [项目页](https://dsshim0125.github.io/odoriko.github.io/)
- [Sony Creative AI](https://github.com/sony/creativeai)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理形状条件、估计/生成双模式与形状恢复边界。
