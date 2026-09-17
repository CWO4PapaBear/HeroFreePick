# Hero travel integration plan

## Scope and current status

Reuse the existing Runes of Return / Runes of Retreat implementation for Class+, Hybrid, and Hero. Classic remains stock trainer/quest travel and does not require this integration.

Class+ can select the Mage travel mastery only as a Mage. Hybrid can select it when Mage is either of its two chosen classes. Hero can select it regardless of original class. Destination eligibility is based on actual character race/faction and level, not the browsed class tab.

The addon currently has one combined Portal Mastery, not a separate Teleport Mastery. It includes stock capital/Shattrath/Dalaran teleports and portals, plus the two neutral Rune portals. The plan below adds the neutral Return spells and replaces other custom-mode travel members with the corresponding existing Rune spells. This plan does not introduce a second Mastery purchase or a second gem cost.

## Shared destination mapping

| Destination | Faction | Return spell (teleport) | Retreat spell (portal) | Unlock |
|---|---|---:|---:|---|
| Stormwind | Alliance | 901111 | 903111 | 10 racial capital / 15 faction capitals |
| Ironforge | Alliance | 901067 | 903067 | 10 racial capital / 15 faction capitals |
| Darnassus | Alliance | 901039 | 903039 | 10 racial capital / 15 faction capitals |
| Exodar | Alliance | 901048 | 903048 | 10 racial capital / 15 faction capitals |
| Orgrimmar | Horde | 901089 | 903089 | 10 racial capital / 15 faction capitals |
| Thunder Bluff | Horde | 901136 | 903136 | 10 racial capital / 15 faction capitals |
| Undercity | Horde | 901142 | 903142 | 10 racial capital / 15 faction capitals |
| Silvermoon City | Horde | 901103 | 903103 | 10 racial capital / 15 faction capitals |
| Ratchet | Neutral | 901090 | 903090 | 25 |
| Booty Bay | Neutral | 901018 | 903018 | 25 |
| Shattrath | Neutral | 901102 | 903102 | 62 |
| Dalaran | Neutral | 901037 | 903037 | 72 |

Mappings originate in `Vanity_Travel_Trainer/Destinations.json`. The saved catalog contains 161 destinations; only the twelve scheduled above belong to this Mastery plan. Use its destination IDs, arrival spells, portal objects, coordinates, phases, and eligibility rules rather than duplicating them.

## Required integration work

1. Package travel support as an optional shared dependency of the custom progression modes. Reuse the existing generated spell patch and server travel definitions. Do not require the Vanity collecting UI or Rune redemption process for Mastery-earned access. Avoid registering duplicate spell scripts/portal objects if Vanity is installed too.
2. Persist a character-specific Mastery travel entitlement after a successful authoritative Hero build commit. Validate selected mode, Mage class access, mastery ownership, race/faction and level. Do not write a Rune account collection unlock or consume an unlock rune for Mastery access.
3. Centralize access checks so the existing Rune collection path and the Hero Mastery path can independently authorize travel. Apply this consistently to teaching, casting through either UI, spellbook casts, and portal entry. Keep existing faction, arrival, combat/location, party and destination restrictions. Inspect every path: the current chat/UI cast path checks Rune ownership while the spell check emphasizes destination eligibility.
4. Grant only eligible Return and Retreat spells at commit, login and level-up. Track each spell's grant source. Removing a Mastery/mode must revoke only Mastery-derived grants; preserve spells also authorized by a Rune account unlock or another legitimate source.
5. Replace custom-mode stock travel entries with the mapped Rune Return/Retreat IDs, add neutral Return spells, and preserve Classic entries. Show required levels and faction requirements in the mastery tooltip and hide ineligible-faction entries. Keep the existing combined 2 AP + one Uncommon gem purchase and free member grants.
6. Keep the existing travel cast/reagent/cooldown/portal-lifetime behavior unless the user requests a separate balance change. Runes of Return/Retreat unlock items remain part of the separate collection system; casting reagents are distinct.
7. Validate all ten stock races at levels 9/10/14/15/24/25/61/62/71/72, Mage as either Hybrid class, non-Mage Class+ denial, Hero access, faction restrictions, learned-spell visibility, direct spellbook casting, portal passengers, removal/regrant, login reconciliation, and coexistence with Rune-owned destinations. Compile and run against the server before claiming travel works.

## Existing limitation

The addon still stages custom builds locally. The server foundation does not yet commit those builds or persist Mastery entitlements. Finding the completed Rune transport implementation removes the need to recreate transport, but does not itself implement Hero learning authorization. This document records the integration plan; it is not an implemented server bridge.
