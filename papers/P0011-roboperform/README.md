<!--
---
id: P0011
title_en: "Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control"
title_zh: "你会即兴表演吗？通过音频控制实现富有表现力的人形机器人运动"
year: 2026
date: 2025-12-29
venue: "CVPR 2026 Highlight"
primary_category: motion-generation
tags:
  - motion-generation
  - whole-body-control
  - audio
  - music
  - diffusion
  - distillation
  - motion-prior
  - g1
  - real-time
  - sim2real
authors:
  - Zhe Li
  - Cheng Chi
  - Yangyang Wei
  - Boan Zhu
  - Tao Huang
  - Zhenguo Sun
  - Yibo Peng
  - Pengwei Wang
  - Zhongyuan Wang
  - Fangzhou Liu
  - Chang Xu
  - Shanghang Zhang
institutions:
  - Beijing Academy of Artificial Intelligence
  - University of Sydney
  - Harbin Institute of Technology
  - Hong Kong University of Science and Technology
  - Shanghai Jiao Tong University
  - Peking University
paper_url: "https://arxiv.org/abs/2512.23650"
project_url: "https://gentlefress.github.io/RoboPerform-proj/"
github_url: "https://github.com/gentlefress/RoboPerform"
video_url: null
open_source:
  code: full
  training_code: full
  inference_code: full
  model_weights: full
  dataset: full
  robot_deployment: full
open_source_checked: 2026-09-03
robots:
  - Unitree G1
inputs:
  - music audio
  - speech audio
  - high-level motion content
  - proprioceptive history
outputs:
  - 23D target joint positions
read_status: deep-read
reproduce_status: not-started
local_materials:
  - "local_archive/P0011/Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control.pdf"
  - "local_archive/P0011/RoboPerform_方法详解与全文中文翻译.docx"
created: 2026-09-03
updated: 2026-09-04
---
-->

# P0011｜RoboPerform：通过音频控制实现富有表现力的人形机器人运动

*Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control*

[论文](https://arxiv.org/abs/2512.23650) · [项目页](https://gentlefress.github.io/RoboPerform-proj/) · [官方代码](https://github.com/gentlefress/RoboPerform) · [方法详解与全文中文翻译](attachments/方法详解与全文中文翻译.docx)

## 基本信息

<!-- AUTO-BASIC-INFO:START -->
> **作者**：Zhe Li、Cheng Chi、Yangyang Wei、Boan Zhu、Tao Huang、Zhenguo Sun、Yibo Peng、Pengwei Wang、Zhongyuan Wang、Fangzhou Liu、Chang Xu、Shanghang Zhang
>
> **机构**：Beijing Academy of Artificial Intelligence、University of Sydney、Harbin Institute of Technology、Hong Kong University of Science and Technology、Shanghai Jiao Tong University、Peking University
>
> **论文时间**：2025-12-29
>
> **期刊 / 会议**：CVPR 2026 Highlight
>
> **主分类**：动作生成
>
> **重点标签**：**动作生成** · **全身控制** · **音频** · **音乐** · **扩散模型** · **蒸馏** · **运动先验** · **Unitree G1** · **实时** · **Sim2Real**
>
> **阅读状态**：已精读　·　**复现状态**：未开始
<!-- AUTO-BASIC-INFO:END -->

### 资料与开源说明

- 开源资源：官方仓库当前含训练、推理、数据/检查点入口、TensorRT 导出、MuJoCo sim2sim 与实机部署说明。

## 本文贡献

- 将“动作内容”和“音频风格”解耦：64D 内容潜变量指定要做什么，256D 音频潜变量表达音乐节拍或语音韵律，二者直接调制控制策略。
- 先用 ResMoE/ΔMoE 教师学习多分布可执行动作，再以 DAgger 风格蒸馏把物理控制知识传给音频条件扩散学生。
- 以四层 MLP 扩散策略、`x0` 预测和两步 DDIM 实现约 5.3 ms 推理，直接输出 23D G1 关节目标，并公开 TensorRT、MuJoCo sim2sim 与实机部署链路。

## 研究问题

常见音频驱动方案先生成完整人体动作，再重定向并跟踪，容易累积重建误差、增加延迟，并削弱音频与执行器之间的时序耦合。论文希望不显式重建人体动作，就能让机器人随音乐舞蹈或随语音生成伴随手势。

## 原论文重点图

![RoboPerform 教师—学生框架](figures/roboperform-framework.png)

**图 1：RoboPerform 总体方法（原论文框架图）。** 上支路先训练带混合专家的教师获得可执行控制分布；音频适配器用对比目标把音乐/语音节奏映射为风格特征；扩散学生联合内容、风格、本体状态和历史动作，经过两步 DDIM 直接给出关节目标。论文的“无需重定向”限定在学生在线推理，教师数据准备仍使用参考动作。

## 研究方法详细解读

RoboPerform 的核心不是“音频先生成一段人体动作，再让 G1 去模仿”，而是用一个强动作教师把物理控制能力蒸馏进音频条件学生。学生把任务内容与音频风格分开：固定内容说明是在跳舞还是演讲，逐帧音频潜变量决定节拍、韵律和表现方式，最终直接输出机器人关节目标。

### 1. 总体定位：它要解决什么问题

传统音频控制经历音频生人体动作、人体到机器人重定向和低层跟踪，误差与延迟逐级累积；直接拼接音频特征又不保证其中含有可用于控制的运动学信息。论文希望在部署端去掉显式人体动作与在线重定向，同时保留音乐节拍和语音韵律，并让学生在自己产生偏差的状态上仍能恢复。这里的“无重定向”只指最终学生链路，教师参考仍经过动作处理。

### 2. 整体训练流程：三条主线汇入一个学生

1. 将 FineDance/BEAT2 动作处理为 G1 参考，在 Isaac Gym 中用 PPO 训练具有嵌套条件专家的 ΔMoE 教师。
2. 用 Motion VAE 编码动作，训练 Transformer 音频适配器，通过 InfoNCE 把音频节奏对齐到动作潜空间。
3. 让当前学生在仿真中 rollout，在其真实访问状态上查询教师的 23 维最优关节目标，形成 DAgger 数据。
4. 学生同时读取本体历史、64 维内容 latent 和 256 维音频 latent，对带噪教师动作做 `x0` 去噪训练。
5. 部署只保留音频特征/适配器、内容提示和两步 DDIM 学生；教师、参考动作、重定向与特权 critic 全部移除。

### 3. 总体信息流：动作教师、音频对齐器与扩散学生

RoboPerform 先在重定向动作上训练能覆盖多动作域的 ΔMoE 教师，再训练音频—动作对齐器把原始音频映射到动作潜空间，最后用 DAgger 采集学生自己访问到的状态，由教师给出目标动作，训练音频条件扩散学生。部署只保留音频编码、内容提示和学生控制策略，学生直接产生 G1 关节目标，不再在线查询参考动作或运行重定向。所谓 retargeting-free 指这一最终在线链路，教师数据和训练监督仍依赖重定向参考。

### ΔMoE 教师的嵌套条件子空间

教师共享控制主干并设置四个按条件逐级扩展的专家：第一个学习无条件基础控制，后续依次加入更细的动作条件。最终动作不是简单加权四个独立专家，而是 `a=w1a1+Σwi(ai-ai-1)`，即门控组合相邻条件级别的残差增量；共性动作由低层专家承担，高层只修正特定风格，减少重复学习。actor 隐层约 `[768,512,128]`、critic 约 `[512,256,128]`，在 Isaac Gym 中按参考跟踪奖励用 PPO 训练，价值网络可用特权状态帮助估值。

### 音频适配器如何获得逐帧风格条件

论文先用 Motion VAE（9 层、4 头）把动作压缩为语义潜变量，再用 6 层、4 头 Transformer 音频适配器处理原始音频特征。训练时以 batch 内正确音频—动作对为正样本、其他配对为负样本，用 InfoNCE 将节拍、韵律和动作时间结构拉到同一空间。固定的内容 latent 表示“跳舞、说话”等粗语义，256 维逐帧音频 latent 表示具体风格和节奏；二者分工防止模型仅凭音频频谱猜错动作类别。

### 扩散学生的观测、结构与输出

学生组合 64 维内容 latent、256 维逐帧音频风格、本体状态和历史动作，并加入扩散时刻；AdaLN 将时间与条件调制到约三层、宽度 1,792 的主体 MLP。网络对带噪的 23 维关节位置目标做 `x0` 预测，而不是预测电机力矩；训练时随机噪声覆盖不同置信度，推理用两步 DDIM 迭代得到最终 PD 目标。扩散输出允许同一音频在相近状态下保留多样性，但低步数也要求学生在蒸馏数据上学到很强的去噪映射。

### DAgger 蒸馏为什么不可省略

如果只在教师访问的理想轨迹上做行为克隆，学生的微小误差会让本体状态逐步偏离数据分布。DAgger 让学生在仿真中用当前策略 rollout，记录其真实访问状态，再查询 ΔMoE 教师应采取的动作；新样本回到训练池反复更新扩散学生。教师因此提供物理稳定的纠偏标签，音频条件保证动作风格，学生则学会在自身误差分布上恢复，而不是仅重现离线关节序列。

### 推理、工程链与证据边界

在线音频经适配器形成逐帧条件，结合当前本体历史和内容提示进入两步 DDIM，论文报告策略计算约 5.3 ms，随后 23 维关节目标交给低层 PD。官方工程包含训练、离线推理、TensorRT 导出、MuJoCo sim2sim 与 G1 实机入口，说明系统链路公开；但接口可获得不等于本知识库已运行。复现时仍须核对机器人自由度、音频/控制时钟同步、动作缩放、PD 增益和导出精度。

## 实验结果与结论

实验覆盖 music-to-dance 与 speech-to-gesture，报告物理可行性、音频节拍/韵律对齐、动作多样性和推理效率方面相对两阶段方案的改善，并展示真实机器人舞者与主持人场景。结论应限定在论文任务分布与 G1 平台，不能直接外推为任意音频、任意机器人或硬件安全保证。

## 局限与复现提醒

- 优点：音频直接进入控制策略；舞蹈与伴随手势统一；低延迟；公开部署链路较完整。
- 局限：内容 latent 仍依赖上游运动先验；训练阶段需要教师和参考动作；长时稳定性、极端音频和人机共域安全仍需独立验证。

### 对个人研究的价值

它提供了 GENMO/OMG 之外更“端到端控制”的音乐接口，可用于比较“先生成轨迹再跟踪”和“音频直接调制策略”两类架构。接入自有系统时应核对 23D 关节顺序、控制频率、动作历史窗口、音频特征对齐以及 TensorRT 输入输出契约。

## 阅读与复现状态

- 阅读：已深读原文和方法详解/全文翻译，核对网络层数、潜变量与输出维度。
- 资源：已核验官方代码、数据/权重和部署入口。
- 运行：尚未执行离线音频推理或 MuJoCo sim2sim。
- 实机：未做独立安全验证。


## 参考资料

- [论文](https://arxiv.org/abs/2512.23650)
- [项目页](https://gentlefress.github.io/RoboPerform-proj/)
- [官方代码](https://github.com/gentlefress/RoboPerform)

## 更新记录

- 2026-09-04：按 ADAPT 式方法导读补充音频直控的核心定位、三阶段串联系统问题和五步教师—对齐器—DAgger 学生流程，明确“无重定向”的实际边界。
- 2026-09-03：依据原论文方法与训练章节，扩展总体流程、数据表征、模块信息流、训练目标、推理/部署及实现边界。
- 2026-09-03：补充正文基本信息卡，展示完整作者、机构、论文时间、期刊/会议、分类、标签与状态。
- 2026-09-03：创建精读档案；登记两份本地材料，核验正式 arXiv 编号及完整公开工程入口。
- 2026-09-03：纳入译解附件与原论文框架图，补充教师、音频适配器、Motion VAE 和扩散学生网络细节。
