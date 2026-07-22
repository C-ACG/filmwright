**English** · [简体中文](README.zh-CN.md)

# Filmwright — Screenwriting & Directing Agent System

**Vendor-neutral contracts for screenwriting, directing, continuity, and
generative production with capable LLMs.**

Filmwright turns a seed, source text, outline, or existing draft into the exact
artifact a project needs: development notes, a treatment, beat sheet, scene map,
Fountain screenplay, continuity state, shot list, AI-video generation packet, or
diagnosis. The creative core remains portable Markdown + Fountain + CSV and needs
no dedicated runtime.

Current source version: **0.2.0** · [Changelog](CHANGELOG.md) ·
[Compatibility evidence](docs/model-compatibility.md)

Filmwright is **vendor-neutral by design**, not “verified on every model.” Exact
model and host results belong in the compatibility matrix; v0.2 starts with those
claims explicitly untested rather than guessed.

## What is new in v0.2

- **Four operating modes:** Guided for co-writing, Sprint for end-to-end drafting,
  Direct for one bounded artifact, and Review for diagnosis without unsolicited
  rewriting.
- **Direct entry:** a shot-list request enters Stage 7d; a scene review enters QA.
  Stage 0 plus eight creative and QA stages (with 7d as a direction substage) form
  a dependency graph, not a ritual.
- **One Project State:** stable IDs, locked canon, character knowledge, timeline,
  props and locations, setups, decisions, and State Deltas survive long projects
  and revisions.
- **Dependency-complete memory:** dependency-validated Event Graph subrecords and
  per-scene Context Packs replace the habit of stuffing an entire history back
  into the model.
- **Source trust boundary:** novels, scripts, web pages, and retrieved text remain
  data—even if they contain instructions. Facts, source canon, inference, and
  invention stay distinguishable.
- **AI-video production:** asset and reference locks, first/last-frame continuity,
  model adapters, proxy/final gates, accepted takes, and multimodal QA.
- **Real maintenance:** SemVer, a changelog, manifest, canonical shot schema,
  deterministic validator, behavioral eval catalog, CI, and a corrected worked
  vertical slice.

## Outputs

| Artifact | Portable format | Canonical template |
|---|---|---|
| Project and canon state | Markdown + YAML header | [`project-state.md`](templates/project-state.md) |
| Treatment | Markdown | [`treatment.md`](templates/treatment.md) |
| Beat sheet | Markdown | [`beat-sheet.md`](templates/beat-sheet.md) |
| Event graph and scene map | Markdown tables | [`event-graph.md`](templates/event-graph.md) / [`scene-card.md`](templates/scene-card.md) |
| Screenplay | Fountain | [`fountain.md`](templates/fountain.md) |
| Shot list | Markdown / canonical CSV | [`shot-list.md`](templates/shot-list.md) / [`shot-list.csv`](templates/shot-list.csv) |
| AI-video execution packet | Markdown / YAML blocks | [`generation-packet.md`](templates/generation-packet.md) |
| Handoff and context | Markdown | [`memory-checkpoint.md`](templates/memory-checkpoint.md) / [`context-pack.md`](templates/context-pack.md) |
| QA | Evidence-based scorecard | [`quality-scorecard.md`](templates/quality-scorecard.md) |

## Quick start

### Repository-aware agent

Open the repository and ask for story work explicitly:

```text
Use Filmwright to develop this synopsis into an 8-minute short film in Guided mode.
Turn the locked SC004 directly into a canonical 60-second shot-list CSV.
Review this screenplay without rewriting it; return hard gates, evidence, and prioritized fixes.
```

`AGENTS.md` and `CLAUDE.md` both route through
[`system/entry-contract.md`](system/entry-contract.md), which distinguishes using
Filmwright from maintaining the repository. Creative work then loads
[`system/orchestrator.md`](system/orchestrator.md) and only the modules needed for
the request.

### Chat-only model

1. Paste `system/orchestrator.md`.
2. Provide the Project Card details you know and the requested mode and deliverable.
3. Paste only the modules named by the relevant task route.
4. Save the emitted Project State or State Delta yourself.

Chat-only and file-aware hosts share the contract, but their execution is not
identical: persistence, research, multimodal inspection, and parallel QA depend on
actual host capabilities.

See [`docs/quickstart.md`](docs/quickstart.md) for mode examples and resume flows.

## Operating modes

| Mode | Best for | Pause behavior |
|---|---|---|
| Guided | Premise, character, and structure choices | Gates consequential decisions with `pass / revise / review` |
| Sprint | Complete drafts and “take it to the end” requests | Continues through reversible choices and logs assumptions |
| Direct | One scene, conversion, continuation, or shot list | Returns the bounded artifact plus a State Delta |
| Review | Diagnosis, comparison, and QA | Preserves the target and rewrites only when authorized |

## Pipeline

```text
0 CONTRACT → 1 CORE ACTION → 2 SYNOPSIS → 3 CHARACTER → 4 WORLD/CANON
→ 5 STRUCTURE → 6 SCENE MAP → 7 SCREENPLAY → 7d DIRECTION → 8 QA
```

Each completed unit has `input → work → artifact → acceptance → State Delta`.
Approved upstream work is reused. Direct and Review requests enter at the earliest
stage their dependencies require.

## State and long-form continuity

Project State is the canonical root. Registered Event Graph and production records
are dependency-validated normative subrecords; checkpoints, Context Packs,
series-bible tables, and micro-drama ledgers are projections—not separate canon.

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

## Supported formats

| Format | Default scale | Module |
|---|---|---|
| Concept ultrashort | 1–3 minutes | [`ultrashort.md`](modules/formats/ultrashort.md) |
| Narrative short | Roughly 5–15 minutes | [`short.md`](modules/formats/short.md) |
| Feature | Feature length | [`feature.md`](modules/formats/feature.md) |
| Series / episodic | Multiple episodes | [`series.md`](modules/formats/series.md) |
| Vertical micro-drama | Platform-defined | [`vertical-microdrama.md`](modules/formats/vertical-microdrama.md) |
| Custom / hybrid | Explicit scale override | Closest structural module plus Project Card |

Runtime labels are defaults, not unsupported gaps. Custom profiles must state which
structural or rhythm assumptions are being overridden.

## Direction and AI video

The direction layer separates blocking, axis and coverage, shot grammar, sound,
and editing from screenplay pages. The canonical shot CSV has one stable 13-field
schema, validated against [`shot-list.schema.json`](schemas/shot-list.schema.json).

For generative production, a shot list remains directorial intent. The optional
[`AI-video module`](modules/production/ai-video.md) adds character, location, and
style locks; reference provenance; first and last frames; continuity edges;
model-specific adapter notes; proxy and final gates; and accepted-take records. It
never hard-codes a “latest best model” or promises an unverified tool capability.

## Quality and evaluation

Ordinary outputs run five lite gates: requested format, locked canon,
realizability, completeness and continuity, and truth labeling. Review and final
releases load the full Script Doctor: hard gates first, then relevant `0–4` quality
dimensions with evidence.

Repository maintenance checks are deterministic and dependency-free:

```text
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

The provider-neutral [`eval catalog`](evals/README.md) covers routing, direct
entry, prompt-injection boundaries, visual writing, long-form state, schema and
runtime behavior, micro-drama, pure anthology, review, adaptation, format
exceptions, and AI-vertical normalization and generation packets. Static CI does
not count as model verification.

## Worked example

[`examples/short-film_the-last-shift/`](examples/short-film_the-last-shift/) is an
honest vertical slice: it plans an 8-minute short through Stage 6, then carries
`SC004` through Fountain pages, a 40-second canonical shot list, and scoped Stage 8
QA. It is not mislabeled as a complete screenplay.

## Repository map

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

## Encoding

Canonical files are UTF-8 without BOM and use LF line endings. Older Windows
PowerShell and Excel versions may guess CSV encoding incorrectly; import CSV
explicitly as UTF-8 rather than changing the canonical file. `.gitattributes` and
`.editorconfig` prevent silent CRLF drift.

## License

[MIT](LICENSE)
