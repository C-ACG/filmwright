# Template · Memory Checkpoint · 记忆检查点

> Portable handoff projected from a specific `project-state` revision. Update canon
> in Project State first, then regenerate this compact view. Never maintain two
> conflicting truths.

```text
════════════════════════════════════════
CHECKPOINT #N · PROJECT <id> · STATE rN
position: <stage / sequence / episode / last approved scene>
artifact: <latest approved path/version>
════════════════════════════════════════

PROJECT CARD (only constraints needed downstream)
  deliverable / format-runtime / audience-platform / language
  must keep / must avoid / production mode

LOCKED FACTS (IDs; never change silently)
  DEC-___:

CURRENT ENTITY STATE (only active/relevant entities)
  CHAR-___: physical/emotional state · knows/doesn't know · wants now
  LOC-___ / PROP-___: state · holder/position · continuity constraint

TIMELINE & RECENT EVENTS
  current story time / deadline / elapsed time
  EVT-___: cause → event → state change

ACTIVE THREADS & SETUPS
  SETUP-___: planted at ___ → planned payoff ___ · status
  unanswered question / hidden line / relationship pressure

CONTRADICTIONS / ASSUMPTIONS
  CON-___: unresolved conflict + affected IDs
  ASM-___: reversible assumption + impact

PACING / ARC POSITION
  last unit plot/emotion tag · current structural position · arc spend

NEXT UNIT
  next Scene Card ID · goal/obstacle/turn · dependencies to load
════════════════════════════════════════
```

## Scale add-ons · 长内容附加

- **Feature:** sequence, A/B/C progress, next major beat, world layer released.
- **Series:** episode/season phase, arc budget, inter-episode handoff, knowledge and
  hidden-line changes.
- **Micro-drama:** locks, payoff class rotation, emotion curve, four ledger views,
  last hook and required three-second pickup.
- **AI video:** accepted take IDs, endpoint references, wardrobe/damage/prop state,
  next generation-unit dependencies.

## Resume protocol · 续写协议

1. Verify checkpoint project/state revision and locate the matching artifact.
2. If a newer Project State exists, regenerate from it instead of trusting this
   stale checkpoint.
3. Build `templates/context-pack.md` for the next unit.
4. After writing, merge the State Delta into Project State and create a new
   checkpoint only at a useful handoff boundary.
