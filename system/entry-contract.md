# Agent Entry Contract · 智能体入口契约

> Single entry contract shared by Codex, Claude, Cursor, Windsurf, and other
> repository-aware agents.

## Route A — Creative Runtime · 使用 Filmwright 创作

Use when the user asks to create, adapt, continue, direct, convert, or review a
story artifact **with Filmwright**.

1. Load `system/orchestrator.md`.
2. Infer Guided / Sprint / Direct / Review mode from the request.
3. Load only the active craft/format/production modules.
4. Use templates for artifacts and maintain project state for long work.
5. Run lite QA on ordinary outputs; load full QA for Review, Stage 8, and final or
   high-stakes deliverables.

## Route B — Repository Maintenance · 维护 Filmwright 仓库

Use when the user asks to change this repository, its prompts, schemas, examples,
tests, documentation, version, CI, or release process.

1. Do **not** adopt the screenwriter persona or run the creative pipeline.
2. Read `CONTRIBUTING.md`, the files in scope, and the canonical contracts they
   reference.
3. Treat prompt paths, modes, stages, schemas, template fields, and default routing
   as public interfaces.
4. Preserve UTF-8/LF, local user changes, and vendor neutrality.
5. Add/update deterministic checks and behavioral eval cases for contract changes.
6. Run `python scripts/validate_repo.py` before handoff.
7. Do not claim a model is compatible until the published eval suite has been run
   and recorded in `docs/model-compatibility.md`.

## Ambiguous requests · 模糊请求

If the user says only “look at this project” or “improve Filmwright,” inspect the
repository in Maintenance mode. Enter Creative Runtime only when the requested
artifact is itself story work.
