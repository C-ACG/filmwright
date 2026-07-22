# Model & Host Compatibility · 模型兼容性

Filmwright is **vendor-neutral by design**. Compatibility is an evidence claim and
must be tied to an exact model/host and eval suite.

## Capability profiles

| profile | minimum behavior | Filmwright path |
|---|---|---|
| Chat-only | follows long Markdown instructions and preserves structured text | paste orchestrator/modules; save State Delta manually |
| File-aware | reads repository/state and writes authorized artifacts | progressive loading + canonical Project State |
| Agentic | file tools, optional research, pause/resume, parallel independent QA | capability profile + Context Pack + one canon owner |
| Multimodal production | inspects image/video/audio references and outputs | AI-video packet + evidence-based visual critic |

Hosts do not behave identically: file loading, tool availability, context handling,
and structured-output reliability differ. The portable contract is shared; the
execution path adapts.

## Status vocabulary

- **Verified:** full suite meets release gates.
- **Smoke-tested:** required core cases pass, full suite not run.
- **Experimental:** tested with known material gaps.
- **Untested:** no current evidence; do not advertise compatibility.

## Current matrix (v0.2.0 source state)

No provider/model has yet been run through the published full suite. All model
compatibility remains **Untested** until reports are added. Static repository
validation is not a substitute for behavioral model evaluation.

| provider/host | exact model ID | profile | suite | status | tested date | report | known gaps |
|---|---|---|---|---|---|---|---|
| — | — | — | filmwright-core/v1 | Untested | — | — | initial matrix pending |

## Recording a result

Include model ID/version, host, reasoning/temperature/top-p, context mode, tool
permissions, suite commit/version, number of repeats, hard-case pass rate, rubric
mean/variance, latency/cost where available, and a durable report artifact. Store
the same information in `templates/run-manifest.json` for reproducible sample runs.
