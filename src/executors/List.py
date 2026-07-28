"""Resolve list-form secret references and return a safe message."""

import os
import sys
from typing import Dict

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.environment import resolve_secret_references
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
    """Compatibility option required by the executor dropdown."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.secret_references = self.request.get_param(
            "secretReferenceList"
        )
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
                "resolved and consumed successfully. "
                "Secret values are masked."
            )
        except Exception as error:
            self.resolved_values = {}
            self.message = (
                "Secret references reached the viewer, but resolution "
                f"failed: {error}"
            )

        return build_response_list(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
