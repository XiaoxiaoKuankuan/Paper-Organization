<!--
---
id: P0024
title_en: "MotionGPT: Human Motion as a Foreign Language"
title_zh: "MotionGPT：将人体动作视为一种外语"
year: 2023
date: 2023-06-26
venue: "NeurIPS 2023"
primary_category: motion-generation
tags: [motion-generation, transformer, autoregressive, text, motion-editing, human-motion]
authors: [Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, Tao Chen]
institutions: [Fudan University, Tencent PCG, ShanghaiTech University]
paper_url: "https://arxiv.org/abs/2306.14795"
project_url: "https://motion-gpt.github.io/"
github_url: "https://github.com/OpenMotionLab/MotionGPT"
video_url: null
open_source: {code: full, training_code: full, inference_code: full, model_weights: full, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, motion tokens, task prompt]
outputs: [motion, text]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0024｜MotionGPT：将人体动作视为一种外语

*MotionGPT: Human Motion as a Foreign Language*

[论文](https://arxiv.org/abs/2306.14795) · [项目页](https://motion-gpt.github.io/) · [官方代码](https://github.com/OpenMotionLab/MotionGPT)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Biao Jiang、Xin Chen、Wen Liu、Jingyi Yu、Gang Yu、Tao Chen
>
> **机构**：Fudan University、Tencent PCG、ShanghaiTech University
>
> **论文时间**：2023-06-26
>
> **期刊 / 会议**：NeurIPS 2023
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **Transformer** · **自回归** · **文本** · **动作编辑** · **人体动作**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 将连续三维动作经 VQ-VAE 转成离散“动作词”，与文本 token 一起交给 T5 式语言模型建模。
- 用混合 motion–language 预训练与提示式问答微调，统一文本生动作、动作描述、预测和插值等任务。
- 把自然语言设为任务和输出接口，使动作理解与生成能在同一序列到序列框架中互相促进。

## 研究问题

传统动作网络按任务设计头部，难复用语言模型的多任务能力。MotionGPT 的关键假设是离散动作 token 可被当作“外语”；挑战是 tokenizer 是否保留细节，以及语言模型的离散正确性如何转化为连续运动质量。

## 原论文重点图

![MotionGPT 总体架构](figures/key-figure.png)

**图 1：MotionGPT 的动作词汇与多任务框架（原论文 Figure 1 所在页）。** 动作 tokenizer 负责连续—离散转换，T5 接收由任务提示、文本和动作 token 组成的序列，再输出目标模态；同一骨干通过提示区分生成、描述、预测和插值。

## 研究方法详细解读

MotionGPT 的核心是把人体动作当作一种可由语言模型读写的“外语”。连续动作先经 VQ-VAE 变成有限 Motion Token，再与文本子词一起放进 T5 的输入/输出序列；动作生成、描述、预测、补全和问答都改写为同一种指令到序列问题，而不是为每个任务增加专用网络头。

### 1. 总体定位：动作为什么要进入语言模型词表

动作是连续高维信号，语言是离散符号，直接让 LLM 回归关节值既难优化也无法利用成熟的序列建模能力。传统 text-to-motion 只会单向生成，不能同时理解动作或执行多轮任务。MotionGPT 用离散动作词表搭桥，使 T5 可以像翻译语言一样在文本和动作 token 之间转换；代价是动作质量受 tokenizer 码本和固定表示上限约束。

### 2. 整体训练流程：tokenizer、预训练、指令微调

1. 在连续人体动作上训练 VQ-VAE，encoder 量化为 Motion Token，decoder 负责还原姿态序列。
2. 将动作 token、模态边界符与 T5 文本词表合并，建立统一 encoder–decoder 输入输出格式。
3. 用 motion-to-text、text-to-motion、动作补全等生成目标做 Motion–Language 预训练，学习跨模态对应与动作语法。
4. 将 15 类核心任务写成自然语言 instruction，继续监督微调同一 T5，使指令决定输出文本还是动作。
5. 推理自回归生成目标序列；若是动作码，再交给冻结 VQ decoder，还原连续人体动作。

### 3. 总体信息流：把动作任务改写成序列到序列指令

MotionGPT 首先训练 VQ-VAE，把连续人体动作变成离散 Motion Token；再将这些 token 作为 T5 词表的扩展符号，与自然语言一起输入 encoder–decoder；最后通过动作—语言预训练和指令微调，让同一模型依据提示输出文字或动作码。推理时若目标是动作，LLM 自回归生成起止标记之间的 Motion Token，冻结 VQ decoder 还原连续姿态；若目标是描述或问答，则直接由原文本词表输出。

### 动作 tokenizer 的训练与上限

一维卷积 encoder 沿时间压缩动作，向量量化选择最近码本项，decoder 上采样恢复原序列。损失由 Smooth-L1 姿态重建、速度一致性、码本 embedding 和 commitment 构成，并用 EMA/重置机制减少 dead code。训练完成后 tokenizer 冻结，动作码顺序和起止标记组成 LLM 可预测的“动作语言”。任何关节抖动、脚接触或高频信息若在此阶段丢失，后续 T5 即便预测完全正确也无法恢复。

### 词表合并与 T5 信息流

文本使用原 SentencePiece token，动作索引映射到新增 token，并用 motion start/end 等特殊符号标记边界。source 序列由自然语言指令、任务输入和部分可见动作组成，T5 encoder 做双向上下文编码；decoder 在 cross-attention 条件下因果预测 target。相同架构可表达 text→motion、motion→text、motion→motion 或 text→text，任务差异在指令模板与 source/target 模态，而不是新增任务专用网络。

### Motion–Language 预训练的两类目标

无监督部分借鉴 T5 span corruption：随机遮蔽文本或动作 token span，让模型恢复缺失片段，从大量单模态序列学习语言语法与动作时序。监督部分使用成对文本—动作，双向训练文本生动作和动作描述，使两套词表通过共享 Transformer 对齐。预训练既需要 tokenizer 固定，又要按数据量平衡文字和动作，防止大规模语言 token 把稀少动作 token 的梯度淹没。

### 指令微调与 15 类核心任务

论文把约 15 类任务写成 instruction–input–output，包括生成、描述、预测、插值、风格/长度编辑和动作问答，并为每类设计多种自然语言模板（总量超过千条）。动作预测在 source 暴露前缀、target 输出未来；插值同时给首尾 token、要求补中间；翻译则改变目标模态。训练仍是 target token 交叉熵，只有 answer 区域计损失，模板多样性用于减少模型记固定措辞。

### 推理和多轮使用

用户提示先被解析成同一模板，encoder 读取所有条件，decoder 用温度/top-k 等策略逐 token 生成到结束符。动作结果经 VQ decoder 输出连续姿态，文本结果无需动作解码；预测/插值时已知 token 只作为上下文，不是连续空间硬约束。统一接口便于串联“先描述—再编辑—再生成”，但每次解码误差与 token 序列错误会累计，模型也不等于具有环境反馈的 Agent。

### 使用边界

所谓零样本/指令能力建立在预训练任务和模板覆盖之上，不能视为对任意新动作任务的保证。输出仍是人体运动；用于人形机器人需要 FPS/骨架/根坐标重定向、动力学筛选和低层跟踪。复现应分别报告 tokenizer 重建、token 生成准确性和最终动作指标，避免将三者混成一个结果。

## 实验结果与结论

论文在文本动作、动作描述、预测和插值等任务达到当时有竞争力结果，说明离散动作可被语言模型统一处理。连续动作质量仍受 VQ 重建限制，且没有机器人动力学闭环。

## 局限与复现提醒

- 必须先验证 tokenizer 的 FPS、关节顺序、归一化与码本利用率，再评价 LLM。
- 文本指标与动作 FID 使用不同评估器，不能混为“通用智能”。
- 机器人使用需重定向、物理筛选和跟踪控制。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：官方代码/权重已核验，未运行。
- 机器人：未验证。

## 参考资料

- [arXiv](https://arxiv.org/abs/2306.14795)
- [官方代码](https://github.com/OpenMotionLab/MotionGPT)

## 更新记录

- 2026-09-04：按 ADAPT 式讲解补充连续动作进入语言模型的表示难点，并用五步流程说明 VQ 词表、跨模态预训练、指令微调和动作解码。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，解析动作词表、T5 统一建模和提示式多任务训练。
