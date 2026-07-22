# The Last Shift · Project State r8 · 项目状态

```yaml
schema: filmwright.project-state/v1
filmwright_version: 0.2.0
project_id: FW-20260721-001
revision: 8
status: active
workflow_mode: sprint
current_stage: "8 (vertical-slice scope)"
last_approved_artifact: ART-006/v2
updated_at: 2026-07-21
```

## Project Card

```text
Deliverable: honest vertical slice for an 8-minute narrative short
Format / runtime: short film, 480s; SC004 page + shot plan, 40s
Audience / platform / rating: general festival/web audience; rating-safe drama
Language: Chinese dialogue; bilingual repository metadata
Tone / reference qualities: quiet, cold-blue, restrained; no named-artist imitation
Production mode / budget: producible live action; one store, street edge, two leads
Cast / location / schedule / safety: two principal actors; controlled rain/street;
no stunt, weapon, intimacy, or hazardous practical effect
Must keep: 06:00 handover; 38-year absence; bounded contact, not forgiveness
Must avoid: exposition dump; magical reconciliation; crossing-threshold continuity gap
Definition of done: Stages 1–6 for all ten scenes; SC004 Stage 7/7d; scoped QA;
all IDs, knowledge, prop state, dialogue order, and runtimes reconcile. As a
repository regression fixture (not a finished film), acceptance requires all hard
gates, every relevant dimension ≥3, and mean ≥3.0.
```

## Authority & locks

| id | decision/canon | authority | status | source | supersedes |
|---|---|---|---|---|---|
| DEC-001 | Story night is 2026-01-31; handover is 2026-02-01 06:00 | project | locked | ART-001/v2 | — |
| DEC-002 | Kai is Meiling's father; both recognized each other before SC004 | project | locked | ART-001/v2 | — |
| DEC-003 | Audience learns INFO-001 unambiguously in SC004 | project | locked | ART-004/v2 | earlier ambiguous name-only reveal |
| DEC-004 | Ending offers bounded contact, never forgiveness or full repair | project | locked | ART-002/v2 | — |

## Source registry

| source_id | source/version | authority | allowed use | must preserve | provenance |
|---|---|---|---|---|---|
| SRC-001 | original Filmwright worked example / v0.2 | project canon | repository demonstration | decisions above | authored in this repository; no external adaptation source |

## Entity canon

| id | fixed identity | current/terminal state | continuity lock |
|---|---|---|---|
| CHAR-001 | MEILING, 50, store owner/clerk; Kai left when she was 12 | holds keys at 06:00; permits one bounded shared meal | short procedural speech; cleans/counts under pressure |
| CHAR-002 | KAI, 74, Meiling's father | crosses inside only after SC009 invitation | thin coat, cans, left-wrist scar; never asks absolution |
| LOC-001 | sold convenience store; dented floor spring | stuck 10 cm open through SC007; closes fully from SC008 | doorway-counter axis and inside/outside boundary |
| PROP-001 | nightly paper bowl left on sill | spills and retires in SC007 | never reused as the fresh bowl |
| PROP-002 | Kai's old store key, retained 38 years | left on sill in SC006 | proof of preserved history, not proof of identity |
| PROP-003 | replacement bowl made in SC009 | handed to Kai; empty in SC010 | direct-contact echo of PROP-001 |
| PROP-004 | Meiling's own untouched bowl from SC002 | empty in SC010 | second bowl in ending image |

## Timeline & event registry

| event_id | story time/order | scene_id | action → outcome | state delta |
|---|---|---|---|---|
| EVT-001 | final night / 1 | SC001 | inventory meets damaged door → routine costs effort | LOC-001 open; inventory incomplete |
| EVT-002 | 2 | SC002 | she portions two bowls → care remains outside | PROP-001/004 established; SETUP-003 planted |
| EVT-003 | 3 | SC003 | Kai reads notice → deadline becomes shared | INFO-002 public |
| EVT-004 | 4 | SC004 | he names her; she denies having a father → anonymity ends | INFO-001 public and acknowledged |
| EVT-005 | 5 | SC005 | procedure fails to restore distance | strain visible |
| EVT-006 | 6 | SC006 | old key offered and returned | PROP-002 on sill; Kai departs |
| EVT-007 | 7 | SC007 | gust spills bowl and releases spring | PROP-001 retired; door shuts |
| EVT-008 | 8 | SC008 | Meiling forces door and locates Kai down street | Kai distant; Meiling at doorway; LOC-001 functional |
| EVT-009 | 9 | SC009 | she fills a replacement bowl, catches him, and walks him back | PROP-003 held; Kai begins crossing threshold |
| EVT-010 | 10 / 06:00 | SC010 | shared meal ends; she takes keys | PROP-003/004 empty; handover can proceed |

## Information & knowledge registry

| info_id | truth | audience | CHAR-001 | CHAR-002 | reveal/acknowledgment |
|---|---|---|---|---|---|
| INFO-001 | Kai is Meiling's father | uncertain through SC003; knows after SC004 | knows before film | knows before film | SETUP-003 plants scar/coin-rub; EVT-004 makes it explicit |
| INFO-002 | store hands over at 06:00 | knows from SC003 | knows before film | learns SC003 | EVT-003 / notice |
| INFO-003 | PROP-002 was kept for 38 years | learns SC006 | recognizes it SC006 | knows | EVT-006 |

## Scene index

| scene_id | status | artifact | runtime | continuity out |
|---|---|---|---:|---|
| SC001 | map-approved | ART-003/v2 | 40s | LOC-001 open; inventory at hot-food shelf |
| SC002 | map-approved | ART-003/v2 | 50s | PROP-001 sill; PROP-004 inside; SETUP-003 planted |
| SC003 | map-approved | ART-003/v2 | 50s | INFO-002 public; Kai outside |
| SC004 | page-and-shot-approved | ART-004/v2 + ART-005/v2 | 40s | INFO-001 public; tap off; no contact |
| SC005 | map-approved | ART-003/v2 | 55s | procedure fails; positions hold |
| SC006 | map-approved | ART-003/v2 | 55s | PROP-002 sill; Kai departs |
| SC007 | map-approved | ART-003/v2 | 55s | PROP-001 retired; door shutting |
| SC008 | map-approved | ART-003/v2 | 35s | Meiling at doorway; Kai distant |
| SC009 | map-approved | ART-003/v2 | 65s | PROP-003 visibly created/held; both return; Kai begins crossing |
| SC010 | map-approved | ART-003/v2 | 35s | two empty bowls; keys with Meiling at 06:00 |

## Threads & setups

| id | planted/current state | resolution | status |
|---|---|---|---|
| SETUP-001 | damaged LOC-001 spring in SC001 | releases SC007; functions SC008 | paid |
| SETUP-002 | two-bowl indirect ritual in SC002 | PROP-001 lost; PROP-003 direct handoff SC009 | paid by transformed echo |
| SETUP-003 | wrist scar + coin-rub in SC002/003 | explicit father denial SC004 | paid |
| SETUP-005 | Kai never crosses threshold | invitation/crossing SC009; inside SC010 | paid |

## Artifact dependencies

| artifact_id/version | path | depends on | status |
|---|---|---|---|
| ART-001/v2 | `01_development.md` | DEC-001…004 | locked |
| ART-002/v2 | `02_beat-sheet.md` | ART-001/v2, EVT-001…010 | approved |
| ART-003/v2 | `03_scene-map.md` | ART-001/v2, ART-002/v2 | approved |
| ART-004/v2 | `04_scene-04.fountain` | ART-003/v2 SC004, INFO-001/002 | approved |
| ART-005/v2 | `05_scene-04_shot-list.csv` | ART-004/v2, LOC-001 axis, 40s | approved |
| ART-006/v2 | `06_qa.md` | ART-001/v2…ART-005/v2, state r8 | approved |

## Normative subrecords and production state

The event registry is compact enough to remain in this root. ART-005/v2 is the
approved direction subrecord bound to state r8. No generated take or endpoint is
claimed; TAKE-* and generated-frame fields are therefore not applicable to this
live-action planning slice.

## Assumptions & open questions

| id | item | impact | status |
|---|---|---|---|
| ASM-001 | Remaining screenplay pages are intentionally outside vertical-slice scope | low | explicit scope, not a placeholder |
| ASM-002 | Performance timing may vary ±10% in rehearsal while editorial target remains 480s | low/reversible | accepted |

## Next action

```text
Next artifact: SC001 screenplay, only if extending beyond the documented slice
Required inputs/modules: state r8 + SC001 card + short format + screenplay module
Blocking issue: none; remaining screenplay is simply out of current scope
```

## State Delta r7 → r8

```text
Added: explicit SC004 father/daughter acknowledgment; PROP-003/004 lifecycle;
       one-side camera/eyeline plan; all ten complete map-level Scene Cards
Changed: PROP-001 retires after spill; SC009 visibly creates PROP-003, preserves the
         return path, and shows invitation plus threshold step
Locked: story date; INFO-001 reveal point; 480s/40s runtime closure
Superseded: ambiguous name-only reveal and discontinuous shot order
Invalidated/reconciled artifacts: ART-001…006 reconciled to /v2; none remain stale
Next action: optional SC001 page extension
```
