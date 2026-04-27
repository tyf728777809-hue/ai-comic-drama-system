# 正式资产索引模板

本文件定义正式资产索引的固定结构。

---

## 模板

```yaml
# === 正式资产索引 ===
# 由 asset-finalization-and-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  version: "1.0"
  status: "draft"         # draft | in_review | approved | rejected
  created_at: ""
  updated_at: ""
  based_on:
    segments: ""           # 引用 segment 总表版本
    asset_manifest: ""     # 引用资产清单版本

# === 资产统计 ===
summary:
  total_assets: 0
  by_type:
    character: 0
    background: 0
    prop: 0
    first_frame: 0
    last_frame: 0
  by_source:
    generated: 0
    reused: 0
  reuse_rate: "0%"
  total_segments: 0
  segments_covered: 0     # 有完整首帧+尾帧的 segment 数

# === 资产列表 ===
assets:
  - asset_id: "CHAR_ep01_seg01_01"
    type: "character"      # character | background | prop | first_frame | last_frame
    segment_id: "SEG01"
    episode_id: "ep01"
    description: ""        # 资产描述
    character_ref: ""      # 对应角色（角色图时填写）
    scene_ref: ""          # 对应场景（场景图时填写）
    prop_ref: ""           # 对应道具（道具图时填写）
    purpose: ""            # 资产用途说明
    source: "generate"     # generate | reuse
    reuse_from: ""         # 引用来源资产 ID（复用时填写）
    is_key_asset: false    # 是否为关键资产
    prompt_ref: ""         # 对应 prompt 编号
    result_file: ""        # 生成结果文件路径
    quality_check: ""      # pass | fail | pending
    status: "draft"
    risks: []
    notes: ""

  - asset_id: "BG_ep01_seg01_01"
    type: "background"
    # ... 同上

  - asset_id: "FF_ep01_seg01_01"
    type: "first_frame"
    # ... 同上

  - asset_id: "LF_ep01_seg01_01"
    type: "last_frame"
    # ... 同上

# === 复用关系 ===
reuse_map:
  - asset_id: ""
    reused_by: []          # 引用该资产的其他资产 ID
    reuse_type: ""         # same_pose | same_scene | same_prop | variant

# === Segment 覆盖检查 ===
segment_coverage:
  - segment_id: "SEG01"
    first_frame: ""        # 首帧资产 ID
    last_frame: ""         # 尾帧资产 ID
    characters: []         # 角色资产 ID 列表
    background: ""         # 场景资产 ID
    props: []              # 道具资产 ID 列表
    is_complete: false     # 首帧+尾帧+主要资产是否齐全

# === 关键资产标记 ===
key_assets:
  - asset_id: ""
    reason: ""             # 为什么是关键资产

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

1. 每个 asset 必须有唯一的 asset_id
2. 每个 segment 必须在 segment_coverage 中有记录
3. segment_coverage 中 is_complete = false 的 segment 必须在 pending_items 中说明原因
4. 复用关系必须在 reuse_map 中明确标注
5. key_assets 至少包含所有主角的首帧资产
6. summary 中的统计数据必须与 assets 列表实际数量一致
