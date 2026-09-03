<!--
---
id: P0027
title_en: "MotionChain: Conversational Motion Controllers via Multimodal Prompts"
title_zh: "MotionChain：通过多模态提示实现对话式动作控制"
year: 2024
date: 2024-04-02
venue: "ECCV 2024"
primary_category: motion-generation
tags: [motion-generation, multimodal, transformer, text, image, motion-editing, autoregressive]
authors: [Biao Jiang, Xin Chen, Chi Zhang, Fukun Yin, Zhuoyuan Li, Gang Yu, Jiayuan Fan]
institutions: [Fudan University, Tencent]
paper_url: "https://arxiv.org/abs/2404.01700"
project_url: null
github_url: "https://github.com/OpenMotionLab/MotionChain"
video_url: null
open_source: {code: full, training_code: full, inference_code: full, model_weights: partial, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, image, motion, multi-turn history]
outputs: [continuous human motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0027｜MotionChain：通过多模态提示实现对话式动作控制

*MotionChain: Conversational Motion Controllers via Multimodal Prompts*

[论文](https://arxiv.org/abs/2404.01700) · [官方代码](https://github.com/OpenMotionLab/MotionChain)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Biao Jiang、Xin Chen、Chi Zhang、Fukun Yin、Zhuoyuan Li、Gang Yu、Jiayuan Fan
>
> **机构**：Fudan University、Tencent
>
> **论文时间**：2024-04-02
>
> **期刊 / 会议**：ECCV 2024
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **Transformer** · **文本** · **图像** · **动作编辑** · **自回归**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 将文本、图像和动作转为多模态 token，引入 Vision-Motion-aware Language Model 处理多轮动作生成与编辑。
- 利用语言、视觉—语言和视觉—动作数据联合训练，使用户可逐轮追加、修改或引用既有动作上下文。
- 以对话历史维持长任务语义，并将多个局部动作指令串成连续长动作控制链。

## 研究问题

单轮 text-to-motion 很难表达“保持上一步风格，再抬左手、最后坐下”这类增量编辑。MotionChain 将历史、图像和动作统一进对话上下文；难点是不同 tokenizer 的时间/语义尺度与段间连续性。

## 原论文重点图

![MotionChain 多轮动作控制](figures/key-figure.png)

**图 1：多模态 token 与对话式动作控制（原论文 Figure 1 所在页）。** 文本/图像/动作分别编码后进入共享语言模型，输出动作 token；下一轮继续读取已有上下文，使动作可以被引用、扩展和修改。

## 研究方法详细解读

### 总体流程：把图像、文字和动作放进多轮对话

MotionChain 先训练 VQ 动作 tokenizer；再将动作词表与 SentencePiece 文本词表合并，并把 CLIP 图像/视频特征投影为语言 token embedding；随后进行单轮跨模态预训练，最后在最多 10 轮的动作对话数据上指令微调。每轮 source 可以混合图像、文本和历史动作，answer 可以是文字或动作 token；模型只对 answer 区域计算因果语言损失，并以结束符决定何时停止。生成动作经 VQ decoder 恢复，所有历史问答保留为下一轮上下文。

### 对话数据如何从动作库构造

基础集合继承 MotionGPT 的 14 类生成/理解任务，再用 HumanML3D caption 让 ChatGPT 生成动作原因、前后事件、角色和工具等 reasoning 问答。TMR 将动作对按相似度分组：中等相似对用于生成“如何把动作 A 改成 B”的编辑指令，高相似对由人工设计长度编辑；单轮任务再随机串成生成、翻译、推理、编辑等多轮链。数据设计显式教模型引用先前动作，而不是期待普通语言预训练自动学会运动编辑。

### 动作与视觉 tokenizer

动作 encoder 用 1D convolution 将 `M` 帧压到 `L=M/l` 个 latent，最近邻选择码本项，decoder 恢复连续动作；重建、embedding、commitment 三项训练完成后冻结。图像由冻结 CLIP visual encoder 提特征，再由可学习线性层映射到 LLM token space；视频逐帧编码、加入时间位置并由带固定查询的 Perceiver 汇总为定长视觉 token。文本沿用 LLM 词表，三种输入最终拥有相同 embedding 宽度但不同序列长度。

### 统一词表和因果目标

文本词表 `Vt` 与保持 VQ 码本顺序的动作词表 `Vm` 拼接，并加入模态边界/结束符；视觉 embedding 放在第一轮 source 前部。模型对 `[system, user source, answer, ...]` 做因果预测，只将 answer token 纳入负对数似然，避免把用户输入当目标。推理按 `p(answer_i | image, all previous sources/answers, current source, answer_<i)` 逐 token 采样，遇到结束符停止，因此文字和动作都遵循同一生成机制。

### 三阶段训练和冻结关系

Stage 1 只训练动作 tokenizer，确定固定动作词表。Stage 2 冻结 tokenizer 和 CLIP visual encoder，联合更新视觉投影与语言模型，在 text→motion、motion→text、image→motion 三个单轮翻译任务上建立跨模态对齐。Stage 3 使用指令化、多任务、多轮数据继续微调，使模型学会引用上下文、推理和编辑。若跳过 Stage 2，复杂对话信号不足以从零建立动作/视觉对应；若 tokenizer 在后期漂移，历史 motion token 的语义会失效。

### 多轮动作组合的连续性处理

论文比较独立解码、只以前一段末尾为条件和 token-joint 三种组合。MotionChain 将过去动作 token 与当前生成 token 拼接后一次送入 motion decoder，联合解码成整段连续动作；相比每段独立解码，这让卷积 decoder 在边界两侧共同重建，减少姿态跳变。它仍只处理表示层连续，根世界位置、速度、接触和物理可执行性若超出 tokenizer 学到的分布，仍可能随轮次累积。

### 推理与边界

实际流程可从图像提取动作、要求文字解释、再按后续指令编辑并继续生成；所有轮次受 LLM 上下文长度限制。所谓多轮“记忆”是 token 上下文，不是外部场景状态或物理反馈。模型输出人体运动，没有机器人控制器；用于机器人时需在联合解码后做重定向和闭环跟踪，并验证多段根轨迹与接触。

## 实验结果与结论

论文在对话式动作生成和多模态控制上报告强结果，并展示更自然的逐步交互。主要指标仍在人体动作域，未验证真实环境规划或机器人闭环。

## 局限与复现提醒

- 多轮历史迅速消耗上下文，动作 token 压缩率和截断策略决定可用长度。
- 图像理解错误会通过语言模型传入动作；段间连续性需单独评测。
- 机器人应用需增加重定向、接触与低层控制。

## 阅读与复现状态

- 阅读：已阅读论文与飞书整理。
- 资源：官方代码入口已核验，未运行。
- 机器人：未验证。

## 参考资料

- [arXiv](https://arxiv.org/abs/2404.01700)
- [官方代码](https://github.com/OpenMotionLab/MotionChain)

## 更新记录

- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理多模态 token、对话上下文与连续动作拼接问题。
