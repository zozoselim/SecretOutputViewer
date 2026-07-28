"""Secret-reference helpers for Secret Output Viewer."""

from typing import Any, Dict, List, Mapping

from sdks.novavision.src.base.environment import (
    Environment,
)


def parse_secret_references(
    secret_context: Mapping[str, Any],
) -> List[str]:
    """Read and validate secret references from safe context."""

    if not isinstance(secret_context, Mapping):
        raise ValueError(
            "secretContext must be an object."
        )

    references = secret_context.get(
        "references"
    )

    if not isinstance(references, list):
        raise ValueError(
            "secretContext.references must be a list."
        )

    if not references:
        raise ValueError(
            "secretContext contains no secret references."
        )

    cleaned_references: List[str] = []
    seen_references = set()

    for reference in references:
        if not isinstance(reference, str):
            raise ValueError(
                "Secret references must be strings."
            )

        cleaned_reference = reference.strip()

        if not cleaned_reference:
            raise ValueError(
                "Secret references cannot be empty."
            )

        if cleaned_reference in seen_references:
            raise ValueError(
                "Secret references must be unique."
            )

        seen_references.add(
            cleaned_reference
        )

        cleaned_references.append(
            cleaned_reference
        )

    return cleaned_references


def resolve_secret_references(
    secret_context: Mapping[str, Any],
) -> Dict[str, str]:
    """
    Resolve referenced secrets through NovaVision's Environment SDK.

    Secret values remain in memory and are never printed or returned.
    """

    references = parse_secret_references(
        secret_context
    )

    environment = Environment()

    resolved_values: Dict[str, str] = {}
    missing_references: List[str] = []

    for reference in references:
        value = environment.get_environment_variable(
            reference
        )

        if value is None or not str(value).strip():
            missing_references.append(
                reference
            )
            continue

        resolved_values[reference] = value

    if missing_references:
        raise RuntimeError(
            "Required secret references were not found: "
            + ", ".join(missing_references)
        )

    return resolved_values


def resolve_secret_context(
    secret_context: Mapping[str, Any],
) -> Dict[str, str]:
    """Compatibility wrapper for existing tests and consumers."""

    return resolve_secret_references(
        secret_context
    )