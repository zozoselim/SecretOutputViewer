"""Consume secret references without exposing their values."""

import os
import sys
from typing import Dict


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../",
    )
)


from sdks.novavision.src.base.component import (
    Component,
)


if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.environment import (
        resolve_secret_references,
    )
    from ..utils.response import build_response
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        PackageModel,
    )
    from components.SecretOutputViewer.src.utils.environment import (
        resolve_secret_references,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response,
    )


class SecretOutputViewer(Component):
    """Resolve and consume trusted secret references."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(
            **self.request.data
        )

        self.secret_context = self.request.get_param(
            "secretContext"
        )

        self.resolved_values: Dict[
            str,
            str,
        ] = {}

        self.message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        self.resolved_values = (
            resolve_secret_references(
                self.secret_context
            )
        )

        # Gerçek downstream işlemi burada yapılır.
        #
        # Örnek:
        # docker_network = self.resolved_values[
        #     "DOCKER_NETWORK"
        # ]
        #
        # Değeri print veya output yapma.

        resolved_count = len(
            self.resolved_values
        )

        self.message = (
            f"{resolved_count} secret value was resolved "
            "and consumed successfully."
        )

        return build_response(
            context=self
        )


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import (
        Executor,
    )

    Executor(sys.argv[1]).run()