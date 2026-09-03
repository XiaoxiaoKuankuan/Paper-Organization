# 动作跟踪与全身控制对比

| 方法 | 关键观测/命令 | 训练重点 | 环境/交互 | 论文硬件证据 | 主要边界 |
|---|---|---|---|---|---|
| [YAHMP 实证研究](../papers/P0014-what-matters-yahmp/README.md) | 参考位置/速度、10 步历史、本体状态 | 六类受控消融，单阶段 PPO | 手力随机化 | Unitree G1 | 结论依赖共同协议，不是跨平台常数 |
| [ZEST](../papers/P0015-zest/README.md) | 下一帧参考、本体状态 | 自适应 RSI、辅助 wrench 课程 | 动态多接触 | Atlas、G1、Spot | 依赖精确执行器/armature 建模 |
| [SONIC](../papers/P0012-sonic/README.md) | Robot/Human/Hybrid token | 数据、模型、算力缩放 | 多接口、平地为主 | Unitree G1 | 约 700 小时自有数据未完整公开 |
| [GigaBrain-WBC](../papers/P0004-gigabrain-wbc-0-5/README.md) | 本体、动作历史、未来行为 | PPO + 状态/GMM 世界模型头 | 支撑面、负载、指令 OOD | G1/L01 展示 | OOD 椭球不是形式化安全保证 |
| [HIL](../papers/P0005-hil/README.md) | 角色、场景、目标 | Tracking + 场景条件 AMP | 跑酷障碍 | 物理角色仿真 | 非真实人形机器人实验 |
| [GenTrack](../papers/P0003-gentrack/README.md) | 机器人原生参考 | 生成器/跟踪器跨轮共同演化 | 仿真平地动作 | 无 | 内部数据与代码未开放 |
| [PhyGile GMT](../papers/P0009-phygile/README.md) | 262D 参考/前缀 | 两阶段课程式 MoE | 高动态技能 | Unitree G1 展示 | 完整生成—跟踪链未全部开源 |

比较时至少固定机器人资产、关节顺序、参考动作集、控制频率、PD 增益、action scale、失败判据和仿真器；否则“成功率更高”无法归因到方法本身。
