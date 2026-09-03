<!--
---
id: P0014
title_en: "What Matters in Humanoid General Motion Tracking? An Empirical Study"
title_zh: "人形机器人通用动作跟踪中什么最重要？一项实证研究"
year: 2026
date: 2026-07-22
venue: "arXiv preprint arXiv:2607.19903"
primary_category: tracking-wbc
tags: [motion-tracking, benchmark, reinforcement-learning, whole-body-control, g1, sim2real]
authors: [Fabio Amadio, Enrico Mingo Hoffman]
institutions: [Inria, Université de Lorraine, CNRS]
paper_url: "https://arxiv.org/abs/2607.19903"
project_url: null
github_url: "https://github.com/hucebot/yahmp"
video_url: "https://youtu.be/BH6FpQzwm8M"
open_source: {code: full, training_code: full, inference_code: full, model_weights: full, dataset: partial, robot_deployment: full}
open_source_checked: 2026-09-03
robots: [Unitree G1]
inputs: [motion reference, observation history, proprioception]
outputs: [residual joint position target]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0014｜人形机器人通用动作跟踪中什么最重要？一项实证研究

*What Matters in Humanoid General Motion Tracking? An Empirical Study*

[论文](https://arxiv.org/abs/2607.19903) · [YAHMP 官方代码](https://github.com/hucebot/yahmp) · [实验视频](https://youtu.be/BH6FpQzwm8M)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Fabio Amadio、Enrico Mingo Hoffman
>
> **机构**：Inria、Université de Lorraine、CNRS
>
> **论文时间**：2026-07-22
>
> **期刊 / 会议**：arXiv preprint arXiv:2607.19903
>
> **主分类**：动作跟踪与全身控制
>
> **重点标签**：**动作跟踪** · **基准** · **强化学习** · **全身控制** · **Unitree G1** · **Sim2Real**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 在同一 YAHMP 框架与动作集上逐项控制变量，比较参考命令、观测历史、动作表示、PD 配置、手部外力随机化和 Teacher–Student，而非比较彼此完全不同的整套系统。
- 给出可操作结论：参考关节速度和约 0.2 秒历史显著重要，残差动作有中等收益，更硬的 PD 不稳定地改善跟踪且增加峰值力矩。
- 开源 50 Hz Unitree G1 的训练、评估、部署与 ONNX 流程，并以零样本实机跟踪、外扰和负载实验补足仿真消融。

## 研究问题

通用跟踪论文往往同时改变网络、奖励、观测和执行器参数，难以知道提升来自哪里。本文固定名义配置，只替换一个因素；因此它的价值不是提出更复杂的 tracker，而是建立能复核设计取舍的受控基线。

## 原论文重点图

![YAHMP 实验框架](figures/key-figure.png)

**图 1：YAHMP 受控实验管线（原论文 Figure 1 所在页）。** MoCap 参考进入统一跟踪环境，右侧六组开关分别控制命令、历史、动作、执行器、手力与训练范式，最终走同一 sim-to-real 链路。每个结论只对这一共同协议内的变量差异负责。

## 研究方法详细解读

### 总体流程：用受控实验拆解跟踪器设计

YAHMP/What Matters 不是再堆一个新控制网络，而是在统一 Unitree G1、统一动作库、奖励、随机化和 PPO 预算下，一次只改变参考命令、历史、动作参数化、PD 增益、外力交互或训练范式。基准链路为：AMASS/OMOMO 动作重定向成 29 自由度参考，策略读取本体和 10 步历史以及未来参考，输出参考附近的残差关节目标，PD 转为力矩；仿真跟踪误差和正则组成奖励。这样消融差异才能归因到被改变的单一设计项。

### 基准观测与参考命令

本体观测包括基座角速度、投影重力、相对名义姿态的关节位置、关节速度和上一动作。命令不仅有参考关节位置/速度，还包含基座平面速度、偏航速度、高度及滚转/俯仰；最近 10 步本体经时间卷积（通道 48/24、核 6/4、步长 2）压成 64 维，再与当前量进入 MLP `[512,512,256,128]`。动作表示为参考关节角上的残差，PD 执行得到力矩，因此网络主要学习动力学纠偏而不是从零重建姿态。

### 参考速度、历史和动作参数化消融

删除参考速度会丢失“同一姿态正向哪个方向运动”的瞬时趋势，位置、速度和末端误差均上升；历史从 0 增至 10 步显著改善部分可观测性，而 20 步并未稳定优于 10 步，说明更长窗口也增加冗余和优化负担。Direct Action 以默认站姿为中心输出绝对目标，Residual Action 则以当前参考为中心，只学误差补偿；后者把运动学先验直接交给执行器，是性能差异的接口原因，而不是简单网络容量变化。

### 机械一致的 PD 增益与动作尺度

Mechanics-based 设置依据关节反射惯量、目标自然频率和阻尼比计算 `Kp/Kd`，再结合力矩限幅设计动作 scale，使策略的归一化输出在不同关节上有相近控制意义。Stiffer 设置代表常见经验高增益：短期误差可能更小，但更容易放大噪声、触发力矩饱和或降低接触顺应性。论文因此把策略参数和执行器闭环一起评估；只复制神经网络 checkpoint 而不复制增益、动作缩放与力矩限制，无法复现实验结论。

### 单阶段 PPO 与 Teacher–Student

单阶段方案让 actor 只看部署观测、critic 使用特权信息，用 PPO 直接训练 20k 迭代。Teacher–Student 先训练可读取更多环境状态的 teacher，再让 student 通过 PPO 加 teacher KL/动作引导训练另一个 20k 迭代；二者总预算和可见信息被明确区分。统一奖励包括姿态/速度/根运动跟踪、接触和动作正则，reset 与基于失败统计的动作相位采样也固定，使蒸馏的收益不被额外 curriculum 混淆。

### 外力交互与训练数据

动作库由 12,175 条 AMASS/OMOMO 片段组成，11,151 训练、1,024 测试；8,192 个并行环境训练约 25 小时（RTX 4090 口径）。手部外力版本在训练中加入受力交互并遵守关节力矩限制，它对自由空间 MPJPE 未必有利，却会显著改变推压、承载等任务表现。因此“最佳 tracker”取决于目标分布：纯动作播放与接触操作不能用同一个单一指标选型。

### 推理与结论边界

部署时只有历史卷积、actor、残差动作和 PD 环在线运行，特权 critic/teacher 均删除。论文结论是在固定 G1 资产与统一协议下得到的因果式消融，不保证相同排序会跨机器人、控制频率或动作库保持。复现应逐项锁定关节序、参考速度定义、历史长度、动作中心、增益、随机化和训练预算，避免一次改变多个变量后仍引用论文结论。

## 实验结果与结论

在 1024 条测试动作上，移除参考速度使基座、关键身体和关节误差普遍恶化；TWIST2 在关键点位置上有优势，但 YAHMP 名义配置在方向和关节空间更均衡。真实 G1 的 mechanics-based 配置比 stiff PD 更平滑、峰值力矩更低。结论是跟踪精度、执行器负担与交互能力必须分别评价。

## 局限与复现提醒

- 结论来自单一机器人、数据处理与奖励实现，不能把“10 步最佳”当作跨平台常数。
- 必须固定重定向动作集、50 Hz、action scale、PD 增益与测试动作，才是控制变量实验。
- 本知识库仅完成静态阅读，尚未运行 YAHMP 或 ONNX 实机链路。

## 阅读与复现状态

- 阅读：已阅读原文、飞书深度整理与主要消融。
- 资源：代码、模型与部署入口已核验。
- 运行：未训练、未仿真、未实机验证。

## 参考资料

- [arXiv](https://arxiv.org/abs/2607.19903)
- [官方代码](https://github.com/hucebot/yahmp)

## 更新记录

- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，系统整理六类消融、50 Hz 部署与原论文实验框架。
