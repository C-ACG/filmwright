# Direction · Shot Breakdown · 分镜流程（场景 → 分镜表）

> Stage 7d. The procedure that turns a finished scene into a director's shot list /
> storyboard plan a crew can execute. This is the bridge from 编 to 导.
> 把写好的场景转成可执行的分镜表 / 故事板计划。从"编"到"导"的桥。

---

## §1. Inputs · 输入

A scene already written in Fountain (stage 7), plus:
- the scene's **micro dramatic action** (goal → obstacle → result) from the breakdown;
- its **dual-track pacing tag** (plot 松/中/紧 × emotion 轻/中/重);
- its **estimated runtime**;
- whose **POV** anchors the scene.

If any is missing, derive it before breaking down — the shot plan is meaningless
without knowing the beat it serves.

---

## §2. Procedure · 流程

**Step 1 — Read for the turn.** Find the scene's value turn (McKee §4 in
`02-structure.md`): where does the emotional charge flip? That moment gets the
scene's most deliberate shot (usually a push-in or a CU/ECU). Everything else is
built to deliver the audience to it.

**Step 2 — Block it.** Decide actor positions and movement (`blocking-and-coverage.md`
§1). Draw the 180° line. Staging first, lenses second.

**Step 3 — Choose the coverage strategy.** Pick the *minimum* set of shots that
build the scene with rhythm (`blocking-and-coverage.md` §3). Typically: an
establishing/master, the dialogue spine (OTS or singles), the reaction(s), the
insert(s), and the one designed shot on the turn.

**Step 4 — Assign grammar per shot.** For each shot decide size, angle, movement,
lens/focus, and lighting intent (`visual-language.md`) — each **motivated** by the
beat. Note the rough duration so the shot durations sum toward the scene runtime.

**Step 5 — Plan the seams.** Choose the transition in and out (`blocking-and-coverage.md`
§4) and any sound bridge.

**Step 6 — Emit the shot list.** Output to `templates/shot-list.md` (human) and/or
`templates/shot-list.csv` (machine). Number shots `SC<scene>-<n>` (e.g. `SC04-03`).

**Step 7 — Self-check.** Run the coverage self-check (`blocking-and-coverage.md` §7)
and confirm the shot durations roughly match the scene's runtime budget.

---

## §3. Shot-list schema · 分镜表字段

One row per shot. Keep it lean enough to fill, rich enough to shoot.

| Field | 中文 | Notes |
|---|---|---|
| `shot_id` | 镜号 | `SC04-03` |
| `size` | 景别 | EWS/WS/MS/MCU/CU/ECU/Insert |
| `angle` | 角度 | eye / high / low / OTS / POV / Dutch / top |
| `movement` | 运镜 | static / pan / tilt / dolly-in / track / crane / handheld / Steadicam / rack-focus |
| `lens_focus` | 焦距景深 | wide/normal/long; deep/shallow |
| `subject_action` | 画面内容 | who does what, in the frame |
| `dialogue_cue` | 台词点 | which line(s) this shot covers, or "—" |
| `light_intent` | 光意图 | low-key / motivated lamp / backlit / etc. |
| `sound_cue` | 声音 | diegetic / sound-bridge / silence / score |
| `duration` | 时长 | ~seconds |
| `transition_out` | 转场 | cut / match-cut / J-cut / dissolve … |
| `notes` | 备注 | the turn, eyeline, continuity flags |

---

## §4. Worked micro-example · 微样例

Scene (Fountain): two people at a table; she's about to tell him she's leaving.
Beat: plot **loose** + emotion **heavy** (the §5 mismatch). POV: him.

```
SC04-01 | WS    | eye        | static     | wide/deep    | The two at the table, room cold and large around them. | —                    | motivated window, low fill | room tone        | 4s  | cut     | establish geography; negative space = distance
SC04-02 | OTS   | eye        | static     | normal/shall | Over his shoulder onto her; she stalls, turns the cup.  | "你今天…比平时安静。"   | window soft               | —                | 5s  | cut     | her screen-right, keep the line
SC04-03 | MCU   | eye        | static     | normal/shall | Her, alone in frame, choosing the words.                | "我下周走。"            | window soft               | room tone        | 3s  | cut     | THE TURN sits in 04-04, not here
SC04-04 | CU→ECU| eye        | slow dolly-in | long/shall | Him. The line lands. He doesn't move; his thumb stops on the glass. | (silent)        | key drops a stop          | SILENCE          | 6s  | L-cut   | push on the realization; reaction carries it
SC04-05 | Insert| top        | static     | normal/deep  | His hand, still, on the glass. Hers withdraws from frame.| —                   | tabletop practical        | next scene audio under | 3s  | J-cut   | sound of next scene bleeds in over the held hand
```

Note how the turn (04-04) gets the only camera move and the silence, and the
listener — not the speaker — carries it. Total ≈ 21s, matching a short, heavy beat.

---

## §5. Format notes · 格式差异

- **Feature / series:** full breakdown per scene; storyboard the set-pieces.
- **Short / ultrashort:** breakdown is where the film is *made* — the visual idea
  often *is* the film; spend the most direction effort here.
- **Vertical micro-drama:** do **not** produce a separate shot list. Fold a
  lightweight per-clip note into the script (a size + a movement on the payoff is
  enough); the format is built for speed and AI-generation pipelines. See
  `modules/formats/vertical-microdrama.md`.
- **AI-generation pipelines (2D / 3D / image-to-video):** the shot list doubles as a
  generation brief — `size + angle + movement + light_intent + subject_action` maps
  cleanly to prompt fields. Keep `subject_action` concrete and free of metaphor.
