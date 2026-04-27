---
name: script-finalization-and-handoff
description: 剧本定稿与交接方法包。负责将成熟剧本整理为正式文件、输出确认前复盘摘要、生成生产规划阶段交接摘要、管理版本与状态。适用于剧本开发阶段完成后进入定稿和交接。
---

# Skill：script-finalization-and-handoff

## 适用场景

当 script-development-agent 判断剧本已基本成熟、准备进入定稿和交接时使用本 skill。

典型触发条件：
- 剧本结构检查和平台适配检查均通过
- 用户确认不再需要大幅改稿
- 准备提交审核
- 需要为生产规划阶段准备交接材料

**不适用**：还在写剧本、改稿、做检查 → 使用 `market-oriented-script-development`

---

## 核心目标

1. 将成熟剧本整理为固定格式的正式文件
2. 为用户输出可确认的复盘摘要
3. 为生产规划阶段输出完整的交接摘要
4. 正确管理版本号和确认状态

---

## 输入

| 输入 | 路径 | 用途 |
|------|------|------|
| 当前最新剧本 | `project_data/projects/{project_id}/episodes/epXX/script/script-vX.yaml` | 定稿整理的基准 |
| 故事梗概 | `project_data/projects/{project_id}/series/synopsis-vX.yaml` | 复盘参考 |
| 分集规划 | `project_data/projects/{project_id}/series/episode-plan-vX.yaml` | 复盘参考 |
| 结构检查结果 | 剧本文件内 structure_check 字段 | 确认无阻断问题 |
| 平台适配检查结果 | 剧本文件内 platform_check 字段 | 确认无阻断问题 |
| 风险检查结果 | 剧本文件内 risks 字段 | 确认无阻断风险 |
| 用户反馈 | 聊天上下文 | 确认是否可以定稿 |

---

## 输出

| 产物 | 输出路径 | 说明 |
|------|---------|------|
| 正式剧本文件 | `project_data/projects/{project_id}/episodes/epXX/script/script-vX.yaml` | 按模板整理的定稿版本 |
| 确认前复盘摘要 | `project_data/projects/{project_id}/episodes/epXX/review-summary-vX.yaml` | 给用户确认的摘要 |
| 生产规划交接摘要 | `project_data/projects/{project_id}/episodes/epXX/segments/handoff-script-to-planning-vX.yaml` | 给生产规划阶段的交接 |

---

## 执行步骤

### 第 1 步：读取当前最新剧本版本

读取 `project_data/projects/{project_id}/episodes/epXX/` 下的最新剧本文件。
确认当前版本号和 status。

### 第 2 步：判断是否具备定稿条件

检查以下条件是否全部满足：

| 条件 | 标准 |
|------|------|
| 结构检查 | structure_check 中无 fail 项 |
| 平台适配检查 | platform_check 中无 fail 项 |
| 风险检查 | risks 中无 fail 项 |
| 待确认项 | pending_items 中无阻断型项目 |
| 用户确认 | 用户明确表示不再需要大幅改稿 |

如果条件不满足 → 返回 `market-oriented-script-development` 继续改稿。
如果条件满足 → 继续定稿。

### 第 3 步：整理正式剧本文件

使用 `final-script-template.md` 模板整理正式剧本文件：
- 补全所有字段的最终值
- 确认场景顺序完整
- 确认钩子/反转/结尾扣子都已标注
- 清理冗余注释
- 更新版本号和 status

将 status 设为 `in_review`（等待用户确认）。

### 第 4 步：生成确认前复盘摘要

使用 `review-summary-template.md` 模板生成复盘摘要：
- 已确认内容清单
- 待确认内容清单
- 主要风险提示
- 确认后下一步说明

将复盘摘要写入 `project_data/projects/{project_id}/episodes/epXX/review-summary-vX.yaml`。

### 第 5 步：生成生产规划阶段交接摘要

使用 `planning-handoff-template.md` 模板生成交接摘要：
- 本集核心内容
- 关键角色和视觉特征
- 关键情绪节点和画面点
- 已锁定设定
- 可细化空间
- 适合拆段强化的内容
- 生产风险提示

将交接摘要写入 `project_data/projects/{project_id}/episodes/epXX/segments/handoff-script-to-planning-vX.yaml`。

### 第 6 步：更新版本号与状态字段

参照 `version-status-rules.md`：
- 递增版本号（如 v1.0 → v2.0，或 v1.0 → v1.1）
- 更新 status 为当前正确状态
- 更新 updated_at 时间戳
- 在 metadata 中记录变更说明

---

## 约束边界

本 skill **不允许**：
- 继续做创意发散
- 直接进入拆段执行
- 越权做生产规划阶段工作
- 调用 Dream Maker 或任何执行型生成工具
- 修改已 approved 的创意设定

本 skill **允许**：
- 读取所有项目文件
- 写入正式剧本文件、复盘摘要、交接摘要
- 更新版本号和状态字段

---

## 完成标准

执行本 skill 后，必须能明确回答：

1. **定稿条件**：当前剧本是否已达到定稿条件
2. **版本号**：当前正式版本号是什么
3. **确认状态**：当前 status 是什么
4. **交接条件**：是否已具备交给生产规划阶段的条件
