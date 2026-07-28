"""Resolve secret references and use values without exposing them."""

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
    from ..utils.environment import (
        resolve_secret_context,
    )
    from ..utils.response import build_response
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        PackageModel,
    )
    from components.SecretOutputViewer.src.utils.environment import (
        resolve_secret_context,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response,
    )


class SecretReferenceConsumer(Component):
    """Use resolved secret values only inside trusted logic."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(
            **self.request.data
        )

        self.secret_context = self.request.get_param(
            "secretContext"
        )

        self.message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        secret_values: Dict[str, str] = (
            resolve_secret_context(
                self.secret_context
            )
        )

        # Real integration code uses secret_values here.
        # Never print, log, or return the dictionary.
        _resolved_secret_count = len(secret_values)

        self.message = (
            "Secret values were resolved and are ready "
            "for trusted internal use."
        )

        return build_response(
            context=self
        )


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import Executor

    Executor(sys.argv[1]).run()
