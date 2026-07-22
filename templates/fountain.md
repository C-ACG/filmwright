# Template · Fountain Screenplay · 标准剧本（Fountain 格式）

> The default portable screenplay format. **Fountain** is a plain-text markup that
> any tool (Highland, Slugline, Fade In, WriterDuet, Final Draft import) renders to
> industry-standard layout, and that diffs cleanly in Git. Write screenplay text in
> Fountain unless the project's platform requires its own format.
> 默认可移植剧本格式。Fountain 是纯文本标记，任何工具都能渲染为行业标准排版，且可在 Git 中干净比对。

---

## Why Fountain
- **Plain text** — version-controllable, tool-agnostic, future-proof.
- **Industry layout on render** — 1 page ≈ 1 minute holds.
- **Round-trips** to Final Draft `.fdx` and PDF via free tools.

## Syntax cheat-sheet · 语法速查

```fountain
Title: The Last Shift
Credit: written by
Author: <name or pen-name>
Draft date: <YYYY-MM-DD>
Contact: <repo or email>

INT. CONVENIENCE STORE - NIGHT

Scene Heading (slugline) is an uppercase line starting with INT./EXT./EST.
Action is plain paragraphs — only what the camera sees and the mic hears.

CHARACTER NAME
A character cue is an uppercase line. Dialogue follows on the next line(s).

@美玲
Prefix a non-Roman character cue with `@` so Fountain parsers recognize it.
The `@` is not printed in the rendered screenplay.

CHARACTER NAME
(parenthetical — sparing; only when it changes the line's meaning)
The dialogue itself.

CHARACTER NAME (O.S.)
Off-screen. (V.O.) for voice-over. (CONT'D) handled by tools.

A line ending in TO: is a transition >  e.g.   CUT TO:
Force a transition by prefixing >   > SMASH CUT TO:
Force a scene heading with a leading .   .ROOFTOP - MOMENTS LATER
For a fully Chinese slugline, force it:   .内景 便利店 - 夜
Center text with > <   > THE END <
```

## Conventions for this system · 本系统约定

- **Action is shootable.** No accidental interior narration or “(he secretly...)”.
  Intentional VO/subjective devices are allowed when the format chooses them and
  they have an audiovisual function.
- **First appearance** of a character gets a one-to-two-line physical/identity
  sketch in the action.
- **Sparing parentheticals.** Only when tone/gesture changes meaning; never to
  explain the inner life.
- **Transitions are thoughts** — use them where they make a point, not as filler
  (`direction/blocking-and-coverage.md` §4).
- **Camera/coverage normally stays out of the script.** Shot sizes, angles, and movement
  live in the **shot list** (`shot-list.md`), produced at stage 7d — the director's
  layer, not the writer's page. Concept ultrashorts, micro-drama, and an explicitly
  requested AV script may integrate essential camera/form instructions because the
  device itself is content.

## Worked excerpt · 范例片段

```fountain
INT. CONVENIENCE STORE - NIGHT

Fluorescent hum. Rain sheets the glass. MEILING (50s, store
apron over a winter coat, hands chapped) restocks a shelf
that is already full.

The door chimes. She doesn't look up.

MEILING
We close in ten minutes.

A YOUNG MAN stands dripping in the doorway. He doesn't move.
She finally looks. The can in her hand stops halfway to the shelf.

MEILING (CONT'D)
...Kai?

KAI
(not stepping in)
You changed the sign.

She sets the can down. Carefully, like it might break.

CUT TO:
```

Chinese cue/slugline example:

```fountain
.内景 便利店 - 夜

@美玲
还有十分钟。

@凯
我不进去。
```

## Export · 导出
- `.fountain` / `.txt` → Highland 2, Slugline, Fade In, WriterDuet (all import).
- → PDF / `.fdx` via the above, or the `afterwriting` CLI (`npm i -g afterwriting`).
- For platform-specific micro-drama formats, see `vertical-microdrama.md` §14.
- Syntax reference: [Fountain official syntax](https://fountain.io/syntax/).
