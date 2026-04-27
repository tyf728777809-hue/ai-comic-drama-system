---
name: producer-recovery-control
description: 主控 Agent 的失败恢复方法包。负责识别失败类型、定位回退节点、指定责任 Agent、生成修复路径和重入清单。适用于审核失败、生成失败、内容缺失等异常场景。
---

# Skill：producer-recovery-control

## 适用场景

当项目流程出现中断或失败时使用本 skill。

典型触发条件：
- 业务审核结论 `conclusion.verdict = fail`
- 合规审核结论 `conclusion.verdict = fail`
- 正式产物文件结构不完整
- 图像生成失败或质量不通过
- 视频生成失败或质量不通过
- 发现上下游依赖冲突
- 发现版本或状态不一致

**不适用**：项目正常推进、无失败 → 使用 `producer-stage-orchestration`

---

## 核心目标

1. 精确识别失败类型
2. 定位失败发生点和最近可修改节点
3. 判断回退影响范围
4. 指定责任 Agent 和修复路径
5. 生成完整的重入检查清单

---

## 输入

| 输入来源 | 路径 | 用途 |
|---------|------|------|
| 失败结论 | 审核文件 / 生成结果文件 | 识别失败类型和原因 |
| 当前阶段产物 | `project_data/projects/{project_id}/episodes/epXX/` | 定位失败发生点 |
| 审核结果 | `project_data/projects/{project_id}/episodes/epXX/reviews/` | 确认是哪种审核失败 |
| 上游依赖 | 上游阶段的 approved 文件 | 判断回退影响范围 |
| 最近有效版本 | 同一产物的历史版本 | 确定回退目标版本 |

读取规则：
- 优先读取失败结论文件（审核结论或生成结果）
- 回溯读取失败产物对应的上游依赖
- 检查是否存在最近一个 approved 版本

---

## 输出

本 skill 输出一个固定格式的恢复结论，包含：

- failure_type：失败类型（见 `failure-type-guide.md`）
- failure_stage：失败发生阶段
- failure_reason：失败原因
- fallback_node：建议回退节点
- fallback_reason：为什么回退到这个节点
- responsible_agent：责任 Agent
- repair_scope：修复范围（局部修复 / 整段重做）
- repair_path：修复后需要重跑的步骤链
- reentry_audits：修复后必须重新经过的审核
- reentry_checklist：重入前必须完成的检查项（见 `reentry-checklist.md`）

---

## 执行步骤

### 第 1 步：识别失败类型

读取最新失败结论，对照 `failure-type-guide.md` 分类：

| 失败类型 | 识别方式 |
|---------|---------|
| 业务审核失败 | 审核结论 verdict = fail，reviewer = business-review-agent |
| 合规审核失败 | 审核结论 verdict = fail，reviewer = compliance-review-agent |
| 内容缺失 | 文件存在但关键字段为空，或文件不存在但阶段标记为进行中 |
| 图像生成失败 | 资产 quality_check = fail，或 file_path 为空 |
| 视频生成失败 | 视频 quality_check = fail，或 file_path 为空 |
| 依赖冲突 | 下游引用了 rejected 或 draft 状态的上游产物 |
| 版本冲突 | 同一产物存在多个版本且状态不一致 |

如果失败类型不明确，标记为"未分类"并记录原始错误信息。

### 第 2 步：判断失败发生点

确定失败具体发生在哪个阶段、哪个产物：

1. 读取失败结论中引用的目标文件
2. 确认该文件属于哪个阶段
3. 确认该文件当前 status
4. 确认该文件的版本号

### 第 3 步：定位最近可修改节点

**回退原则：回退到最近一个需要修改的节点，不回退到不需要改的阶段。**

判断逻辑：
1. 失败是否可以只修改当前阶段产物解决？
   - 可以 → 回退节点 = 当前阶段
   - 不可以 → 继续向上游追溯
2. 修改是否涉及上游产物的内容变更？
   - 不涉及 → 回退节点 = 当前阶段
   - 涉及 → 回退节点 = 上游阶段
3. 合规失败是否涉及根本性设定问题？
   - 是 → 回退到创意定义阶段
   - 否 → 回退到最小必要节点

### 第 4 步：判断影响范围

确认回退会影响哪些下游阶段：
- 列出所有依赖回退节点产物的下游阶段
- 标记哪些下游产物需要重新生成
- 标记哪些下游审核需要重新执行

### 第 5 步：判断责任 Agent

根据失败类型和回退节点，指定负责修复的 Agent：

| 失败类型 | 回退节点 | 责任 Agent |
|---------|---------|-----------|
| 业务审核失败 | 创意定义 | creative-development-agent |
| 业务审核失败 | 剧本开发 | script-development-agent |
| 业务审核失败 | 生产规划 | production-planning-agent |
| 业务审核失败 | 资产生产 | asset-production-agent |
| 业务审核失败 | 视频生产 | video-production-agent |
| 合规审核失败 | 创意定义 | creative-development-agent |
| 合规审核失败 | 剧本开发 | script-development-agent |
| 内容缺失 | 对应阶段 | 对应阶段 Agent |
| 图像生成失败 | 资产生产 | asset-production-agent |
| 视频生成失败 | 视频生产 | video-production-agent |
| 依赖冲突 | 产生冲突的阶段 | 对应阶段 Agent |
| 版本冲突 | 产生冲突的阶段 | 对应阶段 Agent |

### 第 6 步：生成修复路径

输出从修复到恢复的完整步骤链：

```
修复路径示例：
1. [creative-development-agent] 修改创意设定中的 XXX
2. [producer-agent] 更新创意设定版本号，status → draft
3. [creative-development-agent] 补充 YYY 字段
4. [producer-agent] 将创意设定 status → in_review
5. [business-review-agent] 重新执行业务审核
6. [compliance-review-agent] 重新执行合规审核
7. [producer-agent] 确认两项审核均 approved
8. [producer-agent] 使用 producer-stage-orchestration 判断下一步
```

### 第 7 步：生成重入检查清单

参照 `reentry-checklist.md`，输出修复完成后重新进入主流程前的检查清单：
- 需要重过的审核列表
- 需要更新的状态字段
- 需要重新生成的下游产物
- 需要更新的版本号

---

## 约束边界

本 skill **不允许**：
- 直接修改专业内容
- 直接调用生成工具
- 跳过审核直接放行
- 在没有依据时默认建议"重试"
- 回退时跳过必要的中间审核

本 skill **允许**：
- 读取所有项目文件
- 更新产物状态字段
- 写入恢复结论和重入清单
- 调用其他 Agent 和 Skill

---

## 特殊规则

### 合规失败优先级
合规审核失败比业务审核失败优先级更高：
- 合规失败 → 必须优先回退，不得继续任何生成操作
- 如果合规和业务同时失败 → 先处理合规失败

### 局部修复 vs 整段重做

| 情况 | 判定 | 依据 |
|------|------|------|
| 只有少量字段需要补充 | 局部修复 | 不影响整体结构 |
| 关键设定需要变更 | 整段重做 | 影响下游所有依赖 |
| 角色核心设定变更 | 整段重做 | 影响剧本和视觉 |
| 单张图片质量问题 | 局部修复 | 不影响其他资产 |
| 视觉风格整体不一致 | 整段重做 | 需要统一调整 |
| 版权/IP 风险 | 整段重做 | 涉及根本性内容变更 |

---

## 完成标准

执行本 skill 后，主控 Agent 必须能明确回答以下 6 个问题：

1. **失败位置**：失败发生在哪个阶段、哪个产物
2. **失败原因**：为什么失败，失败类型是什么
3. **回退目标**：应该退回到哪个节点，为什么
4. **责任 Agent**：谁负责修复
5. **修复后路径**：修完后怎么继续，需要重跑哪些步骤
6. **重入审核**：修复后必须重新经过哪些审核
