# Platform Pack Template · 平台规则包模板

> Optional, dated facts for a specific platform/region/project. This file is a
> template, not a current platform rule set. Prefer official sources and expire
> stale claims.

```yaml
schema: filmwright.platform-pack/v1
platform: ""
region: ""
as_of: YYYY-MM-DD
review_after: YYYY-MM-DD
verified_by: ""
sources:
  - title: ""
    url: ""
    published_or_updated: ""
    accessed: ""
```

## Verified constraints

```text
delivery: aspect / resolution / codec / captions / audio
episode: allowed or recommended runtime / count / file limits
text: title / description / subtitle / dialogue constraints
monetization: paywall/ad/eligibility facts
content: region-specific safety/rating/compliance requirements
rights: music/footage/likeness/brand requirements
analytics: project-specific retention/drop-off evidence, sample size, date range
```

## Authority

- Mark each item `official rule / official recommendation / project analytics /
  Filmwright heuristic`.
- If a source conflicts with the house defaults in a format module, the current
  official rule wins; project analytics may override creative heuristics.
- No source or expired pack → label the value an assumption; do not fabricate a
  platform rule.
