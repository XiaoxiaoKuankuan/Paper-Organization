<!--
---
id: P0020
title_en: "MACE-Dance: Motion-Appearance Cascaded Experts for Music-Driven Dance Video Generation"
title_zh: "MACE-Dance：面向音乐驱动舞蹈视频生成的动作—外观级联专家"
year: 2025
date: 2025-12-20
venue: "arXiv preprint arXiv:2512.18181"
primary_category: motion-generation
tags: [dance-generation, music, video, diffusion, mixture-of-experts, physical-plausibility]
authors: [Kaixing Yang, Jiashu Zhu, Xulong Tang, Ziqiao Peng, Xiangyue Zhang, Puwei Wang, Jiahong Wu, Xiangxiang Chu, Hongyan Liu, Jun He]
institutions: [Renmin University of China, AMAP Alibaba Group, Malou Tech, Wuhan University, Tsinghua University]
paper_url: "https://arxiv.org/abs/2512.18181"
project_url: "https://macedance.github.io/"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [music, reference image]
outputs: [3D dance motion, dance video]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0020｜MACE-Dance：面向音乐驱动舞蹈视频生成的动作—外观级联专家

*MACE-Dance: Motion-Appearance Cascaded Experts for Music-Driven Dance Video Generation*

[论文](https://arxiv.org/abs/2512.18181) · [项目页](https://macedance.github.io/)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Kaixing Yang、Jiashu Zhu、Xulong Tang、Ziqiao Peng、Xiangyue Zhang、Puwei Wang、Jiahong Wu、Xiangxiang Chu、Hongyan Liu、Jun He
>
> **机构**：Renmin University of China、AMAP Alibaba Group、Malou Tech、Wuhan University、Tsinghua University
>
> **论文时间**：2025-12-20
>
> **期刊 / 会议**：arXiv preprint arXiv:2512.18181
>
> **主分类**：动作生成
>
> **重点标签**：**舞蹈生成** · **音乐** · **视频** · **扩散模型** · **混合专家** · **物理合理性**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 将音乐到舞蹈视频拆成 Motion Expert 与 Appearance Expert：先生成三维身体运动，再按参考人物外观合成时序一致视频。
- Motion Expert 采用 BiMamba–Transformer 扩散骨干与 Guidance-Free Training，同时建模长时音乐结构、运动学合理性和表现力。
- Appearance Expert 使用运动学—美学解耦微调，并构建面向动作质量与视觉外观的联合数据/评测协议。

## 研究问题

音乐舞蹈动作生成、姿态驱动人物动画和最终舞蹈视频的目标不同：动作要踩点且符合人体运动学，视频还要保持身份、纹理和跨帧一致。直接端到端生成容易让外观损失掩盖动作错误，因此论文采用级联专家分工。

## 原论文重点图

![MACE-Dance 总览](figures/key-figure.png)

**图 1：动作—外观级联流程（原论文 Figure 1 所在页）。** 音乐先进入 Motion Expert 得到 3D 舞蹈，随后与参考图共同驱动 Appearance Expert。中间 3D 表示既是可解释接口，也是两阶段误差传播点。

## 研究方法详细解读

### 总体流程：先编舞，再按人物外观渲染视频

MACE-Dance 是严格的两级级联。Motion Expert 读取音乐，扩散生成 SMPL 三维舞蹈；生成姿态经固定相机渲染成人体网格，再由 ViTPose 提取/校正 2D 姿态；Appearance Expert 同时读取这条姿态控制和一张人物参考图，在视频 DiT 中合成保持身份的舞蹈视频。两个专家分别在动作数据和人物视频数据上训练，没有把最终像素损失穿过姿态提取器反向传到 Motion Expert，因此动作与外观的能力和误差来源可以分开分析。

### Motion Expert 的输入与 Dance Block

音乐先由 Librosa 提取节拍、色度等低维特征，再经 BiMamba 编码成长时序条件。带噪三维动作和扩散时刻进入多个 Dance Block：局部 BiMamba 以线性复杂度建模动作连续，cross-attention Transformer 从音乐读取全局段落/节奏，FiLM 用时间步与控制强度调节各层。该组合让 Mamba 负责长序列效率、注意力负责跨模态对齐，最终头直接回归干净连续动作。

### 动作训练目标与 Guidance-Free Training

Motion Expert 以 `x0` 扩散重建为主，同时用前向运动学后的关节位置、帧间速度和接触脚速度约束骨架、平滑与脚滑。Guidance-Free Training 把控制系数 `β` 作为训练条件，随机覆盖弱到强的音乐约束，使一次条件前向就能调节保真度/多样性；它替代传统 CFG 的条件/无条件双前向，但模型仍需在训练中见到不同控制强度。音乐与动作数据在这一阶段完成对齐，尚不涉及人物纹理。

### 姿态桥接与 Appearance Expert

预测 SMPL 先渲染为固定视角 mesh，再转成 2D 骨架，形成与视频生成 backbone 兼容的 pose control。Appearance Expert 基于 Wan-Animate 类架构：body adapter 编码骨架，reference branch 编码人物外观，二者注入视频 DiT，以保持动作、身份和背景时序。这个桥接会把三维根朝向、遮挡和相机假设投影到二维，因此渲染相机与姿态检测器也是系统的一部分，不是无损格式转换。

### 外观模型的两阶段微调

第一阶段“运动学微调”冻结大部分预训练视频 backbone，只训练 body adapter/运动通路，让生成帧遵循骨架且肢体时序稳定；第二阶段“美学微调”固定已学运动通路，在注意力 `q/k/v/o` 与前馈层加入 LoRA，学习人物身份、服装、纹理和镜头风格。分开优化防止美学数据把动作控制冲淡，也避免仅靠姿态数据损害预训练视频画质。

### 推理与误差传播

推理先从音乐采样完整三维舞蹈，再一次性或分段产生 pose sequence，最后与参考图生成视频；Motion Expert 的脚滑、穿插或错误朝向会被 Appearance Expert 忠实渲染甚至视觉放大，后者不能从像素侧修正三维动力学。评估必须同时查看三维生成的 FID/节拍/接触和视频的时空质量、身份保持及姿态一致性。系统面向人体视频，不输出机器人命令；用于机器人还需在三维动作阶段另接重定向与控制。

## 实验结果与结论

论文报告两个专家在各自任务上达到强基线，并在联合 motion–appearance 协议下改善音乐舞蹈视频。结论说明级联可降低跨目标冲突，但并不代表 3D 动作适合机器人执行。

## 局限与复现提醒

- 两阶段推理带来累计误差和更高总延迟；视频身份保持也受参考图质量影响。
- 机器人研究主要可复用 Motion Expert，Appearance Expert 属于视频生成链。
- 当前代码/模型发布边界待核验，本知识库未运行。

## 阅读与复现状态

- 阅读：已阅读原论文摘要、方法页与飞书整理。
- 资源：项目页已核验，代码与模型待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2512.18181)
- [项目页](https://macedance.github.io/)

## 更新记录

- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理动作—外观级联、两类专家及联合评价边界。
