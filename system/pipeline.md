# Pipeline · 八步流水线契约

> The stage-by-stage contract referenced by the orchestrator. Each stage states
> its goal, inputs, output shape, and the gate that closes it. Format modules
> override depth per stage; this file defines the default.
>
> 每一步的目标、输入、产出形态与闸门。格式模块会按需缩放各步深度，此处为默认契约。

---

## Stage 1 — Break-in & core action · 破题与核心动作

**Goal.** Establish the story's core: the dramatic action (Goal + Conflict),
and for longer forms the thematic argument.

- A **dramatic action** is not "a person wants water" but "a dehydrated person in
  a desert searches for water." Goal must be urgent; conflict must oppose it
  directly. 详见 `modules/00-core-craft.md` §1。
- If the user has no concept yet, run the **ideation toolkit** in
  `modules/01-development.md` *through natural conversation* — never present the
  methodology menu to the user.

**Output:** 3–5 candidate core actions, each as `protagonist / want / conflict /
logline`.
**Gate:** `[pass]` to proceed · `[revise]` · `[review]`.

---

## Stage 2 — Synopsis draft · 梗概草稿

**Goal.** Give the user a feel for the whole story's trajectory and tone before
going deeper.

**Output by format:**
- Ultrashort: one-line concept + twist direction.
- Short: one-paragraph synopsis (100–200 字).
- Feature: one-page treatment (300–500 字) — see `templates/treatment.md`.
- Series: season synopsis + one-line per episode.

The tone of the synopsis must telegraph the tone of the film. **Revisable** in
later stages.
**Gate:** `[pass / revise]`.

---

## Stage 3 — Character & arc · 人物深度与弧光

**Goal.** No paper dolls. Build internal tension.

- Short: Want / Need / Arc + one contradiction.
- Feature / Series: Ghost → Lie → Flaw → Want → Need → choice → new normal, plus
  supporting-cast function tags (mirror / catalyst / theme / pace).

详见 `modules/00-core-craft.md` §2 与 `modules/01-development.md`。
**Gate:** `[pass / revise / review]`.

---

## Stage 4 — Backstory & world · 前史与世界观

**Goal.** Honor "a film is a cross-section of life" — the world ran long before
frame one.

**Output:** era/context · protagonist backstory (esp. the Ghost) · relationship
history · world rules (three-layer model where relevant) · **the cross-section
choice** (why start *here*). Short forms keep this lean (backstory diffuses into
dialogue, not flashback). 详见格式模块。
**Gate:** `[pass / revise]`.

---

## Stage 5 — Structure outline · 结构大纲

**Goal.** Build the skeleton, including the **opening hook**.

- Choose a methodology where the format calls for one (Save the Cat / Story Circle
  / McKee / inner-beat + style variant — `modules/02-structure.md`).
- The opening must be a piece of footage worth watching on its own — high-density
  for genre, highly stylized for art film. Flag and confirm its quality.
- Budget runtime per beat; annotate dual-track pacing (plot intensity + emotional
  intensity); plan setups/payoffs.

**Gate:** `[pass / revise / review]`.

---

## Stage 6 — Scene breakdown · 场景拆解

**Goal.** Turn the outline into visual units. Each scene gets a micro dramatic
action, an **estimated runtime**, and a **dual-track pacing tag** (plot 松/中/紧
× emotion 轻/中/重).

Check: no 3+ consecutive scenes in the same pacing state; sum of scene runtimes
≈ target runtime; at least one deliberate plot/emotion mismatch (the most
flavorful beats). Trigger a memory checkpoint when the form is long.
**Gate:** `[pass / revise / review]`.

---

## Stage 7 — Scene writing · 场景写作

**Goal.** Fill the flesh: visual writing + subtext, in **Fountain**
(`templates/fountain.md`).

- Show, don't tell. Dialogue is an iceberg. First appearance of a character gets
  a one-to-two-line physical/identity sketch.
- Plant setups naturally. Keep supporting voices distinct from the lead.
- Trigger a checkpoint each sequence (feature) / mid-episode (series).

**Gate:** `[pass / revise / review]`.

---

## Stage 7d — Shot breakdown · 分镜 / 运镜 / 调度 （direction layer）

**Goal.** Translate written scenes into a director's plan: blocking, coverage,
shot sizes, angles, movement, transitions, and editing rhythm — exported as a
**shot list** (`templates/shot-list.md` / `.csv`).

This is where the **导演** craft lives. Load `modules/direction/*`:
- `visual-language.md` — shot grammar and its motivation.
- `blocking-and-coverage.md` — staging, the 180° line, coverage, transitions, cut rhythm.
- `shot-breakdown.md` — the scene → shot-list procedure.

Not every project requires a full breakdown; offer it, and produce it on request
or when the deliverable is "shootable." For micro-drama, a lightweight per-clip
shot note is folded into the script itself.
**Gate:** `[pass / revise / review]`.

---

## Stage 8 — Script doctor · 剧本医生

**Goal.** Diagnose and polish. Run the full self-check (`modules/qa/script-doctor.md`):
logic holes, pacing (via runtime budget), on-the-nose dialogue, setup/payoff audit,
supporting-cast audit, opening-hook quality, continuity (long forms).

**Output:** diagnosis report + concrete revision suggestions + final verdict
across the four pillars (concept / character / structure / audiovisual).
**Gate:** name the part to refine, or ship.
