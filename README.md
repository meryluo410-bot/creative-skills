# Creative Skills

四个用于生成虚构社交帖子、聊天截图和交易详情截图的 Codex Skills。

| Skill | 用途 |
| --- | --- |
| artifact-template-story-post-generator | 按保留的参考模板生成全英文故事帖子 |
| artifact-template-transaction-screenshot-generator | 生成全英文虚构 iLands 交易详情截图 |
| chat-ui-image-generator | 先确认聊天文案，再生成全英文聊天截图 |
| post-generator | 根据故事直接生成全英文社交帖子截图 |

## 使用

将需要的 Skill 文件夹完整复制到 `~/.codex/skills/`，保留其中的图片、参考文档和脚本。在支持图像生成的 Codex 环境中按 Skill 名称调用。

每个目录中的 `SKILL.md` 包含具体工作流程；图像生成流程依赖环境中的 `imagegen` 能力。
