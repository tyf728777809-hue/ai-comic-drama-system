# 阶段进出矩阵

本文件定义每个阶段的进入条件、退出条件、必须审核项和状态流转规则。

---

## 阶段总览

| 阶段编号 | 阶段名称 | 串行/并行 | 负责 Agent |
|---------|---------|----------|-----------|
| 1 | 创意定义 | 串行 | creative-development-agent |
| 2 | 剧本开发 | 串行 | script-development-agent |
| 3 | 生产规划 | 串行 | production-planning-agent |
| 4 | 资产生产 | 有限并行 | asset-production-agent |
| 5 | 视频生产 | 有限并行 | video-production-agent |

---

## 阶段 1：创意定义

### 进入条件
- 无前置条件（新项目可直接进入）

### 正式产物
- 创意设定文件（`project_data/series/creative-brief-vX.yaml`）

### 退出条件
- [ ] 创意设定文件已生成
- [ ] 所有关键字段已填写（title, logline, characters, world.setting）
- [ ] pending_items 为空或均为非阻断项
- [ ] status 已更新为 approved

### 必须审核
- [x] 业务审核
- [x] 合规审核

### 退出流程
1. 创意设定 status → in_review
2. 调用 business-review-agent
3. 调用 compliance-review-agent
4. 两项均 approved → status → approved → 允许进入阶段 2
5. 任一 rejected → 使用 producer-recovery-control 处理回退

---

## 阶段 2：剧本开发

### 进入条件
- [ ] 阶段 1 创意设定 status = approved
- [ ] 业务审核 approved
- [ ] 合规审核 approved

### 正式产物
- 剧本文件（`project_data/episodes/epXX/script-vX.yaml`）

### 退出条件
- [ ] 剧本文件已生成
- [ ] 所有场景有 action_description 和 emotion
- [ ] pending_items 为空或均为非阻断项
- [ ] status 已更新为 approved

### 必须审核
- [x] 业务审核
- [x] 合规审核

### 退出流程
1. 剧本 status → in_review
2. 调用 business-review-agent
3. 调用 compliance-review-agent
4. 两项均 approved → status → approved → 允许进入阶段 3
5. 任一 rejected → 使用 producer-recovery-control 处理回退

---

## 阶段 3：生产规划

### 进入条件
- [ ] 阶段 2 剧本 status = approved
- [ ] 业务审核 approved
- [ ] 合规审核 approved

### 正式产物
- Segment 总表（`project_data/episodes/epXX/segments-vX.yaml`）
- 单段任务文件（`project_data/episodes/epXX/segment-tasks/`）

### 退出条件
- [ ] Segment 总表已生成
- [ ] 所有 segment 有 key_visual、shot_type、camera_movement
- [ ] 衔接设计已填写
- [ ] pending_items 为空或均为非阻断项
- [ ] status 已更新为 approved

### 必须审核
- [x] 业务审核
- [ ] 合规审核（本节点不强制，但在阶段 4 前需要）

### 退出流程
1. Segment 总表 status → in_review
2. 调用 business-review-agent
3. 业务审核 approved → status → approved → 允许进入阶段 4
4. rejected → 使用 producer-recovery-control 处理回退

---

## 阶段 4：资产生产

### 进入条件
- [ ] 阶段 3 Segment 总表 status = approved
- [ ] 业务审核 approved
- [ ] 资产生成前合规审核 approved

### 正式产物
- 资产清单（`project_data/episodes/epXX/asset-manifest-vX.yaml`）
- 图片文件（`project_data/episodes/epXX/assets/images/`）
- 图片结果归档（`project_data/episodes/epXX/asset-archive-vX.yaml`）

### 退出条件
- [ ] 资产清单覆盖所有 segment
- [ ] 所有图片已生成并归档
- [ ] 所有 asset 的 quality_check = pass
- [ ] pending_items 为空或均为非阻断项
- [ ] status 已更新为 approved

### 必须审核
- [x] 业务审核（资产生成后）
- [x] 合规审核（资产生成前 + 生成后）

### 退出流程
1. 合规审核（生成前）通过 → 启动资产生产
2. 资产生产完成 → status → in_review
3. 调用 compliance-review-agent（生成后）
4. 调用 business-review-agent（生成后）
5. 两项均 approved → status → approved → 允许进入阶段 5
6. 任一 rejected → 使用 producer-recovery-control 处理回退

### 并行条件
- 不同 segment 的资产可并行生产
- 同一 segment 的所有资产必须一起完成后再进入该 segment 的审核

---

## 阶段 5：视频生产

### 进入条件
- [ ] 阶段 4 对应 segment 的图片资产 status = approved
- [ ] 业务审核 approved
- [ ] 合规审核 approved
- [ ] 视频生成前合规审核 approved

### 正式产物
- 视频文件（`project_data/episodes/epXX/videos/`）
- 视频结果归档（`project_data/episodes/epXX/video-archive-vX.yaml`）

### 退出条件
- [ ] 视频覆盖所有 segment
- [ ] 所有视频已生成并归档
- [ ] 所有 result 的 quality_check = pass
- [ ] 衔接连贯性检查通过
- [ ] pending_items 为空或均为非阻断项
- [ ] status 已更新为 approved

### 必须审核
- [x] 业务审核（视频生成后）
- [x] 合规审核（视频生成前 + 生成后）

### 退出流程
1. 合规审核（生成前）通过 → 启动视频生产
2. 视频生产完成 → status → in_review
3. 调用 compliance-review-agent（生成后）
4. 调用 business-review-agent（生成后）
5. 两项均 approved → status → approved → 项目完成
6. 输出阶段交接摘要
7. 任一 rejected → 使用 producer-recovery-control 处理回退

### 并行条件
- 不同 segment 的视频可并行生产（前提：该 segment 的图片已 approved）
- 同一 segment 必须先完成资产生产，再启动视频生产

---

## 状态流转规则

| 当前状态 | 允许的操作 |
|---------|-----------|
| draft | 编辑内容、补充字段 |
| in_review | 等待审核结果，不可编辑内容 |
| approved | 锁定，作为下游输入使用 |
| rejected | 退回修改，修改后重新提交审核 |

**硬性规则：**
- draft 和 in_review 状态不得作为下游阶段的输入
- approved 是唯一允许跨阶段流转的状态
- rejected 必须触发回退处理流程
