<!--
---
id: P0034
title_en: "The Language of Motion: Unifying Verbal and Non-verbal Language of 3D Human Motion"
title_zh: "动作的语言：统一三维人体动作的言语与非言语表达"
year: 2024
date: 2024-12-13
venue: "CVPR 2025"
primary_category: motion-generation
tags: [motion-generation, multimodal, transformer, text, speech, human-motion, motion-editing]
authors: [Changan Chen, Juze Zhang, Shrinidhi K. Lakshmikanth, Yusu Fang, Ruizhi Shao, Gordon Wetzstein, Li Fei-Fei, Ehsan Adeli]
institutions: [Stanford University]
paper_url: "https://arxiv.org/abs/2412.10523"
project_url: "https://languageofmotion.github.io/"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, speech, motion, modality combinations]
outputs: [motion, text, emotion labels]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0034｜动作的语言：统一三维人体动作的言语与非言语表达

*The Language of Motion: Unifying Verbal and Non-verbal Language of 3D Human Motion*

[论文](https://arxiv.org/abs/2412.10523) · [项目页](https://languageofmotion.github.io/)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Changan Chen、Juze Zhang、Shrinidhi K. Lakshmikanth、Yusu Fang、Ruizhi Shao、Gordon Wetzstein、Li Fei-Fei、Ehsan Adeli
>
> **机构**：Stanford University
>
> **论文时间**：2024-12-13
>
> **期刊 / 会议**：CVPR 2025
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **Transformer** · **文本** · **语音** · **人体动作** · **动作编辑**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 用多模态语言模型统一文本、语音和动作的任意输入组合，既生成动作，也执行描述、情绪理解和可编辑手势等任务。
- 为身体、手、脸或上下身设计组合式动作 VQ 表示，避免整个人体由单一码本粗粒度压缩。
- 提出生成式预训练，利用无需严格三元配对的单模态/双模态数据，并在较少监督下提高 co-speech gesture 质量。

## 研究问题

现实交流同时包含说话内容、声学韵律、手势、脸部和身体姿态。专用模型只处理一种输入/输出，不能利用不完整多模态数据。本文将言语和非言语信号都视作可生成语言，并通过组合 tokenizer 保留身体层级。

## 原论文重点图

![动作语言任务总览](figures/key-figure.png)

**图 1：从语音/文本/动作到手势生成、编辑、文本动作和情绪理解（原论文 Figure 1 所在页）。** 各任务共用多模态序列模型；差别由输入可见模态和目标模态定义。

## 研究方法详细解读

The Language of Motion 的核心不是把语音转文字后再生成动作，而是把语言理解扩展到“说了什么”和“怎样说”两层：文本承载言语语义，原始语音承载节奏、情绪与非言语表达。模型把脸、手、上身和下身分别量化，与 HuBERT 语音 token、文本 token 放入同一生成词表，再用指令决定跨模态映射。

### 1. 总体定位：为什么共语动作不能只依赖文字

相同句子在不同重音、语速和情绪下对应不同手势与面部表情；只用文本会丢失这些线索。反过来，音频对局部节奏强，却未必完整表达动作任务。全身各部位的运动尺度也不同，统一 tokenizer 容易牺牲脸手细节。论文因此同时拆分身体通道和语言通道，再通过生成式预训练学习它们之间可组合的关系。

### 2. 整体训练流程：分部位词表到指令生成

1. 将 SMPL-X 全身拆为脸、双手、上身和下身等通路，分别训练 VQ-VAE 保留部位细节。
2. 用 HuBERT 量化语音、沿用 Flan-T5 文本词表，再加入动作 token 和模态边界符形成联合词表。
3. 通过身体部位互译、时间补全等目标学习动作内部的空间与时序关系。
4. 通过音频↔文本等生成任务预训练言语内容与非言语声学线索的对齐。
5. 将 audio/text/emotion→motion 及理解任务改写为大量自然语言指令，对 Flan-T5 做后训练。
6. 针对 co-speech 数据进一步适配；推理按指令生成各部位 token，再分别解码并同步成全身动作。

### 3. 总体信息流：全身分部量化、生成式对齐、指令后训练

The Language of Motion 先把 SMPL-X 全身拆为脸、手、上身和下身四路，分别训练 VQ-VAE；语音由 HuBERT 量化，文本沿用 Flan-T5 词表，所有码与模态边界符组成联合词表。预训练用身体部位互译、时间补全和音频—文本翻译学习无/弱配对先验；后训练再把 audio/text/emotion→motion 等写成千余种指令，用 220M Flan-T5-Base 自回归输出目标模态 token。动作回复由四个 decoder 按时间重组为全身 SMPL-X。

### 四部位动作表示与 tokenizer

SMPL-X 被分为下身 9 关节 54D、上身 13 关节 78D、双手 30 关节 180D，以及头/脸 1 个关节加 100 expression 共 106D，旋转使用 6D。每路 VQ-VAE 以四层 TCN 编码、最近邻量化、decoder 重建；姿态使用 geodesic 或 L2，另在速度、加速度及 SMPL-X mesh 的位置/速度/加速度空间施加损失，再加 commitment。分部码本避免高能量躯干压制手脸，但输出时必须保持四流帧级同步。

### 语音、文本和联合词表

16 kHz 语音经 HuBERT 每 320 个采样下采样一次，约 50 token/s；文本由 T5 的 32k SentencePiece 词表表示。音频、脸、手、上身、下身各有独立 token 范围和开始/结束符，例如某上身码格式化为 `<upper 8>`。所有输入最终成为长度不超过 512 的 token 序列，T5 encoder 双向读取条件，decoder 因果产生固定格式目标，防止不同模态索引被误解释。

### 身体空间与时间的生成式预训练

空间任务随机选择一些身体部位作为条件、预测另一组部位，例如 upper→lower 或 face+upper→hands，迫使模型学习姿态协同；时间任务随机遮蔽动作帧，让模型由可见部分恢复缺失序列，学习运动演化。监督来自同一条动作内部，不要求额外文字/语音配对，因此可利用约 60 小时动作数据。四路输出的交叉熵在统一 LLM 中联合更新，建立“动作语法”。

### 音频—文本对齐预训练

另一条自监督/配对任务在约 1,000 小时语音文本数据上做 audio→text 和 text→audio 式翻译，把 HuBERT token 映射到语言模型已经擅长的语义空间。它不需要音频对应动作，却能让下游 speech-to-gesture 利用语义和节奏线索。消融中的 A2T、空间、时间和整体 motion 预训练分别验证这些目标，但语音文本对齐仍不提供说话人身体风格真值。

### 指令后训练与 co-speech 适配

预训练完成后，用真正配对的 speech-motion、text-motion、emotion-motion 等任务微调。每类任务编写数十个自然语言模板，总计超过千种提示；condition 用模态占位和 token 序列表示，answer 是相应文字或四部位动作码，优化 target 下一 token NLL。论文在 BEATv2 speaker-2 等协议中使用既定动作 tokenizer 进行公平比较；预训练权重使少量配对数据也能适配新说话人。

### 推理与适用边界

输入指令和语音/文本后，T5 逐 token 生成四部位动作序列，分别解码并组合为 SMPL-X 全身；也可反向输出文字。固定 512 长度限制长序列，部位码之间的异步错误可能产生身体不协调。模型输出人体网格/动作，不含机器人动力学；用于机器人需统一手部自由度、FPS、根运动和低层控制，且预训练的语言/动作相关性不能代替物理筛选。

## 实验结果与结论

论文在 co-speech gesture 上取得强结果，并展示可编辑手势、动作情绪理解和文本动作。核心价值是统一人类交流模态；机器人控制仍缺动力学与实时闭环。

## 局限与复现提醒

- 需核对部位 tokenizer 的 FPS、同步策略和面手缺失处理。
- 情绪等标签具有主观性，自动指标不等同于人类交流效果。
- 机器人应用需压缩延迟并增加重定向/跟踪。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 资源：项目页已核验，完整代码/权重状态待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2412.10523)
- [项目页](https://languageofmotion.github.io/)

## 更新记录

- 2026-09-04：按 ADAPT 式讲解补充言语内容与非言语表达的区别，并用六步流程串起分部位 VQ、HuBERT/文本词表、生成式预训练、指令后训练和共语适配。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理组合式动作 token、统一多模态任务与生成式预训练。
