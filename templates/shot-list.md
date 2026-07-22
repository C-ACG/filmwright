# Template · Shot List · 分镜表

> Human-readable view of the canonical shot schema. Machine-readable twin:
> `shot-list.csv`; row schema: `schemas/shot-list.schema.json`.

## Per-scene header · 场次表头

```text
SCENE_ID: SC004 · INT. CONVENIENCE STORE - NIGHT
Dramatic action: she must tell him she is leaving → he will not come in
Pacing: plot 松 / emotion 重 · Target runtime: 21s · POV: CHAR-002
Turn: trust → severance, landing on SC004-SH004
Continuity in/out: <state IDs and changes>
```

## Canonical columns · 规范字段

| shot_id | scene_id | size | angle | movement | lens_focus | subject_action | dialogue_cue | light_intent | sound_cue | duration_s | transition_out | notes |
|---|---|---|---|---|---|---|---|---|---|---:|---|---|
| SC004-SH001 | SC004 | WS | eye | static | wide/deep | The two at the table, cold room around them | — | motivated window, low fill | room tone | 4 | cut | establish geography |
| SC004-SH002 | SC004 | MCU | OTS | static | normal/shallow | Over his shoulder onto her; she turns the cup | “你今天……比平时安静。” | window soft | room tone | 5 | cut | maintain screen side |
| SC004-SH003 | SC004 | MCU | eye | static | normal/shallow | Her alone; fingers stop turning the cup | “我下周走。” | window soft | room tone | 3 | cut | setup for reaction |
| SC004-SH004 | SC004 | CU | eye | dolly_in | long/shallow | His thumb stops against the glass | — | motivated window, low fill | room tone drops | 6 | L_cut | ends ECU; the turn |
| SC004-SH005 | SC004 | INSERT | top | static | normal/deep | His hand remains; hers leaves frame | — | tabletop practical | next-scene audio under | 3 | J_cut | endpoint continuity |

## Vocabulary & IDs · 词汇与编号

- Standalone IDs: `SC004-SH003`; episodic IDs: `EP012-SC004-SH003`.
- `size`: `EWS / WS / MLS / MS / MCU / CU / ECU / INSERT`.
- `angle`: `eye / high / low / OTS / POV / dutch / top`.
- `movement`: `static / pan / tilt / dolly_in / dolly_out / track / crane /
  handheld / steadicam / rack_focus / whip_pan`.
- `transition_out`: `cut / match_cut / J_cut / L_cut / dissolve / fade /
  smash_cut / whip_cut`.
- `duration_s` is a positive number; the scene sum should approximate its target
  runtime.
- Keep `subject_action` observable and metaphor-free.
- For generative production, do not overload this table; add the generation packet.

## Self-check

Run `modules/direction/blocking-and-coverage.md` §7 and the direction checks in
`modules/qa/script-doctor.md` before release.
