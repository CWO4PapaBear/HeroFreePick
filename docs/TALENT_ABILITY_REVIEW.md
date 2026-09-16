# Talent-origin abilities: Area 52 review

144 unique stock talent spells matched Area 52 Ability/TalentAbility records with an Ability Essence cost and zero Talent Essence cost. They are now visible as read-only references in the ability pane and Browse. The existing native talent nodes are unchanged.

Area 52 CharacterAdvancement.dbc SHA-256: `0a6f6311bcd92552a391c5dcf670c3b1896eb3e5a5a0a6da1d0c1e701242666f`.

Costs, rarity and required level come from the Area 52-specific DBC, not randomized/shared-catalog values. Spell identity and class/spec are matched to the existing stock talent catalog. One display entry is retained per native talent. When alternate source records disagree, the existing catalog ID takes precedence; these differences are retained in the audit JSON. Normal-quality records show no rarity-slot cost even when their raw QualityCost field contains 1.

20 Death Knight entries have no direct Browse category; these use the explicitly marked Everything Else fallback. Presence in the exported client table is not proof of current live-realm availability.

Counts by class: {'Mage': 15, 'Warrior': 14, 'Rogue': 13, 'Priest': 15, 'Shaman': 13, 'Druid': 14, 'Warlock': 13, 'Hunter': 13, 'Paladin': 14, 'DeathKnight': 20}. Rarity distribution: {'Normal': 40, 'Epic': 63, 'Rare': 27, 'Legendary': 13, 'Uncommon': 1}.

## Implementation scope

These entries support icons, search, rarity filters, level grouping and cost tooltips. They cannot spend points, assign native talent ranks or change learned selections. Stable display IDs are 20000000 + native talent ID, separate from advancement IDs and existing saved selections.

## Reviewed entries

| Class | Ability | A52 entry | Level | AP | Rarity | Rarity slots |
|---|---|---:|---:|---:|---|---:|
| DeathKnight | Anti-Magic Zone | 1292 | 71 | 6 | Legendary | 2 |
| DeathKnight | Bone Shield | 1258 | 71 | 4 | Epic | 1 |
| DeathKnight | Corpse Explosion | 1244 | 71 | 4 | Normal | 0 |
| DeathKnight | Dancing Rune Weapon | 1233 | 71 | 6 | Epic | 1 |
| DeathKnight | Deathchill | 1241 | 71 | 4 | Epic | 1 |
| DeathKnight | Frost Strike | 1239 | 71 | 4 | Normal | 0 |
| DeathKnight | Ghoul Frenzy | 1284 | 71 | 4 | Normal | 0 |
| DeathKnight | Heart Strike | 1229 | 71 | 4 | Normal | 0 |
| DeathKnight | Howling Blast | 1245 | 71 | 4 | Normal | 0 |
| DeathKnight | Hungering Cold | 1252 | 71 | 4 | Legendary | 1 |
| DeathKnight | Hysteria | 1227 | 71 | 4 | Epic | 1 |
| DeathKnight | Improved Icy Talons | 1293 | 71 | 4 | Normal | 0 |
| DeathKnight | Lichborne | 1288 | 71 | 4 | Epic | 1 |
| DeathKnight | Mark of Blood | 1224 | 71 | 4 | Epic | 1 |
| DeathKnight | Master of Ghouls | 1243 | 71 | 4 | Rare | 2 |
| DeathKnight | Rune Tap | 1218 | 71 | 4 | Rare | 1 |
| DeathKnight | Scourge Strike | 1289 | 71 | 4 | Normal | 0 |
| DeathKnight | Summon Gargoyle | 1253 | 71 | 6 | Normal | 0 |
| DeathKnight | Unbreakable Armor | 1240 | 71 | 4 | Epic | 2 |
| DeathKnight | Vampiric Blood | 1266 | 71 | 4 | Epic | 1 |
| Druid | Berserk | 1022 | 60 | 2 | Epic | 1 |
| Druid | Feral Charge | 616 | 1 | 2 | Epic | 1 |
| Druid | Force of Nature | 906 | 50 | 2 | Epic | 1 |
| Druid | Insect Swarm | 602 | 30 | 2 | Normal | 0 |
| Druid | Leader of the Pack | 620 | 40 | 2 | Rare | 2 |
| Druid | Mangle | 915 | 20 | 2 | Normal | 0 |
| Druid | Moonkin Form | 606 | 40 | 2 | Legendary | 1 |
| Druid | Nature's Swiftness | 631 | 30 | 2 | Epic | 1 |
| Druid | Starfall | 1021 | 60 | 2 | Legendary | 1 |
| Druid | Survival Instincts | 671 | 20 | 3 | Epic | 2 |
| Druid | Swiftmend | 635 | 40 | 2 | Normal | 0 |
| Druid | Tree of Life | 910 | 30 | 2 | Legendary | 1 |
| Druid | Typhoon | 1018 | 50 | 3 | Epic | 2 |
| Druid | Wild Growth | 1012 | 60 | 2 | Normal | 0 |
| Hunter | Aimed Shot | 707 | 20 | 2 | Rare | 1 |
| Hunter | Beast Mastery | 1072 | 60 | 2 | Epic | 1 |
| Hunter | Bestial Wrath | 720 | 40 | 3 | Legendary | 2 |
| Hunter | Black Arrow | 701 | 50 | 2 | Normal | 0 |
| Hunter | Chimera Shot | 1068 | 60 | 2 | Normal | 0 |
| Hunter | Counterattack | 699 | 30 | 2 | Normal | 0 |
| Hunter | Explosive Shot | 1078 | 60 | 2 | Normal | 0 |
| Hunter | Intimidation | 721 | 30 | 3 | Epic | 2 |
| Hunter | Readiness | 713 | 30 | 3 | Epic | 2 |
| Hunter | Scatter Shot | 932 | 20 | 3 | Epic | 2 |
| Hunter | Silencing Shot | 926 | 50 | 2 | Epic | 1 |
| Hunter | Trueshot Aura | 714 | 40 | 2 | Rare | 2 |
| Hunter | Wyvern Sting | 702 | 40 | 3 | Epic | 2 |
| Mage | Arcane Barrage | 950 | 60 | 2 | Normal | 0 |
| Mage | Arcane Power | 434 | 40 | 2 | Epic | 1 |
| Mage | Blast Wave | 404 | 30 | 3 | Epic | 2 |
| Mage | Cold Snap | 422 | 30 | 3 | Epic | 2 |
| Mage | Combustion | 408 | 40 | 2 | Epic | 1 |
| Mage | Deep Freeze | 960 | 60 | 3 | Epic | 2 |
| Mage | Dragon's Breath | 862 | 50 | 3 | Epic | 2 |
| Mage | Focus Magic | 1100 | 20 | 2 | Rare | 2 |
| Mage | Ice Barrier | 421 | 40 | 2 | Epic | 1 |
| Mage | Icy Veins | 419 | 20 | 2 | Epic | 1 |
| Mage | Living Bomb | 955 | 60 | 2 | Normal | 0 |
| Mage | Presence of Mind | 433 | 30 | 2 | Epic | 1 |
| Mage | Pyroblast | 401 | 20 | 2 | Normal | 0 |
| Mage | Slow | 856 | 50 | 2 | Epic | 1 |
| Mage | Summon Water Elemental | 867 | 50 | 2 | Epic | 1 |
| Paladin | Aura Mastery | 745 | 20 | 2 | Epic | 1 |
| Paladin | Avenger's Shield | 878 | 50 | 2 | Epic | 1 |
| Paladin | Beacon of Light | 1088 | 60 | 2 | Rare | 2 |
| Paladin | Blessing of Sanctuary | 3395 | 30 | 1 | Uncommon | 2 |
| Paladin | Crusader Strike | 941 | 1 | 2 | Normal | 0 |
| Paladin | Divine Favor | 744 | 30 | 2 | Epic | 1 |
| Paladin | Divine Illumination | 873 | 50 | 2 | Rare | 1 |
| Paladin | Divine Sacrifice | 1133 | 20 | 3 | Epic | 2 |
| Paladin | Divine Storm | 1082 | 15 | 2 | Normal | 0 |
| Paladin | Hammer of the Righteous | 1092 | 60 | 2 | Normal | 0 |
| Paladin | Holy Shield | 741 | 40 | 2 | Rare | 1 |
| Paladin | Holy Shock | 759 | 40 | 2 | Normal | 0 |
| Paladin | Repentance | 746 | 40 | 3 | Epic | 2 |
| Paladin | Seal of Command | 3410 | 20 | 1 | Rare | 2 |
| Priest | Circle of Healing | 933 | 50 | 2 | Normal | 0 |
| Priest | Desperate Prayer | 540 | 20 | 2 | Epic | 1 |
| Priest | Dispersion | 1005 | 60 | 3 | Legendary | 2 |
| Priest | Guardian Spirit | 1006 | 60 | 2 | Legendary | 1 |
| Priest | Inner Focus | 523 | 20 | 2 | Epic | 1 |
| Priest | Lightwell | 781 | 40 | 2 | Epic | 1 |
| Priest | Mind Flay | 550 | 20 | 2 | Normal | 0 |
| Priest | Pain Suppression | 896 | 50 | 2 | Legendary | 1 |
| Priest | Penance | 994 | 30 | 2 | Normal | 0 |
| Priest | Power Infusion | 516 | 40 | 2 | Epic | 1 |
| Priest | Psychic Horror | 1003 | 50 | 3 | Epic | 2 |
| Priest | Shadowform | 551 | 30 | 2 | Rare | 2 |
| Priest | Silence | 552 | 30 | 2 | Epic | 1 |
| Priest | Vampiric Embrace | 549 | 40 | 2 | Rare | 2 |
| Priest | Vampiric Touch | 899 | 50 | 2 | Normal | 0 |
| Rogue | Adrenaline Rush | 484 | 40 | 2 | Epic | 1 |
| Rogue | Blade Flurry | 488 | 30 | 3 | Epic | 1 |
| Rogue | Cold Blood | 509 | 30 | 2 | Epic | 1 |
| Rogue | Ghostly Strike | 514 | 20 | 2 | Rare | 1 |
| Rogue | Hemorrhage | 591 | 30 | 2 | Normal | 0 |
| Rogue | Hunger For Blood | 1049 | 60 | 2 | Epic | 1 |
| Rogue | Killing Spree | 1054 | 60 | 3 | Legendary | 2 |
| Rogue | Mutilate | 847 | 20 | 2 | Normal | 0 |
| Rogue | Premeditation | 528 | 40 | 2 | Rare | 1 |
| Rogue | Preparation | 512 | 30 | 3 | Epic | 2 |
| Rogue | Riposte | 513 | 20 | 2 | Normal | 0 |
| Rogue | Shadow Dance | 1059 | 60 | 2 | Epic | 1 |
| Rogue | Shadowstep | 844 | 1 | 2 | Epic | 1 |
| Shaman | Cleanse Spirit | 1061 | 40 | 2 | Rare | 2 |
| Shaman | Earth Shield | 831 | 50 | 2 | Rare | 1 |
| Shaman | Elemental Mastery | 560 | 40 | 2 | Epic | 1 |
| Shaman | Feral Spirit | 1038 | 60 | 3 | Legendary | 2 |
| Shaman | Lava Lash | 1122 | 1 | 2 | Normal | 0 |
| Shaman | Mana Tide Totem | 570 | 40 | 2 | Rare | 2 |
| Shaman | Nature's Swiftness | 571 | 30 | 2 | Epic | 1 |
| Shaman | Riptide | 1043 | 20 | 2 | Normal | 0 |
| Shaman | Shamanistic Rage | 827 | 50 | 2 | Rare | 2 |
| Shaman | Stormstrike | 637 | 1 | 2 | Normal | 0 |
| Shaman | Thunderstorm | 1033 | 60 | 3 | Epic | 2 |
| Shaman | Tidal Force | 564 | 60 | 2 | Epic | 1 |
| Shaman | Totem of Wrath | 3475 | 50 | 1 | Rare | 2 |
| Warlock | Chaos Bolt | 989 | 60 | 2 | Normal | 0 |
| Warlock | Conflagrate | 647 | 40 | 2 | Normal | 0 |
| Warlock | Curse of Exhaustion | 665 | 30 | 2 | Epic | 1 |
| Warlock | Dark Pact | 661 | 40 | 2 | Rare | 1 |
| Warlock | Demonic Empowerment | 979 | 40 | 2 | Rare | 1 |
| Warlock | Fel Domination | 680 | 30 | 2 | Epic | 1 |
| Warlock | Haunt | 1027 | 60 | 2 | Normal | 0 |
| Warlock | Metamorphosis | 984 | 60 | 2 | Legendary | 1 |
| Warlock | Shadowburn | 642 | 30 | 2 | Normal | 0 |
| Warlock | Shadowfury | 814 | 50 | 3 | Epic | 2 |
| Warlock | Soul Link | 689 | 20 | 2 | Rare | 2 |
| Warlock | Summon Felguard | 3465 | 50 | 1 | Epic | 2 |
| Warlock | Unstable Affliction | 810 | 50 | 2 | Normal | 0 |
| Warrior | Bladestorm | 965 | 60 | 2 | Legendary | 1 |
| Warrior | Bloodthirst | 475 | 40 | 2 | Normal | 0 |
| Warrior | Concussion Blow | 463 | 30 | 3 | Epic | 2 |
| Warrior | Death Wish | 3126 | 30 | 2 | Epic | 1 |
| Warrior | Devastate | 806 | 1 | 2 | Normal | 0 |
| Warrior | Heroic Fury | 970 | 50 | 2 | Epic | 1 |
| Warrior | Last Stand | 464 | 20 | 3 | Epic | 2 |
| Warrior | Mortal Strike | 449 | 40 | 2 | Rare | 1 |
| Warrior | Piercing Howl | 471 | 20 | 2 | Rare | 1 |
| Warrior | Rampage | 800 | 50 | 2 | Rare | 2 |
| Warrior | Shockwave | 974 | 60 | 3 | Epic | 2 |
| Warrior | Sweeping Strikes | 447 | 30 | 2 | Epic | 1 |
| Warrior | Titan's Grip | 969 | 60 | 2 | Rare | 1 |
| Warrior | Vigilance | 459 | 40 | 2 | Rare | 2 |

## Alternate Area 52 records

29 matches have alternate records with different cost or level metadata. Existing catalog IDs take precedence; availability of replacement IDs requires a later realm review.

- {'talentEntry': 969, 'candidates': [969, 3622], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 969, 'ae': 2, 'quality': 'Rare', 'rarityCost': 1, 'levels': [60, 60, 10]}, {'id': 3622, 'ae': 2, 'quality': 'Rare', 'rarityCost': 1, 'levels': [60, 60, 60]}]}
- {'talentEntry': 488, 'candidates': [488, 3141], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 488, 'ae': 3, 'quality': 'Epic', 'rarityCost': 1, 'levels': [30, 30, 30]}, {'id': 3141, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [30, 30, 30]}]}
- {'talentEntry': 1049, 'candidates': [1049, 3702], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1049, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [60, 60, 30]}, {'id': 3702, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [60, 60, 60]}]}
- {'talentEntry': 514, 'candidates': [514, 3167], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 514, 'ae': 2, 'quality': 'Rare', 'rarityCost': 1, 'levels': [20, 15, 15]}, {'id': 3167, 'ae': 2, 'quality': 'Rare', 'rarityCost': 1, 'levels': [20, 20, 20]}]}
- {'talentEntry': 1059, 'candidates': [1059, 3712], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1059, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [60, 60, 30]}, {'id': 3712, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [60, 60, 60]}]}
- {'talentEntry': 549, 'candidates': [549, 3202], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 549, 'ae': 2, 'quality': 'Rare', 'rarityCost': 2, 'levels': [40, 40, 20]}, {'id': 3202, 'ae': 2, 'quality': 'Rare', 'rarityCost': 2, 'levels': [40, 40, 40]}]}
- {'talentEntry': 564, 'candidates': [564, 3217], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 564, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [60, 20, 20]}, {'id': 3217, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [60, 60, 60]}]}
- {'talentEntry': 1038, 'candidates': [1038, 3691], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1038, 'ae': 3, 'quality': 'Legendary', 'rarityCost': 2, 'levels': [60, 60, 50]}, {'id': 3691, 'ae': 3, 'quality': 'Legendary', 'rarityCost': 2, 'levels': [50, 60, 50]}]}
- {'talentEntry': 1088, 'candidates': [1088, 3741], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1088, 'ae': 2, 'quality': 'Rare', 'rarityCost': 2, 'levels': [60, 60, 30]}, {'id': 3741, 'ae': 2, 'quality': 'Rare', 'rarityCost': 2, 'levels': [30, 60, 30]}]}
- {'talentEntry': 1218, 'candidates': [1218, 34762], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1218, 'ae': 4, 'quality': 'Rare', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34762, 'ae': 2, 'quality': 'Rare', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1224, 'candidates': [1224, 34763], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1224, 'ae': 4, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34763, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1227, 'candidates': [1227, 34764], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1227, 'ae': 4, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34764, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1266, 'candidates': [1266, 34776], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1266, 'ae': 4, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34776, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1229, 'candidates': [1229, 34765], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1229, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34765, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1233, 'candidates': [1233, 34766], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1233, 'ae': 6, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34766, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1288, 'candidates': [1288, 34778], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1288, 'ae': 4, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34778, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1241, 'candidates': [1241, 34769], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1241, 'ae': 4, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34769, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1293, 'candidates': [1293, 34781], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1293, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34781, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1252, 'candidates': [1252, 34773], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1252, 'ae': 4, 'quality': 'Legendary', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34773, 'ae': 2, 'quality': 'Legendary', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1240, 'candidates': [1240, 34768], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1240, 'ae': 4, 'quality': 'Epic', 'rarityCost': 2, 'levels': [71, 71, 71]}, {'id': 34768, 'ae': 2, 'quality': 'Epic', 'rarityCost': 2, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1239, 'candidates': [1239, 34767], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1239, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34767, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1245, 'candidates': [1245, 34772], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1245, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34772, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1244, 'candidates': [1244, 34771], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1244, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34771, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1243, 'candidates': [1243, 34770], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1243, 'ae': 4, 'quality': 'Rare', 'rarityCost': 2, 'levels': [71, 71, 71]}, {'id': 34770, 'ae': 2, 'quality': 'Rare', 'rarityCost': 2, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1292, 'candidates': [1292, 34780], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1292, 'ae': 6, 'quality': 'Legendary', 'rarityCost': 2, 'levels': [71, 71, 71]}, {'id': 34780, 'ae': 2, 'quality': 'Legendary', 'rarityCost': 2, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1284, 'candidates': [1284, 34777], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1284, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34777, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1258, 'candidates': [1258, 34775], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1258, 'ae': 4, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34775, 'ae': 2, 'quality': 'Epic', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1289, 'candidates': [1289, 34779], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1289, 'ae': 4, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34779, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}
- {'talentEntry': 1253, 'candidates': [1253, 34774], 'policy': 'Prefer existing catalog ID; alternate records retained for review', 'variants': [{'id': 1253, 'ae': 6, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}, {'id': 34774, 'ae': 2, 'quality': 'Normal', 'rarityCost': 1, 'levels': [71, 71, 71]}]}

## Differences from shared catalog

| Ability | Area 52 AP | Shared-catalog AP | Area 52 rarity / raw cost | Shared rarity / raw cost |
|---|---:|---:|---|---|
| Living Bomb | 2 | 3 | Normal / 0 | Normal / None |
| Arcane Barrage | 2 | 3 | Normal / 0 | Normal / None |
| Totem of Wrath | 1 | 2 | Rare / 2 | Rare / 2 |
| Summon Felguard | 1 | 2 | Epic / 2 | Epic / 2 |
| Beast Mastery | 2 | 2 | Epic / 1 | Rare / 2 |
| Explosive Shot | 2 | 3 | Normal / 0 | Normal / None |
| Seal of Command | 1 | 2 | Rare / 2 | Rare / 2 |
| Blessing of Sanctuary | 1 | 2 | Uncommon / 2 | Uncommon / 2 |
| Rune Tap | 4 | 2 | Rare / 1 | Rare / 1 |
| Mark of Blood | 4 | 2 | Epic / 1 | Epic / 1 |
| Hysteria | 4 | 2 | Epic / 1 | Epic / 1 |
| Vampiric Blood | 4 | 2 | Epic / 1 | Epic / 1 |
| Heart Strike | 4 | 2 | Normal / 1 | Normal / 1 |
| Dancing Rune Weapon | 6 | 4 | Epic / 1 | Epic / 1 |
| Lichborne | 4 | 2 | Epic / 1 | Epic / 1 |
| Deathchill | 4 | 2 | Epic / 1 | Epic / 1 |
| Improved Icy Talons | 4 | 2 | Normal / 1 | Normal / 1 |
| Hungering Cold | 4 | 2 | Legendary / 1 | Legendary / 1 |
| Unbreakable Armor | 4 | 2 | Epic / 2 | Epic / 2 |
| Frost Strike | 4 | 2 | Normal / 1 | Normal / 1 |
| Howling Blast | 4 | 2 | Normal / 1 | Normal / 1 |
| Corpse Explosion | 4 | 2 | Normal / 1 | Normal / 1 |
| Master of Ghouls | 4 | 2 | Rare / 2 | Rare / 2 |
| Anti-Magic Zone | 6 | 4 | Legendary / 2 | Legendary / 2 |
| Ghoul Frenzy | 4 | 2 | Normal / 1 | Normal / 1 |
| Bone Shield | 4 | 2 | Epic / 1 | Epic / 1 |
| Scourge Strike | 4 | 2 | Normal / 1 | Normal / 1 |
| Summon Gargoyle | 6 | 4 | Normal / 1 | Normal / 1 |
