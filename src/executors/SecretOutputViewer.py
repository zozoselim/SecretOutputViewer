"""Decrypt and consume secret values without exposing plaintext."""

import os
import sys
from typing import Dict

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../",
    )
)

from sdks.novavision.src.base.component import Component

if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.crypto import decrypt_secret_values
    from ..utils.environment import read_transport_key
    from ..utils.response import build_response
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        PackageModel,
    )
    from components.SecretOutputViewer.src.utils.crypto import (
        decrypt_secret_values,
    )
    from components.SecretOutputViewer.src.utils.environment import (
        read_transport_key,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response,
    )


class SecretOutputViewer(Component):
    """Trusted consumer for encrypted secret payloads."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)
        self.encrypted_secrets = self.request.get_param(
            "encryptedSecrets"
        )
        self.resolved_values: Dict[str, str] = {}
        self.message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        transport_key = read_transport_key()
        self.resolved_values = decrypt_secret_values(
            self.encrypted_secrets,
            transport_key,
        )
        self.message = (
            f"{len(self.resolved_values)} secret value(s) were "
            "decrypted and consumed successfully."
        )

        return build_response(context=self)


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import Executor

    Executor(sys.argv[1]).run()
