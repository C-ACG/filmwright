from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from scripts.validate_repo import validate_repository


ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def repository_copy() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as temporary:
        destination = Path(temporary) / "filmwright"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "results"),
        )
        yield destination


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


class RepositoryContractTests(unittest.TestCase):
    def assert_rejected(self, repository: Path, fragment: str) -> list[str]:
        errors = validate_repository(repository)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"Expected an error containing {fragment!r}; got:\n" + "\n".join(errors),
        )
        return errors

    def test_full_repository_contract(self) -> None:
        errors = validate_repository(ROOT)
        self.assertEqual([], errors, "\n" + "\n".join(errors))

    def test_entry_adapters_are_identical(self) -> None:
        self.assertEqual((ROOT / "AGENTS.md").read_bytes(), (ROOT / "CLAUDE.md").read_bytes())

    def test_example_shot_runtime_closes(self) -> None:
        path = ROOT / "examples/short-film_the-last-shift/05_scene-04_shot-list.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            total = sum(float(row["duration_s"]) for row in csv.DictReader(handle))
        self.assertEqual(40.0, total)

    def test_schema_constraint_drift_is_rejected(self) -> None:
        with repository_copy() as repository:
            path = repository / "schemas/shot-list.schema.json"
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema["properties"]["duration_s"]["exclusiveMinimum"] = -1
            schema["properties"]["movement"]["enum"].append("teleport")
            write_json(path, schema)
            errors = self.assert_rejected(repository, "property 'movement' constraints")
            self.assertTrue(any("property 'duration_s' constraints" in error for error in errors))

    def test_canonical_csv_bad_header_cannot_skip_validation(self) -> None:
        with repository_copy() as repository:
            path = repository / "templates/shot-list.csv"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("shot_id,", "legacy_shot_id,", 1), encoding="utf-8", newline="\n")
            self.assert_rejected(repository, "shot header mismatch")

    def test_canonical_csv_rejects_non_finite_duration(self) -> None:
        with repository_copy() as repository:
            path = repository / "templates/shot-list.csv"
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            duration_index = rows[0].index("duration_s")
            rows[1][duration_index] = "NaN"
            with path.open("w", encoding="utf-8", newline="") as handle:
                csv.writer(handle, lineterminator="\n").writerows(rows)
            self.assert_rejected(repository, "duration_s must be a finite number")

    def test_manifest_rejects_external_paths_cycles_and_unregistered_modules(self) -> None:
        with repository_copy() as repository:
            outside = repository.parent / "outside.md"
            outside.write_text("outside\n", encoding="utf-8", newline="\n")
            path = repository / "filmwright.manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["creative_entry"] = outside.as_posix()
            manifest["modules"][0]["depends_on"] = ["qa-script-doctor"]
            write_json(path, manifest)
            (repository / "modules/unregistered.md").write_text(
                "# Orphan\n", encoding="utf-8", newline="\n"
            )
            errors = self.assert_rejected(repository, "must be a relative repository path")
            self.assertTrue(any("module dependency cycle" in error for error in errors))
            self.assertTrue(any("unregistered module" in error for error in errors))

    def test_manifest_rejects_bad_stage_and_field_types(self) -> None:
        with repository_copy() as repository:
            path = repository / "filmwright.manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["modules"][0]["stage"] = ["imaginary-stage"]
            manifest["modules"][0]["depends_on"] = "development"
            write_json(path, manifest)
            errors = self.assert_rejected(repository, "unknown stages")
            self.assertTrue(any("depends_on must be a list" in error for error in errors))

    def test_eval_schema_rejects_bad_mode_policy_and_empty_hard_assertions(self) -> None:
        with repository_copy() as repository:
            path = repository / "evals/cases.json"
            suite = json.loads(path.read_text(encoding="utf-8"))
            suite["repeat_policy"]["critical_min_hard_passes"] = 1
            suite["cases"][0]["expected_mode"] = "telepathy"
            suite["cases"][0]["required"] = []
            write_json(path, suite)
            errors = self.assert_rejected(repository, "invalid expected_mode")
            self.assertTrue(any("hard required assertions" in error for error in errors))
            self.assertTrue(any("critical_min_hard_passes <= runs" in error for error in errors))

    def test_run_manifest_result_shape_is_enforced(self) -> None:
        with repository_copy() as repository:
            path = repository / "templates/run-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            del manifest["qa"]["suite_commit"]
            manifest["qa"]["case_results"][0]["runs"][0]["assertions"][0]["kind"] = "maybe"
            manifest["qa"]["aggregate"]["rubric_mean"] = 5
            write_json(path, manifest)
            errors = self.assert_rejected(repository, "missing required fields ['suite_commit']")
            self.assertTrue(any("kind must be required or forbidden" in error for error in errors))
            self.assertTrue(any("qa.aggregate.rubric_mean" in error for error in errors))

    def test_ci_rejects_inline_comment_unpinned_action_and_write_permission(self) -> None:
        with repository_copy() as repository:
            path = repository / ".github/workflows/quality.yml"
            text = path.read_text(encoding="utf-8")
            text = re_sub_action_sha(text, "actions/setup-python", "main # deliberately unpinned")
            text = text.replace("  contents: read\n", "  contents: read\n  issues: write\n")
            path.write_text(text, encoding="utf-8", newline="\n")
            errors = self.assert_rejected(repository, "not pinned to a full 40-character SHA")
            self.assertTrue(any("permissions must contain only" in error for error in errors))

    def test_ci_requires_triggers_commands_and_non_persistent_checkout(self) -> None:
        with repository_copy() as repository:
            path = repository / ".github/workflows/quality.yml"
            text = path.read_text(encoding="utf-8")
            text = text.replace("  pull_request:\n", "  workflow_dispatch:\n")
            text = text.replace(
                "python scripts/validate_repo.py", "python scripts/not-the-validator.py"
            )
            text = text.replace(
                "        with:\n          persist-credentials: false",
                "        env:\n          persist-credentials: false",
                1,
            )
            path.write_text(text, encoding="utf-8", newline="\n")
            errors = self.assert_rejected(repository, "must declare pull_request: exactly once")
            self.assertTrue(any("missing required run command" in error for error in errors))
            self.assertTrue(any("persist-credentials: false" in error for error in errors))

    def test_worked_example_regressions_are_rejected(self) -> None:
        with repository_copy() as repository:
            example = repository / "examples/short-film_the-last-shift"
            (example / "00_project-state.md").unlink()

            scene_map_path = example / "03_scene-map.md"
            scene_map = scene_map_path.read_text(encoding="utf-8").replace("### SC010", "## SC010", 1)
            scene_map_path.write_text(scene_map, encoding="utf-8", newline="\n")

            fountain_path = example / "04_scene-04.fountain"
            fountain = fountain_path.read_text(encoding="utf-8").replace(
                "别叫。十二岁以后，我就没爸了。", "别叫。", 1
            )
            fountain_path.write_text(fountain, encoding="utf-8", newline="\n")

            shot_path = example / "05_scene-04_shot-list.csv"
            with shot_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            cue_index = rows[0].index("dialogue_cue")
            cue_rows = [row for row in rows[1:] if row[cue_index]]
            cue_rows[0][cue_index], cue_rows[1][cue_index] = (
                cue_rows[1][cue_index],
                cue_rows[0][cue_index],
            )
            with shot_path.open("w", encoding="utf-8", newline="") as handle:
                csv.writer(handle, lineterminator="\n").writerows(rows)

            errors = self.assert_rejected(repository, "00_project-state.md is required")
            self.assertTrue(any("exactly ten ordered Scene Cards" in error for error in errors))
            self.assertTrue(any("dialogue_cue order/content" in error for error in errors))
            self.assertTrue(any("explicit father/daughter reveal line" in error for error in errors))


def re_sub_action_sha(text: str, action: str, replacement: str) -> str:
    import re

    return re.sub(
        rf"({re.escape(action)}@)[0-9a-f]{{40}}",
        rf"\g<1>{replacement}",
        text,
        count=1,
    )


if __name__ == "__main__":
    unittest.main()
