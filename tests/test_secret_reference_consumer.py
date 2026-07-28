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
    _register_package(
        "novavision.package.utils",
        SRC_DIR / "utils",
    )

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


_prepare_imports()

environment_utils = importlib.import_module(
    "novavision.package.utils.environment"
)


def test_resolve_references_uses_environment(
    monkeypatch,
):
    monkeypatch.setenv(
        "ACCESS_TOKEN",
        "private-token",
    )

    result = environment_utils.resolve_secret_references(
        [
            "ACCESS_TOKEN",
        ]
    )

    assert result == {
        "ACCESS_TOKEN": "private-token",
    }


def test_missing_reference_fails(monkeypatch):
    monkeypatch.delenv(
        "MISSING_TOKEN",
        raising=False,
    )

    with pytest.raises(RuntimeError):
        environment_utils.resolve_secret_references(
            [
                "MISSING_TOKEN",
            ]
        )
