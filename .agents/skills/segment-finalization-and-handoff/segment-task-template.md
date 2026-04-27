# 正式单段任务文件模板

本文件定义正式单段任务文件的固定结构。

---

## 模板

```yaml
# === 正式单段任务文件 ===
# 由 segment-finalization-and-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  segment_id: "SEG01"
  version: "1.0"
  status: "draft"             # draft | in_review | approved | rejected
  created_at: ""
  updated_at: ""
  based_on:
    script_act: ""
    script_scene: ""
    script_beat: ""

# === 基本标识 ===
segment_id: "SEG01"
episode_id: "ep01"
duration: "15s"
key_visual: ""
shot_type: ""
camera_movement: ""
transition_in: ""
transition_out: ""

# === 剧情信息 ===
narrative:
  purpose: ""                  # hook | push | twist | resolution | transition
  purpose_description: ""
  content_summary: ""          # 详细内容摘要（200 字以内）
  script_reference: ""         # 剧本原文关键引用

# === 角色与状态 ===
characters:
  - name: ""
    role_in_segment: ""        # 主角 | 配角 | 背景
    appearance: ""             # 引用角色设定
    costume: ""
    state: ""
    action: ""

# === 动作与情绪 ===
action_and_emotion:
  primary_action: ""
  emotion_start: ""
  emotion_end: ""
  emotion_arc: ""
  key_moment: ""               # 本段关键画面

# === 场景信息 ===
scene:
  location: ""
  location_type: ""            # indoor | outdoor | mixed
  time_of_day: ""
  weather: ""
  key_props: []

# === 衔接信息 ===
continuity:
  connects_from: ""            # 上段 segment_id
  connects_to: ""              # 下段 segment_id
  connection_type: ""          # same_scene | scene_change | time_skip | character_focus_change
  transition_description: ""

  first_frame:
    suggested_composition: ""
    character_positions: ""
    key_elements: []
    mood: ""

  last_frame:
    suggested_composition: ""
    character_positions: ""
    key_elements: []
    mood: ""

  transition_hint: ""

# === 资产提示 ===
asset_hints:
  characters_needed: []
  backgrounds_needed: []
  props_needed: []
  first_frame_needed: true/false
  last_frame_needed: true/false

# === 风险 ===
risks:
  - risk_type: ""
    severity: ""
    description: ""
    mitigation: ""

# === 待确认项 ===
pending_items: []

# === 备注 ===
notes: ""
```

---

## 使用规则

1. 每个 segment 一个独立文件
2. 文件名格式：`{episode_id}-SEG{NN}-v{version}.yaml`
3. connects_from 和 connects_to 必须与相邻段互相引用一致
4. 所有描述必须基于剧本原文
5. 无法确认的项必须进入 pending_items
6. 文件存放路径：`project_data/projects/{project_id}/episodes/epXX/segments/tasks/`
