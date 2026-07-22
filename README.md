# Filmwright · 编导智能体系统

**Vendor-neutral screenwriting, directing, continuity, and generative-production
contracts for capable LLMs.**
一套模型中立、可追踪、可恢复的「编剧 + 导演 + 连续性 + AI 视频生产」智能体协议。

Current source version: **0.2.0** · [Changelog](CHANGELOG.md) ·
[Compatibility evidence](docs/model-compatibility.md)

Filmwright turns a seed, source text, outline, or existing draft into the exact
artifact a project needs: development, treatment, beat sheet, scene map, Fountain
screenplay, continuity state, shot list, AI-video generation packet, or diagnosis.
The creative core remains Markdown + Fountain + CSV and needs no runtime.

Filmwright is **vendor-neutral by design**, not “verified on every model.” Exact
model/host results belong in the compatibility matrix; v0.2 starts with those
claims explicitly untested rather than guessed.

## What v0.2 changes · 这次升级了什么

- **Four operating modes:** Guided for co-writing, Sprint for end-to-end drafting,
  Direct for one bounded artifact, Review for diagnosis without unsolicited rewrite.
- **Direct entry:** a shot-list request enters Stage 7d; a scene review enters QA.
  Stage 0 plus eight creative/QA stages (with 7d as a direction substage) form a
  dependency graph, not a ritual.
- **One Project State:** stable IDs, locked canon, character knowledge, timeline,
  props/locations, setups, decisions, and State Deltas survive long work and
  revisions.
- **Dependency-complete memory:** dependency-validated Event Graph subrecords + per-scene
  Context Packs replace the habit of stuffing an entire history back into the model.
- **Source trust boundary:** novels, scripts, web pages, and retrieved text remain
  data—even if they contain instructions. Facts, source canon, inference, and
  invention stay distinguishable.
- **AI-video production:** asset/reference locks, first/last-frame continuity,
  model adapters, proxy/final gates, accepted takes, and multimodal QA.
- **Real maintenance:** SemVer, Changelog, manifest, canonical shot schema,
  deterministic validator, behavioral eval catalog, CI, and a corrected worked
  vertical slice.

## Outputs · 产出物

| Artifact | Portable format | Canonical template |
|---|---|---|
| Project/canon state | Markdown + YAML header | [`project-state.md`](templates/project-state.md) |
| Treatment | Markdown | [`treatment.md`](templates/treatment.md) |
| Beat sheet | Markdown | [`beat-sheet.md`](templates/beat-sheet.md) |
| Event graph / scene map | Markdown tables | [`event-graph.md`](templates/event-graph.md) / [`scene-card.md`](templates/scene-card.md) |
| Screenplay | Fountain | [`fountain.md`](templates/fountain.md) |
| Shot list | Markdown / canonical CSV | [`shot-list.md`](templates/shot-list.md) / [`shot-list.csv`](templates/shot-list.csv) |
| AI-video execution packet | Markdown/YAML blocks | [`generation-packet.md`](templates/generation-packet.md) |
| Handoff/context | Markdown | [`memory-checkpoint.md`](templates/memory-checkpoint.md) / [`context-pack.md`](templates/context-pack.md) |
| QA | evidence-based scorecard | [`quality-scorecard.md`](templates/quality-scorecard.md) |

## Quick start · 快速开始

### Repository-aware agent

Open the repository and ask for story work explicitly:

```text
用 Filmwright 把这段梗概开发成一部 8 分钟短片，用 Guided 模式。
直接把已锁定的 SC004 拆成 60 秒规范分镜 CSV。
审阅这份剧本，不要改写；给我硬闸门、证据和优先修复项。
```

`AGENTS.md` and `CLAUDE.md` both route through
[`system/entry-contract.md`](system/entry-contract.md), which distinguishes using
Filmwright from maintaining the repository. Creative work then loads
[`system/orchestrator.md`](system/orchestrator.md) and only the needed modules.

### Chat-only model

1. Paste `system/orchestrator.md`.
2. Provide the Project Card details you know and the requested mode/deliverable.
3. Paste only the modules named by the relevant task route.
4. Save the emitted Project State/State Delta yourself.

Chat-only and file-aware hosts share the contract, but their execution is not
identical: persistence, research, multimodal inspection, and parallel QA depend on
actual host capabilities.

See [`docs/quickstart.md`](docs/quickstart.md) for mode examples and resume flows.

## Operating modes · 工作模式

| Mode | Best for | Pause behavior |
|---|---|---|
| Guided 引导 | premise/character/structure choices | gates consequential decisions with `pass / revise / review` |
| Sprint 冲刺 | “直接做完”, complete draft spans | continues through reversible choices; logs assumptions |
| Direct 直达 | one scene, conversion, continuation, shot list | returns the bounded artifact + State Delta |
| Review 审阅 | diagnosis, comparison, QA | preserves the target; rewrites only when authorized |

## Pipeline · 流水线

```text
0 CONTRACT → 1 CORE ACTION → 2 SYNOPSIS → 3 CHARACTER → 4 WORLD/CANON
→ 5 STRUCTURE → 6 SCENE MAP → 7 SCREENPLAY → 7d DIRECTION → 8 QA
```

Each completed unit has `input → work → artifact → acceptance → State Delta`.
Approved upstream work is reused. Direct and Review requests enter at the earliest
stage their dependencies require.

## State and long-form continuity · 长篇状态

Project State is the canonical root. Registered Event Graph/production records are
dependency-validated normative subrecords; checkpoints, Context Packs, series-bible
tables, and micro-drama ledgers are projections—not separate canon.

Stable IDs survive revisions:

```text
CHAR-001 · LOC-001 · PROP-001 · SETUP-001 · EVT-001 · SC001 · DEC-001
SC004-SH003 (standalone shot) · EP012-SC004-SH003 (episodic shot)
```

See [`docs/id-conventions.md`](docs/id-conventions.md) for the canonical namespace,
zero-padding, episodic composition, artifact versions, and production take IDs.

Before a new scene, build a Context Pack containing only its relevant locked facts,
knowledge, entity state, causal window, source anchors, and acceptance tests. After
the scene, merge its State Delta and invalidate dependent artifacts when an
upstream decision changes.

## Formats · 支持格式

| Format | Default scale | Module |
|---|---|---|
| Concept ultrashort | 1–3 min | [`ultrashort.md`](modules/formats/ultrashort.md) |
| Narrative short | roughly 5–15 min | [`short.md`](modules/formats/short.md) |
| Feature | feature length | [`feature.md`](modules/formats/feature.md) |
| Series / episodic | multi-episode | [`series.md`](modules/formats/series.md) |
| Vertical micro-drama | platform-defined | [`vertical-microdrama.md`](modules/formats/vertical-microdrama.md) |
| Custom / hybrid | explicit scale override | closest structural module + Project Card |

Runtime labels are defaults, not unsupported gaps. Custom profiles must state which
structural/rhythm assumptions are being overridden.

## Direction and AI video · 导演与生成式生产

The direction layer separates blocking, axis/coverage, shot grammar, sound, and
editing from screenplay pages. The canonical shot CSV has one stable 13-field
schema, validated against [`shot-list.schema.json`](schemas/shot-list.schema.json).

For generative production, a shot list remains directorial intent. The optional
[`AI-video module`](modules/production/ai-video.md) adds character/location/style
locks, reference provenance, first/last frames, continuity edges, model-specific
adapter notes, proxy/final gates, and accepted-take records. It never hard-codes a
“latest best model” or promises an unverified tool capability.

## Quality and evaluation · 质量与评测

Ordinary outputs run five lite gates: requested format, locked canon,
realizability, completeness/continuity, and truth labeling. Review/final releases
load the full Script Doctor: hard gates first, then relevant `0–4` quality
dimensions with evidence.

Repository maintenance checks are deterministic and dependency-free:

```text
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

The provider-neutral [`eval catalog`](evals/README.md) covers routing, direct entry,
prompt-injection boundaries, visual writing, long-form state, schema/runtime,
micro-drama, pure anthology, review, adaptation, format exceptions, and AI-vertical
normalization/generation packets. Static CI does not count as model verification.

## Worked example · 范例

[`examples/short-film_the-last-shift/`](examples/short-film_the-last-shift/) is an
honest vertical slice: it plans an 8-minute short through Stage 6, then carries
`SC004` through Fountain pages, a 40-second canonical shot list, and scoped Stage-8
QA. It is not mislabeled as a complete screenplay.

## Repository map · 目录

```text
system/          entry contract, orchestrator, pipeline
modules/         craft, format, direction, adaptation/research, production, QA
templates/       state, memory, story, screenplay, shot, generation, QA artifacts
schemas/         canonical machine contracts
examples/        regression-friendly worked artifacts
evals/           provider-neutral behavioral cases and rubric
scripts/ tests/  standard-library deterministic maintenance checks
docs/            architecture, compatibility, references, version/release policy
```

Design references and license cautions are documented in
[`docs/references.md`](docs/references.md). Contribution rules are in
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Encoding note · 编码

Canonical files are UTF-8 without BOM and LF. Older Windows PowerShell/Excel may
guess CSV encoding incorrectly; import CSV explicitly as UTF-8 rather than changing
the canonical file. `.gitattributes` and `.editorconfig` prevent silent CRLF drift.

## License

[MIT](LICENSE).
