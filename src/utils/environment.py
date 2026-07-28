"""Resolve secret contexts through NovaVision's Environment SDK."""

import re
from typing import Dict, List, Mapping

from sdks.novavision.src.base.environment import Environment


_ENV_NAME_PATTERN = re.compile(
    r"[A-Za-z_][A-Za-z0-9_]*"
)


def resolve_secret_context(
    secret_context: Mapping,
) -> Dict[str, str]:
    """Resolve references for trusted internal use only."""

    if not isinstance(secret_context, Mapping):
        raise TypeError(
            "secretContext must be an object."
        )

    references = secret_context.get("references")

    if (
        not isinstance(references, list)
        or not references
    ):
        raise ValueError(
            "secretContext.references must be "
            "a non-empty list."
        )

    environment = Environment()
    resolved: Dict[str, str] = {}
    missing_references: List[str] = []

    for reference in references:
        if (
            not isinstance(reference, str)
            or not _ENV_NAME_PATTERN.fullmatch(
                reference.strip()
            )
        ):
            raise ValueError(
                "Secret references must be valid "
                "environment variable names."
            )

        cleaned_reference = reference.strip()
        secret_value = (
            environment.get_environment_variable(
                cleaned_reference
            )
        )

        if (
            secret_value is None
            or not str(secret_value).strip()
        ):
            missing_references.append(
                cleaned_reference
            )
            continue

        resolved[cleaned_reference] = secret_value

    if missing_references:
        raise RuntimeError(
            "Secret references could not be resolved: "
            + ", ".join(missing_references)
        )

    return resolved
