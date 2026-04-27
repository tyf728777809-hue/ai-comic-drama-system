# Templates

这里放的是可直接复制的 starter YAML，不是 schema。

使用方式：

1. 从 `templates/` 复制对应文件到 `project_data/`
2. 去掉 `.template`
3. 改成正式版本名，例如 `creative-bible-v1.0.yaml`
4. 填内容后跑 `python3 tools/workflow_guard.py validate`

## 模板分组

- `templates/series/`：系列级创意和剧本阶段文件
- `templates/reviews/`：业务 / 合规审核报告模板
- `templates/episodes/epXX/`：单集级剧本、segments、assets、videos、orchestration

## 推荐起手顺序

1. `series/creative-bible.template.yaml`
2. `reviews/business-review-report.template.yaml`
3. `reviews/compliance-report.template.yaml`
4. `series/synopsis.template.yaml`
5. `series/episode-plan.template.yaml`
6. `episodes/epXX/script/script.template.yaml`
7. `episodes/epXX/segments/segments.template.yaml`
