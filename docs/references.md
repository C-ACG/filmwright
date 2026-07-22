# Design References · 设计参考

Reviewed on **2026-07-21**. These repositories informed independent Filmwright v0.2
design; their code/prompts were not copied. Re-check current license and activity
before any future reuse.

## Story planning and memory

- [Google DeepMind Dramatron](https://github.com/google-deepmind/dramatron) —
  hierarchical `logline → entities/beats → scenes/dialogue` decomposition and
  human co-writing. Filmwright keeps human gates while adding direct/sprint modes.
- [GOAT Storytelling Agent](https://github.com/GOAT-AI-lab/GOAT-Storytelling-Agent)
  — explicit scene attributes and value turns. Filmwright's Scene Card independently
  formalizes goal, obstacle, turn, exit value, runtime, and state delta.
- [CogWriter](https://github.com/KaiyangWan/CogWriter) — planning, parallel
  candidate generation, monitoring, and revision. Filmwright limits divergence to
  high-value choices so parallel work cannot create competing canon.
- [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) — editable persistent story
  artifacts and recoverable sessions. Filmwright implements a lightweight,
  dependency-free Project State plus task Context Packs.
- [THU-KEG StoryWriter](https://github.com/THU-KEG/StoryWriter) — event relations
  and dynamic history compression. No standard license was identified during this
  review, so only the high-level research idea informed Event Graph/Context Pack
  design.
- [EdwardAThomson NovelWriter](https://github.com/EdwardAThomson/NovelWriter) —
  separate consistency/quality roles and multi-level quality tracking. No standard
  license was identified during review; treat as concept-only reference.

## Direction and generative production

- [PenShot / story-shot-agent](https://github.com/neopen/story-shot-agent) —
  structured script-to-shot planning, hierarchical memory, traceability, and retry
  behavior. Filmwright v0.2 adds canonical scene/shot IDs and separates shot intent
  from the generation packet.
- [FilmAgent](https://github.com/HITsz-TMG/FilmAgent) — production-role separation
  across screenwriting, directing, acting, and cinematography in virtual film
  production.
- [MovieAgent](https://github.com/showlab/MovieAgent) — hierarchical multi-agent
  planning for scenes/shots and long-video consistency.
- [ViMax](https://github.com/HKUDS/ViMax) — script, storyboard, reference management,
  character/scene consistency, audio, and validation in an end-to-end workflow.

The last three motivate asset/reference locks and continuity validation, not a
requirement to automate away creative approval.

## Agent reliability and evaluation

- [LangGraph](https://github.com/langchain-ai/langgraph) — durable state,
  pause/resume, human-in-the-loop, and recoverable long-running workflows.
  Filmwright adopts the state-machine concepts while keeping the Markdown core free
  of runtime dependencies.
- [Promptfoo](https://github.com/promptfoo/promptfoo) — prompt/model matrices,
  deterministic assertions, model-graded rubrics, and CI regression workflows.
- [EQ-Bench creative-writing-bench](https://github.com/EQ-bench/creative-writing-bench)
  — repeated creative tests and pairwise comparison. No standard license was
  identified during review; Filmwright uses independently written fixtures/rubrics
  and documents A/B order-bias controls.

## Principles retained

- Keep Project State visible/editable and production artifacts portable.
- Prefer structured state and event dependencies before adding a vector database.
- Use subagents for independent passes, not decorative role proliferation.
- Do not hard-code a “best current model”; publish measured compatibility.
- Preserve human approval at creative or expensive/irreversible gates.
