"""NovaVision package model for the Secret Output Viewer component."""

from typing import List, Literal, Union

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


class SecretStringInput(Input):
    """One environment-variable reference."""

    name: Literal["secretText"] = "secretText"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Secret Reference"


class SecretListInput(Input):
    """Environment-variable references from the store."""

    name: Literal["secretList"] = "secretList"
    value: List[str]
    type: Literal["object"] = "object"

    class Config:
        title = "Secret References"


class MessageOutput(Output):
    """Human-readable, non-secret status message."""

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class StrInputs(Inputs):
    secretText: SecretStringInput


class ListInputs(Inputs):
    secretList: SecretListInput


class EmptyConfigs(Configs):
    pass


class StrRequest(Request):
    inputs: StrInputs
    configs: EmptyConfigs = EmptyConfigs()

    class Config:
        json_schema_extra = {"target": "inputs"}


class ListRequest(Request):
    inputs: ListInputs
    configs: EmptyConfigs = EmptyConfigs()

    class Config:
        json_schema_extra = {"target": "inputs"}


class ViewerOutputs(Outputs):
    message: MessageOutput


class StrResponse(Response):
    outputs: ViewerOutputs


class ListResponse(Response):
    outputs: ViewerOutputs


class StrExecutor(Config):
    name: Literal["Str"] = "Str"
    value: Union[StrRequest, StrResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Str"
        json_schema_extra = {"target": {"value": 0}}


class ListExecutor(Config):
    name: Literal["List"] = "List"
    value: Union[ListRequest, ListResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "List"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[StrExecutor, ListExecutor]
    type: Literal["executor"] = "executor"
    field: Literal[
        "dependentDropdownlist"
    ] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Reference Input Type"
        json_schema_extra = {
            "shortDescription": (
                "Choose Str for one environment reference "
                "or List for reference lists."
            )
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal[
        "SecretOutputViewer"
    ] = "SecretOutputViewer"
