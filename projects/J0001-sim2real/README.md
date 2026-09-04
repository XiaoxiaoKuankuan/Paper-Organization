---
id: J0001
name: "EGalahad/sim2real：多策略人形机器人统一部署运行时"
repository_url: "https://github.com/EGalahad/sim2real"
paper_ids:
  - P0012
  - P0040
  - P0042
  - P0043
  - P0044
  - P0045
  - P0046
license: unknown
created: 2026-09-04
updated: 2026-09-04
---

# J0001｜EGalahad/sim2real：多策略人形机器人统一部署运行时

[官方仓库](https://github.com/EGalahad/sim2real) · [在线文档](https://egalahad.github.io/sim2real/)

## 功能与定位

`EGalahad/sim2real` 不是一篇新论文，也不是把所有控制方法重新训练成同一策略；它是面向 Unitree G1 的公共推理与部署运行时。项目把“策略特有的观测构造”封装为 Python 观测类和 YAML，把模型推理、参考动作读取、MuJoCo 后端、Pico 遥操作和真实机器人 I/O 作为共享组件。这样接入新 tracker 时主要新增观测适配与模型配置，不必复制整套 sim2real 主循环。

## 输入与输出

- 输入源可包括离线机器人动作、实时 Pico/VR 参考以及策略所需的本体状态、参考窗口、历史缓存和潜变量。
- 每个策略由 `policy.yaml` 规定模型路径、观测字段、历史/前视长度、归一化、动作缩放与关节映射。
- 推理输出通常是 G1 关节目标；运行时再通过 MuJoCo 或物理机器人后端送入相应低层控制接口。
- 该公共外形不表示各策略观测相同：SONIC、HoloMotion、TeleopIT、BFM-Zero 等仍有不同维度、前视、状态定义和 checkpoint 契约。

## 网络、数据与训练

此仓库以模型适配、评测和部署为主，不是各论文的权威训练仓库。MimicLite 的训练位于 `EGalahad/mimic-lite`，HEFT 位于 `Axellwppr/motion_tracking`，HoloMotion、SONIC、Teleopit、Humanoid-GPT 与 BFM-Zero 也各自维护原始实现。仓库分发或引用转换后的 checkpoint；要复现实验训练，应回到原项目核对数据、资产、网络、奖励和导出流程，不能从部署 YAML 反推完整训练配置。

## 推理与实时能力

运行时将策略推理与机器人 I/O 解耦，通过统一生命周期完成模型加载、观测缓冲、参考更新、动作解码和后端切换。不同策略的 motion-lookahead 延迟按 50 Hz 参考契约分别统计，不能只比较单次 ONNX 前向时间。离线动作回放、Pico 遥操作、MuJoCo sim2sim 与 G1 实机共用部分主循环，有助于减少“仿真脚本和实机脚本分别漂移”，但 sim2sim 通过仍不构成硬件安全证明。

## 当前支持的策略族

截至 2026-09-04，官方 README 的适配/分发列表包含：

| 序号 | 策略族 | 配置入口或版本说明 | 本知识库关联 |
|---:|---|---|---|
| 1 | MimicLite-ROA | 最新 `16×16384` PPO-ROA student | [P0040](../../papers/P0040-mimiclite/README.md) |
| 2 | MimicLite-PPO | 最新 `16×16384` Huge PPO | [P0040](../../papers/P0040-mimiclite/README.md) |
| 3 | HEFT | PMG 与负载适配变体 | [P0042](../../papers/P0042-heft/README.md) |
| 4 | HoloMotion v1.4.0 | 使用官方未修改 ONNX | [P0043](../../papers/P0043-holomotion-1/README.md) |
| 5 | SONIC release | G1 与 SMPL encoder 变体 | [P0012](../../papers/P0012-sonic/README.md) |
| 6 | SONIC low-latency | 低前视 G1/SMPL 变体 | [P0012](../../papers/P0012-sonic/README.md) |
| 7 | SONIC v1.1 | heading-normalized reference orientation | [P0012](../../papers/P0012-sonic/README.md) |
| 8 | GRIT v0.0.1 | 九帧参考与十帧本体历史 | 待建立论文档案 |
| 9 | ScaleBFM XL | Hugging Face ONNX 导出 | 待建立论文档案 |
| 10 | ScaleBFM M | Hugging Face ONNX 导出 | 待建立论文档案 |
| 11 | BFM-Zero | latent-conditioned motion tracker | [P0046](../../papers/P0046-bfm-zero/README.md) |
| 12 | TeleopIT | TeleopIT policy wrapper | [P0044](../../papers/P0044-teleopit/README.md) |
| 13 | Humanoid-GPT | Humanoid-GPT policy wrapper | [P0045](../../papers/P0045-humanoid-gpt/README.md) |
| 14 | TWIST2 | TWIST2 policy wrapper | 待建立论文档案 |

列表是当前仓库适配状态，不等于每个策略的训练代码、论文数据和所有模型权重都由本仓库完整发布。

## 支持的机器人与仿真器

- 机器人后端：以 Unitree G1 为主，物理接口与策略关节/观测配置配套。
- 仿真后端：MuJoCo，用于相同部署路径下的策略加载和 sim2sim 评测。
- 输入设备：提供 Pico 遥操作教程和相关参考流接入。
- 模型运行：主要使用 ONNX/ONNX Runtime 等导出模型；个别策略模型来自原项目或 Hugging Face。

## 安装与关键文件

官方用法要求先准备仓库根目录下的 `checkpoints/` 与 `third_party/`，再从策略目录选择配套 `policy.yaml`。接入或排查时应同时核对：

1. YAML 指向的精确 ONNX 与版本；
2. 观测类输出维度、字段顺序、缩放和历史/前视长度；
3. G1 MJCF/URDF、默认姿态、关节名称与动作映射；
4. 参考数据频率、根坐标与四元数约定；
5. MuJoCo 与真机后端的 PD、限位、急停和通信频率。

仅替换模型文件而沿用另一个策略的 YAML，通常会造成输入维度错误，或更危险的“维度相同但字段语义不同”。

## 已验证能力

本知识库本次只核验了官方 README、配置入口和当前策略列表，没有安装依赖、下载 checkpoint、运行 MuJoCo、连接 Pico 或启动真实机器人。上表表示上游仓库宣称/提供的适配范围，不是本地复现勾选；因此项目页不记录 Demo、sim2sim 或实机“已验证”。

## 本地修改与当前问题

- 未对 `EGalahad/sim2real` 源码做本地修改，本页只是知识库项目档案。
- GitHub API 当前未识别出仓库许可证，README 也未给出明确统一许可；本页登记为 `unknown`。各 checkpoint、第三方仓库和数据仍需分别核对许可。
- 策略列表更新很快，后续维护应按精确发布日期/commit 核验，避免把新 wrapper 的观测契约写回旧论文版本。

## 关联论文、项目与数据集

- [P0040 MimicLite](../../papers/P0040-mimiclite/README.md)：项目总入口将本仓库指定为统一部署 runtime。
- [P0042 HEFT](../../papers/P0042-heft/README.md)：本仓库适配 PMG 与负载相关 checkpoint。
- [P0043 HoloMotion-1](../../papers/P0043-holomotion-1/README.md)：使用官方 ONNX，观测 wrapper 由本仓库适配。
- [P0012 SONIC](../../papers/P0012-sonic/README.md)：包含 release、low-latency 与 v1.1 三套不同契约。
- [P0044 Teleopit](../../papers/P0044-teleopit/README.md)、[P0045 Humanoid-GPT](../../papers/P0045-humanoid-gpt/README.md)、[P0046 BFM-Zero](../../papers/P0046-bfm-zero/README.md)：均有独立 wrapper，不应共享错误观测配置。

## 更新日志

- 2026-09-04：创建 J0001 项目档案；核验 14 个当前策略条目、统一观测/YAML 设计、MuJoCo/Pico/G1 边界和许可证未知状态，并关联已建论文档案。
