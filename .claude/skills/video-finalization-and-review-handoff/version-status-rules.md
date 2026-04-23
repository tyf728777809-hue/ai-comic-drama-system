# 视频版本与状态规则

本文件定义视频文件的版本号递增规则和状态取值规则。

---

## 版本号规则

### 格式

版本号格式：`主版本.次版本`（如 `1.0`、`1.1`、`2.0`）

### 递增规则

| 变更类型 | 版本递增 | 示例 | 说明 |
|---------|---------|------|------|
| 首次生成 | → 1.0 | — | 第一次生成视频任务 |
| 少量任务修改 | 次版本 +1 | 1.0 → 1.1 | 修改 1-3 个任务的 prompt 或策略 |
| 大量任务修改 | 主版本 +1 | 1.0 → 2.0 | 超过半数任务需要调整 |
| 单个视频重试 | 次版本 +1 | 1.0 → 1.1 | 部分视频重新生成 |
| 全部重新生成 | 主版本 +1 | 1.0 → 2.0 | 所有视频重新生成 |
| 定稿整理 | 不递增 | 保持当前版本 | 只做格式整理 |

### 版本号管理规则

1. 每次写入新版本时，必须更新 metadata.version
2. 旧版本文件保留，不做删除或覆盖
3. 文件名中包含版本号：`video-tasks-v1.0.yaml`
4. 下游引用（审核结论）必须引用具体版本号
5. 视频 prompt、任务记录、结果归档共用同一版本号体系

---

## 状态规则

### 状态取值

| 状态 | 含义 | 允许的操作 |
|------|------|-----------|
| `draft` | 草稿，正在生成或修改中 | 编辑 prompt、调整策略 |
| `in_review` | 审核中 | 等待审核结果，不可编辑 |
| `approved` | 已审核通过 | 不可编辑，作为最终交付 |
| `rejected` | 审核未通过 | 根据审核意见修改 |

### 状态流转规则

```
draft → in_review → approved
                ↘ rejected → draft → in_review → ...
```

**流转条件：**

| 转换 | 条件 | 执行者 |
|------|------|-------|
| draft → in_review | 所有视频生成完成，风险检查无 fail | video-production-agent |
| in_review → approved | 合规审核 approved + 业务审核 approved | producer-agent |
| in_review → rejected | 任一审核 rejected | review-agent |
| rejected → draft | 主控决定回退，指定修改方向 | producer-agent |

### 视频生成前后的审核

视频阶段有两组审核：

1. **视频生成前合规审核**：在开始生成视频之前，确保 prompt 和输入策略无合规风险
2. **视频生成后合规审核 + 业务审核**：视频生成完成后，检查结果质量

状态流转：
```
视频任务 draft
  → 视频生成前合规审核
    → 通过 → 开始生成视频
    → 不通过 → 回退修改 prompt
  → 视频生成完成
  → 视频生成后合规审核 + 业务审核
    → 通过 → approved
    → 不通过 → 回退修改
```

---

## 多版本并存规则

1. 同一产物最多保留最近 3 个版本文件
2. 超过 3 个版本的，最早的版本可归档到 `project_data/episodes/epXX/videos/archive/`
3. 视频文件按版本归档：`videos/v1.0/`、`videos/v1.1/`
4. 下游引用始终指向最新的 approved 版本
5. 如果最新版本不是 approved，下游引用上溯到最近的 approved 版本

---

## 变更日志

每个版本文件应在 metadata 中记录变更说明：

```yaml
metadata:
  version: "1.1"
  status: "draft"
  changelog:
    - version: "1.1"
      date: ""
      changes:
        - "修改 VTASK_SEG03 的 prompt（增强动作描述）"
        - "将 VTASK_SEG05 的输入策略从首帧改为首尾帧组合"
      reason: "用户反馈：SEG03 动作不够清晰，SEG05 衔接需要加强"
    - version: "1.0"
      date: ""
      changes:
        - "首次生成完整视频任务"
      reason: "基于资产交接摘要首次生成"
```

---

## 审核结论引用规则

审核结论文件必须引用具体版本号：

```yaml
metadata:
  target_file: "video-tasks-final-v1.0.yaml"
  target_version: "1.0"
  target_status: "in_review"
  review_phase: "post_generation"  # pre_generation | post_generation
```

如果审核结论的 target_version 与当前最新版本不一致，需要主控判断是否需要重新审核。
