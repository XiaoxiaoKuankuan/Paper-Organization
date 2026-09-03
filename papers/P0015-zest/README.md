<!--
---
id: P0015
title_en: "ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control"
title_zh: "ZEST：面向运动型机器人控制的零样本具身技能迁移"
year: 2026
date: 2026-01-30
venue: "arXiv preprint arXiv:2602.00401"
primary_category: tracking-wbc
tags: [motion-tracking, reinforcement-learning, whole-body-control, zero-shot, sim2real, humanoid]
authors: [Jean Pierre Sleiman, He Li, Alphonsus Adu-Bredu, Robin Deits, Arun Kumar, Kevin Bergamin, Mohak Bhardwaj, Scott Biddlestone, Nicola Burger, Matthew A. Estrada, Francesco Iacobelli, Twan Koolen, Alexander Lambert, Erica Lin, M. Eva Mungai, Zach Nobles, Shane Rozen-Levy, Yuyao Shi, Jiashun Wang, Jakob Welner, Fangzhou Yu, Mike Zhang, Alfred Rizzi, Jessica Hodgins, Sylvain Bertrand, Yeuhi Abe, Scott Kuindersma, Farbod Farshidian]
institutions: [RAI Institute, Boston Dynamics]
paper_url: "https://arxiv.org/abs/2602.00401"
project_url: null
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: unknown, robot_deployment: unknown}
open_source_checked: 2026-09-03
robots: [Boston Dynamics Atlas, Unitree G1, Boston Dynamics Spot]
inputs: [next reference frame, proprioception]
outputs: [residual joint position target]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0015｜ZEST：面向运动型机器人控制的零样本具身技能迁移

*ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control*

[论文](https://arxiv.org/abs/2602.00401)

## 本文贡献

- 用同一精简 RL 跟踪框架吸收高质量 MoCap、噪声单目视频与非物理动画，并在 Atlas、G1、Spot 三类形态上零样本上机。
- 只使用下一帧参考与残差动作，不依赖接触标签、未来窗口、长历史、显式状态估计器或 Teacher–Student，减少技能迁移链的专用工程。
- 结合难片段自适应 RSI、模型辅助外力课程、闭链执行器 armature 估计与精化执行器模型，解决长时高动态/多接触动作的训练稳定性。

## 研究问题

运动型技能往往因数据来源不同、闭链执行器动态和局部难片段而需要逐技能调奖励。ZEST 追问：如果把初始化采样、辅助课程和执行器建模做好，是否可以用更少的观测与奖励工程获得跨数据源、跨机器人的通用跟踪器。

## 原论文重点图

![ZEST 方法与技能迁移](figures/key-figure.png)

**图 1：ZEST 技能迁移框架（原论文 Figure 1 所在页）。** 论文把三类来源动作统一转成参考，训练阶段通过自适应起始状态和辅助外力攻克失败片段；部署时不使用这些辅助量，仅靠本体观测和下一帧参考输出残差动作。

## 研究方法详细解读

### 极简跟踪接口

每个控制步只给出下一参考帧，避免固定未来窗造成的接口依赖；策略输出相对参考关节位置的残差，使名义运动信息直接进入低层。没有显式接触标签意味着接触时序必须从参考运动与物理交互中隐式学得。

### 难度自适应训练

动作被划为时间分箱，失败率更高的分箱获得更高 RSI 概率，持续把采样预算投向薄弱段。模型辅助 wrench 从强到弱自动退火，为跳跃、爬箱、地面动作等早期难以探索的状态提供可撤销支撑；成功后不再依赖外力。

### 执行器与 sim-to-real

闭链关节的 armature 不能简单沿用开链惯量。论文从近似解析模型选择关节级等效值，并用更贴近硬件的执行器模型配合适度域随机化。这部分与策略结构同等重要：错误惯量/增益会让零样本迁移结论失效。

## 实验结果与结论

Atlas 展示 army crawl、breakdance 等动态多接触技能，Atlas/G1 从视频迁移舞蹈和爬箱，Spot 从动画迁移连续后空翻。证据说明简化接口并不必然牺牲技能范围，但论文展示不能替代对完整成功率分布、硬件冲击和安全边界的复核。

## 局限与复现提醒

- 复现必须获得准确机器人模型、执行器参数、armature、辅助力退火和动作分箱统计。
- “零样本”指仿真训练后不在目标硬件上继续学习，不代表无需重定向、系统辨识或安全调试。
- 当前未核验到完整官方训练代码，条目不宣称可端到端复现。

## 阅读与复现状态

- 阅读：已阅读原文和飞书方法整理。
- 代码：公开边界待核验。
- 运行：未仿真或实机验证。

## 参考资料

- [arXiv](https://arxiv.org/abs/2602.00401)

## 更新记录

- 2026-09-03：新建条目，整理自适应 RSI、辅助外力课程和闭链执行器建模。
