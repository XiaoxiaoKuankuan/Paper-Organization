<!--
---
id: P0006
title_en: "HumanoidArena: Benchmarking Egocentric Hierarchical Whole-body Learning"
title_zh: "HumanoidArena：第一视角层级式全身学习基准"
year: 2026
date: 2026-06-16
venue: "arXiv preprint arXiv:2606.17833"
primary_category: datasets
tags:
  - dataset
  - benchmark
  - human-object-interaction
  - loco-manipulation
  - whole-body-control
  - g1
  - isaac-lab
authors:
  - Taowen Wang
  - Zikang Xie
  - Bin Yang
  - Yunheng Wang
  - Zizhao Yuan
  - Yuetong Fang
  - Yixiao Feng
  - Yichi Wang
  - Xingyu Chen
  - Haodong Chen
  - Qiwei Wu
  - Weisheng Xu
  - Lihan Chen
  - Lusong Li
  - Zecui Zeng
  - Renjing Xu
institutions:
  - The Hong Kong University of Science and Technology (Guangzhou)
  - Beijing University of Technology
  - Harbin Institute of Technology, Shenzhen
  - Shenzhen MSU-BIT University
  - JD Explore Academy
paper_url: "https://arxiv.org/abs/2606.17833"
project_url: "https://humanoidarena.github.io/"
github_url: "https://github.com/William-wAng618/HumanoidArena"
video_url: null
open_source:
  code: full
  training_code: full
  inference_code: full
  model_weights: full
  dataset: full
  robot_deployment: "no"
open_source_checked: 2026-09-03
robots:
  - Unitree G1
inputs:
  - egocentric RGB
  - proprioception
  - task instruction
outputs:
  - 40D intermediate whole-body action
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0006/HUMANOIDARENA：Benchmarking Egocentric.pdf"
  - "local_archive/P0006/HUMANOIDARENA_全文翻译与方法框架图详解.docx"
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0006｜HumanoidArena：第一视角层级式全身学习基准

*HumanoidArena: Benchmarking Egocentric Hierarchical Whole-body Learning*

[论文](https://arxiv.org/abs/2606.17833) · [项目页](https://humanoidarena.github.io/) · [官方代码](https://github.com/William-wAng618/HumanoidArena) · [全文翻译与方法框架图详解](attachments/全文翻译与方法框架图详解.docx)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Taowen Wang、Zikang Xie、Bin Yang、Yunheng Wang、Zizhao Yuan、Yuetong Fang、Yixiao Feng、Yichi Wang、Xingyu Chen、Haodong Chen、Qiwei Wu、Weisheng Xu、Lihan Chen、Lusong Li、Zecui Zeng、Renjing Xu
>
> **机构**：The Hong Kong University of Science and Technology (Guangzhou)、Beijing University of Technology、Harbin Institute of Technology, Shenzhen、Shenzhen MSU-BIT University、JD Explore Academy
>
> **论文时间**：2026-06-16
>
> **期刊 / 会议**：arXiv preprint arXiv:2606.17833
>
> **主分类**：数据集
>
> **重点标签**：**数据集** · **基准** · **人-物交互** · **移动操作** · **全身控制** · **Unitree G1** · **Isaac Lab**
>
> **阅读状态**：已精读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

### 资料与开源说明

- 开源资源：官方页提供代码、训练/评估管线、LeRobot 数据、策略 checkpoint、仿真资产和原始演示；定位为 simulation-first，不宣称实机部署。

## 本文贡献

- 建立第一视角、长时程、全身操作基准，将视觉感知—高层动作预测—低层全身跟踪放入统一评测协议。
- 定义 40D 中间动作和 GMT 适配接口，让 ACT、Diffusion Policy、Flow Policy、π0.5 等高层策略公平连接 TWIST2/SONIC。
- 同时评估视觉、语义、执行扰动及 In-GMT/Cross-GMT 两类适配，揭示任务成功和跌倒并非由高层模型单独决定。

## 研究问题

现有端到端系统难区分高层策略与低层跟踪器各自贡献，也缺少下肢协调对任务成功不可替代的 HOI/HSI 基准。论文关心中间动作是否可执行、对分布变化是否鲁棒、换 GMT 后是否仍可迁移。

## 原论文重点图

![HumanoidArena 基准总览](figures/humanoidarena-overview.png)

**图 1：层级学习与评测总览（原论文 Figure 1）。** 第一视角 RGB、任务指令和本体状态输入高层策略；高层输出统一全身中间动作，再经 GMT 适配为低层跟踪命令。最终评的是机器人闭环任务成功与跌倒，而不是离线动作误差。

![扰动评测](figures/perturbation-evaluation.png)

**图 2：视觉、语义与执行扰动评测（原论文结果图）。** 三类扰动分别定位感知泛化、语义理解和控制容错问题，使失败能追溯到高层策略或 GMT 接口。

## 研究方法详细解读

HumanoidArena 首先是一个分层全身学习基准，而不是又一个低层控制算法。它刻意把“第一视角看懂任务并决定下一目标动作”和“让机器人在动力学中把目标动作做出来”拆成高层策略与 GMT 后端，再通过统一接口交叉替换 tracker，判断失败究竟来自视觉决策还是低层执行。

### 1. 总体定位：这个基准要回答什么问题

具身任务论文常把视觉策略、动作表示、遥操作数据和低层 tracker 捆在一起报告一个成功率，换一个控制后端后结论就可能变化。HumanoidArena 要建立可比较协议：同一批第一视角任务、同一套高层动作和同一份演示，分别接入 TWIST2 与 SONIC 等 GMT，测量策略在原后端和未见后端上的表现，从而暴露 embodiment gap、误差累积及控制器依赖。

### 2. 完整数据与训练流程：五个环节

1. VR 操作者提供头手动作，GMR 在线重定向为机器人参考，选定 GMT 在 IsaacLab 中执行。
2. 同步记录第一视角图像、自然语言、本体状态、高层目标动作和双手开合，形成模仿数据。
3. 高层模型从图像、指令与本体状态预测统一的 40 维下一目标，而不是直接输出电机力矩。
4. 适配器把统一动作转换成不同 GMT 所需命令，低层 tracker 闭环产生机器人控制。
5. 在七类任务、不同扰动和交叉 tracker 组合上评估，分别统计任务完成与低层执行差异。

### 3. 总体信息流：视觉策略与通用动作跟踪器解耦

HumanoidArena 把全身操作拆成“高层视觉模仿策略 + 低层 GMT”。第一视角图像、文字任务指令和规范化本体状态进入高层模型，高层每步输出下一目标基座位姿、29 个关节目标以及双手开合；适配器 `ψm` 将这套统一动作接口转换为 TWIST2 或 SONIC 所需的参考命令，低层跟踪器再依据真实仿真状态产生关节控制。这样同一份任务数据可以在不同 GMT 后端上训练和交叉测试，测出的性能变化能分离视觉决策能力与跟踪后端差异。

### 统一观测、动作与任务定义

本体输入为 64 维：根旋转 6D、29 维关节位置和 29 维关节速度；视觉输入为 640×480 第一视角图像，另有自然语言指令。高层动作共 40 维，由根平面位移 2 维、根高度、根旋转 6D、29 维目标关节以及两只手的二值开合构成。Football、DoubleDesk、P&PBox、OpenDoor、SitSofa、Boxing、VisNavi 七类任务覆盖移动、接触、双手操作和视觉导航，动作定义保持一致，任务差异只通过观测和演示体现。

### VR 示范采集与数据记录链

操作者通过 PICO 设备提供头手运动，GMR 将人体动作在线重定向成机器人参考，并以 35 维 mimic observation 经 Redis 送入所选 GMT 后端；GMT 在 IsaacLab 中闭环执行，系统同步记录相机、本体状态、高层动作和后端标识。失败演示被剔除，每个任务、每个后端保留 100 条成功轨迹，TWIST2 与 SONIC 合计形成 1,400 条、50 Hz 数据；随后转换为统一 LeRobot 格式并检查时序与字段。多相机重放用于补充视角，但不能替代原始闭环演示中的状态—动作对齐。

### 高层策略如何训练

论文把 ACT、Diffusion Policy、Flow Matching 与 π0.5 等基线都适配到相同输入输出契约：视觉编码器提取图像特征，文字条件表达任务，本体历史提供机器人当前构型，动作头预测一段或一步统一高层动作。训练是离线监督模仿，目标来自成功示范，而低层 GMT 参数保持固定；各基线统一训练 100k 梯度步，使比较聚焦模型结构而不是训练预算。序列型方法在推理时按其动作块/生成过程滚动执行，再由适配器逐帧送给 GMT。

### GMT 适配与交叉后端协议

`ψm` 负责把 40 维高层动作改写为后端所需参考：既要处理根姿态与关节目标的坐标约定，也要补齐 TWIST2/SONIC 各自需要的命令窗口；两只手的开合则交给对应手部执行接口。训练—测试使用同一 GMT 测量端到端上限，训练数据来自 A 后端而测试切换 B 后端则测量策略对动作执行分布变化的敏感性。相对保持率、绝对成功率下降和平均摔倒率共同报告，避免只看任务完成而忽略稳定性。

### 推理、评测与证据边界

每次评测由高层读取当前图像/状态、产生统一动作、适配器转换、GMT 执行、环境返回下一观测构成闭环；每项设置使用 3 个随机种子、每种子 20 次 rollout。视觉扰动分别改变外观/光照，语义扰动替换相似资产，状态扰动扩大物体初始位置，用来定位感知与控制失败来源。该基准训练和验证的是 IsaacLab 中的层级策略，不是端到端实机数据；“跨 GMT”也只说明接口迁移，不能等价为跨机器人或硬件安全验证。

## 实验结果与结论

TWIST2 下 Flow Matching 的 HOI/HSI 最佳平均成功率为 36.11%/58.75%；SONIC 下 Diffusion Policy 为 52.22%/65.83%。跨 GMT 后平均性能大幅下降，T→S 与 S→T 的平均绝对下降约 39.9% 与 36.0%，且摔倒/任务保持呈不对称，说明当前 40D 接口仍携带后端特定分布。

## 局限与复现提醒

- 优点：把 GMT 作为显式实验变量；任务要求真实全身协调；数据、checkpoint 与评估协议资源完整。
- 局限：仿真优先、任务数和演示数有限；训练只含成功示范；跨 GMT 脆弱说明“canonical action”尚未真正后端无关。

### 对个人研究的价值

这是验证 GMT 接口是否可替换的直接基准。对于 SONIC/GMT 部署链路，应复用其 64D 状态、40D 动作、adapter 边界和跨后端评估，而不能只比较单一控制器下的任务成功率。

## 阅读与复现状态

- 阅读：已深读原文和完整中文译解，并核对动作接口与评测协议。
- 资源：已核验代码、数据、模型与资产入口。
- 运行：尚未下载验证完整数据契约，也未运行 Isaac Lab benchmark。
- 迁移：尚未独立复测 Cross-GMT。


## 参考资料

- [论文](https://arxiv.org/abs/2606.17833)
- [官方项目页](https://humanoidarena.github.io/)
- [官方代码](https://github.com/William-wAng618/HumanoidArena)

## 更新记录

- 2026-09-04：按 ADAPT 式讲解重构方法开篇，先说明基准要分离的高低层问题，再用 VR 采集、模仿训练、统一动作、GMT 适配和交叉评测五环节串起全链路。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：创建基准精读档案；核验公开代码、数据、权重和资产，明确 simulation-first 边界。
- 2026-09-03：纳入译解附件和原论文总览/扰动图，细化 40D 接口与跨 GMT 评测方法。
