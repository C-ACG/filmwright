# Architecture · 设计说明

Filmwright v0.2 is a portable creative core surrounded by explicit state, artifact,
production, and evaluation contracts.

```text
Agent Entry
  ├─ Repository Maintenance → version / schema / validator / eval / release
  └─ Creative Runtime
       Project Card + capability profile
                 ↓
       Orchestrator state machine
                 ↓
       active craft + format + task modules
                 ↓
       artifact + acceptance + State Delta
                 ↓
       canonical Project State root
                 ↓
       dependency-validated Event Graph / production subrecords
                 ↓
       Context Pack for the next unit
                 ↓
       QA hard gates + evidence scorecard
```

## 1. Entry separation · 入口分离

Opening the repository no longer automatically turns a coding/maintenance agent
into a screenwriter. `system/entry-contract.md` chooses:

- **Creative Runtime** for story artifacts;
- **Repository Maintenance** for prompt/schema/docs/test/version work.

`AGENTS.md` and `CLAUDE.md` are identical thin adapters. The canonical behavior
lives once, preventing host-specific instruction drift.

## 2. Small orchestrator, progressive modules · 小总控与按需模块

The orchestrator owns priorities, trust boundaries, modes, routing, state, and
output contracts. It does not repeat detailed craft. Runtime loading is:

```text
00 core craft (always)
├─ 01 development            stages 1–4
├─ 02 structure              stages 5–6
├─ 03 adaptation/research    source or factual tasks
├─ formats/<active>          scale-specific behavior
├─ direction/*               Stage 7d
├─ production/ai-video       optional generative execution
└─ qa/script-doctor          Review / Stage 8 / final high-stakes output
```

Five lite QA gates remain visible in the orchestrator. The full Script Doctor does
not have to be loaded for every intermediate chat turn.

## 3. Modes and direct entry · 模式与直达

Guided, Sprint, Direct, and Review share the same dependencies but differ in pause
semantics. The pipeline is a state machine:

- reuse approved upstream artifacts;
- enter at the earliest necessary stage;
- skip irrelevant ceremony, not load-bearing dependencies;
- every unit ends with observable acceptance and State Delta.

This preserves human authorship without making a 60-second shot-list request replay
premise development.

## 4. One truth source · 单一真相源

`templates/project-state.md` is canonical for locked decisions, source authority,
entity state, knowledge, timeline, scene index, threads/setups, assumptions, and
next action. Stable IDs survive wording changes.

Detailed records and projections have different authority:

- Event Graph and Production State/generation packets = normative subrecords,
  registered with dependency IDs/revisions and a last-validated root revision;
- checkpoint = portable handoff projection;
- series bible = planning/continuity view;
- micro-drama ledgers = task-focused views;
- Context Pack = disposable subset for one next unit;
- run manifest = reproducibility/provenance record.

On conflict, current root locks/decisions win over a registered subrecord; a current
subrecord wins over a projection. An unrelated root revision does not expire a
subrecord, but a changed dependency makes it stale. Stale, unregistered, or
dependency-mismatched subrecords cannot update canon or feed downstream work.

Changing an upstream event or lock requires a State Delta and review of dependent
scene cards/artifacts. A new draft does not silently become canon.

## 5. Event graph and context compression · 事件图与上下文压缩

Beat sheets describe rhythm; Event Graph nodes describe preconditions, action,
outcome, knowledge changes, state delta, and causal/reveal/payoff edges. Before a
scene, the system assembles only its dependency-complete context.

This is more reliable than assuming a larger context window will remember every
prop, secret, relationship, and deadline with equal priority.

## 6. Writing, direction, production · 编、导、制

- **Writing** owns event, meaning, character choice, scene text, and subtext.
- **Direction** owns blocking, axis/coverage, shot grammar, sound, transition, and
  edit rhythm.
- **Production** converts approved shot intent into executable constraints.

Live-action shot lists remain lean. Generative production gets a separate packet
for asset/reference locks, endpoints, model adapters, takes, provenance, and
acceptance tests. This prevents temporary model syntax from contaminating canon.

## 7. Hard gates vs techniques · 硬闸门与技法分层

Earlier versions overgeneralized useful techniques. v0.2 separates:

- **Hard gates:** safety/rights, instruction boundary, brief, locked canon, source
  fidelity, causality where the chosen form requires it, realizability, completeness.
- **Strong defaults:** visual action, distinct voices, turns, runtime/continuity.
- **Optional techniques:** Want/Need arc, dialogue, VO, dual-track mismatch,
  conventional climax, camera-free screenplay page.

QA marks irrelevant dimensions `N/A`. A character-free, zero-dialogue ultrashort is
not broken merely because a feature-drama heuristic does not apply.

## 8. Portability and capability adapters · 可移植与能力适配

The core remains Markdown/Fountain/CSV and works without a code runtime. Hosts may
add file persistence, web research, multimodal inspection, subagents, or an
optional durable runner. The orchestrator uses only capabilities that actually
exist and never claims a tool action that did not happen.

Chat-only behavior is portable but manual. File/agentic/multimodal behavior is more
capable, not identical.

## 9. Machine contracts and evaluation · 机器契约与评测

`filmwright.manifest.json` versions module paths/dependencies. JSON Schema defines
the canonical shot row. The standard-library validator checks encoding/LF, local
links, version/manifest consistency, adapter parity, schemas/CSV IDs/enums,
Fountain/example regressions, runtime closure, and eval catalog shape.

Behavioral evals assert observable constraints and use evidence rubrics rather than
full creative golden snapshots. Compatibility is published only for exact
model/host/suite runs.

## 10. Design lineage · 设计来源

The original strengths remain: separate writing/direction crafts, progressive
loading, format-specific edges, Fountain/CSV portability, human gates, and memory
checkpoints. v0.2 adds state-machine rigor, provenance, production continuity, and
testable public contracts. External design references and license cautions are in
[`references.md`](references.md).
