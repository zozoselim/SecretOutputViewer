"""NovaVision package model for Secret Output Viewer."""

from typing import Dict, List, Literal, Union

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

    name: Literal["secretContext"] = "secretContext"
    value: Dict[str, Union[str, List[str]]]
    type: Literal["object"] = "object"

    class Config:
        title = "Secret Context"


class ConsumerInputs(Inputs):
    secretContext: SecretContextInput


class EmptyConfigs(Configs):
    pass


class ConsumerRequest(Request):
    inputs: ConsumerInputs
    configs: EmptyConfigs = EmptyConfigs()

    class Config:
        json_schema_extra = {
            "target": "inputs",
        }


class MessageOutput(Output):
    """Non-secret consumer status."""

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class ConsumerOutputs(Outputs):
    message: MessageOutput


class ConsumerResponse(Response):
    outputs: ConsumerOutputs


class SecretReferenceConsumerExecutor(Config):
    name: Literal[
        "SecretReferenceConsumer"
    ] = "SecretReferenceConsumer"

    value: Union[
        ConsumerRequest,
        ConsumerResponse,
    ]

    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Secret Reference Consumer"
        json_schema_extra = {
            "target": {
                "value": 0,
            }
        }


class ConfigExecutor(Config):
    name: Literal[
        "ConfigExecutor"
    ] = "ConfigExecutor"
    value: SecretReferenceConsumerExecutor
    type: Literal["executor"] = "executor"
    field: Literal[
        "dependentDropdownlist"
    ] = "dependentDropdownlist"

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
