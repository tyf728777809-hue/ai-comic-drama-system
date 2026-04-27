# AI 漫剧自动生产系统 — 系统总览

## 系统架构

本系统基于 Codex 的 Agent + Skill 架构，实现从创意到成片的完整漫剧生产流水线。

```text
用户 → 主控 Agent → 调度专业 Agent → 各阶段生产 → 审核 → 推进 / 回退
```

系统以 `.agents/` 作为唯一 canonical 规则源，所有正式产物通过 `schemas/` 和 `tools/workflow_guard.py` 进行校验。

## Agent 一览表

| # | Agent | 文件 | 职责 |
|---|-------|------|------|
| 1 | producer-agent | `.agents/agents/producer-agent.md` | 总控调度、阶段流转、审核门禁、回退控制 |
| 2 | creative-development-agent | `.agents/agents/creative-development-agent.md` | 创意访谈、方向收敛、创意设定输出 |
| 3 | script-development-agent | `.agents/agents/script-development-agent.md` | 梗概、分集、单集剧本、改稿 |
| 4 | production-planning-agent | `.agents/agents/production-planning-agent.md` | 15 秒分段、segment 任务单、衔接设计 |
| 5 | asset-production-agent | `.agents/agents/asset-production-agent.md` | 资产清单、复用判断、生图 prompt、图片归档 |
| 6 | video-production-agent | `.agents/agents/video-production-agent.md` | 视频 prompt、首尾帧策略、视频生成与归档 |
| 7 | business-review-agent | `.agents/agents/business-review-agent.md` | 阶段质量判断、放行或退回 |
| 8 | compliance-review-agent | `.agents/agents/compliance-review-agent.md` | 版权、人物权、敏感内容、平台限制等合规判断 |

## Skill 一览表

每个 Agent 包含 2 个 Skills（一个负责执行，一个负责定稿 / 交接）：

| Agent | Skill 1（执行） | Skill 2（定稿交接） |
|-------|----------------|-------------------|
| producer-agent | producer-stage-orchestration | producer-recovery-control |
| creative-development-agent | creative-discovery-and-convergence | creative-bible-and-handoff |
| script-development-agent | market-oriented-script-development | script-finalization-and-handoff |
| production-planning-agent | segment-planning-and-structuring | segment-finalization-and-handoff |
| asset-production-agent | asset-planning-and-prompting | asset-finalization-and-handoff |
| video-production-agent | video-generation-and-control | video-finalization-and-review-handoff |
| business-review-agent | business-evaluation-and-decision | business-review-finalization |
| compliance-review-agent | compliance-risk-evaluation | compliance-finalization-and-handoff |

## 阶段流转

```text
[创意定义] → [剧本开发] → [生产规划] → [资产生产] → [视频生产]
```

- 前三阶段严格串行，必须整阶段 approved 才能进入下游。
- 后两阶段按 segment 级推进：不同 segment 可并行，但每个 segment 仍按“规划 → 资产 → 审核 → 视频 → 审核”顺序闭环。
- 合规审核拥有一票否决权。

## 审核门禁矩阵

| 审核节点 | 业务审核 | 合规审核 |
|---------|---------|---------|
| 创意设定完成后 | 必须 | 必须 |
| 剧本完成后 | 必须 | 必须 |
| segment 总表完成后 | 必须 | 必须 |
| 资产生成前 | — | 必须 |
| 资产生成后 | 必须 | 必须 |
| 视频生成前 | — | 必须 |
| 视频生成后 | 必须 | 必须 |

审核报告的 `report_status` 仅表示报告文件是否整理完成；推进是否放行只看 `conclusion.verdict` 与 `gate_decision`。

## 目录约定

```text
漫剧生产系统/
├── README.md
├── AGENTS.md
├── .agents/
│   ├── agents/
│   ├── skills/
│   └── settings.json
├── schemas/
├── templates/
├── tools/
│   └── workflow_guard.py
├── project_data/
│   ├── series/
│   │   ├── reviews/
│   │   │   ├── business/
│   │   │   └── compliance/
│   │   └── ...
│   └── episodes/epXX/
│       ├── script/
│       ├── segments/
│       │   └── tasks/
│       ├── assets/
│       │   └── images/
│       ├── videos/
│       ├── reviews/
│       │   ├── business/
│       │   └── compliance/
│       └── orchestration/
└── docs/
```

## 正式产物命名

| 阶段 | 正式文件 |
|------|---------|
| 创意定义 | `project_data/projects/{project_id}/series/creative-bible-v{version}.yaml` |
| 剧本开发 | `project_data/projects/{project_id}/series/synopsis-v{version}.yaml`、`project_data/projects/{project_id}/series/episode-plan-v{version}.yaml`、`project_data/projects/{project_id}/episodes/epXX/script/script-v{version}.yaml` |
| 生产规划 | `project_data/projects/{project_id}/episodes/epXX/segments/segments-v{version}.yaml`、`project_data/projects/{project_id}/episodes/epXX/segments/tasks/{episode_id}-SEG{NN}-v{version}.yaml` |
| 资产生产 | `project_data/projects/{project_id}/episodes/epXX/assets/asset-manifest-v{version}.yaml`、`asset-prompts-v{version}.yaml`、`asset-index-v{version}.yaml`、`asset-archive-v{version}.yaml` |
| 视频生产 | `project_data/projects/{project_id}/episodes/epXX/videos/video-prompts-v{version}.yaml`、`video-tasks-v{version}.yaml`、`video-tasks-final-v{version}.yaml`、`video-archive-v{version}.yaml` |
| 调度 | `project_data/projects/{project_id}/episodes/epXX/orchestration/orchestration-result-v{version}.yaml`、`segment-ledger-v{version}.yaml` |

## 校验与兼容

- `tools/workflow_guard.py validate`：校验目录、命名、schema、状态流转和引用关系。
- `tools/workflow_guard.py status`：只读扫描项目文件，输出 episode 级调度结论和 segment ledger。
- `tools/workflow_guard.py sync-compat`：从 `.agents/` 生成兼容镜像和兼容说明文件。

现有历史样例保留用于迁移提示，不作为 canonical 正式产物。

## 助手型使用入口

- 日常起步看 [README.md](../README.md)
- 直接开项目看 [docs/quick-start.md](quick-start.md)
- 明确人机边界看 [docs/assistant-workflow-sop.md](assistant-workflow-sop.md)
- 复制 starter files 看 [templates/README.md](../templates/README.md)
