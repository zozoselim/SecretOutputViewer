Copy these files into the SecretOutputViewer repository.

Connect:

EnvironmentSecretsStore.secretReferences
    -> SecretOutputViewer.secretList

Select List mode in SecretOutputViewer.

The viewer resolves the real values through NovaVision Environment SDK,
uses them only inside the executor, and returns only a success message.
