# V2 系统总览

V2 的目标是用更少的 Agent 和更深的 Skill，支撑更高标准的 AI 影像生产。

## 架构

- `studio-producer`：总控，不创作。
- `story-agent`：作品灵魂、剧本和剧本医生。
- `director-agent`：镜头、表演、声音意图。
- `visual-asset-agent`：视觉风格和资产。
- `seedance-package-agent`：Seedance 2.0 手工生成包。
- `music-agent`：Suno/Sono 音乐任务。

## 质量系统

V2 不靠增加审核角色提升质量，而靠两个硬 Pass：

- `story-kill-pass`：杀掉平庸创意和弱剧本。
- `audience-jury-pass`：从观众角度发现无聊、混乱、AI 味和情绪失效。

## Seedance 生产

`seedance-director` 保持不改。V2 只增强它的上游输入：

- 完整镜头设计
- 正式图片资产路径
- 最多 9 张上传图清单
- Audio 段
- 禁止项和失败重试建议

最终交付是 `manual-generation-package.yaml`，供用户手工复制 prompt 和上传图片。
