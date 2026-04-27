# 正式视频结果归档模板

本文件定义正式视频结果归档的固定结构。

---

## 模板

```yaml
# === 视频结果归档 ===
# 由 video-finalization-and-review-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  version: "1.0"
  status: "draft"
  created_at: ""
  updated_at: ""

# === 归档统计 ===
summary:
  total_results: 0
  passed: 0
  failed: 0
  pending: 0
  pass_rate: "0%"
  total_retries: 0

# === 视频结果列表 ===
results:
  - task_id: "VTASK_SEG01"
    segment_id: "SEG01"
    episode_id: "ep01"
    input_strategy: "first_frame_only"

    # 输入记录
    inputs_used:
      first_frame: ""
      last_frame: ""
      reference_image: ""

    # 生成结果
    result_file: ""            # 视频文件相对路径
    file_size: ""
    duration: ""
    resolution: ""
    fps: 0
    format: ""                 # mp4 | mov | webm

    # 生成参数
    generation_params:
      model: ""
      seed: ""
      cfg_scale: ""
      motion_strength: ""
      prompt_used: ""          # 实际使用的 prompt（精简版）

    # 质量检查
    quality_check: "pass"      # pass | fail | pending
    quality_notes: ""

    # 连续性检查
    continuity_check: "pass"   # pass | fail | pending
    continuity_notes: ""

    # 重试记录
    retry_count: 0
    retry_log:
      - attempt: 1
        result: ""              # pass | fail
        reason: ""
        action_taken: ""
    final_version: true

    # 状态
    status: "draft"
    review_notes: ""

  - task_id: "VTASK_SEG02"
    # ... 同上

# === 质量检查汇总 ===
quality_summary:
  overall: "pass"               # pass | warning | fail
  character_continuity:
    overall: "pass"
    details: []
  scene_continuity:
    overall: "pass"
    details: []
  motion_quality:
    overall: "pass"
    details: []
  transition_smoothness:
    overall: "pass"
    details: []

# === 失败记录 ===
failed_results:
  - task_id: ""
    failure_reason: ""
    retry_history: []
    current_status: ""           # pending_retry | abandoned | replaced
    replacement_task: ""

# === 版本信息 ===
changelog:
  - version: "1.0"
    date: ""
    changes: []
    reason: ""

pending_items: []
risks: []
```

---

## 使用规则

1. 每条 result 必须与 video-tasks 中的 task 一一对应
2. quality_check = fail 的结果必须在 failed_results 中有详细记录
3. generation_params 必须记录实际使用的参数
4. continuity_check 仅对需要衔接的任务生效
5. retry_count 超过 3 次的结果应标记为 abandoned 或 replaced
6. quality_summary 中的 overall 根据所有结果汇总得出
