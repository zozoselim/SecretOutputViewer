# Secret Output Viewer

Receives the `secretReferences` JSON string from Environment Secrets Store, resolves those names through NovaVision's `Environment` SDK, and consumes the values only in memory.

The component returns only a safe status message. It never outputs plaintext secret values.
