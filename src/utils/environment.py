"""Resolve secret references through NovaVision's Environment SDK."""

import re
from typing import Dict, Sequence

from sdks.novavision.src.base.environment import Environment


_ENV_NAME_PATTERN = re.compile(
    r"[A-Za-z_][A-Za-z0-9_]*"
)


def resolve_secret_references(
    secret_references: Sequence[str],
) -> Dict[str, str]:
    """Return secret values for trusted internal use only."""

    environment = Environment()
    resolved: Dict[str, str] = {}
    missing_references = []

    for secret_reference in secret_references:
        if (
            not isinstance(secret_reference, str)
            or not _ENV_NAME_PATTERN.fullmatch(
                secret_reference.strip()
            )
        ):
            raise ValueError(
                "Secret references must be valid "
                "environment variable names."
            )

        cleaned_reference = secret_reference.strip()
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
