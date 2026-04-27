# 正式合规报告模板

本文件定义合规审核正式报告的固定结构。

---

## 模板

```yaml
# === 合规审核报告 ===
# 由 compliance-finalization-and-handoff skill 生成

metadata:
  report_id: ""                # CR-creative-001, CR-script-001 等
  series_id: ""
  episode_id: ""
  review_type: "compliance"    # compliance
  generated_at: ""

  # 审核对象信息
  target_file: ""
  target_version: ""
  target_stage: ""             # creative | script | asset | video
  target_review_phase: ""      # pre_generation | post_generation
  target_status_before: ""

  # 报告版本
  report_version: "1.0"
  report_status: "draft"       # draft | in_review | approved | rejected

  # 审核轮次
  review_round: 1
  previous_report: ""

# === 合规结论 ===
conclusion:
  verdict: ""                  # pass | conditional_pass | fail
  risk_level: ""               # high | medium | low
  gate_decision: ""            # allowed | conditional | blocked
  next_stage_allowed: true/false
  reason: ""

# === 规则域检查结果 ===
domain_results:
  - domain: "CR-01"            # 版权/IP
    domain_name: "版权 / IP"
    result: ""                 # clear | warning | violation
    notes: ""
  - domain: "CR-02"            # 真实人物
    domain_name: "真实人物 / 明星 / 公众人物"
    result: ""
    notes: ""
  - domain: "CR-03"            # 肖像/声音
    domain_name: "肖像 / 声音"
    result: ""
    notes: ""
  - domain: "CR-04"            # 人格权/名誉
    domain_name: "人格权 / 名誉"
    result: ""
    notes: ""
  - domain: "CR-05"            # 敏感内容
    domain_name: "敏感内容"
    result: ""
    notes: ""
  - domain: "CR-06"            # 平台限制
    domain_name: "平台限制"
    result: ""
    notes: ""
  - domain: "CR-07"            # 输入来源
    domain_name: "输入来源"
    result: ""
    notes: ""

# === 风险汇总 ===
risk_summary:
  total_risks: 0
  high: 0
  medium: 0
  low: 0

# === 风险列表 ===
risks:
  - risk_id: "RSK-001"
    rule_domain: ""
    risk_type: ""
    risk_level: ""             # high | medium | low
    description: ""
    evidence: ""
    remediation: ""
    responsible_agent: ""
    requires_retrial: true/false

  # ... 所有风险逐条列出

# === 审核说明 ===
review_notes:
  summary: ""
  key_findings: []
  areas_of_attention: []

# === 条件（仅 conditional_pass） ===
conditions:
  remediation_required: true/false
  remediation_scope: ""        # 局部修改 | 大幅返工
  remediation_deadline: ""
  remediation_items: []        # 必须整改的风险 ID
  requires_retrial: true/false
  additional_protections: []   # 需要增加的保护措施

# === 退回信息（仅 fail） ===
rejection:
  fallback_stage: ""
  responsible_agent: ""
  fix_scope: ""
  requires_full_retrial: true/false
  estimated_impact: []

# === 审核记录 ===
review_log:
  - round: 1
    date: ""
    verdict: ""
    risks_found: 0
    risks_fixed: 0
    notes: ""

# === 版本信息 ===
changelog:
  - version: "1.0"
    date: ""
    changes:
      - "首次合规审核"
    reason: ""
```

---

## 使用规则

1. 每份合规报告必须有唯一的 report_id
2. report_id 格式：`CR-{stage}-{序号}`
3. target_file 和 target_version 必须精确指向被审核文件
4. domain_results 必须覆盖全部 7 个规则域
5. risks 列表必须与 risk_summary 统计一致
6. conditional_pass 必须填写 conditions 部分
7. fail 必须填写 rejection 部分
8. review_log 记录每轮审核历史
9. 创意阶段审核报告存放路径：`project_data/projects/{project_id}/series/reviews/compliance/`
10. 非创意阶段审核报告存放路径：`project_data/projects/{project_id}/episodes/epXX/reviews/compliance/`
