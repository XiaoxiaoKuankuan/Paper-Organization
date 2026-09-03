<!--
---
id: P0004
title_en: "GigaBrain-WBC-0.5: A Behavior World Model for Robust Whole-Body Control with Environment Interaction"
title_zh: "GigaBrain-WBC-0.5：用于环境交互鲁棒全身控制的行为世界模型"
year: 2026
date: 2026-08-18
venue: "Technical report, arXiv:2608.18234"
primary_category: world-model-vla-agent
tags:
  - world-model
  - whole-body-control
  - motion-tracking
  - transformer
  - physics-feedback
  - g1
  - sim2real
authors:
  - Ziyang Cheng
  - Tianshu Tang
  - Jinxin Lan
  - Xinze Chen
  - Yuhan Gong
  - Zhichao Liu
  - Changzhong Wu
  - Yahao Mao
  - Zongyan Deng
  - Mingxuan Ma
  - Huasen Xi
  - Yilong Liu
  - Yutong Wu
  - Xiaofeng Wang
  - Yang Wang
  - Yun Ye
  - Guan Huang
  - Xiaojie Jin
  - Zheng Zhu
  - Jiwen Lu
institutions:
  - Tsinghua University
  - GigaAI
  - University of Shanghai for Science and Technology
  - Beijing Jiaotong University
  - Institute of Automation, Chinese Academy of Sciences
  - University of Chinese Academy of Sciences
paper_url: "https://arxiv.org/abs/2608.18234"
project_url: "https://shepherd1226.github.io/gigabrain-wbc-0.5/"
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
robots:
  - Unitree G1
  - Maker L01
inputs:
  - proprioception
  - previous action
  - latent behavior command
outputs:
  - joint position target
  - next proprioceptive state
  - next behavior distribution
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0004/GigaBrain-WBC-0.5: A Behavior World Model.pdf"
  - "local_archive/P0004/GigaBrain-WBC-0.5_方法讲解与全文中文翻译.pdf"
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0004｜GigaBrain-WBC-0.5：行为世界模型全身控制

*GigaBrain-WBC-0.5: A Behavior World Model for Robust Whole-Body Control with Environment Interaction*

[论文](https://arxiv.org/abs/2608.18234) · [项目页](https://shepherd1226.github.io/gigabrain-wbc-0.5/) · [方法讲解与全文中文翻译](attachments/方法讲解与全文中文翻译.pdf)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Ziyang Cheng、Tianshu Tang、Jinxin Lan、Xinze Chen、Yuhan Gong、Zhichao Liu、Changzhong Wu、Yahao Mao、Zongyan Deng、Mingxuan Ma、Huasen Xi、Yilong Liu、Yutong Wu、Xiaofeng Wang、Yang Wang、Yun Ye、Guan Huang、Xiaojie Jin、Zheng Zhu、Jiwen Lu
>
> **机构**：Tsinghua University、GigaAI、University of Shanghai for Science and Technology、Beijing Jiaotong University、Institute of Automation, Chinese Academy of Sciences、University of Chinese Academy of Sciences
>
> **论文时间**：2026-08-18
>
> **期刊 / 会议**：Technical report, arXiv:2608.18234
>
> **主分类**：世界模型 / VLA / Agent
>
> **重点标签**：**世界模型** · **全身控制** · **动作跟踪** · **Transformer** · **物理反馈** · **Unitree G1** · **Sim2Real**
>
> **阅读状态**：已精读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

### 资料与开源说明

- 开源状态：项目页标注代码 “coming soon”；当前无官方 GitHub、权重或数据下载入口。

## 本文贡献

- 把全身控制策略扩展为因果行为世界模型，同步预测关节动作、下一本体状态和下一行为分布。
- 从已有动作的接触轨迹自动恢复可仿真支撑几何，构造包含椅子、台阶、负载等环境交互的训练数据，而不只训练空场平地跟踪。
- 在部署时用上一时刻预测的 GMM 检测行为命令是否分布外，并把越界指令沿原意图方向回缩到安全椭球，提供 best-effort 执行。

## 研究问题

大规模跟踪器通常在空场景和平地训练，无法利用椅子、台阶、负载等环境接触；当参考命令在当前环境下不可行时，纯反应式策略也缺少“当前还能做什么”的显式估计。

## 原论文重点图

![GigaBrain-WBC 方法框架](figures/gigabrain-framework.png)

**图 1：行为世界模型控制框架（原论文方法图）。** 当前本体状态、历史动作和未来参考编码进入因果 Transformer；动作头负责 PD 目标，状态头学习一步动力学，行为头输出下一行为的混合高斯分布。部署端以该分布筛查外部指令，形成“预测可行行为—修正命令—闭环执行”的链路。

![交互地形自动生成](figures/terrain-generation.png)

**图 2：接触驱动的三维支撑恢复（原论文方法图）。** 管线从重定向动作中寻找低速接触点，聚类并拟合平面/几何原语，再剔除全身穿透的场景。这使动作和环境不是随机拼接，而是由动作真实发生过的接触关系配对。

## 研究方法详细解读

### 输入、网络与输出

控制频率 50 Hz。输入为 67D 本体状态、29D 上一步动作和 64D 行为命令，共 160D；核心为 6 层、4 头、局部窗口 32 帧的因果 Transformer。三个输出头分别给出 29D PD 关节目标、下一 67D 状态和下一行为的 4 分量对角 GMM。

### 数据构造与联合训练

自动标注管线从重定向动作中的低速接触点恢复点云，经全身穿透过滤、DBSCAN 和几何原语拟合得到可仿真的 3D 支撑。训练动作来自 Bones-Seed、MotionMillion、MotionDecode 共 2188 小时，其中恢复约 72.57 小时地形交互。PPO 主目标配合参考重建/循环一致性、下一状态预测和行为 GMM 似然损失。

### 在线指令修正

原始参考编码后先由上一时刻 GMM 做 OOD 判断；越界时不急停，而是沿原意图方向投影到安全半径 `R_safe=3` 的椭球边界，再由策略执行。这个过滤器检测训练分布偏离，不是形式化物理安全证明。

## 实验结果与结论

论文报告 Standard 成功率 96.3%，Terrain 81.3%，不合理参考下 83.1%，摔倒恢复 99.3%；地形结果约为最强基线 4.3 倍。硬件演示覆盖坐支撑、上平台、携带负载、支撑缺失、外部扰动和跨 Maker L01 微调，但项目页明确说明核心量化表为 MuJoCo sim-to-sim。

## 局限与复现提醒

- 优点：把环境依赖的行为可行性建模、数据生成和部署过滤统一到同一控制器。
- 局限：OOD 距离不是风险或稳定性证明；安全半径需随 checkpoint/机器人重新标定；自动几何只恢复真实接触过的支撑面；代码尚未开放。

### 对个人研究的价值

它为 SONIC/GMT 类控制器补充“环境如何改变可执行行为”的建模层，适合研究从平地跟踪走向支撑交互与 best-effort 指令修正；不应把它当作高层视觉世界模型。

## 阅读与复现状态

- 阅读：已深读原文与方法译解，核对 50 Hz、输入输出和主要量化结果。
- 代码/权重：官方仍标记为即将发布。
- 仿真：尚未复现论文指标。
- 实机：项目视频不等同于本知识库的独立安全验证。


## 参考资料

- [论文](https://arxiv.org/abs/2608.18234)
- [官方项目页](https://shepherd1226.github.io/gigabrain-wbc-0.5/)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：创建精读档案；将项目页“代码即将发布”和 sim-to-sim/硬件演示边界分别记录。
- 2026-09-03：纳入译解附件、行为世界模型图和地形恢复图，细化三输出头与 OOD 回缩机制。
