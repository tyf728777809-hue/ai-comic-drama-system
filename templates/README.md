# V2 Starter YAML 模板

这里保存可复制到 `project_data/projects/{project_id}/...` 的 V2 起始模板。

模板只用于启动新项目，不是正式项目数据。复制后按文件名中的版本号保存，例如：

- `templates/series/creative-thesis.template.yaml`
- `templates/episodes/epXX/script/script.template.yaml`
- `templates/episodes/epXX/script/script-doctor-report.template.yaml`
- `templates/episodes/epXX/director/shot-design-table.template.yaml`
- `templates/episodes/epXX/assets/visual-style-bible.template.yaml`
- `templates/episodes/epXX/assets/asset-index.template.yaml`
- `templates/episodes/epXX/seedance/manual-generation-package.template.yaml`
- `templates/episodes/epXX/music/suno-music-task-card.template.yaml`

日常校验：

```bash
python3 tools/workflow_guard.py validate
python3 tools/workflow_guard.py status --project NEW --episode ep01
```
