# AI 漫剧自动生产系统 — 系统总览

## 系统架构

本系统基于 Claude Code 的 Agent + Skill 架构，实现从创意到成片的完整漫剧生产流水线。

```
用户 → 主控 Agent → 调度专业 Agent → 各阶段生产 → 审核 → 推进/回退
```

---

## Agent 一览表

| # | Agent | 文件 | 职责 |
|---|-------|------|------|
| 1 | producer-agent | `.claude/agents/producer-agent.md` | 总控调度、阶段流转、审核门禁、回退控制 |
| 2 | creative-development-agent | `.claude/agents/creative-development-agent.md` | 创意访谈、方向收敛、创意设定输出 |
| 3 | script-development-agent | `.claude/agents/script-development-agent.md` | 梗概、分集、单集剧本、改稿 |
| 4 | production-planning-agent | `.claude/agents/production-planning-agent.md` | 15 秒分段、segment 任务单、衔接设计 |
| 5 | asset-production-agent | `.claude/agents/asset-production-agent.md` | 资产清单、复用判断、生图 prompt、图片归档 |
| 6 | video-production-agent | `.claude/agents/video-production-agent.md` | 视频 prompt、首尾帧策略、视频生成与归档 |
| 7 | business-review-agent | `.claude/agents/business-review-agent.md` | 阶段质量判断、放行或退回 |
| 8 | compliance-review-agent | `.claude/agents/compliance-review-agent.md` | 版权、人物权、敏感内容、平台限制等合规判断 |

---

## Skill 一览表

每个 Agent 包含 2 个 Skills（一个负责"执行"，一个负责"定稿交接"）：

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

---

## 阶段流转图

```
[创意定义] ──→ [剧本开发] ──→ [生产规划] ──→ [资产生产] ──→ [视频生产]
    ↑              ↑              ↑              ↑              ↑
    └── 业务+合规   └── 业务+合规   └── 业务+合规   └── 业务+合规   └── 业务+合规
        审核           审核           审核           审核           审核
```

前三阶段（创意→剧本→规划）严格串行。
后两阶段（资产→视频）允许有限并行，前提是上游已 approved。

---

## 审核门禁矩阵

| 审核节点 | 业务审核 | 合规审核 |
|---------|---------|---------|
| 创意设定完成后 | 必须 | 必须 |
| 剧本完成后 | 必须 | 必须 |
| segment 总表完成后 | 必须 | — |
| 资产生成前 | — | 必须 |
| 资产生成后 | 必须 | 必须 |
| 视频生成前 | — | 必须 |
| 视频生成后 | 必须 | 必须 |

合规审核具有一票否决权：合规 fail 时，即使业务 pass，也不得推进。

---

## 文件目录约定

```
漫剧生产系统/
├── CLAUDE.md                          # 项目总规则
├── .claude/
│   ├── agents/                        # 8 个 Agent 定义
│   ├── skills/                        # 16 个 Skills（每个含 SKILL.md + supporting files）
│   └── settings.json                  # 项目配置
├── project_data/
│   ├── series/                        # 系列级设定、创意 Bible、访谈记录
│   └── episodes/epXX/                 # 单集数据
│       ├── script/                    # 剧本文件
│       ├── segments/                  # segment 总表和单段任务
│       ├── assets/images/             # 图片资产
│       ├── videos/                    # 视频文件
│       └── reviews/
│           ├── business/              # 业务审核报告
│           └── compliance/            # 合规审核报告
└── docs/                              # 说明文档
```

---

## 状态体系

所有正式产物统一使用 4 状态：

| 状态 | 含义 | 可否进入下一阶段 |
|------|------|---------------|
| `draft` | 初稿，编辑中 | 不可 |
| `in_review` | 已提交审核 | 不可 |
| `approved` | 审核通过 | 可以 |
| `rejected` | 审核退回 | 不可，需回退修改 |

版本号格式：`主版本.次版本`（如 1.0、1.1、2.0）

---

## 审核结论

| 审核类型 | 结论 | 含义 |
|---------|------|------|
| 业务审核 | pass | 质量达标，可推进 |
| 业务审核 | pass_with_revisions | 质量基本达标，需修改后放行 |
| 业务审核 | fail | 质量不达标，需退回 |
| 合规审核 | pass | 合规无风险 |
| 合规审核 | conditional_pass | 存在中低风险，附条件放行 |
| 合规审核 | fail | 存在高风险，必须退回 |
