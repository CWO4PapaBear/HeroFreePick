# A52 Mastery comparison and Classic apply verification

Reviewed September 17, 2026, release 0.32.3.

## Summoner's Armor

Area 52 spell **701521**, a member of **Warlock Armor Mastery (92166)**, empowers these companions: tamed Beast, tamed Dragonkin, dominated Undead, enslaved Demon, summoned Demon, wild Imp and tethered Elemental. Its description says it increases their critical strike chance with spells and abilities and their spell damage. Only one Warlock Armor can be active at a time.

The extracted description uses `$s1%` and `$s2%` for the two bonuses. Those placeholders were not resolved to runtime values in this review; no numerical bonus is asserted. The `@learns:92166@` marker references Warlock Armor Mastery. This is description/relationship evidence, not recovered server aura logic.

## A52 Masteries compared with ours

Source: extracted Area 52 patch-D Spell.dbc descriptions, matched advancement records, and our current Masteries.lua / Adapter.lua. This is a client-data comparison, not verification of live Ascension server behavior.

| Aspect | A52 client evidence | Our interface |
|---|---|---|
| Entry into most Masteries | Automatically learned with any member ability | Mastery purchased first; member requires that Mastery in the pending plan |
| Additional member cost | 21 of the 23 imported descriptions say 1 Ability Essence and no Ability Gems | 0 Ability Points and 0 rarity gems |
| Mastery purchase | Descriptions mostly explain an automatic unlock; raw advancement records alone do not establish the effective server charge | Explicit 2 AP plus imported Mastery gem cost (including zero for records with zero cost) |
| Presence Mastery | Allows category abilities for essence without gems; selection not offered when a member is already known | Same purchase-first and free-member rule as other Masteries |
| Seal Mastery | Draft-specific wording: grants a level-eligible choice and puts member spells into future drafts | No draft/card mechanics; member selection remains manual |
| Demon Mastery members | Succubus, Felhunter, Felguard, Voidwalker; Imp is not listed in its source description | Those four plus Summon Imp, per requested override |
| Demon Mastery level | Imported level 10 | Level 1, per requested override |
| Owning a Mastery | Descriptions advertise reduced costs/access, not a blanket grant of all spells | Unlocks manual member selections; removing it cascades removal of pending members |
| Companion packages | Separate teaching bundles | Four separate bundle purchases, 4 AP + 2 Epic, staging their included skills together |
| Actual learning | Client data alone cannot establish server implementation | Custom modes remain local preparation only; authoritative custom-mode commit is unfinished |

All 23 imported groups were reviewed. Our differences are intentional custom rules, not a claim of exact Ascension parity. Membership and artwork come from the client data with explicit overrides. The generic pending ability setter currently does not independently enforce every displayed ability-level requirement; the server implementation must validate these, and the client should enforce the same rule before custom-mode release. Talent tier checks and Mastery prerequisites are enforced separately.

## Classic plan and apply

The current Classic path stages changes locally, validates the native unspent-point budget, lower-tier investment and prerequisite talents, then queues standard LearnTalent(tab,index) calls. The poller sends one rank at a time and waits for a native-rank acknowledgment before continuing. Committed reductions require a trainer. Combat and missing acknowledgments interrupt the operation; previously confirmed ranks cannot be rolled back by the addon.

Verification performed in the Lua 5.1 harness:
- Planning two ranks makes no native learning call.
- Clicking the actual pending-review Accept button starts the commit.
- The actual frame OnUpdate poller sends each rank once and waits for acknowledgment.
- Two simulated server acknowledgments complete the operation, clear dirty state and close the review.
- No acknowledgment times out without marking a rank learned.
- Existing tests cover trainer-only committed resets and native tooltips.

**This verifies the implementation with mocked WoW APIs, not a live server.** In-game verification is still required. Select Classic, use the normal class talent pane in Hero Advancement (not Archetype Builder), plan a valid allocation, close the window and choose Accept Changes. Confirm the same ranks in the default talent tree and the decrease in native unspent points. No server module is required for that native talent-learning path.

## UI changes in this release

- Swapped Dragonkin Lore and Dismiss Dragonkin icons in main icons and expanded lists.
- The Tame Dragonkin bundle and its same-named child tame action now both show the connected group. Holding Shift on other bundle children also opens the group's expanded list.
- Reduced ability level-header-to-icon offset from 24 to 17 UI units.
