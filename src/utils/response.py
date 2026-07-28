"""Response builder for Secret Output Viewer."""

from sdks.novavision.src.helper.package import PackageHelper

if __package__:
    from ..models.PackageModel import (
        ConfigExecutor,
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
        MessageOutput,
        PackageConfigs,
        PackageModel,
        StrExecutor,
        StrResponse,
        ViewerOutputs,
    )


def build_response_str(context):
    """Return only a safe status message."""

    outputs = ViewerOutputs(
        message=MessageOutput(value=context.message)
    )
    response = StrResponse(outputs=outputs)
    selected_executor = StrExecutor(value=response)
    package_configs = PackageConfigs(
        executor=ConfigExecutor(value=selected_executor)
    )
    helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )
    return helper.build_model(context)
