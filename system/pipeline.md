# Filmwright Pipeline · 流水线契约

> The full creative state machine for Filmwright v0.2. Format modules scale its
> depth. Guided mode gates consequential decisions; Sprint and Direct modes may
> traverse or enter stages without ceremonial pauses.

## Shared stage contract · 通用步骤契约

Every stage has five parts:

1. **Input** — approved upstream artifacts and current state revision.
2. **Work** — the creative or analytical operation.
3. **Artifact** — a named, reusable deliverable.
4. **Acceptance** — observable checks, not “looks good”.
5. **State Delta** — what became true, changed, locked, or remains unresolved.

Do not regenerate approved upstream work merely to change phrasing. If a downstream
discovery invalidates it, propose a specific revision and mark the superseded
decision.

### Format override contract

The active format and Project Card may replace a generic character-led technique
with an explicit alternate progression contract. Mark non-applicable fields `N/A`
and name what replaces them. This can override protagonist, Want/Need, conventional
climax, dialogue, or goal/conflict defaults; it cannot waive safety/rights, the
instruction boundary, brief, locked canon, source fidelity, realizability,
continuity, or completeness.

## Stage 0 — Contract · 项目契约

**Goal:** understand the requested outcome with minimum friction.

**Artifact:** Project Card:

```text
deliverable · format/runtime · audience/platform/rating · language · tone/reference
canon/source · must-keep · must-avoid · production mode/budget/constraints · workflow mode
```

**Acceptance:** the deliverable and non-negotiables are clear; missing details are
either blocking questions or explicit reversible assumptions. For multi-session or
multi-artifact work, initialize `templates/project-state.md`.

## Stage 1 — Core action · 核心动作

**Goal:** establish the governing engine. Character-led narrative uses protagonist
+ urgent goal + direct obstacle + stakes/pressure. Character-free/formal work uses
an explicit observable progression rule from the active format contract.

**Artifact:** 3–5 genuinely different candidates when exploring; one approved
logline and core action when converging.

**Acceptance:** photographable/audible premise; the selected engine can generate
progression; options differ in engine rather than surface decoration.

## Stage 2 — Synopsis · 梗概

**Goal:** let the user experience the whole trajectory and tone before detail.

**Artifact by scale:** one line for ultrashort; 100–250 Chinese characters for a
short; a one-page treatment for feature/season; episode line map for series.

**Acceptance:** beginning condition, progression, decisive choice/rupture/re-reading,
and ending image are legible; prose carries the intended genre/tone; no beat-list
disguised as a treatment.

## Stage 3 — Character and relationship · 人物与关系

**Goal:** build behavior-producing contradictions, not biographies for their own
sake.

**Artifact:** Want / Need / contradiction / pressure behavior / voice fingerprint /
arc; for long form add Ghost / Lie / Flaw, relationship matrix, and supporting-role
functions.

**Acceptance:** choices follow from character; principal voices remain identifiable
without name labels; every speaking support role has a dramatic function.

For character-free work, record `N/A — character-free` and validate the entities,
objects, narration, or formal rules that carry continuity instead.

## Stage 4 — Backstory, world, and canon · 前史、世界与正史

**Goal:** know the world before choosing the cross-section shown on screen.

**Artifact:** era/context; relationship history; world rules and reveal schedule;
cross-section choice; canon/source locks; adaptation ledger when applicable.

**Acceptance:** story starts at the most charged useful moment; rules create action;
backstory has a delivery path other than exposition; source facts and inventions are
distinguishable.

## Stage 5 — Structure · 结构

**Goal:** design escalation or formal progression, reversals, pacing,
setups/payoffs, and a decisive climax/rupture/re-reading appropriate to the format.

**Artifact:** timed beat sheet with plot/emotion tracks, opening hook, setup/payoff
IDs, subplot crossings, and ending image.

**Acceptance:** each beat changes value, pressure, knowledge, or the declared
pattern; runtime adds up; the decisive turn externalizes a choice or visibly changes
the governing form; no three consecutive beats repeat the same pacing state without
intent.

## Stage 6 — Scene map · 场景地图

**Goal:** turn beats into executable dramatic units.

**Artifact:** one Scene Card per scene:

```text
scene_id · slugline · POV/alignment · goal+obstacle or formal unit job · turn · exit value
runtime · plot/emotion tag · setup/payoff IDs · continuity in/out
```

**Acceptance:** every scene/unit causes, enables, reframes, or intentionally
contrasts with the next under the declared form; no dead unit without a turn or
indispensable setup function; total runtime is plausible; continuity deltas are
explicit.

Long work creates a checkpoint after the map and at sequence/episode boundaries.

## Stage 7 — Screenplay · 场景写作

**Goal:** realize the map as performance, image, sound, and subtext in Fountain or
the required platform format.

**Artifact:** screenplay pages with stable scene IDs kept in comments/headers or
the companion scene map.

**Acceptance:** only intentional subjective devices; distinct spoken voices;
action is concrete; setup/payoff IDs land naturally; runtime remains within budget;
the scripted scene produces the planned state delta.

## Stage 7d — Direction · 导演拆解

**Goal:** translate a finished scene into blocking, coverage, shot rhythm, sound,
and transitions.

**Artifact:** shot list. Live-action vertical micro-drama may keep the lightweight
shot note embedded in the script. AI-generated vertical work must normalize that
note to the canonical shot-row fields before adding
`templates/generation-packet.md`; the normalized CSV may remain an intermediate
unless the user requests it.

**Acceptance:** each shot has a narrative job; geography/axis/eyelines are coherent;
the scene turn receives deliberate emphasis; durations approximate the scene
budget; continuity in/out is executable.

## Stage 8 — QA and revision · 诊断与修订

**Goal:** find defects, repair them, and prove the revision improved the artifact.

**Artifact:** hard-gate result; evidence-based scorecard; prioritized fixes; revised
artifact when authorized; before/after delta.

**Acceptance:** no hard-gate failure; all required score dimensions meet the release
threshold; fixes do not break locked canon or introduce new continuity errors.

## Entry rules · 直达规则

- **Existing draft review:** enter Stage 8, loading only the modules needed to judge
  that artifact.
- **Single-scene rewrite:** validate its Scene Card, then enter Stage 7.
- **Shot list request:** derive missing Stage-6 fields, then enter Stage 7d.
- **Continuation:** start from latest state + next Scene Card; do not recap unless
  needed.
- **Adaptation:** enter Stage 0/4 for source locks before changing plot.
- **AI-video execution:** require approved shot intent and asset/continuity locks;
  then use Stage 7d production packets.

## Gate behavior · 闸门行为

- **Guided:** offer `pass / revise / review` at decisions that materially constrain
  later work. Do not pause after trivial formatting work.
- **Sprint:** continue across requested stages, preserving an assumption log. Pause
  only for a blocker, rights/safety issue, destructive action, or expensive render
  gate.
- **Direct:** return the bounded deliverable plus state delta.
- **Review:** return diagnosis first; do not silently replace the user's work.
