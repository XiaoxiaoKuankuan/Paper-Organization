<!--
---
id: P0013
title_en: "Hybrid Internal Model: Learning Agile Legged Locomotion with Simulated Robot Response"
title_zh: "混合内部模型：利用模拟机器人响应学习敏捷足式运动"
year: 2023
date: 2023-12-18
venue: "ICLR 2024"
primary_category: locomotion-prior
tags: [locomotion, reinforcement-learning, contrastive-learning, motion-prior, sim2real, biped]
authors: [Junfeng Long, Zirui Wang, Quanyi Li, Jiawei Gao, Liu Cao, Jiangmiao Pang]
institutions: [OpenRobotLab, Shanghai AI Laboratory, Zhejiang University, Tsinghua University]
paper_url: "https://arxiv.org/abs/2312.11460"
project_url: null
github_url: "https://github.com/OpenRobotLab/HIMLoco"
video_url: null
open_source: {code: full, training_code: full, inference_code: full, model_weights: unknown, dataset: "no", robot_deployment: partial}
open_source_checked: 2026-09-03
robots: [Unitree A1, Unitree Go1]
inputs: [proprioception, velocity command]
outputs: [joint position target, hybrid internal embedding]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0013｜混合内部模型：利用模拟机器人响应学习敏捷足式运动

*Hybrid Internal Model: Learning Agile Legged Locomotion with Simulated Robot Response*

[论文](https://arxiv.org/abs/2312.11460) · [官方代码](https://github.com/OpenRobotLab/HIMLoco)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Junfeng Long、Zirui Wang、Quanyi Li、Jiawei Gao、Liu Cao、Jiangmiao Pang
>
> **机构**：OpenRobotLab、Shanghai AI Laboratory、Zhejiang University、Tsinghua University
>
> **论文时间**：2023-12-18
>
> **期刊 / 会议**：ICLR 2024
>
> **主分类**：Locomotion 与运动先验
>
> **重点标签**：**运动控制** · **强化学习** · **对比学习** · **运动先验** · **Sim2Real** · **双足机器人**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 把难以直接感知的地形、摩擦和外部扰动视为未知环境动力学，用机器人短期响应反推对控制真正有用的隐变量。
- 构造“显式速度 + 隐式稳定性”的混合内部嵌入，只依赖关节编码器和 IMU，避免部署时模仿仅在仿真可得的特权地形状态。
- 以原型聚类和交换分配式对比学习改善噪声鲁棒性与样本效率，并与 PPO 交替优化，完成零样本 sim-to-real 越障。

## 研究问题

盲式运动控制既要跟踪速度，又要适应不可见地形和外力。Teacher–Student 若让学生回归特权状态，可能压缩掉对控制有用但难命名的信息；纯历史编码又缺少明确的训练目标。HIM 的假设是：环境因素会通过后继本体状态显现，因此“响应”比手工环境标签更适合作为内部模型目标。

## 原论文重点图

![HIM 总览](figures/key-figure.png)

**图 1：HIM 动机与实机能力总览（原论文 Figure 1 所在页）。** 上半部分对比特权 teacher/mimic 路线与只依赖最小传感器的 HIM；下半部分展示冲刺、楼梯、粗糙斜坡和高台等测试。图中“1 小时/RTX 4090”是论文训练配置，不应外推到不同机器人和并行环境数。

## 研究方法详细解读

HIM 的核心不是单独训练一个速度估计器，而是让短时本体历史同时回答两个问题：机器人现在实际以多快移动，以及当前地形、质量、摩擦和扰动属于哪一种“隐式动力学情形”。显式速度和隐式表示一起送入行走策略，使控制器无需在部署时读取仿真器特权参数，也能根据身体响应在线适应。

### 1. 总体定位：为什么策略需要内部模型

只看单帧关节与 IMU，很难区分“命令没跟上”究竟是斜坡、打滑、负载变化还是外力造成；直接把所有随机化参数给 actor 又无法实机使用。传统显式状态估计只预测基座速度，遗漏了无法命名但影响控制的动力学因素。HIM 因此把历史编码拆成可监督的速度分量和自监督的隐式分量，要求后者能预测后继状态所属的动力学原型，再由 PPO 学会如何使用这两类信息。

### 2. 整体训练流程：表示学习与 PPO 交替进行

1. 在随机地形、质量、摩擦和外力条件下运行当前策略，收集连续本体历史和后继状态。
2. 历史编码器读取最近 5 步，输出显式基座速度与 16 维隐式动力学表示。
3. 目标编码器处理后继状态；两路特征通过原型分配、交换预测和速度回归建立 HIO 表示目标。
4. 固定/分阶段更新表示后，将速度命令、当前本体和 HIM embedding 输入 actor，用 PPO 奖励训练运动策略。
5. 新策略访问新的状态分布，再反过来刷新表示数据；部署只运行历史编码器和 actor，不需要目标编码器、原型损失或特权随机化参数。

### 3. 总体信息流：用历史预测动力学类别，再辅助行走策略

HIM 的训练闭环是：仿真器随机化质量、摩擦、地形和外力，机器人策略产生 rollout；最近 5 步本体历史送入历史编码器，同时预测显式基座速度和 16 维隐式动力学表示；后继状态由目标编码器投到同一原型空间，构成自监督表示损失；随后冻结/固定该表示更新阶段，用速度命令、当前观测和 HIM embedding 做 PPO 控制更新。两种优化交替，使表示持续适应当前策略访问到的状态，而不是脱离控制目标做一次离线预训练。

### 策略观测、动作和物理随机化

actor 读取期望前向/横向速度与偏航速度、关节位置/速度、基座角速度、投影重力和上一动作；critic 额外看到外力和地形高度等特权信息。策略输出相对默认关节姿态的动作，经缩放后作为 PD 目标。仿真通过质量、质心、摩擦、电机强度、观测噪声和推力随机化产生不同动力学响应，地形 curriculum 在 20×10 网格上按成功程度升降难度，使历史编码器必须从真实响应而非显式参数标签推断环境变化。

### 显式速度与隐式表示如何分工

5 步历史经三层 MLP（512、256、128）汇总，头部一方面回归可解释的基座线速度，另一方面输出 16 维 latent。速度头用仿真真值监督，直接补足真实机器人难以准确测量的平面速度；隐式头不尝试逐项回归摩擦系数或载荷，而编码这些因素共同导致的状态转移模式。策略同时接收两者：速度用于命令误差，latent 告诉策略“相同动作在当前动力学下会怎样响应”。

### 原型分配与交换预测

源分支编码当前历史，目标分支编码其后继状态；两者与一组可学习原型计算相似度。Sinkhorn–Knopp 在 batch 内产生近似均衡的软分配，避免全部样本坍塌到同一个原型；SwAV 式 swapped prediction 要求当前历史预测后继状态所属原型，同时后继表征能对应当前动力学语义。相比直接回归所有下一状态数值，原型任务更关注可重复的响应类型，也降低单帧噪声和不可观测参数对监督的干扰。

### HIO 与 PPO 的交替优化

一次周期先固定控制策略，用新 rollout 更新历史/目标编码器及原型（HIO）；再固定 HIM 表示，用 PPO 的 clipped objective、价值损失和熵项更新 actor/critic。控制奖励包含速度/偏航跟踪、机身姿态、足部接触、能耗和动作平滑等，HIM 本身不替代这些任务信号。随着策略改善，访问状态发生变化，下一轮 HIO 会在新分布上重新组织原型，这正是交替训练优于一次性表征学习的原因。

### 推理与实机边界

部署只保留历史编码器和 actor：滚动缓存 5 步本体观测，估计速度/latent，与用户命令共同输出关节目标；目标编码器、Sinkhorn、原型分配和特权 critic 都不在线运行。论文在仿真和实机地形/扰动上验证适应性，但 16 维 latent 没有可逐维解释的物理含义。迁移时必须保持历史顺序、归一化、控制周期、关节顺序和 PD 增益一致，不能把“隐式动力学识别”视为显式系统辨识结果。

## 实验结果与结论

论文在四足平台上展示楼梯、斜坡、高台、负载和未见扰动，并报告约 2 亿仿真帧即可训练。核心结论是显式速度与隐式稳定性互补、对比原型优于直接特权状态模仿；这些证据建立在论文的平台与奖励上，尚不能直接证明对人形机器人同样成立。

## 局限与复现提醒

- HIM 是足式 locomotion 的环境适应模块，不生成语义动作，也不等同于显式世界模型。
- 复现必须核对历史长度、16D 嵌入、原型数、Sinkhorn 温度、PPO/表征更新比例和实际传感器观测。
- 本知识库尚未运行官方训练或实机部署。

## 阅读与复现状态

- 阅读：已阅读论文与飞书方法整理。
- 代码：已核验官方训练仓库，未运行。
- 实机：论文有四足实机证据，本知识库无独立验证。

## 参考资料

- [arXiv](https://arxiv.org/abs/2312.11460)
- [官方代码](https://github.com/OpenRobotLab/HIMLoco)

## 更新记录

- 2026-09-04：按 ADAPT 式方法结构补充内部模型的动机，并用五步交替流程讲清显式速度、隐式原型表示、HIO 更新、PPO 控制和部署组件。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，纳入飞书清单，补充原论文 Figure 1、混合嵌入与对比学习解读。
