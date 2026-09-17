# Hero travel integration plan

## Scope

Use all 160 Rune destinations except Acherus for Mage travel: 160 teleports and 160 portals. The complete schedule and source-derived arrival data are in [HERO-TRAVEL-DESTINATIONS.md](HERO-TRAVEL-DESTINATIONS.md) and [hero-travel-destinations.json](hero-travel-destinations.json). The older twelve-city scope is superseded. Theramore and Stonard are included at level 30.

Classic remains stock. Class+ requires Mage as the original class; Hybrid requires Mage as either selected class; Hero permits any original class. Use the actual character faction and race, never the currently browsed class tab.

## Independent Masteries

- Portal Mastery: entry 21818045, level 10, 2 Ability Points and one Uncommon gem.
- Teleport Mastery: entry 21818046, level 10, 2 Ability Points and one Uncommon gem, Teleport: Dalaran icon.
- Each purchase grants only its own level-eligible spells, at no further AP or gem cost. Neither purchase implies the other. The new Teleport Mastery is an addon catalog entry; its placeholder spell 0 is not a castable or allocated server spell.
- Existing Portal selections retain their Portal purchase. Teleport members now require the separately selected Teleport Mastery; migration must not silently spend another 2 AP/gem or grant a free purchase.

The current 0.39.0 addon implements the split for its existing city catalog (13 members per Mastery, including faction Shattrath variants and the neutral cities). The full 160-destination catalog is specified, not yet imported into the addon or implemented as Mage server spells.

## Levels and factions

Both travel types use racial capital at 10, own-faction capitals at 15, Ratchet/Booty Bay at 25, Shattrath at 62 and Dalaran at 72. Other destinations follow the recorded zone entry bands; noncapital starter settlements begin at 15. These extra levels are design assignments, not pre-existing Rune level requirements.

Preserve the Rune catalog's exact faction tags: Alliance destinations only Alliance, Horde only Horde, neutral either. Do not infer access from a destination's name or change neutral reputation-gated settlements to a faction capital. The two Dark Portal records remain distinct faction arrivals. Faction restrictions apply to grant, cast, arrival and every portal passenger. Unknown faction fails closed for faction-restricted destinations.

Keep enabled flags, exact arrival coordinates/orientation, map and destination phase. Preserve Brunnhildar quest 12905 started/completed/rewarded, Crusaders' Pinnacle quest 13141 rewarded, Dun Nifflelem quest 12924 started/completed/rewarded OR 12967 rewarded, and Shadow Vault faction quest 12896/12897 rewarded. Required reputation must be Neutral or better. Acherus and its Death Knight requirements are excluded entirely from Mage travel. Do not compare the caster's unrelated current-area phase to the destination phase.

## Independent ownership and spell definitions

Allocate collision-checked Mage teleport, portal, arrival and gameobject IDs. Clone travel mechanics and arrival data, not Rune ownership authorization. Do not reuse Rune spell IDs for the finished Mage versions: their existing handlers require Rune ownership and consume reagents.

After a successful authoritative build commit, persist character-specific entitlement to each Mastery independently. Never update `bear_vanity_unlock`, grant account Rune ownership, consume Rune unlock items, or teach the Rune-owned spell IDs. Removing a Mastery revokes only its Mage-specific spells. Rune purchases and Rune cast behavior remain unchanged.

Current neutral-city addon entries still reference Rune spells for preview. Those references are not the finished independent Mage implementation and do not bypass Rune ownership or alter reagent behavior.

## Mage reagent production

Mage versions require and consume no casting reagent. On successful personal teleport, give the caster one Rune of Teleportation (17031). On successful caster traversal of their own Mage portal, give that caster one Rune of Portals (17032), at most once per portal cast. This implements "after they travel": creation alone, failed/interrupted travel and other passengers generate no item. Only these ordinary reagent items are produced, not the Rune collection unlock items.

Remove reagent requirements from both Mage client spell definitions and server definitions. Generate the item only after server-confirmed arrival, using a durable, unique operation per cast so reconnects or repeated portal use cannot duplicate it. Inventory-full delivery needs a persisted pending reward/recovery path rather than silently losing the item. Retain existing cast time, cooldown and portal lifetime unless separately changed.

Portal passengers must be the caster or members of the same party/subgroup, meet the destination faction/level/quest/reputation and normal travel restrictions, and need not own either Mastery or a Rune unlock. Revalidate the caster's entitlement while the portal exists. Casting and arrival remain prohibited while dead, in combat, in flight or in a battleground as in the Rune implementation.

## Implementation and validation still required

The Hero server foundation does not yet persist or commit custom builds. Connect its trusted commit handler to independent travel entitlements before enabling server grants. Add login/level-up reconciliation, isolated spell definitions/client patch and server cast/arrival/portal handlers. The addon cannot implement inventory rewards or override stock reagent checks on its own.

Test all races, faction boundaries, both Hybrid Mage positions, non-Mage Class+ denial, independent purchases/refunds, every level boundary, all 160 arrivals, quest/reputation failures, passengers, rewards after successful arrival only, inventory-full/reconnect recovery and Rune coexistence. Compile and test on the actual core before claiming server travel works. WSL access was denied during this task; no server compilation or deployment has occurred.
