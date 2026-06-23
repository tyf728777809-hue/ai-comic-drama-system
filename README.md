# V2 AI 影像生产助手

这是一套给你和 Codex 协作使用的 AI 影像生产系统。它不是自动生成成片的流水线，而是一个轻量、高标准的 AI 电影工作室：帮助你把创意、剧本、镜头、视觉资产和 Seedance 2.0 手工生成包整理到可执行状态。

## 当前主流程

1. `story-agent`：作品灵魂、剧本、剧本医生、对白去 AI 味。
2. `director-agent`：按戏剧动作拆镜头，设计表演、镜头和声音意图。
3. `visual-asset-agent`：锁定视觉风格、角色、服装、场景和资产。
4. `seedance-package-agent`：生成 Seedance 2.0 音画一体任务包。
5. `music-agent`：生成 Suno/Sono 音乐任务卡和候选记录。

## 入口

- 总规则：[AGENTS.md](AGENTS.md)
- 系统总览：[docs/system-overview.md](docs/system-overview.md)
- 快速开始：[docs/quick-start.md](docs/quick-start.md)
- 协作 SOP：[docs/assistant-workflow-sop.md](docs/assistant-workflow-sop.md)
- 模板说明：[templates/README.md](templates/README.md)

## 日常命令

```bash
python3 tools/workflow_guard.py validate
python3 tools/workflow_guard.py status --project PROJECT_ID --episode ep01
python3 tools/workflow_guard.py sync-compat
python3 -m unittest tests.test_workflow_guard
```

## 关键边界

- Seedance 2.0 负责视频和声音一体生成。
- 系统不接入 Seedance API，只交付手工生成包。
- 不做独立配音，不做 lipsync，不做剪辑评审。
- Suno/Sono 只做音乐候选，不做对白。
