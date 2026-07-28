"""NovaVision environment helper for encrypted secret transport."""

from sdks.novavision.src.base.environment import Environment


TRANSPORT_KEY_VARIABLE = "NOVAVISION_SECRET_TRANSPORT_KEY"


def read_transport_key() -> str:
    """Read the shared Fernet key without printing it."""

    environment = Environment()
    value = environment.get_environment_variable(
        TRANSPORT_KEY_VARIABLE
    )

    if value is None or not str(value).strip():
        raise RuntimeError(
            f"{TRANSPORT_KEY_VARIABLE} was not found or was empty."
        )

    return str(value).strip()
