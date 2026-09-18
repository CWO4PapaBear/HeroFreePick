# Starting-ability and Area 52 level-one audit

Auto Shot was missing from custom modes because only the Classic supplement was imported. Added custom entry 24000075: native spell 75, Hunter Marksmanship, level 1, 2 AP, no rarity gems. Ascension source entry 392 uses custom spell 965202 at the same cost/level. Classic entry 19200000 remains unchanged.

## Stock automatic grants

Reviewed stock class-skill automatic grants (`classic-starting.json`), the empty stock playercreateinfo_spell_custom table, and the server StartingSpells allowlist. All ordinary non-DK starting active abilities are present after this fix. Fireball, Heroic Strike, Sinister Strike, Raptor Strike, Lesser Heal, Smite, Healing Wave, Lightning Bolt, Healing Touch, Wrath, Shadow Bolt and Holy Light are already paid level-one choices. Frost Armor, Battle Stance, Eviscerate, Demon Skin and Seal of Righteousness are free members of their paid Masteries; do not charge twice.

The DK redesign is intentionally preserved: Death Coil, Death Grip, Rune Strike, Runic Focus and Forceful Deflection do not all become level-one purchases merely because a stock DK starts at 55. Frost Fever/Blood Plague support records are not promoted to independent buttons. Hidden DND effects, racial abilities, weapon/armor proficiencies and passive support grants are outside the purchasable active-spell audit. The old Seal of Righteousness wrapper 20154 is represented by native usable spell 21084.

## Area 52 paid level-one reference

Source: area-52 patch-D CharacterAdvancement.dbc, joined to shared English JSON by advancement ID. Uses the realm-specific AP, quality and level fields rather than the shared JSON defaults. Filters Ability records with positive AP, level 1, standard classes, and excludes shared flags & 9 as used in the existing import audit. This is a client-data reference, not proof every row was simultaneously offered on the live realm. Duplicated advancement variants are retained for traceability.

| Class | Ability | Source entry | AP | Rarity cost | Our Hero-mode match (level; AP or controller) |
|---|---|---:|---:|---|---|
| DeathKnight | Dominate Undead | 1153 | 4 | 2 Epic | 23000891 (level 1; 4 AP); 25000899 (level 1; group 23000891) |
| DeathKnight | Dominate Undead | 34703 | 4 | 2 Epic | 23000891 (level 1; 4 AP); 25000899 (level 1; group 23000891) |
| Druid | Bear Form | 2855 | 1 | 1 Epic | 201 (level 1; group 21954710) |
| Druid | Bear Form | 34878 | 1 | 1 Epic | 201 (level 1; group 21954710) |
| Druid | Cat Form | 2728 | 1 | 1 Epic | 74 (level 20; group 21954710) |
| Druid | Cat Form | 34868 | 1 | 1 Epic | 74 (level 20; group 21954710) |
| Druid | Demoralizing Roar | 8 | 2 | 1 Uncommon | 8 (level 1; 2 AP) |
| Druid | Demoralizing Roar | 2662 | 2 | 1 Uncommon | 8 (level 1; 2 AP) |
| Druid | Feral Charge | 616 | 2 | 1 Epic | 20000804 (level 30; 2 AP) |
| Druid | Feral Charge | 3269 | 2 | 1 Epic | 20000804 (level 30; 2 AP) |
| Druid | Feral Shapeshift Mastery | 1370 | 1 | 1 Epic | 21954710 (level 1; 2 AP) |
| Druid | Feral Shapeshift Mastery | 34808 | 1 | 1 Epic | 21954710 (level 1; 2 AP) |
| Druid | Growl | 2881 | 2 | 0 Normal | 227 (level 1; 2 AP) |
| Druid | Healing Touch | 188 | 2 | 0 Normal | 188 (level 1; 2 AP) |
| Druid | Healing Touch | 2842 | 2 | 0 Normal | 188 (level 1; 2 AP) |
| Druid | Mark of the Wild | 100 | 2 | 2 Uncommon | 100 (level 1; 2 AP) |
| Druid | Mark of the Wild | 2754 | 2 | 2 Uncommon | 100 (level 1; 2 AP) |
| Druid | Maul | 228 | 2 | 0 Normal | 228 (level 1; 2 AP) |
| Druid | Maul | 2882 | 2 | 0 Normal | 228 (level 1; 2 AP) |
| Druid | Moonfire | 257 | 2 | 0 Normal | 257 (level 1; 2 AP) |
| Druid | Moonfire | 2911 | 2 | 0 Normal | 257 (level 1; 2 AP) |
| Druid | Prowl | 191 | 2 | 1 Epic | 191 (level 20; 2 AP) |
| Druid | Prowl | 2845 | 2 | 1 Epic | 191 (level 20; 2 AP) |
| Druid | Rejuvenation | 77 | 2 | 0 Normal | 77 (level 1; 2 AP) |
| Druid | Rejuvenation | 2731 | 2 | 0 Normal | 77 (level 1; 2 AP) |
| Druid | Rip | 95 | 2 | 0 Normal | 95 (level 1; 2 AP) |
| Druid | Rip | 2749 | 2 | 0 Normal | 95 (level 1; 2 AP) |
| Druid | Swipe (Cat) | 379 | 2 | 0 Normal | 379 (level 1; 2 AP) |
| Druid | Swipe (Cat) | 3032 | 2 | 0 Normal | 379 (level 1; 2 AP) |
| Druid | Thorns | 34 | 2 | 1 Uncommon | 34 (level 1; 2 AP) |
| Druid | Thorns | 2688 | 2 | 1 Uncommon | 34 (level 1; 2 AP) |
| Druid | Wrath | 187 | 2 | 0 Normal | 187 (level 1; 2 AP) |
| Druid | Wrath | 2841 | 2 | 0 Normal | 187 (level 1; 2 AP) |
| Hunter | Arcane Shot | 176 | 2 | 0 Normal | 176 (level 1; 2 AP) |
| Hunter | Arcane Shot | 2830 | 2 | 0 Normal | 176 (level 1; 2 AP) |
| Hunter | Aspect of the Hawk | 2923 | 1 | 2 Rare | 269 (level 1; group 21092156) |
| Hunter | Aspect of the Hawk | 34849 | 1 | 2 Rare | 269 (level 1; group 21092156) |
| Hunter | Aspect of the Monkey | 2922 | 1 | 2 Rare | 268 (level 1; group 21092156) |
| Hunter | Aspect of the Monkey | 34848 | 1 | 2 Rare | 268 (level 1; group 21092156) |
| Hunter | Auto Shot | 392 | 2 | 0 Normal | 24000075 (level 1; 2 AP) |
| Hunter | Auto Shot | 3045 | 2 | 0 Normal | 24000075 (level 1; 2 AP) |
| Hunter | Disengage | 79 | 3 | 2 Legendary | 79 (level 20; 3 AP) |
| Hunter | Disengage | 2733 | 3 | 2 Legendary | 79 (level 20; 3 AP) |
| Hunter | Hunter Aspect Mastery | 1313 | 1 | 2 Rare | 21092156 (level 1; 2 AP) |
| Hunter | Hunter Aspect Mastery | 34788 | 1 | 2 Rare | 21092156 (level 1; 2 AP) |
| Hunter | Hunter's Mark | 101 | 2 | 1 Rare | 101 (level 1; 2 AP) |
| Hunter | Hunter's Mark | 2755 | 2 | 1 Rare | 101 (level 1; 2 AP) |
| Hunter | Mongoose Bite | 112 | 2 | 0 Normal | 112 (level 1; 2 AP) |
| Hunter | Mongoose Bite | 2766 | 2 | 0 Normal | 112 (level 1; 2 AP) |
| Hunter | Raptor Strike | 171 | 2 | 0 Normal | 171 (level 1; 2 AP) |
| Hunter | Raptor Strike | 2825 | 2 | 0 Normal | 171 (level 1; 2 AP) |
| Hunter | Serpent Sting | 139 | 2 | 0 Normal | 139 (level 1; 2 AP) |
| Hunter | Serpent Sting | 2793 | 2 | 0 Normal | 139 (level 1; 2 AP) |
| Hunter | Steady Shot | 373 | 2 | 0 Normal | 373 (level 30; 2 AP) |
| Hunter | Steady Shot | 3026 | 2 | 0 Normal | 373 (level 30; 2 AP) |
| Hunter | Tame Beast | 391 | 4 | 2 Epic | 23965200 (level 1; 4 AP); 25001515 (level 1; group 23965200) |
| Hunter | Tame Beast | 3044 | 4 | 2 Epic | 23965200 (level 1; 4 AP); 25001515 (level 1; group 23965200) |
| Mage | Arcane Intellect | 108 | 2 | 2 Uncommon | 108 (level 1; 2 AP) |
| Mage | Arcane Intellect | 2762 | 2 | 2 Uncommon | 108 (level 1; 2 AP) |
| Mage | Arcane Missiles | 185 | 2 | 0 Normal | 185 (level 1; 2 AP) |
| Mage | Arcane Missiles | 2839 | 2 | 0 Normal | 185 (level 1; 2 AP) |
| Mage | Blink | 137 | 3 | 3 Legendary | 137 (level 20; 3 AP) |
| Mage | Blink | 2791 | 3 | 3 Legendary | 137 (level 20; 3 AP) |
| Mage | Brilliance Aura | 1189 | 2 | 2 Rare | No matching custom entry; requires separate review |
| Mage | Brilliance Aura | 34739 | 2 | 2 Rare | No matching custom entry; requires separate review |
| Mage | Conjure Food | 47 | 1 | 0 Normal | 47 (level 1; 1 AP) |
| Mage | Conjure Food | 2701 | 1 | 0 Normal | 47 (level 1; 1 AP) |
| Mage | Conjure Water | 202 | 1 | 0 Normal | 202 (level 1; 1 AP) |
| Mage | Conjure Water | 2856 | 1 | 0 Normal | 202 (level 1; 1 AP) |
| Mage | Fire Blast | 149 | 2 | 0 Normal | 149 (level 1; 2 AP) |
| Mage | Fire Blast | 2803 | 2 | 0 Normal | 149 (level 1; 2 AP) |
| Mage | Fireball | 18 | 2 | 0 Normal | 18 (level 1; 2 AP) |
| Mage | Fireball | 2672 | 2 | 0 Normal | 18 (level 1; 2 AP) |
| Mage | Frost Armor | 2675 | 1 | 2 Rare | 21 (level 1; group 21092155) |
| Mage | Frost Armor | 34834 | 1 | 2 Rare | 21 (level 1; group 21092155) |
| Mage | Frostbolt | 10 | 2 | 0 Normal | 10 (level 1; 2 AP) |
| Mage | Frostbolt | 2664 | 2 | 0 Normal | 10 (level 1; 2 AP) |
| Mage | Mage Armor | 2864 | 1 | 2 Rare | 210 (level 34; group 21092155) |
| Mage | Mage Armor | 34839 | 1 | 2 Rare | 210 (level 34; group 21092155) |
| Mage | Mage Armor Mastery | 1312 | 1 | 2 Rare | 21092155 (level 1; 2 AP) |
| Mage | Mage Armor Mastery | 34787 | 1 | 2 Rare | 21092155 (level 1; 2 AP) |
| Mage | Mana-forged Barrier | 1300 | 2 | 1 Epic | No matching custom entry; requires separate review |
| Mage | Mana-forged Barrier | 34782 | 2 | 1 Epic | No matching custom entry; requires separate review |
| Mage | Tame Dragonkin | 1195 | 4 | 2 Epic | 23091634 (level 1; 4 AP); 25093558 (level 1; group 23091634) |
| Mage | Tame Dragonkin | 34745 | 4 | 2 Epic | 23091634 (level 1; 4 AP); 25093558 (level 1; group 23091634) |
| Paladin | Blessing Mastery | 1369 | 1 | 2 Uncommon | 21954711 (level 1; 2 AP) |
| Paladin | Blessing Mastery | 34807 | 1 | 2 Uncommon | 21954711 (level 1; 2 AP) |
| Paladin | Blessing of Might | 2937 | 1 | 2 Uncommon | 283 (level 1; group 21954711) |
| Paladin | Blessing of Might | 34893 | 1 | 2 Uncommon | 283 (level 1; group 21954711) |
| Paladin | Blessing of Wisdom | 2938 | 1 | 2 Uncommon | 284 (level 1; group 21954711) |
| Paladin | Blessing of Wisdom | 34894 | 1 | 2 Uncommon | 284 (level 1; group 21954711) |
| Paladin | Concentration Aura | 2939 | 1 | 2 Uncommon | 285 (level 22; group 21092157) |
| Paladin | Concentration Aura | 34850 | 1 | 2 Uncommon | 285 (level 22; group 21092157) |
| Paladin | Consecration | 314 | 2 | 0 Normal | 314 (level 1; 2 AP) |
| Paladin | Consecration | 2968 | 2 | 0 Normal | 314 (level 1; 2 AP) |
| Paladin | Crusader Strike | 941 | 2 | 0 Normal | 20001823 (level 50; 2 AP) |
| Paladin | Crusader Strike | 3594 | 2 | 0 Normal | 20001823 (level 50; 2 AP) |
| Paladin | Devotion Aura | 2687 | 1 | 2 Uncommon | 33 (level 1; group 21092157) |
| Paladin | Devotion Aura | 34835 | 1 | 2 Uncommon | 33 (level 1; group 21092157) |
| Paladin | Holy Light | 55 | 2 | 0 Normal | 55 (level 1; 2 AP) |
| Paladin | Holy Light | 2709 | 2 | 0 Normal | 55 (level 1; 2 AP) |
| Paladin | Judgement Mastery | 1324 | 1 | 2 Rare | 21092169 (level 1; 2 AP) |
| Paladin | Judgement Mastery | 34798 | 1 | 2 Rare | 21092169 (level 1; 2 AP) |
| Paladin | Judgement of Light | 2955 | 1 | 2 Rare | 301 (level 1; group 21092169) |
| Paladin | Judgement of Light | 34855 | 1 | 2 Rare | 301 (level 1; group 21092169) |
| Paladin | Judgement of Wisdom | 3020 | 1 | 2 Rare | 367 (level 1; group 21092169) |
| Paladin | Judgement of Wisdom | 34862 | 1 | 2 Rare | 367 (level 1; group 21092169) |
| Paladin | Paladin Aura Mastery | 1314 | 1 | 2 Uncommon | 21092157 (level 1; 2 AP) |
| Paladin | Paladin Aura Mastery | 34789 | 1 | 2 Uncommon | 21092157 (level 1; 2 AP) |
| Paladin | Righteous Fury | 313 | 2 | 1 Uncommon | 313 (level 1; 2 AP) |
| Paladin | Righteous Fury | 2967 | 2 | 1 Uncommon | 313 (level 1; 2 AP) |
| Paladin | Seal Mastery | 1366 | 1 | 2 Rare | 21954707 (level 1; 2 AP) |
| Paladin | Seal Mastery | 34804 | 1 | 2 Rare | 21954707 (level 1; 2 AP) |
| Paladin | Seal of Righteousness | 2959 | 1 | 2 Rare | 305 (level 1; group 21954707) |
| Paladin | Seal of Righteousness | 34899 | 1 | 2 Rare | 305 (level 1; group 21954707) |
| Paladin | Seal of Wisdom | 2951 | 1 | 2 Rare | 297 (level 38; group 21954707) |
| Paladin | Seal of Wisdom | 34897 | 1 | 2 Rare | 297 (level 38; group 21954707) |
| Paladin | Shield of Righteousness | 368 | 2 | 0 Normal | 368 (level 1; 2 AP) |
| Paladin | Shield of Righteousness | 3021 | 2 | 0 Normal | 368 (level 1; 2 AP) |
| Priest | Greater Heal | 142 | 2 | 0 Normal | 142 (level 1; 2 AP) |
| Priest | Greater Heal | 2796 | 2 | 0 Normal | No matching custom entry; requires separate review |
| Priest | Power Word: Fortitude | 105 | 2 | 2 Uncommon | 105 (level 1; 2 AP) |
| Priest | Power Word: Fortitude | 2759 | 2 | 2 Uncommon | 105 (level 1; 2 AP) |
| Priest | Renew | 20 | 2 | 0 Normal | 20 (level 1; 2 AP) |
| Priest | Renew | 2674 | 2 | 0 Normal | 20 (level 1; 2 AP) |
| Priest | Shadow Word: Pain | 49 | 2 | 0 Normal | 49 (level 1; 2 AP) |
| Priest | Shadow Word: Pain | 2703 | 2 | 0 Normal | 49 (level 1; 2 AP) |
| Priest | Smite | 45 | 2 | 0 Normal | 45 (level 1; 2 AP) |
| Priest | Smite | 2699 | 2 | 0 Normal | 45 (level 1; 2 AP) |
| Rogue | Advanced Finishing Move Mastery | 1367 | 1 | 2 Rare | 21954708 (level 1; 2 AP) |
| Rogue | Advanced Finishing Move Mastery | 34805 | 1 | 2 Rare | 21954708 (level 1; 2 AP) |
| Rogue | Backstab | 3 | 2 | 0 Normal | 3 (level 1; 2 AP) |
| Rogue | Backstab | 2657 | 2 | 0 Normal | 3 (level 1; 2 AP) |
| Rogue | Eviscerate | 147 | 2 | 0 Normal | 147 (level 1; group 21006002) |
| Rogue | Eviscerate | 2801 | 2 | 0 Normal | 147 (level 1; group 21006002) |
| Rogue | Pick Pocket | 85 | 1 | 0 Normal | 85 (level 1; 1 AP) |
| Rogue | Pick Pocket | 2739 | 1 | 0 Normal | 85 (level 1; 1 AP) |
| Rogue | Recuperate | 34902 | 1 | 2 Rare | 22965425 (level 10; group 21954708) |
| Rogue | Shadowstep | 844 | 2 | 1 Epic | 20001714 (level 50; 2 AP) |
| Rogue | Shadowstep | 3497 | 2 | 1 Epic | 20001714 (level 50; 2 AP) |
| Rogue | Sinister Strike | 124 | 2 | 0 Normal | 124 (level 1; 2 AP) |
| Rogue | Sinister Strike | 2778 | 2 | 0 Normal | 124 (level 1; 2 AP) |
| Rogue | Slice and Dice | 2840 | 1 | 2 Rare | 186 (level 1; group 21954708) |
| Rogue | Slice and Dice | 34876 | 1 | 2 Rare | 186 (level 1; group 21954708) |
| Rogue | Stealth | 127 | 2 | 1 Epic | 127 (level 1; 2 AP) |
| Rogue | Stealth | 2781 | 2 | 1 Epic | 127 (level 1; 2 AP) |
| Shaman | Earth Shock | 238 | 2 | 0 Normal | 238 (level 1; group 21006001) |
| Shaman | Earth Shock | 2892 | 2 | 0 Normal | 238 (level 1; group 21006001) |
| Shaman | Earth Totem Mastery | 1319 | 1 | 2 Uncommon | 21092163 (level 1; 2 AP) |
| Shaman | Earth Totem Mastery | 34794 | 1 | 2 Uncommon | 21092163 (level 1; 2 AP) |
| Shaman | Fire Totem Mastery | 1316 | 1 | 2 Rare | 21092159 (level 1; 2 AP) |
| Shaman | Fire Totem Mastery | 34791 | 1 | 2 Rare | 21092159 (level 1; 2 AP) |
| Shaman | Flametongue Totem | 34888 | 1 | 1 Uncommon | 252 (level 28; group 21092159) |
| Shaman | Healing Wave | 24 | 2 | 0 Normal | 24 (level 1; 2 AP) |
| Shaman | Healing Wave | 2678 | 2 | 0 Normal | 24 (level 1; 2 AP) |
| Shaman | Lava Lash | 1122 | 2 | 0 Normal | 20002249 (level 45; 2 AP) |
| Shaman | Lava Lash | 3775 | 2 | 0 Normal | 20002249 (level 45; 2 AP) |
| Shaman | Lightning Bolt | 29 | 2 | 0 Normal | 29 (level 1; 2 AP) |
| Shaman | Lightning Bolt | 2683 | 2 | 0 Normal | 29 (level 1; 2 AP) |
| Shaman | Lightning Shield | 23 | 2 | 2 Rare | 23 (level 1; 2 AP) |
| Shaman | Lightning Shield | 2677 | 2 | 2 Rare | 23 (level 1; 2 AP) |
| Shaman | Searing Totem | 2833 | 1 | 1 Rare | 179 (level 1; group 21092159) |
| Shaman | Searing Totem | 34874 | 1 | 1 Rare | 179 (level 1; group 21092159) |
| Shaman | Stoneclaw Totem | 2860 | 1 | 1 Rare | 206 (level 1; group 21092163) |
| Shaman | Stoneclaw Totem | 34880 | 1 | 1 Uncommon | 206 (level 1; group 21092163) |
| Shaman | Stoneskin Totem | 2895 | 1 | 1 Rare | 241 (level 1; group 21092163) |
| Shaman | Stoneskin Totem | 34883 | 1 | 1 Uncommon | 241 (level 1; group 21092163) |
| Shaman | Stormstrike | 637 | 2 | 0 Normal | 20000901 (level 40; 2 AP) |
| Shaman | Stormstrike | 3290 | 2 | 0 Normal | 20000901 (level 40; 2 AP) |
| Shaman | Tether Elemental | 1615 | 4 | 2 Epic | 23091606 (level 1; 4 AP); 25093569 (level 1; group 23091606) |
| Shaman | Tether Elemental | 34824 | 4 | 2 Epic | 23091606 (level 1; 4 AP); 25093569 (level 1; group 23091606) |
| Warlock | Corruption | 22 | 2 | 0 Normal | 22 (level 1; 2 AP) |
| Warlock | Corruption | 2676 | 2 | 0 Normal | 22 (level 1; 2 AP) |
| Warlock | Curse of Agony | 87 | 2 | 0 Normal | 87 (level 1; 2 AP) |
| Warlock | Curse of Agony | 2741 | 2 | 0 Normal | 87 (level 1; 2 AP) |
| Warlock | Curse of Weakness | 67 | 2 | 1 Uncommon | 67 (level 1; 2 AP) |
| Warlock | Curse of Weakness | 2721 | 2 | 1 Uncommon | 67 (level 1; 2 AP) |
| Warlock | Demon Skin | 2713 | 1 | 2 Rare | 59 (level 1; group 21092166) |
| Warlock | Demon Skin | 34837 | 1 | 2 Rare | 59 (level 1; group 21092166) |
| Warlock | Enslave Demon | 1205 | 4 | 2 Epic | 97 (level 30; 2 AP); 23000890 (level 1; 4 AP); 25000896 (level 1; group 23000890) |
| Warlock | Enslave Demon | 34755 | 4 | 2 Epic | 97 (level 30; 2 AP); 23000890 (level 1; 4 AP); 25000896 (level 1; group 23000890) |
| Warlock | Immolate | 26 | 2 | 0 Normal | 26 (level 1; 2 AP) |
| Warlock | Immolate | 2680 | 2 | 0 Normal | 26 (level 1; 2 AP) |
| Warlock | Life Tap | 107 | 2 | 2 Rare | 107 (level 1; 2 AP) |
| Warlock | Life Tap | 2761 | 2 | 2 Rare | 107 (level 1; 2 AP) |
| Warlock | Shadow Bolt | 58 | 2 | 0 Normal | 58 (level 1; 2 AP) |
| Warlock | Shadow Bolt | 2712 | 2 | 0 Normal | 58 (level 1; 2 AP) |
| Warlock | Summon Imp | 60 | 2 | 2 Rare | 60 (level 1; group 21954705) |
| Warlock | Summon Imp | 2714 | 2 | 2 Rare | 60 (level 1; group 21954705) |
| Warlock | Summoner's Armor | 1311 | 1 | 2 Rare | 22701521 (level 1; group 21092166) |
| Warlock | Summoner's Armor | 34910 | 1 | 2 Rare | 22701521 (level 1; group 21092166) |
| Warlock | Warlock Armor Mastery | 1321 | 1 | 2 Rare | 21092166 (level 1; 2 AP) |
| Warlock | Warlock Armor Mastery | 34796 | 1 | 2 Rare | 21092166 (level 1; 2 AP) |
| Warrior | Battle Shout | 2877 | 1 | 2 Uncommon | 223 (level 1; group 21954709) |
| Warrior | Battle Shout | 34882 | 1 | 2 Uncommon | 223 (level 1; group 21954709) |
| Warrior | Battle Stance | 2806 | 1 | 2 Rare | 152 (level 1; group 21954704) |
| Warrior | Battle Stance | 34872 | 1 | 2 Rare | 152 (level 1; group 21954704) |
| Warrior | Bloodrage | 159 | 2 | 1 Rare | 159 (level 1; 2 AP) |
| Warrior | Bloodrage | 2813 | 2 | 1 Rare | 159 (level 1; 2 AP) |
| Warrior | Charge | 2663 | 2 | 1 Epic | 2663 (level 1; 2 AP) |
| Warrior | Charge | 34830 | 2 | 1 Epic | 2663 (level 1; 2 AP) |
| Warrior | Defensive Stance | 2659 | 1 | 2 Rare | 5 (level 1; group 21954704) |
| Warrior | Defensive Stance | 34864 | 1 | 2 Rare | 5 (level 1; group 21954704) |
| Warrior | Demoralizing Shout | 34869 | 1 | 2 Uncommon | 103 (level 14; group 21954709) |
| Warrior | Devastate | 806 | 2 | 0 Normal | 20001666 (level 50; 2 AP) |
| Warrior | Hamstring | 121 | 2 | 2 Rare | 121 (level 1; 2 AP) |
| Warrior | Hamstring | 2775 | 2 | 2 Rare | 121 (level 1; 2 AP) |
| Warrior | Heroic Strike | 7 | 2 | 0 Normal | 7 (level 1; 2 AP) |
| Warrior | Heroic Strike | 2661 | 2 | 0 Normal | 7 (level 1; 2 AP) |
| Warrior | Rend | 76 | 2 | 0 Normal | 76 (level 1; 2 AP) |
| Warrior | Rend | 2730 | 2 | 0 Normal | 76 (level 1; 2 AP) |
| Warrior | Shield Block | 155 | 2 | 1 Rare | 155 (level 1; 2 AP) |
| Warrior | Shield Block | 2809 | 2 | 1 Rare | 155 (level 1; 2 AP) |
| Warrior | Shout Mastery | 1368 | 1 | 2 Uncommon | 21954709 (level 1; 2 AP) |
| Warrior | Shout Mastery | 34806 | 1 | 2 Uncommon | 21954709 (level 1; 2 AP) |
| Warrior | Slam | 110 | 2 | 0 Normal | 110 (level 30; 2 AP) |
| Warrior | Slam | 2764 | 2 | 0 Normal | 110 (level 30; 2 AP) |
| Warrior | Stance Mastery | 1363 | 1 | 2 Rare | 21954704 (level 1; 2 AP) |
| Warrior | Stance Mastery | 34801 | 1 | 2 Rare | 21954704 (level 1; 2 AP) |
| Warrior | Thunder Clap | 216 | 2 | 0 Normal | 216 (level 1; 2 AP) |
| Warrior | Thunder Clap | 2870 | 2 | 0 Normal | 216 (level 1; 2 AP) |
| Warrior | Victory Rush | 342 | 2 | 0 Normal | 342 (level 1; 2 AP) |
| Warrior | Victory Rush | 2996 | 2 | 0 Normal | 342 (level 1; 2 AP) |

223 source records; 114 distinct class/name choices. This reference does not override our accepted level, Mastery, or DK policies. Missing matches are a review list, not automatically imported custom spells.
