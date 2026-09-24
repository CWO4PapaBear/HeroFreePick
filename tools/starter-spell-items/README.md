# Ability-based initial spell supplies

Active on PTR. Full compile passed, source restored after build, and startup verified. In-game grant testing remains pending. HeroFreePick server module, custom modes only. Checks actual owned catalog spells/native active-spec talents, not race or original class. Existing characters receive eligible supplies during login/build synchronization.

Grants matching Earth/Fire/Water/Air totem for spell requirements, one initial reagent stack capped at 20 (Soul Shard and low-stack items respect their stack limit), and 200 arrows plus 200 bullets when Auto Shot is known. Does not equip ammunition, grant weapons, modify item templates or grant profession/quest materials. Reagents are restricted to an allowlist and require a current server spell dependency. Higher-rank reagent types get their own first grant when required.

Bank inventory counts toward ownership. Full inventory postpones the grant until a later login/build sync. A per-item PlayerSettings ledger prevents refills after consumption, selling or build reselection; no new SQL schema. Inventory and ledger use the existing build SaveToDB transaction. No periodic inventory polling. PlayerSettings must be enabled.

Rollback restores prior server code/image; legitimately granted items and inert ledger records remain. Never restore a whole character database. Test cross-class/race totems, ammo, existing inventory/bank items, full bags then retry, repeat login, reset/relearn and Classic isolation before publication.
