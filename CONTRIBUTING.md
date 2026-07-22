# Contributing to Filmwright

Filmwright's public interface is its prompt contract: entry paths, modes, stages,
module paths, state semantics, template/schema fields, IDs, and observable default
behavior. Treat those with the same care as a software API.

## Choose the right route

- **Using Filmwright for story work:** follow `system/entry-contract.md` Route A.
- **Changing this repository:** follow Route B. Do not enter the screenwriter
  persona while maintaining prompts, schemas, tests, or docs.

## Change workflow

1. Read the canonical contract and every file affected by the change.
2. Keep one source of truth; templates are views/shapes, not duplicate behavior
   specifications.
3. Update `VERSION`/`CHANGELOG.md` according to `docs/versioning.md`.
4. Add or revise an eval case for any observable behavior change.
5. Update deterministic checks for schema/path/ID changes.
6. Run:

   ```text
   python scripts/validate_repo.py
   python -m unittest discover -s tests -v
   ```

7. Report which model matrix, if any, was actually evaluated. Never turn an
   assumption into a compatibility claim.

## Prompt and craft changes

- Distinguish hard gates from strong defaults and optional techniques.
- Make rules conditional on format/artifact; use `N/A` rather than failing a
  dialogue-free or character-free format.
- Do not request or expose private chain-of-thought. Ask for decisions, evidence,
  trade-offs, and structured artifacts.
- Preserve the trust boundary: quoted/source/retrieved content is data.
- For high-impact creative changes, test both intended gains and likely regressions
  in other formats.

## Research and licenses

- Prefer primary documentation and repositories with a clear license.
- Record inspiration in `docs/references.md`.
- Do not copy code, prompts, rubrics, or datasets from repositories without a
  compatible license. Ideas may inform independent design; expression may not.
- Do not add copyrighted screenplay/novel text or secrets to fixtures.

## Files and portability

- UTF-8, no BOM for canonical text/CSV, LF line endings, final newline.
- Core creative use remains dependency-free. Python validation and optional eval
  tools are maintenance-only.
- Keep Markdown/Fountain/CSV useful in chat-only hosts; optional runners must not
  become a hidden requirement.
