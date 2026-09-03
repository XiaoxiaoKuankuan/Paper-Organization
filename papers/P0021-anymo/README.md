<!--
---
id: P0021
title_en: "AnyMo: Scaling Any-Modality Conditional Motion Generation with Masked Modeling"
title_zh: "AnyMo：通过掩码建模扩展任意模态条件动作生成"
year: 2026
date: 2026-05-28
venue: "arXiv preprint arXiv:2605.29488"
primary_category: motion-generation
tags: [motion-generation, multimodal, masked-modeling, transformer, large-scale-data, text, music, speech]
authors: [Yiheng Li, Zhuo Li, Ruibing Hou, Yingjie Chen, Hong Chang, Hao Liu, Shiguang Shan]
institutions: [Institute of Computing Technology CAS, University of Chinese Academy of Sciences]
paper_url: "https://arxiv.org/abs/2605.29488"
project_url: null
github_url: null
video_url: null
open_source: {code: unknown, training_code: unknown, inference_code: unknown, model_weights: unknown, dataset: unknown, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, speech, music, trajectory, arbitrary modality combinations]
outputs: [human motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0021｜AnyMo：通过掩码建模扩展任意模态条件动作生成

*AnyMo: Scaling Any-Modality Conditional Motion Generation with Masked Modeling*

[论文](https://arxiv.org/abs/2605.29488)

## 本文贡献

- 构建 OmniHuMo：超过 5000 小时、320 万动作序列和精确对齐的文本、语音、音乐、轨迹标注，用于研究多模态规模化。
- 使用 Residual FSQ 动作 tokenizer 与可扩展 Masked Modeling Transformer，把不同条件组合统一成补全动作 token 的任务。
- 通过随机条件/动作掩码让同一模型支持单模态、任意组合与空间—风格联合控制，并分析数据/模型扩展趋势。

## 研究问题

多模态动作模型常固定输入组合，换模态就要改网络；更根本的瓶颈是缺少大规模严格时间对齐数据。AnyMo 先建设 OmniHuMo，再把“有什么条件”转为掩码模式，避免按任务分别定义生成头。

## 原论文重点图

![AnyMo 与 OmniHuMo](figures/key-figure.png)

**图 1：OmniHuMo 数据规模与 AnyMo 统一掩码建模（原论文 Figure 1 所在页）。** 数据从海量视频提取人体、音频、说话人、文本和轨迹；模型把可见条件 token 与被遮动作 token 共同送入 Transformer，迭代恢复未知部分。

## 研究方法详细解读

### OmniHuMo 自动管线

从超过 2 亿视频筛选候选，使用 YOLOv11/MOTRv2 跟踪人物、RTMW/GVHMR 恢复姿态、Demucs 分离音源、节拍/说话人/同步工具对齐音频，最后用视觉语言模型生成描述。每一阶段的误检都会传播，因此数据量不能替代抽样人工质检。

### Residual FSQ 动作 tokenizer

有限标量量化避免大型向量码本的低利用率，残差层逐级编码未解释细节。连续动作先变成紧凑离散 token，掩码 Transformer 才能以统一分类/恢复目标处理长序列和缺失条件。

### 任意模态掩码训练

训练随机保留或遮蔽文本、音频、轨迹和动作区间，使条件组合成为同一输入空间的不同可见集合。推理通过迭代 mask-predict 从高置信 token 开始补全；迭代次数、置信调度和条件冲突处理直接影响延迟与多样性。

## 实验结果与结论

论文报告任意模态组合下的动作质量、空间控制与风格一致性，并显示规模扩大带来稳定收益。该结论依赖 OmniHuMo 的自动标注与评测器，尚不能说明生成动作具备物理机器人可执行性。

## 局限与复现提醒

- 大规模互联网数据包含估计偏差、版权与分布不均问题；需区分原始视频、派生动作和可公开部分。
- tokenizer 的 FPS、骨架与归一化是模型接口，不能与其他动作库直接混用。
- 当前未核验完整数据/代码开放，本知识库未运行。

## 阅读与复现状态

- 阅读：已阅读原论文与飞书数据/方法整理。
- 资源：开源边界待核验。
- 运行：未进行数据构建或模型推理。

## 参考资料

- [arXiv](https://arxiv.org/abs/2605.29488)

## 更新记录

- 2026-09-03：新建条目，整理 OmniHuMo 自动管线、Residual FSQ 与任意模态掩码建模。
