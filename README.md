# Secret Output Viewer

This trusted test component receives the `encryptedSecrets` string from
Environment Secrets Store, decrypts it in memory, and returns only a safe status
message.

Both packages must receive the same runtime environment variable:

```text
NOVAVISION_SECRET_TRANSPORT_KEY=<Fernet key>
```

Workflow connection:

```text
Environment Secrets Store.encryptedSecrets
    -> Secret Output Viewer.encryptedSecrets
```

The decrypted mapping is available only inside:

```python
self.resolved_values
```

It is never returned, printed, or logged.
