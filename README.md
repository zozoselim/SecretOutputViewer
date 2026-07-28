# Secret Output Viewer

Use the `Str` executor and connect:

```text
EnvironmentSecretsStore.message
    -> SecretOutputViewer.secretText
```

Environment Secrets Store first verifies access to the configured
environment values and returns a safe success message.

Secret Output Viewer receives that string and returns:

```text
Environment Secrets Store was connected successfully.
```

No secret value is transferred or displayed.
