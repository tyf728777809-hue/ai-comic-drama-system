# 整改建议报告模板

本文件定义合规审核整改建议的固定结构。面向责任 Agent，提供可执行的整改指南。

---

## 模板

```yaml
# === 整改建议报告 ===
# 由 compliance-finalization-and-handoff skill 生成

metadata:
  advice_id: ""                # RA-compliance-creative-001 等
  series_id: ""
  episode_id: "ep01"
  based_on_report: ""          # 对应的合规报告 report_id
  target_file: ""
  target_version: ""
  target_stage: ""
  generated_at: ""

# === 整改概览 ===
remediation_overview:
  total_items: 0
  high_items: 0
  medium_items: 0
  low_items: 0
  remediation_scope: ""        # 局部修改 | 大幅返工
  estimated_effort: ""

# === 整改项列表 ===
remediation_items:
  - risk_id: "RSK-001"
    risk_level: ""             # high | medium | low
    rule_domain: ""            # CR-01 到 CR-07
    priority: ""               # P0 | P1 | P2

    # 风险描述
    problem: ""
    evidence: ""
    current_state: ""

    # 整改建议
    remediation: ""            # 具体整改方向
    remediation_approach: ""   # 替换 | 删除 | 修改 | 增加标注 | 更换素材
    remediation_scope_description: ""
    constraints: []            # 整改时需遵守的约束

    # 责任归属
    responsible_agent: ""
    related_agents: []
    affected_segments: []

    # 重审要求
    requires_retrial: true/false
    retrial_scope: ""          # 全量重审 | 仅整改项 | 整改项+关联域

  # ... 所有整改项逐条列出

# === 整改优先级 ===
priority_order:
  - description: "高风险项必须优先整改"
    items: []
    rationale: "不整改无法放行"
  - description: "中风险项建议同步整改"
    items: []
    rationale: "可随高风险项一起整改，减少重审轮次"

# === 整改约束 ===
remediation_constraints:
  do_not_change: []            # 不要修改的部分
  keep_consistent: []          # 整改后需保持一致的部分
  reference_files: []          # 整改时需要参考的文件
  upstream_dependencies: []
  downstream_impact: []

# === 整改保护措施 ===
protections:
  - protection: ""             # 需要增加的保护措施
    reason: ""
    apply_to: []               # 适用范围

# === 整改后要求 ===
post_remediation:
  requires_retrial: true/false
  retrial_type: ""             # full | partial | targeted
  retrial_domains: []
  submission_requirements:
    - "更新版本号"
    - "更新 status 为 in_review"
    - "提交整改说明"
  expected_next_verdict: ""
```

---

## 使用规则

1. 整改建议只在结论为 conditional_pass 或 fail 时生成
2. pass 时标记为"无需整改"
3. 每个整改项必须引用对应的 risk_id
4. remediation_approach 必须具体可执行
5. priority_order 按 high → medium → low 排序
6. remediation_constraints 必须明确整改边界
7. protections 列出需要增加的保护措施（如免责声明等）
8. post_remediation 必须明确重审范围和提交要求
9. 报告存放路径：`project_data/projects/{project_id}/episodes/epXX/reviews/compliance/`
