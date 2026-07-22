# Template · Context Pack · 场景上下文包

> Minimal, dependency-complete context assembled for one next unit. It is generated
> from Project State/Event Graph and discarded after the unit; it is not canon.

```text
STATE HEAD + PROVENANCE
  project_id / root revision / root artifact or hash:
  compiled_at:
  subrecords used:
    subrecord_id / status / depends_on IDs+revisions /
    validated_through_revision / content hash:
  rejected stale/unregistered sources:

TARGET
  Scene/episode/shot ID:
  requested artifact:
  Scene Card / generation-unit contract:

LOCKED BRIEF (relevant subset only)
  format/runtime/tone/production constraints:
  must keep / must avoid:

RELEVANT CANON
  character identity/state/voice:
  who knows what:
  location/prop/wardrobe/injury/time state:
  relationships:

CAUSAL WINDOW
  immediate incoming event(s):
  required outgoing state:
  active setup/payoff IDs touched here:

TEXT EVIDENCE
  approved lines/pages/scenes that must be matched:
  source anchors/citations if adapting:

EXCLUSIONS
  unrelated history intentionally omitted:
  unresolved assumptions not to canonize:

OUTPUT + QA
  format/schema:
  hard gates and acceptance tests:
```

Compile only from the named root revision and subrecords that are registered,
approved/locked, and current against every declared dependency. A stale,
unregistered, or dependency-mismatched subrecord is a blocker—not context. Preserve
this provenance header with the generated artifact so the pack can be audited.

If a dependency cannot be represented without loading large source material, cite
the exact source anchor and load that bounded passage. More context is not
automatically better; missing a dependency is worse than using a compact pack.
