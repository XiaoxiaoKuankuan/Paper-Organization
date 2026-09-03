# 日常维护流程

## 新增论文

1. 执行 `git status --short`，确认不会覆盖已有工作。
2. 在现有档案中按题名、arXiv ID、DOI、项目页和 GitHub URL 查重。
3. 选择下一个未使用的 `Pxxxx`，复制 `templates/paper-template.md` 到 `papers/Pxxxx-short-name/README.md`。
4. 从原论文、补充材料、官方项目页与官方仓库核验元数据。
5. 复制本地原文和翻译到 `local_archive/Pxxxx/`，在论文 YAML 中登记相对路径。
6. 依据材料撰写精读内容；事实、材料解读与个人判断分开。
7. 在论文页和根 `CHANGELOG.md` 中记录本次更新。
8. 执行：

```bash
python3 scripts/validate_library.py --strict-local
python3 scripts/build_index.py
python3 scripts/build_index.py --check
git diff --check
```

## 更新开源状态

开源状态可能随时间变化。更新时访问官方项目页和官方仓库，修改对应分项与 `open_source_checked`，不要仅把“有仓库”写成“完整开源”。

## GPT/Codex 维护提示词

```text
请按仓库 AGENTS.md 维护知识库。先检查 Git 状态并查重；读取本地材料后，以原论文、官方项目页和官方仓库核验元数据。未知项写 null，不得猜测。每篇论文只选一个主分类，标签只能来自 TAGS.md。受版权约束的原文和完整翻译只放 local_archive，不提交 Git。完成后更新论文页与 CHANGELOG.md，运行 validate_library.py --strict-local、build_index.py、build_index.py --check 和 git diff --check，并分别报告内容校验、索引校验与实际复现边界。
```
