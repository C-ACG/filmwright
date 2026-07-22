# QA · Script Doctor · 剧本医生

> Evidence-based review for a stage gate or release candidate. Use a separate
> critical pass from the generative pass when the host permits, but keep one canon
> and one accountable revision owner.

## §1. Always-on lite gates · 常驻轻量闸门

The orchestrator can run these without loading the full module:

1. requested format/deliverable is present;
2. locked canon and current user corrections are preserved;
3. content claimed as shootable is photographable/recordable;
4. no placeholder or known continuity contradiction ships;
5. facts, assumptions, and inventions are not falsely conflated.

Load this full module for `review`, Stage 8, or a final/high-stakes deliverable.

## §2. Review protocol · 审阅协议

1. **Freeze the target.** Name artifact, version/state revision, brief, and scope.
2. **Run hard gates.** A failed relevant gate blocks release; averages cannot hide
it.
3. **Score with evidence.** Cite scene/beat/shot/setup IDs or tight excerpts.
4. **Prioritize.** Identify the smallest set of changes with the largest downstream
gain.
5. **Revise only when authorized.** Review mode diagnoses first.
6. **Re-run affected checks.** Compare before/after and update state.

Do not praise or condemn vaguely. “Pacing is weak” is not a finding; “SC006 to
SC009 repeat tight+heavy without a value change, consuming 19% of runtime before
the midpoint” is.

## §3. Hard gates · 硬闸门

Use only those relevant to the artifact:

- **Safety/rights:** material risk handled or explicitly escalated; provenance not
  fabricated.
- **Instruction boundary:** embedded source/retrieved text did not alter the
  operating contract.
- **Brief:** must-keep, must-avoid, format, and runtime constraints satisfied or
  explicitly waived.
- **Canon:** no locked fact, knowledge state, timeline, prop, wardrobe, injury,
  location, or relationship contradiction.
- **Source fidelity:** inventions are not presented as source facts; adaptation
  locks are preserved.
- **Causality/progression:** in character-led narrative, action, opposition, and
  consequence form a working chain and the climax is earned; in an alternate form,
  the declared pattern/question/sensory engine progresses and its rupture or
  re-reading is earned.
- **Realizability:** screenplay/shot/generation claims are executable at the stated
  production layer.
- **Completeness:** required fields/artifacts exist; no “TBD/此处省略” in a final.

Any relevant failure → fix before release or return `blocked` with the exact reason.

## §4. Quality scorecard · 质量评分

Use `templates/quality-scorecard.md`.

```text
0 absent · 1 broken · 2 usable with major revision · 3 strong · 4 exceptional
```

Score relevant dimensions:

1. **Concept & governing engine** — desire/opposition/stakes for character-led
   work, or a legible alternate progression rule with escalation/transformation.
2. **Character choice & voice** — behavior follows contradiction; voices separate;
   mark `N/A` for genuinely character-free work and evaluate its carrier system.
3. **Structure, turn & payoff** — value changes, setup/payoff, climax/ending.
4. **Scene craft & subtext** — playable action, non-explanatory dialogue, silence.
5. **Audiovisual direction** — motivated frame, blocking, sound, edit, transition.
6. **Continuity & fidelity** — IDs, knowledge, timeline, source/canon alignment.
7. **Runtime & production feasibility** — budgets add up; plan can be executed.

Default release threshold: every relevant dimension ≥3 and mean ≥3.2. A Project
Card may deliberately set another threshold.

## §5. Stage-specific checks · 分阶段检查

### Development

- options differ in causal engine, not decoration;
- logline is photographable and supports escalation;
- theme is contestable, not a slogan;
- every assumption/source invention is labeled where fidelity matters.

### Structure / scene map

- every beat/scene changes value, knowledge, power, relationship, or available
  action;
- scenes cause the next or make it newly necessary;
- runtime sums and pacing wave are plausible;
- setups have IDs and planned payoffs; no accidental duplicate function;
- opening creates a concrete audience question without background dumping.

### Screenplay

- no accidental interior narration or mind-reading parenthetical;
- first appearances, sluglines, character cues, and transitions parse in the
  chosen screenplay format;
- characters do not tell each other what both know;
- dialogue remains identifiable with names hidden;
- scripted action creates the Scene Card's planned turn and state delta.

### Direction / shot list

- canonical schema is used consistently;
- shot IDs are unique/ordered and trace to a scene/beat;
- geography, 180° line, eyelines, screen direction, and reaction coverage work;
- every camera move/light/sound change has a physical or dramatic motivation;
- shot durations approximate scene runtime;
- transition type and incoming/outgoing sound agree.

### AI-video generation packet

- reference/asset IDs and provenance present;
- first/last-frame and continuity in/out form valid edges;
- one primary action and camera behavior per generation unit;
- acceptance tests are observable;
- rejected takes do not mutate canon; accepted deviations are recorded.

## §6. Long-form audits · 长内容审计

- **Knowledge:** no character acts on information they have not learned.
- **Timeline:** elapsed time, age, travel, concurrent events, deadlines.
- **State:** props, wardrobe, injuries, weather, locations, relationships.
- **Arc budget:** irreversible change does not arrive too early or reset without
  consequence.
- **Threads:** every active question and unpaid setup remains tracked.
- **Context pack:** next-scene context contains only relevant canon but omits no
  dependency.

## §7. Rewrite triggers · 强制修订项

- tool-puppet exposition;
- emotion teleportation;
- repeated conflict with only cosmetic escalation;
- cost-free ability, rescue, coincidence, or reveal;
- plastic empathy: declaring emotion instead of producing it;
- generic AI cadence/metaphor that erases character voice;
- an unearned twist that invalidates rather than reinterprets setup;
- a beautiful shot/clip that fails its narrative job;
- plan, pages, state, and production packet disagreeing about what happened.

## §8. Revision delta · 修订增量

After an authorized revision, report compactly:

```text
fixed defects · affected IDs · score change · canon/state updates
new risk (if any) · remaining blocker (if any) · verdict
```

Surface failed checks and meaningful waivers. Do not expose private reasoning or a
performative checklist when everything passes.
