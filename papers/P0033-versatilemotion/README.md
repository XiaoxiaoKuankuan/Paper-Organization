<!--
---
id: P0033
title_en: "VersatileMotion: A Unified Framework for Motion Synthesis and Comprehension"
title_zh: "VersatileMotion（原 MotionLLaMA）：动作合成与理解统一框架"
year: 2024
date: 2024-11-26
venue: "ACM Transactions on Graphics, 2026"
primary_category: motion-generation
tags: [motion-generation, multimodal, transformer, flow-matching, autoregressive, smplx, large-scale-data]
authors: [Zeyu Ling, Bo Han, Shiyang Li, Jikang Cheng, Hongdeng Shen, Changqing Zou]
institutions: [Zhejiang University, ByteDance, University of Chinese Academy of Sciences, Zhejiang Lab]
paper_url: "https://arxiv.org/abs/2411.17335"
project_url: null
github_url: "https://github.com/ZeyuLing/MotionLLaMA"
video_url: null
open_source: {code: full, training_code: full, inference_code: full, model_weights: partial, dataset: full, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, speech, motion, interaction motion]
outputs: [motion, captions, multimodal comprehension]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0033｜VersatileMotion（原 MotionLLaMA）：动作合成与理解统一框架

*VersatileMotion: A Unified Framework for Motion Synthesis and Comprehension*

[论文](https://arxiv.org/abs/2411.17335) · [官方代码（原 MotionLLaMA 名称）](https://github.com/ZeyuLing/MotionLLaMA)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Zeyu Ling、Bo Han、Shiyang Li、Jikang Cheng、Hongdeng Shen、Changqing Zou
>
> **机构**：Zhejiang University、ByteDance、University of Chinese Academy of Sciences、Zhejiang Lab
>
> **论文时间**：2024-11-26
>
> **期刊 / 会议**：ACM Transactions on Graphics, 2026
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **Transformer** · **流匹配** · **自回归** · **SMPL-X** · **大规模数据**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 提出 FlowVQ：用固定动作码承载离散语义，再以 token 条件的 flow-matching decoder 恢复连续细节，降低普通 VQ 解码的量化上限。
- 用可扩展的 decoder-only Transformer 统一文本、音乐、语音、单人/多人动作的生成与理解，并以通用预训练、通用 SFT、专项 SFT 区分广度和专项性能。
- 构建 MotionHub：596.48 小时、358,847 条单人和 19,633 条多人动作片段，并提供多粒度文字、音频与九项标准任务。

## 研究问题

动作 LLM 的瓶颈一端是跨数据集、跨人数和跨模态任务缺少统一消息/评测接口，另一端是离散 token 丢失连续细节。VersatileMotion 用 MotionHub 建任务与数据底座，以 FlowVQ 组合离散语义和连续流恢复，再由可扩展 GPT 建模任意输入/输出模态。

## 原论文重点图

![VersatileMotion 总体框架](figures/key-figure.png)

**图 1：统一动作 tokenizer、LLM 与生成/理解任务（原论文 Figure 1 所在页）。** 动作、音频和文本转为对应 token，LLM 通过指令选择任务；FlowVQ 以固定动作码提供语义条件，并由 flow-matching decoder 恢复连续动作细节。

## 研究方法详细解读

VersatileMotion 的核心是把“动作 token 要有语义”和“解码动作要高保真”拆开。FlowVQ 先用 VQ 建立可供 GPT 预测的离散语义码，再用条件 flow-matching decoder 从这些码恢复连续细节；文本、音频和动作 token 随后写成统一的 Instruction—Condition—Reply 消息，由 decoder-only Transformer 完成生成与理解任务。

### 1. 总体定位：为什么普通 VQ 会限制统一动作模型

码本过小会丢失手部、多人关系和快速变化，码本过大又让语言模型难以预测；固定 VQ decoder 还会把离散误差直接带到最终动作。VersatileMotion 用离散码承担高层语义与序列长度，用 flow decoder 建模同一码对应的连续多样性，从而让语言模型保持可管理词表，同时提升恢复质量。

### 2. 整体训练流程：FlowVQ 两阶段加统一 GPT

1. 将 MotionHub 的单人、多人和全身数据统一为含全局关系的动作表示，并整理文本/音频条件。
2. FlowVQ Stage 1 训练 VQ encoder 与码本，把连续动作压成离散语义 token。
3. FlowVQ Stage 2 固定/使用离散码作为条件，训练 flow-matching decoder 从噪声连续细化高保真动作。
4. 文本走子词 tokenizer、音频走独立 VQ，三种 token 统一写入 Instruction—Condition—Reply 对话格式。
5. decoder-only Transformer 按模态预训练、跨模态对齐和指令微调三个阶段学习动作合成与理解。
6. 推理先生成回复 token；动作回复由 FlowVQ 连续解码，文字/音频则由各自接口处理。

### 3. 总体信息流：FlowVQ 负责动作词表，GPT 负责跨模态任务

VersatileMotion 先把 MotionHub 中单人/多人全身动作训练成 FlowVQ token：VQ-VAE 产生离散语义码，flow-matching decoder 在码条件下恢复高保真连续轨迹；文本使用子词 tokenizer，音频使用另一个 VQ-VAE。三类 token 被写成统一的“Instruction—Condition—Reply”消息，decoder-only GPT 先做通用预训练，再做九类 benchmark 的 generalist SFT，最后可按单一领域做 specialist SFT。推理时 GPT 生成 reply token，动作回复由 FlowVQ 解码。

### MotionHub 数据和全局多人表示

MotionHub 统一文本、语音、音乐、单人/多人动作及 interaction metadata，并为生成与理解构造任务对。动作表示保留世界位置关系，多个 agent 各自以 Motion BOS/EOS 包裹，中间用 `AGENT_SEP`，所以 token 顺序隐式保留多人空间关系而无需固定人数输出 head。数据处理与评测必须保留同一全局坐标、agent 顺序和时间对齐，否则多人 token 的相对几何语义会被破坏。

### FlowVQ 第一阶段：离散语义编码

Motion VQ-VAE 的 encoder `E` 把连续动作压成 latent，码本 `Q` 最近邻量化为序列 `z`，普通 decoder 先按动作重建、码本和 commitment 目标训练。离散码缩短 LLM 序列并提供分类词表，但 VQ 重建容易平滑速度、手部和接触。训练完成后 encoder 与码本冻结，为后续 flow decoder 和 GPT 提供不再漂移的动作符号。

### FlowVQ 第二阶段：连续流细化

固定 `E/Q`，把干净动作按噪声日程扰动成 `x_t`；Transformer flow decoder 以 `x_t`、离散码 `z` 和时刻 `t` 为输入，经 self/cross-attention预测速度场 `v≈x-x_t`，最小化 L2 flow-matching loss。推理从噪声沿该速度场积分，在 token 所规定的宏观动作附近恢复平滑轨迹。它将离散规划效率和连续细节结合，token 错误仍会限制可恢复内容，但不必让 GPT 直接输出每帧浮点姿态。

### 统一消息与 decoder-only Transformer

文本、`<AUD_x>` 和 `<MOT_y>` 均进入同一词表，模态序列有各自 BOS/EOS。每条训练样本由短自然语言 instruction、任意组合的 condition 和 reply 构成；训练随机插入时长、风格、多 agent 等可选条件。GPT 对整条序列因果建模，但 SFT 只监督 reply，结构上比 T5 encoder–decoder 更容易扩到大参数和现有 LLM 预训练框架，也使任意模态都能成为输入或输出。

### 三阶段语言模型训练

Generalist Pretraining 从 MotionHub metadata 自动组合 text/audio/motion 的翻译、补全、无条件和多人任务，对全消息做 next-token 学习，建立统一先验；Generalist SFT 在九个标准 benchmark 的 instruction-condition→reply 上只计算回复损失，校准任务格式；Specialist SFT 再从通才 checkpoint 针对单一领域训练，以牺牲部分广度换取更高专项指标。三种 checkpoint 目标不同，复现不能把 specialist 结果写成单一通才同时达到。

### 推理与边界

模型可输出文本、音频或任意人数动作 token，FlowVQ 将动作回复细化为连续全局轨迹。自回归 reply 受上下文长度和错误累积影响，flow 只修连续性、不验证接触动力学。论文是人体多模态框架，不是机器人控制器；机器人使用需在连续输出后做骨架映射、碰撞/接触检查和跟踪，并明确 generalist/specialist checkpoint。

## 实验结果与结论

论文在补全、双人文本动作和理解任务上报告领先或有竞争力结果，MotionHub 扩展任务范围。结果支持统一 tokenizer + LLM 路线，但并未验证人体动作的机器人可执行性。

## 局限与复现提醒

- 仓库/论文存在 MotionLLaMA→VersatileMotion 更名与版本演进，需锁定 commit、配置和 checkpoint。
- FlowVQ 的平均重建好不代表手指、接触或多人相对位置无损，仍需分部位和交互指标。
- 机器人链路还需重定向、接触修正和 GMT。

## 阅读与复现状态

- 阅读：已阅读论文、版本说明与飞书整理。
- 资源：代码和 MotionHub 入口已核验，未运行。
- 机器人：未适配。

## 参考资料

- [arXiv](https://arxiv.org/abs/2411.17335)
- [官方代码](https://github.com/ZeyuLing/MotionLLaMA)

## 更新记录

- 2026-09-04：按 ADAPT 式方法导读补充离散语义与连续保真的矛盾，并用六步流程讲清 MotionHub、FlowVQ 两阶段、统一消息和 GPT 三阶段训练。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，明确 MotionLLaMA/VersatileMotion 名称演进；本次按当前论文版本将旧 HoMi 描述校正为 FlowVQ、MotionHub 与三阶段 LLM 训练。
