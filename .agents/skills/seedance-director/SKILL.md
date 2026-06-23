---
name: seedance-director
description: Seedance 2.0 视频提示词导演方法包。负责将已通过视频生产门禁检查的 segment 场景信息、正式图片资产和输入策略，转化为可嵌入正式 YAML 的中英双语 Seedance 视频 prompt。适用于视频生产阶段的最终提示词写作，不负责阶段门禁、资产归档、审核放行或执行生成。
---

# Skill：seedance-director

## 适用场景

当 `video-generation-and-control` 已经确认某个 segment 可以启动视频生产，并需要写 Seedance 2.0 专用视频 prompt 时使用本 skill。

本 skill 只负责“把已确认的信息写成 Seedance 可用的导演提示词”。它不判断 `can_start_video`，不选择是否回退上游，不修改 segment 或资产文件，不调用视频生成工具。

---

## 输入契约

上游必须提供以下结构化信息：

- `segment_id`
- `duration`，默认 10 秒，最高不超过 15 秒
- `scene`：地点、环境、光线、氛围
- `characters`：角色名或角色功能标签、外观锚点、画面位置、朝向
- `action`：可见动作，15 秒内不超过 2 个主要动作
- `camera_movement`：固定、推、拉、摇、移、环绕等镜头指令
- `emotion_arc`：情绪或权力关系的起止变化
- `continuity_hint`：衔接自哪个 segment、衔接至哪个 segment、首尾帧要求
- `input_strategy`：`reference_only`、`first_frame_only`、`last_frame_only`、`first_and_last`
- `inputs`：正式项目资产路径，必须来自 `project_data/projects/{project_id}/episodes/epXX/assets/images/`
- `restrictions`：需要避免的画面错误

缺少核心剧情、角色、场景或动作信息时，不得脑补成正式设定；返回待确认项给 `video-generation-and-control`。

---

## 输出契约

本 skill 的直接输出是一个 JSON 数组，包含英文和中文两条 prompt：

```json
[
  {"lang": "en", "prompt": "..."},
  {"lang": "zh", "prompt": "..."}
]
```

`video-generation-and-control` 必须把结果嵌入 `video-prompts-vX.yaml`：

```yaml
target_model: "Seedance 2.0"
prompt_writer: "seedance-director"
seedance_prompt:
  en: ""
  zh: ""
  source_contract: "seedance-director-json-v1"
```

正式 YAML 文件不保存独立 JSON 数组，只保存拆出的 `en` 和 `zh` 字段。

---

## Prompt 结构

每条 Seedance prompt 使用连续文本，不使用 Shot 1 / Beat 2 等内部编号。

必须包含以下段落标签：

1. `Style & Mood:` 色彩、光线、镜头质感、氛围
2. `Dynamic Description:` 镜头、运动、动作，以现在时描述
3. `Static Description:` 场景、道具、环境细节
4. `Audio:` 仅在对话场景或用户明确要求声音时使用

`Narrative Summary:` 可选；中文长度接近上限时优先删掉。

中文 prompt 必须是中文导演语气的重写，不是逐字翻译。中文长度上限为 1800 字。

---

## Seedance 写作规则

1. 只写画面中能看见或能听见的内容。
2. 不发明上游没有确认的核心角色、地点、道具和剧情信息；可以补充灰尘、光线、雾气等环境运动。
3. 角色描述优先使用角色名、身份、服装、发型、标志物和动作，不使用年龄标签。
4. 单段跨镜头追踪角色不超过 3 个。
5. 角色离开画面后，不在同一个连续镜头内重新入画。
6. 不依赖镜面、水面、刀面等反射镜头表达关键信息。
7. 需要表达微表情时，用物理动作写：下颌收紧、指节发白、视线停顿，而不是抽象情绪词。
8. 用户或上游指定的镜头运动必须同时出现在英文和中文 prompt 中。

---

## 首尾帧约束

- `first_frame_only`：开头必须贴合首帧内容，结尾可自然延展，但不能突然换场。
- `first_and_last`：动态描述必须明确从首帧状态过渡到尾帧状态；不得添加会破坏首尾帧连续性的无关硬切。
- `last_frame_only`：必须围绕尾帧的结束状态组织动作，但该策略默认不推荐单独使用。
- `reference_only`：只能作为风格或构图辅助，不得与首帧、尾帧资产冲突。

如果首尾帧差异过大，必须返回风险说明，而不是强行写成可执行 prompt。

---

## 禁止事项

本 skill 不允许：

- 调用 Dream Maker、Seedance 或任何执行型视频生成工具
- 修改 `segments`、`asset-index`、`asset-archive` 等上游文件
- 引用 `.codex/generated_images/` 临时路径
- 替代业务审核或合规审核做放行决定
- 为省事把上游资产问题伪装成 prompt 优化问题

---

## 完成标准

完成后必须能交还：

1. 英文 Seedance prompt
2. 中文 Seedance prompt
3. 使用的输入策略
4. 是否存在首尾帧或连续性风险
5. 需要写入 `pending_items` 的待确认项
