<!--
---
id: P0017
title_en: "Kimodo: Scaling Controllable Human Motion Generation"
title_zh: "Kimodo：可控人体动作生成的规模化"
year: 2026
date: 2026-03-16
venue: "NVIDIA Technical Report, arXiv:2603.15546"
primary_category: motion-generation
tags: [motion-generation, diffusion, transformer, text, keypoints, large-scale-data, human-motion]
authors: [Davis Rempe, Mathis Petrovich, Ye Yuan, Haotian Zhang, Xue Bin Peng, Yifeng Jiang, Tingwu Wang, Umar Iqbal, David Minor, Michael de Ruyter, Jiefeng Li, Chen Tessler, Edy Lim, Eugene Jeong, Sam Wu, Ehsan Hassani, Michael Huang, Jin-Bey Yu, Chaeyeon Chung, Lina Song, Olivier Dionne, Jan Kautz, Simon Yuen, Sanja Fidler]
institutions: [NVIDIA]
paper_url: "https://arxiv.org/abs/2603.15546"
project_url: "https://research.nvidia.com/labs/sil/projects/kimodo"
github_url: "https://github.com/nv-tlabs/kimodo"
video_url: null
open_source: {code: full, training_code: full, inference_code: full, model_weights: full, dataset: partial, robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, full-body keyframes, sparse joint constraints, 2D waypoints, 2D paths]
outputs: [SOMA human motion]
read_status: deep-read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0017｜Kimodo：可控人体动作生成的规模化

*Kimodo: Scaling Controllable Human Motion Generation*

[论文](https://arxiv.org/abs/2603.15546) · [项目页](https://research.nvidia.com/labs/sil/projects/kimodo) · [官方代码](https://github.com/nv-tlabs/kimodo) · [中英左右对照技术报告](attachments/中英左右对照技术报告.pdf)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Davis Rempe、Mathis Petrovich、Ye Yuan、Haotian Zhang、Xue Bin Peng、Yifeng Jiang、Tingwu Wang、Umar Iqbal、David Minor、Michael de Ruyter、Jiefeng Li、Chen Tessler、Edy Lim、Eugene Jeong、Sam Wu、Ehsan Hassani、Michael Huang、Jin-Bey Yu、Chaeyeon Chung、Lina Song、Olivier Dionne、Jan Kautz、Simon Yuen、Sanja Fidler
>
> **机构**：NVIDIA
>
> **论文时间**：2026-03-16
>
> **期刊 / 会议**：NVIDIA Technical Report, arXiv:2603.15546
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **扩散模型** · **Transformer** · **文本** · **关键点** · **大规模数据** · **人体动作**
>
> **阅读状态**：已精读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 在 700 小时高质量光学 MoCap 上训练可扩展扩散模型，系统分析数据规模与模型规模对动作质量、泛化和约束精度的影响。
- 设计根部—身体两阶段去噪器：先稳定全局轨迹，再在其条件下生成局部身体细节，降低根漂移与脚部伪影。
- 统一文本、全身关键帧、稀疏关节位置/旋转、2D waypoint 和稠密 2D path 等约束，实现同一模型的强可控生成。

## 研究问题

公开 MoCap 规模限制了动作生成的长尾覆盖，而把所有控制条件直接塞进一个去噪器容易让全局轨迹与局部姿态互相干扰。Kimodo 通过大规模高质量数据和结构化分解检验“规模是否能转化为可控性”，而不仅是提高无条件视觉质量。

## 原论文重点图

![Kimodo 方法总览](figures/key-figure.png)

**图 1：Kimodo 控制条件与两阶段生成（原论文 Figure 1 所在页）。** 文本提供语义，关键帧/关节/二维路径提供不同粒度几何约束；root denoiser 先确定全局移动，body denoiser 再补全身体动作。分解让路径约束不必与高维局部关节在同一预测头直接竞争。

## 研究方法详细解读

Kimodo 的核心不是把根轨迹和身体姿态分给两个模型后各跑一次，而是在每个扩散去噪步中让 Root-Diffuser 与 Body-Diffuser 反复交换结果。根模型先处理世界轨迹、方向和空间约束，身体模型再根据最新根状态生成全身；下一步根模型又看到更新后的身体条件，因此全局可控性和局部动作自然性在整个采样过程中共同收敛。

### 1. 总体定位：为什么一个动作扩散器难以同时处理所有约束

文本决定高层语义，二维/三维关键点、朝向和已有帧可能只约束局部时空位置，而长序列根轨迹与高维身体姿态的尺度和统计规律不同。单个网络既要规划世界路径又要补足肢体细节，容易让强约束压制动作先验，或让自然姿态偏离目标。Kimodo 因此把根与身体分层建模，并用统一 mask 接口表示任意组合的已知条件。

### 2. 整体训练与推理流程：分阶段训练、交替去噪

1. 统一大规模人体动作、文本和稀疏控制，构造全局根表示、局部身体表示及条件可见 mask。
2. 先训练 Root-Diffuser，根据文本和空间约束恢复根位置、朝向、局部速度与高度。
3. 再训练 Body-Diffuser，以干净/预测根轨迹和外部条件恢复全身姿态，并通过课程逐步接触根预测误差。
4. 推理每个扩散步先更新根，再将根交给身体模型；身体结果反馈到下一去噪步，而不是两个模型各采样一次。
5. 生成结果是 SOMA/人体动作，可用于编辑、补全和长序列控制；机器人部署仍需重定向、可执行性筛选和 tracker。

### 3. 总体信息流：先生成全局根，再补全身体

Kimodo 把输入文本、朝向、二维/三维稀疏关键点和已有动作帧统一成带 mask 的约束。扩散推理在每个时间步交替运行两个模型：Root-Diffuser 先决定全局根位置/朝向，转换为局部速度与高度；Body-Diffuser 再以最新根轨迹和外部约束恢复全身。下一去噪步又把身体结果反馈给根模型，如此迭代直到得到完整 SOMA 动作。两阶段不是简单串行一次，而是在去噪循环中反复交换当前估计，使路径与身体姿态共同收敛。

### 全局表示与约束编码

动作保留平滑后的全局根位置和 heading 的正余弦；各关节使用相对根的水平位置、全局高度、全局速度、全局 6D 旋转及接触。训练时从真值中随机抽取不同关节、时间密度和 2D/3D 形式的目标值，未约束处由 mask 标明；目标值直接覆盖对应带噪输入并把 mask 拼接给网络。文本经 LLM2Vec 得到 4,096 维语义，heading 与约 49 个零占位 token 共同保持统一条件长度。

### Root/Body 两个扩散 Transformer

两个去噪器各为 16 层、8 头、隐宽 1,024 的 Transformer，总规模约 282M。Root 分支预测全局轨迹后显式求局部平面速度和根高度，Body 分支读取这些根量并预测关节通道；这种拆分让用户路径约束直接落在可解释的全局变量，而高维身体细节不拖累根轨迹优化。根输出进入身体前必须用同一规范化和坐标变换，否则小的偏航误差会转成全身位置漂移。

### 损失函数与两阶段课程

训练以分量 Smooth-L1 监督根和身体输出，并通过前向运动学把预测旋转转换为关节位置，加入旋转—位置一致性及速度/接触相关约束。前 500k 步只做文本到动作，先建立不受稀疏条件干扰的运动与语义先验；后 500k 步混合关键帧、路径等约束，其中约 25% 使用组合约束、10% 无约束，文本也以约 10% 概率丢弃。优化使用 EMA，最大 10 秒、30 FPS，论文设置 batch 2,048、16 张 A100、`atan2` 学习率调度和约 `2e-5` 学习率。

### 推理时条件组合与长序列编辑

推理采用 100 步 DDIM，并把文本和空间约束相对无条件分支的引导分开加权（典型权重为 2），因此可以独立调节“语义像不像”和“关键点准不准”。多提示长序列通过时间区间与重叠窗口拼接，完整身体关键帧可作为段间锚点，重叠区域再融合。可选 foot-lock、IK 或优化后处理用于修复接触，但论文主实验未用这些步骤，比较时不能把后处理收益算到基础模型上。

### 数据缩放与机器人边界

论文从约 700 小时高质量动作中逐步增加子集和模型规模，观察生成质量与约束遵循；收益来自覆盖和采集质量，并非任意互联网数据堆叠。输出位于 SOMA 人体表示，接入机器人需经 SOMA Retargeter 和低层跟踪器。私有数据使完整缩放曲线难以公开复现，且人体约束满足、足接触观感与机器人动力学可执行是三个不同验证层级。

## 实验结果与结论

在大规模 MoCap 与 HumanML3D 等协议上，Kimodo 在文本质量和多类运动学约束上取得强结果，并能生成训练分布外组合。论文支持“数据/模型扩大提升可控性”的结论，但不证明生成结果具备机器人接触与力矩可行性。

## 局限与复现提醒

- 700 小时光学 MoCap 未等价完整公开数据，公开代码无法单独复现数据缩放结论。
- 二维路径需要明确相机/地面坐标定义；SOMA 到 SMPL/机器人需额外转换。
- 本知识库已深读对照文档，但未运行官方模型。

## 阅读与复现状态

- 阅读：已深读技术报告与中英左右对照材料。
- 资源：代码和模型入口已核验，训练数据仅部分可得。
- 运行：未执行生成或约束评测。

## 参考资料

- [arXiv](https://arxiv.org/abs/2603.15546)
- [项目页](https://research.nvidia.com/labs/sil/projects/kimodo)
- [官方代码](https://github.com/nv-tlabs/kimodo)

## 更新记录

- 2026-09-04：按 ADAPT 式方法结构补充单模型处理多类约束的矛盾，并用五步流程明确 Root/Body 两阶段训练、课程连接和逐去噪步交替反馈。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建精读条目，纳入中英对照附件和原论文重点图，解析 root/body 两阶段与控制条件。
