# 正式 segment 总表模板

本文件定义正式 segment 总表的固定结构。

---

## 模板

```yaml
# === 正式 segment 总表 ===
# 由 segment-finalization-and-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  version: "1.0"
  status: "draft"             # draft | in_review | approved | rejected
  created_at: ""
  updated_at: ""
  based_on:
    script_file: ""            # 引用剧本文件路径
    script_version: ""         # 引用剧本版本号
    script_handoff: ""         # 引用剧本交接摘要路径

# === 总表统计 ===
summary:
  total_segments: 0
  total_duration: ""           # 如 "3m30s"
  by_purpose:
    hook: 0
    push: 0
    twist: 0
    resolution: 0
    transition: 0
  by_scene:
    - scene: ""
      count: 0
  by_risk:
    high: 0
    medium: 0
    low: 0

# === segment 列表 ===
segments:
  - segment_id: "SEG01"
    duration: "15s"
    purpose: ""                # hook | push | twist | resolution | transition
    purpose_description: ""
    content_summary: ""        # 100 字以内
    key_characters: []
    scene: ""
    key_visual: ""
    shot_type: ""
    camera_movement: ""
    transition_in: ""
    transition_out: ""
    emotion_start: ""
    emotion_end: ""
    risk_level: ""             # high | medium | low
    risk_notes: ""
    pending_items: []

  # ... 所有 segment 逐段列出

# === 衔接关系 ===
continuity_map:
  - from_segment: "SEG01"
    to_segment: "SEG02"
    connection_type: ""        # same_scene | scene_change | time_skip | character_focus_change
    transition_description: ""
    risk_level: ""
    notes: ""

  # ... 所有相邻段对

# === 角色出场统计 ===
character_appearances:
  - character: ""
    segments: []
    total_appearances: 0

# === 场景使用统计 ===
scene_appearances:
  - scene: ""
    segments: []
    total_appearances: 0

# === 风险汇总 ===
risks:
  high: []
  medium: []
  low: []

# === 已知限制 ===
known_limitations: []

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

1. 每个 segment 必须在总表中有对应条目
2. continuity_map 必须覆盖所有相邻段对
3. summary 统计必须与实际 segment 列表一致
4. risks 按 high → medium → low 排序
5. 总表存放路径：`project_data/projects/{project_id}/episodes/epXX/segments/`
