# Secret Output Viewer v0.4.2

Select **Str** and connect:

`Environment Secrets Store.secretReferences`
to
`Secret Output Viewer.secretReferences`

The incoming value contains only environment-variable names, such as:

`["DOCKER_NETWORK"]`

The viewer resolves the real values through NovaVision's runtime
`Environment` SDK, keeps them only in memory, and outputs a safe message.
