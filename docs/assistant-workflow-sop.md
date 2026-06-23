# V2 协作 SOP

## 默认工作方式

1. 先判断当前缺少哪个正式产物。
2. 调用对应 Agent 和 Skill。
3. 产出文件，而不是只在聊天里给结论。
4. 跑 `workflow_guard validate`。
5. 只有关键上游文件 `approved` 后才进入高成本生产。

## 阶段推进

- 作品与剧本：先过 `story-kill-pass`。
- 导演设计：每镜头必须有戏剧、视觉、声音三重目的。
- 视觉资产：角色、服装、场景先锁定，再做首尾帧。
- Seedance 试拍：先校准代表镜头，再批量整理手工任务包。
- 音乐：可并行，不阻塞 Seedance 准备。

## Seedance 手工包

`manual-generation-package.yaml` 必须让用户能直接操作：

- 看上传图顺序
- 复制中文或英文 prompt
- 确认 Audio 段
- 看到禁止项
- 看到失败后的重试建议

每个任务上传图不得超过 9 张。
