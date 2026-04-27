# 单段任务信息模板

本文件定义单个 segment 的任务信息结构。拆解阶段使用此模板填写每个段落的详细信息。

---

## 模板

```yaml
# === 单段任务信息 ===
# 由 segment-planning-and-structuring skill 生成

# === 基本标识 ===
segment_id: "SEG01"
episode_id: "ep01"
duration: "15s"
version: "1.0"
status: "draft"

# === 剧情信息 ===
narrative:
  purpose: ""                  # hook | push | twist | resolution | transition
  purpose_description: ""      # 具体目的描述
  content_summary: ""          # 150 字以内的内容摘要

  # 剧本来源
  source:
    act: ""                    # 剧本幕次
    scene: ""                  # 剧本场景
    beat: ""                   # 剧本节拍
    script_reference: ""       # 剧本原文引用（关键句）

# === 角色与状态 ===
characters:
  - name: ""
    role_in_segment: ""        # 主角 | 配角 | 背景
    appearance: ""             # 外观描述（引用设定）
    costume: ""                # 服装描述
    state: ""                  # 情绪/身体状态
    position: ""               # 在场景中的位置
    action: ""                 # 本段动作

  # ... 更多角色

# === 动作与情绪 ===
action_and_emotion:
  primary_action: ""           # 主要动作
  secondary_actions: []        # 次要动作
  emotion_start: ""            # 段首情绪
  emotion_end: ""              # 段尾情绪
  emotion_arc: ""              # 情绪变化描述
  key_moment: ""               # 本段关键画面时刻

# === 场景信息 ===
scene:
  location: ""                 # 场景名称
  location_type: ""            # indoor | outdoor | mixed
  time_of_day: ""              # morning | afternoon | evening | night
  weather: ""                  # 天气/氛围
  key_props: []                # 关键道具
  background_description: ""   # 背景描述

# === 衔接信息 ===
continuity:
  connects_from: ""            # 上一段 segment_id（首段为 null）
  connects_to: ""              # 下一段 segment_id（末段为 null）
  connection_type: ""          # same_scene | scene_change | time_skip | character_focus_change
  transition_description: ""   # 过渡描述

  # 首帧建议
  first_frame:
    suggested_composition: ""  # 构图建议（全景/中景/特写）
    character_positions: ""    # 角色位置
    key_elements: []           # 画面关键元素
    mood: ""                   # 画面情绪

  # 尾帧建议
  last_frame:
    suggested_composition: ""
    character_positions: ""
    key_elements: []
    mood: ""

  # 首尾帧衔接提示
  transition_hint: ""          # 给视频阶段的衔接提示

# === 资产提示 ===
asset_hints:
  characters_needed: []        # 需要的角色资产
  backgrounds_needed: []       # 需要的场景资产
  props_needed: []             # 需要的道具资产
  first_frame_needed: true/false
  last_frame_needed: true/false
  reference_images_needed: []  # 需要的参考图

# === 风险提示 ===
risks:
  - risk_type: ""              # continuity | production | complexity | asset
    severity: ""               # high | medium | low
    description: ""
    mitigation: ""             # 缓解建议

# === 待确认项 ===
pending_items:
  - item: ""
    type: ""                   # content | asset | timing | continuity | other
    question: ""               # 需要确认的问题
    impact: ""                 # 不确认的影响
    default: ""                # 建议默认值

# === 备注 ===
notes: ""
```

---

## 使用规则

1. 每个 segment 必须完整填写此模板
2. 段号和集号必须按 segment-id-rules.md 的格式
3. purpose 必须从五种类型中选择
4. characters 至少包含一个角色
5. connects_from 和 connects_to 必须与相邻段一致
6. 首帧和尾帧建议必须具体到构图和位置
7. 无法确认的项必须进入 pending_items
8. risks 中 high 级别必须给出 mitigation
9. 模板中的所有描述必须基于剧本原文，不得自行创作
