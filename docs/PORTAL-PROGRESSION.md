# Portal Mastery progression — 0.38.1

Tracking Mastery unlocks at level 1; Portal Mastery unlocks at level 10. Both retain 2 AP and one Uncommon gem. Classic is unchanged.

| Level | Custom Portal Mastery grants |
|---:|---|
| 10 | Teleport and portal to racial capital (Gnomes share Ironforge; Trolls share Orgrimmar). |
| 15 | Teleports and portals to the four capitals of the character's faction. |
| 25 | Ratchet and Booty Bay portals, using existing Runes of Retreat spell IDs. |
| 62 | Own-faction Shattrath teleport/portal variants. |
| 72 | Dalaran teleport and portal. |

Theramore and Stonard have no assigned tier in this schedule and are excluded from this custom Mastery. Opposite-faction portals are not granted. Unknown race cannot receive a racial-capital grant. Mastery tooltips retain faction labels and display race-dependent levels. Old preview grants are reconciled with the new eligibility rules.

## Existing Rune data reused

Saved catalog: outputs/Vanity_Travel_Trainer/Destinations.json, 161 destinations.

- Booty Bay: Return 901018, Retreat 903018, arrival 905018, portal object 960018.
- Ratchet: Return 901090, Retreat 903090, arrival 905090, portal object 960090.

This update references the Retreat IDs only; it does not duplicate or modify the Rune module, grant account collection ownership, or copy its client patch. The existing travel server module checks account unlocks. The future Hero commit handler must authorize Mastery destination access while retaining the established travel eligibility and casting rules. Current Hero ability learning remains a local preview; this package does not make new learned spells castable on the server. The Rune spells retain their original cast/reagent/cooldown behavior unless separately changed.
