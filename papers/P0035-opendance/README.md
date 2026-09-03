<!--
---
id: P0035
title_en: "OpenDance: Multimodal Controllable 3D Dance Generation with Large-scale Internet Data"
title_zh: "OpenDance：基于大规模互联网数据的多模态可控三维舞蹈生成"
year: 2025
date: 2025-06-09
venue: "CVPR 2026"
primary_category: motion-generation
tags: [dance-generation, multimodal, masked-modeling, transformer, large-scale-data, music, text]
authors: [Jinlu Zhang, Zixi Kang, Libin Liu, Jianlong Chang, Qi Tian, Feng Gao, Yizhou Wang]
institutions: [Peking University, Huawei Cloud]
paper_url: "https://arxiv.org/abs/2506.07565"
project_url: "https://open-dance.github.io/"
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [music, text, keypoints, trajectory]
outputs: [3D dance motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0035｜OpenDance：基于大规模互联网数据的多模态可控三维舞蹈生成

*OpenDance: Multimodal Controllable 3D Dance Generation with Large-scale Internet Data*

[论文](https://arxiv.org/abs/2506.07565) · [项目页](https://open-dance.github.io/)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Jinlu Zhang、Zixi Kang、Libin Liu、Jianlong Chang、Qi Tian、Feng Gao、Yizhou Wang
>
> **机构**：Peking University、Huawei Cloud
>
> **论文时间**：2025-06-09
>
> **期刊 / 会议**：CVPR 2026
>
> **主分类**：动作生成
>
> **重点标签**：**舞蹈生成** · **多模态** · **掩码建模** · **Transformer** · **大规模数据** · **音乐** · **文本**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 从互联网构建超过 100 小时、14 种风格、147 位舞者的 OpenDanceSet，每条样本对齐 RGB、音频、2D 关键点、3D 动作和细粒度文本。
- 提出解耦舞蹈自动编码器，将空间/运动内容与风格因素分开，减少多舞者、多视角数据对动作 token 的污染。
- 以 OpenDanceNet 的多模态联合掩码训练统一音乐、文本、关键点和轨迹控制，使单模态/混合条件都成为 token 补全。

## 研究问题

小型棚拍数据限制舞种和身份覆盖，互联网数据又有相机运动、遮挡、身份与服装偏差。OpenDance 同时处理数据恢复质量、内容—风格解耦和条件组合，目标是让规模化不以失去精确控制为代价。

## 原论文重点图

![OpenDance 数据与模型](figures/key-figure.png)

**图 1：OpenDanceSet 与 OpenDanceNet（原论文 Figure 1 所在页）。** 左侧从大规模 RGB 视频建立五模态对齐数据，中间显示风格覆盖，右侧将关键点、轨迹、音乐和文本编码为条件 token，通过联合掩码 Transformer 恢复舞蹈动作。

## 研究方法详细解读

### 互联网舞蹈数据构建

视频需经历人物跟踪、2D/3D 姿态恢复、音频抽取和文本标注，再按质量筛选。147 位舞者和 14 风格提高覆盖，但相机、服装与估计器偏差仍会进入 3D 动作；数据统计应与有效可训练时长区分。

### 解耦舞蹈 tokenizer

编码器将随时间变化的动作内容与较稳定的风格/身份因素拆分，再重建统一动作 token。解耦有利于跨舞者复用编舞，但如果风格本身体现在局部运动学中，过强分离也可能损失表现力。

### 联合掩码生成

训练随机遮蔽动作、空间控制和风格条件，让 OpenDanceNet 在不同可见组合下补全。关键点/轨迹偏几何，音乐/文本偏节奏语义；联合掩码让模型学习协同，但冲突条件仍由概率模型软处理。

## 实验结果与结论

论文在音乐舞蹈、多模态控制和跨风格生成上报告强结果，并展示大数据与解耦/掩码设计的消融。其贡献主要是互联网舞蹈数据与人体生成，不证明动作可直接由机器人跟踪。

## 局限与复现提醒

- 需记录数据许可、视频去重、姿态估计器和人工筛选标准。
- 3D 恢复误差可能被模型学习为风格；应检查足接触、根漂移和骨长稳定性。
- 接机器人前需重定向、FPS 对齐、接触重算和物理筛选。

## 阅读与复现状态

- 阅读：已阅读论文与飞书数据/方法整理。
- 资源：项目页已核验，完整数据和代码发布边界待核验。
- 运行：未复现。

## 参考资料

- [arXiv](https://arxiv.org/abs/2506.07565)
- [项目页](https://open-dance.github.io/)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理五模态数据、解耦 tokenizer 和联合掩码生成。
