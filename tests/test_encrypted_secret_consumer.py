import importlib
import json
import os
import sys
import types
from pathlib import Path

import pytest
from cryptography.fernet import Fernet


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
        "novavision.package.executors",
        SRC_DIR / "executors",
    )
    _register_package(
        "novavision.package.models",
        SRC_DIR / "models",
    )
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

crypto_utils = importlib.import_module(
    "novavision.package.utils.crypto"
)
environment_utils = importlib.import_module(
    "novavision.package.utils.environment"
)
executor_module = importlib.import_module(
    "novavision.package.executors.SecretOutputViewer"
)
SecretOutputViewer = executor_module.SecretOutputViewer


class FakeRequest:
    def __init__(self, encrypted_payload):
        self.data = {
            "type": "component",
            "name": "SecretOutputViewer",
            "configs": {},
        }
        self.model = None
        self.params = {
            "encryptedSecrets": encrypted_payload,
        }

    def get_param(self, name):
        return self.params[name]


def make_payload(key: str, values: dict) -> str:
    return Fernet(key.encode()).encrypt(
        json.dumps(values).encode()
    ).decode()


def test_single_executor_and_run_method():
    executors_dir = SRC_DIR / "executors"
    assert (executors_dir / "SecretOutputViewer.py").is_file()
    assert not (executors_dir / "List.py").exists()
    assert not (executors_dir / "Str.py").exists()
    assert callable(getattr(SecretOutputViewer, "run", None))


def test_reads_transport_key(monkeypatch):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv(
        "NOVAVISION_SECRET_TRANSPORT_KEY",
        key,
    )
    assert environment_utils.read_transport_key() == key


def test_decrypts_secret_mapping():
    key = Fernet.generate_key().decode()
    payload = make_payload(
        key,
        {"ACCESS_TOKEN": "private-token"},
    )

    assert crypto_utils.decrypt_secret_values(
        payload,
        key,
    ) == {"ACCESS_TOKEN": "private-token"}


def test_rejects_wrong_key():
    payload = make_payload(
        Fernet.generate_key().decode(),
        {"ACCESS_TOKEN": "private-token"},
    )

    with pytest.raises(RuntimeError):
        crypto_utils.decrypt_secret_values(
            payload,
            Fernet.generate_key().decode(),
        )


def test_executor_consumes_without_exposing_plaintext(
    monkeypatch,
    capsys,
):
    key = Fernet.generate_key().decode()
    payload = make_payload(
        key,
        {"ACCESS_TOKEN": "do-not-expose-me"},
    )
    request = FakeRequest(payload)
    executor = SecretOutputViewer(
        request=request,
        bootstrap={},
    )

    monkeypatch.setattr(
        executor_module,
        "read_transport_key",
        lambda: key,
    )

    response = executor.run()
    captured = capsys.readouterr()

    assert executor.resolved_values == {
        "ACCESS_TOKEN": "do-not-expose-me"
    }
    assert "do-not-expose-me" not in str(response)
    assert "do-not-expose-me" not in captured.out
    assert "do-not-expose-me" not in captured.err
    assert response["message"].startswith("1 secret value")
