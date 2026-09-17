# Overlooked Mastery audit

Scanned all 1,415 spell records with “Mastery” in their name, without requiring essence/gem-discount wording. Reviewed 153 records with advancement records, embedded spell references, or teaching descriptions. Compared them with the 23 previously imported mastery records. This is a client-data audit, not confirmation of live server behavior. No gameplay changes were made.

## Confirmed omissions in Area 52 advancement data

| Group | Class | Spell | Level | A52 cost | Findings |
|---|---|---:|---:|---|---|
| Tracking Mastery | Hunter | 801494 | 10 | 2 Ability Essence + 1 Uncommon gem | Advancement entries 389/3042. Explicitly includes Track Beasts, Demons, Dragonkin, Elementals, Giants and Undead; description also says 1% damage bonus against the tracked creature type. |
| Portal Mastery | Mage | 818045 | 20 | 2 Ability Essence + 1 Uncommon gem | Advancement entries 390/3043. Unlocks learning teleport/portal spells in towns and cities; does not state that they are all automatically granted. |

Portal Mastery has 27 spell descriptions explicitly requiring it, including faction variants of stock teleports/portals and Portal: Azzar Faire (364768). Those links establish prerequisites, not automatic granting or stock-client support. Azzar Faire needs separate compatibility review.

Both omissions lacked the cost-discount wording used by the earlier importer.

## Additional candidates, not confirmed Area 52 imports

| Group | Spell | Shared-data association | Status |
|---|---:|---|---|
| Beast Mastery Aspects | 701520 | Hunter, ability entry 1309 | Describes seven aspects: Viper, Monkey, Hawk, Beast, Cheetah, Pack, Wild. Present in shared data but absent from the extracted Area 52 advancement table; cost, level and current availability remain unverified. |
| Timeline Mastery | 300761 | Chronomancer talent | Teaches Timeline Guardian and Timeline Destroyer. Outside our ten stock classes; no Area 52 advancement match. |
| Pact Mastery | 705119 | DemonHunter ability | Teaches Legionfel Pact and Vengeful Pact. Outside our ten stock classes; no Area 52 advancement match. |
| Summoning Mastery | 805042 | Necromancer ability/talent | Teaches Flesh Golems and Gurgling Horrors. Outside our ten stock classes; no Area 52 advancement match. |

Other matches, such as Elemental Mastery, Aura Mastery, Tactical Mastery, Trap Mastery and Ghoul Mastery, describe talents, activations, or enhancements rather than independently purchased ability bundles. Tracking spell variants 801495/801496 lack separate Area 52 purchase entries and should not become duplicate groups. Mystic Scroll/gear-enchant variants are also excluded.

## Import guidance

Discover candidates using names, teaching/unlock language, embedded member references, and reverse prerequisite references. Confirm against the Area 52 advancement table before importing; shared client files also contain other game modes/classes. Keep Classic trainer/quest progression separate. Integrating Portal Mastery into our automatic-grant system would be a deliberate custom rule change from its stated A52 acquisition behavior.

## Import completed in 0.38.0

Tracking and Portal Mastery are imported for custom modes at levels 10 and 20, each costing 2 AP and one Uncommon gem. Their 6 and 26 connected spells use zero-cost automatic grants under our rules. Portal member levels come from A52 spell data (level 1), so our mastery prerequisite makes them available at level 20. This deliberately differs from A52 city learning. Classic catalog entries stay independent. Portal: Azzar Faire is excluded by user request. Custom learning remains local preparation until the server commit handler is implemented.
