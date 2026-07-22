# Format · Series · 剧集（多集）

> N stories that compose one larger story. Two-layer structure, budgeted arc,
> staged world-reveal, continuity management. Minimum format dependency: `00`;
> task routes add development/structure only when needed.

## Configure first · 先确认配置
```
Total episodes N · per-episode runtime · per-episode structure (four-part /
STC-compressed / Story Circle / inner-beat) · series type · season arc (yes/no) ·
world complexity (simple / layered / needs release schedule)
```

| Type 类型 | Episode independence | Season continuity |
|---|---|---|
| Pure anthology 纯单元剧 | 100% | 0–10% |
| Anthology + hidden line 单元+暗线 | 70–80% | 20–30% |
| Semi-serial 半连续剧 | 40–60% | 40–60% |
| Strong serial 强连续剧 | 10–20% | 80–90% |

When episode-good and season-arc conflict, **episode-good wins**.

## Series vs feature
- With `season arc = yes`, arc is **budgeted** across N episodes—early episodes
  cannot change the character so much that the back half has nowhere to go.
- With layered world mystery, release surface rules early, operating logic mid, and
  underlying truth at finale; know that finale reveal before writing episode 1.
- With `season arc = no`, each episode stands alone. Keep only recurring entity,
  setting, tone, and publicly-known-information continuity that the Project Card
  actually requires; mark season reveal/arc/hidden-line fields `N/A`.

## Two-layer structure
**Layer 1 — episode** (proportional, any runtime):
```
Cold open / hook  — before the title; the key hook position. Ep1's open builds
                    world + character + genre/editorial promise; add a season seed
                    only when season arc = yes.
Setup ~15%        — this episode's normal + inciting incident
Development ~40%  — escalate (≥2 turns); episode B-story; diffuse season-line seeds
                    only when season arc = yes
Climax ~25%       — episode's peak; decisive choice/turn; Lie expression is optional
                    and applies only to the configured character/season arc
Resolution + act-out ~20% — this episode's new normal; serial forms hook the next,
                    pure anthology may close locally without a plot handoff
```
**Layer 2 — season arc** (only when `season arc = yes`; four phases by proportion):
```
Setup (first 25%)     — surface rules; Want + Lie established; relationship net; seed
Development (25–65%)  — escalate; operating logic revealed; false changes; weave
Crisis (65–85%)       — season all-is-lost; face Ghost & Lie; key relationship breaks
Climax & close (last 15%) — underlying truth; season-level choice; arc complete; finale
```
Proportional mapping (8/10/12/16/24 ep) is in the planning step; phases scale to N.

## Budgeted arc · 弧光预算
Plan each episode's *change quota*. First 25% of episodes: cumulative progress
≤15%. At least one false change + retreat (40–60%). 65–85% is the acceleration
zone. Not every episode needs an arc event. Pure anthology can skip the budget and
keep only character-state tracking. Track with the arc-budget table.

## World-information release schedule · 信息释放时间表
```
Layer | Content | Release (by proportion) | How
surface rules  | basic operation     | first 10–15% | direct show
operating logic | why the world is so | 40–55%       | investigation/discovery
underlying truth | ultimate truth     | last 20%     | climax reveal
setup payoffs   | details re-meant    | last 1–2 ep  | "so that's why" moment
```
Each layer needs 1–2 episodes of planting; reveal through action, not narration;
each reveal re-colors known information; max one new layer per episode.

## Continuity management (most important) · 连续性管理
After every episode, merge the State Delta into `templates/project-state.md`, then
refresh four tracking views (templates in `series-bible.md`):
A. character state · B. hidden-line progress · C. plant/payoff register · D.
publicly-known-information list. Before writing a new episode, read the tables. On
conflict, fix the new episode, not locked old ones. **Checkpoint each episode**
(`00-core-craft.md` §7). Project State—not a checkpoint or view—is the single
source of truth.

## Conditional elements

Every series requires episode-level setup/payoff and continuity appropriate to its
configuration. Only `season arc = yes` requires multi-range foreshadowing,
cross-episode micro-arcs, 1–3 hidden lines with explicit start/reveal episodes, and
a season-level subplot weave. Pure anthology may mark all of those `N/A`; do not
manufacture a finale payoff for a configuration that explicitly rejects one.

## Inter-episode pacing · 集间节奏
No 3+ consecutive episodes of one tonal type (setup / light / tense / breath /
pivot / pressure / collapse / dark-night / counter / climax). A tense/pressure
episode is followed by ≥1 breath or light episode; a breath episode is not a dead
episode (it deepens relationships and advances B-plot); mid-season (40–60%) suits a
pivot that redirects the back half.

## Workflow — two phases
**Phase 1 (once, may iterate): season plan + episode outlines.**
- *Season plan:* config · season premise and editorial promise; when
  `season arc = yes`, add one-page season synopsis, protagonist season arc + Lie,
  layered-world release schedule, arc budget, and hidden-line plan; otherwise mark
  these `N/A` and define episode independence plus recurring continuity locks.
- *Episode outlines (the most critical step — pull the whole season through before
  writing any episode):* per episode, `logline / core dramatic action / tonal type
  / timed inner structure / episode setup-payoff / recurring continuity /
  inter-episode links`. When `season arc = yes`, also include arc spend,
  hidden-line, layered-world release, and season subplot connections. Self-check
  every map for hooks, pacing wave, episode integrity, natural act-outs, and runtime
  sums; check four-phase arc, arc budget, layered release, running subplots, and
  season foreshadow only when that branch applies.
**Phase 2: per-episode pipeline.** Stages 2 and 4 reduce to "confirm
against the outline." Cold open per episode; continuity audit and checkpoint at
stage 8.

## Traps
skipping the episode-outline map · sacrificing episode quality for the arc · info
released too fast · arc budget out of control · continuity errors · forced
act-outs · same structure every episode · too many running subplots · one-line
outlines · drifting from the outline without updating later episodes · no runtime
estimate · consecutive high-intensity episodes · forgotten payoffs · supporting
roles that vanish when not needed · tracks always in sync.
