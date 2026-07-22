# Template · Project State · 项目状态

> Canonical root state for multi-artifact or multi-session work. Keep one current
> copy. Detailed Event Graph and production records are dependency-validated subrecords
> registered here; checkpoints and Context Packs are disposable projections.

```yaml
schema: filmwright.project-state/v1
filmwright_version: 0.2.0
project_id: FW-YYYYMMDD-001
revision: 1
status: active
workflow_mode: guided
current_stage: contract
last_approved_artifact: null
updated_at: YYYY-MM-DD
```

## Project Card · 项目卡

```text
Deliverable:
Format / runtime:
Audience / platform / rating:
Language:
Tone / reference qualities:
Production mode / budget:
Cast / location / schedule / safety constraints:
Must keep:
Must avoid:
Definition of done:
```

## Authority & locks · 权威与锁定

| id | decision/canon | authority | status | source | supersedes |
|---|---|---|---|---|---|
| DEC-001 |  | user / source / working | proposed / approved / locked / superseded |  | — |

## Source registry · 来源表

| source_id | source/version | authority | allowed use | must preserve | citation/provenance |
|---|---|---|---|---|---|
| SRC-001 |  |  |  |  |  |

## Entity canon · 实体正史

### Characters

| id | fixed identity | current physical/emotional state | knows | wants now | voice/behavior lock |
|---|---|---|---|---|---|
| CHAR-001 |  |  |  |  |  |

### Locations / props / style assets

| id | fixed description | current state/holder | continuity constraints | reference IDs |
|---|---|---|---|---|
| LOC-001 |  |  |  |  |
| PROP-001 |  |  |  |  |

## Timeline & event registry · 时间线与事件表

| event_id | story time / order | scene_id | participants | precondition → action → outcome | state delta | detailed record |
|---|---|---|---|---|---|---|
| EVT-001 |  | SC001 | CHAR-001 |  |  | `event-graph.md#EVT-001` |

## Information & knowledge registry · 信息与认知表

| info_id | truth / claim | audience knows | character knowledge | learned/revealed at | authority/status |
|---|---|---|---|---|---|
| INFO-001 |  | no | CHAR-001: knows; CHAR-002: does not know | EVT-001 / SC001 | working |

## Scene index · 场景索引

| scene_id | status | slugline | POV | turn / exit value | runtime | continuity out | artifact |
|---|---|---|---|---|---|---|---|
| SC001 | planned / map-approved / drafted / approved / locked / stale |  |  |  |  |  |  |

## Threads & setups · 线索与伏笔

| id | type | planted/current state | owner/knowers | planned resolution | status |
|---|---|---|---|---|---|
| SETUP-001 | setup / hidden line / question |  |  |  | active / paid / dropped |

## Artifact dependencies · 产物依赖

| artifact_id/version | path | depends on IDs/revisions | status | invalidated by |
|---|---|---|---|---|
| ART-001/v1 |  | DEC-001, SC001, state r1 | draft / approved / locked / stale | — |

## Normative subrecords · 规范子记录

Subrecords contain detail that is too large for this root. They are authoritative
only while registered here, approved/locked, and all declared dependency
IDs/revisions remain current. `validated_through_revision` records the last root
revision at which that test passed; it does **not** expire merely because an
unrelated State Delta advances the root. If a delta touches a declared dependency,
mark the subrecord `stale` immediately and reconcile it before downstream use.

| subrecord_id | type/path | depends on IDs/revisions | validated_through_revision | owns detail for | status |
|---|---|---|---:|---|---|
| ART-002/v1 | Event Graph / `event-graph.md` | DEC-001, SC001 | 1 | EVT-* edges and event-local deltas | draft / approved / locked / stale |
| ART-003/v1 | Production State / generation packet | SC001, ART-002/v1 | 1 | TAKE-* results and endpoint continuity | draft / approved / locked / stale |

Conflict order: current root locks and decisions → current registered subrecord →
derived projection. After a relevant upstream change, reconcile the subrecord,
update dependency versions, and advance `validated_through_revision`.

## Production continuity registry · 生产连续性表

| shot_id | take_id | status | depends on | first/last-frame refs | continuity out | provenance / accepted by | validated through |
|---|---|---|---|---|---|---|---:|
| SC001-SH001 | TAKE-001 | planned / keyframe-approved / generated / accepted / rejected / stale | SC001, ART-002/v1 |  |  |  | 1 |

## Assumptions & open questions · 假设与待决

| id | assumption/question | impact | reversible? | owner | status |
|---|---|---|---|---|---|
| ASM-001 |  | low / medium / high | yes / no | user / Filmwright | open |

## Next action · 下一步

```text
Next artifact:
Required inputs/modules:
Blocking issue (if any):
```

## State Delta · 状态增量

Append after each completed unit:

```text
DELTA rN → rN+1
Added:
Changed:
Locked / unlocked:
Superseded:
Continuity effects:
Invalidated/reconciled artifacts:
New conflicts / assumptions:
Next action:
```
