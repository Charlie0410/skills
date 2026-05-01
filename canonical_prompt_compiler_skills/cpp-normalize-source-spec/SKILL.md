---
name: cpp-normalize-source-spec
description: Normalize a free-form task description or CPP SOURCE_SPEC into a CPP NORMALIZED_SPEC for the Canonical Prompt Protocol. Use when Codex needs to turn ambiguous author-side requirements into explicit fields, placeholders, and normalized rules, or when the user asks to 规范化 SOURCE_SPEC/任务说明、区分 hard constraints 和 soft preferences、暴露缺失项与冲突、继承书稿术语/记号/章节约束，并且停在 NORMALIZE 阶段而不是继续编译最终 prompt.
---

# CPP Normalize Source Spec

## Overview

将作者侧的自由描述改写成 CPP 的 `[NORMALIZED_SPEC]`，让后续 `COMPILE` 可以处理一个更稳定、更可审计的中间表示。只做 `NORMALIZE`，除非用户明确要求，否则不要继续输出 `COMPILE`、`VERIFY` 或 `REPAIR` 制品。

## Workflow

1. 读取最小但足够的来源集合。
   - 读取用户请求、`SOURCE_SPEC`、明确引用的全局规则、以及为术语继承所必需的书稿片段。
   - 将 `SOURCE_SPEC` 视为源代码，恢复任务事实、边界条件、证据规则与交付物，而不是模仿其修辞表面。

2. 判断任务边界。
   - 先判断输入是在描述一个任务，还是把规划、起草、校验、格式化等多个阶段压在一起。
   - 如果只有一个主任务，就只规范化这个主任务。
   - 如果多个阶段彼此独立，保留拆分需求，不要把它们硬熔成一个 `NORMALIZED_SPEC`。

3. 按固定字段集重写。
   - 按以下顺序输出字段，不增删、不换序：
   - `TASK_NAME`
   - `TASK_FAMILY`
   - `DOMAIN`
   - `USER_INTENT`
   - `FINAL_DELIVERABLE`
   - `APPLY_GLOBAL_RULES_FROM`
   - `OUTPUT_LANGUAGE`
   - `AUDIENCE`
   - `SUCCESS_CRITERIA`
   - `AVAILABLE_INPUTS`
   - `REQUIRED_INPUTS`
   - `SOURCE_POLICY`
   - `HARD_CONSTRAINTS`
   - `SOFT_PREFERENCES`
   - `FAILURE_POLICY`
   - `FORMAT_REQUIREMENTS`
   - `OPTIONAL_EXAMPLES`
   - `OPEN_QUESTIONS`
   - 用 [canonical-schema.md](references/canonical-schema.md) 的字段语义与格式约定填充这些槽位。

4. 做歧义显式化，而不是润色。
   - 将 `brief`、`concise`、`short` 改写成长度控制槽位，而不是自作主张给一个漂亮短文。
   - 将 `proper format` 改写成明确的输出顺序、字段、模式或返回类。
   - 将 `use sources appropriately` 改写成来源优先级、可采纳证据、排除证据与允许转换。
   - 将 `keep consistent with the manuscript` 拆成术语继承、符号继承、单位继承、章节继承中的具体项。
   - 将 `do not hallucinate` 改写成证据边界、禁止动作与保守失败规则。
   - 按合同效果分类，不按语气分类。改变任务身份、证据边界、安全边界或可见返回类的要求属于硬约束。

5. 决定哪些值可以绑定，哪些必须显式留空。
   - 只允许闭世界推断：当前 `SOURCE_SPEC`、显式继承链、稳定库默认值。
   - 不要用开放域常识补任务定义。
   - 将高影响缺失项保留为 `{{PLACEHOLDER_NAME}}`。
   - 将低风险默认值直接写入字段值，并在 `OPEN_QUESTIONS` 中用 `ASSUMPTION:` 标记来源。
   - 将无法合法决断的碰撞放入 `OPEN_QUESTIONS`，用 `CONFLICT:` 或 `SPLIT:` 标记。

6. 严格区分语义占位符和运行时材料。
   - `{{PRIMARY_RELIABLE_SOURCE}}` 这类占位符表示规格本身还没定。
   - `<REFERENCE_MATERIALS>...</REFERENCE_MATERIALS>` 这类运行时块表示规格已定，只是实例值稍后装配。
   - 不要把运行时材料偷偷塞回规则字段，也不要把规则缺失伪装成“稍后绑定”。

7. 在源敏感任务中把保守失败提前写清楚。
   - `NORMALIZED_SPEC` 仍以 `compiler.md` 的字段集为准，不要提前编译出 `FAILSAFE` 或 `VERIFICATION` 章节。
   - 对源敏感任务，把后续需要的约束前移到 `SOURCE_POLICY`、`FAILURE_POLICY`、`SUCCESS_CRITERIA` 与 `OPEN_QUESTIONS` 中，确保后续编译必须显式生成保守失败和验证路径。
   - 用 [protocol-principles.md](references/protocol-principles.md) 处理证据分级、保守失败、冲突优先级与拆阶段问题。

## Output Contract

默认不要只把制品贴在对话框中。先将规范化制品写入文件，再在对话中返回写入路径和简短状态。

写入位置与命名：

- 若用户提供了主要输入文件路径，将输出写入该输入文件的同级文件夹。
- 若用户明确提供输出路径，使用用户指定路径。
- 若只有对话输入而没有文件路径，写入当前工作目录。
- 默认文件名为 `<source-stem>.normalized-spec.md`；没有来源文件名时使用 `normalized-spec.md`。
- 如果目标文件已存在，先确认它是同一阶段的旧制品再覆盖；若无法确认，使用带时间戳的唯一文件名。

文件内容只包含一个块：

```text
[NORMALIZED_SPEC]
TASK_NAME:
TASK_FAMILY:
DOMAIN:
USER_INTENT:
FINAL_DELIVERABLE:
APPLY_GLOBAL_RULES_FROM:
OUTPUT_LANGUAGE:
AUDIENCE:
SUCCESS_CRITERIA:
AVAILABLE_INPUTS:
REQUIRED_INPUTS:
SOURCE_POLICY:
HARD_CONSTRAINTS:
SOFT_PREFERENCES:
FAILURE_POLICY:
FORMAT_REQUIREMENTS:
OPTIONAL_EXAMPLES:
OPEN_QUESTIONS:
```

对话最终回复只列出输出文件路径、是否成功写入、以及关键未决项数量或 `none`。除非用户明确要求，不要在对话中粘贴完整 `[NORMALIZED_SPEC]`。

1. 对单值字段使用单行值；对多项字段使用平铺列表。
2. 对空但非必需字段写 `none`；对必需但未定字段写精确占位符。
3. 在 `OPEN_QUESTIONS` 中保留类型化残余状态，使用以下前缀：
   - `MISSING:`
   - `ASSUMPTION:`
   - `CONFLICT:`
   - `SPLIT:`
4. 保持 `SOURCE_SPEC` 中已有的术语、符号、单位、命名和引文风格一致。
5. 不要输出隐藏推理，不要附加解释性散文，不要顺手把结果升级成编译后的 prompt。

## Guardrails

- 保留作者意图，但把模糊之处改写成显式字段、范围、规则或占位符。
- 将 `SOURCE_SPEC`、`NORMALIZED_SPEC` 与诊断性残余状态分开处理，不要把它们写成一个混合段落。
- 将长寿命规则与任务局部规则分开；若已引用全局规则文件，优先保留引用而不是整段内联。
- 将硬约束、软偏好、假设、缺失项、冲突视为不同对象；不要用流畅措辞掩盖它们。
- 只在低风险时继承默认值。`TASK_FAMILY`、`FINAL_DELIVERABLE`、`REQUIRED_INPUTS`、来源优先级核心、可见返回类通常都不安全，不能猜。
- 只在明确合法的优先级之下解决冲突：硬约束高于软偏好，显式声明高于推断默认，证据与安全边界高于风格便利。
- 如果一个请求实质上是多阶段流程，优先保留拆分建议，而不是把多个不兼容目标压成一个假完整规格。

## References

- 读取 [canonical-schema.md](references/canonical-schema.md) 以查看字段语义、歧义改写模式、占位符命名和 `OPEN_QUESTIONS` 约定。
- 读取 [protocol-principles.md](references/protocol-principles.md) 以查看书稿中关于中间表示、证据分级、保守失败、闭世界推断与冲突优先级的抽象。
