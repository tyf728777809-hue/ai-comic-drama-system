---
name: producer-stage-orchestration
description: 主控 Agent 的正常推进方法包。负责阶段判断、状态同步、审核门禁、并行调度和推进决策。适用于项目处于正常流转状态时使用，不处理失败恢复。
---

# Skill：producer-stage-orchestration

## 适用场景

当主控 Agent 需要判断"项目当前在哪一步、下一步该做什么"时使用本 skill。

典型触发条件：
- 用户发起新项目
- 用户说"继续推进""下一步"
- 某个阶段刚完成，需要判断能否进入下一阶段
- 需要确认当前项目状态
- 需要判断是否可以并行

**不适用**：审核失败、生成失败、需要回退时 → 使用 `producer-recovery-control`

---

## 核心目标

1. 基于文件和状态精确判断当前阶段
2. 识别当前缺失的正式产物和审核
3. 判断是否满足阶段退出条件
4. 输出固定格式的调度结论

---

## 输入

本 skill 通过读取以下位置获取信息：

| 输入来源 | 路径 | 用途 |
|---------|------|------|
| 系列级设定 | `project_data/series/` | 确认创意设定是否存在及状态 |
| 单集数据 | `project_data/episodes/epXX/` | 确认剧本、segment、资产、视频产物 |
| 业务审核结论 | `project_data/episodes/epXX/reviews/` | 确认业务审核状态 |
| 合规审核结论 | `project_data/episodes/epXX/reviews/` | 确认合规审核状态 |

读取规则：
- 如果目标文件不存在，视为该产物"未产出"
- 如果文件存在但缺少 status 字段，视为 status = "unknown"
- 不靠猜测，不靠上下文记忆

---

## 输出

本 skill 输出一个固定格式的调度结论。模板见 `orchestration-output-template.md`。

结论必须包含以下字段：

- current_stage：当前阶段
- current_goal：当前目标
- available_inputs：当前已具备的输入
- missing_deliverables：当前缺失的正式产物
- missing_reviews：当前缺失的审核
- next_agent：建议调用的 Agent
- next_skill：建议调用的 Skill
- needs_business_review：是否需要业务审核
- needs_compliance_review：是否需要合规审核
- can_advance：是否允许进入下一阶段
- parallel_allowed：是否允许并行
- parallel_tasks：可并行任务列表（如不允许则为空）
- block_reason：不允许推进的原因（如允许则为空）

---

## 执行步骤

### 第 1 步：识别任务归属

判断当前请求属于哪种类型：

| 类型 | 判断依据 |
|------|---------|
| 新项目启动 | `project_data/` 下无任何 series 级文件 |
| 阶段推进 | 当前阶段有正式产物，状态为 draft 或 in_review |
| 审核后修改 | 最新审核结论为 rejected |
| 回退后重进 | 有 rejected 状态 + 已有修改记录 |
| 交接下一阶段 | 当前阶段产物为 approved，判断下游条件 |

### 第 2 步：读取当前项目状态

使用 Glob 扫描以下目录，确认文件是否存在：
```
project_data/series/*.yaml
project_data/episodes/ep*/script*.yaml
project_data/episodes/ep*/segments*.yaml
project_data/episodes/ep*/assets*.yaml
project_data/episodes/ep*/videos*.yaml
project_data/episodes/ep*/reviews/*.yaml
```

使用 Read 读取每个存在文件的状态字段。

需确认的信息：
- 当前阶段（参照 `stage-detection-rules.md`）
- 每个已有产物的最新版本号
- 每个已有产物的 status 字段
- 待确认项列表
- 最近审核结果

### 第 3 步：判断当前阶段是否完整

参照 `stage-detection-rules.md`，对当前阶段执行完整性检查：
- 本阶段应产出的正式产物是否都已存在
- 每个产物的关键字段是否填写完整
- 是否存在阻断型缺口（status = unknown、关键字段为空）

### 第 4 步：判断是否需要审核

参照 `phase-entry-exit-matrix.md`，检查当前阶段是否处于审核门禁节点：
- 本阶段完成后是否需要业务审核
- 本阶段完成后是否需要合规审核
- 如果需要，确认审核结论是否已存在且为 approved

### 第 5 步：判断下一步执行者

根据当前阶段和状态，确定：
- 应调用哪个 Agent（参见下方调度映射表）
- 是否需要先补文件
- 是否需要先过审核

**调度映射表：**

| 当前阶段 | 产物状态 | 下一步 Agent |
|---------|---------|-------------|
| 无（新项目） | — | creative-development-agent |
| 创意定义 | draft/in_review | creative-development-agent 继续完善 |
| 创意定义 | 待审核 | business-review-agent + compliance-review-agent |
| 创意定义 | approved | script-development-agent |
| 剧本开发 | draft/in_review | script-development-agent 继续完善 |
| 剧本开发 | 待审核 | business-review-agent + compliance-review-agent |
| 剧本开发 | approved | production-planning-agent |
| 生产规划 | draft/in_review | production-planning-agent 继续完善 |
| 生产规划 | 待审核 | business-review-agent + compliance-review-agent |
| 生产规划 | approved | asset-production-agent + compliance-review-agent（生成前） |
| 资产生产 | 待合规审核 | compliance-review-agent |
| 资产生产 | 待业务审核 | business-review-agent |
| 资产生产 | approved | video-production-agent |
| 视频生产 | 待合规审核 | compliance-review-agent |
| 视频生产 | 待业务审核 | business-review-agent |
| 视频生产 | approved | 项目完成，输出阶段交接摘要 |

### 第 6 步：判断是否允许并行

并行规则：
- 阶段 1/2/3：**禁止并行**
- 阶段 4/5：满足以下全部条件时允许并行
  1. segment 总表状态为 approved
  2. 当前 segment 的图片资产已 approved
  3. 资产生成后合规审核已通过
  4. 当前任务不存在共享资源冲突（如同一资产正在被修改）

并行场景：
- 不同 segment 的资产生产和视频生产可以并行
- 同一 segment 必须先完成资产生产，再启动视频生产

### 第 7 步：输出调度结论

按 `orchestration-output-template.md` 输出固定格式的调度结论。
输出后向用户说明：当前阶段、已完成内容、卡点、下一步。

---

## 约束边界

本 skill **不允许**：
- 直接撰写创意、剧本、segment、prompt 等专业内容
- 直接调用 Dream Maker 或任何执行型生成工具
- 越权修改专业 Agent 的正式产物
- 跳过审核直接放行
- 在信息不足时猜测阶段状态

本 skill **允许**：
- 读取所有项目文件
- 写入调度结论和阶段交接摘要
- 调用其他 Agent 和 Skill

---

## 完成标准

执行本 skill 后，主控 Agent 必须能明确回答以下 7 个问题：

1. **当前阶段**：项目处于 5 个阶段中的哪一个
2. **判断依据**：基于哪些文件和状态字段判断的
3. **缺失项**：还缺什么正式产物或审核
4. **下一步执行者**：应该调用哪个 Agent
5. **审核需求**：是否需要先过业务审核或合规审核
6. **并行判断**：是否允许并行，为什么
7. **推进决策**：是否允许进入下一阶段，如果不允许原因是什么
