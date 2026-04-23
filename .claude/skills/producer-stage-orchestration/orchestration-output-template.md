# 调度输出模板

本文件定义主控 Agent 每次调度后必须输出的固定格式。

---

## 输出模板

```yaml
# === 调度结论 ===
# 由 producer-stage-orchestration skill 生成

orchestration_result:
  # --- 基础信息 ---
  timestamp: ""                    # ISO 8601 格式
  series_id: ""                    # 系列 ID
  episode_id: ""                   # 单集 ID（如适用）

  # --- 阶段状态 ---
  current_stage: ""                # 未启动 | 创意定义 | 剧本开发 | 生产规划 | 资产生产 | 视频生产 | 已完成
  stage_status: ""                 # 未开始 | 进行中 | 审核中 | 已退回 | 已完成
  detection_basis: ""              # 判断依据：基于哪些文件和字段

  # --- 当前目标 ---
  current_goal: ""                 # 一句话描述当前应完成的目标

  # --- 已具备的输入 ---
  available_inputs:
    - name: ""                     # 产物名称
      path: ""                     # 文件路径
      version: ""                  # 版本号
      status: ""                   # draft | in_review | approved | rejected | missing

  # --- 缺失项 ---
  missing_deliverables:
    - name: ""                     # 缺失的产物名称
      required_by: ""              # 谁需要它
      priority: ""                 # critical | high | normal

  # --- 缺失审核 ---
  missing_reviews:
    - review_type: ""              # business_review | compliance_review
      target: ""                   # 审核对象
      phase: ""                    # 生成前 | 生成后
      required_before: ""          # 在什么操作之前必须完成

  # --- 调度决策 ---
  next_agent: ""                   # 建议调用的 Agent
  next_skill: ""                   # 建议调用的 Skill
  next_action: ""                  # 具体动作描述

  # --- 审核需求 ---
  needs_business_review: false
  needs_compliance_review: false

  # --- 推进判断 ---
  can_advance: false               # 是否允许进入下一阶段
  advance_reason: ""               # 允许或拒绝的原因

  # --- 并行判断 ---
  parallel_allowed: false          # 是否允许并行
  parallel_tasks: []               # 可并行任务列表
  parallel_block_reason: ""        # 不允许并行的原因

  # --- 阻断项 ---
  blockers:
    - description: ""              # 阻断描述
      type: ""                     # missing_deliverable | missing_review | pending_item | other
      resolution: ""               # 解决方案

  # --- 下一步建议 ---
  next_steps:
    - step: 1
      action: ""                   # 动作描述
      responsible_agent: ""        # 负责 Agent
      estimated_output: ""         # 预期产物
```

---

## 使用规则

1. 每次调度必须填充所有一级字段
2. 列表字段如果没有内容，填空列表 `[]`
3. 布尔字段必须明确 `true` 或 `false`，不能省略
4. `detection_basis` 必须说明判断依据，不能为空
5. 如果 `can_advance = false`，`advance_reason` 必须填写原因
6. 如果 `parallel_allowed = false`，`parallel_block_reason` 必须填写原因

---

## 输出示例

### 示例 1：新项目启动

```yaml
orchestration_result:
  timestamp: "2026-04-21T10:00:00Z"
  series_id: ""
  episode_id: ""

  current_stage: "未启动"
  stage_status: "未开始"
  detection_basis: "project_data/series/ 和 project_data/episodes/ 均为空目录"

  current_goal: "启动创意定义，收集项目创意需求"

  available_inputs: []

  missing_deliverables:
    - name: "创意设定文件"
      required_by: "剧本开发阶段"
      priority: "critical"

  missing_reviews: []

  next_agent: "creative-development-agent"
  next_skill: ""
  next_action: "启动创意访谈，收集项目创意需求并产出创意设定文件"

  needs_business_review: false
  needs_compliance_review: false

  can_advance: false
  advance_reason: "项目尚未启动，需先完成创意定义"

  parallel_allowed: false
  parallel_tasks: []
  parallel_block_reason: "前三个阶段严格串行"

  blockers:
    - description: "无创意设定文件"
      type: "missing_deliverable"
      resolution: "启动 creative-development-agent 进行创意访谈"

  next_steps:
    - step: 1
      action: "启动创意访谈"
      responsible_agent: "creative-development-agent"
      estimated_output: "创意设定文件 (draft)"
```

### 示例 2：创意定义完成，等待审核

```yaml
orchestration_result:
  timestamp: "2026-04-21T14:30:00Z"
  series_id: "SER001"
  episode_id: ""

  current_stage: "创意定义"
  stage_status: "审核中"
  detection_basis: "creative-brief-v1.yaml 存在，status = draft，所有关键字段已填写"

  current_goal: "将创意设定提交业务审核和合规审核"

  available_inputs:
    - name: "创意设定文件"
      path: "project_data/series/creative-brief-v1.yaml"
      version: "1.0"
      status: "draft"

  missing_deliverables: []

  missing_reviews:
    - review_type: "business_review"
      target: "creative-brief-v1.yaml"
      phase: "生成后"
      required_before: "进入剧本开发阶段"
    - review_type: "compliance_review"
      target: "creative-brief-v1.yaml"
      phase: "生成后"
      required_before: "进入剧本开发阶段"

  next_agent: "business-review-agent"
  next_skill: ""
  next_action: "依次调用业务审核和合规审核"

  needs_business_review: true
  needs_compliance_review: true

  can_advance: false
  advance_reason: "创意设定尚未审核，需业务审核和合规审核均通过后才能进入剧本开发"

  parallel_allowed: false
  parallel_tasks: []
  parallel_block_reason: "前三个阶段严格串行"

  blockers:
    - description: "创意设定未经过审核"
      type: "missing_review"
      resolution: "调用 business-review-agent 和 compliance-review-agent 进行审核"

  next_steps:
    - step: 1
      action: "创意设定 status 更新为 in_review"
      responsible_agent: "producer-agent"
      estimated_output: "状态更新"
    - step: 2
      action: "执行业务审核"
      responsible_agent: "business-review-agent"
      estimated_output: "业务审核结论"
    - step: 3
      action: "执行合规审核"
      responsible_agent: "compliance-review-agent"
      estimated_output: "合规审核结论"
```

### 示例 3：资产和视频并行

```yaml
orchestration_result:
  timestamp: "2026-04-22T09:00:00Z"
  series_id: "SER001"
  episode_id: "ep01"

  current_stage: "资产生产"
  stage_status: "进行中"
  detection_basis: "segments-v1.yaml approved，合规审核（生成前）approved，资产清单 draft"

  current_goal: "并行推进 SEG01-SEG03 的资产生产和 SEG01 的视频生产"

  available_inputs:
    - name: "Segment 总表"
      path: "project_data/episodes/ep01/segments-v1.yaml"
      version: "1.0"
      status: "approved"
    - name: "SEG01 图片资产"
      path: "project_data/episodes/ep01/assets/seg01/"
      version: "1.0"
      status: "approved"

  missing_deliverables:
    - name: "SEG02 图片资产"
      required_by: "视频生产"
      priority: "high"
    - name: "SEG03 图片资产"
      required_by: "视频生产"
      priority: "high"

  missing_reviews: []

  next_agent: "asset-production-agent"
  next_skill: ""
  next_action: "并行推进 SEG02/SEG03 资产生产 + SEG01 视频生产"

  needs_business_review: false
  needs_compliance_review: false

  can_advance: false
  advance_reason: "资产生产尚未全部完成"

  parallel_allowed: true
  parallel_tasks:
    - "SEG02 资产生产（asset-production-agent）"
    - "SEG03 资产生产（asset-production-agent）"
    - "SEG01 视频生产（video-production-agent）"
  parallel_block_reason: ""

  blockers: []

  next_steps:
    - step: 1
      action: "并行启动 SEG02/SEG03 资产生产"
      responsible_agent: "asset-production-agent"
      estimated_output: "SEG02/SEG03 图片资产"
    - step: 2
      action: "并行启动 SEG01 视频生产"
      responsible_agent: "video-production-agent"
      estimated_output: "SEG01 视频文件"
    - step: 3
      action: "全部资产完成后进行合规审核和业务审核"
      responsible_agent: "compliance-review-agent, business-review-agent"
      estimated_output: "审核结论"
```
