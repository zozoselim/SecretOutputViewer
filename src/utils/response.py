"""Response builder for Secret Output Viewer."""

from sdks.novavision.src.helper.package import PackageHelper

if __package__:
    from ..models.PackageModel import (
        ConfigExecutor,
        MessageOutput,
        PackageConfigs,
        PackageModel,
        SecretOutputViewerExecutor,
        ViewerOutputs,
        ViewerResponse,
    )
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        ConfigExecutor,
        MessageOutput,
        PackageConfigs,
        PackageModel,
        SecretOutputViewerExecutor,
        ViewerOutputs,
        ViewerResponse,
    )


def build_response(context):
    outputs = ViewerOutputs(
        message=MessageOutput(value=context.message)
    )
    response = ViewerResponse(outputs=outputs)
    selected_executor = SecretOutputViewerExecutor(value=response)
    package_configs = PackageConfigs(
        executor=ConfigExecutor(value=selected_executor)
    )
    helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )
    return helper.build_model(context)
