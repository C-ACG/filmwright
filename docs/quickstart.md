# Quickstart · 快速开始

Three ways to run Filmwright, depending on your environment.

---

## 1. Claude / Claude Code

The repository ships a `CLAUDE.md` that points the model here. Open the repo as a
project (Claude Code: `cd` into it; Claude.ai: add it as a project) and just ask:

```
用 Filmwright 把这段梗概开发成一部 10 分钟短片。
Develop this premise into a 10-minute short film using Filmwright.
把上面写好的第 4 场拆成分镜表。
Break scene 4 down into a shot list.
```

Claude loads `system/orchestrator.md`, asks one routing question if the format is
unclear, then advances stage by stage, pausing for your `pass / revise / review`.

---

## 2. Codex / Cursor / Windsurf / other agents

The repository ships an `AGENTS.md` with the same contract. Point your tool's
system/instructions at the repo root; it will read `AGENTS.md` → `orchestrator.md`
→ modules on demand.

---

## 3. Any chat model (no file access)

1. **Paste** `system/orchestrator.md` into the system prompt (or the first message).
2. **Describe** your project — seed, format, runtime, any constraints. If you don't
   name a format, the model asks once.
3. **Paste modules on demand.** When the model says it needs, e.g.,
   `modules/formats/short.md` or `modules/direction/shot-breakdown.md`, paste that
   file's contents. Behavior is identical to file-based loading.

A minimal first message:

```
[paste system/orchestrator.md]

种子：一个上夜班的便利店店员，发现常来的流浪老人其实是失联多年的父亲。
格式：10 分钟叙事短片。语言：中文。
```

---

## What to expect at each gate · 每一步的闸门

After every stage the model pauses and offers three moves:

- **`通过 / pass`** — accept and continue to the next stage.
- **`修改 / revise`** — give notes; the model reworks the current stage.
- **`自检 / review`** — the model runs the explicit self-check (`modules/qa/
  script-doctor.md`) and reports failures and waivers.

The micro-drama format is the exception — it batches output into three larger
deliverables instead of gating every stage (see `modules/formats/vertical-microdrama.md`).

---

## Resuming a long project · 续写

For features and series, the model emits **memory checkpoints**
(`templates/memory-checkpoint.md`). Save them. To resume in a new session, paste the
latest checkpoint back; the model rebuilds context and continues.

---

## A complete example · 完整范例

See [`examples/short-film_the-last-shift/`](../examples/short-film_the-last-shift/)
for a 10-minute short carried from premise through treatment, beat sheet, a Fountain
scene, and that scene's shot list.
