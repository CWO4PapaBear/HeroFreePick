# Class+ spell availability audit

This is the first server-integration inventory, not installable spell SQL or a client patch. It compares the effective FreePick catalog against the saved stock 3.3.5 Spell.dbc (hash matched to the earlier stock catalog). No live server has been queried.

## Coverage

All Class+ source classes, both factions, all referenced ranks plus primary stat choices. Retired companion duplicates and Classic-only supplements excluded.

1492 catalog/stat entries; 2906 spell references; 2761 distinct nonzero IDs.

| Classification | References |
|---|---:|
| absent-from-stock | 66 |
| catalog-only | 1 |
| stock-id-name-conflict | 120 |
| stock-present | 2719 |

**66 distinct referenced spell IDs are absent from the stock baseline.** These are candidates for new definitions, not a count of new records ultimately needed: wrappers can be server entitlements, stock equivalents may be reusable, and triggered/dependent spells can add requirements.

## Implementation rules

1. Reuse stock spell IDs when the intended mechanics match. Unavailable training/access is not the same as a missing spell.
2. Never overwrite an existing stock ID with an imported ability. Name conflicts require a mechanic comparison and, when different, new namespaced IDs.
3. Mastery wrappers can be authoritative purchase/grant entitlements without a castable spell record. Teleport Mastery currently uses UI-only spell 0.
4. Pet behavior belongs to More Minions; Mage travel needs independent IDs and its agreed reagent-generation handlers. Reference IDs in the current UI are not finished server definitions.
5. For genuinely new castable abilities, define matching client/server records, effects, triggered dependencies, required hooks, scaling, ranks, visuals and ownership rules. Spell records alone do not implement unsupported effects.
6. Pin the actual target core and audit its DBC/SQL/SpellMgr data before reserving IDs or generating install/uninstall SQL. Preserve Classic records unchanged.

## Missing and conflicting references

Names and IDs only; no extracted binary or full spell definitions are shipped here. A52 presence is evidence for research, not a working implementation.

| Class | Entry | Ability | Spell | Status | Stock name | Reference name | Owner |
|---|---|---|---:|---|---|---|---|
| All | primary-stat-Agility | Primary Stat: Agility | 84865 | absent-from-stock | — | Primary Stat: Agility | Class+ spell mechanics |
| All | primary-stat-Intellect | Primary Stat: Intellect | 84866 | absent-from-stock | — | Primary Stat: Intellect | Class+ spell mechanics |
| All | primary-stat-Spirit | Primary Stat: Spirit | 84867 | absent-from-stock | — | Primary Stat: Spirit | Class+ spell mechanics |
| All | primary-stat-Strength | Primary Stat: Strength | 84864 | absent-from-stock | — | Primary Stat: Strength | Class+ spell mechanics |
| DeathKnight | 25000893 | Dismiss Undead | 893 | absent-from-stock | — | Dismiss Undead | More Minions |
| DeathKnight | 23000891 | Dominate Undead | 891 | absent-from-stock | — | Dominate Undead | More Minions |
| DeathKnight | 25000899 | Dominate Undead | 899 | absent-from-stock | — | Dominate Undead | More Minions |
| DeathKnight | 21092418 | Presence Mastery | 92418 | absent-from-stock | — | Presence Mastery | Entitlement/grant rules |
| DeathKnight | 25000885 | Raise Undead | 885 | absent-from-stock | — | Raise Undead | More Minions |
| DeathKnight | 25000889 | Revive Undead | 889 | absent-from-stock | — | Revive Undead | More Minions |
| DeathKnight | 25109980 | Undead Lore | 109980 | absent-from-stock | — | Undead Lore | More Minions |
| Druid | 908 | Empowered Rejuvenation | 33886 | stock-id-name-conflict | Empowered Rejuvenation | Nature's Rejuvenation | Class+ spell mechanics |
| Druid | 908 | Empowered Rejuvenation | 33887 | stock-id-name-conflict | Empowered Rejuvenation | Nature's Rejuvenation | Class+ spell mechanics |
| Druid | 908 | Empowered Rejuvenation | 33888 | stock-id-name-conflict | Empowered Rejuvenation | Nature's Rejuvenation | Class+ spell mechanics |
| Druid | 908 | Empowered Rejuvenation | 33889 | stock-id-name-conflict | Empowered Rejuvenation | Nature's Rejuvenation | Class+ spell mechanics |
| Druid | 908 | Empowered Rejuvenation | 33890 | stock-id-name-conflict | Empowered Rejuvenation | Nature's Rejuvenation | Class+ spell mechanics |
| Druid | 21954710 | Feral Shapeshift Mastery | 954710 | absent-from-stock | — | Feral Shapeshift Mastery | Entitlement/grant rules |
| Druid | 1114 | Improved Insect Swarm | 57849 | stock-id-name-conflict | Improved Insect Swarm | Celestial Bane | Class+ spell mechanics |
| Druid | 1114 | Improved Insect Swarm | 57850 | stock-id-name-conflict | Improved Insect Swarm | Celestial Bane | Class+ spell mechanics |
| Druid | 1114 | Improved Insect Swarm | 57851 | stock-id-name-conflict | Improved Insect Swarm | Celestial Bane | Class+ spell mechanics |
| Druid | 631 | Nature's Swiftness | 17116 | stock-id-name-conflict | Nature's Swiftness | Natural Alacrity | Class+ spell mechanics |
| Druid | 20000831 | Nature's Swiftness | 17116 | stock-id-name-conflict | Nature's Swiftness | Natural Alacrity | Class+ spell mechanics |
| Druid | 160 | Remove Curse | 2782 | stock-id-name-conflict | Remove Curse | Abolish Curse | Class+ spell mechanics |
| Druid | 607 | Thick Hide | 16929 | stock-id-name-conflict | Thick Hide | Elder Hide | Class+ spell mechanics |
| Druid | 607 | Thick Hide | 16930 | stock-id-name-conflict | Thick Hide | Elder Hide | Class+ spell mechanics |
| Druid | 607 | Thick Hide | 16931 | stock-id-name-conflict | Thick Hide | Elder Hide | Class+ spell mechanics |
| Druid | 905 | Wrath of Cenarius | 33606 | stock-id-name-conflict | Wrath of Cenarius | Wrath of Cenarius (Capstone SLS) | Class+ spell mechanics |
| Druid | 905 | Wrath of Cenarius | 33607 | stock-id-name-conflict | Wrath of Cenarius | Wrath of Cenarius Capstone | Class+ spell mechanics |
| Hunter | 21092164 | Advanced Trap Mastery | 92164 | absent-from-stock | — | Advanced Trap Mastery | Entitlement/grant rules |
| Hunter | 698 | Deflection | 19295 | stock-id-name-conflict | Deflection | Improved Counterattack | Class+ spell mechanics |
| Hunter | 698 | Deflection | 19297 | stock-id-name-conflict | Deflection | Improved Counterattack | Class+ spell mechanics |
| Hunter | 698 | Deflection | 19298 | stock-id-name-conflict | Deflection | Improved Counterattack | Class+ spell mechanics |
| Hunter | 21092156 | Hunter Aspect Mastery | 92156 | absent-from-stock | — | Hunter Aspect Mastery | Entitlement/grant rules |
| Hunter | 769 | Improved Tracking | 52783 | stock-id-name-conflict | Improved Tracking | Lone Wolf | Class+ spell mechanics |
| Hunter | 769 | Improved Tracking | 52785 | stock-id-name-conflict | Improved Tracking | Lone Wolf | Class+ spell mechanics |
| Hunter | 23965200 | Tame Beast | 965200 | absent-from-stock | — | Tame Beast Abilities | More Minions |
| Hunter | 21801494 | Tracking Mastery | 801494 | absent-from-stock | — | Tracking Mastery | Entitlement/grant rules |
| Mage | 426 | Arcane Focus | 11222 | stock-id-name-conflict | Arcane Focus | Alacrity | Class+ spell mechanics |
| Mage | 426 | Arcane Focus | 12839 | stock-id-name-conflict | Arcane Focus | Alacrity | Class+ spell mechanics |
| Mage | 426 | Arcane Focus | 12840 | stock-id-name-conflict | Arcane Focus | Alacrity | Class+ spell mechanics |
| Mage | 22092171 | Arcane Ward | 92171 | absent-from-stock | — | Arcane Ward | Class+ spell mechanics |
| Mage | 25091631 | Call Dragonkin | 91631 | absent-from-stock | — | Call Dragonkin | More Minions |
| Mage | 25091652 | Dismiss Dragonkin | 91652 | absent-from-stock | — | Dismiss Dragonkin | More Minions |
| Mage | 25109982 | Dragonkin Lore | 109982 | absent-from-stock | — | Dragonkin Lore | More Minions |
| Mage | 866 | Empowered Frostbolt | 31682 | stock-id-name-conflict | Empowered Frostbolt | Empowering Frostbolt | Class+ spell mechanics |
| Mage | 866 | Empowered Frostbolt | 31683 | stock-id-name-conflict | Empowered Frostbolt | Empowering Frostbolt | Class+ spell mechanics |
| Mage | 22760204 | Holy Ward | 760204 | absent-from-stock | — | Holy Ward | Class+ spell mechanics |
| Mage | 414 | Improved Cone of Cold | 11190 | stock-id-name-conflict | Improved Cone of Cold | Flash Freeze | Class+ spell mechanics |
| Mage | 414 | Improved Cone of Cold | 12489 | stock-id-name-conflict | Improved Cone of Cold | Flash Freeze | Class+ spell mechanics |
| Mage | 414 | Improved Cone of Cold | 12490 | stock-id-name-conflict | Improved Cone of Cold | Flash Freeze | Class+ spell mechanics |
| Mage | 21092155 | Mage Armor Mastery | 92155 | absent-from-stock | — | Mage Armor Mastery | Entitlement/grant rules |
| Mage | 22760210 | Nature Ward | 760210 | absent-from-stock | — | Nature Ward | Class+ spell mechanics |
| Mage | 21818045 | Portal Mastery | 818045 | absent-from-stock | — | Portal Mastery | Entitlement/grant rules |
| Mage | 22903018 | Portal: Booty Bay | 903018 | absent-from-stock | — | Void Strike | Mage travel |
| Mage | 22903090 | Portal: Ratchet | 903090 | absent-from-stock | — | Thorn Shot | Mage travel |
| Mage | 36 | Remove Curse | 475 | stock-id-name-conflict | Remove Curse | Dispel Curse | Class+ spell mechanics |
| Mage | 25091633 | Revive Dragonkin | 91633 | absent-from-stock | — | Revive Dragonkin | More Minions |
| Mage | 23091634 | Tame Dragonkin | 91634 | absent-from-stock | — | Tame Dragonkin | More Minions |
| Mage | 25093558 | Tame Dragonkin | 93558 | absent-from-stock | — | Tame Dragonkin | More Minions |
| Mage | 21818046 | Teleport Mastery | 0 | catalog-only | — | — | Entitlement/grant rules |
| Mage | 22901018 | Teleport: Booty Bay | 901018 | absent-from-stock | — | — | Mage travel |
| Mage | 22901090 | Teleport: Ratchet | 901090 | absent-from-stock | — | Rapid Killing | Mage travel |
| Mage | 21092170 | Ward Mastery | 92170 | absent-from-stock | — | Ward Mastery | Entitlement/grant rules |
| Paladin | 21954711 | Blessing Mastery | 954711 | absent-from-stock | — | Blessing Mastery | Entitlement/grant rules |
| Paladin | 731 | Deflection | 20060 | stock-id-name-conflict | Deflection | Light's Vengeance | Class+ spell mechanics |
| Paladin | 731 | Deflection | 20061 | stock-id-name-conflict | Deflection | Light's Vengeance | Class+ spell mechanics |
| Paladin | 731 | Deflection | 20062 | stock-id-name-conflict | Deflection | Light's Vengeance | Class+ spell mechanics |
| Paladin | 21092169 | Judgement Mastery | 92169 | absent-from-stock | — | Judgement Mastery | Entitlement/grant rules |
| Paladin | 740 | One-Handed Weapon Specialization | 20196 | stock-id-name-conflict | One-Handed Weapon Specialization | Blessed Weapons | Class+ spell mechanics |
| Paladin | 740 | One-Handed Weapon Specialization | 20197 | stock-id-name-conflict | One-Handed Weapon Specialization | Blessed Weapons | Class+ spell mechanics |
| Paladin | 740 | One-Handed Weapon Specialization | 20198 | stock-id-name-conflict | One-Handed Weapon Specialization | Blessed Weapons | Class+ spell mechanics |
| Paladin | 21092157 | Paladin Aura Mastery | 92157 | absent-from-stock | — | Paladin Aura Mastery | Entitlement/grant rules |
| Paladin | 21954707 | Seal Mastery | 954707 | absent-from-stock | — | Seal Mastery | Entitlement/grant rules |
| Paladin | 737 | Toughness | 20143 | stock-id-name-conflict | Toughness | Tenacity | Class+ spell mechanics |
| Paladin | 737 | Toughness | 20144 | stock-id-name-conflict | Toughness | Tenacity | Class+ spell mechanics |
| Paladin | 737 | Toughness | 20145 | stock-id-name-conflict | Toughness | Tenacity | Class+ spell mechanics |
| Paladin | 737 | Toughness | 20146 | stock-id-name-conflict | Toughness | Tenacity (old) | Class+ spell mechanics |
| Paladin | 737 | Toughness | 20147 | stock-id-name-conflict | Toughness | Tenacity (old) | Class+ spell mechanics |
| Priest | 897 | Focused Mind | 33213 | stock-id-name-conflict | Focused Mind | Void-touched Mind | Class+ spell mechanics |
| Priest | 897 | Focused Mind | 33214 | stock-id-name-conflict | Focused Mind | Void-touched Mind | Class+ spell mechanics |
| Priest | 897 | Focused Mind | 33215 | stock-id-name-conflict | Focused Mind | Void-touched Mind | Class+ spell mechanics |
| Priest | 142 | Lesser Heal | 2050 | stock-id-name-conflict | Lesser Heal | Greater Heal | Class+ spell mechanics |
| Priest | 526 | Silent Resolve | 14523 | stock-id-name-conflict | Silent Resolve | Copious Power | Class+ spell mechanics |
| Priest | 526 | Silent Resolve | 14784 | stock-id-name-conflict | Silent Resolve | Copious Power | Class+ spell mechanics |
| Priest | 526 | Silent Resolve | 14785 | stock-id-name-conflict | Silent Resolve | Copious Power | Class+ spell mechanics |
| Rogue | 21954708 | Advanced Finishing Move Mastery | 954708 | absent-from-stock | — | Advanced Finishing Move Mastery | Entitlement/grant rules |
| Rogue | 22954809 | Crimson Tempest | 954809 | absent-from-stock | — | Crimson Tempest | Class+ spell mechanics |
| Rogue | 480 | Deflection | 13713 | stock-id-name-conflict | Deflection | Improved Riposte | Class+ spell mechanics |
| Rogue | 480 | Deflection | 13853 | stock-id-name-conflict | Deflection | Improved Riposte | Class+ spell mechanics |
| Rogue | 480 | Deflection | 13854 | stock-id-name-conflict | Deflection | Improved Riposte | Class+ spell mechanics |
| Rogue | 22954553 | Dispatch | 954553 | absent-from-stock | — | Dispatch | Class+ spell mechanics |
| Rogue | 21006002 | Essential Finishing Move Mastery | 6002 | absent-from-stock | — | Essential Finishing Move Mastery | Entitlement/grant rules |
| Rogue | 497 | Improved Ambush | 14079 | stock-id-name-conflict | Improved Ambush | Out of Nowhere | Class+ spell mechanics |
| Rogue | 497 | Improved Ambush | 14080 | stock-id-name-conflict | Improved Ambush | Out of Nowhere | Class+ spell mechanics |
| Rogue | 479 | Lightning Reflexes | 13712 | stock-id-name-conflict | Lightning Reflexes | Quick Reflexes | Class+ spell mechanics |
| Rogue | 479 | Lightning Reflexes | 13788 | stock-id-name-conflict | Lightning Reflexes | Quick Reflexes | Class+ spell mechanics |
| Rogue | 479 | Lightning Reflexes | 13789 | stock-id-name-conflict | Lightning Reflexes | Quick Reflexes | Class+ spell mechanics |
| Rogue | 22965426 | Meditate | 965426 | absent-from-stock | — | Meditate | Class+ spell mechanics |
| Rogue | 476 | Precision | 13705 | stock-id-name-conflict | Precision | Accuracy | Class+ spell mechanics |
| Rogue | 476 | Precision | 13832 | stock-id-name-conflict | Precision | Accuracy | Class+ spell mechanics |
| Rogue | 476 | Precision | 13843 | stock-id-name-conflict | Precision | Accuracy | Class+ spell mechanics |
| Rogue | 476 | Precision | 13844 | stock-id-name-conflict | Precision | Accuracy | Class+ spell mechanics |
| Rogue | 476 | Precision | 13845 | stock-id-name-conflict | Precision | Accuracy | Class+ spell mechanics |
| Rogue | 22965425 | Recuperate | 965425 | absent-from-stock | — | Recuperate | Class+ spell mechanics |
| Shaman | 21092160 | Air Totem Mastery | 92160 | absent-from-stock | — | Air Totem Mastery | Entitlement/grant rules |
| Shaman | 576 | Anticipation | 16254 | stock-id-name-conflict | Anticipation | Ghostlike Reflexes | Class+ spell mechanics |
| Shaman | 576 | Anticipation | 16271 | stock-id-name-conflict | Anticipation | Ghostlike Reflexes | Class+ spell mechanics |
| Shaman | 576 | Anticipation | 16272 | stock-id-name-conflict | Anticipation | Ghostlike Reflexes | Class+ spell mechanics |
| Shaman | 25091651 | Dismiss Elemental | 91651 | absent-from-stock | — | Dismiss Elemental | More Minions |
| Shaman | 824 | Dual Wield | 30798 | stock-id-name-conflict | Dual Wield | Empowered Stormstrike | Class+ spell mechanics |
| Shaman | 21092163 | Earth Totem Mastery | 92163 | absent-from-stock | — | Earth Totem Mastery | Entitlement/grant rules |
| Shaman | 25109983 | Elemental Lore | 109983 | absent-from-stock | — | Elemental Lore | More Minions |
| Shaman | 21092159 | Fire Totem Mastery | 92159 | absent-from-stock | — | Fire Totem Mastery | Entitlement/grant rules |
| Shaman | 567 | Healing Focus | 16181 | stock-id-name-conflict | Healing Focus | Natural Focus | Class+ spell mechanics |
| Shaman | 567 | Healing Focus | 16230 | stock-id-name-conflict | Healing Focus | Natural Focus | Class+ spell mechanics |
| Shaman | 567 | Healing Focus | 16232 | stock-id-name-conflict | Healing Focus | Natural Focus | Class+ spell mechanics |
| Shaman | 559 | Improved Fire Nova | 16086 | stock-id-name-conflict | Improved Fire Nova | Rising Flames | Class+ spell mechanics |
| Shaman | 559 | Improved Fire Nova | 16544 | stock-id-name-conflict | Improved Fire Nova | Rising Flames | Class+ spell mechanics |
| Shaman | 790 | Improved Windfury Totem | 29192 | stock-id-name-conflict | Improved Windfury Totem | Improved Wind Totems | Class+ spell mechanics |
| Shaman | 790 | Improved Windfury Totem | 29193 | stock-id-name-conflict | Improved Windfury Totem | Improved Wind Totems | Class+ spell mechanics |
| Shaman | 25091602 | Raise Elemental | 91602 | absent-from-stock | — | Raise Elemental | More Minions |
| Shaman | 562 | Reverberation | 16115 | stock-id-name-conflict | Reverberation | Reverberation (OLD) | Class+ spell mechanics |
| Shaman | 562 | Reverberation | 16116 | stock-id-name-conflict | Reverberation | Reverberation (OLD) | Class+ spell mechanics |
| Shaman | 25091605 | Revive Elemental | 91605 | absent-from-stock | — | Revive Elemental | More Minions |
| Shaman | 1124 | Shamanism | 62100 | stock-id-name-conflict | Shamanism | Shamanism CDR | Class+ spell mechanics |
| Shaman | 21006001 | Shock Mastery | 6001 | absent-from-stock | — | Shock Mastery | Entitlement/grant rules |
| Shaman | 23091606 | Tether Elemental | 91606 | absent-from-stock | — | Tether Elemental | More Minions |
| Shaman | 25093569 | Tether Elemental | 93569 | absent-from-stock | — | Tether Elemental | More Minions |
| Shaman | 585 | Toughness | 16308 | stock-id-name-conflict | Toughness | Toughness (CAPSTONE SLS) | Class+ spell mechanics |
| Shaman | 21092161 | Water Totem Mastery | 92161 | absent-from-stock | — | Water Totem Mastery | Entitlement/grant rules |
| Shaman | 21092158 | Weapon Enhancement Mastery | 92158 | absent-from-stock | — | Weapon Enhancement Mastery | Entitlement/grant rules |
| Shaman | 787 | Weapon Mastery | 29082 | stock-id-name-conflict | Weapon Mastery | Enhanced Weapon Mastery | Class+ spell mechanics |
| Shaman | 787 | Weapon Mastery | 29084 | stock-id-name-conflict | Weapon Mastery | Enhanced Weapon Mastery | Class+ spell mechanics |
| Shaman | 787 | Weapon Mastery | 29086 | stock-id-name-conflict | Weapon Mastery | Enhanced Weapon Mastery | Class+ spell mechanics |
| Warlock | 21954706 | Conjuring Mastery | 954706 | absent-from-stock | — | Conjuring Mastery | Entitlement/grant rules |
| Warlock | 25109981 | Demon Lore | 109981 | absent-from-stock | — | Demon Lore | More Minions |
| Warlock | 21954705 | Demon Mastery | 954705 | absent-from-stock | — | Demon Mastery | More Minions |
| Warlock | 25000892 | Dismiss Demon | 892 | absent-from-stock | — | Dismiss Demon | More Minions |
| Warlock | 23000890 | Enslave Demon | 890 | absent-from-stock | — | Enslave Demon | More Minions |
| Warlock | 25000896 | Enslave Demon | 896 | absent-from-stock | — | Enslave Demon | More Minions |
| Warlock | 97 | Enslave Demon | 1098 | stock-id-name-conflict | Enslave Demon | Temporary Enslaved Demon | Class+ spell mechanics |
| Warlock | 25000887 | Revive Demon | 887 | absent-from-stock | — | Revive Demon | More Minions |
| Warlock | 25000884 | Summon Demon | 884 | absent-from-stock | — | Summon Demon | More Minions |
| Warlock | 22701521 | Summoner's Armor | 701521 | absent-from-stock | — | Summoner's Armor | Class+ spell mechanics |
| Warlock | 657 | Suppression | 18174 | stock-id-name-conflict | Suppression | Death's Grasp | Class+ spell mechanics |
| Warlock | 657 | Suppression | 18175 | stock-id-name-conflict | Suppression | Death's Grasp | Class+ spell mechanics |
| Warlock | 657 | Suppression | 18176 | stock-id-name-conflict | Suppression | Death's Grasp | Class+ spell mechanics |
| Warlock | 21092166 | Warlock Armor Mastery | 92166 | absent-from-stock | — | Warlock Armor Mastery | Entitlement/grant rules |
| Warrior | 452 | Anticipation | 12297 | stock-id-name-conflict | Anticipation | Adaptive Defense | Class+ spell mechanics |
| Warrior | 452 | Anticipation | 12750 | stock-id-name-conflict | Anticipation | Adaptive Defense | Class+ spell mechanics |
| Warrior | 452 | Anticipation | 12751 | stock-id-name-conflict | Anticipation | Adaptive Defense | Class+ spell mechanics |
| Warrior | 452 | Anticipation | 12752 | stock-id-name-conflict | Anticipation | Adaptive Defense | Class+ spell mechanics |
| Warrior | 452 | Anticipation | 12753 | stock-id-name-conflict | Anticipation | Adaptive Defense | Class+ spell mechanics |
| Warrior | 1323 | Dual Wield Specialization | 23584 | stock-id-name-conflict | Dual Wield Specialization | Sidearm Specialization | Class+ spell mechanics |
| Warrior | 1323 | Dual Wield Specialization | 23585 | stock-id-name-conflict | Dual Wield Specialization | Sidearm Specialization | Class+ spell mechanics |
| Warrior | 1323 | Dual Wield Specialization | 23586 | stock-id-name-conflict | Dual Wield Specialization | Sidearm Specialization | Class+ spell mechanics |
| Warrior | 1323 | Dual Wield Specialization | 23587 | stock-id-name-conflict | Dual Wield Specialization | Sidearm Specialization | Class+ spell mechanics |
| Warrior | 1323 | Dual Wield Specialization | 23588 | stock-id-name-conflict | Dual Wield Specialization | Sidearm Specialization | Class+ spell mechanics |
| Warrior | 802 | Endless Rage | 29623 | stock-id-name-conflict | Endless Rage | Two-Handed Weapon Mastery | Class+ spell mechanics |
| Warrior | 467 | Flurry | 12319 | stock-id-name-conflict | Flurry | Shredding Blows | Class+ spell mechanics |
| Warrior | 467 | Flurry | 12971 | stock-id-name-conflict | Flurry | Shredding Blows | Class+ spell mechanics |
| Warrior | 467 | Flurry | 12972 | stock-id-name-conflict | Flurry | Shredding Blows | Class+ spell mechanics |
| Warrior | 467 | Flurry | 12973 | stock-id-name-conflict | Flurry | Shredding Blows | Class+ spell mechanics |
| Warrior | 467 | Flurry | 12974 | stock-id-name-conflict | Flurry | Shredding Blows | Class+ spell mechanics |
| Warrior | 761 | Improved Berserker Rage | 20500 | stock-id-name-conflict | Improved Berserker Rage | Raging Berserker | Class+ spell mechanics |
| Warrior | 761 | Improved Berserker Rage | 20501 | stock-id-name-conflict | Improved Berserker Rage | Raging Berserker | Class+ spell mechanics |
| Warrior | 472 | Improved Demoralizing Shout | 12324 | stock-id-name-conflict | Improved Demoralizing Shout | Improved Victory Rush | Class+ spell mechanics |
| Warrior | 472 | Improved Demoralizing Shout | 12876 | stock-id-name-conflict | Improved Demoralizing Shout | Improved Victory Rush | Class+ spell mechanics |
| Warrior | 472 | Improved Demoralizing Shout | 12877 | stock-id-name-conflict | Improved Demoralizing Shout | Improved Victory Rush | Class+ spell mechanics |
| Warrior | 472 | Improved Demoralizing Shout | 12878 | stock-id-name-conflict | Improved Demoralizing Shout | Disabled spell | Class+ spell mechanics |
| Warrior | 472 | Improved Demoralizing Shout | 12879 | stock-id-name-conflict | Improved Demoralizing Shout | Disabled spell | Class+ spell mechanics |
| Warrior | 1121 | Improved Spell Reflection | 59088 | stock-id-name-conflict | Improved Spell Reflection | Shield Cover | Class+ spell mechanics |
| Warrior | 1121 | Improved Spell Reflection | 59089 | stock-id-name-conflict | Improved Spell Reflection | Shield Cover | Class+ spell mechanics |
| Warrior | 798 | Precision | 29590 | stock-id-name-conflict | Precision | Fervor | Class+ spell mechanics |
| Warrior | 798 | Precision | 29591 | stock-id-name-conflict | Precision | Fervor | Class+ spell mechanics |
| Warrior | 798 | Precision | 29592 | stock-id-name-conflict | Precision | Fervor | Class+ spell mechanics |
| Warrior | 457 | Puncture | 12308 | stock-id-name-conflict | Puncture | Fracture | Class+ spell mechanics |
| Warrior | 457 | Puncture | 12810 | stock-id-name-conflict | Puncture | Fracture | Class+ spell mechanics |
| Warrior | 457 | Puncture | 12811 | stock-id-name-conflict | Puncture | Fracture | Class+ spell mechanics |
| Warrior | 21954709 | Shout Mastery | 954709 | absent-from-stock | — | Shout Mastery | Entitlement/grant rules |
| Warrior | 21954704 | Stance Mastery | 954704 | absent-from-stock | — | Stance Mastery | Entitlement/grant rules |
| Warrior | 453 | Toughness | 12299 | stock-id-name-conflict | Toughness | Firm Grip | Class+ spell mechanics |
| Warrior | 453 | Toughness | 12761 | stock-id-name-conflict | Toughness | Firm Grip | Class+ spell mechanics |
| Warrior | 453 | Toughness | 12762 | stock-id-name-conflict | Toughness | Firm Grip | Class+ spell mechanics |
| Warrior | 795 | Vitality | 29140 | stock-id-name-conflict | Vitality | Resolve | Class+ spell mechanics |
| Warrior | 795 | Vitality | 29143 | stock-id-name-conflict | Vitality | Resolve | Class+ spell mechanics |
| Warrior | 795 | Vitality | 29144 | stock-id-name-conflict | Vitality | Resolve | Class+ spell mechanics |

## Next implementation milestone

Review the missing/conflicting queue by class; separate actual combat spells from wrapper entitlements, pet-module dependencies and travel-module dependencies. Resolve each ability's intended mechanics and dependency graph before producing any client patch or server insert. The JSON retains all references, including stock-present label mismatches, for that review.

## Reproducing this audit

With the repository's Lua 5.1 test dependency (`lupa`) installed:

```text
python tools/audit_classplus_spells.py --stock /path/to/stock/Spell.dbc --reference /path/to/reference/Spell.dbc
```

The generator verifies the reviewed stock baseline hash, runs the existing addon mock setup, includes both factions, and writes this report plus JSON. It never modifies either source DBC. Inputs are local research data and are not shipped in the repository.

The planned 160-destination Mage expansion is not yet in the current addon catalog, so these totals include only current travel references. Four missing travel references are not the final travel implementation count. The 120 stock/reference name conflicts largely involve existing stock talent IDs; retaining stock talent behavior requires no replacement simply because the other client renamed them.
