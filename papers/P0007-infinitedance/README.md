<!--
---
id: P0007
title_en: "InfiniteDance: Scalable 3D Dance Generation Towards in-the-wild Generalization"
title_zh: "InfiniteDance：面向野外泛化的可扩展三维舞蹈生成"
year: 2026
date: 2026-03-10
venue: "ECCV 2026"
primary_category: motion-generation
tags:
  - motion-generation
  - music
  - human-motion
  - diffusion
  - transformer
  - motion-capture
  - large-scale-data
authors:
  - Ronghui Li
  - Zhongyuan Hu
  - Li Siyao
  - Youliang Zhang
  - Haozhe Xie
  - Mingyuan Zhang
  - Jie Guo
  - Xiu Li
  - Ziwei Liu
institutions:
  - Tsinghua University
  - Peng Cheng Laboratory
  - S-Lab, Nanyang Technological University
paper_url: "https://arxiv.org/abs/2603.13375"
project_url: "https://infinitedance.github.io/"
github_url: "https://github.com/MotrixLab/InfiniteDance"
video_url: null
open_source:
  code: full
  training_code: full
  inference_code: full
  model_weights: full
  dataset: full
  robot_deployment: "no"
open_source_checked: 2026-09-03
robots: []
inputs:
  - music
  - retrieved dance references
outputs:
  - 3D human dance motion
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0007/InfiniteDance： Scalable 3D Dance Generation.pdf"
  - "local_archive/P0007/InfiniteDance_full_translation_explanation.docx"
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0007｜InfiniteDance：面向野外泛化的可扩展三维舞蹈生成

*InfiniteDance: Scalable 3D Dance Generation Towards in-the-wild Generalization*

[论文](https://arxiv.org/abs/2603.13375) · [项目页](https://infinitedance.github.io/) · [官方代码](https://github.com/MotrixLab/InfiniteDance) · [全文翻译与方法详解](attachments/全文翻译与方法详解.docx)

## 1. 基本信息

- 论文：[arXiv:2603.13375](https://arxiv.org/abs/2603.13375)，ECCV 2026。
- 项目页：[InfiniteDance](https://infinitedance.github.io/)
- 代码与资源：[MotrixLab/InfiniteDance](https://github.com/MotrixLab/InfiniteDance)，提供训练/推理代码、数据与权重下载。

## 本文贡献

- 构建 100.69 小时野外三维舞蹈数据管线，把单目恢复、物理模仿、足部修复和人工筛选串联起来。
- 用 RVQ-VAE 将长动作压缩成层级离散 token，再以 ChoreoLLaMA 自回归生成，扩大序列长度与动作词汇容量。
- 提出基于音乐检索的 RAG 与 Cadence-MoE，使生成同时利用外部编舞记忆和快慢节奏专家，提高长时节奏一致性与未见音乐泛化。

## 3. 研究问题

现有音乐舞蹈数据规模小、舞种窄；单目重建存在脚滑、漂浮和穿透；传统生成器面对野外音乐时易产生无结构动作。论文认为数据规模、动作物理质量和音乐条件建模必须共同解决。

## 原论文重点图

![FRDM 足部修复](figures/frdm.png)

**图 1：FRDM 足部修复与数据构建（原论文方法图）。** 单目恢复的 SMPL-X 先经物理模仿获得较稳定轨迹，FRDM 再依据足接触和根运动修复脚滑；它在接触约束下联动调整足部与全身，不是简单时域平滑。

![ChoreoLLaMA](figures/choreollama.png)

**图 2：ChoreoLLaMA 长时舞蹈生成（原论文方法图）。** 音乐由 MuQ 编码，舞蹈由 RVQ-VAE 转为多层 token，自回归主干预测后续 token，以离散压缩降低长序列建模成本。

![Cadence-MoE](figures/cadence-moe.png)

**图 3：检索增强与 Cadence-MoE（原论文方法图）。** RAG 从动作库取回与当前音乐相近的舞蹈片段，节奏专家按音乐结构路由；前者提供外部动作记忆，后者提供条件专门化。

## 研究方法详细解读

### 数据恢复与动作修复

管线先从单人视频估计 SMPL-X 身体、手和脸，再用物理模仿减少整体非物理伪影。FRDM 在更线性的关节位置/速度/旋转空间中学习足部恢复，并用接触与几何约束抑制脚滑，同时尽量保留原舞蹈表现力。最终数据覆盖 6 大类、30 个细粒度舞种，含音乐、手部与面部信息。

### 离散动作建模与条件训练

MuQ 提取音乐表示，RVQ-VAE 把舞蹈量化为多层 token。跨模态 RAG 检索与输入音乐相近的参考舞蹈作为提示；Cadence-MoE 让专家适配快慢节奏；LLaMA3.2-1B 主干自回归生成舞蹈 token。训练与评估同时使用 InfiniteDance 和公开舞蹈数据。

### 长时推理与机器人适配

输入野外音乐后，系统检索参考、路由节奏专家并生成 3D 人体舞蹈。它不是机器人控制器；若用于人形机器人，仍需重定向、物理筛选和低层跟踪。

## 实验结果与结论

论文报告在跨数据集与 OOD 音乐上优于现有方法，长于 30 秒的生成没有明显指标崩塌；检索距离分析显示输出不是简单复制参考。具体数值应按原论文相同数据集和评估器比较，不能跨协议直接横比。

## 局限与复现提醒

- 优点：完整覆盖“数据采集—物理修复—可扩展生成”；同时关注手脸与野外音乐；资源开放度高。
- 局限：单目恢复与自动筛选仍会传播误差；RAG 依赖检索库覆盖；人体舞蹈指标不证明机器人可执行性；权重与数据体积大。

### 对个人研究的价值

适合作为音乐到人体舞蹈的上游数据/模型来源，并为 GENMO/OMG 的音乐分支提供对比。接机器人时必须额外记录 SMPL-X→robot 表征、FPS 重采样、接触重算和跟踪验证。

## 阅读与复现状态

- 阅读：已深读原文和完整译解，核对核心模块与数据口径。
- 资源：已核验代码、权重和数据入口。
- 运行：尚未下载全量资源或执行生成 Demo。
- 机器人：尚未进行重定向和物理执行验证。


## 参考资料

- [论文](https://arxiv.org/abs/2603.13375)
- [项目页](https://infinitedance.github.io/)
- [官方代码](https://github.com/MotrixLab/InfiniteDance)

## 更新记录

- 2026-09-03：创建精读档案；登记公开代码、数据和权重，明确人体生成与机器人执行的边界。
- 2026-09-03：纳入译解附件及 FRDM、ChoreoLLaMA、Cadence-MoE 原图，扩展长时生成解读。
