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
| `aca-slide-gen/` | 单个 skill | 从用户提供的学术文本、图、数据和公式生成一页 16:9 学术主内容 HTML slide。 |
| `aca-slide-pptx-gen/` | 单个 skill | 在 `aca-slide-gen` 的学术内容约束基础上，使用 OfficeCLI 生成一页 16:9 学术主内容 `.pptx`。 |
| `project-config/` | 单个 skill | 管理项目本地 TOML 配置，例如 trust、sandbox 和 approval 等项目级设置。 |
| `send-completion-reminder/` | 单个 skill | 在任务完成后调用本地提醒程序发送提醒邮件。 |
| `canonical_prompt_compiler_skills/` | skill 集合 | 围绕 Canonical Prompt Protocol 的一组阶段化 skill，包括 `normalize`、`compile`、`package`、`verify`、`repair`，其中 `package` 用于把 compiled prompt 要求提交的本地材料打包成附件。 |
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

## 每个技能的使用方法

| Skill | 路径 | 适用场景 | 使用方法 |
| --- | --- | --- | --- |
| `aca-slide-gen` | `aca-slide-gen/SKILL.md` | 需要从论文、报告、图表、数据或公式生成一页 16:9 学术主内容 HTML slide。 | 先收集 `section_title`、`topic` 和正文或等价结构化内容，再按 skill 的输入契约生成单页自包含 HTML。 |
| `aca-slide-pptx-gen` | `aca-slide-pptx-gen/SKILL.md` | 需要真实 `.pptx` 文件，而不是 HTML slide，且内容仍是学术主内容页。 | 先确认 OfficeCLI 可用，再按输入契约创建或修改一页 16:9 PowerPoint 内容 slide，并运行对应验证。 |
| `project-config` | `project-config/SKILL.md` | 需要读取、创建、预演或应用某个项目路径下的本地 TOML 配置。 | 明确目标项目路径，只操作项目本地 `.tooling/config.toml`，优先用脚本 API 或 CLI 做 dry-run 后再 apply。 |
| `send-completion-reminder` | `send-completion-reminder/SKILL.md` | 用户希望任务完成后自动发送一封提醒邮件。 | 正常完成主任务，最后且仅一次调用 `C:\Program Files\self\send_reminder.exe` 发送包含实际结果的简短提醒。 |
| `cpp-normalize-source-spec` | `canonical_prompt_compiler_skills/cpp-normalize-source-spec/SKILL.md` | 需要把自由任务描述或 CPP `SOURCE_SPEC` 规范化为 `[NORMALIZED_SPEC]`。 | 读取最小权威来源，区分 hard constraints 与 soft preferences，只输出 NORMALIZE 阶段制品。 |
| `cpp-compile-prompt` | `canonical_prompt_compiler_skills/cpp-compile-prompt/SKILL.md` | 需要把 `[NORMALIZED_SPEC]` 或等价源任务编译成可复用 CPP prompt。 | 读取编译器规则和模板，选择 lite 或 full profile，输出 `[COMPILATION_DIAGNOSTICS]` 与 `[COMPILED_PROMPT]`。 |
| `cpp-package-materials` | `canonical_prompt_compiler_skills/cpp-package-materials/SKILL.md` | 需要把 `.compiled-prompt.md` 要求提交的本地运行材料打包成附件。 | 用 materials-map JSON 或 `--material` 绑定逻辑材料 ID，运行 `package_materials.py` 生成 zip 与 sidecar manifest。 |
| `cpp-verify-prompt` | `canonical_prompt_compiler_skills/cpp-verify-prompt/SKILL.md` | 需要审查已编译 CPP draft prompt 是否忠实于源任务、协议和 profile。 | 读取 `SOURCE_SPEC`、`DRAFT_PROMPT`、CPP 规则与必要模板，只输出 `[VERIFY_REPORT]`。 |
| `cpp-repair-prompt` | `canonical_prompt_compiler_skills/cpp-repair-prompt/SKILL.md` | 已有 `VERIFY_REPORT`，需要对 compiled prompt 做有边界的修复。 | 以 `SOURCE_SPEC`、`DRAFT_PROMPT` 和 `VERIFY_REPORT` 为边界，输出 `[REPAIR_SUMMARY]` 与 `[REPAIRED_PROMPT]`。 |
| `mpl-figure-generator` | `mpl-figure-skill/skills/mpl-figure-generator/SKILL.md` | 需要用 Matplotlib 和仓库内 mplstyle 直接生成科学图、元数据，或调试标注图。 | 先读取 `mpl-figure-skill/README.md` 和 skill 文件，确认数据、图型、样式和 LaTeX 前置条件，再生成 production 或 debug 输出。 |

## 维护原则

- 先保证 skill 能表达清楚用途和边界，再考虑是否包装成统一格式。
- 优先保留真实工作流，而不是为了“整齐”过度抽象。
- 允许不同 skill 采用不同结构，只要入口清晰、依赖关系明确即可。
- 已经比较稳定的 skill，可以再补充示例、资源文件和独立说明。

## 后续

后面会继续把平时用得上的 skill 往这里收，逐步整理成更清晰、可复用、可迁移的形式。
