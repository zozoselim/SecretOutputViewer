"""Resolve secret references and return a plaintext-free status message."""

import os
import sys
from typing import Dict

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.environment import resolve_secret_references
    from ..utils.response import build_response_str
else:
    from components.SecretOutputViewer.src.models.PackageModel import PackageModel
    from components.SecretOutputViewer.src.utils.environment import (
        resolve_secret_references,
    )
    from components.SecretOutputViewer.src.utils.response import (
        build_response_str,
    )


class Str(Component):
    """Compatibility executor based on the older working viewer."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.secret_references = self.request.get_param("secretReferences")
        self.resolved_values: Dict[str, str] = {}
        self.message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        try:
            self.resolved_values = resolve_secret_references(
                self.secret_references
            )
            self.message = (
                f"{len(self.resolved_values)} secret reference(s) were "
                "resolved and consumed successfully. Secret values are masked."
            )
        except Exception as error:
            # Return a visible, safe diagnostic instead of silently producing
            # zero outputs. Variable names may appear, secret values never do.
            self.resolved_values = {}
            self.message = (
                "Secret references were received but could not be resolved: "
                f"{error}"
            )

        return build_response_str(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
