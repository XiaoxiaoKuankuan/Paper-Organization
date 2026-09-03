<!--
---
id: P0002
title_en: "GENMO: A GENeralist Model for Human MOtion"
title_zh: "GENMO：一个用于人体运动的通才模型"
year: 2025
date: 2025-05-02
venue: "ICCV 2025 (Highlight)"
primary_category: motion-generation
tags:
  - motion-generation
  - human-motion
  - multimodal
  - diffusion
  - transformer
  - text
  - music
  - video
  - smpl
authors:
  - Jiefeng Li
  - Jinkun Cao
  - Haotian Zhang
  - Davis Rempe
  - Jan Kautz
  - Umar Iqbal
  - Ye Yuan
institutions:
  - NVIDIA
paper_url: "https://arxiv.org/abs/2505.01425"
project_url: "https://research.nvidia.com/labs/dair/genmo"
github_url: "https://github.com/NVlabs/GENMO"
video_url: null
open_source:
  code: full
  training_code: full
  inference_code: full
  model_weights: full
  dataset: "no"
  robot_deployment: "no"
open_source_checked: 2026-09-03
robots: []
inputs:
  - video
  - 2D keypoints
  - text
  - music
  - 3D keyframes
outputs:
  - SMPL human motion
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0002/GENMO：A GENeralist Model for Human MOtion.pdf"
  - "local_archive/P0002/GENMO_方法详解与全文翻译.pdf"
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0002｜GENMO：一个用于人体运动的通才模型

*GENMO: A GENeralist Model for Human MOtion*

[论文](https://arxiv.org/abs/2505.01425) · [项目页](https://research.nvidia.com/labs/dair/genmo) · [官方代码](https://github.com/NVlabs/GENMO) · [方法详解与全文翻译](attachments/方法详解与全文翻译.pdf)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Jiefeng Li、Jinkun Cao、Haotian Zhang、Davis Rempe、Jan Kautz、Umar Iqbal、Ye Yuan
>
> **机构**：NVIDIA
>
> **论文时间**：2025-05-02
>
> **期刊 / 会议**：ICCV 2025 (Highlight)
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **人体动作** · **多模态** · **扩散模型** · **Transformer** · **文本** · **音乐** · **视频** · **SMPL**
>
> **阅读状态**：已精读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

### 资料与开源说明

- 名称说明：官方项目后来将 GENMO 更名为 GEM，但论文题名和永久档案 ID 保持不变。
- 开源核验：官方仓库提供训练/推理代码与 GEM-SMPL 权重；训练所需完整数据集未随仓库发布。

## 本文贡献

- 提出统一的扩散 Transformer，把视频/2D 姿态下的确定性动作估计与文本、音乐、关键帧下的多样动作生成放入同一训练目标。
- 设计逐帧加法条件融合与带时间区间的 Multi-Text Attention，使不同模态、多个文本片段和可变长度序列能共用主干。
- 通过“生成模式 + 最大噪声估计模式”以及关节、顶点、接触、2D 重投影等几何监督，让生成先验反哺估计，并用野外 2D 视频扩大训练分布。

## 研究问题

传统方法把估计与生成拆成不同模型，无法共享人体时序和运动学先验。论文希望同一网络既能在视频条件下精确恢复动作，又能在文本或音乐条件下保持多样性，并支持变长、分时段和多模态组合控制。

## 原论文重点图

![GENMO 统一模型](figures/genmo-model.png)

**图 1：GENMO 统一模型设计（原论文方法图）。** 带噪动作与逐帧条件先投影到同一隐空间，视频特征、2D 关键点、相机、音乐等通过加法融合；文本通过跨注意力注入。相同 Transformer 主干依据条件强弱既可执行扩散去噪，也可在最大噪声处直接回归。

![多文本时间控制](figures/multi-text-attention.png)

**图 2：Multi-Text Attention（原论文方法图）。** 每条文本附带有效时间区间，注意力掩码只允许对应动作帧读取该文本，从而表达“前半段走路、后半段跳舞”等分段控制，而不必把文本硬对齐为逐帧特征。

## 研究方法详细解读

### 条件编码与统一主干

- 逐帧对齐条件先经独立 MLP 投影和有效区间掩码，再在公共隐空间加法融合。
- 文本没有天然帧对齐关系，因此通过带时间窗口的跨注意力注入；多段文本可控制不同时间区间。
- RoPE 与滑动窗口注意力负责变长时序建模，减少绝对位置长度绑定。
- 输出使用 151 维动作表示，联合局部关节旋转、gravity-view 全局轨迹、相机相关量和手脚接触；主干隐层为 512、12 层、8 个注意力头，RoPE 支持滑窗外推。

### 双模式训练与几何监督

同一网络按样本切换两类目标：文本/音乐等高方差条件使用标准扩散生成损失；视频/2D 关键点等低方差强条件同时使用生成模式和最大噪声下直接回归的估计模式。解码后的关节、顶点、接触和 2D 重投影损失提供几何约束。对于仅有 2D 标注的野外视频，模型先估计伪 3D，再用重投影监督反哺生成训练。

### 推理与机器人链路

推理从噪声出发，在一次扩散过程中接受任意可用条件组合。论文输出是人体 SMPL 运动，不是机器人关节控制；接入人形机器人仍需重定向和跟踪控制链路。

## 实验结果与结论

论文在人体运动估计、文本生成、音乐舞蹈、关键帧插值和混合条件任务上评估。AIST++ 中统一模型的动作多样性、PFC 与 BAS 优于专用 music-only 版本，但 FID 存在分布贴合权衡。双模式训练优于仅扩散或仅回归，说明生成先验与精确估计可相互促进。

## 局限与复现提醒

- “任意长度”依赖滑动窗口和训练外泛化，长序列仍可能累积漂移。
- 不同动作表示转换带来分布偏移。
- 人体运动质量不等于机器人动力学可执行性。

### 对个人研究的价值

GENMO 适合作为视频/文本/音乐到人体运动的统一上游。机器人链路需要明确区分：GENMO 生成 SMPL → 重定向得到机器人参考 → GMT/SONIC 跟踪执行。

## 阅读与复现状态

- 阅读：已深读原文、方法详解与全文翻译。
- 资源：已核验官方代码与权重入口。
- 运行：本知识库尚未执行官方 Demo 或训练。
- 机器人：尚未完成重定向与闭环控制验证。


## 参考资料

- [论文](https://arxiv.org/abs/2505.01425)
- [项目页](https://research.nvidia.com/labs/dair/genmo)
- [官方代码](https://github.com/NVlabs/GENMO)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：建立 GENMO 精读档案，记录 GEM 更名与当前开源状态，登记本地原文和译解材料。
- 2026-09-03：纳入译解附件和原论文方法图，补充 151D 表征、网络结构及双模式训练解读。
