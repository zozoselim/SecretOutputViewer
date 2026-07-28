"""NovaVision package model for Secret Output Viewer."""

from typing import List, Literal, Union

from pydantic import Field

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
    """JSON string produced by Environment Secrets Store."""

    name: Literal["secretReferences"] = "secretReferences"
    value: str = ""
    type: Literal["string"] = "string"

    class Config:
        title = "Secret References"


class SecretReferenceListInput(Input):
    """Compatibility list input for the second executor option."""

    name: Literal["secretReferenceList"] = "secretReferenceList"
    value: List[str] = Field(default_factory=list)
    type: Literal["object"] = "object"

    class Config:
        title = "Secret Reference List"


class MessageOutput(Output):
    """Safe status output that never contains secret values."""

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class StrInputs(Inputs):
    secretReferences: SecretReferencesInput


class ListInputs(Inputs):
    secretReferenceList: SecretReferenceListInput


class EmptyConfigs(Configs):
    pass


class StrRequest(Request):
    inputs: StrInputs
    configs: EmptyConfigs = Field(default_factory=EmptyConfigs)

    class Config:
        json_schema_extra = {"target": "inputs"}


class ListRequest(Request):
    inputs: ListInputs
    configs: EmptyConfigs = Field(default_factory=EmptyConfigs)

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
        title = "Resolve String References"
        json_schema_extra = {"target": {"value": 0}}


class ListExecutor(Config):
    name: Literal["List"] = "List"
    value: Union[ListRequest, ListResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Resolve Reference List"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    """Keep the two-option structure used by the working viewer."""

    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[StrExecutor, ListExecutor]
    type: Literal["executor"] = "executor"
    field: Literal[
        "dependentDropdownlist"
    ] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Input Type"
        json_schema_extra = {
            "shortDescription": (
                "Use Str for the secretReferences string produced by "
                "Environment Secrets Store."
            )
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["SecretOutputViewer"] = "SecretOutputViewer"
