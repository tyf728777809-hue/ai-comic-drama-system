---
name: market-oriented-script-development
description: 市场化剧本开发方法包。负责从已批准创意设定生成故事梗概、分集规划、单集剧本，并进行编剧结构检查和平台适配检查。适用于剧本开发阶段的内容生产与改稿。
---

# Skill：market-oriented-script-development

## 适用场景

当 script-development-agent 需要执行以下工作时使用本 skill：
- 基于已 approved 创意设定生成故事梗概
- 生成分集规划
- 写单集正式剧本
- 根据用户反馈定向改稿
- 对剧本做编剧结构检查
- 对剧本做平台适配检查

**不适用**：剧本定稿整理、确认复盘、生产规划交接 → 使用 `script-finalization-and-handoff`

---

## 核心目标

1. 从已批准创意设定稳定生成完整剧本内容
2. 保证剧本结构与戏剧推进成立
3. 保证剧本适合漫剧平台消费逻辑
4. 保证剧本适合后续 15 秒拆段和 AI 生产
5. 支持定向改稿而非整篇重写

---

## 输入

| 输入 | 路径 | 用途 |
|------|------|------|
| 创意设定文件 | `project_data/projects/{project_id}/series/creative-bible-vX.yaml` | 剧本展开的基准输入 |
| 创意阶段交接摘要 | `project_data/projects/{project_id}/series/script-handoff-vX.yaml` | 了解交接要求 |
| 历史剧本版本 | `project_data/projects/{project_id}/episodes/epXX/script/script-vX.yaml` | 改稿时参考 |
| 用户本轮反馈 | 聊天上下文 | 改稿方向 |

---

## 输出

根据当前进度输出以下内容之一或多个：

| 产物 | 输出路径 | 触发条件 |
|------|---------|---------|
| 故事梗概 | `project_data/projects/{project_id}/series/synopsis-vX.yaml` | 首次进入剧本阶段 |
| 分集规划 | `project_data/projects/{project_id}/series/episode-plan-vX.yaml` | 梗概完成后 |
| 单集剧本 | `project_data/projects/{project_id}/episodes/epXX/script/script-vX.yaml` | 分集规划完成后 |
| 结构风险提示 | 剧本文件内 risks 字段 | 每次剧本输出时 |
| 平台适配提示 | 剧本文件内 platform_risks 字段 | 每次剧本输出时 |

---

## 执行步骤

### 第 1 步：读取创意设定与交接摘要

读取 `project_data/projects/{project_id}/series/creative-bible-vX.yaml`（status 必须为 approved）。
如果存在交接摘要，一并读取。

确认以下信息：
- `project_positioning.title`、`project_positioning.genre`、`project_positioning.style`、`project_positioning.target_audience`
- `core_hook.logline`
- `story_core.premise`、`story_core.core_conflict`
- `protagonist`、`supporting_characters`
- `worldbuilding.setting`、`worldbuilding.visual_style`、`worldbuilding.color_palette`
- `production_params.episode_count`、`production_params.episode_duration`、`production_params.segment_duration`

### 第 2 步：检查输入是否足够写剧本

检查清单：
- [ ] 创意设定 status = approved
- [ ] 至少有 1 个主角
- [ ] 核心冲突已定义
- [ ] 世界观设定已定义
- [ ] 目标集数和单集时长已定义

如果有阻断型缺失 → 停止，输出缺口清单，要求主控退回创意阶段补全。
如果有非阻断缺失 → 标记为"待确认项"，继续推进。

### 第 3 步：生成故事梗概

基于创意设定，输出故事梗概，包含：
- one_liner：一句话故事（不超过 30 字）
- core_conflict：核心矛盾
- story_arc：主线推进逻辑（起 → 承 → 转 → 合）
- selling_points：核心卖点（3-5 个）
- platform_hooks：平台化看点摘要（对漫剧平台有吸引力的点）

将梗概写入 `project_data/projects/{project_id}/series/synopsis-v1.0.yaml`，status = draft。
使用 `synopsis-template.md` 模板。

### 第 4 步：生成分集规划

基于故事梗概，输出分集规划。使用 `episode-planning-template.md` 模板。

每集必须包含：
- episode_id：集号
- title：暂定标题
- goal：本集目标（一句话）
- core_conflict：本集核心冲突
- key_advances：主要推进点（2-3 个）
- ending_hook：结尾钩子
- emotion_peak：情绪峰值描述
- key_characters：本集关键角色

将分集规划写入 `project_data/projects/{project_id}/series/episode-plan-v1.0.yaml`，status = draft。

### 第 5 步：生成单集剧本

按分集规划逐集生成单集剧本。每次只生成 1 集。

每集剧本结构：
- 集数与标题
- 本集目标
- 剧情推进（分场景）
- 场景顺序（每个场景标注序号、地点、时间、角色）
- 角色动作（可视觉化描述）
- 对白（如有）
- 情绪转折点标注
- 钩子 / 反转 / 结尾扣子
- 风险提示
- 待确认项
- 版本号
- 确认状态

参照 `script-structure-guide.md` 的结构化写法。

将单集剧本写入 `project_data/projects/{project_id}/episodes/epXX/script/script-v1.0.yaml`，status = draft。

### 第 6 步：编剧结构检查

对当前剧本执行结构检查（参照 `script-structure-guide.md`）：

| 检查项 | 通过标准 |
|-------|---------|
| premise | 有明确的核心前提 |
| 外在目标与核心冲突 | 主角有清晰目标，冲突明确 |
| 主角推进线 | 每集主角有主动行为 |
| 激励事件 | 第一集前段有足够强的激励事件 |
| 中点变化或反转 | 整体故事有中点转折 |
| 结尾扣子 | 每集有结尾钩子 |
| 场景价值变化 | 每个场景有明确的情绪/信息推进 |
| 人物关系张力 | 角色之间有冲突或张力 |
| 无效段落 | 无明显松散、空转、重复段落 |

将检查结果写入剧本文件的 `structure_check` 字段。

### 第 7 步：平台适配检查

对当前剧本执行平台适配检查（参照 `platform-fit-checklist.md`）：

| 检查项 | 通过标准 |
|-------|---------|
| 开头节奏 | 第一场景前 3 秒内进入矛盾 |
| 留人点 | 每集前段有留人钩子 |
| 情绪峰值 | 每集至少 1 个明显情绪峰值 |
| 反转/爽点 | 每集至少 1 个反转或爽点 |
| 追更驱动 | 每集结尾有牵引到下一集的钩子 |
| 短段适配 | 每个场景可拆为 2-4 个 15 秒段 |
| 视觉化 | 无过多难视觉化的内心独白 |
| AI 生成友好 | 无过多难 AI 生成的大场面/群像/复杂动作 |
| 角色记忆点 | 每个主要角色有视觉记忆特征 |

将检查结果写入剧本文件的 `platform_check` 字段。

### 第 8 步：根据用户反馈定向改稿

当用户提出修改意见时：
1. 读取用户反馈
2. 定位需要修改的具体场景或要素
3. 判断修改是否与已锁定创意设定冲突
   - 冲突 → 标注风险，要求用户确认
   - 不冲突 → 执行修改
4. 只修改受影响的部分，不做整篇重写
5. 递增版本号（参照 `script-finalization-and-handoff/version-status-rules.md`）
6. 重新执行结构检查和平台适配检查

### 第 9 步：输出当前版本结果

每次完成修改后输出：
- 当前版本号
- 本次修改了什么
- 当前结构检查结果
- 当前平台适配检查结果
- 当前待确认项
- 建议下一步（继续改稿 / 进入定稿整理）

---

## 约束边界

本 skill **不允许**：
- 擅自修改已 approved 的创意设定
- 直接做 15 秒拆段
- 直接写分镜级方案
- 直接写资产 prompt 或视频 prompt
- 调用 Dream Maker 或任何执行型生成工具
- 越权进入生产规划阶段

本 skill **允许**：
- 读取所有项目文件
- 写入剧本相关文件（梗概、分集规划、单集剧本）
- 在剧本文件内标注风险和待确认项

---

## 完成标准

执行本 skill 后，必须能明确回答：

1. **当前版本**：剧本当前版本号和状态
2. **创意一致性**：是否与已批准创意设定一致，有无冲突
3. **结构风险**：当前是否还有明显结构问题
4. **平台适配风险**：当前是否还有明显平台适配问题
5. **下一步**：是继续改稿还是进入定稿整理（`script-finalization-and-handoff`）
