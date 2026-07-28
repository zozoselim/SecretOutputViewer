# Secret Output Viewer

Select **List** mode.

Input:

```json
["DOCKER_NETWORK", "ACCESS_TOKEN"]
```

The list contains only environment-variable names. The executor resolves the
actual values through NovaVision's `Environment` SDK, keeps them in memory, and
returns only a safe success message.

The actual values are available inside `self.resolved_values` for trusted
downstream work and are never written to the output.
