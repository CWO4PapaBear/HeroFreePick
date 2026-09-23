# Healing tooltip review

Current PTR export: baseline-20260923-221639, image 41de9640ae3f1d923806ad846890eb34988b692bc145c59e0087d852758286ee. All requested evidence exported successfully and hashes verified.

Scanned 512 descriptions with healing effects or healing-related text (not 512 unique healing spells). Twelve previously unresolved descriptions now show explicit base-rank values. SpellDescriptionVariables supplies the missing min/max, total and multiplier definitions. The no-bonus branches are used and clearly labelled as before level scaling, spell power, talents, glyphs and target modifiers. This is not a prediction of final character healing.

Includes Regrowth, Earthliving Weapon, Death Coil, Mend Pet, Renew, Lightwell, Rejuvenation, Earth Shield, Mana Tide Totem, Healing Touch, Lifebloom and Siphon Life. Existing resolved descriptions and unsupported entries are retained. Divine Star, Seal of Light and other unsupported expressions remain yellow.

Reviewed spell_bonus_data coefficients separately; they are not silently added to base amounts. Verified Earth Shield and Lightwell glyph modification paths and Death Coil int32 healing conversion in exported class scripts. audit.json retains per-entry source expressions and before/after values. Unknown formulas do not imply missing mechanics.

One client file staged: HeroFreePick/ResolvedServerTooltips.lua. No server, SQL or MPQ changes required. Installed in the owner client with backup; not launcher-published. Close WoW before the backed-up installer.
