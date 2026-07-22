# Behavioral Evals · 行为回归

`cases.json` is a provider-neutral catalog of observable Filmwright behavior. It
tests contracts and constraints, not exact creative wording.

## What to evaluate

- mode selection and direct entry;
- trust boundary/source fidelity;
- shootable scene craft and format-aware exceptions;
- pure-anthology `season arc=no` and AI-vertical normalization branches;
- state/knowledge/prop continuity;
- canonical shot schema and runtime closure;
- Review behavior and AI-video asset/continuity packets.

## Release procedure

1. Bind the exact repository commit, model ID, host, parameters, and loaded paths in
   `templates/run-manifest.json`.
2. Run every case three times. Use each case's `hard_passes_required`; ordinary
   cases require at least 2/3 hard passes and `critical: true` cases require 3/3.
3. Apply deterministic `required`/`forbidden` checks first.
4. Grade the written `rubric` with an independent context/model where possible.
5. For creative comparisons, run both A/B and B/A order and retain human spot
   checks.
6. Record each run's required/forbidden assertion evidence, rubric dimension
   scores, per-case mean/variance, and aggregate counts in the run manifest.
7. Save raw outputs and scores under ignored `evals/results/`; publish only a
   sanitized durable report.

No model is marked compatible until this catalog (and any release-specific cases)
has actually been run and recorded in `docs/model-compatibility.md`.

Promptfoo can consume an adapter-generated configuration, but it is optional and
not a runtime dependency. Keep provider/model IDs out of the canonical cases so the
same suite can compare hosts without prompt drift.
