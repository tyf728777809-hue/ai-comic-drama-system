# 阶段进出矩阵

本文件定义每个阶段的进入条件、退出条件、必须审核项和状态流转规则。

## 阶段总览

| 阶段编号 | 阶段名称 | 粒度 | 负责 Agent |
|---------|---------|------|-----------|
| 1 | 创意定义 | 系列级 | creative-development-agent |
| 2 | 剧本开发 | 系列级 + 单集级 | script-development-agent |
| 3 | 生产规划 | 单集级 | production-planning-agent |
| 4 | 资产生产 | segment 级 | asset-production-agent |
| 5 | 视频生产 | segment 级 | video-production-agent |

## 阶段 1：创意定义

### 进入条件
- 无前置条件

### 正式产物
- `project_data/projects/{project_id}/series/creative-bible-vX.yaml`

### 退出条件
- 正式创意设定存在且 `metadata.status = approved`
- `project_positioning`、`core_hook`、`story_core`、`protagonist`、`worldbuilding`、`production_params` 完整
- `pending_items` 中无 P0 项
- 系列级业务审核 verdict 已放行
- 系列级合规审核 verdict 已放行

### 必须审核
- 业务审核：`project_data/projects/{project_id}/series/reviews/business/`
- 合规审核：`project_data/projects/{project_id}/series/reviews/compliance/`

## 阶段 2：剧本开发

### 进入条件
- 创意阶段正式文件 approved
- 创意阶段业务与合规 verdict 允许推进

### 正式产物
- `project_data/projects/{project_id}/series/synopsis-vX.yaml`
- `project_data/projects/{project_id}/series/episode-plan-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/script/script-vX.yaml`

### 退出条件
- 梗概、分集规划、单集剧本存在
- 单集剧本 `metadata.status = approved`
- 每个场景包含 `action`、`emotion`、`estimated_duration`
- `pending_items` 中无 P0 项
- 当前集业务审核 verdict 已放行
- 当前集合规审核 verdict 已放行

### 必须审核
- `project_data/projects/{project_id}/episodes/epXX/reviews/business/`
- `project_data/projects/{project_id}/episodes/epXX/reviews/compliance/`

## 阶段 3：生产规划

### 进入条件
- 当前集剧本 approved
- 剧本业务与合规 verdict 允许推进

### 正式产物
- `project_data/projects/{project_id}/episodes/epXX/segments/segments-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/segments/tasks/{episode_id}-SEG{NN}-v{version}.yaml`

### 退出条件
- segment 总表和全部任务文件存在
- segment 总表 `metadata.status = approved`
- 每个 segment 包含 `key_visual`、`shot_type`、`camera_movement`、`transition_in`、`transition_out`
- `pending_items` 中无 P0 项
- 当前集业务审核 verdict 已放行
- 当前集合规审核 verdict 已放行

### 必须审核
- `project_data/projects/{project_id}/episodes/epXX/reviews/business/`
- `project_data/projects/{project_id}/episodes/epXX/reviews/compliance/`

## 阶段 4：资产生产

### 进入条件
- 当前集 segment 总表 approved
- 规划阶段业务与合规 verdict 允许推进
- 当前 segment 的资产生成前合规 verdict 已放行

### 正式产物
- `project_data/projects/{project_id}/episodes/epXX/assets/asset-manifest-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/assets/asset-prompts-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/assets/asset-index-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/assets/asset-archive-vX.yaml`

### 退出条件
- 资产归档覆盖所有需启动的 segment
- 每个资产结果存在 `result_file`
- 对应正式文件 `metadata.status = approved`
- 资产生成后业务审核 verdict 已放行
- 资产生成后合规审核 verdict 已放行

### 必须审核
- 生成前合规审核
- 生成后业务审核
- 生成后合规审核

### 并行条件
- 不同 segment 可并行
- 同一 segment 的视频启动必须等待该 segment 资产通过生成后业务与合规审核

## 阶段 5：视频生产

### 进入条件
- 当前 segment 资产结果 approved
- 资产生成后业务与合规 verdict 已放行
- 视频生成前合规 verdict 已放行

### 正式产物
- `project_data/projects/{project_id}/episodes/epXX/videos/video-prompts-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/videos/video-tasks-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/videos/video-tasks-final-vX.yaml`
- `project_data/projects/{project_id}/episodes/epXX/videos/video-archive-vX.yaml`

### 退出条件
- 视频结果覆盖可启动的 segment
- 每个结果存在 `result_file`
- `video-tasks-final` 与 `video-archive` 均为 approved
- 视频生成后业务审核 verdict 已放行
- 视频生成后合规审核 verdict 已放行

### 必须审核
- 生成前合规审核
- 生成后业务审核
- 生成后合规审核

## 状态流转规则

| 对象 | 推进依据 |
|------|---------|
| 正式产物 | 只看 `metadata.status` |
| 审核报告 | 只看 `conclusion.verdict` 与 `gate_decision` |
| segment 视图 | 只看 ledger 中的固定字段 |

硬性规则：
- `draft` / `in_review` / `rejected` 的正式产物不得作为下游输入
- 审核 verdict 为 `fail` 必须触发回退
- `report_status` 不能作为推进依据
- 视频启动必须经过 segment 级门禁判断
