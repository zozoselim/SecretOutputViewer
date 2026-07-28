"""Authenticated decryption helpers for secret payloads."""

import json
from typing import Dict

from cryptography.fernet import Fernet, InvalidToken


def decrypt_secret_values(
    encrypted_payload: str,
    transport_key: str,
) -> Dict[str, str]:
    """Decrypt and validate a secret mapping in memory."""

    if not isinstance(encrypted_payload, str) or not encrypted_payload.strip():
        raise ValueError(
            "encryptedSecrets must be a non-empty string."
        )

    try:
        cipher = Fernet(transport_key.encode("utf-8"))
        plaintext = cipher.decrypt(
            encrypted_payload.strip().encode("utf-8")
        )
    except (InvalidToken, TypeError, ValueError) as error:
        raise RuntimeError(
            "Encrypted secret payload could not be authenticated or decrypted."
        ) from error

    try:
        values = json.loads(plaintext.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "Decrypted secret payload is not valid JSON."
        ) from error

    if (
        not isinstance(values, dict)
        or not values
        or not all(
            isinstance(name, str) and isinstance(value, str)
            for name, value in values.items()
        )
    ):
        raise RuntimeError(
            "Decrypted secret payload is not a valid secret mapping."
        )

    return values
