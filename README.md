# AI 漫剧生产助手

这不是无人值守自动生产线，而是一套给你和 Codex 协作使用的漫剧生产助手系统。

它覆盖 5 个生产阶段、两条审核线、正式文件命名、schema 校验、状态扫描和兼容镜像。你负责拍板，助手负责按规则产出、整理、复核和提醒门禁。

## 入口

- 总规则：[AGENTS.md](AGENTS.md)
- 架构总览：[docs/system-overview.md](docs/system-overview.md)
- 快速开跑：[docs/quick-start.md](docs/quick-start.md)
- 人机协作 SOP：[docs/assistant-workflow-sop.md](docs/assistant-workflow-sop.md)
- Starter files：[templates/README.md](templates/README.md)

## 日常命令

```bash
python3 tools/workflow_guard.py validate
python3 tools/workflow_guard.py status --project PROJECT_ID --episode ep01
python3 tools/workflow_guard.py sync-compat
python3 -m unittest tests.test_workflow_guard
```

## 推荐使用方式

1. 从 `templates/` 复制当前阶段的 starter YAML 到 `project_data/`
2. 让助手按对应 Agent / Skill 补内容
3. 正式文件写完后跑 `validate`
4. 审核文件补齐后跑 `status`
5. 只在放行 verdict 明确时进入下一阶段

## 适合与不适合

- 适合：助手式生产、阶段门禁、审核留痕、项目复盘
- 不适合：无人值守自动推进、自动跳阶段、自动外部生成
