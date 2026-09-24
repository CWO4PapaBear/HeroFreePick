# Hybrid beast tame completion repair

Observed: Pettest, Hunter secondary, Mottled Boar; successful channel with no pet or error. Confirmed native EffectTameCreature silently rejected a non-Hunter original class.

Narrow exception for completion spell 13481 (triggered by channel spell 1515): learned Tame Beast, authoritative custom mode, and selected Hunter class mask (Hero permits free selection). Keeps native Hunter behavior and existing cast/target/level/exotic/ownership/occupied-pet checks. Does not globally change IsClass or demon capture.

Pet loading: the DK ghoul visibility exception applies only to non-Hunter-type pets, allowing DK/Hunter beast pets to restore. Existing tameability/exotic checks remain.

Full build and local entitlement tests passed. Activated on PTR; image 3c7c136f5d4ba8fe70fc285fe62e2e0f4938395a0d8786b967eb9c64df6d3796 and startup verified. In-game acceptance remains pending. No SQL/client changes. Test tame, dismiss/call, death/revive, relog, stable store/retrieve; primary Hunter and DK/Hunter cases; reject absent entitlement, too-high-level/untameable/exotic targets without authorization and existing active pets. Startup must retain starter-item, shared progression and Martial Fluidity readiness.

Apply the narrow integration patch to the matching pre-repair PTR source, not over an already patched tree. Full proprietary baseline and deployment backups remain local. Rollback uses the retained previous image/source; it must not restore the character database or remove newly earned pets.

The initial completion guard incorrectly checked channel ID 1515. Exported PTR Spell.dbc confirms 1515 triggers 13481, whose effect 55 creates the pet. The corrected guard is compiled and active; entitlement still requires learned 1515. In-game acceptance remains pending.
