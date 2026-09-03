<!--
---
id: P0028
title_en: "MCM: Multi-condition Motion Synthesis Framework"
title_zh: "MCM：多条件动作合成框架"
year: 2024
date: 2024-04-19
venue: "IJCAI 2024"
primary_category: motion-generation
tags: [motion-generation, multimodal, diffusion, transformer, text, audio, mixture-of-experts]
authors: [Zeyu Ling, Bo Han, Yongkang Wongkan, Han Lin, Mohan Kankanhalli, Weidong Geng]
institutions: [Zhejiang University, National University of Singapore]
paper_url: "https://arxiv.org/abs/2404.12886"
project_url: null
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, speech]
outputs: [human motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0028｜MCM：多条件动作合成框架

*MCM: Multi-condition Motion Synthesis Framework*

[论文](https://arxiv.org/abs/2404.12886)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Zeyu Ling、Bo Han、Yongkang Wongkan、Han Lin、Mohan Kankanhalli、Weidong Geng
>
> **机构**：Zhejiang University、National University of Singapore
>
> **论文时间**：2024-04-19
>
> **期刊 / 会议**：IJCAI 2024
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **扩散模型** · **Transformer** · **文本** · **音频** · **混合专家**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 提出主分支 + 控制分支的双分支扩散框架，将已训练文本动作模型扩展到音乐、语音与多条件输入。
- 控制分支复制主分支结构和权重，并通过零初始化连接注入新条件，尽量保留主模型已有文本生成能力。
- 设计 MWNet 与 multi-wise attention，同时在时间、关节/通道等维度建模动作相关性，可作为 DDPM 类主干。

## 研究问题

不同模态条件粒度差异明显：文本全局、音频逐帧；直接联合训练可能破坏已有单模态能力。MCM 借鉴 ControlNet 思路，将新模态适配隔离到控制分支，再逐层影响冻结/稳定主分支。

## 原论文重点图

![MCM 双分支框架](figures/key-figure.png)

**图 1：MCM 主分支—控制分支方法（原论文 Figure 1 所在页）。** 主分支保留原文本扩散能力，控制分支读取音频或其他条件；多层零卷积/零映射把控制残差注入主干，使初始模型行为不被突然破坏。

## 研究方法详细解读

### 总体流程：先学文本动作主干，再插入音频控制分支

MCM 采用两阶段 ControlNet 式训练。Stage 1 在 HumanML3D 上训练文本条件 MWNet 主分支，学会动作质量和语义；Stage 2 复制主分支形成可训练 control branch，冻结原主干，将音乐或语音 Jukebox 特征与带噪动作相加送入控制分支；其每层输出经零初始化 bridge 加到主分支对应层。最终主分支仍负责扩散 `x0` 预测，控制分支只学习音频相对既有文本动作先验的残差。

### 统一数据和条件前处理

HumanML3D、AIST++ 与 BEAT 都转换为相同 22 关节骨架/动作表示和 20 FPS，使同一扩散网络可接收日常动作、舞蹈和说话手势。文本由冻结 CLIP 提取，音乐与语音均取 Jukebox 前层特征并下采样到动作帧率。统一骨架只是张量契约，三个数据集的动作风格和条件密度仍不同；训练第二阶段时必须明确使用哪种音频数据和对应分支。

### MWNet 的 Multi-Wise Attention

带噪动作 `X∈T×C` 先线性映射，网络在每层交替做 time-wise self-attention 与 channel-wise self-attention：前者计算不同帧的相关性，后者转置注意力方向，在通道组内学习关节/姿态维度的协同。cross-attention读取文本，FFN 处理逐 token 特征；扩散 timestep 经 FiLM 产生缩放和偏置，在注意力/FFN 后调制特征。相比只沿时间注意，channel 分支显式建模左右肢体和关节通道关系，但并非固定骨架图卷积。

### 控制分支与 bridge 的信息流

control branch 结构和初始化均复制训练好的主干，输入是动作 latent 与逐帧音频特征的逐元素和；每层控制特征通过全连接或 1D convolution bridge 注入主干下一层。bridge 权重从零开始，所以 Stage 2 第一步的系统输出与文本主干完全相同，之后才逐渐学会节拍/语音偏移；主干冻结避免新数据破坏基础动作。代价是训练和推理近似多运行一套网络，实时预算需包含控制分支。

### 扩散目标与训练参数

前向过程使用 1,000 个 DDPM 步，`β` 从 0.0001 线性增至 0.02；网络不预测噪声，而是回归干净 `x_start`，让姿态重建监督更直接。两阶段都用 Adam、学习率 `2e-4`：第一阶段更新 MWNet 文本主干，第二阶段只更新 control branch 和 bridges。音频逐帧条件、文本全局条件及扩散时间在不同位置注入，不能简化为把多模态向量一次拼到输入。

### 推理与多条件组合

推理从高斯动作噪声开始，每个反向步由冻结文本主干给出语义/动作先验，音频分支经 bridge 修正各层特征，反复得到干净动作。仅文本时可关闭控制分支；音乐或语音时启用对应训练分支；文本+音频同时输入则形成软融合。条件冲突没有硬优先级或可满足性求解，结果由 bridge 强度和训练分布决定。

### 证据边界

MCM 统一的是人体动作生成主干，AIST++/BEAT 的节拍和语义指标不含机器人动力学。零初始化保证训练起点不破坏主干，不保证训练结束后完全无遗忘；复现应分别评估 Stage 1 主干、Stage 2 单模态和混合条件。机器人应用仍需要重定向、物理筛选与低层跟踪。

## 实验结果与结论

论文在文本动作上达到强结果，在音乐舞蹈和语音手势上具有竞争力，并展示多条件控制。贡献主要在可插拔条件适配，而非新的机器人控制算法。

## 局限与复现提醒

- 双分支提高显存和推理成本；“保留能力”需用旧任务回归测试验证。
- 音频 FPS、特征窗口与动作帧对齐是核心接口。
- 生成结果未经过机器人动力学验证。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：代码/权重开源状态待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2404.12886)

## 更新记录

- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，解析双分支条件适配、零初始化和 MWNet。
