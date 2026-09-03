<!--
---
id: P0008
title_en: "OMG: Omni-Modal Motion Generation for Generalist Humanoid Control"
title_zh: "OMG：面向通用人形机器人控制的全模态动作生成"
year: 2026
date: 2026-06-09
venue: "arXiv preprint arXiv:2606.10340"
primary_category: motion-generation
tags:
  - motion-generation
  - multimodal
  - diffusion
  - transformer
  - text
  - audio
  - music
  - g1
  - real-time
authors:
  - Siqiao Huang
  - Kun-Ying Lee
  - Dongming Qiao
  - Guanqi He
  - Zhenyu Wang
  - Yitang Li
  - Shaoting Zhu
  - Hang Zhao
institutions:
  - Tsinghua University
paper_url: "https://arxiv.org/abs/2606.10340"
project_url: "https://tsinghua-mars-lab.github.io/OMG/"
github_url: "https://github.com/Tsinghua-MARS-Lab/OMG"
video_url: null
open_source:
  code: full
  training_code: partial
  inference_code: partial
  model_weights: partial
  dataset: full
  robot_deployment: partial
open_source_checked: 2026-09-03
robots:
  - Unitree G1
inputs:
  - language
  - audio
  - human reference motion
  - motion history
outputs:
  - robot-native future motion
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0008/OMG：Omni-Modal Motion Generation for.pdf"
  - "local_archive/P0008/OMG-leftToRight.pdf"
  - "local_archive/P0008/OMG_论文全文翻译与方法框架详解.docx"
created: 2026-09-03
updated: 2026-09-03
---
-->

# P0008｜OMG：面向通用人形机器人控制的全模态动作生成

*OMG: Omni-Modal Motion Generation for Generalist Humanoid Control*

[论文](https://arxiv.org/abs/2606.10340) · [项目页](https://tsinghua-mars-lab.github.io/OMG/) · [官方代码](https://github.com/Tsinghua-MARS-Lab/OMG) · [全文翻译与方法框架详解](attachments/全文翻译与方法框架详解.docx) · [中英左右对照全文](attachments/中英左右对照全文.pdf)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Siqiao Huang、Kun-Ying Lee、Dongming Qiao、Guanqi He、Zhenyu Wang、Yitang Li、Shaoting Zhu、Hang Zhao
>
> **机构**：Tsinghua University
>
> **论文时间**：2026-06-09
>
> **期刊 / 会议**：arXiv preprint arXiv:2606.10340
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **多模态** · **扩散模型** · **Transformer** · **文本** · **音频** · **音乐** · **Unitree G1** · **实时**
>
> **阅读状态**：已精读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

### 资料与开源说明

- 开源资源：官方仓库当前含数据、训练、生成、跟踪、benchmark 与 G1 实时部署文档，采用 MIT License。

## 本文贡献

- 构建 1174.66 小时 OMG-Data，把文本、音频、人体参考等异构来源清洗、GMR 重定向、VLM 标注并用 MuJoCo 跟踪结果过滤到统一 G1 空间。
- 提出直接在 125D 机器人动作空间做 `x`-prediction 的共享 OMG-DiT；语言/历史用交叉注意力，音频/人体参考用逐帧 FiLM。
- 将生成器作为高层“动作大脑”接入 HoloMotion 跟踪器，支持单模态、未联合训练过的模态组合和实时 G1 部署；新条件以零初始化适配器接入以保留先验。

## 研究问题

通用跟踪器能执行参考动作，却不能自行把高层多模态意图变成参考；人体动作数据又高度异构，缺少统一机器人空间和物理筛选。论文要构建可扩展的动作生成“大脑”，放在反应式跟踪“小脑”之上。

## 原论文重点图

![OMG 系统总览](figures/omg-overview.png)

**图 1：全模态生成—控制系统（原论文 Figure 1）。** 不同条件统一驱动机器人原生动作生成器，未来参考再由 HoloMotion 闭环跟踪。生成和控制仍是两个模型，部署必须保证表示、帧率、关节顺序与历史窗口一致。

![OMG 数据管线](figures/omg-data.png)

**图 2：OMG-Data 构建（原论文数据图）。** 原始人体、舞蹈和语音动作经清洗、分段、GMR、语言标注与物理过滤统一为 G1 轨迹；1174.66 小时是模态覆盖有重叠的总库口径。

![OMG-DiT](figures/omg-dit.png)

**图 3：OMG-DiT 条件注入（原论文方法图）。** 语言与动作历史作为全局 token 经交叉注意力进入主干；音频与人体关键点逐帧对齐，因此使用 FiLM 调制。随机丢模态支持 classifier-free guidance。

## 研究方法详细解读

### 数据、筛选与动作表征

OMG-Data 将异构来源清洗、分段、重定向、语言标注和仿真过滤后统一为 30 Hz、1174.66 小时 G1 动作；文本、人体参考、音频覆盖时长相互重叠，不能相加。每帧 125D 动作由规范化根位置/旋转、关节角和机器人连杆位置组成。过滤把低高度、过大倾角及其持续组合判为跌倒，因此得到的是“在指定跟踪器/仿真配置下可执行”的分布，并非平台无关的绝对物理可行性。

### 网络与训练

OMG-DiT 直接在动作空间做 `x`-prediction，不额外依赖 VAE/tokenizer。语言与历史作为全局上下文经交叉注意力注入，35D 音频和 66D 人体关键点经逐帧 FiLM 注入；模态随机丢弃支持 classifier-free guidance。新模态通过零初始化适配器接入，减少对已有动作先验的破坏。

### 推理与部署

生成器根据最近历史与当前条件预测未来窗口，支持文本、音频、人体参考和训练中未见的文本+音频组合。官方部署把 GPU 工作站上的实时生成服务器、G1 Orin 上的 HoloMotion 跟踪模型与实机桥接分开运行。

## 实验结果与结论

OMG-XL 在文本任务上报告 FID 6.03（论文缩放口径）和 R@1 65.43%；音频任务两种规模跌倒率为 0；人体参考条件下 MPJPE 18.84 mm。50M/300M/500M 模型显示随容量扩大误差下降；在新文本分布和 Pico 关键点条件上，预训练模型比同数据量从头训练更具样本效率。

## 局限与复现提醒

- 训练数据以平地为主；生成与跟踪仍模块化，未用真实执行反馈联合适配；更大生成器并非所有跟踪/限位指标都同步改善。
- 官方仓库有主要训练、生成和部署代码，但完整 GMR 预处理与 HoloMotion tracker 权重并未全部开放；这会阻断从原始人体数据到同口径实机部署的完整复现。

### 对个人研究的价值

OMG 是“多模态动作生成大脑 + GMT 小脑”的直接工程参考，可与 GENMO（人体动作）和 SONIC（跟踪控制）形成清晰分层；实际使用必须锁定 125D 表征、30 Hz 数据、跟踪器接口和部署协议。

## 阅读与复现状态

- 阅读：已深读原文、左右对照和方法详解。
- 资源：已核验官方仓库公开边界；GMR 预处理和跟踪器资源并非全部齐备。
- 运行：本知识库尚未执行官方 Demo 或训练。
- 实机：未做独立安全验证。


## 参考资料

- [论文](https://arxiv.org/abs/2606.10340)
- [项目页](https://tsinghua-mars-lab.github.io/OMG/)
- [官方代码](https://github.com/Tsinghua-MARS-Lab/OMG)

## 更新记录

- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：创建精读档案；登记三份本地材料并核验当前完整开源与部署入口。
- 2026-09-03：纳入两份译解附件与三张原论文重点图；修正 GMR/跟踪权重开源边界，扩展数据筛选、条件注入和部署解读。
