# 资产 Prompt 文件模板

本文件定义资产 prompt 文件的固定结构。

```yaml
metadata:
  series_id: ""
  episode_id: "ep01"
  version: "1.0"
  status: "draft"
  created_at: ""
  updated_at: ""
  based_on:
    asset_manifest: ""
    creative_bible: ""
    segments: ""

summary:
  total_prompts: 0
  by_type:
    character_turnaround: 0
    expression_sheet: 0
    pose_sheet: 0
    scene_master: 0
    ui_spec: 0
    prop_reference: 0
    first_frame: 0
    last_frame: 0
  global_requirements:
    aspect_ratio: "16:9"
    consistency_pack_required: true

prompts:
  - prompt_id: "APROMPT_ep01_LINCHE_TURNAROUND"
    asset_id: "ASSET_ep01_LINCHE_TURNAROUND"
    segment_id: "GLOBAL"
    type: "character_turnaround"
    subject: "核心角色三视图"
    prompt_text: ""
    negative_prompt: ""
    continuity_hint: "作为该角色所有 segment 首尾帧和姿态变体的唯一外观基准。"
    status: "draft"
    risks: []
    notes: ""
  - prompt_id: "APROMPT_ep01_SEG01_FF"
    asset_id: "ASSET_ep01_SEG01_FF"
    segment_id: "SEG01"
    type: "first_frame"
    subject: "SEG01 首帧"
    prompt_text: ""
    negative_prompt: ""
    continuity_hint: "必须引用角色三视图、场景母版和 UI / 道具规范。"
    status: "draft"
    risks: []
    notes: ""

changelog:
  - version: "1.0"
    date: ""
    changes: []
    reason: ""

pending_items: []
```
