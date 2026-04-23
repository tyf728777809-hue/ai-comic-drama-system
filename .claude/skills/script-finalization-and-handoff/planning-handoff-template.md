# 生产规划阶段交接摘要模板

本文件定义剧本阶段向生产规划阶段交接的固定格式。

---

## 设计原则

- 交接摘要应让生产规划 Agent 不需要读剧本全文就能开始工作
- 重点说明"做什么""什么不能改""什么可以优化"
- 为 15 秒拆段提供直接可用的信息

---

## 模板

```yaml
# === 生产规划阶段交接摘要 ===
# 由 script-finalization-and-handoff skill 生成

metadata:
  series_id: ""
  episode_id: "ep01"
  script_version: "1.0"
  handoff_version: "1.0"
  generated_at: ""
  handoff_from: "script-development-agent"
  handoff_to: "production-planning-agent"

# === 本集核心 ===
episode_summary:
  what_happens: ""            # 本集讲什么，2-3 句
  core_conflict: ""           # 核心冲突是什么
  resolution: ""              # 本集冲突如何（暂时）解决或升级
  emotion_tone: ""            # 整体情绪基调

# === 关键角色 ===
key_characters:
  - name: ""
    role: ""                  # 主角 / 对手 / 助手 / 其他
    appearance: ""            # 外观视觉关键词（发色、服装、标志物）
    key_expressions: []       # 本集关键表情/动作（用于资产生成参考）
    scenes: []                # 出场场景列表

# === 关键情绪节点 ===
emotion_nodes:
  - scene_id: ""
    emotion: ""               # 情绪类型
    intensity: ""             # 高 / 中 / 低
    visual_expression: ""     # 如何用画面表达该情绪
    is_peak: false            # 是否为本集情绪峰值

# === 已锁定设定（不可改） ===
locked_settings:
  characters: []              # 已锁定角色设定
  world_rules: []             # 已锁定世界观规则
  visual_style: ""            # 已锁定视觉风格
  color_palette: ""           # 已锁定色彩方案
  core_conflict_framework: "" # 已锁定核心冲突框架

# === 可细化空间（生产规划阶段可调整） ===
flexible_areas:
  - area: ""                  # 可细化的方面
    current_state: ""         # 当前状态
    suggestion: ""            # 建议细化方向
    constraint: ""            # 细化时的限制条件

# === 适合拆段强化的内容 ===
segment_enhancement_candidates:
  - scene_id: ""
    content: ""               # 该场景内容摘要
    why_enhance: ""           # 为什么适合拆段强化
    suggested_focus: ""       # 建议强化方向（如：慢镜头、特写、画面冲击）
    hook_potential: ""        # 钩子潜力评估

# === 视觉亮点（适合做封面/预告帧） ===
visual_highlights:
  - scene_id: ""
    description: ""           # 画面描述
    purpose: ""               # 封面帧 / 预告帧 / 社交传播图
    visual_keywords: []       # 视觉关键词（用于 prompt）

# === 场景清单与预估 ===
scene_summary:
  - scene_id: "SCENE_01"
    location: ""
    characters: []
    key_visual: ""            # 该场景关键画面
    estimated_duration: ""
    estimated_segments: 0     # 预估 15 秒段数
    production_difficulty: "" # 低 / 中 / 高
    difficulty_reason: ""     # 难度原因

# === 生产风险提示 ===
production_risks:
  - risk: ""
    severity: ""              # 高 / 中 / 低
    affected_scenes: []
    mitigation: ""            # 缓解建议

# === 版本信息 ===
version_info:
  script_version: ""
  handoff_version: ""
  status: "draft"
  pending_items: []
```

---

## 使用规则

1. 生产规划 Agent 应先读本交接摘要，再按需读取完整剧本
2. `locked_settings` 中的内容，生产规划阶段不得修改
3. `flexible_areas` 中的内容，生产规划阶段可在约束内细化
4. `segment_enhancement_candidates` 提供拆段优化的直接输入
5. `visual_highlights` 直接用于封面帧和预告帧的 prompt 设计
6. `scene_summary` 中的 `estimated_segments` 为预估值，生产规划阶段需重新精确计算
7. `production_risks` 应在生产规划中逐条处理

---

## 与生产规划阶段的边界

剧本阶段交接后，以下工作由生产规划阶段负责：
- 精确 15 秒分段
- segment 任务单编写
- 衔接设计
- 资产清单初版

剧本阶段不负责：
- 具体拆段方案
- 分镜设计
- 资产 prompt
- 视频 prompt
