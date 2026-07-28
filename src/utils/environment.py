"""Resolve environment-variable references without exposing their values."""

import json
import re
from typing import Dict, List, Sequence, Union

from sdks.novavision.src.base.environment import Environment


_ENV_NAME_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _unwrap_value(raw_value):
    """Extract values from SDK models and raw port dictionaries."""

    if raw_value is None:
        return None

    if hasattr(raw_value, "value"):
        return _unwrap_value(raw_value.value)

    if hasattr(raw_value, "model_dump"):
        return _unwrap_value(raw_value.model_dump())

    if hasattr(raw_value, "dict"):
        return _unwrap_value(raw_value.dict())

    if isinstance(raw_value, dict):
        if "value" in raw_value:
            return _unwrap_value(raw_value["value"])
        if "secretReferences" in raw_value:
            return _unwrap_value(raw_value["secretReferences"])

    return raw_value


def parse_secret_references(
    raw_value: Union[str, Sequence[str]],
) -> List[str]:
    """Convert the incoming string/list into validated variable names."""

    raw_value = _unwrap_value(raw_value)

    if isinstance(raw_value, str):
        text = raw_value.strip()
        if not text:
            raise ValueError("secretReferences is empty.")

        try:
            decoded = json.loads(text)
        except json.JSONDecodeError:
            decoded = [text]

        return parse_secret_references(decoded)

    if not isinstance(raw_value, (list, tuple)) or not raw_value:
        raise ValueError(
            "secretReferences must contain at least one variable name."
        )

    references: List[str] = []
    seen = set()

    for item in raw_value:
        item = _unwrap_value(item)

        if not isinstance(item, str):
            raise ValueError(
                "Every environment-variable reference must be a string."
            )

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


def resolve_secret_references(raw_value) -> Dict[str, str]:
    """Read values from the runtime and retain them only in memory."""

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
