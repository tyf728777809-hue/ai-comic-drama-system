# Quick Start

这份文档只讲怎么把一个项目真正开起来。

## 0. 先确认定位

这套仓库的推荐用法是：

1. 你决定项目方向和关键取舍
2. 助手按 `.agents/` 里的角色和方法包推进
3. 关键结果必须落成正式 YAML
4. `workflow_guard.py` 负责校验和状态判断

不要把它当全自动生产器来用。

## 1. 新项目起步

先复制系列级模板：

- [templates/series/creative-bible.template.yaml](../templates/series/creative-bible.template.yaml)
- [templates/reviews/business-review-report.template.yaml](../templates/reviews/business-review-report.template.yaml)
- [templates/reviews/compliance-report.template.yaml](../templates/reviews/compliance-report.template.yaml)

落盘目标：

- `project_data/projects/{project_id}/series/creative-bible-v1.0.yaml`
- `project_data/projects/{project_id}/series/reviews/business/business-review-report-creative-v1.0.yaml`
- `project_data/projects/{project_id}/series/reviews/compliance/compliance-report-creative-stage-gate-v1.0.yaml`

## 2. 创意阶段完成标准

至少要有：

- `creative-bible-v{version}.yaml`
- 业务审核结论
- 合规审核结论

然后运行：

```bash
python3 tools/workflow_guard.py validate
python3 tools/workflow_guard.py status --project PROJECT_ID --episode ep01
```

如果 `status` 还显示创意阶段未放行，不要进剧本。

## 3. 单集起步

复制以下模板并改名：

- [templates/series/synopsis.template.yaml](../templates/series/synopsis.template.yaml)
- [templates/series/episode-plan.template.yaml](../templates/series/episode-plan.template.yaml)
- [templates/episodes/epXX/script/script.template.yaml](../templates/episodes/epXX/script/script.template.yaml)
- [templates/episodes/epXX/segments/segments.template.yaml](../templates/episodes/epXX/segments/segments.template.yaml)
- [templates/episodes/epXX/segments/tasks/epXX-SEG01.template.yaml](../templates/episodes/epXX/segments/tasks/epXX-SEG01.template.yaml)

## 4. 资产阶段起步

复制：

- [templates/episodes/epXX/assets/asset-manifest.template.yaml](../templates/episodes/epXX/assets/asset-manifest.template.yaml)
- [templates/episodes/epXX/assets/asset-prompts.template.yaml](../templates/episodes/epXX/assets/asset-prompts.template.yaml)
- [templates/episodes/epXX/assets/asset-index.template.yaml](../templates/episodes/epXX/assets/asset-index.template.yaml)
- [templates/episodes/epXX/assets/asset-archive.template.yaml](../templates/episodes/epXX/assets/asset-archive.template.yaml)

注意：

- 资产生成前必须先做合规预检
- 资产生成后必须补业务和合规审核

## 5. 视频阶段起步

复制：

- [templates/episodes/epXX/videos/video-prompts.template.yaml](../templates/episodes/epXX/videos/video-prompts.template.yaml)
- [templates/episodes/epXX/videos/video-tasks.template.yaml](../templates/episodes/epXX/videos/video-tasks.template.yaml)
- [templates/episodes/epXX/videos/video-tasks-final.template.yaml](../templates/episodes/epXX/videos/video-tasks-final.template.yaml)
- [templates/episodes/epXX/videos/video-archive.template.yaml](../templates/episodes/epXX/videos/video-archive.template.yaml)

注意：

- 视频生成前必须先做合规预检
- 视频生成后必须补业务和合规审核

## 6. 调度与台账

如果你想把当前集状态正式落盘，复制：

- [templates/episodes/epXX/orchestration/orchestration-result.template.yaml](../templates/episodes/epXX/orchestration/orchestration-result.template.yaml)
- [templates/episodes/epXX/orchestration/segment-ledger.template.yaml](../templates/episodes/epXX/orchestration/segment-ledger.template.yaml)

`status` 命令本身是只读的，不会自动写盘。

## 7. 每个阶段结束后的固定动作

1. 更新正式文件 `status`
2. 补业务 / 合规审核文件
3. 跑 `validate`
4. 跑 `status`
5. 只在放行 verdict 明确后继续

## 8. 推荐对话句式

- “按创意开发 Agent 的规则，基于这个想法补一版 creative-bible 草稿。”
- “按业务审核 Agent 的标准，审核这个创意文件，输出正式业务审核报告。”
- “现在只做 ep01 的 segment 规划，不进入资产阶段。”
- “先跑 validate 和 status，告诉我下一步缺什么文件。”
