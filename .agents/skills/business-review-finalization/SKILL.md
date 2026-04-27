---
name: business-review-finalization
description: 审核定稿与交接方法包。负责将业务审核结果整理为正式审核报告、输出修改建议、生成主控交接摘要、管理版本与状态。适用于业务审核完成后的定稿和交接。
---

# 审核定稿与交接

## 适用场景

当 `business-evaluation-and-decision` skill 完成质量评估后，本 skill 负责将评估结果整理为正式文件并交接给主控 Agent。

不适用于评估阶段本身、合规审核、内容修改。

## 核心目标

1. 将业务审核结果整理为固定格式的正式文件
2. 输出明确的修改建议和修复路径
3. 生成主控 Agent 可直接消费的交接摘要
4. 管理审核结论的版本号和确认状态
5. 明确后续动作（放行、附条件放行、退回重做）

## 输入

| 输入项 | 来源 | 必需 |
|--------|------|------|
| 审核结论 | business-evaluation-and-decision 输出 | 是 |
| 缺陷归类结果 | business-evaluation-and-decision 输出 | 是 |
| 审核对象文件路径 | 主控调度指令 | 是 |
| 当前版本号 | 审核对象 metadata | 是 |
| 当前状态 | 审核对象 metadata | 是 |
| 历史审核记录 | reviews/ 目录 | 否 |

## 输出

| 输出项 | 文件 | 说明 |
|--------|------|------|
| 正式审核报告 | review-report-template.md | 完整审核记录 |
| 修改建议报告 | revision-advice-template.md | 面向责任 Agent 的修改指南 |
| 主控交接摘要 | producer-handoff-template.md | 面向主控的决策依据 |

## 执行步骤

### 步骤 1：读取审核结果

1. 接收 `business-evaluation-and-decision` skill 的评估结果：
   - 审核结论（pass / pass_with_revisions / fail）
   - 风险等级（high / medium / low）
   - 缺陷列表（含 blocking / major / minor 分类）
   - 各维度评分（pass / warning / fail）
   - 放行判断（allowed / not_allowed）
2. 确认审核对象元信息：文件路径、版本号、状态

### 步骤 2：整理正式审核报告

1. 按 [review-report-template.md](review-report-template.md) 填写正式审核报告
2. 确保以下字段完整：
   - metadata：series_id、episode_id、审核对象信息、版本号
   - 审核结论：结论、风险等级、放行判断
   - 维度评分：每个维度的 pass / warning / fail 及说明
   - 缺陷列表：按 blocking → major → minor 排序
3. 审核报告的版本号按 [version-status-rules.md](version-status-rules.md) 规则递增

### 步骤 3：整理修改建议

1. 如果结论为 pass_with_revisions 或 fail，按 [revision-advice-template.md](revision-advice-template.md) 生成修改建议
2. 修改建议必须包含：
   - 每个缺陷的具体修改方向
   - 建议的修改范围（局部 / 大幅返工）
   - 建议的责任 Agent
   - 修改后是否需要重审
   - 修改时限建议
3. 如果结论为 pass，修改建议部分标记为"无需修改"

### 步骤 4：生成主控交接摘要

1. 按 [producer-handoff-template.md](producer-handoff-template.md) 生成给主控 Agent 的交接摘要
2. 交接摘要必须能让主控直接做出推进或回退决策：
   - 当前审核结论
   - 是否可放行
   - 如果不可放行，回退到哪个阶段、由谁修复
   - 修复后是否需要重审
   - 跨阶段影响评估

### 步骤 5：更新版本与状态

1. 根据 [version-status-rules.md](version-status-rules.md) 更新版本号和状态：
   - pass → 审核报告 status 设为 approved
   - pass_with_revisions → 审核报告 status 设为 in_review，待修改后重审
   - fail → 审核报告 status 设为 rejected
2. 更新审核对象的 status：
   - pass → approved
   - pass_with_revisions → 保持 in_review
   - fail → rejected
3. 写入 changelog 记录本次审核

## 约束边界

| 约束 | 说明 |
|------|------|
| 不修改上游正式文件 | 审核定稿只修改审核结论文件和交接摘要 |
| 不推进下一阶段 | 只输出审核结论，由主控决定推进或回退 |
| 不代替主控做流程控制 | 回退决策由主控执行 |
| 不混入内容修改 | 只输出修改建议，不做实际内容修改 |
| 不做合规判断 | 合规审核由 compliance-review-agent 负责 |

## 完成标准

执行完成后，必须能明确回答以下 3 个问题：

1. 审核结果是否已正式落档？ → 已生成正式审核报告
2. 主控是否可以直接消费结论？ → 已生成主控交接摘要，含明确决策依据
3. 是否已明确修复路径和重审要求？ → 已生成修改建议（如需要）
