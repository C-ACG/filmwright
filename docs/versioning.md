# Versioning · 版本策略

Filmwright uses [Semantic Versioning](https://semver.org/) for its **prompt
contract**, not only for executable code.

## Public contract

- entry files and module paths/loading order;
- workflow modes, stages, gates, and direct-entry behavior;
- Project State, checkpoint, Scene Card, Event Graph, and ledger semantics;
- template and CSV/JSON field names, ID formats, and required values;
- default format routing and observable output behavior.

## Version increments

- **Major:** remove/rename required paths or fields; change stage/mode semantics or
  defaults incompatibly; invalidate saved state without a migration.
- **Minor:** add a compatible mode, module, format, optional field, capability, or
  stronger behavior covered by migration notes/evals.
- **Patch:** wording, links, examples, or rubrics that preserve the intended public
  behavior and pass regression checks.

During `0.x`, minor releases may contain contract migrations, but they must be
called out in `CHANGELOG.md`. Publish `1.0.0` only after the contract is stable and
the same full eval suite has been verified on at least three major model families.

## Prompt compatibility

“Works on any LLM” is not a test result. Use the status vocabulary in
`docs/model-compatibility.md`: `Verified`, `Smoke-tested`, `Experimental`, or
`Untested`.

## Release artifacts

Every release should bind together:

- exact Git tag and `VERSION`;
- Changelog entry/migration notes;
- `filmwright.manifest.json` and schema versions;
- deterministic validator/test result;
- model eval suite/report IDs and exact model configurations;
- optional `run-manifest` for reproducible sample runs.
