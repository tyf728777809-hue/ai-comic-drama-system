# 阶段检测规则

本文件定义如何根据项目文件判断当前所处阶段。

---

## 检测原则

1. 检测基于文件存在性 + 文件内 status 字段，不靠猜测
2. 如果文件不存在，视为该阶段未完成
3. 如果文件存在但 status 为 draft 或 in_review，视为当前阶段进行中
4. 如果文件存在且 status 为 approved，视为该阶段已完成
5. 阶段判断从后往前检查：先检查下游阶段，再检查上游阶段

---

## 阶段判定流程

按以下顺序依次检查。命中第一个满足条件的即停止。

### 检查 1：项目是否为空

```
扫描 project_data/series/ 目录
扫描 project_data/episodes/ 目录
```

- 如果两个目录均为空 → **阶段：未启动（新项目）**
- 最小进入条件：无
- 下一步：启动创意定义阶段

### 检查 2：创意定义阶段

```
读取 project_data/series/ 下的创意设定文件
检查 status 字段
```

| 条件 | 判定 |
|------|------|
| 文件不存在 | 阶段：创意定义（未开始） |
| status = draft | 阶段：创意定义（进行中） |
| status = in_review | 阶段：创意定义（审核中） |
| status = rejected | 阶段：创意定义（已退回） |
| status = approved | 创意定义已完成，继续检查下游 |

**创意设定最小完成条件：**
- title 字段已填写
- logline 字段已填写
- characters 列表至少有 1 个角色
- world.setting 字段已填写
- pending_items 为空或均为非阻断项

### 检查 3：剧本开发阶段

```
读取 project_data/episodes/epXX/ 下的剧本文件
检查 status 字段
```

| 条件 | 判定 |
|------|------|
| 文件不存在 | 阶段：剧本开发（未开始） |
| status = draft | 阶段：剧本开发（进行中） |
| status = in_review | 阶段：剧本开发（审核中） |
| status = rejected | 阶段：剧本开发（已退回） |
| status = approved | 剧本开发已完成，继续检查下游 |

**剧本最小完成条件：**
- synopsis 字段已填写
- scenes 列表至少有 1 个场景
- 每个场景有 action_description 和 emotion
- pending_items 为空或均为非阻断项

### 检查 4：生产规划阶段

```
读取 project_data/episodes/epXX/ 下的 segment 总表文件
检查 status 字段
```

| 条件 | 判定 |
|------|------|
| 文件不存在 | 阶段：生产规划（未开始） |
| status = draft | 阶段：生产规划（进行中） |
| status = in_review | 阶段：生产规划（审核中） |
| status = rejected | 阶段：生产规划（已退回） |
| status = approved | 生产规划已完成，继续检查下游 |

**Segment 总表最小完成条件：**
- segments 列表至少有 1 个 segment
- 每个 segment 有 key_visual、shot_type、camera_movement
- 每个 segment 有 transition_in 和 transition_out
- total_segments 字段已填写
- pending_items 为空或均为非阻断项

### 检查 5：资产生产阶段

```
读取 project_data/episodes/epXX/ 下的资产清单和图片结果归档
检查各自 status 字段
```

| 条件 | 判定 |
|------|------|
| 文件不存在 | 阶段：资产生产（未开始） |
| status = draft | 阶段：资产生产（进行中） |
| status = in_review | 阶段：资产生产（审核中） |
| status = rejected | 阶段：资产生产（已退回） |
| status = approved | 资产生产已完成，继续检查下游 |

**资产清单最小完成条件：**
- assets 列表覆盖所有 segment
- 每个 asset 有 prompt 字段
- 每个 asset 有 file_path 字段（已生成）
- 所有 asset 的 quality_check 为 pass
- pending_items 为空或均为非阻断项

### 检查 6：视频生产阶段

```
读取 project_data/episodes/epXX/ 下的视频结果归档
检查 status 字段
```

| 条件 | 判定 |
|------|------|
| 文件不存在 | 阶段：视频生产（未开始） |
| status = draft | 阶段：视频生产（进行中） |
| status = in_review | 阶段：视频生产（审核中） |
| status = rejected | 阶段：视频生产（已退回） |
| status = approved | 视频生产已完成 |

**视频结果最小完成条件：**
- results 列表覆盖所有 segment
- 每个 result 有 file_path 字段（已生成）
- 所有 result 的 quality_check 为 pass
- pending_items 为空或均为非阻断项

---

## 多集项目处理

当项目包含多集时：
- 每集独立判断阶段
- 系列级设定（创意定义）为共享上游
- 各集的剧本、segment、资产、视频独立推进
- 主控按集输出调度结论
