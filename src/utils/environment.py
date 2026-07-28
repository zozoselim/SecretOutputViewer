"""Resolve secret references through NovaVision's Environment SDK."""

import json
from typing import Dict, List, Sequence, Union

from sdks.novavision.src.base.environment import Environment


def _extract_raw_value(raw_references):
    """Unwrap SDK/Pydantic values when the runtime passes a wrapper."""

    if hasattr(raw_references, "value"):
        raw_references = raw_references.value

    if hasattr(raw_references, "model_dump"):
        dumped = raw_references.model_dump()
        if isinstance(dumped, dict) and "value" in dumped:
            raw_references = dumped["value"]

    return raw_references


def parse_secret_references(
    raw_references: Union[str, Sequence[str]],
) -> List[str]:
    """Parse the JSON string emitted by Environment Secrets Store."""

    raw_references = _extract_raw_value(raw_references)

    if isinstance(raw_references, str):
        try:
            references = json.loads(raw_references)
        except json.JSONDecodeError as error:
            raise ValueError(
                "secretReferences must be a valid JSON list string."
            ) from error
    elif isinstance(raw_references, (list, tuple)):
        references = list(raw_references)
    else:
        raise ValueError(
            "secretReferences must be a JSON list string."
        )

    if not isinstance(references, list) or not references:
        raise ValueError(
            "secretReferences must contain at least one reference."
        )

    cleaned_references: List[str] = []
    seen_references = set()

    for reference in references:
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError(
                "Secret references must be non-empty strings."
            )

        cleaned_reference = reference.strip()
        normalized_reference = cleaned_reference.lower()
        if normalized_reference in seen_references:
            raise ValueError(
                "Secret references must be unique."
            )

        seen_references.add(normalized_reference)
        cleaned_references.append(cleaned_reference)

    return cleaned_references


def resolve_secret_references(raw_references) -> Dict[str, str]:
    """Resolve values in memory without printing or returning plaintext."""

    references = parse_secret_references(raw_references)
    environment = Environment()
    resolved_values: Dict[str, str] = {}
    missing_references: List[str] = []

    for reference in references:
        value = environment.get_environment_variable(reference)

        if value is None or not str(value).strip():
            missing_references.append(reference)
            continue

        resolved_values[reference] = value

    if missing_references:
        raise RuntimeError(
            "Required secret references were not found or were empty: "
            + ", ".join(missing_references)
        )

    return resolved_values
