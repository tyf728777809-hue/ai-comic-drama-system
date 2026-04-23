---
name: segment-finalization-and-handoff
description: 生产规划定稿与交接方法包。负责将成熟的 segment 规划整理为正式总表和单段任务文件、输出确认前复盘摘要、生成资产生产阶段交接摘要、管理版本与状态。适用于生产规划完成后的定稿和交接。
---

# 生产规划定稿与交接

## 适用场景

当 `segment-planning-and-structuring` skill 完成拆解后，本 skill 负责将结果整理为正式文件并交接给资产生产阶段。

不适用于拆解阶段本身、资产 prompt 生成、视频生成。

## 核心目标

1. 将成熟的生产规划整理为固定格式的正式文件
2. 给用户一个适合确认的复盘摘要
3. 把规划阶段结果打包交给资产生产阶段
4. 管理版本号和确认状态
5. 明确哪些内容已锁定、哪些仍可细化

## 输入

| 输入项 | 来源 | 必需 |
|--------|------|------|
| segment 规划结果 | segment-planning-and-structuring 输出 | 是 |
| 连续性风险提示 | segment-planning-and-structuring 输出 | 是 |
| 生产风险提示 | segment-planning-and-structuring 输出 | 是 |
| 用户反馈 | 用户指令 | 否 |
| 当前版本号 | 规划文件 metadata | 是 |
| 当前状态 | 规划文件 metadata | 是 |

## 输出

| 输出项 | 文件 | 说明 |
|--------|------|------|
| 正式 segment 总表 | `project_data/episodes/epXX/segments/segments-v{version}.yaml` | 所有 segment 概览 |
| 正式单段任务文件 | `project_data/episodes/epXX/segments/segment-tasks/epXX-SEG{NN}-v{version}.yaml` | 每个 segment 详细任务 |
| 确认前复盘摘要 | `project_data/episodes/epXX/segments/planning-review-summary-v{version}.yaml` | 面向用户的确认材料 |
| 资产生产阶段交接摘要 | `project_data/episodes/epXX/segments/asset-handoff-v{version}.yaml` | 面向资产生产阶段的交接 |

## 执行步骤

### 步骤 1：读取当前最新生产规划版本

1. 读取 segment-planning-and-structuring 输出的所有 segment 数据
2. 读取连续性风险和生产风险提示
3. 读取用户反馈（如有）
4. 确认当前版本号和状态

### 步骤 2：判断是否具备定稿条件

定稿条件检查：

| 条件 | 说明 |
|------|------|
| 所有 segment 编号完整 | 无缺失编号 |
| 所有 segment 任务信息完整 | 无关键字段为空 |
| 无 high 级别连续性风险未解决 | 或已标注为"已知风险" |
| 无 high 级别生产风险未解决 | 或已标注为"已知风险" |
| 无阻断型待确认项 | 所有关键问题已确认 |

如果不具备定稿条件：
- 列出缺失项
- 返回拆解 skill 继续修正
- 不强行定稿

### 步骤 3：整理正式 segment 总表

1. 按 [segment-index-template.md](segment-index-template.md) 填写正式 segment 总表
2. 确保以下字段完整：
   - metadata：series_id、episode_id、版本号、状态
   - summary：总段数、总时长、按场景/情绪分布统计
   - segments：每个 segment 的概览信息
   - continuity_map：相邻段衔接关系
   - risks：风险汇总
3. 更新版本号按 [version-status-rules.md](version-status-rules.md) 规则

### 步骤 4：整理正式单段任务文件

1. 按 [segment-task-template.md](segment-task-template.md) 为每个 segment 生成正式任务文件
2. 确保每个文件包含完整的任务信息
3. 确保相邻段的衔接信息一致（connects_from / connects_to 互相引用）

### 步骤 5：生成确认前复盘摘要

1. 按 [planning-review-summary-template.md](planning-review-summary-template.md) 生成复盘摘要
2. 复盘摘要面向用户，必须能让用户快速了解：
   - 当前已确认什么
   - 当前还有什么待确认
   - 主要风险
   - 如果确认，下一步是什么
   - 如果不确认，可以怎么调整

### 步骤 6：生成资产生产阶段交接摘要

1. 按 [asset-handoff-template.md](asset-handoff-template.md) 生成交接摘要
2. 交接摘要面向资产生产 Agent，必须能让其直接开始资产规划：
   - 本集共拆成多少段
   - 每段的总体任务特征
   - 哪些段落风险较高
   - 哪些段落适合优先出资产
   - 哪些设定不能改
   - 哪些地方仍可细化

### 步骤 7：更新版本号与状态字段

1. 根据 [version-status-rules.md](version-status-rules.md) 更新版本号和状态：
   - 定稿文件 status 设为 draft（等待用户确认）
   - 用户确认后更新为 in_review（提交审核）
   - 审核通过后更新为 approved
2. 写入 changelog 记录本次定稿

## 约束边界

| 约束 | 说明 |
|------|------|
| 不继续重拆 | 定稿阶段不做大规模重拆，只做格式整理 |
| 不越权做资产工作 | 不写资产 prompt，不规划资产生成 |
| 不调用工具 | 不调用 Dream Maker 或任何执行型工具 |
| 不推进流程 | 只输出定稿结果，由主控决定推进 |

## 完成标准

执行完成后，必须能明确回答以下 4 个问题：

1. 是否达到定稿条件？ → 已检查并列出条件
2. 正式版本号是什么？ → 已更新
3. 确认状态是什么？ → 已更新
4. 是否具备交给资产生产的条件？ → 交接摘要已完成
