"""Response builders for Secret Output Viewer."""

from sdks.novavision.src.helper.package import PackageHelper

if __package__:
    from ..models.PackageModel import (
        ConfigExecutor,
        ListExecutor,
        ListResponse,
        MessageOutput,
        PackageConfigs,
        PackageModel,
        StrExecutor,
        StrResponse,
        ViewerOutputs,
    )
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        ConfigExecutor,
        ListExecutor,
        ListResponse,
        MessageOutput,
        PackageConfigs,
        PackageModel,
        StrExecutor,
        StrResponse,
        ViewerOutputs,
    )


def _build(context, mode: str):
    message_output = MessageOutput(value=context.message)
    outputs = ViewerOutputs(message=message_output)

    if mode == "Str":
        response = StrResponse(outputs=outputs)
        selected_executor = StrExecutor(value=response)
    elif mode == "List":
        response = ListResponse(outputs=outputs)
        selected_executor = ListExecutor(value=response)
    else:
        raise ValueError(f"Unsupported viewer mode: {mode}")

    package_configs = PackageConfigs(
        executor=ConfigExecutor(value=selected_executor)
    )
    helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )
    return helper.build_model(context)


def build_response_str(context):
    return _build(context=context, mode="Str")


def build_response_list(context):
    return _build(context=context, mode="List")
