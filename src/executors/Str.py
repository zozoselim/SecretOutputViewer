"""Display a safe status message for one secret string."""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.response import build_response_str
else:
    from components.SecretOutputViewer.src.models.PackageModel import PackageModel
    from components.SecretOutputViewer.src.utils.response import build_response_str


class Str(Component):
    """Consume one secret without exposing its value."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.secret_text = self.request.get_param("secretText")
        self.message = "Str output received successfully. Secret value is masked."

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def run(self):
        return build_response_str(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
