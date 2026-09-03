<!--
---
id: P0038
title_en: "TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control"
title_zh: "TextOp：实时交互式文本驱动人形机器人动作生成与控制"
year: 2026
date: 2026-02-07
venue: "arXiv preprint arXiv:2602.07439"
primary_category: motion-generation
tags: [motion-generation, motion-tracking, diffusion, autoregressive, text, real-time, humanoid, sim2real]
authors: [Weiji Xie, Jiakun Zheng, Jinrui Han, Jiyuan Shi, Weinan Zhang, Chenjia Bai, Xuelong Li]
institutions: [Institute of Artificial Intelligence TeleAI China Telecom, Shanghai Jiao Tong University, East China University of Science and Technology]
paper_url: "https://arxiv.org/abs/2602.07439"
project_url: "https://text-op.github.io/"
github_url: null
video_url: null
open_source: {code: partial, training_code: unknown, inference_code: full, model_weights: unknown, dataset: unknown, robot_deployment: partial}
open_source_checked: 2026-09-03
robots: [humanoid]
inputs: [streaming text, motion history, proprioception]
outputs: [short-horizon motion, joint control]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0038｜TextOp：实时交互式文本驱动人形机器人动作生成与控制

*TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control*

[论文](https://arxiv.org/abs/2602.07439) · [项目页与开源入口](https://text-op.github.io/)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Weiji Xie、Jiakun Zheng、Jinrui Han、Jiyuan Shi、Weinan Zhang、Chenjia Bai、Xuelong Li
>
> **机构**：Institute of Artificial Intelligence TeleAI China Telecom、Shanghai Jiao Tong University、East China University of Science and Technology
>
> **论文时间**：2026-02-07
>
> **期刊 / 会议**：arXiv preprint arXiv:2602.07439
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **动作跟踪** · **扩散模型** · **自回归** · **文本** · **实时** · **人形机器人** · **Sim2Real**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 提出两层实时系统：高层自回归动作扩散不断生成短时运动学参考，低层通用跟踪策略在真实人形机器人上闭环执行。
- 支持执行过程中流式输入和即时修改文本，使站立、挥手、舞蹈、跳跃、太极等技能在一次连续试验中平滑切换。
- 通过动作历史条件和短窗滚动生成解决传统离线 text-to-motion 必须先生成完整序列、难以响应用户意图变化的问题。

## 研究问题

预定义轨迹灵活性低，持续遥操作又要求人全程参与。文本能表达自由意图，但离线生成延迟和动作段拼接不适合闭环。TextOp 选择“短时生成 + 稳健跟踪”，在语义响应速度与低层稳定性之间分层。

## 原论文重点图

![TextOp 连续文本控制](figures/key-figure.png)

**图 1：单次连续试验中的在线提示切换（原论文 Figure 1 所在页）。** 时间轴上用户依次发送 bow、stand、wave、hiphop、punch 等命令；高层生成器滚动续写，低层 tracker 不重启，从而避免技能切换时回到默认站姿。

## 研究方法详细解读

### 高层自回归扩散

生成器以当前文本、最近动作历史和当前状态为条件，只预测下一短窗运动学轨迹。新窗口接回历史继续生成；提示变化在下一滚动周期生效。窗口越短响应越快但上下文不足，越长则延迟和重规划代价增加。

### 动作衔接

历史条件让生成器看到当前姿态/速度，避免每个文本独立从标准初态采样。训练需模拟不同提示和历史边界，否则推理时会出现根跳变、速度断裂或脚接触不连续。

### 低层跟踪与实机

低层策略将运动学参考变成关节动作，吸收模型误差与扰动。生成器的“流畅”与机器人“可执行”由不同模块保证；端到端延迟必须包含文本编码、扩散、传输、tracker 和机器人控制周期。

## 实验结果与结论

论文用离线指标与真实机器人连续试验展示即时响应、平滑切换和多种高动态技能。结果证明文本可作为实时上层接口，但具体成功率、安全和跨平台泛化仍受 tracker 与硬件限制。

## 局限与复现提醒

- 长时自回归会累积漂移；突变提示可能在动力学上不可直接衔接。
- 复现必须锁定生成窗/历史窗、文本更新时间、动作表示、tracker checkpoint 与控制频率。
- 官方页面提供开源入口，但训练、权重和完整部署项应逐项核验；本知识库未运行。

## 阅读与复现状态

- 阅读：已阅读原文与飞书方法整理。
- 资源：项目页已核验，开源分项保守记录。
- 运行：未进行仿真或实机验证。

## 参考资料

- [arXiv](https://arxiv.org/abs/2602.07439)
- [项目页](https://text-op.github.io/)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理短窗自回归生成、历史衔接和低层跟踪接口。
