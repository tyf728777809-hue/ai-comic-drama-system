# 审核阶段交接摘要模板

本文件定义视频阶段向审核阶段交接的固定格式。

---

## 模板

```yaml
# === 审核阶段交接摘要 ===
# 由 video-finalization-and-review-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  video_version: "1.0"
  handoff_version: "1.0"
  generated_at: ""
  handoff_from: "video-production-agent"
  handoff_to: "business-review-agent + compliance-review-agent"

# === 视频总览 ===
video_overview:
  total_segments: 0
  total_videos: 0
  all_review_ready: true       # 所有视频是否都可进入审核
  key_warning: ""              # 如果不是全部 ready，主要原因

# === 可直接审核的视频 ===
review_ready:
  - task_id: ""
    segment_id: "SEG01"
    duration: "15s"
    result_file: ""
    input_strategy: ""
    quality_check: "pass"
    continuity_check: "pass"
    review_notes: ""

# === 存在连续性风险的视频 ===
continuity_risks:
  - task_id: ""
    segment_id: ""
    risk_type: ""               # character_drift | scene_inconsistency | motion_discontinuity | transition_gap
    description: ""
    severity: ""                # 高 | 中 | 低
    affected_segments: []
    mitigation: ""              # 审核时的关注点

# === 建议重试的视频 ===
retry_suggested:
  - task_id: ""
    segment_id: ""
    issue: ""
    retry_count: 0
    recommendation: ""          # 调整 prompt | 调整参数 | 更换策略
    estimated_effort: ""

# === 建议回退上游的视频 ===
fallback_suggested:
  - task_id: ""
    segment_id: ""
    problem: ""
    root_cause: ""              # asset_quality | planning_design | input_conflict
    fallback_target: ""         # asset_stage | planning_stage
    reason: ""
    required_fix: ""
    affected_segments: []

# === 角色一致性参考 ===
character_consistency:
  - character_name: ""
    visual_keywords: ""
    segments_appeared: []
    consistency_status: "stable"  # stable | minor_drift | significant_drift
    notes: ""

# === 场景一致性参考 ===
scene_consistency:
  - scene_name: ""
    segments_appeared: []
    consistency_status: "stable"  # stable | minor_drift | significant_drift
    notes: ""

# === 衔接连贯性参考 ===
transition_consistency:
  - from_segment: ""
    to_segment: ""
    transition_type: ""           # same_scene | scene_change | time_skip
    smoothness: "smooth"          # smooth | slight_jump | noticeable_gap
    notes: ""

# === 生产风险提示 ===
production_risks:
  - risk: ""
    severity: ""
    affected_segments: []
    mitigation: ""

# === 版本信息 ===
version_info:
  video_version: ""
  handoff_version: ""
  status: "draft"
  pending_items: []
```

---

## 使用规则

1. 审核阶段应先读本交接摘要，再按需读取具体视频文件
2. review_ready 中的视频可直接进入审核流程
3. continuity_risks 中的视频应在审核时额外关注
4. retry_suggested 中的视频不建议进入审核，应先重试
5. fallback_suggested 中的视频不应进入审核，应先回退上游
6. 角色和场景一致性参考用于审核时的对比检查

---

## 与审核阶段的边界

视频阶段交接后，以下工作由审核阶段负责：
- 业务质量审核
- 合规审核

视频阶段不负责：
- 审核结论的判定
- 审核后的放行决策
- 后期剪辑和成片组装
