# ID Conventions · ID 约定

Filmwright IDs are public prompt-contract fields. Assign an ID once, keep it across
rewrites, and never recycle a deleted or superseded ID for a different object.
Canonical IDs use uppercase ASCII prefixes and three-digit zero padding unless a
row below explicitly defines another form.

## Namespace

| Kind | Canonical form | Example |
|---|---|---|
| Project | `FW-YYYYMMDD-NNN` | `FW-20260721-001` |
| Character | `CHAR-NNN` | `CHAR-001` |
| Location | `LOC-NNN` | `LOC-001` |
| Prop | `PROP-NNN` | `PROP-001` |
| Style lock | `STYLE-NNN` | `STYLE-001` |
| Wardrobe state | `WARD-NNN` | `WARD-003` |
| Makeup/damage state | `MAKEUP-NNN` | `MAKEUP-002` |
| Setup/payoff | `SETUP-NNN` | `SETUP-001` |
| Creative/canon decision | `DEC-NNN` | `DEC-001` |
| Source | `SRC-NNN` | `SRC-001` |
| Reference asset | `REF-NNN` | `REF-001` |
| Information unit | `INFO-NNN` | `INFO-004` |
| Event | `EVT-NNN` | `EVT-001` |
| Assumption | `ASM-NNN` | `ASM-001` |
| Contradiction/conflict | `CON-NNN` | `CON-001` |
| Episode | `EPNNN` | `EP012` |
| Standalone scene | `SCNNN` | `SC004` |
| Episodic scene | `EPNNN-SCNNN` | `EP012-SC004` |
| Standalone shot | `SCNNN-SHNNN` | `SC004-SH003` |
| Episodic shot | `EPNNN-SCNNN-SHNNN` | `EP012-SC004-SH003` |
| Versioned artifact | `ART-NNN/vN` | `ART-001/v2` |
| Production take | `TAKE-NNN` | `TAKE-002` |

`EP01` and similar short episode labels may appear in human-facing prose, but
machine-readable scene, shot, state, and production records use the padded
canonical form (`EP001`). A shot ID always contains its full scene ID; `SH003` and
scene-local shorthand are not valid standalone IDs. A take has its own project-wide
ID and is bound to a full `shot_id` in the production-state row.

## Validation patterns

```text
project_id    ^FW-[0-9]{8}-[0-9]{3}$
named_id      ^(CHAR|LOC|PROP|STYLE|WARD|MAKEUP|SETUP|DEC|SRC|REF|INFO|EVT|ASM|CON|TAKE)-[0-9]{3}$
episode_id    ^EP[0-9]{3}$
scene_id      ^(EP[0-9]{3}-)?SC[0-9]{3}$
shot_id       ^(EP[0-9]{3}-)?SC[0-9]{3}-SH[0-9]{3}$
artifact_id   ^ART-[0-9]{3}/v[1-9][0-9]*$
```

State revisions use `rN` (`r12`) and deltas use `rN → rN+1`; revisions are
monotonic counters, not reusable entity IDs.

## Lifecycle rules

- Preserve IDs when names, wording, or descriptions change.
- Create a new ID only for a genuinely new entity/event/decision, not a revision.
- Record replacement with `supersedes`; do not renumber downstream records.
- Prefix episodic scenes and shots with their episode ID to prevent collisions.
- Keep asset/reference/take IDs distinct: an accepted take may update state only
  through an approved State Delta.
