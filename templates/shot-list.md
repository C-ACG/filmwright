# Template · Shot List · 分镜表

> The stage-7d direction deliverable. One row per shot; the bridge from script to
> set (or to an AI-generation pipeline). Schema and procedure in
> `modules/direction/shot-breakdown.md`. Machine-readable twin: `shot-list.csv`.

## Per-scene header · 场次表头

```
SCENE 04 · INT. CONVENIENCE STORE - NIGHT
Dramatic action 戏剧动作: she must tell him she's selling the store → he won't come in
Pacing 节奏: plot 松 / emotion 重   ·   Runtime 时长: ~21s   ·   POV: Kai
The turn 价值转折: trust → severance, landing on SC04-04
```

## Shot rows · 分镜行

| shot_id | size | angle | movement | lens/focus | subject_action | dialogue_cue | light_intent | sound_cue | dur | trans_out | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SC04-01 | WS | eye | static | wide/deep | The two at the table, cold room around them | — | motivated window, low fill | room tone | 4s | cut | establish geography; negative space = distance |
| SC04-02 | OTS | eye | static | normal/shallow | Over his shoulder onto her; she turns the cup | "你今天…比平时安静。" | window soft | — | 5s | cut | her screen-right; hold the line |
| SC04-03 | MCU | eye | static | normal/shallow | Her alone, choosing the words | "我下周走。" | window soft | room tone | 3s | cut | the turn is in 04-04, not here |
| SC04-04 | CU→ECU | eye | slow dolly-in | long/shallow | Him; the line lands; thumb stops on the glass | (silent) | key drops a stop | SILENCE | 6s | L-cut | push on the realization; the reaction carries it |
| SC04-05 | Insert | top | static | normal/deep | His still hand on the glass; hers leaves frame | — | tabletop practical | next-scene audio under | 3s | J-cut | sound of next scene bleeds in over the held hand |

## Conventions
- **shot_id** = `SC<scene>-<n>`.
- Sizes EWS/WS/MLS/MS/MCU/CU/ECU/Insert · angles eye/high/low/OTS/POV/Dutch/top.
- Movement: static / pan / tilt / dolly-in|out / track / crane / handheld /
  Steadicam / rack-focus / whip.
- Keep `subject_action` concrete and metaphor-free — it doubles as an AI-generation
  prompt field (`shot-breakdown.md` §5).
- Shot durations should sum toward the scene's runtime budget.

## Self-check
Run `modules/direction/blocking-and-coverage.md` §7 before shipping a breakdown.
