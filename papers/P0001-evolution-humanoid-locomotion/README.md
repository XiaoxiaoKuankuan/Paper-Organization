<!--
---
id: P0001
title_en: "Evolution of Humanoid Locomotion Control"
title_zh: "人形机器人运动控制的演进"
year: 2026
date: 2026-08-19
venue: "Science Robotics, 11(117), eaed3973"
primary_category: locomotion-prior
tags:
  - humanoid
  - locomotion
  - reinforcement-learning
  - physics-guidance
  - world-model
authors:
  - Yan Gu
  - Guanya Shi
  - Fan Shi
  - I-Chia Chang
  - Yen-Jen Wang
  - Qilong Cheng
  - Zachary Olkin
  - Ivan Lopez-Sanchez
  - Yunchu Feng
  - Jian Zhang
  - Aaron D. Ames
  - Hao Su
  - Koushil Sreenath
institutions:
  - Purdue University
  - Carnegie Mellon University
  - National University of Singapore
  - University of California, Berkeley
  - New York University
  - California Institute of Technology
  - Meta Platforms Inc.
paper_url: "https://doi.org/10.1126/scirobotics.aed3973"
project_url: "https://github.com/purdue-tracelab/Humanoid-Locomotion-Survey"
github_url: "https://github.com/purdue-tracelab/Humanoid-Locomotion-Survey"
video_url: null
open_source:
  code: "no"
  training_code: "no"
  inference_code: "no"
  model_weights: "no"
  dataset: "no"
  robot_deployment: "no"
open_source_checked: 2026-09-03
robots: []
inputs: []
outputs: []
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0001/Evolution_of_Humanoid_Locomotion_Control_20260819.pdf"
  - "local_archive/P0001/Evolution_of_Humanoid_Locomotion_Control_中英对照全文翻译.pdf"
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0001｜人形机器人运动控制的演进

*Evolution of Humanoid Locomotion Control*

[论文](https://doi.org/10.1126/scirobotics.aed3973) · [配套资料](https://github.com/purdue-tracelab/Humanoid-Locomotion-Survey) · [中英对照全文翻译](attachments/中英对照全文翻译.pdf)

## 1. 基本信息

- 类型：综述论文，而非新控制器或可复现代码项目。
- 发表：Science Robotics 11(117)，文章号 eaed3973，2026-08-19。
- DOI：[10.1126/scirobotics.aed3973](https://doi.org/10.1126/scirobotics.aed3973)
- 作者单位覆盖 Purdue、CMU、NUS、UC Berkeley、NYU、Caltech 与 Meta。

### 开源状态

论文没有对应训练代码、模型权重或数据集；GitHub 链接是综述配套资料入口，不应标记为“控制代码已开源”。

## 本文贡献

- 建立“经典控制—学习控制—生成式控制”的统一历史坐标，而不是把强化学习视为与模型控制割裂的替代品。
- 用物理建模、受约束决策与不确定性适应三条主线解释各代方法共同解决的问题与不同取舍。
- 将未来方向归纳为物理引导生成、多模态感知、任务级智能和安全部署，并指出从展示性敏捷动作走向开放世界仍缺可靠性评价。

## 3. 研究问题

综述试图回答：过去用于稳定行走的解析控制、近年用于敏捷全身运动的强化学习，以及正在兴起的生成模型如何构成一条连续技术路线，而不是彼此割裂的范式。

## 原论文重点图

![人形运动控制范式演进](figures/control-evolution.png)

**图 1：数十年人形运动控制范式演进（原论文 Figure 1）。** 横向从经典控制、学习式控制走向生成式智能；纵向同时比较控制器所利用的模型/数据、工具来源和任务能力。重点不是简单“新方法淘汰旧方法”，而是计算与数据规模扩大后，控制器能处理的动力学丰富度和任务开放性同步上升。

![控制范式与计算层级](figures/control-paradigms.png)

**图 2：控制范式的统一视角（原论文 Figure 3）。** 论文用模型—数据复杂度和在线—离线计算两个维度组织经典反馈、MPC、强化学习与混合方法。这张图解释了为什么现代系统仍常保留低层 PD/WBC：学习策略把大量优化离线编码进网络，但在线稳定执行仍需要快速反馈层。

## 研究方法详细解读

### 范式划分依据

- 模型驱动阶段强调可解释动力学、轨迹优化和稳定性保证，但对复杂接触、模型误差和大技能库扩展困难。
- 强化学习阶段借助并行仿真、动作模仿和域随机化获得敏捷性与鲁棒性，但依赖奖励、数据和安全验证。
- 生成式阶段开始把文本、视觉、动作历史和环境上下文统一为条件，生成未来动作或控制目标。
- 三条核心原则不是简单按年代替换：物理模型仍约束学习系统，约束决策仍限制生成结果，不确定性适应决定真实世界鲁棒性。

### 输入、输出与动作接口

本论文是综述，没有单一模型输入输出。比较不同方法时，应分别记录状态估计、参考动作、任务命令、环境感知、输出力矩/关节目标和控制频率，不能把它们压成同一接口。

### 训练、优化与部署层级

不适用单一实现。论文讨论的技术谱系涵盖解析 WBC/MPC、模仿与强化学习策略、运动先验、生成模型和预测式控制。

## 实验结果与结论

- 人形运动控制的目标已从“保持稳定”扩展到敏捷、鲁棒、可表达并能与环境交互。
- 纯模型或纯数据路线都不足以覆盖开放世界，未来系统需要把优化、学习和预测推理结合起来。
- 安全、可访问性和接近人类水平能力仍是开放问题，展示视频不能替代严格评估。

## 局限与复现提醒

优点是建立跨经典控制、强化学习和生成模型的统一坐标系；局限是综述跨度很大，不能替代对具体控制器的接口、数据、奖励和实机协议审计。

### 对个人研究的价值

适合作为整个知识库的路线图：GENMO/OMG 等位于生成式“上层大脑”，SONIC/跟踪器位于反应式执行层，物理反馈与约束机制负责连接生成和真实执行。

## 阅读与复现状态

- 阅读：已深读原文与中英对照材料，并完成路线梳理。
- 延伸整理：持续补齐文中代表性系统档案。
- 复现：综述本身无单一代码系统，不适用 Demo/训练复现。


## 参考资料

- [Science Robotics / DOI](https://doi.org/10.1126/scirobotics.aed3973)
- [PubMed 书目信息](https://pubmed.ncbi.nlm.nih.gov/42616832/)
- [配套 GitHub](https://github.com/purdue-tracelab/Humanoid-Locomotion-Survey)

## 更新记录

- 2026-09-03：创建精读档案，登记原文与中英对照材料；开源状态按综述属性记录。
- 2026-09-03：隐藏元数据，纳入翻译附件与原论文 Figure 1/3，重写贡献和方法解读结构。
