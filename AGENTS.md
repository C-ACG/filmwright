# AGENTS.md

Entry point for **Codex**, **OpenAI agents**, **Cursor**, **Windsurf**, and any
agentic coding/writing tool working in this repository. (Claude users: see
`CLAUDE.md` — identical contract.)

## What this is
Filmwright — a vendor-neutral screenwriter + director (编导 + 导演) agent system.
It takes any creative seed and runs it through an eight-stage pipeline to a
shootable script plus a director's shot breakdown, in any format and runtime.
Pure Markdown + Fountain + CSV; **no tools or runtime required** beyond a capable
LLM that reads Markdown and holds a conversation.

## How to operate
1. **Load `system/orchestrator.md` as the system prompt.** It defines role, hard
   rules, routing, the pipeline, state management, and output discipline.
2. **Progressive module loading** — load only what the current stage needs:
   - core `modules/00-core-craft.md` · dev `modules/01-development.md` ·
     structure `modules/02-structure.md`
   - format `modules/formats/{ultrashort,short,feature,series,vertical-microdrama}.md`
   - direction (stage 7d) `modules/direction/*.md` · QA `modules/qa/script-doctor.md`
3. **Stage gating** — complete a stage, then wait for the user's `pass / revise /
   review`. Do not emit all stages at once (micro-drama batches; see its module).
4. **Silent self-check** before every output (`modules/qa/script-doctor.md` §1).
5. **Templates** in `templates/` shape every deliverable.

## If the host can't read files
Paste `system/orchestrator.md` as the system prompt, then paste the relevant
module(s) when the pipeline reaches that stage. Behavior is identical to file-based
loading.

## Hard rules (never relax)
- No interior narration / parenthetical mind-reading / setting-explaining dialogue /
  anything the camera can't see (orchestrator §1.1).
- Safety, compliance, and rule-conflict priority: orchestrator §1.3.

## Conventions
- Match the user's working language; default to Chinese prose + English keys.
- Outputs: Markdown / Fountain / CSV — version-control-friendly by design.
