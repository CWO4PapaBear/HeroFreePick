# Ascension ability previews and class-trainer restriction

## Scope and behavior

Imported all 65 missing class/ability names found by the Area 52 CharacterAdvancement audit across the ten supported classes. Duplicate realm/season records are consolidated, using the lowest source ID; all duplicate costs and levels agree. The audit examined 1,007 Ability rows for the supported classes, excluding shared flags & 9 using the existing import rule. This does not import Ascension's separate custom classes, hidden/system records, or extra talent trees. Existing abilities, aliases, Masteries and companion groups are retained instead of duplicated.

Each new record contains its source level, AP and rarity price, description and packaged icon. The established Class+/Hybrid level-10-and-below-to-level-1 rule still applies; existing stock progression, capstone and DK overrides remain. Classic cannot see or purchase these entries. New entries are explicitly server-pending and excluded from the generated stock purchase allowlist, even if a source ID later appears in a baseline. They can be drafted; they cannot be committed to the test server yet. The supported purchase catalog remains 37033160.

Packaged and decoded 73 icon textures (about 0.42 MB including metadata), including art for 11 existing custom metadata fallbacks. Corrected source icon path typos by matching normalized archive filenames. Source descriptions are preserved in the local audit JSON; tooltip previews resolve fixed numeric references, select the base branch of conditional bonuses, and show readable scaling formulas instead of unresolved client tokens. They are not live server damage calculations.

## Imported abilities

| Class | Ability | Source level | AP | Rarity cost | Source entry |
|---|---|---:|---:|---|---:|
| DeathKnight | Unholy Frenzy | 71 | 4 | 2 Rare | 353 |
| Druid | Efflorescence | 60 | 2 | 1 Epic | 1207 |
| Druid | Flourish | 32 | 2 | 0 Normal | 1638 |
| Druid | Hypnosis | 30 | 3 | 2 Epic | 1624 |
| Druid | Ironfur | 40 | 2 | 1 Epic | 1635 |
| Druid | Mass Entanglement | 18 | 2 | 1 Epic | 1209 |
| Druid | Solar Beam | 34 | 3 | 2 Epic | 1211 |
| Druid | Stampeding Roar | 28 | 2 | 1 Epic | 1208 |
| Druid | Starsurge | 32 | 2 | 0 Normal | 1614 |
| Druid | Ursol's Vortex | 42 | 2 | 1 Epic | 1210 |
| Hunter | Frenzy Shot | 20 | 2 | 1 Epic | 1305 |
| Hunter | Glaive Toss | 15 | 2 | 0 Normal | 1618 |
| Mage | Alter Time | 40 | 3 | 2 Legendary | 1303 |
| Mage | Arcane Orb | 40 | 2 | 1 Epic | 1617 |
| Mage | Brilliance Aura | 1 | 2 | 2 Rare | 1189 |
| Mage | Fizzle | 10 | 2 | 1 Epic | 1622 |
| Mage | Frozen Orb | 30 | 2 | 1 Epic | 1627 |
| Mage | Invocation | 14 | 2 | 1 Rare | 1302 |
| Mage | Mana-forged Barrier | 1 | 2 | 1 Epic | 1300 |
| Mage | Mass Invisibility | 44 | 3 | 2 Legendary | 1631 |
| Mage | Meteor | 36 | 2 | 1 Epic | 1629 |
| Mage | Ring of Frost | 36 | 3 | 2 Epic | 1603 |
| Paladin | Blinding Light | 34 | 3 | 2 Epic | 1190 |
| Paladin | Execution Sentence | 40 | 2 | 1 Epic | 1608 |
| Paladin | Light of Dawn | 30 | 2 | 1 Epic | 1637 |
| Paladin | Light's Hammer | 36 | 2 | 1 Epic | 1607 |
| Paladin | Rebuke | 10 | 2 | 1 Epic | 1621 |
| Priest | Angelic Feather | 28 | 2 | 1 Legendary | 1632 |
| Priest | Divine Star | 30 | 2 | 1 Epic | 1628 |
| Priest | Halo | 36 | 2 | 1 Epic | 1602 |
| Priest | Leap of Faith | 40 | 2 | 1 Legendary | 1196 |
| Priest | Void Eruption | 28 | 2 | 1 Epic | 1640 |
| Priest | Void Shift | 30 | 2 | 1 Legendary | 1197 |
| Rogue | Combat Readiness | 36 | 2 | 1 Epic | 1191 |
| Rogue | Gloomblade | 26 | 2 | 0 Normal | 1636 |
| Rogue | Grappling Hook | 28 | 3 | 2 Legendary | 1633 |
| Rogue | Roll the Bones | 26 | 2 | 1 Epic | 1634 |
| Rogue | Shuriken Toss | 14 | 2 | 0 Normal | 1611 |
| Rogue | Smoke Bomb | 38 | 3 | 2 Legendary | 1193 |
| Shaman | Air Ascendance | 40 | 2 | 1 Epic | 1605 |
| Shaman | Bind Elemental | 20 | 2 | 1 Rare | 1199 |
| Shaman | Capacitor Totem | 36 | 2 | 1 Epic | 1198 |
| Shaman | Cloudburst Totem | 28 | 2 | 1 Epic | 1626 |
| Shaman | Earthquake | 20 | 2 | 1 Epic | 1304 |
| Shaman | Elemental Blast | 40 | 2 | 0 Normal | 1613 |
| Shaman | Flame Ascendance | 34 | 2 | 1 Epic | 1625 |
| Shaman | Healing Rain | 24 | 2 | 0 Normal | 1606 |
| Shaman | Petrification Totem | 40 | 3 | 2 Epic | 1623 |
| Shaman | Sundering | 34 | 3 | 2 Epic | 1639 |
| Shaman | Windwalk Totem | 30 | 2 | 1 Epic | 1200 |
| Warlock | Blood Horror | 40 | 2 | 1 Epic | 1201 |
| Warlock | Burning Rush | 42 | 2 | 1 Legendary | 1609 |
| Warlock | Demonic Leap | 30 | 3 | 2 Legendary | 1203 |
| Warlock | Hand of Gul'dan | 32 | 2 | 0 Normal | 1206 |
| Warlock | Soul Harvest | 36 | 2 | 1 Epic | 1202 |
| Warlock | Soul Swap | 28 | 2 | 1 Epic | 1604 |
| Warlock | Unending Resolve | 42 | 2 | 1 Legendary | 1204 |
| Warrior | Avatar | 40 | 3 | 2 Legendary | 1188 |
| Warrior | Bloodbath | 42 | 2 | 1 Epic | 1601 |
| Warrior | Colossus Smash | 30 | 2 | 1 Rare | 1187 |
| Warrior | Demoralizing Banner | 32 | 2 | 1 Epic | 1612 |
| Warrior | Heroic Leap | 30 | 3 | 3 Legendary | 1186 |
| Warrior | Raging Blow | 28 | 2 | 0 Normal | 1600 |
| Warrior | Siegebreaker | 40 | 2 | 1 Epic | 1616 |
| Warrior | Skull Banner | 40 | 3 | 2 Epic | 1185 |

## Trainer behavior

The server overrides class-trainer spell state to Unavailable, which blocks direct purchase requests as well as normal clicks. It also removes the list shown to custom characters and sends a marked greeting. The addon replaces that window with the requested text and its current Hero Advancement binding (including rebound and unbound cases). Profession, riding, pet trainers and Classic are not subject to the class-trainer rule. Hidden client buttons are not the security boundary.

The dialogue offers Open Hero Advancement and Reset Talents. Reset requires an unexpired class-trainer visit, valid nearby trainer, correct trainer eligibility and being out of combat. It opens native talent-wipe confirmation, letting the core quote and charge its normal reset price. It does not debit gold directly, waive costs, or reset talents before confirmation. Existing trainer gossip reset options are retained. `HeroTrainer::TalentResetPrice` exposes the same core/configuration price calculation for the future interface reset implementation; remote custom-build reset remains unfinished.

## Server integration boundary

The shared gate accepts authoritative Classic, ClassPlus, Hybrid, Hero and Pending states. `HeroTrainer::PublishMode(guid, mode)` must be called after the server loads or commits a verified character mode; never accept an addon-supplied mode as authoritative. The optional server foundation registers the hooks but does not itself implement production mode persistence. Its existing profile registration is NOT sufficient to identify individual players. Unpublished characters remain stock/Classic.

The staged test module connects its persisted test phase to the gate at creation, login and confirmed choice. Therefore the existing test deployment enforces Class+ and pending test characters immediately after installation. Hybrid and Hero production enforcement requires their future authoritative mode persistence to call this same API; it is not claimed live for those modes. Do not install the test gate and production foundation gate together.

The gate caches modes rather than querying the database for every trainer spell. It loads class trainer IDs on startup. If that lookup fails, custom-mode trainer purchases fail closed and the staged startup readiness check fails. Restart after changing trainer categories in the database.

## Validation and deployment

Lua 5.1 mock tests cover descriptions/icons, costs, every custom-mode level boundary, Classic isolation, profession/class routing and bound/rebound/unbound keys. C++ policy tests cover all mode/type combinations. Full AzerothCore compilation and in-game interaction still require the staged WSL deployment. WSL returned E_ACCESSDENIED in this session; no live server/client changes were made.

Close WoW and run:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_ClassPlus_All_Classes_Test/ascension-trainer-update/deploy.py
```

This stage expects the active v4.9 test state, keeps the existing supported purchase catalog, takes backups, and rolls back on failed build/readiness. Test: Classic normal training; custom class trainer dialogue; rebound key; profession training; direct class purchase rejection; native reset cancel/accept and price; preview-only ability refusal on Accept.

API reference: https://github.com/azerothcore/azerothcore-wotlk/blob/master/src/server/game/Entities/Creature/Trainer.cpp (GetSpellState / CanTeachSpell), and the exported local PlayerScript trainer hook declarations.
