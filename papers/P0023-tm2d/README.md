<!--
---
id: P0023
title_en: "TM2D: Bimodality Driven 3D Dance Generation via Music-Text Integration"
title_zh: "TM2D：通过音乐—文本融合进行双模态三维舞蹈生成"
year: 2023
date: 2023-04-05
venue: "ICCV 2023"
primary_category: motion-generation
tags: [dance-generation, music, text, multimodal, autoregressive, motion-prior]
authors: [Kehong Gong, Dongze Lian, Heng Chang, Chuan Guo, Zihang Jiang, Xinxin Zuo, Michael Bi Mi, Xinchao Wang]
institutions: [National University of Singapore, Huawei Technologies]
paper_url: "https://arxiv.org/abs/2304.02419"
project_url: "https://garfield-kh.github.io/TM2D/"
github_url: null
video_url: null
open_source: {code: partial, training_code: unknown, inference_code: partial, model_weights: unknown, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [music, timed text]
outputs: [3D dance motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0023｜TM2D：通过音乐—文本融合进行双模态三维舞蹈生成

*TM2D: Bimodality Driven 3D Dance Generation via Music-Text Integration*

[论文](https://arxiv.org/abs/2304.02419) · [项目页](https://garfield-kh.github.io/TM2D/)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Kehong Gong、Dongze Lian、Heng Chang、Chuan Guo、Zihang Jiang、Xinxin Zuo、Michael Bi Mi、Xinchao Wang
>
> **机构**：National University of Singapore、Huawei Technologies
>
> **论文时间**：2023-04-05
>
> **期刊 / 会议**：ICCV 2023
>
> **主分类**：动作生成
>
> **重点标签**：**舞蹈生成** · **音乐** · **文本** · **多模态** · **自回归** · **运动先验**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 提出音乐 + 带起止时间文本的双模态舞蹈任务，让文本在指定区间注入“侧手翻/旋转”等语义，同时维持整段音乐节奏。
- 用共享 motion VQ-VAE 将来源分布不同的文本动作与音乐舞蹈数据投到同一离散空间，绕过缺少三模态成对数据的问题。
- 设计跨模态 Transformer 融合文本与音乐，并提出 MPD、Freezing Score 评价动作连续性和冻结比例。

## 研究问题

音乐决定节拍和整体风格，却难精确表达动作事件；文本能描述事件，但没有细粒度节奏。由于几乎不存在“音乐—文本—舞蹈”三元配对，TM2D 需要借共享动作 tokenizer 组合两个数据集的监督。

## 原论文重点图

![TM2D 双模态控制](figures/key-figure.png)

**图 1：带时间区间的文本—音乐控制（原论文 Figure 1 所在页）。** 连续音乐覆盖全序列，文本只在指定 6–8 秒、16–18 秒区间生效；生成舞蹈既要保持节奏，又要在局部完成语义动作。

## 研究方法详细解读

TM2D 最关键的设计是：训练时没有“音乐+文本+舞蹈”三者同时配对的数据，它仍要在推理时让音乐负责节奏、文本负责局部语义。做法不是伪造三模态真值，而是让音乐到舞蹈和文本到动作共享一个离散动作词表与自回归主干，最后在指定时间区间融合两条 token 概率分布。

### 1. 总体定位：三模态控制为什么缺监督

AIST++ 有音乐—舞蹈配对但缺细粒度文本，HumanML3D 有文本—日常动作配对却没有音乐。同一个“转身”在舞蹈与日常动作中分布也不同。若分别训练两个生成器，输出 token 和时序无法直接拼接；若强行合成三模态标签，又会引入虚假监督。TM2D 要证明的是：只靠两类双模态数据，能否通过共享动作量化和概率级融合得到可控舞蹈。

### 2. 整体训练与推理流程：共享词表，双路学习

1. 将 HumanML3D 与 AIST++ 统一为同一 22 关节动作表示，训练共享 VQ-VAE 动作 tokenizer。
2. 音乐编码器提取逐帧节奏特征，文本编码器提取语义条件。
3. 在同一自回归 Transformer 中交替训练 music-to-dance 与 text-to-motion，只对各自真实配对数据监督。
4. 推理时音乐分支持续给出下一动作 token logits；文本分支只在用户指定区间提供语义 logits。
5. 用随时间变化的权重融合两路分布后采样 token，再由共享 VQ decoder 还原完整三维舞蹈。

### 3. 总体信息流：两种配对数据训练一个动作解码器

TM2D 先把 HumanML3D 日常动作与 AIST++ 舞蹈转成同一 22 关节表示，用共享 VQ-VAE 建立动作 token；之后在同一个自回归 Transformer 中交替训练 music-to-dance 和 text-to-motion 两条支路。推理时音乐始终提供逐帧节奏，文本只在指定时间段提高权重，两个分支的 token logits 做时间变化融合；采样出的统一 token 最后由 VQ decoder 解码成连续动作。因此方法不需要“同一舞蹈同时有音乐和文本”的三元组。

### 共享 VQ-VAE 与动作词表

两数据集先统一 FPS、骨架和根坐标，1D convolution encoder 每 8 帧压成一个 latent，再以最近码本向量替换；decoder 从码本恢复关节序列。训练使用重建、embedding 和 commitment 损失，论文设置 crop 64 帧、batch 128、学习率 `1e-4`。共享码本是两任务可融合的必要接口：音乐和文本头必须对同一索引分布打分；若两个数据域各占完全不交叠的码区，logit 融合会退化成域选择而非动作组合。

### 音乐与文本条件编码

音乐由 Librosa 提取 MFCC、delta、chroma、tempogram 和 onset 等时序特征，保留节拍到每个动作 token 的对应；文本用 GloVe/文本 encoder 形成词序列。Transformer decoder 有因果 self-attention读取历史动作码，并配置独立的音乐/文本 cross-attention，以相同隐藏维度向目标 token 提供条件。模型约 6 层、隐藏 512、8 头，训练 batch 64，两个数据流分别计算下一 token 交叉熵并共享动作 decoder 参数。

### 无三模态配对下的训练逻辑

music-to-dance batch 只启用音乐 cross-attention，目标来自 AIST++；text-to-motion batch 只启用文本 cross-attention，目标来自 HumanML3D。共享 VQ 码本和因果主干让两类条件最终落到相同 token 语义，但训练没有直接监督“某段文字应如何修改某首音乐的舞蹈”。因此文本+音乐组合能力是一种通过共享输出空间得到的迁移，必须与有真实三元组监督的方法区分。

### 推理时的时间变化 logit 融合

给定音乐和带有效区间的文本，模型在每个 token 位置分别得到音乐分支与文本分支 logits。文本区间内使用半余弦权重逐渐升到约 0.8 再下降，音乐权重取 `1-w_text`；区间外完全由音乐主导。融合分布采样下一个 token 并循环到结束，再经共享 VQ decoder 还原动作。平滑权重减轻条件突然切换的边界跳变，但属于概率软融合，不保证文本要求与节拍冲突时两者同时满足。

### 评价与失效诊断

除 FID 与 Beat Alignment 外，论文用 Motion Prediction Distance 衡量生成与真实动作分布差异，并用 Freezing Score 统计长时间几乎静止的退化段。后者能发现模型靠停住来降低局部错误，但阈值仍依赖 FPS、骨架和速度定义。复现应先检查 VQ 重建与码本占用，再分别评估两单模态分支和融合输出，不能只用最终舞蹈视频主观判断。

### 机器人边界

输出为人体 22 关节动作，没有机器人关节限位、接触或力矩监督。若用作机器人音乐舞蹈上游，必须先处理人体到机器人骨架映射和 8 倍 token 下采样带来的接触细节，再用物理跟踪器执行；文本时间区间也需转换到机器人参考的实际控制频率。

## 实验结果与结论

论文显示双模态模型能按时间插入文本动作，同时保持与单音乐方法相近的舞蹈质量。结论证明共享离散空间可缓解三元配对缺失，但复杂文本与快速节拍冲突仍有限。

## 局限与复现提醒

- 跨数据集统一的 FPS、骨架和 root 表示是关键前处理。
- 文本区间需用户显式给定，尚非自动从语言推断时间结构。
- 生成人体舞蹈不含物理可执行性约束。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：项目页已核验，未运行代码。
- 机器人：未适配。

## 参考资料

- [arXiv](https://arxiv.org/abs/2304.02419)
- [项目页](https://garfield-kh.github.io/TM2D/)

## 更新记录

- 2026-09-04：按 ADAPT 式方法导读补充三模态真值缺失这一核心问题，并用五步流程讲清共享 VQ 词表、双路训练和时间变化 logit 融合。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理共享码本、时段文本控制和评价指标。
