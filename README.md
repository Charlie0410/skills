# skills

这是一个个人 `skills` 仓库，主要用来存放我平时积累、整理和迭代的各种 skill。

这里的内容不一定都已经整理成统一的发布形态。有些目录是单个 skill，有些是同一主题下的一组 skill，也有一些是带示例、资源文件和独立说明的完整小项目。整体上，这个仓库更像一个长期维护的 skill 工作区和归档库。

## 仓库定位

- 沉淀日常工作里反复出现的流程和方法。
- 把临时做法整理成可复用的 `SKILL.md`。
- 作为 skill 的开发、试验、重构和归档空间。

## 当前内容

| 路径 | 内容 | 说明 |
| --- | --- | --- |
| `send-completion-reminder/` | 单个 skill | 在任务完成后调用本地提醒程序发送提醒邮件。 |
| `canonical_prompt_compiler_skills/` | skill 集合 | 围绕 Canonical Prompt Protocol 的一组阶段化 skill，包括 `normalize`、`compile`、`verify`、`repair`。 |
| `mpl-figure-skill/` | 独立 skill 项目 | 一个相对完整的技能项目，包含 `skills/`、`assets/`、`references/`、`examples/` 和独立 `README.md`。 |

## 目录约定

虽然这个仓库里的目录组织并不完全一致，但大致遵循下面这些约定：

- `SKILL.md`：skill 的核心入口，描述用途、触发条件、工作流和约束。
- `references/`：补充规则、背景资料或压缩后的参考说明。
- `assets/`：模板、样式文件、静态资源等。
- `agents/`：和 agent 运行相关的配置。
- `examples/`：示例输入、示例输出、脚本或测试材料。

## 使用方式

通常只需要：

1. 找到目标目录。
2. 打开对应的 `SKILL.md`。
3. 如果 skill 还依赖 `references/`、`assets/` 或 `examples/`，再按需继续读取。

如果某个目录本身就是一个独立的小型 skill 项目，比如 `mpl-figure-skill/`，则优先查看它自己的 `README.md` 和内部结构。

## 维护原则

- 先保证 skill 能表达清楚用途和边界，再考虑是否包装成统一格式。
- 优先保留真实工作流，而不是为了“整齐”过度抽象。
- 允许不同 skill 采用不同结构，只要入口清晰、依赖关系明确即可。
- 已经比较稳定的 skill，可以再补充示例、资源文件和独立说明。

## 后续

后面会继续把平时用得上的 skill 往这里收，逐步整理成更清晰、可复用、可迁移的形式。
