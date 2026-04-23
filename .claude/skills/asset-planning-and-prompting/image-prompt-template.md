# 生图 Prompt 模板

本文件定义面向生图模型的正式 prompt 结构模板。

---

## 设计原则

1. Prompt 的首要目标是**服务后续视频生产**，不是单纯好看
2. 角色一致性是最高优先级
3. 场景清晰性是第二优先级
4. 每条 prompt 必须包含连续性提示，确保与其他资产关联
5. 禁止项必须明确，避免常见生成错误

---

## 通用 Prompt 结构

每条 prompt 由以下部分组成，按顺序拼接：

```
[质量前缀], [主体描述], [动作/姿态], [场景/背景], [视角/构图], [风格/色彩], [连续性提示], [禁止项]
```

---

## 按资产类型的 Prompt 模板

### 一、角色图 Prompt

```
[质量]: masterpiece, best quality, highly detailed
[主体]: 1girl/1boy, {角色外观描述}, {服装描述}, {标志物描述}
[姿态]: {姿态描述}, {表情描述}
[场景]: {场景简述}
[视角]: {shot_type}, {构图描述}
[风格]: {画风流派}, {色彩方案}, {光影描述}
[连续性]: reference sheet style, consistent character design
[禁止]: negative prompt: {禁止项}
```

**字段说明：**

| 字段 | 来源 | 填写规则 |
|------|------|---------|
| 角色外观 | creative-brief → visual_keywords | 必须包含：发色、发型、肤色、体型、年龄感 |
| 服装 | creative-brief + segment 任务 | 必须与已锁定设定一致 |
| 标志物 | creative-brief → visual_keywords | 配饰、纹身、疤痕等 |
| 姿态 | segment 任务 → key_visual | 必须具体，不使用"自然姿态"等模糊词 |
| 表情 | segment 任务 → emotion | 必须具体，不使用"正常表情" |
| 场景简述 | segment 任务 → location | 简要地点描述 |
| shot_type | segment 任务 → shot_type | 特写/中景/全景等 |
| 画风流派 | creative-brief → visual_style | 全局统一的画风关键词 |
| 色彩方案 | creative-brief → color_palette | 全局统一的色彩关键词 |
| 光影 | segment 任务 → 时间/氛围 | 根据时间和氛围确定 |

**示例：**
```
masterpiece, best quality, highly detailed,
1girl, long black hair, red eyes, pale skin, slender build, young adult,
wearing dark blue school uniform with red ribbon,
standing with right hand raised to chest, determined expression with slight frown,
school rooftop at sunset, wind blowing,
medium shot, waist up, centered composition,
anime style, warm color palette, golden hour lighting, soft shadows,
reference sheet style, consistent character design,
negative prompt: deformed, extra fingers, blurry, low quality, text, watermark
```

### 二、场景图 Prompt

```
[质量]: masterpiece, best quality, highly detailed
[主体]: no humans, {场景主体描述}
[环境]: {地点描述}, {天气/光线}, {氛围}
[细节]: {场景细节元素}
[视角]: {视角描述}, {景深描述}
[风格]: {画风流派}, {色彩方案}
[连续性]: background art, consistent environment design
[禁止]: negative prompt: {禁止项}
```

**示例：**
```
masterpiece, best quality, highly detailed,
no humans,
modern city rooftop, tall buildings in background,
sunset sky with orange and purple clouds, warm golden light, peaceful atmosphere,
fence on rooftop edge, water tank on the side, pigeon feathers on ground,
wide angle shot, deep depth of field, rule of thirds,
anime style, warm color palette, cinematic lighting,
background art, consistent environment design,
negative prompt: people, characters, text, watermark, low quality
```

### 三、道具图 Prompt

```
[质量]: masterpiece, best quality, highly detailed
[主体]: {道具描述}, {道具状态}
[环境]: {放置环境简述}
[视角]: {视角描述}
[风格]: {画风流派}, {色彩方案}
[连续性]: prop design, consistent style
[禁止]: negative prompt: {禁止项}
```

### 四、首帧 Prompt

```
[质量]: masterpiece, best quality, highly detailed
[主体]: {角色描述}, {姿态}, {表情}
[场景]: {完整场景描述}
[动作]: {角色在做什么}
[视角]: {shot_type}, {构图}, {焦点位置}
[风格]: {画风流派}, {色彩方案}, {光影}
[连续性]: {与上一 segment 尾帧的衔接提示}, starting frame
[禁止]: negative prompt: {禁止项}
```

**首帧特殊规则：**
- 必须包含与上一 segment 尾帧的衔接提示
- 如果是本集第一个 segment，衔接提示改为"episode opening frame"
- 构图必须精确匹配 segment 任务中的 transition_in 描述

### 二、尾帧 Prompt

```
[质量]: masterpiece, best quality, highly detailed
[主体]: {角色描述}, {姿态}, {表情}
[场景]: {完整场景描述}
[动作]: {角色在做什么}
[视角]: {shot_type}, {构图}, {焦点位置}
[风格]: {画风流派}, {色彩方案}, {光影}
[连续性]: {与下一 segment 首帧的衔接提示}, ending frame, {悬念/钩子的视觉表达}
[禁止]: negative prompt: {禁止项}
```

**尾帧特殊规则：**
- 必须包含与下一 segment 首帧的衔接提示
- 如果是本集最后一个 segment，衔接提示改为"episode ending frame, cliffhanger"
- 必须表达该 segment 的 ending_hook 的视觉含义

### 三、场景图 Prompt

```
[质量]: masterpiece, best quality, highly detailed background
[场景]: {完整场景描述}, {时间}, {天气/光线}, {氛围}
[细节]: {场景中的关键元素}
[风格]: {画风流派}, {色彩方案}
[连续性]: consistent background style, {与其他场景的关联}
[视角]: {视角描述}, no characters
[禁止]: negative prompt: {禁止项}, character, person
```

### 四、道具图 Prompt

```
[质量]: masterpiece, best quality, highly detailed object
[主体]: {道具完整描述}, {材质}, {状态}
[视角]: {视角描述}, clean background
[风格]: {画风流派}, {色彩方案}
[禁止]: negative prompt: {禁止项}, character, person, hand
```

---

## 禁止项通用列表

| 禁止项 | 适用场景 | 原因 |
|-------|---------|------|
| deformed, bad anatomy | 角色图 | 防止人体结构错误 |
| extra fingers, extra limbs | 角色图 | 防止多余肢体 |
| blurry, low quality | 所有 | 保证清晰度 |
| watermark, signature | 所有 | 防止水印 |
| text, watermark | 所有 | 防止文字干扰 |
| inconsistent style | 所有 | 防止风格不一致 |
| multiple views | 角色/场景 | 防止多视角混乱 |

---

## Prompt 质量检查

每条 prompt 生成后必须检查：

| 检查项 | 标准 | 级别 |
|-------|------|------|
| 角色描述是否完整 | 包含发色、发型、肤色、服装、标志物 | fail |
| 场景描述是否具体 | 不使用"某处"等模糊词 | fail |
| 姿态是否明确 | 不使用"自然姿态"等模糊词 | fail |
| 风格是否与全局一致 | 画风和色彩与 creative-brief 一致 | fail |
| 连续性提示是否存在 | 每条 prompt 必须有连续性提示 | fail |
| 禁止项是否完整 | 至少包含通用禁止项 | warning |
| prompt 长度是否合理 | 不超过模型 token 上限的 80% | warning |
