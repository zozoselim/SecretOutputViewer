"""NovaVision package model for Secret Output Viewer."""

from typing import Any, Dict, Literal, Union

from pydantic import Field, field_validator

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


class SecretContextInput(Input):
    """Safe references received from Environment Secrets Store."""

    name: Literal[
        "secretContext"
    ] = "secretContext"

    value: Dict[str, Any] = Field(
        default_factory=dict
    )

    type: Literal[
        "object"
    ] = "object"

    @field_validator(
        "value",
        mode="before",
    )
    @classmethod
    def normalize_empty_placeholder(
        cls,
        value,
    ):
        """
        NovaVision initially represents an unresolved object input
        as an empty string. Convert only that placeholder to an
        empty object while keeping the field's schema as object.
        """

        if value is None or value == "":
            return {}

        return value

    class Config:
        title = "Secret Context"


class MessageOutput(Output):
    """Non-secret execution status."""

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class ViewerInputs(Inputs):
    secretContext: SecretContextInput


class EmptyConfigs(Configs):
    pass


class ViewerRequest(Request):
    inputs: ViewerInputs

    configs: EmptyConfigs = Field(
        default_factory=EmptyConfigs
    )

    class Config:
        json_schema_extra = {
            "target": "inputs",
        }


class ViewerOutputs(Outputs):
    message: MessageOutput


class ViewerResponse(Response):
    outputs: ViewerOutputs


class SecretOutputViewerExecutor(Config):
    name: Literal[
        "SecretOutputViewer"
    ] = "SecretOutputViewer"

    value: Union[
        ViewerRequest,
        ViewerResponse,
    ]

    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Secret Output Viewer"
        json_schema_extra = {
            "target": {
                "value": 0,
            }
        }


class ConfigExecutor(Config):
    name: Literal[
        "ConfigExecutor"
    ] = "ConfigExecutor"

    value: SecretOutputViewerExecutor

    type: Literal["executor"] = "executor"

    field: Literal[
        "dependentDropdownlist"
    ] = "dependentDropdownlist"

    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value",
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"

    name: Literal[
        "SecretOutputViewer"
    ] = "SecretOutputViewer"