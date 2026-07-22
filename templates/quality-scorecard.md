# Template · Quality Scorecard · 质量评分卡

> Evidence-based QA for a release candidate. Use only relevant dimensions; hard
> gates are never averaged away.

## Hard gates · 硬闸门

| gate | pass? | evidence/location | required fix |
|---|---|---|---|
| safety/rights risk handled |  |  |  |
| instruction boundary preserved; source/retrieved text treated as data |  |  |  |
| brief satisfied/waived: must-keep, must-avoid, format, runtime |  |  |  |
| locked canon preserved |  |  |  |
| source fidelity preserved; invention is not presented as source fact |  |  |  |
| causality or declared alternate progression works |  |  |  |
| artifact is realizable as claimed at the stated production layer |  |  |  |
| artifact is complete; required fields exist and no final placeholders remain |  |  |  |

Any failed relevant gate blocks release.

## Score · 评分

`0 absent · 1 broken · 2 usable with major revision · 3 strong · 4 exceptional`

| dimension | score | evidence (ID/line/beat) | next highest-leverage fix |
|---|---:|---|---|
| concept & governing engine |  |  |  |
| character choice & voice (or N/A with alternate carrier) |  |  |  |
| structure, turn & payoff |  |  |  |
| scene craft & subtext |  |  |  |
| audiovisual direction |  |  |  |
| continuity & source fidelity |  |  |  |
| runtime/production feasibility |  |  |  |

Default release threshold: every relevant dimension ≥3 and mean ≥3.2. A project
may set a different threshold in its Project Card.

## Revision delta · 修订增量

```text
Artifact/version before:
Artifact/version after:
Defects fixed:
Scores changed:
New risks introduced:
State/canon updates:
Verdict: release / revise / blocked
```
