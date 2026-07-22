#!/usr/bin/env python3
"""Deterministic repository contract checks; standard library only."""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote


TEXT_SUFFIXES = {".md", ".csv", ".json", ".yml", ".yaml", ".fountain", ".py"}
CANONICAL_SHOT_FIELDS = [
    "shot_id",
    "scene_id",
    "size",
    "angle",
    "movement",
    "lens_focus",
    "subject_action",
    "dialogue_cue",
    "light_intent",
    "sound_cue",
    "duration_s",
    "transition_out",
    "notes",
]
SHOT_ID_RE = re.compile(r"^(?:EP\d{3}-)?SC\d{3}-SH(\d{3})$")
SCENE_ID_RE = re.compile(r"^(?:EP\d{3}-)?SC\d{3}$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

MANIFEST_SCHEMA = "filmwright.manifest/v1"
RUN_MANIFEST_SCHEMA = "filmwright.run-manifest/v1"
EVAL_SCHEMA = "filmwright.evals/v1"
EVAL_SUITE = "filmwright-core/v1"
ALLOWED_STAGES = {
    "all",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "7d",
    "8",
    "batch",
    "final",
    "high-stakes",
    "review",
    "release",
}
ALLOWED_EVAL_MODES = {"guided", "sprint", "direct", "review"}
ALLOWED_EVAL_CATEGORIES = {
    "routing",
    "direct-entry",
    "trust-boundary",
    "scene-craft",
    "continuity",
    "schema",
    "format",
    "review",
    "ai-video",
    "adaptation",
    "format-exception",
}

EXPECTED_SHOT_PROPERTIES = {
    "shot_id": {
        "type": "string",
        "pattern": r"^(EP[0-9]{3}-)?SC[0-9]{3}-SH[0-9]{3}$",
    },
    "scene_id": {
        "type": "string",
        "pattern": r"^(EP[0-9]{3}-)?SC[0-9]{3}$",
    },
    "size": {"enum": ["EWS", "WS", "MLS", "MS", "MCU", "CU", "ECU", "INSERT"]},
    "angle": {"enum": ["eye", "high", "low", "OTS", "POV", "dutch", "top"]},
    "movement": {
        "enum": [
            "static",
            "pan",
            "tilt",
            "dolly_in",
            "dolly_out",
            "track",
            "crane",
            "handheld",
            "steadicam",
            "rack_focus",
            "whip_pan",
        ]
    },
    "lens_focus": {"type": "string", "minLength": 1},
    "subject_action": {"type": "string", "minLength": 1},
    "dialogue_cue": {"type": "string"},
    "light_intent": {"type": "string"},
    "sound_cue": {"type": "string"},
    "duration_s": {"type": "number", "exclusiveMinimum": 0},
    "transition_out": {
        "enum": [
            "cut",
            "match_cut",
            "J_cut",
            "L_cut",
            "dissolve",
            "fade",
            "smash_cut",
            "whip_cut",
        ]
    },
    "notes": {"type": "string"},
}

EXPECTED_SHOT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": CANONICAL_SHOT_FIELDS,
    "properties": EXPECTED_SHOT_PROPERTIES,
}


def _display(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    root_resolved = root.resolve()
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            path.resolve().relative_to(root_resolved)
        except (OSError, RuntimeError, ValueError):
            # Registered paths are reported by the manifest validator. Never read
            # through an escaping symlink merely to perform encoding checks.
            continue
        relative = path.relative_to(root).as_posix()
        if relative.startswith("evals/results/") or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
            "VERSION",
            "LICENSE",
            ".gitattributes",
            ".editorconfig",
            ".gitignore",
        }:
            files.append(path)
    return sorted(files)


def _read_utf8(root: Path, path: Path, errors: list[str]) -> str | None:
    data = path.read_bytes()
    label = _display(root, path)
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{label}: UTF-8 BOM is not allowed in canonical files")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{label}: invalid UTF-8 ({exc})")
        return None


def _validate_text_encoding(root: Path, errors: list[str]) -> None:
    for path in _text_files(root):
        text = _read_utf8(root, path, errors)
        if text is None:
            continue
        label = _display(root, path)
        if "\r" in text:
            errors.append(f"{label}: CR/CRLF found; canonical line ending is LF")
        if text and not text.endswith("\n"):
            errors.append(f"{label}: missing final newline")


def _load_json(root: Path, path: Path, errors: list[str]) -> object | None:
    text = _read_utf8(root, path, errors)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{_display(root, path)}: invalid JSON ({exc})")
        return None


def _validate_json_files(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*.json")):
        relative = path.relative_to(root).as_posix()
        if ".git" not in path.parts and not relative.startswith("evals/results/"):
            _load_json(root, path, errors)


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _resolve_manifest_file(
    root: Path,
    value: object,
    label: str,
    errors: list[str],
    required_directory: str | None = None,
) -> Path | None:
    if not isinstance(value, str) or not value or value != value.strip():
        errors.append(f"filmwright.manifest.json: {label} must be a non-empty path string")
        return None
    if "\\" in value:
        errors.append(f"filmwright.manifest.json: {label} must use portable '/' separators: {value!r}")
        return None

    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if posix.is_absolute() or windows.is_absolute() or ".." in posix.parts:
        errors.append(f"filmwright.manifest.json: {label} must be a relative repository path: {value!r}")
        return None
    if required_directory is not None and (
        not posix.parts or posix.parts[0] != required_directory
    ):
        errors.append(
            f"filmwright.manifest.json: {label} must live under {required_directory}/: {value!r}"
        )
        return None

    candidate = root.joinpath(*posix.parts)
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        errors.append(f"filmwright.manifest.json: {label} path missing: {value!r}")
        return None
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(
            f"filmwright.manifest.json: {label} resolves outside repository (external symlink/path): {value!r}"
        )
        return None
    if not resolved.is_file():
        errors.append(f"filmwright.manifest.json: {label} path is not a file: {value!r}")
        return None
    return candidate


def _inventory(root: Path, directory: str, suffix: str | None = None) -> set[str]:
    base = root / directory
    if not base.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in base.rglob("*")
        if path.is_file() and (suffix is None or path.suffix == suffix)
    }


def _report_inventory_difference(
    label: str, registered: set[str], discovered: set[str], errors: list[str]
) -> None:
    for value in sorted(discovered - registered):
        errors.append(f"filmwright.manifest.json: unregistered {label}: {value}")
    for value in sorted(registered - discovered):
        errors.append(f"filmwright.manifest.json: registered {label} is not discoverable: {value}")


def _validate_dependency_graph(graph: dict[str, list[str]], errors: list[str]) -> None:
    states: dict[str, int] = {}
    stack: list[str] = []
    reported: set[tuple[str, ...]] = set()

    def visit(module_id: str) -> None:
        state = states.get(module_id, 0)
        if state == 2:
            return
        if state == 1:
            start = stack.index(module_id)
            cycle = tuple(stack[start:] + [module_id])
            if cycle not in reported:
                reported.add(cycle)
                errors.append(
                    "filmwright.manifest.json: module dependency cycle: " + " -> ".join(cycle)
                )
            return
        states[module_id] = 1
        stack.append(module_id)
        for dependency in graph.get(module_id, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        states[module_id] = 2

    for module_id in graph:
        visit(module_id)


def _validate_version_and_manifest(root: Path, errors: list[str]) -> None:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(version):
        errors.append(f"VERSION: expected SemVer, found {version!r}")

    manifest_path = root / "filmwright.manifest.json"
    manifest = _load_json(root, manifest_path, errors)
    if not isinstance(manifest, dict):
        errors.append("filmwright.manifest.json: root must be an object")
        return
    if manifest.get("$schema") != MANIFEST_SCHEMA:
        errors.append(f"filmwright.manifest.json: $schema must be {MANIFEST_SCHEMA!r}")
    if manifest.get("version") != version:
        errors.append("filmwright.manifest.json: version must match VERSION")

    for key in ("entry_contract", "creative_entry", "pipeline", "canonical_state_template"):
        _resolve_manifest_file(root, manifest.get(key), key, errors)

    schemas = manifest.get("canonical_schemas")
    registered_schemas: list[str] = []
    if not isinstance(schemas, dict) or not schemas:
        errors.append("filmwright.manifest.json: canonical_schemas must be a non-empty object")
    else:
        for name, value in schemas.items():
            if not isinstance(name, str) or not name:
                errors.append("filmwright.manifest.json: schema names must be non-empty strings")
            if _resolve_manifest_file(root, value, f"schema {name}", errors, "schemas"):
                registered_schemas.append(value)
    if len(registered_schemas) != len(set(registered_schemas)):
        errors.append("filmwright.manifest.json: schema paths must be unique")
    _report_inventory_difference(
        "schema",
        set(registered_schemas),
        _inventory(root, "schemas", ".json"),
        errors,
    )

    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        errors.append("filmwright.manifest.json: modules must be a non-empty list")
        modules = []
    module_ids: list[str] = []
    module_paths: list[str] = []
    graph: dict[str, list[str]] = {}
    valid_items: list[tuple[int, dict[str, object]]] = []
    module_required = {"id", "version", "path", "stage", "depends_on", "scope"}
    for index, item in enumerate(modules):
        if not isinstance(item, dict):
            errors.append(f"filmwright.manifest.json: module {index} must be an object")
            continue
        missing = module_required - set(item)
        if missing:
            errors.append(f"filmwright.manifest.json: module {index} missing {sorted(missing)}")
        valid_items.append((index, item))
        module_id = item.get("id")
        if not isinstance(module_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", module_id):
            errors.append(f"filmwright.manifest.json: module {index} has invalid id {module_id!r}")
        else:
            module_ids.append(module_id)

    if len(module_ids) != len(set(module_ids)):
        errors.append("filmwright.manifest.json: module IDs must be unique")
    known_ids = set(module_ids)

    for index, item in valid_items:
        module_id = item.get("id")
        label = module_id if isinstance(module_id, str) else str(index)
        path_value = item.get("path")
        if _resolve_manifest_file(root, path_value, f"module {label}", errors, "modules"):
            if isinstance(path_value, str):
                module_paths.append(path_value)
        if item.get("version") != version:
            errors.append(f"filmwright.manifest.json: module {label} version mismatch")

        stages = item.get("stage")
        if not isinstance(stages, list) or not stages:
            errors.append(f"filmwright.manifest.json: module {label} stage must be a non-empty list")
        elif any(not isinstance(stage, str) for stage in stages):
            errors.append(f"filmwright.manifest.json: module {label} stages must be strings")
        else:
            if len(stages) != len(set(stages)):
                errors.append(f"filmwright.manifest.json: module {label} stages must be unique")
            unknown = sorted(set(stages) - ALLOWED_STAGES)
            if unknown:
                errors.append(f"filmwright.manifest.json: module {label} has unknown stages {unknown}")
            if "all" in stages and len(stages) != 1:
                errors.append(f"filmwright.manifest.json: module {label} stage 'all' must stand alone")

        dependencies = item.get("depends_on")
        valid_dependencies: list[str] = []
        if not isinstance(dependencies, list):
            errors.append(f"filmwright.manifest.json: module {label} depends_on must be a list")
        elif any(not isinstance(dependency, str) or not dependency for dependency in dependencies):
            errors.append(
                f"filmwright.manifest.json: module {label} dependencies must be non-empty strings"
            )
        else:
            valid_dependencies = dependencies
            if len(dependencies) != len(set(dependencies)):
                errors.append(f"filmwright.manifest.json: module {label} dependencies must be unique")
            for dependency in dependencies:
                if dependency not in known_ids:
                    errors.append(
                        f"filmwright.manifest.json: module {label} has unknown dependency {dependency}"
                    )
        if isinstance(module_id, str) and module_id in known_ids:
            graph[module_id] = valid_dependencies

        scope = item.get("scope")
        if not isinstance(scope, str) or not scope.strip():
            errors.append(f"filmwright.manifest.json: module {label} scope must be non-empty text")

    if len(module_paths) != len(set(module_paths)):
        errors.append("filmwright.manifest.json: module paths must be unique")
    _report_inventory_difference(
        "module",
        set(module_paths),
        _inventory(root, "modules", ".md"),
        errors,
    )
    _validate_dependency_graph(graph, errors)

    templates = manifest.get("templates")
    registered_templates: list[str] = []
    if not isinstance(templates, list) or not templates:
        errors.append("filmwright.manifest.json: templates must be a non-empty list")
    else:
        for index, value in enumerate(templates):
            if _resolve_manifest_file(root, value, f"template {index}", errors, "templates"):
                if isinstance(value, str):
                    registered_templates.append(value)
    if len(registered_templates) != len(set(registered_templates)):
        errors.append("filmwright.manifest.json: template paths must be unique")
    _report_inventory_difference(
        "template",
        set(registered_templates),
        _inventory(root, "templates"),
        errors,
    )

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        errors.append(f"CHANGELOG.md: missing release section for {version}")

    _validate_run_manifest(root, version, errors)


def _missing_fields(
    value: dict[str, object], required: set[str], label: str, errors: list[str]
) -> set[str]:
    missing = required - set(value)
    if missing:
        errors.append(f"{label}: missing required fields {sorted(missing)}")
    return missing


def _validate_string_list(
    value: object,
    label: str,
    errors: list[str],
    *,
    allow_empty: bool,
) -> list[str] | None:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a list" if allow_empty else "a non-empty list"
        errors.append(f"{label}: must be {qualifier} of non-empty strings")
        return None
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label}: entries must be non-empty strings")
        return None
    if len(value) != len(set(value)):
        errors.append(f"{label}: entries must be unique")
    return value


def _validate_repeat_policy(
    value: object, label: str, errors: list[str]
) -> dict[str, int] | None:
    required = {"runs", "default_min_hard_passes", "critical_min_hard_passes"}
    if not isinstance(value, dict):
        errors.append(f"{label}: must be an object")
        return None
    missing = _missing_fields(value, required, label, errors)
    if missing:
        return None
    if set(value) - required:
        errors.append(f"{label}: unexpected fields {sorted(set(value) - required)}")
    if any(not _is_int(value.get(field)) for field in required):
        errors.append(f"{label}: all policy values must be integers")
        return None
    policy = {field: value[field] for field in required}
    runs = policy["runs"]
    default = policy["default_min_hard_passes"]
    critical = policy["critical_min_hard_passes"]
    if runs < 1 or not 1 <= default <= runs or not default <= critical <= runs:
        errors.append(
            f"{label}: require 1 <= default_min_hard_passes <= "
            "critical_min_hard_passes <= runs"
        )
    return policy


def _validate_run_manifest(root: Path, version: str, errors: list[str]) -> None:
    label = "templates/run-manifest.json"
    run_manifest = _load_json(root, root / "templates/run-manifest.json", errors)
    if not isinstance(run_manifest, dict):
        errors.append(f"{label}: root must be an object")
        return

    required = {
        "schema",
        "filmwright_version",
        "repository_commit",
        "project_id",
        "state_revision",
        "workflow_mode",
        "artifact_ids",
        "host",
        "model",
        "prompt",
        "inputs",
        "outputs",
        "started_at",
        "completed_at",
        "usage",
        "qa",
    }
    _missing_fields(run_manifest, required, label, errors)
    if run_manifest.get("schema") != RUN_MANIFEST_SCHEMA:
        errors.append(f"{label}: schema must be {RUN_MANIFEST_SCHEMA!r}")
    if run_manifest.get("filmwright_version") != version:
        errors.append(f"{label}: filmwright_version must match VERSION")

    commit = run_manifest.get("repository_commit")
    if not isinstance(commit, str) or (commit and not re.fullmatch(r"[0-9a-f]{40}", commit)):
        errors.append(f"{label}: repository_commit must be empty or a 40-character Git SHA")
    if not isinstance(run_manifest.get("project_id"), str):
        errors.append(f"{label}: project_id must be a string")
    revision = run_manifest.get("state_revision")
    if not _is_int(revision) or revision < 0:
        errors.append(f"{label}: state_revision must be a non-negative integer")
    if run_manifest.get("workflow_mode") not in ALLOWED_EVAL_MODES:
        errors.append(f"{label}: workflow_mode must be one of {sorted(ALLOWED_EVAL_MODES)}")
    _validate_string_list(
        run_manifest.get("artifact_ids"), f"{label}: artifact_ids", errors, allow_empty=True
    )

    host = run_manifest.get("host")
    if not isinstance(host, dict):
        errors.append(f"{label}: host must be an object")
    else:
        _missing_fields(host, {"name", "version", "capability_profile"}, f"{label}: host", errors)
        for field in ("name", "version"):
            if not isinstance(host.get(field), str):
                errors.append(f"{label}: host.{field} must be a string")
        _validate_string_list(
            host.get("capability_profile"),
            f"{label}: host.capability_profile",
            errors,
            allow_empty=True,
        )

    model = run_manifest.get("model")
    if not isinstance(model, dict):
        errors.append(f"{label}: model must be an object")
    else:
        _missing_fields(
            model,
            {"provider", "model_id", "reasoning_or_temperature", "other_parameters"},
            f"{label}: model",
            errors,
        )
        for field in ("provider", "model_id", "reasoning_or_temperature"):
            if not isinstance(model.get(field), str):
                errors.append(f"{label}: model.{field} must be a string")
        if not isinstance(model.get("other_parameters"), dict):
            errors.append(f"{label}: model.other_parameters must be an object")

    prompt = run_manifest.get("prompt")
    if not isinstance(prompt, dict):
        errors.append(f"{label}: prompt must be an object")
    else:
        _missing_fields(
            prompt,
            {"manifest_version", "loaded_paths", "content_hashes"},
            f"{label}: prompt",
            errors,
        )
        if prompt.get("manifest_version") != version:
            errors.append(f"{label}: prompt.manifest_version must match VERSION")
        _validate_string_list(
            prompt.get("loaded_paths"),
            f"{label}: prompt.loaded_paths",
            errors,
            allow_empty=True,
        )
        hashes = prompt.get("content_hashes")
        if not isinstance(hashes, dict) or any(
            not isinstance(path, str)
            or not path
            or not isinstance(digest, str)
            or not digest
            for path, digest in (hashes.items() if isinstance(hashes, dict) else [])
        ):
            errors.append(f"{label}: prompt.content_hashes must map paths to non-empty hashes")

    for field in ("inputs", "outputs"):
        value = run_manifest.get(field)
        if not isinstance(value, list) or any(not isinstance(item, (str, dict)) for item in value):
            errors.append(f"{label}: {field} must be a list of path strings or descriptor objects")
    timestamp_re = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
    for field in ("started_at", "completed_at"):
        value = run_manifest.get(field)
        if not isinstance(value, str) or (value and not timestamp_re.fullmatch(value)):
            errors.append(f"{label}: {field} must be empty or an ISO-8601 timestamp with timezone")

    usage = run_manifest.get("usage")
    if not isinstance(usage, dict):
        errors.append(f"{label}: usage must be an object")
    else:
        _missing_fields(usage, {"tokens", "latency_ms", "cost", "currency"}, f"{label}: usage", errors)
        for field in ("tokens", "latency_ms"):
            value = usage.get(field)
            if value is not None and (not _is_int(value) or value < 0):
                errors.append(f"{label}: usage.{field} must be null or a non-negative integer")
        cost = usage.get("cost")
        if cost is not None and (not _is_number(cost) or cost < 0):
            errors.append(f"{label}: usage.cost must be null or a non-negative finite number")
        if usage.get("currency") is not None and not isinstance(usage.get("currency"), str):
            errors.append(f"{label}: usage.currency must be null or a string")

    suite = _load_json(root, root / "evals/cases.json", errors)
    suite_policy = suite.get("repeat_policy") if isinstance(suite, dict) else None
    case_catalog = {
        case.get("id"): case
        for case in (suite.get("cases", []) if isinstance(suite, dict) else [])
        if isinstance(case, dict) and isinstance(case.get("id"), str)
    }
    qa = run_manifest.get("qa")
    if not isinstance(qa, dict):
        errors.append(f"{label}: qa must be an object")
        return
    qa_required = {"suite", "suite_commit", "repeat_policy", "case_results", "aggregate", "report"}
    _missing_fields(qa, qa_required, f"{label}: qa", errors)
    if not isinstance(qa.get("suite"), str) or qa.get("suite") not in {"", EVAL_SUITE}:
        errors.append(f"{label}: qa.suite must be empty or {EVAL_SUITE!r}")
    suite_commit = qa.get("suite_commit")
    if not isinstance(suite_commit, str) or (
        suite_commit and not re.fullmatch(r"[0-9a-f]{40}", suite_commit)
    ):
        errors.append(f"{label}: qa.suite_commit must be empty or a 40-character Git SHA")
    qa_policy = _validate_repeat_policy(qa.get("repeat_policy"), f"{label}: qa.repeat_policy", errors)
    if isinstance(suite_policy, dict) and qa_policy is not None and qa_policy != suite_policy:
        errors.append(f"{label}: qa.repeat_policy must match evals/cases.json")

    case_results = qa.get("case_results")
    if not isinstance(case_results, list) or not case_results:
        errors.append(f"{label}: qa.case_results must contain a result-shape example or results")
    else:
        seen_case_ids: set[str] = set()
        for index, result in enumerate(case_results):
            result_label = f"{label}: qa.case_results[{index}]"
            if not isinstance(result, dict):
                errors.append(f"{result_label} must be an object")
                continue
            _missing_fields(
                result,
                {
                    "case_id",
                    "critical",
                    "hard_passes_required",
                    "hard_pass_count",
                    "case_pass",
                    "runs",
                    "rubric_mean",
                    "rubric_variance",
                },
                result_label,
                errors,
            )
            case_id = result.get("case_id")
            if not isinstance(case_id, str):
                errors.append(f"{result_label}.case_id must be a string")
                case_id = ""
            elif case_id:
                if case_id in seen_case_ids:
                    errors.append(f"{result_label}.case_id is duplicated: {case_id}")
                seen_case_ids.add(case_id)
                if case_id not in case_catalog:
                    errors.append(f"{result_label}.case_id is not in evals/cases.json: {case_id}")
            catalog_case = case_catalog.get(case_id)
            critical = result.get("critical")
            if not isinstance(critical, bool):
                errors.append(f"{result_label}.critical must be boolean")
            hard_required = result.get("hard_passes_required")
            policy_runs = qa_policy["runs"] if qa_policy else 0
            if not _is_int(hard_required) or not 1 <= hard_required <= max(policy_runs, 1):
                errors.append(f"{result_label}.hard_passes_required is outside repeat policy")
            if isinstance(catalog_case, dict):
                if critical != catalog_case.get("critical"):
                    errors.append(f"{result_label}.critical must match eval catalog")
                if hard_required != catalog_case.get("hard_passes_required"):
                    errors.append(f"{result_label}.hard_passes_required must match eval catalog")

            hard_count = result.get("hard_pass_count")
            if hard_count is not None and (
                not _is_int(hard_count) or hard_count < 0 or hard_count > max(policy_runs, 1)
            ):
                errors.append(f"{result_label}.hard_pass_count must be null or within repeat policy")
            if result.get("case_pass") is not None and not isinstance(result.get("case_pass"), bool):
                errors.append(f"{result_label}.case_pass must be null or boolean")

            runs = result.get("runs")
            if not isinstance(runs, list) or not runs:
                errors.append(f"{result_label}.runs must be a non-empty list")
                runs = []
            if case_id and qa_policy and len(runs) != qa_policy["runs"]:
                errors.append(f"{result_label}.runs must contain exactly {qa_policy['runs']} runs")
            run_numbers: list[int] = []
            for run_index, run in enumerate(runs):
                run_label = f"{result_label}.runs[{run_index}]"
                if not isinstance(run, dict):
                    errors.append(f"{run_label} must be an object")
                    continue
                _missing_fields(
                    run,
                    {
                        "run",
                        "hard_pass",
                        "assertions",
                        "rubric_scores",
                        "rubric_mean",
                        "latency_ms",
                        "output_path",
                    },
                    run_label,
                    errors,
                )
                run_number = run.get("run")
                if not _is_int(run_number) or run_number < 1 or (
                    qa_policy and run_number > qa_policy["runs"]
                ):
                    errors.append(f"{run_label}.run must be within repeat policy")
                else:
                    run_numbers.append(run_number)
                if run.get("hard_pass") is not None and not isinstance(run.get("hard_pass"), bool):
                    errors.append(f"{run_label}.hard_pass must be null or boolean")
                assertions = run.get("assertions")
                if not isinstance(assertions, list) or not assertions:
                    errors.append(f"{run_label}.assertions must be a non-empty list")
                else:
                    for assertion_index, assertion in enumerate(assertions):
                        assertion_label = f"{run_label}.assertions[{assertion_index}]"
                        if not isinstance(assertion, dict):
                            errors.append(f"{assertion_label} must be an object")
                            continue
                        _missing_fields(
                            assertion, {"kind", "text", "pass", "evidence"}, assertion_label, errors
                        )
                        kind = assertion.get("kind")
                        text = assertion.get("text")
                        if not isinstance(kind, str) or kind not in {"required", "forbidden"}:
                            errors.append(f"{assertion_label}.kind must be required or forbidden")
                        if not isinstance(text, str):
                            errors.append(f"{assertion_label}.text must be a string")
                        if assertion.get("pass") is not None and not isinstance(
                            assertion.get("pass"), bool
                        ):
                            errors.append(f"{assertion_label}.pass must be null or boolean")
                        if not isinstance(assertion.get("evidence"), str):
                            errors.append(f"{assertion_label}.evidence must be a string")
                        if (
                            isinstance(catalog_case, dict)
                            and kind in {"required", "forbidden"}
                            and isinstance(text, str)
                            and text
                        ):
                            if text not in catalog_case.get(kind, []):
                                errors.append(f"{assertion_label}.text is not a catalog {kind} assertion")
                rubric_scores = run.get("rubric_scores")
                if not isinstance(rubric_scores, dict) or any(
                    not isinstance(dimension, str)
                    or not dimension
                    or not _is_number(score)
                    or not 0 <= score <= 4
                    for dimension, score in (
                        rubric_scores.items() if isinstance(rubric_scores, dict) else []
                    )
                ):
                    errors.append(f"{run_label}.rubric_scores must map dimensions to scores from 0 to 4")
                elif isinstance(catalog_case, dict):
                    unknown_dimensions = set(rubric_scores) - set(
                        catalog_case.get("rubric_dimensions", [])
                    )
                    if unknown_dimensions:
                        errors.append(
                            f"{run_label}.rubric_scores has unknown dimensions {sorted(unknown_dimensions)}"
                        )
                rubric_mean = run.get("rubric_mean")
                if rubric_mean is not None and (
                    not _is_number(rubric_mean) or not 0 <= rubric_mean <= 4
                ):
                    errors.append(f"{run_label}.rubric_mean must be null or between 0 and 4")
                latency = run.get("latency_ms")
                if latency is not None and (not _is_int(latency) or latency < 0):
                    errors.append(f"{run_label}.latency_ms must be null or a non-negative integer")
                if not isinstance(run.get("output_path"), str):
                    errors.append(f"{run_label}.output_path must be a string")
            if len(run_numbers) != len(set(run_numbers)):
                errors.append(f"{result_label}.run numbers must be unique")
            for field, maximum in (("rubric_mean", 4), ("rubric_variance", None)):
                value = result.get(field)
                if value is not None and (
                    not _is_number(value) or value < 0 or (maximum is not None and value > maximum)
                ):
                    errors.append(f"{result_label}.{field} has an invalid value")

    aggregate = qa.get("aggregate")
    aggregate_fields = {
        "cases_passed",
        "cases_total",
        "critical_cases_passed",
        "critical_cases_total",
        "rubric_mean",
        "rubric_variance",
    }
    if not isinstance(aggregate, dict):
        errors.append(f"{label}: qa.aggregate must be an object")
    else:
        _missing_fields(aggregate, aggregate_fields, f"{label}: qa.aggregate", errors)
        for field in (
            "cases_passed",
            "cases_total",
            "critical_cases_passed",
            "critical_cases_total",
        ):
            value = aggregate.get(field)
            if value is not None and (not _is_int(value) or value < 0):
                errors.append(f"{label}: qa.aggregate.{field} must be null or non-negative integer")
        for field, maximum in (("rubric_mean", 4), ("rubric_variance", None)):
            value = aggregate.get(field)
            if value is not None and (
                not _is_number(value) or value < 0 or (maximum is not None and value > maximum)
            ):
                errors.append(f"{label}: qa.aggregate.{field} has an invalid value")
    if not isinstance(qa.get("report"), str):
        errors.append(f"{label}: qa.report must be a string")


def _validate_entry_adapters(root: Path, errors: list[str]) -> None:
    agents = (root / "AGENTS.md").read_bytes()
    claude = (root / "CLAUDE.md").read_bytes()
    if agents != claude:
        errors.append("AGENTS.md and CLAUDE.md must remain identical thin adapters")
    contract = "system/entry-contract.md"
    if contract not in agents.decode("utf-8"):
        errors.append("AGENTS.md: canonical entry contract is not referenced")


def _validate_markdown_links(root: Path, errors: list[str]) -> None:
    root_resolved = root.resolve()
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            candidate = (path.parent / unquote(target)).resolve()
            try:
                candidate.relative_to(root_resolved)
            except ValueError:
                errors.append(f"{_display(root, path)}: local link escapes repository: {raw_target}")
                continue
            if not candidate.exists():
                errors.append(f"{_display(root, path)}: broken local link: {raw_target}")


def _validate_shot_schema(schema: object, errors: list[str]) -> bool:
    label = "schemas/shot-list.schema.json"
    start = len(errors)
    if not isinstance(schema, dict):
        errors.append(f"{label}: root must be an object")
        return False
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{label}: $schema must select JSON Schema draft 2020-12")
    schema_id = schema.get("$id")
    if not isinstance(schema_id, str) or not schema_id.startswith("https://"):
        errors.append(f"{label}: $id must be an HTTPS URI")
    if not isinstance(schema.get("title"), str) or not schema.get("title", "").strip():
        errors.append(f"{label}: title must be non-empty text")
    if schema.get("type") != "object":
        errors.append(f"{label}: type must be 'object'")
    if schema.get("additionalProperties") is not False:
        errors.append(f"{label}: additionalProperties must be false")
    if schema.get("required") != CANONICAL_SHOT_FIELDS:
        errors.append(f"{label}: required fields must match canonical CSV order")

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        errors.append(f"{label}: properties must be an object")
        return False
    missing = set(EXPECTED_SHOT_PROPERTIES) - set(properties)
    extra = set(properties) - set(EXPECTED_SHOT_PROPERTIES)
    if missing:
        errors.append(f"{label}: missing properties {sorted(missing)}")
    if extra:
        errors.append(f"{label}: unexpected properties {sorted(extra)}")
    for field, expected in EXPECTED_SHOT_PROPERTIES.items():
        actual = properties.get(field)
        if actual != expected:
            errors.append(
                f"{label}: property {field!r} constraints must equal canonical {expected!r}"
            )
    return len(errors) == start


def _validate_shot_instance(
    instance: dict[str, object], schema: dict[str, object], label: str, errors: list[str]
) -> None:
    required = schema.get("required")
    properties = schema.get("properties")
    if not isinstance(required, list) or not isinstance(properties, dict):
        return
    for field in required:
        if isinstance(field, str) and field not in instance:
            errors.append(f"{label}: missing required field {field!r}")
    if schema.get("additionalProperties") is False:
        extra = set(instance) - set(properties)
        if extra:
            errors.append(f"{label}: unexpected fields {sorted(extra)}")

    for field, rules in properties.items():
        if field not in instance or not isinstance(rules, dict):
            continue
        value = instance[field]
        expected_type = rules.get("type")
        type_ok = True
        if expected_type == "string":
            type_ok = isinstance(value, str)
        elif expected_type == "number":
            type_ok = _is_number(value)
        if not type_ok:
            errors.append(f"{label}: {field} must be a finite {expected_type}")
            continue
        enum = rules.get("enum")
        if isinstance(enum, list) and value not in enum:
            errors.append(f"{label}: {field} value {value!r} is outside canonical enum")
        pattern = rules.get("pattern")
        if isinstance(pattern, str) and isinstance(value, str) and re.search(pattern, value) is None:
            errors.append(f"{label}: {field} value {value!r} does not match schema pattern")
        minimum_length = rules.get("minLength")
        if _is_int(minimum_length) and isinstance(value, str) and len(value) < minimum_length:
            errors.append(f"{label}: {field} must contain at least {minimum_length} character(s)")
        exclusive_minimum = rules.get("exclusiveMinimum")
        if _is_number(exclusive_minimum) and _is_number(value) and value <= exclusive_minimum:
            errors.append(f"{label}: {field} must be greater than {exclusive_minimum}")


def _validate_shot_csv(
    root: Path, path: Path, schema: dict[str, object], errors: list[str]
) -> None:
    label = _display(root, path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CANONICAL_SHOT_FIELDS:
            errors.append(
                f"{label}: shot header mismatch; expected {','.join(CANONICAL_SHOT_FIELDS)}"
            )
            return
        seen: set[str] = set()
        last_number: dict[str, int] = {}
        row_count = 0
        for line_number, row in enumerate(reader, start=2):
            row_count += 1
            if None in row:
                errors.append(f"{label}:{line_number}: extra CSV fields")
                row.pop(None, None)
            instance: dict[str, object] = dict(row)
            raw_duration = instance.get("duration_s")
            if isinstance(raw_duration, str):
                try:
                    instance["duration_s"] = float(raw_duration)
                except ValueError:
                    pass
            row_label = f"{label}:{line_number}"
            _validate_shot_instance(instance, schema, row_label, errors)

            shot_id = instance.get("shot_id")
            scene_id = instance.get("scene_id")
            match = SHOT_ID_RE.fullmatch(shot_id) if isinstance(shot_id, str) else None
            if not match:
                # The schema error contains the malformed value; this message makes
                # the cross-row ID contract explicit as well.
                errors.append(f"{row_label}: invalid shot_id {shot_id!r}")
            if not isinstance(scene_id, str) or not SCENE_ID_RE.fullmatch(scene_id):
                errors.append(f"{row_label}: invalid scene_id {scene_id!r}")
            if match and isinstance(scene_id, str) and shot_id.rsplit("-SH", 1)[0] != scene_id:
                errors.append(f"{label}:{line_number}: shot_id does not belong to scene_id")
            if isinstance(shot_id, str) and shot_id in seen:
                errors.append(f"{label}:{line_number}: duplicate shot_id {shot_id}")
            if isinstance(shot_id, str):
                seen.add(shot_id)
            if match and isinstance(scene_id, str):
                number = int(match.group(1))
                expected = last_number.get(scene_id, 0) + 1
                if number != expected:
                    errors.append(
                        f"{label}:{line_number}: expected next shot number {expected:03d}, found {number:03d}"
                    )
                last_number[scene_id] = number
        if row_count == 0:
            errors.append(f"{label}: shot list must contain at least one row")


def _validate_shot_contract(root: Path, errors: list[str]) -> None:
    schema = _load_json(root, root / "schemas/shot-list.schema.json", errors)
    schema_valid = _validate_shot_schema(schema, errors)
    row_schema = schema if schema_valid and isinstance(schema, dict) else EXPECTED_SHOT_SCHEMA

    canonical_paths = {
        root / "templates/shot-list.csv",
        root / "examples/short-film_the-last-shift/05_scene-04_shot-list.csv",
    }
    validated: set[Path] = set()
    for path in sorted(canonical_paths):
        if not path.is_file():
            errors.append(f"{_display(root, path)}: canonical shot CSV is missing")
            continue
        _validate_shot_csv(root, path, row_schema, errors)
        validated.add(path.resolve())
    for path in sorted(root.rglob("*.csv")):
        if ".git" in path.parts:
            continue
        if path.resolve() in validated:
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            first = next(csv.reader(handle), [])
        shot_filename = path.name == "shot-list.csv" or path.name.endswith("_shot-list.csv")
        resembles_shot_schema = len(set(first) & set(CANONICAL_SHOT_FIELDS)) >= 2
        if shot_filename or resembles_shot_schema:
            _validate_shot_csv(root, path, row_schema, errors)

    markdown = (root / "templates/shot-list.md").read_text(encoding="utf-8")
    expected_header = "| " + " | ".join(CANONICAL_SHOT_FIELDS) + " |"
    if expected_header not in markdown:
        errors.append("templates/shot-list.md: canonical header not found")

    module = (root / "modules/direction/shot-breakdown.md").read_text(encoding="utf-8")
    for field in CANONICAL_SHOT_FIELDS:
        if f"`{field}`" not in module:
            errors.append(f"modules/direction/shot-breakdown.md: missing canonical field `{field}`")


def _validate_example(root: Path, errors: list[str]) -> None:
    example = root / "examples/short-film_the-last-shift"
    state_path = example / "00_project-state.md"
    project_state = ""
    if not state_path.is_file():
        errors.append("example: 00_project-state.md is required as the canonical root state")
    else:
        project_state = state_path.read_text(encoding="utf-8")

    shot_path = example / "05_scene-04_shot-list.csv"
    total = 0.0
    shot_dialogue: list[str] = []
    with shot_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                duration = float(row.get("duration_s", ""))
            except (TypeError, ValueError):
                errors.append("example: SC004 shot duration is not numeric")
            else:
                if math.isfinite(duration):
                    total += duration
                else:
                    errors.append("example: SC004 shot duration must be finite")
            cue = row.get("dialogue_cue")
            if isinstance(cue, str) and cue.strip():
                shot_dialogue.append(cue.strip())
    scene_map = (example / "03_scene-map.md").read_text(encoding="utf-8")
    match = re.search(r"\| SC004 \| (\d+) \|", scene_map)
    if not match:
        errors.append("example scene map: SC004 runtime not found")
    else:
        target = float(match.group(1))
        if abs(total - target) > max(1.0, target * 0.10):
            errors.append(f"example: SC004 shot total {total:g}s does not match {target:g}s target")

    scene_rows = re.findall(r"\| SC(\d{3}) \| (\d+) \|", scene_map)
    scene_ids = [int(scene) for scene, _ in scene_rows]
    if scene_ids != list(range(1, len(scene_ids) + 1)):
        errors.append("example scene map: scene IDs must be unique and sequential")
    if sum(int(seconds) for _, seconds in scene_rows) != 480:
        errors.append("example scene map: scene runtimes must sum to 480s")
    scene_card_ids = re.findall(r"(?m)^### SC(\d{3})\s*$", scene_map)
    expected_scene_cards = [f"{number:03d}" for number in range(1, 11)]
    if scene_card_ids != expected_scene_cards:
        errors.append("example scene map: expected exactly ten ordered Scene Cards SC001-SC010")

    beat_sheet = (example / "02_beat-sheet.md").read_text(encoding="utf-8")
    beat_seconds = 0
    for line in beat_sheet.splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 3 and parts[0].isdigit() and re.fullmatch(r"\d+:\d{2}", parts[2]):
            minutes, seconds = (int(value) for value in parts[2].split(":"))
            beat_seconds += minutes * 60 + seconds
    if beat_seconds != 480:
        errors.append(f"example beat sheet: beat runtimes sum to {beat_seconds}s, expected 480s")

    fountain = (example / "04_scene-04.fountain").read_text(encoding="utf-8")
    if re.search(r"(?m)^====$", fountain):
        errors.append("example Fountain: redundant title-page break found")
    for phrase in ("It always is", "The name lands", "Like it might break"):
        if phrase.lower() in fountain.lower():
            errors.append(f"example Fountain: non-photographable legacy phrase remains: {phrase}")
    if "INT. CONVENIENCE STORE - NIGHT" not in fountain:
        errors.append("example Fountain: scene heading not found")

    fountain_dialogue: list[str] = []
    fountain_lines = fountain.splitlines()
    for index, line in enumerate(fountain_lines):
        speaker = line.strip()
        if speaker not in {"MEILING", "KAI"}:
            continue
        dialogue_index = index + 1
        while dialogue_index < len(fountain_lines):
            candidate = fountain_lines[dialogue_index].strip()
            if not candidate or (candidate.startswith("(") and candidate.endswith(")")):
                dialogue_index += 1
                continue
            fountain_dialogue.append(f"{speaker}: {candidate}")
            break
    if shot_dialogue != fountain_dialogue:
        errors.append(
            "example: shot-list dialogue_cue order/content must exactly follow the SC004 Fountain dialogue"
        )

    reveal_line = "别叫。十二岁以后，我就没爸了。"
    if reveal_line not in fountain:
        errors.append("example Fountain: INFO-001 requires the explicit father/daughter reveal line")
    if not any(reveal_line in cue for cue in shot_dialogue):
        errors.append("example shot list: explicit INFO-001 reveal cue is missing")
    if "INFO-001 reveal" not in scene_map or "father/daughter truth" not in scene_map:
        errors.append("example scene map: SC004 must explicitly record the INFO-001 reveal")
    if project_state and not (
        re.search(r"\| INFO-001 \| Kai is Meiling's father \|", project_state)
        and "INFO-001 public and acknowledged" in project_state
    ):
        errors.append("example project state: INFO-001 truth and SC004 acknowledgment must be explicit")

    for legacy in (
        example / "03_scene-04.fountain",
        example / "04_scene-04_shot-list.csv",
    ):
        if legacy.exists():
            errors.append(f"example: legacy artifact should be removed: {legacy.name}")


def _validate_evals(root: Path, errors: list[str]) -> None:
    path = root / "evals/cases.json"
    suite = _load_json(root, path, errors)
    if not isinstance(suite, dict):
        errors.append("evals/cases.json: root must be an object")
        return
    top_level = {"schema", "suite", "filmwright_version", "repeat_policy", "cases"}
    missing_top = top_level - set(suite)
    if missing_top:
        errors.append(f"evals/cases.json: missing top-level fields {sorted(missing_top)}")
    if set(suite) - top_level:
        errors.append(f"evals/cases.json: unexpected top-level fields {sorted(set(suite) - top_level)}")
    if suite.get("schema") != EVAL_SCHEMA:
        errors.append(f"evals/cases.json: schema must be {EVAL_SCHEMA!r}")
    if suite.get("suite") != EVAL_SUITE:
        errors.append(f"evals/cases.json: suite must be {EVAL_SUITE!r}")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if suite.get("filmwright_version") != version:
        errors.append("evals/cases.json: filmwright_version must match VERSION")
    policy = _validate_repeat_policy(
        suite.get("repeat_policy"), "evals/cases.json: repeat_policy", errors
    )
    cases = suite.get("cases")
    if not isinstance(cases, list) or len(cases) < 10:
        errors.append("evals/cases.json: at least 10 cases are required")
        return
    seen: set[str] = set()
    categories: set[str] = set()
    required = {
        "id",
        "category",
        "critical",
        "hard_passes_required",
        "rubric_dimensions",
        "input",
        "expected_mode",
        "required",
        "forbidden",
        "rubric",
    }
    fixture_anchors = {
        "DIRECT-01": ("Scene Card", "锁定页面"),
        "QA-01": ("内景 客厅 夜", "不要替换原文"),
        "PROD-01": ("前镜 SC004-SH009", "后镜 SC004-SH011"),
        "ADAPT-01": ("原文：", "母亲没有获救"),
    }
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"evals/cases.json: case {index} must be an object")
            continue
        missing = required - set(case)
        if missing:
            errors.append(f"evals/cases.json: case {index} missing {sorted(missing)}")
        if set(case) - required:
            errors.append(f"evals/cases.json: case {index} has unexpected fields {sorted(set(case) - required)}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{2}", case_id):
            errors.append(f"evals/cases.json: case {index} has invalid id")
        elif case_id in seen:
            errors.append(f"evals/cases.json: duplicate case id {case_id}")
        else:
            seen.add(case_id)

        category = case.get("category")
        if category not in ALLOWED_EVAL_CATEGORIES:
            errors.append(
                f"evals/cases.json: case {case_id or index} has invalid category {category!r}"
            )
        elif isinstance(category, str):
            categories.add(category)
        if case.get("expected_mode") not in ALLOWED_EVAL_MODES:
            errors.append(
                f"evals/cases.json: case {case_id or index} has invalid expected_mode "
                f"{case.get('expected_mode')!r}"
            )
        for field in ("input", "rubric"):
            if not isinstance(case.get(field), str) or not case.get(field, "").strip():
                errors.append(f"evals/cases.json: case {case_id or index} {field} must be non-empty text")

        critical = case.get("critical")
        if not isinstance(critical, bool):
            errors.append(f"evals/cases.json: case {case_id or index} critical must be boolean")
        hard_required = case.get("hard_passes_required")
        if not _is_int(hard_required):
            errors.append(
                f"evals/cases.json: case {case_id or index} hard_passes_required must be integer"
            )
        elif policy is not None and isinstance(critical, bool):
            expected = policy[
                "critical_min_hard_passes" if critical else "default_min_hard_passes"
            ]
            if hard_required != expected:
                errors.append(
                    f"evals/cases.json: case {case_id or index} hard_passes_required "
                    f"must be {expected} for critical={critical}"
                )

        dimensions = _validate_string_list(
            case.get("rubric_dimensions"),
            f"evals/cases.json: case {case_id or index} rubric_dimensions",
            errors,
            allow_empty=False,
        )
        if dimensions is not None and any(
            not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", dimension)
            for dimension in dimensions
        ):
            errors.append(
                f"evals/cases.json: case {case_id or index} rubric dimensions must use kebab-case IDs"
            )

        assertion_lists: dict[str, list[str]] = {}
        for field in ("required", "forbidden"):
            assertions = _validate_string_list(
                case.get(field),
                f"evals/cases.json: case {case_id or index} hard {field} assertions",
                errors,
                allow_empty=False,
            )
            if assertions is not None:
                assertion_lists[field] = assertions
        if set(assertion_lists.get("required", [])) & set(assertion_lists.get("forbidden", [])):
            errors.append(
                f"evals/cases.json: case {case_id or index} assertion cannot be both required and forbidden"
            )

        if isinstance(case_id, str) and case_id in fixture_anchors and isinstance(
            case.get("input"), str
        ):
            for anchor in fixture_anchors[case_id]:
                if anchor not in case["input"]:
                    errors.append(
                        f"evals/cases.json: case {case_id} is missing scoreable fixture anchor {anchor!r}"
                    )

    missing_categories = ALLOWED_EVAL_CATEGORIES - categories
    if missing_categories:
        errors.append(f"evals/cases.json: missing coverage categories {sorted(missing_categories)}")


def _strip_yaml_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, character in enumerate(line):
        if quote == '"':
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue
        if quote == "'":
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index]
    return line


def _yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _workflow_step_bounds(
    lines: list[tuple[int, int, str]], line_index: int
) -> tuple[int, int, int] | None:
    _, line_indent, line_content = lines[line_index]
    if line_content.startswith("-"):
        step_start = line_index
        step_indent = line_indent
    else:
        step_start = -1
        step_indent = -1
        for candidate in range(line_index - 1, -1, -1):
            _, indent, content = lines[candidate]
            if indent < line_indent and content.startswith("-"):
                step_start = candidate
                step_indent = indent
                break
        if step_start < 0:
            return None
    has_steps_parent = False
    for candidate in range(step_start - 1, -1, -1):
        _, indent, content = lines[candidate]
        if indent == step_indent - 2:
            has_steps_parent = content == "steps:"
            break
        if indent < step_indent - 2:
            break
    if not has_steps_parent:
        return None
    step_end = len(lines)
    for candidate in range(step_start + 1, len(lines)):
        _, indent, content = lines[candidate]
        if indent == step_indent and content.startswith("-"):
            step_end = candidate
            break
        if indent < step_indent:
            step_end = candidate
            break
    return step_start, step_end, step_indent


def _validate_ci(root: Path, errors: list[str]) -> None:
    path = root / ".github/workflows/quality.yml"
    text = path.read_text(encoding="utf-8")
    label = ".github/workflows/quality.yml"
    lines: list[tuple[int, int, str]] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        clean = _strip_yaml_comment(raw).rstrip()
        if not clean.strip():
            continue
        prefix = clean[: len(clean) - len(clean.lstrip())]
        if "\t" in prefix:
            errors.append(f"{label}:{line_number}: YAML indentation must not use tabs")
        lines.append((line_number, len(prefix.expandtabs(8)), clean.lstrip()))

    if any(re.fullmatch(r"(?:-\s*)?pull_request_target\s*:.*", content) for _, _, content in lines):
        errors.append(".github/workflows/quality.yml: pull_request_target is not allowed")

    permission_indices = [
        index for index, (_, _, content) in enumerate(lines) if content == "permissions:"
    ]
    if len(permission_indices) != 1:
        errors.append(f"{label}: exactly one permissions block is required")
    else:
        permission_index = permission_indices[0]
        _, permission_indent, _ = lines[permission_index]
        if permission_indent != 0:
            errors.append(f"{label}: permissions must be workflow-level")
        permission_children: list[tuple[int, str]] = []
        for _, indent, content in lines[permission_index + 1 :]:
            if indent <= permission_indent:
                break
            permission_children.append((indent, content))
        if permission_children != [(permission_indent + 2, "contents: read")]:
            errors.append(f"{label}: permissions must contain only 'contents: read'")

    on_indices = [index for index, (_, indent, content) in enumerate(lines) if indent == 0 and content == "on:"]
    if len(on_indices) != 1:
        errors.append(f"{label}: exactly one top-level on: block is required")
    else:
        on_index = on_indices[0]
        trigger_names: list[str] = []
        for _, indent, content in lines[on_index + 1 :]:
            if indent == 0:
                break
            if indent == 2:
                match = re.fullmatch(r"([A-Za-z_]+)\s*:.*", content)
                if match:
                    trigger_names.append(match.group(1))
        for trigger in ("push", "pull_request"):
            if trigger_names.count(trigger) != 1:
                errors.append(f"{label}: on: must declare {trigger}: exactly once")

    uses_entries: list[tuple[int, int, int, str]] = []
    run_values: set[str] = set()
    for index, (line_number, indent, content) in enumerate(lines):
        uses_match = re.fullmatch(r"(?:-\s*)?uses\s*:\s*(.+)", content)
        if uses_match:
            uses_entries.append((index, line_number, indent, _yaml_scalar(uses_match.group(1))))
            bounds = _workflow_step_bounds(lines, index)
            if bounds is None or (
                index != bounds[0] and indent != bounds[2] + 2
            ):
                errors.append(f"{label}:{line_number}: uses must be a direct workflow-step field")
        elif re.search(r"(?:^|\s)uses\s*:", content):
            errors.append(f"{label}:{line_number}: malformed or empty uses value")
        run_match = re.fullmatch(r"(?:-\s*)?run\s*:\s*(.+)", content)
        if run_match:
            bounds = _workflow_step_bounds(lines, index)
            if bounds is None or (
                index != bounds[0] and indent != bounds[2] + 2
            ):
                errors.append(f"{label}:{line_number}: run must be a direct workflow-step field")
            else:
                run_values.add(re.sub(r"\s+", " ", _yaml_scalar(run_match.group(1))).strip())

    if not uses_entries:
        errors.append(f"{label}: no actions found")
    pinned_action_re = re.compile(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?@[0-9a-f]{40}"
    )
    action_values = [value for _, _, _, value in uses_entries]
    for _, line_number, _, value in uses_entries:
        if not pinned_action_re.fullmatch(value):
            errors.append(f"{label}:{line_number}: action is not pinned to a full 40-character SHA: {value}")
    for action in ("actions/checkout@", "actions/setup-python@"):
        if sum(value.startswith(action) for value in action_values) != 1:
            errors.append(f"{label}: exactly one pinned {action[:-1]} step is required")

    required_runs = {
        "python scripts/validate_repo.py",
        "python -m unittest discover -s tests -v",
    }
    for command in sorted(required_runs - run_values):
        errors.append(f"{label}: missing required run command: {command}")

    for line_index, line_number, uses_indent, value in uses_entries:
        if not value.startswith("actions/checkout@"):
            continue
        bounds = _workflow_step_bounds(lines, line_index)
        if bounds is None:
            continue
        step_start, step_end, step_indent = bounds
        with_indices = [
            index
            for index in range(step_start, step_end)
            if lines[index][1] == step_indent + 2 and lines[index][2] == "with:"
        ]
        persist_values: list[str] = []
        if len(with_indices) == 1:
            with_index = with_indices[0]
            with_indent = lines[with_index][1]
            for _, indent, content in lines[with_index + 1 : step_end]:
                if indent <= with_indent:
                    break
                match = re.fullmatch(r"persist-credentials\s*:\s*(.+)", content)
                if match and indent == with_indent + 2:
                    persist_values.append(_yaml_scalar(match.group(1)).lower())
        if persist_values != ["false"]:
            errors.append(
                f"{label}:{line_number}: checkout step must set persist-credentials: false exactly once"
            )


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    _validate_text_encoding(root, errors)
    _validate_json_files(root, errors)
    _validate_version_and_manifest(root, errors)
    _validate_entry_adapters(root, errors)
    _validate_markdown_links(root, errors)
    _validate_shot_contract(root, errors)
    _validate_example(root, errors)
    _validate_evals(root, errors)
    _validate_ci(root, errors)
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    if errors:
        print(f"Filmwright validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Filmwright validation passed: encoding, links, manifest, schemas, examples, and eval catalog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
