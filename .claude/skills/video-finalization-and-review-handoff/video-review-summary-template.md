# 视频确认前复盘摘要模板

本文件定义给用户的视频确认前复盘摘要的固定格式。

---

## 模板

```yaml
# === 视频确认前复盘摘要 ===
# 由 video-finalization-and-review-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  video_version: "1.0"
  generated_at: ""

# === 视频统计 ===
video_stats:
  total_segments: 0
  total_tasks: 0
  completed_videos: 0
  failed_videos: 0
  pass_rate: "0%"
  total_retries: 0
  by_strategy:
    first_frame_only: 0
    first_and_last: 0
    reference_only: 0

# === 已确认内容 ===
confirmed:
  - item: "Segment 覆盖完整性"
    status: "confirmed"
    detail: "所有 segment 都有对应的视频任务"
  - item: "首帧输入完整性"
    status: "confirmed"
    detail: "所有任务都有首帧输入资产"
  - item: "视频 prompt 充分性"
    status: "confirmed"
    detail: "所有 prompt 包含完整场景、角色、动作、镜头描述"
  - item: "角色连续性"
    status: "confirmed"
    detail: "同角色跨 segment 描述一致"
  - item: "场景连续性"
    status: "confirmed"
    detail: "同场景跨 segment 描述一致"
  - item: "首尾帧衔接"
    status: "confirmed"
    detail: "相邻 segment 首尾帧兼容"
  - item: "视频风险检查"
    status: "confirmed"
    detail: "无 fail 级别风险项"

# === 待确认内容 ===
pending:
  - item: ""
    type: "video_choice"      # video_choice | quality_check | strategy_preference | other
    question: ""               # 需要用户回答的问题
    options: []                # 可选项
    impact: ""                 # 如果不确认的影响
    default: ""                # 建议默认值

# === 主要风险 ===
key_risks:
  - risk: ""
    severity: "warning"        # warning | info
    affected_segments: []
    mitigation: ""

# === 质量问题 ===
quality_issues:
  - task_id: ""
    segment_id: ""
    issue: ""
    severity: "warning"        # warning | minor
    suggestion: ""

# === 重试/回退建议 ===
retry_recommendations:
  - task_id: ""
    segment_id: ""
    issue: ""
    recommendation: "retry"    # retry | fallback_asset | fallback_planning
    reason: ""

# === 如果确认，下一步 ===
if_confirmed:
  next_stage: "业务审核 + 合规审核（视频生成后）"
  process:
    - step: 1
      action: "视频任务 status 更新为 in_review"
    - step: 2
      action: "提交合规审核（视频生成后）"
    - step: 3
      action: "提交业务审核（视频生成后）"
    - step: 4
      action: "两项审核均通过后，status 更新为 approved"
    - step: 5
      action: "项目完成，输出阶段交接摘要"
  review_ready_videos: 0       # 可直接进入审核的视频数
  review_blocked_videos: 0     # 暂不可审核的视频数

# === 如果不确认 ===
if_not_confirmed:
  options:
    - action: "修改特定视频 prompt"
      description: "指出需要修改的具体任务，返回生成阶段"
    - action: "调整输入策略"
      description: "更换部分任务的输入策略"
    - action: "重试失败视频"
      description: "对质量不达标的视频重新生成"
    - action: "回退上游问题"
      description: "将上游问题退回资产或规划阶段"
    - action: "暂停"
      description: "暂不定稿，保存当前版本"
```

---

## 使用规则

1. video_stats 必须与视频任务和结果数据一致
2. confirmed 列表应覆盖所有关键检查点
3. pending 只列真正需要用户决定的内容
4. key_risks 只列 warning 级别风险
5. retry_recommendations 明确区分 retry 和 fallback
6. if_confirmed 必须清晰说明审核流程
