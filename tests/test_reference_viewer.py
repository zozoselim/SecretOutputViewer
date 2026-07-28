import importlib
import os
import sys
import types
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


def _register_package(name: str, path: Path) -> None:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules[name] = module


def _prepare_imports() -> None:
    _register_package("novavision", SRC_DIR)
    _register_package("novavision.package", SRC_DIR)
    _register_package("novavision.package.executors", SRC_DIR / "executors")
    _register_package("novavision.package.models", SRC_DIR / "models")
    _register_package("novavision.package.utils", SRC_DIR / "utils")

    for module_name in [
        "sdks",
        "sdks.novavision",
        "sdks.novavision.src",
        "sdks.novavision.src.base",
    ]:
        module = types.ModuleType(module_name)
        module.__path__ = []
        sys.modules[module_name] = module

    environment_module = types.ModuleType(
        "sdks.novavision.src.base.environment"
    )

    class FakeEnvironment:
        @staticmethod
        def get_environment_variable(variable):
            return os.getenv(variable)

    environment_module.Environment = FakeEnvironment
    sys.modules[
        "sdks.novavision.src.base.environment"
    ] = environment_module

    component_module = types.ModuleType(
        "sdks.novavision.src.base.component"
    )

    class FakeComponent:
        def __init__(self, request=None, bootstrap=None):
            self.request = request
            self.bootstrap_data = bootstrap

    component_module.Component = FakeComponent
    sys.modules[
        "sdks.novavision.src.base.component"
    ] = component_module

    model_module = types.ModuleType(
        "novavision.package.models.PackageModel"
    )

    class FakePackageModel:
        def __init__(self, **data):
            self.data = data

    model_module.PackageModel = FakePackageModel
    sys.modules[
        "novavision.package.models.PackageModel"
    ] = model_module

    response_module = types.ModuleType(
        "novavision.package.utils.response"
    )

    def fake_build_response(context):
        return {"message": context.message}

    response_module.build_response = fake_build_response
    sys.modules[
        "novavision.package.utils.response"
    ] = response_module


_prepare_imports()

environment_utils = importlib.import_module(
    "novavision.package.utils.environment"
)
executor_module = importlib.import_module(
    "novavision.package.executors.SecretOutputViewer"
)
SecretOutputViewer = executor_module.SecretOutputViewer


class FakeRequest:
    def __init__(self, references):
        self.data = {
            "type": "component",
            "name": "SecretOutputViewer",
            "configs": {},
        }
        self.model = None
        self.params = {"secretReferences": references}

    def get_param(self, name):
        return self.params[name]


def test_resolve_reference_string(monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN", "private-token")
    result = environment_utils.resolve_secret_references(
        '["ACCESS_TOKEN"]'
    )
    assert result == {"ACCESS_TOKEN": "private-token"}


def test_missing_reference_fails(monkeypatch):
    monkeypatch.delenv("MISSING_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        environment_utils.resolve_secret_references(
            '["MISSING_TOKEN"]'
        )


def test_executor_returns_only_message(monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN", "do-not-expose-me")
    executor = SecretOutputViewer(
        request=FakeRequest('["ACCESS_TOKEN"]'),
        bootstrap={},
    )
    response = executor.run()

    assert executor.resolved_values == {
        "ACCESS_TOKEN": "do-not-expose-me"
    }
    assert response == {
        "message": (
            "1 secret value(s) were resolved and consumed "
            "successfully."
        )
    }
    assert "do-not-expose-me" not in str(response)
