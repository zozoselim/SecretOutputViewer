# Secret Output Viewer

This demo consumer receives a safe `secretContext` object from
Environment Secrets Store.

Connect:

```text
EnvironmentSecretsStore.secretContext
    -> SecretOutputViewer.secretContext
```

The consumer resolves the referenced environment variables through
NovaVision's `Environment` SDK. Real values are available only inside
the executor and are never returned or logged.

Successful output:

```text
Secret values were resolved and are ready for trusted internal use.
```
