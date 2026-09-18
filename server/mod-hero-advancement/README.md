# Hero Advancement server foundation

Original, optional AzerothCore policy module. Classic does not need this package. Copy into `modules/mod-hero-advancement` alongside any desired mode modules and rebuild. Hook signatures follow the local exported AzerothCore sources; compilation against your checkout remains required.

Includes authoritative-input validation rules for class restrictions, level-based talent tiers, points, gems, Masteries, and one-time mode-choice eligibility. It does not yet receive or apply builds, persist choices, deduct/reset resources, or manage extra resource bars/form/weapon restrictions. Startup explicitly reports this limitation.

Travel integration for custom modes will reuse the existing Rune Return/Retreat system. See [the integration plan](../../docs/HERO-TRAVEL-INTEGRATION-PLAN.md) for destination mappings, character-specific Mastery authorization, and coexistence with account Rune unlocks. The bridge is not implemented yet.

## Class-trainer gate

The foundation registers ClassTrainerGate.h. Production mode persistence must publish verified per-character modes through HeroTrainer::PublishMode on login and confirmed changes; registering a profile does not activate a character mode. Classic defaults remain stock. See ../../docs/ASCENSION-ABILITIES-AND-TRAINERS.md for hook dependencies, deployment boundaries, native trainer reset pricing, and tests.
