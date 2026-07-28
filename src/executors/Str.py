"""Resolve one secret reference without exposing its value."""

import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../",
    )
)

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.environment import (
        resolve_secret_references,
    )
    from ..utils.response import build_response_str
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        PackageModel,
    )
    from components.SecretOutputViewer.src.utils.environment import (
        resolve_secret_references,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response_str,
    )


class Str(Component):
    """Consume one reference and resolve its secret internally."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(
            **self.request.data
        )

        self.secret_reference = self.request.get_param(
            "secretText"
        )

        self.message = (
            "Secret reference was resolved successfully. "
            "The secret value was not returned."
        )

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        secret_values = resolve_secret_references(
            [self.secret_reference]
        )

        # A trusted package can use the value here.
        # Never print it, log it, or include it in the response.
        _secret_value = secret_values[
            self.secret_reference
        ]

        return build_response_str(
            context=self
        )


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
