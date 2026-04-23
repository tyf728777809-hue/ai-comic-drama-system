# 正式创意设定文件模板

本文件定义创意 Bible 的固定结构。所有已确认的创意内容必须按此模板输出。

---

## 模板

```yaml
# === 创意设定文件 ===
# 由 creative-bible-and-handoff skill 生成

metadata:
  project_name: ""
  series_id: ""
  version: "1.0"
  status: "draft"             # draft | in_review | approved | rejected
  generated_at: ""
  previous_version: ""
  changelog:
    - version: "1.0"
      date: ""
      changes:
        - "初始创意设定"
      reason: "创意收敛后首次定稿"

# === 作品定位 ===
project_positioning:
  title: ""                   # 项目名称
  format: ""                  # 作品形态：竖屏短剧 / 横屏短剧 / 系列短视频
  genre: ""                   # 题材类型：都市/校园/悬疑/甜宠/奇幻/古风/职场/家庭
  style: ""                   # 风格基调：轻松/紧张/治愈/燃/悲情/暗黑/搞笑
  target_audience: ""         # 目标受众
  platform: ""                # 发布平台

# === 核心钩子 ===
core_hook:
  logline: ""                 # 一句话概述（25 字以内）
  hook_description: ""        # 核心钩子描述
  core_selling_point: ""      # 核心卖点
  opening_hook: ""            # 开场 3 秒钩子设计

# === 故事核心 ===
story_core:
  premise: ""                 # 故事 premise
  core_conflict: ""           # 核心冲突
  central_question: ""        # 核心悬念（故事要回答的问题）
  emotional_core: ""          # 情感核心
  narrative_arc: ""           # 叙事弧线概述

# === 主角设定 ===
protagonist:
  name: ""
  age: ""
  occupation: ""
  personality: ""             # 核心性格特征（3-5 个关键词）
  appearance: ""              # 外形描述（影响 AI 生图）
  signature_look: ""          # 标志性外观元素（发型/穿搭/配饰）
  core_desire: ""             # 核心欲望
  core_flaw: ""               # 核心弱点/矛盾
  starting_state: ""          # 故事开始时的状态
  arc_direction: ""           # 角色弧光方向
  special_notes: ""           # 特别说明

# === 主要配角设定 ===
supporting_characters:
  - name: ""
    role: ""                  # 在故事中的功能
    relationship_to_protagonist: ""
    personality: ""
    appearance: ""
    signature_look: ""
    narrative_function: ""    # 推动冲突/提供信息/制造反转/情感支撑
    arc_direction: ""
    special_notes: ""

  # ... 最多 3 个核心配角

# === 人物关系 ===
character_relationships:
  core_relationship: ""       # 最重要的关系
  relationship_type: ""       # 对手/伙伴/CP/亲人/镜像
  core_tension: ""            # 关系中的核心张力
  relationship_arc: ""        # 关系变化方向
  other_relationships:
    - characters: ""
      type: ""
      tension: ""

# === 世界观规则 ===
worldbuilding:
  setting: ""                 # 时代和地点
  type: ""                    # 现实/轻度架空/完全架空/奇幻/科幻
  core_rules: []              # 世界观核心规则（最多 3 条）
  visual_style: ""            # 视觉风格描述
  daily_life: ""              # 角色日常生活概述
  constraints: []             # 世界观限制条件

# === 生产参数 ===
production_params:
  episode_duration: ""        # 单集时长
  episode_count: ""           # 总集数
  segment_duration: ""        # 段时长（通常 15 秒）
  segments_per_episode: ""    # 每集段数
  format_notes: ""            # 形式补充说明

# === 商业目标 ===
business_goals:
  primary_goal: ""            # 主要目标
  secondary_goals: []         # 次要目标
  target_metrics: ""          # 目标指标
  brand_constraints: []       # 品牌约束（如有）

# === 参考系 ===
references:
  - name: ""
    type: ""                  # 动漫/剧集/电影/小说/漫画
    aligned_dimensions:
      - dimension: ""
        detail: ""
    not_aligned: []
    priority: 1

# === 禁区与边界 ===
boundaries:
  hard_no: []                 # 绝对不要的内容
  tone_limits: []             # 基调限制
  content_restrictions: []    # 内容限制（暴力/血腥/敏感等）
  visual_avoid: []            # 视觉上要避免的

# === 风险提示 ===
risk_assessment:
  narrative_risks: []         # 叙事层面风险
  production_risks: []        # 生产层面风险
  ai_friendly_notes: []       # AI 生产友好性提示
  mitigation_suggestions: []  # 风险缓解建议

# === 待确认项 ===
pending_items:
  - item: ""
    priority: ""              # P0 | P1 | P2
    impact: ""                # 对后续阶段的影响
    suggested_resolution: ""  # 建议解决方式

# === 锁定与探索边界 ===
locked_vs_explorable:
  locked: []                  # 已锁定、不可修改的设定
  explorable: []              # 仍可在剧本阶段细化/探索的内容
  flexibility_notes: ""
```

---

## 使用规则

1. 每份创意设定必须有唯一的 series_id
2. version 和 status 必须与 [version-status-rules.md](version-status-rules.md) 一致
3. protagonist 和 supporting_characters 的 appearance 字段必须足够具体，能指导 AI 生图
4. pending_items 中所有 P0 项必须在 approved 前解决
5. locked_vs_explorable 必须明确，剧本阶段需遵守此边界
6. 文件存放路径：`project_data/series/`
7. 文件命名：`creative-bible-v{version}.yaml`
