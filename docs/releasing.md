# Release Guide · 发布指南

## Checklist

1. Choose SemVer impact from `docs/versioning.md`.
2. Update `VERSION`, manifest version, template schema versions, and Changelog.
3. Confirm all referenced paths/schemas exist and no legacy column names remain.
4. Run deterministic validation and unit tests.
5. Run the full behavioral eval matrix for release candidates; compare against the
   previous release and inspect variance, not only averages.
6. Human-review at least five anchors: development, scene map, screenplay,
   shot list, long-form continuity/AI-video packet.
7. Update `docs/model-compatibility.md` with exact model IDs, settings, repetitions,
   date, suite version, score, and report artifact.
8. Verify fixtures contain no secret, API key, or unlicensed source text.
9. Create an annotated `vX.Y.Z` tag and GitHub Release only after the commit under
   test is final.
10. Recreate an empty `Unreleased` section after publication.

## Recommended gates

- Deterministic CI: all pass.
- Ordinary hard behavioral cases: pass in at least 2 of 3 runs; cases marked
  `critical: true` (trust/canon/schema/production fidelity) must pass 3 of 3.
- Relevant quality dimensions: meet the suite threshold.
- Mean score regression vs prior release: no unexplained drop greater than the
  configured tolerance.
- Pairwise creative comparison: run both A/B and B/A order to reduce position bias.

Do not run secret-bearing model evals on untrusted fork workflows. Pin third-party
GitHub Actions to immutable commit SHAs before a public release.
