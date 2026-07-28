"""Parse and resolve runtime secret references."""

import json
import re
from typing import Dict, List

from sdks.novavision.src.base.environment import Environment


_ENV_NAME_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _unwrap_value(raw_value):
    """Handle strings, SDK models and raw output dictionaries."""

    if raw_value is None:
        return None

    if hasattr(raw_value, "value"):
        return _unwrap_value(raw_value.value)

    if hasattr(raw_value, "model_dump"):
        dumped = raw_value.model_dump()
        return _unwrap_value(dumped)

    if hasattr(raw_value, "dict"):
        dumped = raw_value.dict()
        return _unwrap_value(dumped)

    if isinstance(raw_value, dict):
        if "value" in raw_value:
            return _unwrap_value(raw_value["value"])
        if "secretReferences" in raw_value:
            return _unwrap_value(raw_value["secretReferences"])

    return raw_value


def parse_secret_references(raw_value) -> List[str]:
    """Return validated environment-variable names from the input payload."""

    raw_value = _unwrap_value(raw_value)

    if isinstance(raw_value, str):
        text = raw_value.strip()
        if not text:
            raise ValueError("secretReferences is empty.")

        try:
            decoded = json.loads(text)
        except json.JSONDecodeError:
            # Accept a single plain environment-variable name defensively.
            decoded = [text]

        return parse_secret_references(decoded)

    if isinstance(raw_value, (list, tuple)):
        if not raw_value:
            raise ValueError("secretReferences contains no references.")

        references: List[str] = []
        seen = set()

        for item in raw_value:
            item = _unwrap_value(item)
            if not isinstance(item, str):
                raise ValueError("Every secret reference must be a string.")

            reference = item.strip()
            if not _ENV_NAME_PATTERN.fullmatch(reference):
                raise ValueError(
                    f"Invalid environment-variable reference: {reference!r}."
                )

            normalized = reference.lower()
            if normalized in seen:
                continue

            seen.add(normalized)
            references.append(reference)

        return references

    raise ValueError(
        "secretReferences must be a JSON list string or a list of names."
    )


def resolve_secret_references(raw_value) -> Dict[str, str]:
    """Read referenced values in memory without returning plaintext."""

    references = parse_secret_references(raw_value)
    environment = Environment()
    resolved: Dict[str, str] = {}
    missing: List[str] = []

    for reference in references:
        value = environment.get_environment_variable(reference)
        if value is None or not str(value).strip():
            missing.append(reference)
        else:
            resolved[reference] = value

    if missing:
        raise RuntimeError(
            "Environment variable(s) were not found or were empty: "
            + ", ".join(missing)
        )

    return resolved
