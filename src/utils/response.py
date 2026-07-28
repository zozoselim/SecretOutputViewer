"""Response builder for Secret Output Viewer."""

from sdks.novavision.src.helper.package import PackageHelper

if __package__:
    from ..models.PackageModel import (
        ConfigExecutor,
        ConsumerOutputs,
        ConsumerResponse,
        MessageOutput,
        PackageConfigs,
        PackageModel,
        SecretReferenceConsumerExecutor,
    )
else:
    from components.SecretOutputViewer.src.models.PackageModel import (
        ConfigExecutor,
        ConsumerOutputs,
        ConsumerResponse,
        MessageOutput,
        PackageConfigs,
        PackageModel,
        SecretReferenceConsumerExecutor,
    )


def build_response(context):
    """Return a safe downstream success message."""

    outputs = ConsumerOutputs(
        message=MessageOutput(
            value=context.message,
        )
    )

    response = ConsumerResponse(
        outputs=outputs,
    )

    selected_executor = SecretReferenceConsumerExecutor(
        value=response,
    )

    package_configs = PackageConfigs(
        executor=ConfigExecutor(
            value=selected_executor
        )
    )

    helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )

    return helper.build_model(context)
