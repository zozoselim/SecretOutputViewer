"""NovaVision package model for Secret Output Viewer."""

from typing import Literal, Union

from sdks.novavision.src.base.model import (
    Config,
    Configs,
    Input,
    Inputs,
    Output,
    Outputs,
    Package,
    Request,
    Response,
)


class SecretReferencesInput(Input):
    """JSON string containing environment-variable names."""

    name: Literal["secretReferences"] = "secretReferences"
    value: str = ""
    type: Literal["string"] = "string"

    class Config:
        title = "Secret References"


class MessageOutput(Output):
    """Safe status message that never contains secret values."""

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class StrInputs(Inputs):
    secretReferences: SecretReferencesInput


class EmptyConfigs(Configs):
    pass


class StrRequest(Request):
    inputs: StrInputs
    # Keep the same structure as the older viewer version that NovaVision ran.
    configs: EmptyConfigs = EmptyConfigs()

    class Config:
        json_schema_extra = {"target": "inputs"}


class ViewerOutputs(Outputs):
    message: MessageOutput


class StrResponse(Response):
    outputs: ViewerOutputs


class StrExecutor(Config):
    """String executor retained for compatibility with the working package."""

    name: Literal["Str"] = "Str"
    value: Union[StrRequest, StrResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Resolve Secret References"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: StrExecutor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "shortDescription": (
                "Receives secretReferences from Environment Secrets Store "
                "and resolves them through the runtime environment."
            )
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["SecretOutputViewer"] = "SecretOutputViewer"
