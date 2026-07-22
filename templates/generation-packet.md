# Template · Generation Packet · AI 视频生成包

> Model-neutral extension of an approved shot list. One block per generation unit;
> use with `modules/production/ai-video.md`.

```yaml
subrecord_id: ART-003/v1
project_id: FW-YYYYMMDD-001
status: draft              # draft / approved / locked / stale
depends_on: [SC001, ART-002/v1]
validated_through_revision: 1
content_hash: ""
```

## Asset locks · 资产锁

| asset_id | canonical description/state | approved reference IDs | provenance/allowed use | forbidden drift |
|---|---|---|---|---|
| CHAR-001 |  | REF-001 front / REF-002 profile |  |  |
| LOC-001 |  | REF-010 |  |  |

## Unit · 生成单元

```yaml
shot_id: SC001-SH001
scene_id: SC001
narrative_job: ""
status: planned            # planned / keyframe-approved / generated / accepted / rejected / stale
duration_s: 0
aspect_ratio: "9:16"
reference_ids: []

continuity_in:
  subject_position: ""
  screen_direction_gaze: ""
  pose_action_phase: ""
  wardrobe_hair_makeup: ""
  prop_state: ""
  light_time_weather: ""
continuity_out: {}

first_frame: ""
last_frame: ""

prompt:
  subject_action: ""
  environment: ""
  composition_camera: ""
  lighting_color: ""
  motion_physics: ""
  style_lock: "STYLE-001"
dialogue_audio: ""
negative_constraints: []

render_plan:
  adapter: ""
  proxy_then_final: true
  seed_or_take: ""
acceptance_tests:
  - "identity matches CHAR-001 references"
  - "last frame satisfies continuity_out"
result:
  take_id: ""
  deviations: []
  accepted_by: ""
```

## Sequence continuity table · 镜间连续性

| from shot | state/reference out | to shot | required match | verified |
|---|---|---|---|---|
| SC001-SH001 |  | SC001-SH002 |  | ❌ |

## Rules

- one primary subject action and one primary camera behavior per unit;
- repeat canonical asset wording/IDs exactly—do not synonym-drift identities;
- validate keyframe and continuity before expensive motion/final generation;
- record accepted take and deviations; rejected output does not alter canon;
- register dependency IDs/revisions and `validated_through_revision` for accepted
  takes/endpoints; an unrelated root delta does not expire them, but a touched
  dependency marks the unit `stale` until reconciled;
- tool-specific capabilities live in an adapter note and must be verified.
