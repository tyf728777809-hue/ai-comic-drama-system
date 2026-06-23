# V2 快速开始

## 1. 创建项目目录

```bash
mkdir -p project_data/projects/PROJECT_ID/series
mkdir -p project_data/projects/PROJECT_ID/episodes/ep01/{script,director,assets,seedance,music}
mkdir -p project_data/projects/PROJECT_ID/episodes/ep01/assets/images
```

## 2. 复制模板

```bash
cp templates/series/creative-thesis.template.yaml project_data/projects/PROJECT_ID/series/creative-thesis-v1.0.yaml
cp templates/episodes/epXX/script/script.template.yaml project_data/projects/PROJECT_ID/episodes/ep01/script/script-v1.0.yaml
cp templates/episodes/epXX/director/shot-design-table.template.yaml project_data/projects/PROJECT_ID/episodes/ep01/director/shot-design-table-v1.0.yaml
cp templates/episodes/epXX/assets/visual-style-bible.template.yaml project_data/projects/PROJECT_ID/episodes/ep01/assets/visual-style-bible-v1.0.yaml
cp templates/episodes/epXX/seedance/manual-generation-package.template.yaml project_data/projects/PROJECT_ID/episodes/ep01/seedance/manual-generation-package-v1.0.yaml
```

## 3. 让 Agent 补内容

按顺序调用：

1. `story-agent`
2. `director-agent`
3. `visual-asset-agent`
4. `seedance-package-agent`
5. `music-agent`

## 4. 校验

```bash
python3 tools/workflow_guard.py validate
python3 tools/workflow_guard.py status --project PROJECT_ID --episode ep01
```

`status` 会输出 `studio_status` 和 `shot_ledger`，用于判断下一步应该推进哪里。
