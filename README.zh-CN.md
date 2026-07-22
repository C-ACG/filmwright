[English](README.md) · **简体中文**

# Filmwright：编导智能体系统

**一套面向高能力大模型、模型中立的编剧、导演、连续性管理与生成式制作协议。**

Filmwright 可以把一句创意、原始资料、故事大纲或已有剧本，转化为项目当前真正需要的产出物：开发笔记、故事梗概、节拍表、场景地图、Fountain 剧本、连续性状态、分镜表、AI 视频生成执行包，或诊断报告。其创作核心完全采用可移植的 Markdown、Fountain 与 CSV，不依赖专用运行环境。

当前源码版本：**0.2.0** · [更新日志](CHANGELOG.md) ·
[模型兼容性证据](docs/model-compatibility.md)

Filmwright 的设计目标是**模型中立**，这不等于“已经在所有模型上验证”。具体模型与宿主环境的测试结果应记录在兼容性矩阵中；v0.2 对尚未实测的能力明确标记为未测试，而不是凭空猜测。

## v0.2 新增内容

- **四种工作模式：** Guided 用于协作创作，Sprint 用于端到端起草，Direct 用于直接生成一个边界明确的产出物，Review 用于只诊断、不擅自改写。
- **直接进入目标阶段：** 分镜请求可直接进入阶段 7d，场景审阅可直接进入质量检查。阶段 0 加上八个创作与质量阶段（其中 7d 为导演子阶段），共同组成依赖图，而不是必须机械走完的仪式流程。
- **唯一项目状态：** 稳定 ID、已锁定设定、角色知识、时间线、道具与场景、伏笔、决策和状态增量，都能跨越长项目与多轮修改持续保存。
- **依赖完整的记忆机制：** 经过依赖校验的事件图子记录与逐场景上下文包，取代把全部历史内容反复塞回模型的做法。
- **来源信任边界：** 小说、剧本、网页和检索文本始终被视为数据，即使其中包含指令。事实、原作设定、推断和新增创作可以清楚区分。
- **AI 视频制作支持：** 素材与参考锁定、首尾帧连续性、模型适配器、代理版与终版闸门、已采纳镜次记录，以及多模态质量检查。
- **可维护的工程体系：** 语义化版本、更新日志、清单文件、统一分镜规范、确定性校验器、行为评测目录、持续集成，以及修正后的端到端示例。

## 产出物

| 产出物 | 可移植格式 | 标准模板 |
|---|---|---|
| 项目与设定状态 | Markdown + YAML 文件头 | [`project-state.md`](templates/project-state.md) |
| 故事梗概 | Markdown | [`treatment.md`](templates/treatment.md) |
| 节拍表 | Markdown | [`beat-sheet.md`](templates/beat-sheet.md) |
| 事件图与场景地图 | Markdown 表格 | [`event-graph.md`](templates/event-graph.md) / [`scene-card.md`](templates/scene-card.md) |
| 剧本 | Fountain | [`fountain.md`](templates/fountain.md) |
| 分镜表 | Markdown / 标准 CSV | [`shot-list.md`](templates/shot-list.md) / [`shot-list.csv`](templates/shot-list.csv) |
| AI 视频执行包 | Markdown / YAML 区块 | [`generation-packet.md`](templates/generation-packet.md) |
| 交接与上下文 | Markdown | [`memory-checkpoint.md`](templates/memory-checkpoint.md) / [`context-pack.md`](templates/context-pack.md) |
| 质量检查 | 基于证据的评分卡 | [`quality-scorecard.md`](templates/quality-scorecard.md) |

## 快速开始

### 可读取仓库的智能体

打开本仓库，并明确提出创作任务：

```text
用 Filmwright 把这段梗概开发成一部 8 分钟短片，使用 Guided 模式。
直接把已锁定的 SC004 拆成一份 60 秒标准分镜 CSV。
审阅这份剧本，不要改写；给我硬闸门、证据和按优先级排列的修复项。
```

`AGENTS.md` 与 `CLAUDE.md` 都会先进入
[`system/entry-contract.md`](system/entry-contract.md)，用来区分“使用 Filmwright 创作”和“维护 Filmwright 仓库”。进入创作任务后，再加载
[`system/orchestrator.md`](system/orchestrator.md) 以及本次请求真正需要的模块。

### 纯聊天模型

1. 粘贴 `system/orchestrator.md`。
2. 提供你已知的项目卡信息，并说明所需模式与产出物。
3. 只粘贴对应任务路线指定的模块。
4. 自行保存模型输出的项目状态或状态增量。

纯聊天宿主和可读取文件的宿主遵循同一份协议，但执行能力并不完全相同。状态持久化、资料检索、多模态检查和并行质量检查，都取决于宿主环境是否真正具备相应能力。

模式示例与恢复工作流程见 [`docs/quickstart.md`](docs/quickstart.md)。

## 工作模式

| 模式 | 最适合 | 暂停规则 |
|---|---|---|
| Guided | 前提、人物与结构选择 | 遇到影响重大的决策时，通过 `pass / revise / review` 闸门确认 |
| Sprint | 完整草稿和“直接做完”类请求 | 对可逆选择继续执行，并记录假设 |
| Direct | 单场戏、转换、续写或分镜表 | 返回边界明确的产出物以及状态增量 |
| Review | 诊断、比较与质量检查 | 保持审阅对象不变，只有获得授权后才改写 |

## 工作流程

```text
0 契约 → 1 核心行动 → 2 梗概 → 3 人物 → 4 世界与设定
→ 5 结构 → 6 场景地图 → 7 剧本 → 7d 导演设计 → 8 质量检查
```

每个完成单元都遵循 `输入 → 工作 → 产出物 → 验收 → 状态增量`。已经批准的上游成果会被复用；Direct 与 Review 请求会从满足依赖所需的最早阶段进入。

## 状态与长篇连续性

项目状态是唯一的标准根记录。已登记的事件图与制作记录，是经过依赖校验的规范子记录；检查点、上下文包、剧集圣经表格和微短剧台账都只是投影视图，不是彼此竞争的多套设定真相。

稳定 ID 在修改后仍保持不变：

```text
CHAR-001 · LOC-001 · PROP-001 · SETUP-001 · EVT-001 · SC001 · DEC-001
SC004-SH003（独立分镜）· EP012-SC004-SH003（剧集分镜）
```

标准命名空间、补零规则、剧集组合方式、产出物版本和制作镜次 ID，详见
[`docs/id-conventions.md`](docs/id-conventions.md)。

开始新场景前，应构建一个上下文包，只包含本场景相关的已锁定事实、角色知识、实体状态、因果窗口、来源锚点和验收测试。场景完成后，将其状态增量合并回项目状态；上游决策一旦改变，应使受影响的下游产出物失效。

## 支持的格式

| 格式 | 默认规模 | 模块 |
|---|---|---|
| 概念超短片 | 1–3 分钟 | [`ultrashort.md`](modules/formats/ultrashort.md) |
| 叙事短片 | 约 5–15 分钟 | [`short.md`](modules/formats/short.md) |
| 长片 | 长片规模 | [`feature.md`](modules/formats/feature.md) |
| 剧集 / 单集 | 多集 | [`series.md`](modules/formats/series.md) |
| 竖屏微短剧 | 由平台定义 | [`vertical-microdrama.md`](modules/formats/vertical-microdrama.md) |
| 自定义 / 混合形式 | 明确覆盖默认规模 | 最接近的结构模块加项目卡 |

运行时标签只是默认分类，不代表其他形式不受支持。自定义配置必须明确说明覆盖了哪些结构或节奏假设。

## 导演设计与 AI 视频

导演层把走位、轴线与覆盖、镜头语法、声音和剪辑从剧本页面中独立出来。标准分镜 CSV 采用一套稳定的 13 字段规范，并通过
[`shot-list.schema.json`](schemas/shot-list.schema.json) 校验。

在生成式制作中，分镜表仍然表达导演意图。可选的
[`AI 视频模块`](modules/production/ai-video.md) 进一步加入人物、场景与风格锁定，参考来源记录，首尾帧，连续性边，模型专用适配说明，代理版与终版闸门，以及已采纳镜次记录。它不会把某个工具硬编码成“当前最强模型”，也不会承诺未经验证的工具能力。

## 质量与评测

普通产出会经过五项轻量闸门：请求格式、已锁定设定、可实现性、完整性与连续性、事实标签。Review 和最终发布会加载完整的剧本诊断器：先检查硬闸门，再针对相关的 `0–4` 分质量维度提供证据。

仓库维护检查是确定性的，且不依赖第三方包：

```text
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

模型中立的 [`评测目录`](evals/README.md) 覆盖路由、直接进入、提示词注入边界、视觉化写作、长篇状态、规范与运行行为、微短剧、纯单元剧、审阅、改编、格式例外，以及 AI 竖屏项目的规范化与生成执行包。静态持续集成通过不等于模型能力已经验证。

## 完整示例

[`examples/short-film_the-last-shift/`](examples/short-film_the-last-shift/) 是一个如实标注范围的端到端示例（vertical slice）：它先把一部 8 分钟短片规划到阶段 6，再将 `SC004` 继续制作成 Fountain 剧本页面、40 秒标准分镜表和限定范围的阶段 8 质量检查。它不会被错误地宣传成一部完整剧本。

## 仓库目录

```text
system/          入口协议、编排器、工作流程
modules/         创作技法、格式、导演、改编与调研、制作、质量检查
templates/       状态、记忆、故事、剧本、分镜、生成、质量检查模板
schemas/         标准机器可读协议
examples/        便于回归检查的完整示例产出
evals/           模型中立的行为测试用例与评分规则
scripts/ tests/  仅使用标准库的确定性维护检查
docs/            架构、兼容性、参考资料、版本与发布策略
```

设计参考与许可证注意事项记录在 [`docs/references.md`](docs/references.md)，贡献规则见
[`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 编码

标准文件统一采用不带 BOM 的 UTF-8 编码和 LF 换行。较旧的 Windows PowerShell 或 Excel 可能会错误猜测 CSV 编码；请在导入 CSV 时明确选择 UTF-8，而不是修改标准文件的编码。`.gitattributes` 与 `.editorconfig` 会防止换行符被悄悄改成 CRLF。

## 许可证

[MIT](LICENSE)
