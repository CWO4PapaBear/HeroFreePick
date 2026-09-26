# Hero Advancement Warrior stance support reservation

Spell ID **9905301** belongs to the optional Hero Advancement stance support implementation. Warrior spell-family word C bit 29 (`0x20000000`) is reserved for the twelve player Charge/Thunder Clap ranks and this support aura's effect mask.

The fresh PTR Spell.dbc, world spell overrides, bindings, and source searches were checked for collisions. Every installation must repeat the collector/preparation/preflight checks against its own data. Never overwrite an existing record at this ID or reuse the mask bit without reconciliation. Imported catalogs and other modules may introduce future conflicts.

The original module header and `tools/warrior-stance-exemption/integration.patch` integrate into Hero Advancement's existing mode lifecycle; they do not require More Minions or Auto-Attack Forever. Apply to a clean compatible Hero Advancement installation and build against that installation's core. Deployment scripts are specific to this PTR and must be adapted for other installations. No shared core patch or SQL migration is required; both client and server spell data are required.

See the tool README for installation, validation, current limits and rollback. This is a reservation for this feature, not a complete register of all imported spells.
