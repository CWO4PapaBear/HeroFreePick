# Persistent Class+ enrollment runtime

This optional runtime removes the Hfstart name requirement. Newly created characters of the ten supported classes receive a persistent Pending record and reviewed starting-spell snapshot. Classic restores the snapshot; Class+ uses the existing server-validated purchase ledger. Selection remains restricted to the class starting level (1, or stock DK 55) and out of combat. This update does not implement the planned level-one DK creation/relocation.

Enrollment is keyed by character GUID, verified account and class. Character names are audit text only; renames do not lose enrollment. Existing enrolled characters and purchases retain their data. Existing unenrolled characters remain Classic; there is no automatic conversion of established characters. Invalid snapshots produce an error rather than being treated as valid enrollment. Deleting a character removes its four ownership records in the core deletion transaction.

## Installation boundaries

Classic-only users do not install this package or its bridge addons. For a fresh Class+ server install `mod-hero-starting-path` under modules, apply `sql/characters.sql` to the characters database once, rebuild, and install HeroFreePick plus the `HeroStartingPathTest` and `HeroClassPlusCommitTest` addon folders. Their historical folder/table names are retained for compatibility; names no longer restrict enrollment.

This runtime already includes its trainer gate. Do not also load mod-hero-advancement or the policy-only mode modules alongside it: those are a separate foundation and may register duplicate trainer hooks. Hybrid/Hero commits are not provided by this runtime. Current supported stock-ability purchases are covered; unsupported custom spells and full custom talent commits remain outside this update.

Existing test installations retain their four `_test` database tables unchanged; do not rerun the fresh-install SQL. Use the staged deployment for the current test server. The deployment builds before restarting, checks readiness, preserves purchases and backs up the module and bridges. It refuses rollback to the name-limited server after new characters have enrolled, because doing so would strand their progression.

## Validation

Pure C++ eligibility tests cover arbitrary names, all ten classes, starting levels and rejected modes. Lua tests cover server-confirmed choice, login recovery, legacy Classic isolation and bridge syntax. The full AzerothCore adapter must still compile during deployment and be tested in game.

After deployment: create an ordinary-name Mage, verify starting spells are withheld; choose Class+, buy an ability, relog and verify the mode and purchase persist. Create another ordinary-name character, choose Classic and verify stock starting spells/trainer access. Confirm an existing unenrolled character remains unchanged and existing Hfstart Class+ purchases still work.
