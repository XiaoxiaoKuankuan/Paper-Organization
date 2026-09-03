<!--
---
id: P0025
title_en: "A Unified Framework for Multimodal, Multi-Part Human Motion Synthesis"
title_zh: "UDE-2：多模态、多身体部位人体动作合成统一框架"
year: 2023
date: 2023-11-28
venue: "arXiv preprint arXiv:2311.16471"
primary_category: motion-generation
tags: [motion-generation, multimodal, autoregressive, transformer, text, music, speech]
authors: [Zixiang Zhou, Yu Wan, Baoyuan Wang]
institutions: [Xiaobing.AI]
paper_url: "https://arxiv.org/abs/2311.16471"
project_url: "https://zixiangzhou916.github.io/UDE-2/"
github_url: "https://github.com/zixiangzhou916/UDE-2"
video_url: null
open_source: {code: partial, training_code: "no", inference_code: partial, model_weights: full, dataset: "no", robot_deployment: "no"}
open_source_checked: 2026-09-03
robots: []
inputs: [text, music, speech, auxiliary conditions]
outputs: [torso motion, hand motion, full-body motion]
read_status: read
reproduce_status: not-started
local_materials: []
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0025｜UDE-2：多模态、多身体部位人体动作合成统一框架

*A Unified Framework for Multimodal, Multi-Part Human Motion Synthesis*

[论文](https://arxiv.org/abs/2311.16471) · [项目页](https://zixiangzhou916.github.io/UDE-2/) · [官方代码](https://github.com/zixiangzhou916/UDE-2)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Zixiang Zhou、Yu Wan、Baoyuan Wang
>
> **机构**：Xiaobing.AI
>
> **论文时间**：2023-11-28
>
> **期刊 / 会议**：arXiv preprint arXiv:2311.16471
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **自回归** · **Transformer** · **文本** · **音乐** · **语音**
>
> **阅读状态**：已阅读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

## 本文贡献

- 将 UDE 从文本/音乐驱动身体扩展到文本、音乐、语音三模态和躯干、手部等多身体部位。
- 为不同身体部位分别学习离散码本，并设计分层 torso VQ-VAE，将局部姿态解码、全局轨迹估计和全局细化拆成两阶段。
- 以 CLIP、MTR、HuBERT 编码条件，统一预测部位专用动作 token，并用语义增强和语义感知采样平衡一致性与多样性。

## 研究问题

全身动作各部位频率和条件不同：语音强约束上身/手势，音乐约束整体节奏，文本提供片段语义。单一码本容易让大幅躯干动作淹没手部细节，完全分开又难保持协调。UDE-2 通过部位码本和共享条件到 token 框架折中。

## 原论文重点图

![UDE-2 多模态多部位总览](figures/key-figure.png)

**图 1：UDE-2 支持文本、音乐和语音驱动不同身体部位（原论文 Figure 1 所在页）。** 条件先进入预训练模态编码器，再由统一序列模型选择对应部位码本，最后分层重建连续全身动作。

## 研究方法详细解读

### 总体流程：按身体部位量化，再统一条件生成

UDE-2 先分别训练躯干、左手和右手动作 tokenizer，把不同运动尺度压成独立词表；文本、音乐和语音由各自预训练 encoder 提取，再经 adapter 进入共享 Transformer encoder；base causal decoder 读取条件和历史动作 token，各部位/模态 head 预测下一 token。预测码按部位送回相应 decoder，躯干恢复根轨迹与身体，手部恢复精细手势，最后拼为全身动作。统一的是条件—动作建模骨干，不是把所有身体部位强行塞进一个码本。

### 躯干与手部 tokenizer 的分工

手部关节幅度小、细节高，左右手各用专用 VQ；躯干表示根增量和身体旋转，采用层级 decoder：先恢复局部姿态并积分得到粗全局运动，再用一维 U-Net 细化全局位置。训练损失同时覆盖局部、子全局和全局坐标，防止只在局部旋转准确却让根漂移。检测到不活跃码时，从高使用率码加噪重新初始化，提升码本覆盖；各 tokenizer 稳定后冻结，为语言模型提供固定目标。

### 三类条件编码与共享 Transformer

文本使用 CLIP，音乐使用 MTR，语音使用 HuBERT；adapter 将不同长度和维度对齐到共享 hidden space，额外的 persona、身体部位或任务信息以可学习 embedding 附加。Transformer encoder 双向建模条件，causal decoder 依据已生成动作码预测下一码；base decoder 共享通用时序，输出 head 按部位和模态选择对应词表，避免从左手词表采样出躯干 token。不同模态数据可以分批训练而复用动作语法。

### 语义增强为什么位于 latent 层

冻结动作 autoencoder 将真值动作编码成连续语义向量，条件 encoder 的 pooled 表示被要求与之保持较高余弦相似；这项辅助损失直接拉近“说了什么/音乐表达什么”与“动作整体是什么”，弥补纯下一 token 交叉熵偏重局部频率的问题。它不替代 token 监督，因为 pooled 对齐无法约束准确顺序、节拍或手指细节，只作为条件空间的全局正则。

### 训练顺序与联合目标

第一阶段分别训练三个 tokenizer，检查重建、根积分和码本利用率；第二阶段冻结 tokenizer/预训练条件 encoder 的既定部分，训练 adapter、共享 encoder–decoder 和输出 heads，最小化各部位 token 交叉熵及语义对齐；多模态 batch 通过任务/部位 embedding 路由。最后可联合微调条件映射，但保持动作词表不漂移，否则旧 head 和 decoder 的索引语义会失配。

### 语义感知采样与完整动作恢复

自回归推理时先得到 top 候选 token，再依据候选码 embedding 与条件语义的距离重新加权概率，在“最高语言模型概率”和“全局语义一致”之间调节；随后左右手和躯干序列分别解码并按共同时间轴合并。该采样能纠正局部高频 token 对语义的忽略，也可能牺牲多样性；权重、温度和三个序列的结束时刻是复现关键。

### 适用边界

CLIP/MTR/HuBERT 的域偏移会直接影响文本、音乐和语音条件，部位分解也不自动保证双手与躯干接触一致。UDE-2 输出人体动作，不含机器人动力学；用于机器人须处理手型/自由度映射、根坐标、时钟和低层控制，并重新验证整合后的自碰撞与接触。

## 实验结果与结论

论文在文本动作、音乐舞蹈与语音手势数据上验证统一生成。公开仓库提供 demo 与预训练权重，但 TODO 明确训练/评估代码未发布，因此只能称部分开源。

## 局限与复现提醒

- 分部位码本需要显式同步，否则手势与躯干可能相位不一致。
- 公开实现缺完整训练与评测脚本，无法仅凭 demo 复现论文表格。
- 不含机器人动力学或接触控制。

## 阅读与复现状态

- 阅读：已阅读论文、项目页和飞书方法整理。
- 资源：demo/权重可得，训练评估代码未发布。
- 运行：未执行 demo。

## 参考资料

- [arXiv](https://arxiv.org/abs/2311.16471)
- [项目页](https://zixiangzhou916.github.io/UDE-2/)
- [官方代码](https://github.com/zixiangzhou916/UDE-2)

## 更新记录

- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：新建条目，整理分部位量化、三模态编码与公开资源边界。
