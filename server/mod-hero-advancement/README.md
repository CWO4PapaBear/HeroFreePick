# Hero Advancement server foundation

Original, optional AzerothCore policy module. Classic does not need this package. Copy into `modules/mod-hero-advancement` alongside any desired mode modules and rebuild. Hook signatures follow the local exported AzerothCore sources; compilation against your checkout remains required.

Includes authoritative-input validation rules for class restrictions, level-based talent tiers, points, gems, Masteries, and one-time mode-choice eligibility. It does not yet receive or apply builds, persist choices, deduct/reset resources, or manage extra resource bars/form/weapon restrictions. Startup explicitly reports this limitation.
