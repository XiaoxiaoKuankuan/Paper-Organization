# 重定向与统一表示对比

| 路线 | 输入 → 输出 | 核心机制 | 是否考虑机器人动力学 | 代表条目 |
|---|---|---|---:|---|
| 人体模型统一层 | SMPL/MHR/Anny/posed vertices → SOMA | 拓扑、骨架、姿态三层抽象 | 否 | [SOMA / GEM-X](../papers/P0016-soma-gem-x/README.md) |
| 优化式 Human→Robot | SMPL 动作 → G1 参考 | 形态映射 + 运动学优化 | 间接，由后续 tracker 反馈 | [RLPF](../papers/P0010-rlpf/README.md) |
| 数据构建期 GMR | 多源人体动作 → 125D G1 动作 | 清洗、GMR、仿真过滤 | 是，过滤阶段 | [OMG](../papers/P0008-omg/README.md) |
| 机器人原生生成 | 文本 → 机器人状态 | 训练时直接学习 robot-native 表示 | 通过 prefix/tracker 验证 | [PhyGile](../papers/P0009-phygile/README.md)、[GenTrack](../papers/P0003-gentrack/README.md) |

统一人体模型解决的是表示兼容，Human→Robot 重定向解决的是形态与运动学映射，GMT 解决的是闭环动力学执行；三者不能互相替代。
