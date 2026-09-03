# 人形机器人舞蹈：从音乐到硬件的完整链路

当前馆藏可将技术路线拆成四层：

1. **数据与人体生成**：InfiniteDance/OpenDance 侧重野外舞蹈数据和音乐一致性；GENMO、AnyMo、OmniMotion-X 进一步统一文本、音乐、视频或轨迹条件。
2. **机器人原生参考**：OMG、PhyGile 直接生成 G1/机器人表示；RLPF、GenTrack 用 tracker 的物理反馈对齐生成分布。
3. **低层动作跟踪**：SONIC、YAHMP、ZEST 将参考动作变成关节目标并处理扰动、执行器和 sim-to-real。
4. **音频直接控制**：RoboPerform 省去在线人体动作重建，让音乐/语音 latent 直接调制扩散控制策略。

## 关键条目

- 数据与长时音乐建模：[InfiniteDance](../papers/P0007-infinitedance/README.md)、[OpenDance](../papers/P0035-opendance/README.md)、[TM2D](../papers/P0023-tm2d/README.md)。
- 多模态人体动作底座：[GENMO](../papers/P0002-genmo/README.md)、[AnyMo](../papers/P0021-anymo/README.md)、[VersatileMotion](../papers/P0033-versatilemotion/README.md)。
- 机器人原生生成：[OMG](../papers/P0008-omg/README.md)、[PhyGile](../papers/P0009-phygile/README.md)。
- 实时执行：[RoboPerform](../papers/P0011-roboperform/README.md)、[SONIC](../papers/P0012-sonic/README.md)、[TextOp](../papers/P0038-textop/README.md)。

## 数据与接口核对项

- 人体/机器人骨架、关节名称和顺序；SMPL/SMPL-X/SOMA 与机器人资产的映射。
- 原始 FPS、生成 FPS、控制 FPS以及重采样；旋转插值与速度/接触重算。
- 根坐标、朝向、相对/绝对轨迹、音乐特征时间戳和动作窗口对齐。
- 生成质量、节拍一致性、物理可执行性、跟踪误差、跌倒率和硬件安全分开评估。
