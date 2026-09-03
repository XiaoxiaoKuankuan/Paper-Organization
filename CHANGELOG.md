# 变更日志

本文件记录知识库的实质性改动。日期采用北京时间，论文自身的细节变化同时记录在对应论文页末尾。

## 2026-09-03

### 初始化知识库框架

- 将空白工作区关联到 `XiaoxiaoKuankuan/Paper-Organization` 远程仓库并统一初始分支为 `main`；最初未执行提交或推送，随后根据用户长期授权完成首次提交与推送。
- 建立论文、项目、数据集、分类索引、主题、对比、模板、本地档案与维护文档目录。
- 建立永久 ID、单一主分类、受控标签、阅读/复现状态和分项开源状态规范。
- 新增自动索引与结构校验脚本，分类索引以论文 YAML 元数据为唯一数据源。
- 将 `local_archive/` 设置为本地档案层，防止论文原文、全文翻译和方法详解进入公开 Git 历史。

### 首批论文整理

- 新增 `P0001`—`P0012` 共 12 篇精读档案：Evolution of Humanoid Locomotion Control、GENMO、GenTrack、GigaBrain-WBC-0.5、HIL、HumanoidArena、InfiniteDance、OMG、PhyGile、RLPF、RoboPerform、SONIC。
- 每篇档案补充中英文题名、作者与单位、日期与出版信息、论文/项目/代码入口、分项开源状态、输入输出、方法框架、实验结论、局限、研究价值及阅读/复现状态。
- 用 Mermaid 重绘 12 篇论文的方法数据流，避免把论文原图直接提交到公开仓库；本地原文和精读文档保留在 Git 忽略的档案层。
- 将 26 份本地材料按永久 ID 归入 `local_archive/P0001`—`local_archive/P0012`；明确排除毕业生公寓意向登记材料等隐私文件。
- 核验 `2602.00401v1.pdf` 的题名为 ZEST，不将其误归为 RoboPerform；RoboPerform 使用实际原文 `Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control.pdf`。

### 代码与验证

- 新增 `scripts/library_common.py`：统一 YAML front matter 读取、分类与状态枚举、论文目录遍历和 Markdown 转义。
- 新增 `scripts/build_index.py`：从论文元数据生成首页统计、最近更新、论文总索引和八个分类页，支持 `--check` 防止生成内容过期。
- 新增 `scripts/validate_library.py`：检查永久 ID、必填字段、主分类、受控标签、URL、分项开源状态、本地材料路径和公开 Markdown 相对链接，支持本机严格模式。
- 新增 GitHub Actions 校验流程与 PyYAML 依赖声明；代码文件均包含中文模块说明，所有实现保持本地档案只读。
- 修正 YAML 1.1 会把未加引号的 `no` 解析为布尔值的问题，将开源状态统一保存为字符串 `"no"`。
- 统一文本文件结尾为单个换行，并修正首页生成器，防止后续重建再次产生文件尾空白行。

### Git 工作流授权

- 记录用户长期授权：本仓库每次修改完成并通过必要验证后，默认创建提交并推送到当前分支，无需逐次询问。
- 明确提交说明、变更日志、代码注释和交付描述均使用中文；合并、变基、强制推送等历史改写操作不包含在默认授权内。
