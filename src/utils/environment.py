"""Resolve secret references through NovaVision's Environment SDK."""

from typing import Dict, List, Sequence

from sdks.novavision.src.base.environment import Environment


def resolve_secret_references(
    references: Sequence[str],
) -> Dict[str, str]:
    """Resolve values in memory without printing or returning them."""

    if not isinstance(references, list) or not references:
        raise ValueError(
            "secretReferences must be a non-empty list."
        )

    environment = Environment()
    resolved_values: Dict[str, str] = {}
    missing_references: List[str] = []

    for reference in references:
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError(
                "Secret references must be non-empty strings."
            )

        cleaned_reference = reference.strip()
        value = environment.get_environment_variable(
            cleaned_reference
        )

        if value is None or not str(value).strip():
            missing_references.append(
                cleaned_reference
            )
            continue

        resolved_values[cleaned_reference] = value

    if missing_references:
        raise RuntimeError(
            "Required secret references were not found: "
            + ", ".join(missing_references)
        )

    return resolved_values
