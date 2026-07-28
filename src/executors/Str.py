"""Confirm receipt of the upstream status message."""

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
    from ..utils.response import build_response_str
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        PackageModel,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response_str,
    )


class Str(Component):
    """Confirm that the upstream package is connected."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(
            **self.request.data
        )

        self.upstream_message = self.request.get_param(
            "secretText"
        )

        self.message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        if not self.upstream_message.strip():
            raise RuntimeError(
                "Environment Secrets Store message was empty."
            )

        self.message = (
            "Environment Secrets Store was connected "
            "successfully."
        )

        return build_response_str(
            context=self
        )


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
