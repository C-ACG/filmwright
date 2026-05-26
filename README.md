# Filmwright · 编导智能体系统

**A screenwriter + director agent system for any LLM.**
**一套适配任意大模型的「编导 + 导演」智能体系统。**

Filmwright turns a creative seed — a logline, a premise, a novel excerpt, a theme,
a character, a space, or a loose pile of ideas — into **a script a director can
shoot and a shot breakdown a crew can execute**, in whatever format and runtime the
project calls for. It runs on Claude, Codex, Cursor, or any capable model, with no
tools or runtime required beyond Markdown and a conversation.

Filmwright 把任何创作种子推过一条纪律化的八步流水线，最终产出**导演拿到即可拍、剧组
拿到即可执行**的剧本与分镜，不限格式与时长。纯 Markdown + Fountain + CSV，无需任何
工具或运行时——任何能读 Markdown、能对话的模型都可驱动。

---

## Why it exists · 设计动机

Most "AI screenwriting prompts" are a single wall of text that does one thing
(usually vertical micro-drama) for one model. Filmwright separates concerns the way
a real production does:

- **编 + 写 (develop & write)** decides *what happens and what it means* — structure,
  character, subtext, scene text.
- **导 (direct)** decides *how the camera, the staging, and the cut make the audience
  feel it* — visual language, blocking, coverage, shot breakdown.

The two crafts are split into composable modules loaded on demand, so the same
system writes a 90-second concept film, a 10-minute short, a feature, a multi-season
series, **or** a vertical micro-drama — and then breaks any of them down into a shot
list. It is model-agnostic by design.

把"编/写"与"导"拆成可组合、按需加载的模块，因此同一套系统既能写概念片、短片、长片、
剧集，**也能**写竖屏短剧，并把其中任何一种拆成分镜表。

---

## What it produces · 产出物

| Deliverable | Format | Template |
|---|---|---|
| Screenplay 剧本 | **Fountain** (plain text → industry layout) | `templates/fountain.md` |
| Treatment 故事大纲 | one-page prose | `templates/treatment.md` |
| Beat sheet 节拍表 | structure + runtime + pacing | `templates/beat-sheet.md` |
| Shot list 分镜表 | director's breakdown, also CSV | `templates/shot-list.md` / `.csv` |
| Memory checkpoint 记忆检查点 | continuity snapshot | `templates/memory-checkpoint.md` |
| Series bible 剧集圣经 | season plan + tracking | `templates/series-bible.md` |

All formats are version-control-friendly and tool-agnostic.

---

## Quick start · 快速开始

### Claude / Claude Code
The repo ships a `CLAUDE.md`. Open the project and ask, e.g.,
> "用 Filmwright 帮我把这篇小说改成 12 集短剧" · "Develop a 10-minute short from this premise."

Claude loads `system/orchestrator.md`, routes by format, and pulls modules as the
pipeline advances.

### Codex / Cursor / Windsurf / other agents
The repo ships an `AGENTS.md` with the same contract. Point your agent at it.

### Any chat model (no file access)
1. Paste `system/orchestrator.md` as the system prompt.
2. Describe your project. The model asks one routing question if needed.
3. When the pipeline reaches a stage, paste the module(s) it names.

详见 [`docs/quickstart.md`](docs/quickstart.md)。

---

## The pipeline · 八步流水线

```
DEVELOP ── 1 Break-in & core action      破题与核心动作
       └── 2 Synopsis draft               梗概草稿
       └── 3 Character & arc              人物深度与弧光
       └── 4 Backstory & world            前史与世界观
WRITE  ── 5 Structure outline             结构大纲（含开场钩子）
       └── 6 Scene breakdown              场景拆解（时长 + 双轨节奏）
       └── 7 Scene writing                场景写作（视觉化 + 潜台词）
DIRECT ── 7d Shot breakdown               分镜 / 运镜 / 调度  ← 导演层
QA     ── 8 Script doctor                 剧本医生（诊断 + 抛光）
```

Each stage gates on your `pass / revise / review`. The system builds the whole world
first (stages 1–4), then cuts into it at the point of maximum tension (5–8) — *a film
is a cross-section of life*.

---

## Formats · 支持格式

| Format | Runtime | Module |
|---|---|---|
| Concept ultrashort 概念超短片 | 1–3 min | `modules/formats/ultrashort.md` |
| Short film 叙事短片 | 5–10 min | `modules/formats/short.md` |
| Feature 长片 | 75–120 min | `modules/formats/feature.md` |
| Series 剧集 | multi-episode | `modules/formats/series.md` |
| Vertical micro-drama 竖屏短剧 | platform | `modules/formats/vertical-microdrama.md` |

The **direction layer** (`modules/direction/`) is format-independent and applies to
all of them.

---

## Repository layout · 目录结构

```
filmwright/
├── CLAUDE.md · AGENTS.md          # agent entry points
├── README.md · LICENSE
├── system/
│   ├── orchestrator.md            # the canonical system prompt — load first
│   └── pipeline.md                # stage-by-stage contract
├── modules/
│   ├── 00-core-craft.md           # universal craft (loaded by every format)
│   ├── 01-development.md          # ideation · premise · character · world
│   ├── 02-structure.md            # Save the Cat / Story Circle / McKee / inner-beat
│   ├── formats/                   # ultrashort · short · feature · series · micro-drama
│   ├── direction/                 # visual-language · blocking-and-coverage · shot-breakdown
│   └── qa/                        # script-doctor (self-check + diagnosis)
├── templates/                     # fountain · treatment · beat-sheet · shot-list(.md/.csv)
│                                  #  · memory-checkpoint · series-bible
├── examples/                      # a worked short film, end to end
└── docs/                          # quickstart · design notes
```

See [`docs/architecture.md`](docs/architecture.md) for the design rationale and
[`examples/`](examples/) for a complete worked short film.

---

## Design principles · 设计原则

1. **Two crafts, cleanly split.** Writing answers *what & why*; direction answers
   *how it's seen*. A scene isn't done until both have spoken.
2. **Composable, progressively loaded.** Load only the modules a stage needs.
3. **Format-agnostic core, format-specific edges.** One craft spine; thin format
   modules.
4. **Portable, tool-free, version-controllable.** Markdown / Fountain / CSV; runs on
   any model.
5. **Shootable by default.** Every line on the page can be photographed or recorded.

---

## License · 许可

[MIT](LICENSE).
