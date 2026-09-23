# Server spell tooltip resolution

Staged client-only update, not installed or launcher-published. Uses the PTR Abomination audit export (Spell.dbc plus SQL spell_dbc overrides) and exported duration/range/radius tables. Later Abomination additions do not change these player spell records. Source hashes and before/after descriptions are retained in audit.json; raw DBC/SQL exports are not distributed.

Reviewed 2,955 installed server spell descriptions. 175 contain unresolved syntax; 110 now resolve completely and 65 remain yellow. Counts are spell/rank descriptions, not unique abilities or proof of gameplay implementation.

Serpent Sting (1978) uses its server formula: 4 damage per tick, 5 ticks over 15 seconds, plus 20% ranged attack power. At 500 ranged AP its displayed total is 120. AP/RAP/Spirit formula operands are read on hover; these are spell-definition tooltip values, not predictions of final combat damage after all talents, mitigation or custom handlers.

Fixed signed cooldown arithmetic, numeric duration operands, periodic totals, combo-point fields, effect multipliers, target counts, referenced spell fields and supported arithmetic. Unknown named variables, unsupported character-stat/weapon formulas and custom syntax stay yellow. Existing missing-implementation warnings are preserved. Classic uses its existing path.

Close WoW and run Install-Client.py --wow-closed in WSL. It validates hashes, backs up changed files, and refuses unfamiliar client changes. The existing Shift toggle and paragraph spacing are preserved. No MPQ or server update is required. Launch Wow.exe directly while testing this local package.

Validation: Lua 5.1 compilation and renderer tests cover Serpent Sting totals at multiple RAP values, stat API failure, negative cooldowns, cross-spell ticks, unsupported expression rejection, yellow unresolved text, existing implementation warnings and Classic isolation. Visual testing in game is still required.

## Descriptions still needing data or formula support

| Spell | Name | Unresolved expressions |
|---|---|---|
| 8936 | Regrowth | ${$m2*7*$<mult>} |
| 92171 | Arcane Ward | @learns:92170@ |
| 879 | Exorcism | ${$M1+0.15*$SPH+0.15*$AP}, ${$m1+0.15*$SPH+0.15*$AP} |
| 51730 | Earthliving Weapon | $<chance> |
| 45462 | Plague Strike | $<bonus>, $<weapon> |
| 1454 | Life Tap | ${$m1*$<mult>+$SPS*.5*$<mult>} |
| 44572 | Deep Freeze | ${$71757M1*$<mult>}, ${$71757m1*$<mult>} |
| 10 | Blizzard | ${$42208m1*8*$<mult>} |
| 2812 | Holy Wrath | ${$M1+0.07*$SPH+0.07*$AP}, ${$m1+0.07*$SPH+0.07*$AP} |
| 20375 | Seal of Command | ${0.19*$MW+0.08*$AP+0.13*$SPH}, ${0.19*$mw+0.08*$AP+0.13*$SPH}, ${0.36*$MW}, ${0.36*$mw} |
| 954553 | Dispatch | ${$M1+(($b1*1)+$AP*0.07)*$<mult>}, ${$M1+(($b1*2)+$AP*0.14)*$<mult>}, ${$M1+(($b1*3)+$AP*0.21)*$<mult>}, ${$M1+(($b1*4)+$AP*0.28)*$<mult>}, ${$M1+(($b1*5)+$AP*0.35)*$<mult>}, ${$m1+(($b1*1)+$AP*0.056)*$<mult>}, ${$m1+(($b1*2)+$AP*0.112)*$<mult>}, ${$m1+(($b1*3)+$AP*0.168)*$<mult>}, ${$m1+(($b1*4)+$AP*0.224)*$<mult>}, ${$m1+(($b1*5)+$AP*0.28)*$<mult>} |
| 760050 | Gloomblade | ${$760193m1+$760193ppl1+($SP+$AP)*0.0779} |
| 760060 | Divine Star | $?s760194/s760195/s760196[][${$760062m1+$760062ppl1+$bh*0, ${($760062m1+$760062ppl1+$bh*0.156)*(($760194m1/100)+1)}, ${($760062m1+$760062ppl1+$bh*0.156)*(($760195m1/100)+1)}, ${($760062m1+$760062ppl1+$bh*0.156)*(($760196m1/100)+1)} |
| 1079 | Rip | ${($m1+$b1*1+0.01*$AP)*$<dur>}, ${($m1+$b1*2+0.02*$AP)*$<dur>}, ${($m1+$b1*3+0.03*$AP)*$<dur>}, ${($m1+$b1*4+0.04*$AP)*$<dur>}, ${($m1+$b1*5+0.05*$AP)*$<dur>} |
| 47541 | Death Coil | $<damage>, $<healing> |
| 760210 | Nature Ward | @learns:92170@ |
| 116 | Frostbolt | ${$M2*$<mult>}, ${$m2*$<mult>} |
| 120 | Cone of Cold | ${$M2*$<mult>}, ${$m2*$<mult>} |
| 1943 | Rupture | $<dur1>, $<dur2>, $<dur3>, $<dur4>, $<dur5> |
| 122 | Frost Nova | ${$M1*$<mult>}, ${$m1*$<mult>} |
| 136 | Mend Pet | $<total> |
| 139 | Renew | $<total> |
| 954809 | Crimson Tempest | ${$m1+$b1*1+($SP+$AP)*1*1*0.015+($SP+$AP)*0.02}, ${$m1+$b1*2+($SP+$AP)*2*2*0.015+($SP+$AP)*0.02}, ${$m1+$b1*3+($SP+$AP)*3*3*0.015+($SP+$AP)*0.02}, ${$m1+$b1*4+($SP+$AP)*4*4*0.015+($SP+$AP)*0.02}, ${$m1+$b1*5+($SP+$AP)*5*5*0.015+($SP+$AP)*0.02}, ${($m3+$b3*1+($SP+$AP)*1*1*0.002+($SP+$AP)*0.01)*4}, ${($m3+$b3*2+($SP+$AP)*2*2*0.002+($SP+$AP)*0.01)*4}, ${($m3+$b3*3+($SP+$AP)*3*3*0.002+($SP+$AP)*0.01)*4}, ${($m3+$b3*4+($SP+$AP)*4*4*0.002+($SP+$AP)*0.01)*4}, ${($m3+$b3*5+($SP+$AP)*5*5*0.002+($SP+$AP)*0.01)*4} |
| 954835 | Shuriken Toss | ${$M1+$ppl1+$SP*0.375+$RAP*0.4}, ${$m1+$ppl1+$SP*0.375+$RAP*0.4} |
| 44614 | Frostfire Bolt | ${$M2*$<mult>}, ${$m2*$<mult>} |
| 5308 | Execute | $*10 |
| 22568 | Ferocious Bite | ${$f1+$AP/410}.1 |
| 22570 | Maim | ${$b1*1+$M1+$MW}, ${$b1*1+$m1+$mw}, ${$b1*2+$M1+$MW}, ${$b1*2+$m1+$mw}, ${$b1*3+$M1+$MW}, ${$b1*3+$m1+$mw}, ${$b1*4+$M1+$MW}, ${$b1*4+$m1+$mw}, ${$b1*5+$M1+$MW}, ${$b1*5+$m1+$mw} |
| 556 | Astral Recall | $z |
| 45902 | Blood Strike | $<bonus> |
| 724 | Lightwell | ${$7001m1*3*$<mult>} |
| 772 | Rend | ${0.2*5*(($MWB+$mwb)/2+$AP/14*$MWS)} |
| 774 | Rejuvenation | ${$m1*5*$<mult>} |
| 8921 | Moonfire | ${$m1*3*$<mult>} |
| 974 | Earth Shield | $<heal> |
| 965426 | Meditate | @learns:954708@ |
| 965425 | Recuperate | @learns:954708@ |
| 1752 | Sinister Strike | $<percent> |
| 20165 | Seal of Light | ${0.15*$AP+0.15*$SPH}, ${1+0.25*$SPH+0.16*$AP} |
| 701521 | Summoner's Armor | @learns:92166@ |
| 24275 | Hammer of Wrath | ${$M1+0.15*$SPH+0.15*$AP}, ${$m1+0.15*$SPH+0.15*$AP} |
| 26573 | Consecration | ${8*($m1+0.04*$SPH+0.04*$AP)} |
| 21084 | Seal of Righteousness | ${$MWS*(0.022*$AP+0.044*$SPH)}, ${1+0.2*$AP+0.32*$SPH} |
| 26679 | Deadly Throw | ${$M1+($b1*1)+$RWB}, ${$M1+($b1*2)+$RWB}, ${$M1+($b1*3)+$RWB}, ${$M1+($b1*4)+$RWB}, ${$M1+($b1*5)+$RWB}, ${$m1+($b1*1)+$rwb}, ${$m1+($b1*2)+$rwb}, ${$m1+($b1*3)+$rwb}, ${$m1+($b1*4)+$rwb}, ${$m1+($b1*5)+$rwb} |
| 20166 | Seal of Wisdom | ${1+0.25*$SPH+0.16*$AP} |
| 30455 | Ice Lance | ${$M1*$<mult>}, ${$m1*$<mult>} |
| 53736 | Seal of Corruption | ${(0.013*$SPH+0.025*$AP)*5}, ${1+0.22*$SPH+0.14*$AP} |
| 16190 | Mana Tide Totem | $<mana> |
| 31801 | Seal of Vengeance | ${(0.013*$SPH+0.025*$AP)*5}, ${1+0.22*$SPH+0.14*$AP} |
| 5185 | Healing Touch | $<max>, $<min> |
| 31935 | Avenger's Shield | ${$M1+0.07*$SPH+0.07*$AP}, ${$m1+0.07*$SPH+0.07*$AP} |
| 5171 | Slice and Dice | ${(12+$<glyph>)*(100+$<mult>)/100}, ${(15+$<glyph>)*(100+$<mult>)/100}, ${(18+$<glyph>)*(100+$<mult>)/100}, ${(21+$<glyph>)*(100+$<mult>)/100}, ${(9+$<glyph>)*(100+$<mult>)/100} |
| 16511 | Hemorrhage | $<bonus> |
| 20164 | Seal of Justice | ${1+0.25*$SPH+0.16*$AP} |
| 33763 | Lifebloom | ${$m1*7*$<mult>} |
| 1329 | Mutilate | $<percent> |
| 2098 | Eviscerate | ${$M1+(($b1*1)+$AP*0.07)*$<mult>}, ${$M1+(($b1*2)+$AP*0.14)*$<mult>}, ${$M1+(($b1*3)+$AP*0.21)*$<mult>}, ${$M1+(($b1*4)+$AP*0.28)*$<mult>}, ${$M1+(($b1*5)+$AP*0.35)*$<mult>}, ${$m1+(($b1*1)+$AP*0.03)*$<mult>}, ${$m1+(($b1*2)+$AP*0.06)*$<mult>}, ${$m1+(($b1*3)+$AP*0.09)*$<mult>}, ${$m1+(($b1*4)+$AP*0.12)*$<mult>}, ${$m1+(($b1*5)+$AP*0.15)*$<mult>} |
| 13795 | Immolation Trap | ${($RAP*($<mult>/100)+$13797m1)*$<duration>} |
| 49998 | Death Strike | $F |
| 50720 | Vigilance | $<threat> |
| 55050 | Heart Strike | $<bonus>, ${$<bonus>/2} |
| 55342 | Mirror Image | $<images> |
| 63108 | Siphon Life | $<percent> |
| 760204 | Holy Ward | @learns:92170@ |
| 31687 | Summon Water Elemental | $?(s70937)[][ |
