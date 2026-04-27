# 正式视频任务文件模板

本文件定义正式视频任务记录的固定结构。

---

## 模板

```yaml
# === 正式视频任务记录 ===
# 由 video-finalization-and-review-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  version: "1.0"
  status: "draft"         # draft | in_review | approved | rejected
  created_at: ""
  updated_at: ""
  based_on:
    segments: ""           # 引用 segment 总表版本
    asset_handoff: ""      # 引用资产交接摘要版本

# === 任务统计 ===
summary:
  total_tasks: 0
  by_strategy:
    reference_only: 0
    first_frame_only: 0
    last_frame_only: 0
    first_and_last: 0
  by_status:
    pending: 0
    completed: 0
    failed: 0
  total_retries: 0

# === 任务列表 ===
tasks:
  - task_id: "VTASK_SEG01"
    segment_id: "SEG01"
    episode_id: "ep01"
    duration: "15s"
    planning_status: "approved"

    # 输入策略
    input_strategy: "first_frame_only"  # reference_only | first_frame_only | last_frame_only | first_and_last
    strategy_reason: ""

    # 输入资产
    inputs:
      first_frame:
        asset_id: ""
        file_path: ""
        description: ""
      last_frame:
        asset_id: ""
        file_path: ""
        description: ""
      reference_image:
        asset_id: ""
        file_path: ""
        description: ""

    # 视频 prompt
    prompt:
      scene: ""
      characters: ""
      action: ""
      camera_movement: ""
      emotion_arc: ""
      continuity_hint: ""
      restrictions: []

    # 生成参数
    generation_params:
      model: ""
      seed: ""
      cfg_scale: ""
      motion_strength: ""
      duration: ""

    # 状态
    status: "draft"          # draft | generating | completed | failed
    quality_check: "pending"  # pass | fail | pending
    retry_count: 0
    max_retries: 3
    final_attempt: true

    # 连续性
    connects_from: ""        # 上一任务 ID
    connects_to: ""          # 下一任务 ID
    continuity_notes: ""

    # 风险
    risks: []
    notes: ""

  - task_id: "VTASK_SEG02"
    # ... 同上

# === 衔接关系 ===
continuity_map:
  - from_task: "VTASK_SEG01"
    to_task: "VTASK_SEG02"
    connection_type: ""      # same_scene | scene_change | character_transition
    risk_level: ""           # low | medium | high
    notes: ""

# === 版本信息 ===
changelog:
  - version: "1.0"
    date: ""
    changes: []
    reason: ""

pending_items: []
```

---

## 使用规则

1. 每个任务必须有唯一的 task_id
2. 每个 segment 必须有对应的任务
3. input_strategy 必须与实际输入资产一致
4. 首尾帧组合策略必须同时有 first_frame 和 last_frame
5. continuity_map 必须覆盖所有相邻任务对
6. summary 统计必须与实际任务列表一致
