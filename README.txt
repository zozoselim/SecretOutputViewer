Copy these files into the SecretOutputViewer package.

Environment Secrets Store now outputs secretReferences as List[str].
In SecretOutputViewer select the List executor and connect:

EnvironmentSecretsStore.secretReferences
    -> SecretOutputViewer.secretList

The viewer resolves each reference through NovaVision Environment SDK.
It never returns, prints, or logs the secret values.
