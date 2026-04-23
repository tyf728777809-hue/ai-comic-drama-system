# 确认前复盘摘要模板

本文件定义面向用户的复盘摘要模板。语言面向用户，不用内部术语。

---

## 模板

```yaml
# === 创意确认前复盘摘要 ===
# 由 creative-bible-and-handoff skill 生成

metadata:
  project_name: ""
  version: ""
  generated_at: ""
  status: "in_review"

# === 项目概述 ===
overview:
  one_sentence: ""            # 一句话说清楚这个项目
  genre_and_style: ""         # 题材 + 风格
  target_platform: ""         # 目标平台
  episode_plan: ""            # 集数和时长

# === 已确认内容 ===
confirmed:
  - category: "故事核心"
    items:
      - "premise: ..."
      - "核心冲突: ..."
      - "核心卖点: ..."

  - category: "角色"
    items:
      - "主角: ..."
      - "配角: ..."
      - "核心关系: ..."

  - category: "风格"
    items:
      - "视觉风格: ..."
      - "情绪基调: ..."

  - category: "生产参数"
    items:
      - "单集时长: ..."
      - "总集数: ..."

# === 待确认内容 ===
pending:
  - item: ""
    why_important: ""         # 用用户能理解的语言说明为什么重要
    options: []               # 如果有 2-3 个选项，列出来
    impact_if_unresolved: ""  # 不确认会怎样

# === 风险提示 ===
risks:
  high: []
  medium: []
  low: []
  risk_summary: ""            # 风险总体评估（一句话）

# === 下一步 ===
next_steps:
  if_confirmed:
    - "创意设定将进入业务审核"
    - "审核通过后进入剧本开发阶段"
    - "剧本开发 Agent 将基于此创意设定开始工作"

  if_not_confirmed:
    - "标注需要修改的部分"
    - "回到创意收敛阶段继续讨论"
    - "修改后重新生成复盘摘要"

  if_partial:
    - "已确认部分先锁定"
    - "待确认部分标注为待定"
    - "可进入下一阶段但需在剧本阶段前补齐"
```

---

## 使用规则

1. 每次提交用户确认前必须生成复盘摘要
2. confirmed 部分只列用户已明确确认的内容
3. pending 部分必须说明为什么重要、不确认会有什么影响
4. risks 按高/中/低分级，高风险必须用通俗语言解释
5. next_steps 必须清楚说明确认/不确认/部分确认各自的后果
6. 语言必须面向用户，避免内部 Agent 术语
7. 文件存放路径：`project_data/series/`
8. 文件命名：`review-summary-v{version}.yaml`
