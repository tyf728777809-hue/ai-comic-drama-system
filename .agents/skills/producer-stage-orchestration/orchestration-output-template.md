# 调度输出模板

本文件定义主控 Agent 每次调度后必须输出的固定格式。

## 输出模板

```yaml
orchestration_result:
  timestamp: ""
  project_id: ""
  series_id: ""
  episode_id: ""
  current_stage: ""
  stage_status: ""
  detection_basis: ""
  current_goal: ""
  available_inputs:
    - name: ""
      path: ""
      version: ""
      status: ""
  missing_deliverables:
    - name: ""
      required_by: ""
      priority: ""
  missing_reviews:
    - review_type: ""        # business_review | compliance_review
      target: ""
      phase: ""              # pre_generation | post_generation | stage_gate
      required_before: ""
      verdict: ""            # missing | pass | pass_with_revisions | conditional_pass | fail
  next_agent: ""
  next_skill: ""
  next_action: ""
  needs_business_review: false
  needs_compliance_review: false
  can_advance: false
  advance_reason: ""
  parallel_allowed: false
  parallel_tasks: []
  parallel_block_reason: ""
  blockers:
    - description: ""
      type: ""               # missing_deliverable | missing_review | pending_item | blocked_segment | other
      resolution: ""
  next_steps:
    - step: 1
      action: ""
      responsible_agent: ""
      estimated_output: ""

segment_ledger:
  project_id: ""
  episode_id: ""
  generated_at: ""
  items:
    - segment_id: "SEG01"
      planning_status: ""            # missing | draft | in_review | approved | rejected
      asset_precheck_compliance: ""  # missing | pass | conditional_pass | fail
      asset_output_status: ""        # missing | draft | in_review | approved | rejected
      asset_business_verdict: ""     # missing | pass | pass_with_revisions | fail
      asset_compliance_verdict: ""   # missing | pass | conditional_pass | fail
      video_precheck_compliance: ""  # missing | pass | conditional_pass | fail
      video_output_status: ""        # missing | draft | in_review | approved | rejected
      video_business_verdict: ""     # missing | pass | pass_with_revisions | fail
      video_compliance_verdict: ""   # missing | pass | conditional_pass | fail
      blocked_by: []
      can_start_asset: false
      can_start_video: false
```

## 使用规则

1. 每次调度必须填充所有一级字段
2. 列表字段为空时使用 `[]`
3. `detection_basis` 必须引用实际文件和字段
4. `missing_reviews` 必须显式写出 verdict，而不是只写“待审核”
5. `segment_ledger` 在阶段 1/2/3 可返回空 `items: []`
6. 对话里可以按上面的组合结构输出；实际落盘时拆成两个文件：
   - `project_data/projects/{project_id}/episodes/epXX/orchestration/orchestration-result-v{version}.yaml`
   - `project_data/projects/{project_id}/episodes/epXX/orchestration/segment-ledger-v{version}.yaml`
7. `orchestration-result` 文件根节点直接从 `timestamp` 开始，不额外套一层 `orchestration_result:`
8. `segment-ledger` 文件根节点直接从 `episode_id` 开始，不额外套一层 `segment_ledger:`

## 判定要点

- 审核是否放行只看 `conclusion.verdict` 和 `gate_decision`
- `report_status` 只可出现在说明里，不可参与 `can_advance`
- `can_start_video = true` 的唯一条件：
  - `planning_status = approved`
  - `asset_output_status = approved`
  - `asset_business_verdict` 为 `pass` 或 `pass_with_revisions`
  - `asset_compliance_verdict` 为 `pass` 或 `conditional_pass`
  - `video_precheck_compliance` 为 `pass` 或 `conditional_pass`
