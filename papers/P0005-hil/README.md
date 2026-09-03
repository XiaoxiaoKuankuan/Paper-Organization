<!--
---
id: P0005
title_en: "HIL: Hybrid Imitation Learning for Dynamic Athletic Control"
title_zh: "HIL：面向动态运动控制的混合模仿学习"
year: 2026
date: null
venue: "ACM Transactions on Graphics (TOG), 2026"
primary_category: locomotion-prior
tags:
  - imitation-learning
  - adversarial-learning
  - reinforcement-learning
  - motion-tracking
  - motion-prior
  - locomotion
authors:
  - Jiashun Wang
  - Yifeng Jiang
  - Haotian Zhang
  - Chen Tessler
  - Davis Rempe
  - Jessica Hodgins
  - Xue Bin Peng
institutions:
  - Carnegie Mellon University
  - NVIDIA
  - Simon Fraser University
paper_url: "https://arxiv.org/abs/2505.12619"
project_url: "https://xbpeng.github.io/projects/HIL/index.html"
github_url: null
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
inputs:
  - character state
  - scene geometry
  - goal condition
outputs:
  - simulated character control
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0005/Hybrid_Imitation_Learning_TOG.pdf"
  - "local_archive/P0005/HIL_2026-leftToRight.pdf"
  - "local_archive/P0005/HIL_全文翻译与方法框架详解.pdf"
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0005｜HIL：面向动态运动控制的混合模仿学习

*HIL: Hybrid Imitation Learning for Dynamic Athletic Control*

[论文](https://arxiv.org/abs/2505.12619) · [项目页](https://xbpeng.github.io/projects/HIL/index.html) · [全文翻译与方法框架详解](attachments/全文翻译与方法框架详解.pdf) · [中英左右对照全文](attachments/中英左右对照全文.pdf)

## 1. 基本信息

- 发表：ACM Transactions on Graphics，2026。
- 项目页：[HIL](https://xbpeng.github.io/projects/HIL/index.html)
- 预印本：[arXiv:2505.12619](https://arxiv.org/abs/2505.12619)。预印本题名与最终 TOG 版本题名不同，本页以最终版本为准。
- 开源状态：官方项目页提供论文与视频，但截至核验日没有 HIL 专用代码、权重或数据下载入口。

## 本文贡献

- 在同一策略、观测与动作空间中并行训练精确动作跟踪和目标驱动对抗模仿，避免两套专家的切换开销。
- 引入场景条件判别器，使动作“像参考”之外还必须符合障碍几何与可供性，缓解 AMP 在复杂场景中的错误技能复用。
- 使用 Perturbed State Initialization 扩大参考轨迹邻域，让策略学习偏离后的恢复和技能衔接，在保真度、技能覆盖与任务完成之间取得平衡。

## 3. 研究问题

逐帧跟踪可以忠实复现动作，却难以偏离参考去适应新场景；只做对抗式分布匹配更自由，却容易模式坍塌并反复使用少数简单技能。论文目标是让一个控制器同时保留两者优势。

## 原论文重点图

![HIL 任务总览](figures/hil-overview.png)

**图 1：动态运动控制任务总览（原论文 Figure 1）。** 参考库提供跑、跳、翻越等技能，但场景目标常要求策略改变时序、组合技能或在受扰后恢复；这正是单纯逐帧跟踪与纯 AMP 各自不足的交叉区域。

![HIL 网络与训练结构](figures/hil-network.png)

**图 2：混合模仿学习结构（原论文方法图）。** Tracking 与 Goal-Directed 环境共享策略；前者给出参考跟踪奖励以固定动作质量，后者把任务奖励与场景条件判别器输出的风格奖励组合。两路 rollouts 合并进行 PPO 更新，因此混合发生在数据与目标层而非部署时的专家切换。

## 研究方法详细解读

### 双分支共享策略

- 两类并行环境共享策略与观测空间，不依赖只在参考动作中存在的相位或未来姿态。
- 跟踪分支保证技能被正确、自然地复现；对抗分支允许策略围绕目标改变时序和组合技能。
- 判别器同时接收动作与场景，使“自然”还要符合障碍可供性。
- Perturbed State Initialization 在参考状态上加扰动，训练偏离轨迹后的恢复与技能衔接。

### 训练目标与推理

策略在动作跟踪和目标驱动 AMP 环境中并行收集经验，通过共享 PPO 更新。部署时只保留统一策略，根据角色、场景和目标条件输出物理仿真角色控制，不需要在两套专家间手工切换。

## 实验结果与结论

论文在程序化跑酷障碍与 heading control 中评估。跑酷任务中，HIL 的技能准确率 0.66、跟踪误差 0.31，优于对比方法；任务完成率 0.74 虽非最高，却在自然度、技能覆盖和完成率之间更均衡。Warm-start AMP 的完成率可达 0.85，但明显偏用少数翻越动作。

## 局限与复现提醒

- 优点：训练结构简单清晰；统一目标条件让两种模仿模式可共享知识；场景条件判别器减轻无视障碍的风格匹配。
- 局限：主要是物理角色动画/仿真实验，不能直接视为真实人形机器人控制结果；技能和场景仍受参考动作与程序化任务范围限制；未开放复现代码。

### 对个人研究的价值

HIL 适合用于理解“跟踪保真”和“任务适应”的权衡，也可为舞蹈/跑酷控制中同时保留动作风格与允许动态修正提供奖励设计参考。

## 阅读与复现状态

- 阅读：已深读最终论文、中英对照、方法奖励与消融。
- 代码：尚无 HIL 专用官方代码。
- 仿真：尚未复现。
- 机器人：论文以物理角色动画为主，尚无本知识库的人形机器人迁移验证。


## 参考资料

- [官方项目页](https://xbpeng.github.io/projects/HIL/index.html)
- [预印本](https://arxiv.org/abs/2505.12619)

## 更新记录

- 2026-09-03：创建精读档案；区分预印本与最终 TOG 题名，登记三份本地材料。
- 2026-09-03：纳入两份译解附件和原论文总览/网络图，扩展混合训练与场景条件判别器解读。
