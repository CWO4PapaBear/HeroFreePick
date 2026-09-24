# Hybrid beast tame completion repair

Observed: Pettest, Hunter secondary, Mottled Boar; successful channel with no pet or error. Confirmed native EffectTameCreature silently rejected a non-Hunter original class.

Narrow exception for spell 1515: learned Tame Beast, authoritative custom mode, and selected Hunter class mask (Hero permits free selection). Keeps native Hunter behavior and existing cast/target/level/exotic/ownership/occupied-pet checks. Does not globally change IsClass or demon capture.

Pet loading: the DK ghoul visibility exception applies only to non-Hunter-type pets, allowing DK/Hunter beast pets to restore. Existing tameability/exotic checks remain.

Full build and local entitlement tests passed. Activated on PTR; image 6c40dbc3a8721c5c09b21402676e3e975ec69a39d2a7dd1fbd7a655e691a59f8 and startup verified. In-game acceptance remains pending. No SQL/client changes. Test tame, dismiss/call, death/revive, relog, stable store/retrieve; primary Hunter and DK/Hunter cases; reject absent entitlement, too-high-level/untameable/exotic targets without authorization and existing active pets. Startup must retain starter-item, shared progression and Martial Fluidity readiness.

Apply the narrow integration patch to the matching pre-repair PTR source, not over an already patched tree. Full proprietary baseline and deployment backups remain local. Rollback uses the retained previous image/source; it must not restore the character database or remove newly earned pets.
