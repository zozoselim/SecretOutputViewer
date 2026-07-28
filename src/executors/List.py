"""Resolve secret references without exposing their values."""

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
    from ..utils.response import build_response_list
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        PackageModel,
    )
    from components.SecretOutputViewer.src.utils.environment import (
        resolve_secret_references,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response_list,
    )


class List(Component):
    """Resolve received references and use secrets internally."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(
            **self.request.data
        )

        self.secret_references = self.request.get_param(
            "secretList"
        )

        self.message = (
            "Secret values were accessed successfully. "
            "No secret value was returned."
        )

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        secret_values = resolve_secret_references(
            self.secret_references
        )

        # Trusted business logic uses secret_values here.
        # Never print, log, or include it in the response.
        _resolved_secret_count = len(secret_values)

        return build_response_list(
            context=self
        )


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
