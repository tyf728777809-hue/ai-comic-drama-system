---
name: asset-planning-and-prompting
description: 资产规划与 prompt 生成方法包。负责从已批准生产规划推导资产需求、判断复用策略、生成生图 prompt、检查资产风险。适用于资产生产阶段的内容规划与 prompt 设计。
---

# Skill：asset-planning-and-prompting

## 适用场景

当 asset-production-agent 需要执行以下工作时使用本 skill：
- 从 segment 总表推导图片资产需求
- 区分角色图、场景图、道具图、首帧、尾帧
- 规划角色三视图、表情表、姿态表、场景母版和 UI 规范
- 判断资产复用策略
- 生成生图 prompt
- 检查资产风险

**不适用**：资产结果归档、确认复盘、视频生产交接 → 使用 `asset-finalization-and-handoff`

---

## 核心目标

1. 从已批准生产规划稳定推导出完整资产需求
2. 正确区分资产类型和用途
3. 最大化资产复用，降低生产成本
4. 输出适合后续视频生产的生图 prompt
5. 先锁定视频一致性资产包，降低人物、场景和 UI 在视频阶段漂移的风险
6. 提前识别会影响视频阶段的资产风险

---

## 输入

| 输入 | 路径 | 用途 |
|------|------|------|
| Segment 总表 | `project_data/projects/{project_id}/episodes/epXX/segments/segments-vX.yaml` | 资产需求来源 |
| 单段任务文件 | `project_data/projects/{project_id}/episodes/epXX/segments/tasks/` | 每个 segment 的视觉规格 |
| 生产规划交接摘要 | `project_data/projects/{project_id}/episodes/epXX/segments/handoff-script-to-planning-vX.yaml` | 剧本阶段交接信息 |
| 已锁定设定 | 创意设定文件中的 `project_positioning`、`protagonist`、`supporting_characters`、`worldbuilding` | 角色外观和场景风格基准 |
| 历史资产版本 | `project_data/projects/{project_id}/episodes/epXX/assets/` | 复用判断参考 |
| 共享资产库 | `project_data/projects/{project_id}/series/shared-assets/` | 跨集复用资源 |

---

## 输出

| 产物 | 输出路径 | 触发条件 |
|------|---------|---------|
| 资产清单 | `project_data/projects/{project_id}/episodes/epXX/assets/asset-manifest-vX.yaml` | 首次资产规划时 |
| 生图 prompt 文件 | `project_data/projects/{project_id}/episodes/epXX/assets/asset-prompts-vX.yaml` | 资产清单完成后 |
| 资产风险提示 | 清单和 prompt 文件内 risks 字段 | 每次输出时 |

---

## 执行步骤

### 第 1 步：读取生产规划与交接摘要

读取 segment 总表（status 必须为 approved）。
读取单段任务文件，确认每个 segment 的视觉规格。

确认以下信息：
- 总 segment 数量和编号
- 每个 segment 的 key_visual、shot_type、camera_movement
- 每个 segment 的 transition_in 和 transition_out
- 交接摘要中的 locked_settings 和 visual_highlights

### 第 2 步：检查输入是否足够做资产规划

检查清单：
- [ ] Segment 总表 status = approved
- [ ] 每个 segment 有 key_visual 描述
- [ ] 每个 segment 有 shot_type 和 camera_movement
- [ ] 主角和主要配角已有 `appearance` 或 `visual_keywords`
- [ ] 场景风格已定义（`worldbuilding.visual_style` 和 `worldbuilding.color_palette`）
- [ ] 核心常驻角色规划了三视图、表情表、姿态表
- [ ] 核心场景规划了场景母版
- [ ] 关键 UI / 道具规划了统一规范

如果有阻断型缺失 → 停止，输出缺口清单，要求主控退回上游补全。
如果有非阻断缺失 → 标记为"待确认项"，继续推进。

### 第 3 步：先规划视频一致性资产包

精品漫剧进入逐 segment 生图前，必须先规划以下一致性资产：

1. **核心角色三视图**：正面、侧面、背面；用于锁定发型、服装、体型、标志物。
2. **核心角色表情表**：覆盖本集主要情绪，不得用“正常表情”等模糊描述。
3. **核心角色姿态表**：覆盖本集高频动作和关键动作。
4. **场景母版**：同一地点、同一氛围的基础空间图，用于后续首尾帧复用。
5. **UI / 道具规范**：对关键卡牌、系统红字、好友头像、手牌 UI 等建立可复用视觉规范。

角色处理规则：
- 多段常驻角色必须有三视图、表情表、姿态表。
- 只以记忆符号存在的角色不得被扩展成完整人物资产；应使用头像、语音波形、模糊回忆等符号。
- 如果本集只需要半身、剪影或投影形态，应按实际使用方式建立半身/投影/剪影一致性包，不强行生成复杂全身动作。

### 第 4 步：提取 segment 的资产需求

对每个 segment，提取以下资产需求（参照 `asset-planning-rules.md`）：

1. **角色图**：该 segment 中出现的角色，需要的姿态、表情、动作
2. **场景图**：该 segment 的地点、环境、氛围
3. **道具图**：该 segment 中出现的关键道具
4. **首帧**：该 segment 入场画面的完整构图
5. **尾帧**：该 segment 出场画面的完整构图

每个 segment 必须至少有独立首帧和尾帧资产；首尾帧 prompt 必须引用对应角色一致性包、场景母版和 UI / 道具规范。

将所有需求汇总为资产清单，写入 `asset-manifest-vX.yaml`。
使用 `asset-manifest-template.md` 模板。

### 第 5 步：做资产复用判断

对资产清单中的每一项，执行复用判断（参照 `asset-reuse-rules.md`）：

1. 同集内复用：检查是否有其他 segment 需要相同或相似的资产
2. 跨集复用：检查共享资产库中是否有可复用的资产
3. 场景复用：同一地点的不同角度/时间是否可以共享基础场景
4. 角色复用：同一角色的不同姿态是否可以通过 prompt 变体实现

对每个资产标注：
- `source: generate`（必须新建）
- `source: reuse`（可复用，标注 reuse_from）

### 第 6 步：生成生图 prompt

对需要新建的资产，使用 `image-prompt-template.md` 模板生成 prompt。

prompt 必须包含：
- 角色描述（外貌、服装、姿态、表情）
- 场景描述（地点、环境、光线、氛围）
- 动作描述（角色在做什么）
- 视角描述（镜头类型、构图）
- 风格描述（画风流派、色彩方案）
- 连续性提示（与其他资产的关联）
- 禁止项（需要避免的元素）

首尾帧 prompt 还必须包含：
- 引用的角色一致性资产
- 引用的场景母版
- 引用的 UI / 道具规范
- 与上一段尾帧或下一段首帧的衔接提示

将 prompt 写入 `asset-prompts-vX.yaml`。
使用 `asset-prompts-template.md` 汇总正式 prompt 文件。

### 第 7 步：做资产风险检查

对当前资产清单和 prompt 执行风险检查（参照 `asset-risk-checklist.md`）：

| 检查类别 | 检查内容 |
|---------|---------|
| 视频一致性资产包 | 核心角色三视图、表情表、姿态表、场景母版、UI 规范是否完整 |
| 角色一致性 | 同一角色在不同资产中是否保持外观一致 |
| 场景一致性 | 同一场景在不同 segment 中是否保持风格一致 |
| 首尾帧衔接 | 相邻 segment 的尾帧和下一 segment 的首帧是否能自然衔接 |
| Prompt 充分性 | prompt 是否足够明确，能否稳定产出预期结果 |
| 资产完整性 | 每个 segment 是否都有足够的资产支撑 |
| 资产重复 | 是否存在不必要的重复资产 |
| 生产成本 | 总资产数量是否在合理范围内 |

将检查结果写入资产清单的 `risks` 字段。

### 第 8 步：必要时给出替代资产策略

当某个 segment 的资产需求存在以下问题时，给出替代策略：
- 资产需求不明确（生产规划描述模糊）
- 生产成本过高（资产数量远超预期）
- 技术不可行（当前生图模型难以实现）

替代策略格式：
- 问题说明
- 2-3 种可选方案
- 每种方案的成本、风险、效果评估
- 推荐方案

### 第 9 步：输出当前版本结果

每次完成规划后输出：
- 当前版本号
- 资产总数和分类型统计
- 复用率统计
- 当前风险检查结果
- 当前待确认项
- 建议下一步（继续修正 / 进入定稿整理）

---

## 约束边界

本 skill **不允许**：
- 擅自修改已 approved 的生产规划
- 直接生成视频 prompt
- 直接进入视频生产
- 越权修改上游剧本或拆段
- 调用 Dream Maker 或任何执行型生成工具

本 skill **允许**：
- 读取所有项目文件
- 写入资产清单和生图 prompt 文件
- 在资产文件内标注风险和待确认项

---

## 完成标准

执行本 skill 后，必须能明确回答：

1. **当前版本**：资产规划当前版本号和状态
2. **资产完整性**：是否已形成覆盖所有 segment 的完整资产清单
3. **资产风险**：当前是否还有明显资产风险
4. **复用状态**：当前是否还有复用冲突
5. **下一步**：是继续修正还是进入定稿整理（`asset-finalization-and-handoff`）
