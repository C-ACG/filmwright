# Production · AI Video · 生成式视频生产

> Optional production layer for image/video-generation workflows. It converts an
> approved screenplay and shot plan into model-neutral, continuity-aware generation
> units. It does not replace story or direction.

## §1. Principle · 原则

Generative video is a **stateful shot-production problem**, not a bag of prompts.
The unit of control is an approved shot with narrative intent, references,
continuity in/out, and acceptance tests.

Keep model-specific syntax in a project adapter, not in canon. Never promise a
feature, duration, resolution, or reference behavior that the active tool has not
verified.

## §2. Required inputs · 必要输入

- approved Scene Card and screenplay passage;
- approved canonical shot intent/list; for vertical micro-drama this is the
  normalized 13-field row derived from the embedded clip note;
- Project Card: aspect, target runtime, language, production form, delivery specs;
- Asset Bible: character/location/prop/style IDs and approved references;
- latest project-state revision, including wardrobe, damage, time, weather, and prop
  ownership;
- rights/provenance notes for every reference asset.

If a visible entity has no lock, create/approve the lock before generating dependent
shots.

## §3. Asset Bible · 资产圣经

### Character lock

```text
CHAR-001 · immutable face/body/age anchors · hair · costume state · tag object
approved reference IDs/angles · voice/performance anchors · forbidden drift
```

Use the exact same canonical wording and IDs across shots. Add temporary states
(`WARD-003 torn sleeve`, `MAKEUP-002 bloodless bruise`) rather than rewriting the
base identity.

### Location/style/prop locks

```text
LOC-001: geometry · entrances/axis · materials · practical lights · time/weather
STYLE-001: medium/look · palette · contrast · texture · camera behavior · avoid
PROP-001: appearance · holder · condition · screen direction · continuity events
```

Reference images are evidence, not prose decoration. Record `ref_id`, origin,
allowed use, and which lock it supports.

## §4. Generation unit · 生成单元

Use `templates/generation-packet.md`. One unit should normally contain one primary
subject action and one primary camera behavior. Split choreography that requires
several independent actions, locations, or temporal jumps.

Required fields:

```text
shot_id · narrative_job · duration/aspect · continuity_in/out · reference_ids
first_frame · last_frame · subject/action · environment · composition/camera
lighting/color · motion/physics · dialogue/audio · negative_constraints
render_plan · acceptance_tests · take/status
```

The prompt describes observable state. Avoid emotion labels without performance
evidence, contradictory camera verbs, generic “cinematic/masterpiece” filler, and
long lists of mutually competing actions.

## §5. Continuity graph · 连续性图

Each accepted shot produces a state edge:

```text
SC004-SH003 last_frame/state  →  SC004-SH004 first_frame/state
```

Track at minimum: subject position and screen direction; pose/action phase; gaze;
wardrobe/hair/makeup/damage; held props; lighting/time/weather; location geometry;
lens/scale relationship; dialogue/action timing.

For cross-scene continuity, use approved endpoint frames or references when the
active tool supports them. If it does not, carry the state text and validate the
first generated frame before motion.

## §6. Production loop · 生产循环

1. **Plan** — approve narrative job, locks, and first/last-frame intent.
2. **Keyframe gate** — validate identity, composition, geography, and continuity on
   a cheap still/proxy where possible.
3. **Motion pass** — generate only after the visual anchor passes.
4. **Critic pass** — compare output to acceptance tests and references; identify the
   smallest failing variable.
5. **Retry narrowly** — change one dominant variable at a time; do not churn canon.
6. **Accept take** — record take ID, provenance, deviations, and continuity out.
7. **Edit/audio pass** — assemble, then evaluate rhythm, A/V sync, dialogue, room
   tone, music, and transition—not just isolated clip beauty.

Generate low-cost proxies before high-cost finals when the tool offers such tiers.
The user approves expensive or irreversible production gates.

## §7. Multimodal critic · 多模态质检

When visual inspection is available, score with evidence:

- identity/reference match;
- action and narrative-job match;
- shot grammar/composition;
- physical/temporal continuity;
- artifact/physics integrity;
- text/lip/audio sync where applicable;
- editability: clean handles, stable endpoint, usable duration.

Reject a beautiful clip that fails the story job. Do not silently canonize a model
accident; propose it as a discovery and update the state only after approval.

## §8. Model adapter · 模型适配层

Keep a small per-tool note outside the creative canon:

```text
supported inputs/references · tested duration/aspect · prompt order
camera/motion vocabulary · audio/lip behavior · seed/retry controls · known failures
```

Verify current capabilities from official documentation or an actual test. The
portable generation packet remains stable when tools change.
