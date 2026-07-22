# Template · Event Graph · 事件图

> A normative subrecord of Project State, not an independent truth source. Register
> its artifact ID, dependency IDs/revisions, and `validated_through_revision`.
> Unrelated root deltas do not expire it; a delta that changes an affected node,
> edge, or dependency marks this graph `stale` until reconciled.

> Causal and knowledge graph for long-form work. This complements a beat sheet:
> beats describe rhythm; events describe what becomes true and why.

```yaml
subrecord_id: ART-002/v1
project_id: FW-YYYYMMDD-001
status: draft              # draft / approved / locked / stale
depends_on: [DEC-001, SC001]
validated_through_revision: 1
content_hash: ""
```

## Event nodes · 事件节点

| event_id | scene/episode | preconditions | participants | action/conflict | outcome | state delta |
|---|---|---|---|---|---|---|
| EVT-001 | SC001 |  |  |  |  |  |

## Edges · 关系边

| from | relation | to | required? | evidence/notes |
|---|---|---|---|---|
| EVT-001 | causes / blocks / reveals / enables / pays-off / contradicts | EVT-002 | yes |  |

## Knowledge changes · 认知变化

| event_id | information ID | audience knows before/after | character knows before/after | reveal method |
|---|---|---|---|---|
| EVT-001 | INFO-001 | no → yes | CHAR-001: no → no | visual clue |

## Validation · 校验

- every load-bearing event has preconditions and an observable state delta;
- no character uses information before a knowledge edge grants it;
- every setup has a planned payoff edge or an explicit decision to drop it;
- deleting a scene cannot leave an event referenced without a new source;
- changes to a node invalidate dependent scene cards/artifacts until reviewed.
