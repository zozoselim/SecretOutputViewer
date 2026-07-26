# Secret Output Viewer

A small NovaVision demo component designed to be connected after Environment Secrets Store.
It confirms whether the upstream output is `Str` or `List` without printing secret values.

## Modes

- **Str**: accepts the string output of Environment Secrets Store and emits a safe message.
- **List**: accepts the list/object output of Environment Secrets Store and emits a safe message containing only the number of received secrets.

## Application flow

```text
EnvironmentSecretsStore (Str)  -> SecretOutputViewer (Str)
EnvironmentSecretsStore (List) -> SecretOutputViewer (List)
```

Select the same mode in both components. The terminal application output will be the viewer's `message` output.

## Example outputs

Str:

```text
Str output received successfully. Secret value is masked.
```

List:

```text
List output received successfully. 2 secret value(s) are masked.
```

Use the existing Open CV image for `Str`, `List`, and `SecretOutputViewer` when registering the package in NovaVision.
