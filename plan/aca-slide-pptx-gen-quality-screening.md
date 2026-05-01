# aca-slide-pptx-gen 品质提升筛选结果

来源报告：`C:\Users\charlie\Downloads\deep-research-report.md`

目标技能：`aca-slide-pptx-gen`

目标：尽可能多地筛出能提升学术 `.pptx` 单页生成质量的内容，尤其保留可转写为
技能说明、参考规范、版式 preset、验证检查或后续实现任务的规则。

## 中文主筛选结果

本文件只筛选对 `aca-slide-pptx-gen` 有直接质量提升价值的内容。筛选重点不是
“学术 PPT 一般美化建议”，而是能转写进技能说明、布局规范、输入契约、验证脚本、
版式 preset 或人工验收清单的规则。

## 一句话结论

报告中最值得吸收到 `aca-slide-pptx-gen` 的方向是：把默认生成逻辑从“标题 +
若干文本/图表”升级为“结论句主张 + 单一主证据 + 可访问标注”的
assertion-evidence 学术幻灯片结构，并用可量化的字号、对比度、色觉友好、
图表标注和场景化预览规则兜底。

## 用户增加的有关pptx的排版规则

1. 文本框背景色要在文本对象上实现，而不是单独生成背景颜色
2. 文本list不要每一条一个文本框，如果是相关的、在同一个背景框下的信息要在同一个文本框中生成并且要加bulletin
3. 标题下方横线要贯穿左右。linewidth=2
4. caption 默认改为采用italic font with no background color.

## 最高优先级筛选项

用户修改意见:

1. 复杂的academic slide通常不能采用“主标题应尽量是完整结论句或问题陈述”这种方法，排除
2. 关于图表配色的建议超出了本技能边界
3. 排除深色背景的scenario
4. 不需要包含线上直播相关的内容

| 优先级 | 可筛入内容 | 对 `aca-slide-pptx-gen` 的价值 | 建议落点 |
|---|---|---|---|
| P0 | 每页只承载一个中心信息单元。 | 防止单页同时塞背景、方法、结果、结论。 | `SKILL.md` 工作流、输入压缩规则、验证清单 |
| P0 | 默认采用 assertion-evidence 结构。 | 让幻灯片以“可被证明的主张”组织，而不是主题词标题加项目符号。 | `SKILL.md`、布局规范、新 preset |
| P0 | 标题/主标题应尽量是完整结论句或问题陈述。 | 让听众先获得可理解的中心信息。 | 输入契约新增 `central_claim` 或 `main_claim` |
| P0 | 图、表、公式、流程图应承担主要解释任务。 | 减少正文堆叠，提高学术证据感。 | 版式选择、图表规则 |
| P0 | 正文默认不应低于 24pt，18pt 只作为硬下限。 | 现有规范的 15-20pt 正文、12-15pt caption 偏小。 | `layout-and-style-spec.md`、验证脚本 |
| P0 | 普通文本对比度至少 4.5:1，大号文本和关键图形至少 3:1。 | 当前只列颜色，没有可测的可访问性阈值。 | 色彩规范、验证脚本 |
| P0 | 不能只靠颜色表达含义。 | 避免色觉缺陷用户无法辨别分组或强调。 | 图表规则、验证清单 |
| P0 | 图内直接标注优先，远置图例次之。 | 减少跨区域匹配颜色/线型造成的认知负担。 | 图表规则、preset |
| P0 | 坐标轴、图例、图题、caption 必须保留完整变量名和单位。 | 避免学术含义缺失。 | 图表/table 规则、验证清单 |
| P1 | 灰度、投影、线上小窗三类预览应纳入验收。 | 当前验证偏文件结构和 OfficeCLI issues，缺少真实观看场景检查。 | `verification-checklist.md` |
| P1 | 使用高分辨率原图或矢量图，并裁切到支持论点的区域。 | 避免模糊截图和装饰性图片降低证据质量。 | 图像规则 |
| P1 | 每页应有唯一、可描述标题，阅读顺序应与视觉顺序一致。 | 强化 PowerPoint 可访问性。 | 输出契约、验证脚本 |
| P1 | 表格只保留关键列，密集数字应转成图表或高亮结论。 | 防止生成不可读的大表。 | table 规则、输入压缩 |
| P1 | 多系列图表采用色觉友好 palette。 | 当前仅有蓝/红强调色，不足以支持分类图表。 | `layout-presets.json` |
| P2 | 按口头报告、线上直播、深色会场等场景调整字号和留白。 | 单页生成也会受观看场景影响。 | 输入契约、preset |

## 与现有技能的差距

| 领域 | 现有 `aca-slide-pptx-gen` 已覆盖 | 从报告筛出的增强点 |
|---|---|---|
| 画布 | 已固定 16:9、`33.87cm x 19.05cm`、安全边界。 | 增加投影/小窗/灰度预览，不只验证几何边界。 |
| 标题 | 已要求左上 `section_title` 和分隔线。 | 增加独立 `main_claim`，避免 section title 过泛。 |
| 来源约束 | 已要求不编造事实、数据、公式和结论。 | 补充：只有来源支持时才可把主题改写成结论句。 |
| 字体 | 已区分中文 `Microsoft YaHei`、英文 `Calibri`。 | 字号区间需整体上调，caption 和图表标签尤其明显。 |
| 色彩 | 已有 caption 黄底黑字、蓝/红强调色。 | 增加 WCAG 对比度、色觉友好和非颜色编码。 |
| 图像 | 已要求图片 alt text 和 placeholder 标记。 | 增加原图/矢量优先、证据区域裁切、图片内文字转写。 |
| 图表 | 已要求只有 chart-ready data 才画图。 | 增加“分析任务决定图表类型”、直接标注、单位完整性。 |
| 表格 | 已允许 OfficeCLI table。 | 增加关键列筛选、密表转图或转 speaker notes。 |
| 公式 | 已保留 LaTeX，优先 equation。 | 增加公式作为主证据时的字号、留白和定义靠近规则。 |
| 验证 | 已有 OfficeCLI validate/issues/annotated/text/html/no-alt。 | 增加字号、对比度、文本密度、阅读顺序、灰度、小窗检查。 |

## 内容组织规则

这些规则适合直接写入 `SKILL.md` 或 `references/input-contract.md`：

- 把 `topic` 视为候选中心信息，而不是必然可直接上屏的标题。
- 若 `topic` 只是名词短语，优先从用户文本中提炼来源支持的结论句。
- 若来源不支持明确结论，不得强行生成结论句；改用中性问题句或描述性标题。
- 每张内容页只表达一个中心信息单元。
- 默认可见结构应为：主张、证据、简短限定条件或 takeaway。
- 不要让背景、方法、结果、结论在一页上获得同等视觉权重。
- 过长材料应按优先级删减：中心主张、最强证据、必要实验条件、关键限定。
- 能由演讲者口头补充的长解释，应进入 speaker notes，而不是压小字号放入画布。
- 如果必须把正文压到 18pt 以下才能放下，说明这一页信息过密，应询问拆页或摘要。
- 项目符号页应成为 fallback；默认应转为图、表、流程图、公式或标注式证据。
- 若不可避免使用项目符号，控制在 3-5 条，每条不超过约一行半。
- 不要把论文摘要、引言段落或方法段落整段搬上幻灯片。
- 中文内容应短句、短行、多换行，避免大块连续段落。
- 主标题应让听众在不听讲解时也能知道本页“想证明什么”。
- 细节、补充证明、完整引用、备选数据优先放入 speaker notes。

## Assertion-Evidence 结构

建议把下列结构作为默认母版，而不是少数场景的可选项：

| 组件 | 作用 | 生成要求 |
|---|---|---|
| `SectionTitle` | 章节或小节定位。 | 保持左上角，字号可以小于主张。 |
| `MainClaim` | 本页核心结论、判断或问题。 | 使用来源支持的完整句；字号大于正文。 |
| `EvidenceVisual` | 主要图、表、公式、流程图或机制图。 | 占据最大视觉空间，只服务一个中心信息。 |
| `EvidenceAnnotation` | 箭头、标签、圈注、关键值。 | 直接连接证据与主张，避免图例远置。 |
| `Qualifier` | 实验条件、适用范围、限制或简短 takeaway。 | 一行或短句，不与主证据竞争。 |
| `SpeakerNotes` | 细节解释和口头讲稿。 | 只来自用户给定来源。 |

## 字号与排版规则

从报告筛出的建议字号：

| 元素 | 口头报告建议 | 线上直播建议 | 对现有技能的影响 |
|---|---|---|---|
| 章节标签 | 18-22pt | 20-24pt | 现有 18pt 可保留为 section label。 |
| 主标题/主张 | 32-44pt | 36-48pt | 现有 18-24pt 不适合作为主张标题。 |
| 二级标题/panel heading | 24-32pt | 28-36pt | 现有 24-28pt 可作为下限。 |
| 正文 | 24-32pt | 28-36pt | 现有 15-20pt 应改为紧急 fallback。 |
| 图表坐标/标签 | 20-28pt | 24-32pt | 需要新增图表标签字号要求。 |
| Caption/注释 | 18-20pt | 20-24pt | 现有 12-15pt 明显偏小。 |
| 公式 | 22-30pt | 24-32pt | 中央公式应大于普通公式。 |

可筛入的排版细则：

- 18pt 应定义为所有可见文字的硬下限，而不是常规正文大小。
- 正文默认使用 24pt 以上；线上或直播场景整体再上调一级。
- 多行正文行距控制在 1.3-1.5。
- 双语、定义密集或术语较多的文本可用 1.4-1.6 行距。
- 主标题行距控制在 1.1-1.2。
- 段落文本左对齐，避免强制两端对齐。
- 字体数量控制在两种以内；中英混排可按脚本拆分形状或 runs。
- 不应通过缩小字号解决溢出，先删减内容或改变版式。
- 图表标签比普通 caption 更需要可读，因为投影后最容易看不清。

## 色彩与可访问性规则

可直接筛入的色彩规则：

- 普通文字与背景对比度至少 `4.5:1`。
- 大号文字和关键图形对象对比度至少 `3:1`。
- 图表类别不应只靠颜色区分。
- 类别区分应叠加形状、线型、marker、标签、描边、箭头或分组文字。
- 避免用红绿对置作为主要编码。
- 强调色只用于结论、关键数值、显著变化、警示或用户明确要求强调的对象。
- 红色强调应配合文字、线型或标注，不能单独作为“危险/显著”的唯一表达。
- 黄色不宜作为白底正文颜色；若用 `FFC000` 做 caption 底色，文字必须为黑色，并检查边界和对比。
- 图表和强调信息应通过灰度预览仍能被区分。
- 除黑白灰外，同页尽量控制在两种色系以内；多分类图表例外，但必须使用可辨识 palette。

可筛入的浅底 palette：

| 角色 | 色值 |
|---|---|
| 背景 | `FFFFFF` |
| 正文 | `111827` |
| 主色 | `0B5CAD` |
| 辅助色 | `64748B` |
| 强调色 | `C2410C` |

可筛入的深底/会场 palette：

| 角色 | 色值 |
|---|---|
| 背景 | `0B1020` |
| 正文 | `F8FAFC` |
| 主色 | `7DD3FC` |
| 辅助色 | `94A3B8` |
| 强调色 | `F59E0B` |

可作为多分类图表 palette 的色觉友好色值：

- `0072B2`
- `E69F00`
- `009E73`
- `D55E00`
- `CC79A7`
- `56B4E9`

## 布局规则

可筛入的布局骨架：

1. 顶部定位区：`section_title` + 分隔线。
2. 主张区：一个完整结论句或研究问题。
3. 证据区：一张主图、一张主表、一个公式、一个流程图或一个机制图。
4. 标注区：贴近证据的标签、箭头、圈注、关键数值。
5. 限定区：实验条件、适用范围、来源说明或一行 takeaway。

具体规则：

- 主要信息应放在上方或视觉路径最早到达的位置。
- 主标题和证据区之间保留清楚留白。
- 一页优先保留一个主视觉对象。
- 避免同页放三张以上同等大小的小图。
- 并列比较时，视觉对象与对应解释必须上下或左右对齐。
- 2-row 比较结构应优先让视觉在上、解释在下。
- 机制、流程、因果路径优先画成流程图或机制示意图，不写成段落。
- 公式推导页应让核心公式居中或占据主要空间，假设/定义贴近公式。
- 线上模式应避开字幕、摄像头或会议控件可能遮挡的角落。
- 留白用于分组和降低竞争，不作为装饰。

## 图表规则

按分析任务筛入图表选择规则：

| 分析任务 | 优先图表 | 谨慎使用 | 关键规则 |
|---|---|---|---|
| 类别比较 | 条形图、点图 | 饼图、3D 柱图 | 按数值或逻辑顺序排列，突出基准线。 |
| 时间变化 | 折线图 | 过多系列叠加图 | 1-4 条最清晰，6 条以上应拆分或简化。 |
| 变量关系 | 散点图 | 仅靠面积编码的气泡图 | 坐标含义和单位必须清楚。 |
| 分布形态 | 直方图、箱线图 | 大表格堆数字 | 同组之间保持一致分箱和尺度。 |
| 构成占比 | 堆叠条形图 | 饼图、环形图 | 仅类别很少且不需精确比较时考虑。 |
| 流程机制 | 流程图、机制图 | 项目符号段落 | 使用箭头、阶段名和直接标签。 |

图表标注规则：

- 图内直接标注优先。
- 只有当直接标注会严重拥挤时才使用独立图例。
- 图例应靠近数据对象，视觉显著度低于数据本体。
- 轴标题、图题、图例和 caption 写完整变量名与单位。
- 不使用未解释缩写。
- 保留来源单位、实验条件和分组名称。
- 高亮只用于来源明确支持的关键结果。
- 数据不足时不得生成虚构图表；应询问或建立明确 placeholder。

## 图片与插图规则

可筛入的图片规则：

- 优先使用原始高分辨率图片或矢量图。
- 有源图、矢量导出或数据可重画时，不使用低清截图。
- 插入前裁切到能支持本页主张的证据区域。
- 删除无关装饰背景。
- 学术证据页不使用剪贴画、氛围图或装饰性大图。
- 图片内若有关键文字，必须在 alt text 或邻近文本中重复。
- Caption 要保留图号、实验条件、单位和来源描述。
- 用箭头、圈注、短标签降低误读。
- 只有用户提供了足够图片描述但没有文件时，才建立 placeholder。
- Placeholder 必须明确标注为 placeholder，并保留用户原始描述。
- 机制图、流程图、框架图优先使用矢量 shape，便于缩放和跨平台显示。

## 表格规则

可筛入的表格规则：

- 表格只用于精确值比较或紧凑条件对照。
- 列很多时，只保留支撑中心主张的关键列。
- 如果任务是比较大小、趋势或分布，优先转成图表。
- 只高亮一到两个关键数值，避免整片高亮。
- 单位放入表头。
- 数字列应便于比较，尽量对齐。
- 表格不能通过压到 18pt 以下来强行适配。
- 密集补充数值进入 speaker notes，或提示用户拆页。

## 公式规则

可筛入的公式规则：

- 公式可以作为主证据，不应被当成脚注。
- 中心公式应大于普通正文。
- OfficeCLI equation 不可靠时保留原 LaTeX，而不是错误转换。
- 定义、假设、边界条件放在公式附近。
- 长解释进入 side note 或 speaker notes。
- 若公式支撑主结论，应给足留白，保证投影可读。

## 输入契约增强项

建议给 `input-contract.md` 增加这些可选字段：

```json
{
  "central_claim": "optional source-supported sentence used as the main claim",
  "presentation_mode": "optional: oral, online, poster_like; default oral",
  "audience_context": "optional viewing distance, venue, or viewer constraints",
  "evidence_priority": "optional ranked figures, data, formulas, or claims",
  "chart_task": "optional: category_comparison, trend, relationship, distribution, composition, process",
  "accessibility_level": "optional: standard or strict",
  "label_policy": "optional preference for direct labels, legend, or both",
  "color_constraints": "optional institutional colors or color-blind-safe requirement"
}
```

建议新增澄清触发条件：

- 用户材料无法无损压缩成一个中心主张。
- 用户要求结论句，但来源没有支持。
- 用户要求图表，但没有 chart-ready data。
- 关键视觉对象内部文字过多，无法投影阅读。
- 只有低于 18pt 才能放下所有内容。
- 用户指定线上/投影/海报场景，但尺寸、可读性或遮挡区域会改变版式。

## 验证清单增强项

适合加入 `verification-checklist.md`：

- 是否有来源支持的 `MainClaim`。
- 是否只有一个中心信息单元。
- 可见正文是否不低于 18pt。
- 常规正文是否尽量达到 24pt 以上。
- Caption 是否不低于 18pt。
- 图表标签是否足够大。
- 普通文字对比度是否达到 4.5:1。
- 大号文字和关键图形是否达到 3:1。
- 是否没有仅靠颜色表达的分组或强调。
- 红绿是否没有作为唯一编码。
- 多系列图表是否有直接标签或近距离图例。
- 轴、图例、caption 是否保留变量名和单位。
- 是否有唯一描述性标题。
- 阅读顺序是否为标题、主张、证据、标注、caption、限定说明。
- 图片是否有 alt text。
- 图片内关键文字是否在可访问文本中重复。
- 灰度预览后类别和强调是否仍可辨认。
- 投影或缩小预览后是否仍可读。
- 线上小窗或 125% 缩放检查是否可读。
- 是否没有文本裁切、重叠或越界。
- Speaker notes 是否只来自用户来源。

## 验证脚本可实现项

适合后续增强 `scripts/validate_academic_pptx.py`：

| 检查项 | 通过标准 | 实现提示 |
|---|---|---|
| 字号下限 | 可见文字不低于 18pt。 | 依赖 OfficeCLI shape 查询能力。 |
| 正文字号 | `Body*` 等文本形状尽量不低于 24pt。 | 需要命名约定。 |
| Caption 字号 | `Caption*` 不低于 18pt。 | 需先更新规范。 |
| 对比度 | 普通文本 4.5:1，大号文本/图形 3:1。 | 从 font color 和 fill 计算。 |
| 文本密度 | 可见字符或 token 不超过阈值。 | 使用 `officecli view text`。 |
| Bullet 数量 | 项目符号不超过 5 条。 | 解析提取文本。 |
| 长段落 | 过长连续文本报警。 | 字符数/行数启发式。 |
| Alt text | 图片无 alt text 报错。 | 已有 `picture:no-alt`，可继续扩展。 |
| 命名形状 | 检查 `SectionTitle`、`MainClaim`、`EvidenceVisual`、`Caption`。 | 依赖 `view annotated` 或 query。 |
| 阅读顺序 | 命名形状顺序符合视觉顺序。 | 可先人工检查，后自动化。 |
| 色彩风险 | 红绿唯一编码或多色无标签报警。 | 可做启发式，难以完全自动化。 |
| 图表单位 | 轴/图例/caption 缺单位时报警。 | 需要从源数据或文本中推断。 |
| 灰度/小窗 | 导出预览用于人工或截图检查。 | 可先作为人工验收项。 |

## Layout Preset 候选

适合加入 `assets/layout-presets.json` 的 preset：

| Preset | 用途 | 默认特征 |
|---|---|---|
| `oral_light_assertion_evidence` | 默认学术口头报告页。 | 白底、深色文字、34-38pt 主张、一个主证据。 |
| `online_light_large_text` | 线上会议或直播页。 | 更大字号、更少元素、预留角落安全区。 |
| `dark_venue_assertion_evidence` | 深色会场或录屏。 | 深底、高对比、线宽和 marker 加粗。 |
| `comparison_direct_label` | 并列结果比较。 | 视觉上排、解释下排、直接标注优先。 |
| `formula_evidence` | 公式/推导作为主证据。 | 中央大公式、侧边定义、短限定。 |
| `table_to_takeaway` | 小表格支持结论。 | 关键列、关键值高亮、短 takeaway。 |

## 后续改造最小集合

如果后续只做一轮小改造，建议优先做这六项：

1. 把 `main_claim` / `central_claim` 加入输入和默认结构。
2. 把 assertion-evidence 设为默认生成策略。
3. 把可见文字硬下限设为 18pt，并提高正文/caption 默认字号。
4. 加入 4.5:1 / 3:1 对比度规则。
5. 图表必须有完整变量名、单位，并优先直接标注。
6. 验证清单增加灰度、投影和线上小窗预览。

## 低优先级或暂不直接筛入内容

- “每分钟约一页”主要用于整套报告节奏，对单页生成只作为信息密度参考。
- 海报式长图的 2-4 列浏览路径不是 `aca-slide-pptx-gen` 默认目标，除非用户明确要 poster-like slide。
- 实时字幕、媒体字幕更适合完整演示工作流；本技能可先做遮挡安全区或 final response 提醒。
- 课题组级母版治理有价值，但对一次性单页生成不是最小必要项。

## English Working Appendix

## Screening Criteria

Keep a finding when it satisfies at least one condition:

- It improves comprehension, recall, or reduces misunderstanding in academic slides.
- It can be translated into a concrete one-slide `.pptx` generation rule.
- It can be verified through OfficeCLI output inspection, a validation script, or manual
  preview.
- It strengthens accessibility, readability, chart interpretation, or source-faithful
  academic communication.
- It reduces common failure modes in generated slides, such as dense text, small labels,
  low contrast, weak figure captions, remote legends, or unsupported visual claims.

Deprioritize findings when they mainly target cover pages, full-deck sequencing, poster
design, marketing slides, or software-specific features unavailable through OfficeCLI.

## Highest-Value Additions

These findings should be treated as the strongest candidates for direct integration into
`aca-slide-pptx-gen`.

| Priority | Finding | Why it improves the skill | Likely target |
|---|---|---|---|
| P0 | Use assertion-evidence structure: one sentence-like central claim plus visual evidence. | Current skill has `section_title` and `topic`, but does not strongly require a conclusion-style main claim. | `SKILL.md`, `layout-and-style-spec.md`, input contract |
| P0 | One slide should carry one central information unit. | Prevents generated slides from trying to include background, method, result, and conclusion on one canvas. | input reduction rules, verification checklist |
| P0 | Prefer visual evidence over dense bullet lists. | Aligns with academic presentation evidence structure and reduces text overflow. | workflow, layout rules |
| P0 | Raise default readable font sizes. | Existing spec allows body text at 15-20pt and captions at 12-15pt, which is below the report's safer oral-presentation recommendations. | typography spec, validator |
| P0 | Add contrast checks: normal text 4.5:1, large text and key graphics 3:1. | Current color rules name colors but do not define measurable contrast thresholds. | style spec, validator |
| P0 | Do not rely on color alone; add shape, line style, direct labels, arrows, or text. | Current emphasis colors can fail for color-vision-deficient viewers. | chart rules, visual rules |
| P0 | Prefer direct labels inside charts over distant legends. | Reduces visual search and improves accessibility. | chart generation rules |
| P0 | Require complete variable names and units on axes, labels, legends, captions, and tables. | Protects academic meaning and source fidelity. | chart/table rules |
| P1 | Use grayscale, projection, and online-small-window previews as final checks. | Adds realistic presentation environment verification beyond schema validity. | verification checklist |
| P1 | Use high-resolution or vector images; crop to the evidence-bearing region. | Prevents decorative or unreadable image insertion. | figure rules |
| P1 | Keep each slide's visible title unique and descriptive, even if a structural title is separate from the section label. | Helps accessibility and reading order. | output contract, validator |
| P1 | Check reading order and alt text, not only visual placement. | Current checklist includes alt text but not reading order. | verification checklist |
| P1 | Use color-blind-safe palettes for multi-series charts. | Current palette is limited to two emphasis colors and no chart palette. | layout presets |
| P1 | Keep line length short and avoid pasted paragraph blocks. | Helps Chinese and English slide readability. | text reduction rules |
| P2 | Add scene-aware presets for oral, online, and poster-like exports. | The target skill creates one slide, but viewing context can affect font sizes and layout density. | input contract, presets |

## Existing Coverage Versus Missing Upgrades

| Area | Already present in `aca-slide-pptx-gen` | Useful upgrades from report |
|---|---|---|
| Canvas | 16:9 `33.87cm x 19.05cm`, safe bounds. | Add projection/online readability checks and subtitle/camera safe zone for online mode. |
| Header | Upper-left section title plus separator. | Add a separate sentence-like main claim when `section_title` is only a section label. |
| Source policy | Strong anti-fabrication rules. | Add explicit "do not strengthen topic into a claim unless source supports it"; otherwise ask or use a neutral question title. |
| Typography | Explicit fonts, Chinese `Microsoft YaHei`, English `Calibri`. | Raise defaults; make 18pt a hard floor, not normal body size; use larger chart labels. |
| Colors | Fixed caption and emphasis colors. | Add contrast ratios, color-blind-safe chart colors, and no-color-only encoding. |
| Captions | Caption fill `FFC000`, black text. | Add caption length limits, unit/condition preservation, and contrast validation for yellow fill. |
| Figures | Insert pictures, placeholders, and alt text. | Add cropping, high-resolution/vector preference, image text duplication in alt text. |
| Charts | Use charts only with chart-ready data. | Add chart type selection by analytic task and direct labeling. |
| Tables | Use compact tables. | Add "key columns only"; prefer chart or highlighted values when a table is dense. |
| Formulas | Preserve LaTeX and use equation when possible. | Add larger formula sizing and side-note layout guidance. |
| Verification | OfficeCLI validate, issues, annotated, text, html, no-alt. | Add font-size minima, contrast, density, reading order, grayscale, and small-window checks. |

## Content Structure Rules To Transfer

1. Treat `topic` as the candidate central message, not merely a noun phrase.
2. If `topic` is a topic-word title, derive a source-supported assertion only when the
   supplied text clearly supports it.
3. If no supported assertion can be derived, use a neutral research question or
   descriptive topic and avoid inventing a conclusion.
4. Keep one central information unit per slide.
5. Prefer this hierarchy: main claim, visual evidence, one short qualifier or takeaway.
6. Do not place background, method, result, and conclusion at equal visual weight on a
   single slide.
7. When source material is overlong, reduce in this order:
   central claim first, strongest evidence second, essential method/condition third,
   caveat or limitation fourth.
8. Delete text that the speaker can say aloud and that does not need to be visually
   retained.
9. If a slide would need body text below 18pt, treat it as too dense and ask to split,
   summarize, or choose the main evidence.
10. Convert bullet-heavy input into visual evidence plus compact annotations where
    source data supports it.
11. If bullets are unavoidable, keep 3-5 bullets maximum and keep each bullet within
    roughly one to one-and-a-half lines.
12. Avoid paragraph blocks copied from papers or abstracts.
13. Use short phrases, short lines, and intentional line breaks for Chinese slides.
14. Make the title or main claim meaningful enough that a viewer can understand the
    slide's message before hearing the narration.
15. Use speaker notes for source-supported details that should not occupy the visible
    slide.

## Assertion-Evidence Pattern

Add an explicit pattern for most academic content slides:

- `section_title`: small location label at upper-left, such as chapter, subsection, or
  paper section.
- `main_claim`: larger sentence-style assertion or research question below the rule or
  at the top of the content region.
- `evidence_visual`: the main figure, chart, table, formula, or mechanism diagram.
- `evidence_annotations`: arrows, labels, callouts, or highlighted values that connect
  the visual to the claim.
- `qualifier`: a short source-supported limitation, condition, or interpretation.

This avoids the current risk that `section_title` becomes the only title and remains too
generic to guide audience understanding.

## Typography Rules To Transfer

Use these as safer defaults for generated oral academic slides:

| Element | Recommended range | Notes for skill integration |
|---|---|---|
| Section label | 18-22pt | Existing 18pt is acceptable because it is a locator, not the main message. |
| Main claim/title | 32-44pt oral; 36-48pt online | Current 18-24pt is too small for the main academic claim. |
| Panel heading | 24-32pt oral; 28-36pt online | Existing 24-28pt is acceptable but should not shrink. |
| Body text | 24-32pt oral; 28-36pt online | Current 15-20pt should become fallback-only. |
| Chart axis labels | 20-28pt oral; 24-32pt online | Raise labels because chart text often becomes unreadable first. |
| Captions | 18-20pt oral; 20-24pt online | Existing 12-15pt is too small for projected slides. |
| Footnotes/references | 18-20pt, minimal | If below 18pt is needed, move detail to notes or backup context. |
| Formulas | 22-30pt, larger for central equations | Existing 18-26pt can stay only for compact secondary formulas. |

Additional typography constraints:

- Treat 18pt as an accessibility floor for any visible content, not as the normal body
  size.
- Prefer 24pt or larger for body text in line-of-sight oral presentations.
- Use 28pt or larger for online/live-stream slides because viewers may see a compressed
  or small-window stream.
- Use line spacing around 1.3-1.5 for body text.
- Use line spacing around 1.4-1.6 for bilingual or definition-heavy blocks.
- Use title line spacing around 1.1-1.2.
- Avoid forced full justification; use left alignment for prose.
- Keep a single slide to no more than two font families unless mixed-script coverage
  requires fallback handling.
- Keep Chinese text in a screen-stable sans font. Existing `Microsoft YaHei` is usable;
  future optional presets could include Source Han Sans or Noto Sans SC when available.
- Keep English text in Calibri by default; optional accessible labels can use Arial,
  Verdana, or Atkinson Hyperlegible if installed and requested.
- Avoid reducing font size to solve layout overflow; reduce content first.

## Color And Contrast Rules To Transfer

Add measurable color quality rules:

- Normal text and background contrast should be at least `4.5:1`.
- Large text contrast should be at least `3:1`.
- Essential graphical objects should contrast at least `3:1` against adjacent colors.
- Do not use color as the only semantic encoding.
- For chart categories, pair color with one or more of:
  shape, line style, direct text label, marker type, pattern, arrow, or group label.
- Avoid red-green opposition as the main distinction between two groups.
- For warning or significance emphasis, red can be used only with text, icon, line style,
  or label support.
- Yellow should not be used as body text color on white. Existing `FFC000` caption fill
  is acceptable only with black text and adequate boundary contrast.
- Check grayscale legibility for charts and emphasis.
- Avoid decorative one-hue palettes that reduce visual hierarchy.

Candidate palettes from the report:

| Use | Background | Text | Main | Secondary | Emphasis |
|---|---|---|---|---|---|
| Light academic | `FFFFFF` | `111827` | `0B5CAD` | `64748B` | `C2410C` |
| Dark venue/stream | `0B1020` | `F8FAFC` | `7DD3FC` | `94A3B8` | `F59E0B` |

Candidate color-blind-safe chart colors:

- `0072B2`
- `E69F00`
- `009E73`
- `D55E00`
- `CC79A7`
- `56B4E9`

These should be added as chart palettes, not as decorative slide-wide color themes.

## Layout Rules To Transfer

Recommended slide skeleton:

1. Header/locator area: section title plus separator.
2. Claim area: one complete sentence or question that names the slide's message.
3. Evidence area: one dominant figure, chart, table, formula, or mechanism diagram.
4. Annotation layer: labels, arrows, callouts, or highlights attached to evidence.
5. Footer/qualifier area: short caveat, condition, source note, or method qualifier.

Detailed layout guidance:

- Put the most important message near the top or the earliest visual path.
- Keep title and evidence separated by visible whitespace.
- Use one dominant visual object whenever possible.
- Avoid three or more equally sized small figures on one slide.
- When comparing panels, keep each visual aligned with its matched explanation.
- For parallel comparisons, prefer a 2-row structure: visual row above, explanation row
  below.
- For mechanism or workflow content, use a flow diagram rather than paragraphs.
- For formula derivations, place the central equation in a large formula region and move
  assumptions/definitions into side notes.
- For online mode, reserve space where subtitles, meeting controls, or camera overlays
  are likely to obscure corners.
- Use generous whitespace as an information grouping device, not decoration.
- Keep animation rare and only for stepwise explanation; do not depend on animation for
  the static `.pptx` to make sense.

## Chart Type Selection Rules

Map the analytic task to chart type before styling:

| Task | Prefer | Use cautiously | Rules to add |
|---|---|---|---|
| Category comparison | Bar chart or dot plot | Pie chart, 3D bar chart | Sort by value or logical order; show baseline. |
| Time trend | Line chart | Too many overlapping series | 1-4 lines are clearest; 6+ should be split or simplified. |
| Variable relationship | Scatter plot | Bubble chart if area is the only encoding | Label axes with full names and units. |
| Distribution | Histogram or box plot | Dense numeric table | Keep bins/scales consistent across groups. |
| Composition | Stacked bar | Pie or donut chart | Use only when categories are few and exact comparison is not central. |
| Process/mechanism | Flowchart or mechanism diagram | Bullet list | Use arrows and direct labels. |
| Key numeric result | Large number plus small context chart | Full table | Include unit, denominator, and condition. |

Chart labeling rules:

- Prefer direct labels on or near plotted objects.
- Use remote legends only when direct labeling would overload the figure.
- If a legend is necessary, place it close to the associated data.
- Keep legend less visually prominent than the data.
- Write full variable names and units.
- Avoid unexplained abbreviations in axes and labels.
- Preserve source units exactly.
- Highlight only source-supported key results.
- Do not invent chart values; if data are missing, ask or create a labeled placeholder.

## Figure And Image Rules

Transfer these image-quality rules:

- Prefer original high-resolution images or vector assets.
- Do not use low-resolution screenshots when a source figure, vector export, or data
  redraw is available.
- Crop images to the evidence-bearing region.
- Remove decorative or irrelevant background areas.
- Do not use clip art or atmospheric images for academic evidence.
- If a picture contains essential text, repeat that information in alt text or nearby
  accessible text.
- Add concise captions that preserve figure labels, experimental conditions, units, and
  source-provided descriptions.
- Use arrows, circles, labels, or short callouts to reduce ambiguity.
- Use placeholders only when the user gave enough figure description but no file.
- Label placeholders explicitly and preserve the user's wording.
- For mechanism diagrams and workflows, prefer vector shapes so scaling remains clear.

## Table Rules

Transfer these table-specific rules:

- Use tables only for compact comparisons where exact values matter.
- If a table has many columns, keep only the columns required by the central message.
- Prefer a chart when the viewer needs to compare magnitudes or trends.
- Highlight only one or two key values, not entire rows indiscriminately.
- Keep units in headers.
- Use readable numeric alignment.
- Avoid compressing tables until text falls below 18pt.
- Move dense supplementary values to speaker notes or ask whether to split.

## Formula Rules

Useful formula improvements:

- Treat central equations as evidence visuals, not footnotes.
- Use larger equation sizing than ordinary body text.
- Preserve original LaTeX exactly when conversion is uncertain.
- Put definitions, assumptions, and boundary conditions close to the equation.
- Use side notes rather than long inline prose.
- If a formula is the main claim support, give it enough whitespace to be read from a
  projector.

## Accessibility Rules To Transfer

Add these to the output contract and verification checklist:

- Every slide should have a unique descriptive title in the structural layer or an
  equivalent named title shape.
- Reading order should match visual order: title, main claim, evidence, labels, caption,
  qualifier.
- Every real picture should have alt text.
- Images with embedded text should have the important embedded text repeated in alt text
  or slide text.
- Contrast should meet measurable thresholds.
- Charts should remain understandable in grayscale.
- Meaning should not depend on color alone.
- Text should not be clipped or hidden by shape boundaries.
- Viewer-critical content should not sit in likely subtitle/camera-overlay regions for
  online slides.
- Caption or speaker-note source support should be traceable to supplied material.

## Verification And Validator Upgrades

Candidate additions for `validate_academic_pptx.py` or a future validation layer:

| Check | Pass condition | Implementation notes |
|---|---|---|
| Minimum visible font size | No visible text below 18pt except explicitly allowed structural metadata. | Query shape text sizes if OfficeCLI exposes them. |
| Body font default | Main body text should be 24pt or larger in oral mode. | May need shape naming conventions such as `Body*`, `Caption*`, `AxisLabel*`. |
| Caption size | Captions should be 18pt or larger. | Current spec should change first. |
| Contrast ratio | Text/background >= 4.5:1 normal; >= 3:1 large. | Compute from shape fill and font color when available. |
| Color-only encoding | Warn when charts use multiple colors but no labels/marker variation. | Hard to automate fully; can be a heuristic. |
| Red-green risk | Warn when red and green are the only category differentiators. | Check chart palette or named shapes. |
| Direct labels | Warn when multi-series charts have a legend but no direct labels. | Best as manual checklist unless OfficeCLI chart internals are queryable. |
| Axis units | Warn when chart axes lack units and source data included units. | Requires source metadata or shape text search. |
| Text density | Warn when visible text exceeds a threshold. | Count tokens/characters from `officecli view text`. |
| Bullet density | Warn on more than 5 visible bullets. | Parse extracted text. |
| Paragraph block | Warn on long paragraph text blocks. | Character count and line count heuristic. |
| Reading order | Verify named shapes follow intended order. | Use OfficeCLI annotated output if available. |
| Alt text completeness | Already partly covered by `picture:no-alt`; expand to embedded-text cases manually. | Add final checklist item. |
| Grayscale preview | Produce or request grayscale preview check. | May be manual or image-export based. |
| Small-window preview | Use HTML preview or exported image at reduced size. | Manual or automated screenshot comparison. |
| Bounds | Already covered conceptually; keep strict geometry checks. | Existing shape bounds rule remains useful. |

## Input Contract Additions

Potential optional fields to add:

```json
{
  "central_claim": "optional source-supported sentence to use as the main claim",
  "presentation_mode": "optional: oral, online, poster_like, default oral",
  "audience_context": "optional viewing distance, venue, or expected viewer constraints",
  "evidence_priority": "optional ranked list of figures, data, formulas, or claims",
  "chart_task": "optional analytic task such as category_comparison, trend, relationship, distribution, composition, process",
  "accessibility_level": "optional: standard or strict",
  "label_policy": "optional preference for direct labels, legend, or both",
  "color_constraints": "optional institutional colors or color-blind-safe requirement"
}
```

Clarification triggers to add:

- Ask when the supplied content cannot be reduced to one central claim without changing
  meaning.
- Ask when chart-ready data are absent but the user requests a chart.
- Ask when the user requests a conclusion sentence not supported by the source.
- Ask when a required visual contains too much small embedded text to be readable.
- Ask when a slide can fit only by using text below the minimum readable size.

## Preset Additions

Useful future presets:

| Preset | Purpose | Defaults |
|---|---|---|
| `oral_light_assertion_evidence` | Default academic talk slide. | White background, dark text, main claim 34-38pt, body 24-28pt, one dominant visual. |
| `online_light_large_text` | Meeting or live-stream slide. | White background, larger type, fewer objects, reserved lower corner safe area. |
| `dark_venue_assertion_evidence` | Dark lecture hall or recording. | Dark background, high-contrast text, larger chart lines and markers. |
| `comparison_direct_label` | Parallel result panels. | 2-row panel layout, direct labels, no remote legend when possible. |
| `formula_evidence` | Equation-centered slide. | Large central equation, side definitions, source-supported qualifier. |
| `table_to_takeaway` | Compact table plus highlighted conclusion. | Key columns only, highlight one result, short takeaway. |

## Skill Document Changes Worth Planning

Candidate changes for `aca-slide-pptx-gen/SKILL.md`:

- Add `main_claim` as a first-class concept separate from `section_title`.
- State that the default slide pattern is assertion-evidence.
- State that dense bullet slides are fallback, not the default.
- Raise typography guidance and define 18pt as a floor.
- Add measurable contrast and no-color-only rules.
- Add direct chart labeling and chart-type selection by analytic task.
- Add reading order and unique descriptive title requirements.
- Add projection, grayscale, and online preview checks to verification.

Candidate changes for `references/layout-and-style-spec.md`:

- Revise typography ranges upward.
- Add assertion-evidence layout geometry.
- Add oral, online, and dark-mode presets.
- Add chart palette and contrast thresholds.
- Add direct-label chart guidance.
- Add subtitle/camera safe-area guidance for online mode.

Candidate changes for `references/verification-checklist.md`:

- Add font-size minima.
- Add contrast ratio checks.
- Add no-color-only checks.
- Add chart direct-label/near-legend checks.
- Add axis/unit completeness checks.
- Add reading order checks.
- Add grayscale and small-window preview checks.
- Add text-density and bullet-count checks.

Candidate changes for `references/input-contract.md`:

- Add optional `central_claim`, `presentation_mode`, `audience_context`,
  `evidence_priority`, `chart_task`, `accessibility_level`, and `color_constraints`.
- Add clarification triggers for unsupported central claims and over-dense slides.

Candidate changes for `assets/layout-presets.json`:

- Add assertion-evidence geometry.
- Add oral/online/dark variants.
- Add chart palette definitions.
- Add semantic shape names for validation.

Candidate changes for `scripts/validate_academic_pptx.py`:

- Add style-rule checks if OfficeCLI exposes shape-level font, fill, and color metadata.
- Add heuristic checks over extracted text for density and bullets.
- Add named-shape checks for `SectionTitle`, `MainClaim`, `EvidenceVisual`,
  `Caption`, `Qualifier`, and `Notes`.

## Proposed Quality Rubric

Use this rubric to score generated slides during future tests:

| Dimension | Good output | Common failure to catch |
|---|---|---|
| Central claim | One clear source-supported message. | Topic-only title or invented conclusion. |
| Evidence | One dominant visual or compact evidence block. | Many small figures competing equally. |
| Text density | Short visible text, details in notes. | Abstract-like paragraphs or long bullets. |
| Typography | Main claim and body readable from projection. | 12-18pt body/caption used to force fit. |
| Contrast | Meets measurable thresholds. | Pale text, yellow text, low-contrast chart objects. |
| Color accessibility | Color plus label/shape/line encoding. | Red-green or color-only categories. |
| Chart clarity | Correct chart type, direct labels, units. | Pie/3D chart, distant legend, missing units. |
| Image quality | Cropped high-resolution evidence. | Blurry screenshot or decorative image. |
| Accessibility | Alt text, reading order, unique title. | Picture-only slide with no alt text. |
| Source fidelity | No unsupported claims or numbers. | Generated labels or conclusions not in source. |

## Screened Findings Not Directly Integrated

These report elements are useful context but less direct for the current one-slide skill:

- Full-deck pacing such as "one page per minute" is only indirectly useful because the
  skill outputs one slide.
- Poster-specific sizing and 2-4 column poster paths are lower priority unless the user
  requests poster-like slide output.
- Live subtitles and media captioning are relevant to full presentations, but the one
  slide generator can only reserve space or note the requirement.
- Institution-level master template governance is useful for future presets but not
  necessary for single-slide generation.

## Minimal Update Set If Time Is Limited

If only a small implementation pass is possible later, prioritize these six upgrades:

1. Add `main_claim` and assertion-evidence as the default structure.
2. Raise visible font defaults: body/captions at least 18pt, normal body preferably
   24pt or larger.
3. Add WCAG-style contrast thresholds.
4. Require chart labels/units and avoid color-only encoding.
5. Prefer direct chart labels over distant legends.
6. Add grayscale, projection, and small-window checks to verification.
