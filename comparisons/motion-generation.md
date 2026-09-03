# 动作生成方法对比

下表用于判断“条件如何进入模型、输出属于人体还是机器人、物理反馈位于哪里”，不把不同数据集上的 FID 直接横向比较。

| 方法 | 条件 | 核心表示/生成范式 | 流式 | 机器人原生 | 物理可行性来源 |
|---|---|---|---:|---:|---|
| [GENMO](../papers/P0002-genmo/README.md) | 视频、2D、文本、音乐、关键帧 | 151D SMPL，扩散 Transformer，估计/生成双模式 | 否 | 否 | 无；需重定向与跟踪 |
| [InfiniteDance](../papers/P0007-infinitedance/README.md) | 音乐、检索动作 | SMPL-X + RVQ-VAE，ChoreoLLaMA 自回归 | 长时离线 | 否 | 数据阶段物理模仿 + FRDM |
| [OMG](../papers/P0008-omg/README.md) | 文本、音频、人体参考、历史 | 125D G1，DiT `x`-prediction | 是 | 是 | MuJoCo 数据过滤 + HoloMotion |
| [PhyGile](../papers/P0009-phygile/README.md) | 文本、已验证动作前缀 | 262D robot-native，TP-MoE 扩散 | 分段 | 是 | Physics-Prefix + GMT 验证 |
| [RLPF](../papers/P0010-rlpf/README.md) | 文本 | 离散人体动作 token，LLaMA + GRPO | 否 | 否 | SMPL→G1→冻结 tracker 反馈 |
| [RoboPerform](../papers/P0011-roboperform/README.md) | 音乐/语音、内容 latent、本体状态 | 两步 DDIM，直接输出 23D 关节目标 | 是 | 是 | RL 教师蒸馏到扩散学生 |
| [Kimodo](../papers/P0017-kimodo/README.md) | 文本、关键帧、关节、2D 路径 | SOMA，root/body 两阶段扩散 | 否 | 否 | 运动学约束，不含动力学 |
| [MotionBricks](../papers/P0018-motionbricks/README.md) | 速度、风格、关键帧、交互原语 | 模块化动作 latent + Smart Primitives | 是 | 生成参考 | G1 端依赖外部跟踪器 |
| [ARDY](../papers/P0019-ardy/README.md) | 在线文本、关键帧、路径、历史 | 显式根 + 身体 latent，4 步自回归扩散 | 是 | 否 | 无；人体动作域 |
| [AnyMo](../papers/P0021-anymo/README.md) | 文本、语音、音乐、轨迹任意组合 | Residual FSQ + 掩码 Transformer | 否 | 否 | 无；互联网动作筛选 |
| [OmniMotion-X](../papers/P0036-omnimotion-x/README.md) | 文本、音乐、语音、参考、空间约束 | SMPL-X，分块自回归 DiT | 是 | 否 | 无；需后续控制 |
| [TextOp](../papers/P0038-textop/README.md) | 流式文本、动作历史 | 短窗自回归扩散 + 低层 tracker | 是 | 参考层 | 闭环跟踪策略 |

## 选型提示

- 需要视频/文本/音乐统一人体先验：优先比较 GENMO、AnyMo、VersatileMotion、OmniMotion-X。
- 需要直接生成机器人轨迹：重点比较 OMG、PhyGile，以及 GenTrack 的共同后训练。
- 需要音乐/语音直接进入实时控制：重点比较 RoboPerform 与“上游生成 + SONIC/GMT”两阶段方案。
- 需要运行中修改提示：ARDY 与 TextOp 都是短窗自回归，但 TextOp 明确包含机器人低层执行。
