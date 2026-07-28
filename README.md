# Secret Output Viewer v0.4.1

Compatibility-oriented viewer for the `secretReferences` string emitted by
Environment Secrets Store.

The package keeps the older working `Str` executor structure, parses the JSON
reference list, resolves values through NovaVision's `Environment` SDK, stores
values only in memory, and returns only a safe status message.

Connection:

```text
Environment Secrets Store.secretReferences
    -> Secret Output Viewer.secretReferences
```

No `cryptography` package or transport key is required.
