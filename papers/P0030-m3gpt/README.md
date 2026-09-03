<!--
---
id: P0030
title_en: "M3GPT: An Advanced Multimodal, Multitask Framework for Motion Comprehension and Generation"
title_zh: "M³GPT：用于动作理解与生成的高级多模态多任务框架"
year: 2024
date: 2024-05-25
venue: "NeurIPS 2024"
primary_category: motion-generation
tags: [motion-generation, multimodal, autoregressive, transformer, text, music, human-motion]
authors: [Mingshuang Luo, Ruibing Hou, Zhuo Li, Hong Chang, Zimo Liu, Yaowei Wang, Shiguang Shan]
institutions: [Institute of Computing Technology CAS, Peng Cheng Laboratory, University of Chinese Academy of Sciences, WeChat Tencent, Harbin Institute of Technology Shenzhen]
paper_url: "https://arxiv.org/abs/2405.16273"
project_url: "https://luomingshuang.github.io/M3GPT/"
github_url: "https://github.com/luomingshuang/M3GPT"
video_url: null
open_source: {code: full, training_code: full, inference_code: full, model_weights: partial, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, motion]
outputs: [text, music, motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0030｜M³GPT：用于动作理解与生成的高级多模态多任务框架

*M³GPT: An Advanced Multimodal, Multitask Framework for Motion Comprehension and Generation*

[论文](https://arxiv.org/abs/2405.16273) · [项目页](https://luomingshuang.github.io/M3GPT/) · [官方代码](https://github.com/luomingshuang/M3GPT)

## 本文贡献

- 将文本、音乐和动作分别离散化并纳入统一词表，用同一自回归模型完成跨模态理解与生成。
- 除离散 token 交叉熵外，联合训练动作 detokenizer，让连续动作重建误差反向传播到 LLM，缓解离散量化丢失细节。
- 以文本作为音乐和舞蹈之间的语义桥，增加 music-to-text、text-to-dance 等辅助任务，促进难学的 music-to-dance 对齐。

## 研究问题

LLM 对文本熟悉，却不了解音乐/动作 token 的结构；直接把三者串联容易只学表层共现。M³GPT 用共享词表建立形式统一，再用连续动作损失和文本桥接任务建立内容层对齐。

## 原论文重点图

![M3GPT 多模态多任务框架](figures/key-figure.png)

**图 1：M³GPT 三层框架（原论文 Figure 1 所在页）。** 多模态 tokenizer 产生离散序列，核心 LLM 做 next-token 预测，动作 detokenizer 同时返回连续空间误差；任务包括文本↔动作、音乐↔舞蹈、描述、预测和插值。

## 研究方法详细解读

### 多模态 tokenizer

动作和音乐使用各自 VQ 模型，文本沿用语言词表；所有索引通过类型/范围映射进共享 embedding。动作与舞蹈共享 tokenizer 以促进迁移，音乐保留独立声学码本。

### 离散—连续联合优化

LLM 先预测动作 token，再经可微近似/对应 embedding 输入 decoder 重建连续动作；连续损失对姿态细节提供更直接梯度。实现必须防止 decoder 绕开离散语义或因 teacher forcing 造成训练—推理不一致。

### 文本桥接多任务

music-to-text 与 text-to-dance 把音乐和动作分别对齐到 LLM 擅长的语义空间，再与 music-to-dance 联合训练。instruction tuning 用任务模板区分输出模态，并支持 zero-shot 组合。

## 实验结果与结论

论文在 Motion-X、AIST++、FineDance 等数据上评估文本/音乐/动作双向任务，并报告零样本组合能力。结论是连续动作反馈与文本桥接可改善统一建模，但仍受 tokenizer 与数据对齐质量限制。

## 局限与复现提醒

- 动作、音乐、文本 tokenizer 的时间倍率和特殊 token 必须严格一致。
- 多任务采样比例会显著影响稀有任务；zero-shot 需区别于模板近似训练分布。
- 不含机器人物理执行。

## 阅读与复现状态

- 阅读：已阅读论文、NeurIPS 页面和飞书整理。
- 资源：官方训练仓库已核验，未运行。
- 机器人：未适配。

## 参考资料

- [NeurIPS 论文页](https://proceedings.neurips.cc/paper_files/paper/2024/hash/316648eb8b4ffb6010f531b07848c300-Abstract-Conference.html)
- [arXiv](https://arxiv.org/abs/2405.16273)
- [官方代码](https://github.com/luomingshuang/M3GPT)

## 更新记录

- 2026-09-03：新建条目，解析三模态词表、连续动作反馈与文本桥接任务。
