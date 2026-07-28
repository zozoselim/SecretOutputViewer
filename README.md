# Secret Output Viewer v0.4.2

Select **Str** and connect:

`Environment Secrets Store.secretReferences`
to
`Secret Output Viewer.secretReferences`

The Viewer receives only names such as:

```json
["DOCKER_NETWORK"]
```

It resolves the actual values again from the same NovaVision runtime
through the `Environment` SDK, retains them only in memory, and outputs
a safe success message. Secret values are never returned in the Viewer
output.
