<!--
---
id: P0026
title_en: "AvatarGPT: All-in-One Framework for Motion Understanding, Planning, Generation and Beyond"
title_zh: "AvatarGPT：动作理解、规划、生成及更多任务的一体化框架"
year: 2023
date: 2023-11-28
venue: "CVPR 2024"
primary_category: world-model-vla-agent
tags: [motion-generation, autoregressive, transformer, text, motion-editing, human-motion]
authors: [Zixiang Zhou, Yu Wan, Baoyuan Wang]
institutions: [Xiaobing.AI]
paper_url: "https://arxiv.org/abs/2311.16468"
project_url: null
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: unknown, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [instructions, text, motion tokens]
outputs: [motion, captions, task plans]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0026｜AvatarGPT：动作理解、规划、生成及更多任务的一体化框架

*AvatarGPT: All-in-One Framework for Motion Understanding, Planning, Generation and Beyond*

[论文](https://arxiv.org/abs/2311.16468)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Zixiang Zhou、Yu Wan、Baoyuan Wang
>
> **机构**：Xiaobing.AI
>
> **论文时间**：2023-11-28
>
> **期刊 / 会议**：CVPR 2024
>
> **主分类**：世界模型 / VLA / Agent
>
> **重点标签**：**动作生成** · **自回归** · **Transformer** · **文本** · **动作编辑** · **人体动作**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 将动作理解、文本生动作、动作补全与高层任务规划统一成共享 LLM 上的指令任务。
- 把人体动作量化为扩展词表 token，用自然语言作为高低层任务之间的公共接口，形成“规划—生成—描述”的闭环。
- 从野外视频自动生成动作—语言数据，缓解高层规划描述与低层动作对缺乏的问题，并通过迭代任务遍历生成长动作。

## 研究问题

动作系统通常把规划、生成、描述拆开，接口是不可读 latent；这使多轮修正和长任务组合困难。AvatarGPT 将动作 token 接入 LLM，但必须同时处理高层文本逻辑和低层连续动作精度之间的尺度差异。

## 原论文重点图

![AvatarGPT 一体化任务](figures/key-figure.png)

**图 1：AvatarGPT 从任务描述到步骤、动作和反馈的闭环（原论文 Figure 1 所在页）。** LLM 先把长任务拆成步骤，再为步骤产生动作 token；动作也可反向描述为文本，使多轮对话在语言上下文中保持状态。

## 研究方法详细解读

### 动作扩展词表

VQ tokenizer 把动作序列变为离散索引，并扩展 LLM embedding/output head。语言负责语义组合，tokenizer decoder 恢复连续姿态；若动作词重建较差，LLM 再强也无法恢复接触细节。

### 指令联合训练

每个任务都包装成 instruction–input–output 对，包含文本到动作、动作到文本、预测、插值与规划。联合训练让文本成为任务桥梁，但数据配比决定模型是否偏向文本问答而忽略动作生成。

### 长动作闭环

模型将高层计划拆成步骤，逐段生成并用描述/上下文连接下一段。所谓“无限长”是迭代拼接能力，不代表误差不累积；段间根位姿、速度和接触连续性仍需额外处理。

## 实验结果与结论

AvatarGPT 在多项低层动作任务取得强结果，并首次系统展示动作规划与多轮组合。高层规划主要为生成式演示，不等同于具备环境感知和物理反馈的机器人 Agent。

## 局限与复现提醒

- 动作 token 的离散误差和段间拼接漂移会随长时生成累积。
- 自动视频标注可能含语义/时序噪声；规划正确也不保证动作可执行。
- 公开代码/权重状态需进一步核验，本知识库未运行。

## 阅读与复现状态

- 阅读：已阅读论文与飞书整理。
- 资源：开源状态待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2311.16468)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，解析动作扩展词表、指令多任务和长动作闭环。
