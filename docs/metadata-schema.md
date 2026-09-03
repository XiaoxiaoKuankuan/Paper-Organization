# 元数据规范

论文 YAML front matter 是自动索引的唯一数据源。

## 必填字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | 字符串 | 与目录前缀一致，如 `P0001` |
| `title_en` / `title_zh` | 字符串 | 中英文题目；无官方中文名时使用忠实译名 |
| `year` | 整数 | 首次公开年份 |
| `date` | 日期或 `null` | 可核验的首次公开日期 |
| `venue` | 字符串 | 会议、期刊或 arXiv |
| `primary_category` | 枚举 | 八个主分类之一 |
| `tags` | 字符串列表 | 只能来自 `TAGS.md` |
| `authors` / `institutions` | 列表 | 按一手来源记录 |
| `read_status` | 枚举 | `unread` / `skimmed` / `read` / `deep-read` |
| `reproduce_status` | 枚举 | 见 `AGENTS.md` |
| `created` / `updated` | 日期 | 档案创建和最后更新日期 |

## URL 与开源状态

`paper_url`、`project_url`、`github_url`、`video_url` 使用官方 HTTPS 链接或 `null`。`open_source` 必须拆分为：

- `code`
- `training_code`
- `inference_code`
- `model_weights`
- `dataset`
- `robot_deployment`

每项只允许 `full`、`partial`、`no`、`unknown`，并使用 `open_source_checked` 记录核验日期。

## 本地材料

`local_materials` 是仓库根目录下的相对路径列表，统一指向 `local_archive/<ID>/`。这些文件存在于本机但不会被 Git 跟踪；使用 `--strict-local` 可检查路径是否存在。
