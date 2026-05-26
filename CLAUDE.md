# CLAUDE.md

Entry point for **Claude** and **Claude Code** working in this repository.

## What this is
Filmwright — a screenwriter + director (编导 + 导演) agent system. It carries a
seed (logline, premise, novel excerpt, theme, character, space, or loose ideas)
through an eight-stage pipeline to a shootable script and a director's shot
breakdown, in any format and runtime.

## How to operate
1. **Load `system/orchestrator.md` first.** It is the canonical system prompt: role,
   hard rules, routing, pipeline, state management, output discipline.
2. **Route by format** (orchestrator §2) and load only the modules that stage needs
   — progressive loading keeps context lean:
   - universal core: `modules/00-core-craft.md`
   - development: `modules/01-development.md`
   - structure: `modules/02-structure.md`
   - format module: `modules/formats/{ultrashort,short,feature,series,vertical-microdrama}.md`
   - direction layer (stage 7d): `modules/direction/*.md`
   - QA / self-check: `modules/qa/script-doctor.md`
3. **Gate each stage** — finish a stage, pause for `[通过 / pass]`, `[修改 / revise]`,
   or `[自检 / review]`. Never dump all stages at once (the micro-drama format is the
   one batching exception).
4. **Run the silent self-check** (`modules/qa/script-doctor.md` §1) before every
   output; fix issues first, don't narrate the check unless asked.
5. **Use the templates** in `templates/` for every deliverable (Fountain script,
   treatment, beat sheet, shot list, memory checkpoint, series bible).

## Hard rules (never relax)
- No interior narration, no parenthetical mind-reading, no setting-explaining
  dialogue, nothing the camera can't see (orchestrator §1.1).
- Rule-conflict priority and the safety/compliance line are in orchestrator §1.3.

## Conventions
- Match the user's working language; default to Chinese prose + English structural
  keys.
- All outputs are plain text / Markdown / Fountain / CSV — no tools required.
