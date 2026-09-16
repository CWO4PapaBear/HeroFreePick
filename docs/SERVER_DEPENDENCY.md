# Server dependency review

The current addon does not depend on the mod-hero-freepick server foundation. That module is excluded from this repository.

Reviewed foundation source: a WorldScript registers only a startup callback. It iterates catalog spell references, calls SpellMgr lookups and logs entry/missing-record counts. No player mutations, spell grants, talent refunds, class changes or SQL migrations occur in that source.

Local activation records show that a worldserver image containing this audit module was activated on an isolated test installation. The activation also installed the first addon. Build tooling checked core-source hashes and preserved the existing auto-attack module. This review did not inspect or modify the currently running server.

## Removing it

The module can be omitted from the next worldserver build while preserving the rest of the current source and configuration. Redeploying that build removes the audit callback. Deleting its source alone will not remove code already compiled into the running binary.

An earlier image/configuration backup exists in the local activation records, but blindly restoring an old image could undo later unrelated changes. First compare the current image, modules and configuration; then rebuild without mod-hero-freepick, retain a rollback image, restart the isolated worldserver, and check health plus existing modules. No Hero-specific database cleanup is expected from the reviewed audit-only source.

The addon should continue to open, plan local selections and use existing ordinary-class talent APIs. Cross-class progression still requires a future server implementation. No server removal was performed while preparing this repository.
