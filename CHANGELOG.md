# Changelog

All notable changes to Filmwright are documented here. The project follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Split the mixed-language README into dedicated English and Simplified Chinese
  editions with a top-level language switch.

## [0.2.0] - 2026-07-21

### Added

- Guided, Sprint, Direct, and Review operating modes with direct-entry routing.
- Canonical Project State, State Delta, stable entity IDs, Event Graph, Scene Card,
  Context Pack, and evidence-based Quality Scorecard.
- Unified ID registry for story, artifact, episode/scene/shot, reference, and take
  namespaces.
- Adaptation/research trust boundary with source registry, fidelity lock, and
  provenance tracking.
- Model-neutral AI-video production layer with asset locks, first/last-frame state,
  continuity graph, take tracking, and multimodal acceptance tests.
- Canonical shot-list JSON Schema and unified CSV/Markdown fields.
- Repository validator, behavioral eval catalog, quality CI, version/release docs,
  model compatibility policy, and research references.
- A complete Stage-6 scene map and scoped Stage-8 QA for the worked vertical slice.

### Changed

- Agent entry now distinguishes Creative Runtime from Repository Maintenance.
- Checkpoints, series bibles, and micro-drama ledgers are views of one Project
  State instead of competing truth sources.
- QA now separates always-on lite gates, format-aware hard gates, and scored
  heuristics; subjective devices and zero-dialogue formats are no longer falsely
  rejected by universal rules.
- “Any LLM” compatibility claim is replaced by vendor-neutral design plus an
  evidence-based compatibility matrix.
- Shot IDs use `SC004-SH003` or `EP012-SC004-SH003`; canonical columns use
  `scene_id`, `lens_focus`, `duration_s`, and `transition_out`.

### Fixed

- Inconsistent pass/revise/review gate semantics across stages.
- Shot schema drift between module, Markdown template, and CSV.
- Worked-example age, timeline, handover, knowledge-state, door physics, Fountain,
  light/sound transition, and runtime contradictions.
- Worked-example script/shot order, explicit identity reveal, Project State/ten
  Scene Cards, prop lifecycle, threshold crossing, camera axis, and QA gate evidence.
- Format precedence for character-free shorts, no-season-arc anthologies, and one
  canonical AI-generated vertical-shot handoff.
- Misleading “complete film” wording for an example that is intentionally a
  vertical slice.
- Fountain guidance for non-Roman character cues and forced scene headings.

### Migration

- Load `system/entry-contract.md` before choosing creative or maintenance behavior.
- Convert long projects to `templates/project-state.md`; treat older checkpoints as
  import sources, not canonical state.
- Rename shot columns/IDs to the v0.2 schema before validation.

## [0.1.0] - 2026-05-27

### Added

- Initial vendor-neutral Markdown screenwriter/director system, five format
  modules, direction layer, templates, and partial worked example.

[Unreleased]: https://github.com/C-ACG/filmwright/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/C-ACG/filmwright/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/C-ACG/filmwright/commit/d5a8429a2a72b1b691adbf93ff09f3ed6430f486
