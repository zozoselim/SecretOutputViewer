"""Display a safe status message for a list of secret values."""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.response import build_response_list
else:
    from components.SecretOutputViewer.src.models.PackageModel import PackageModel
    from components.SecretOutputViewer.src.utils.response import build_response_list


class List(Component):
    """Consume secret values without exposing them."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.secret_list = self.request.get_param("secretList")
        if not isinstance(self.secret_list, list):
            raise TypeError("secretList must be a list.")
        self.message = (
            f"List output received successfully. {len(self.secret_list)} "
            "secret value(s) are masked."
        )

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        return build_response_list(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
