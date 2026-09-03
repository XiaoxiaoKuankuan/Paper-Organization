# 日常维护流程

## 新增论文

1. 执行 `git status --short`，确认不会覆盖已有工作。
2. 在现有档案中按题名、arXiv ID、DOI、项目页和 GitHub URL 查重。
3. 选择下一个未使用的 `Pxxxx`，复制 `templates/paper-template.md` 到 `papers/Pxxxx-short-name/README.md`。
4. 从原论文、补充材料、官方项目页与官方仓库核验元数据。
5. 原论文备份放在 `local_archive/Pxxxx/`；方法详解、个人全文翻译和左右对照材料放入论文目录的 `attachments/` 并建立正文链接。
6. 从原论文提取总览图、方法图和必要的关键结果图到 `figures/`，保留原论文图号并写中文图解，不使用自绘图代替。
7. 深读论文与已有讲解文档，完成“本文贡献”和“研究方法详细解读”；事实、材料解读与个人判断分开。
8. 在论文页和根 `CHANGELOG.md` 中记录本次更新。
9. 执行：

```bash
python3 scripts/sync_paper_info.py
python3 scripts/validate_library.py --strict-local
python3 scripts/build_index.py
python3 scripts/sync_paper_info.py --check
python3 scripts/build_index.py --check
git diff --check
```

## 更新开源状态

开源状态可能随时间变化。更新时访问官方项目页和官方仓库，修改对应分项与 `open_source_checked`，不要仅把“有仓库”写成“完整开源”。

## GPT/Codex 维护提示词

```text
请按仓库 AGENTS.md 维护知识库。先检查 Git 状态并查重；深读原论文与已有方法讲解/翻译材料，再以原论文、官方项目页和官方仓库核验元数据。未知项写 null，不得猜测。每篇论文只选一个主分类，重点标签只能来自 TAGS.md。隐藏 YAML 元数据，正文使用中文栏目；作者、机构、论文时间、期刊/会议必须写入 YAML，并运行 sync_paper_info.py 同步为正文无表格信息卡。把方法详解和个人翻译放进论文目录 attachments/，从原论文提取重点图到 figures/ 并写中文详解，不用自绘图替代。完成后更新论文页与 CHANGELOG.md，运行 sync_paper_info.py --check、validate_library.py --strict-local、build_index.py、build_index.py --check 和 git diff --check，并分别报告内容校验、索引校验与实际复现边界。
```
