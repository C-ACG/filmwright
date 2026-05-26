# Architecture · 设计说明

Why Filmwright is shaped the way it is.

---

## The core idea: two crafts, cleanly split

A film set separates the writer from the director for a reason — they answer
different questions:

- **Writing** answers *what happens and what it means*: structure, character,
  subtext, the words on the page.
- **Direction** answers *how the camera, the staging, and the cut make the audience
  feel it*: shot grammar, blocking, coverage, the breakdown.

Most prompt-based "AI screenwriters" collapse these into one undifferentiated blob,
which is why their output reads like a story summary rather than something a crew
can shoot. Filmwright keeps them separate (`modules/` vs `modules/direction/`) and
joins them at stage 7d, where a written scene becomes a shot list.

---

## Progressive loading

The orchestrator (`system/orchestrator.md`) is small and always loaded. Everything
else loads on demand based on the routed format and the current pipeline stage. A
concept-ultrashort job never loads the series module; a writing job that hasn't
reached the breakdown never loads the direction modules. This keeps the working
context lean on any model and makes each module independently legible and editable.

```
orchestrator (always)
   ├── 00-core-craft        (every format)
   ├── 01-development        (stages 1–4)
   ├── 02-structure          (stage 5, cinematic formats)
   ├── formats/<one>         (the routed format)
   ├── direction/<as needed> (stage 7d)
   └── qa/script-doctor      (stage 8 + silent self-check)
```

---

## Format-agnostic core, format-specific edges

The craft that does not change — dramatic action, Want/Need, show-don't-tell,
dual-track pacing, runtime estimation, memory checkpoints, cross-format borrowing —
lives once in `00-core-craft.md`. Each format module is thin: it states the format's
traits, scales each pipeline stage up or down, and adds only what is genuinely
specific (e.g. the micro-drama emotion engine, the series two-layer structure).

This is what lets the same system span 90 seconds to a full season without
duplicating method, and what makes "not limited to short-drama" structurally true
rather than a slogan: micro-drama is **one format module among five**, not the
center of gravity.

---

## Portability

Filmwright assumes nothing beyond a capable LLM that reads Markdown and converses.
No code, no runtime, no API. Deliverables are **Fountain** (screenplay), **CSV /
Markdown tables** (shot lists, ledgers), and prose (treatments) — all
version-control-friendly and importable by standard industry tools. The two agent
entry files (`CLAUDE.md`, `AGENTS.md`) carry an identical contract so the system
behaves the same on Claude, Codex, Cursor, or a bare chat window.

---

## Lineage

Filmwright consolidates and re-engineers three earlier prompt systems into one
agent-native, model-agnostic package:

- a professional multi-format screenwriting engine (format routing; Want/Need,
  Ghost/Lie/Flaw; Save the Cat / Story Circle / McKee; dual-track pacing; foreshadow
  audits; memory checkpoints) — now the craft core and the four cinematic formats;
- two iterations of a vertical-microdrama engine (emotion engine, payoff arsenal,
  three locks, four ledgers, compliance rail, AI-production adaptation) — now folded
  in as the micro-drama format module.

The new contribution is the **direction layer** — visual language, blocking,
coverage, transitions, editing rhythm, and a scene→shot-list procedure — which the
source systems deliberately left to a human director, and which makes the output
shootable rather than merely written.
