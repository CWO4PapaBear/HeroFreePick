# Recent package icon audit

Audited the four companion bundles, their 21 included abilities, all 23 Masteries and their linked catalog abilities, including Summon Imp: 142 records. Checked named texture paths against all 26 MPQ archives and loose Interface files in the configured Auto-Attack-Test client. No archives failed to open. This checks asset presence, not visual rendering.

## A52 textures absent from the test client

| A52 icon name | Affected abilities |
|---|---|
| `spell_warlock_demonbolt` | Enslave Demon |
| `inv_misc_steelweaponchain` | Dominate Undead |
| `spell_warrior_dragoncharge` | Call Dragonkin |
| `novart_books_(2)_Border` | Dismiss Dragonkin |
| `ability_warrior_dragonroar` | Revive Dragonkin |
| `spell_warlock_demonicportal_purple` | Summon Demon |
| `ability_warlock_ancientgrimoire` | Dismiss Demon |
| `ability_demonhunter_sigilofmisery` | Revive Demon |
| `_Undead_03` | Revive Undead |
| `inv_knife_1h_cataclysm_c_05` | Crimson Tempest |
| `5_warlock05_Border` | Summoner's Armor |
| `spell_fire_twilightfireward` | Arcane Ward |

Total: **12 distinct missing A52 textures**. None has been imported or substituted.

## Existing fallback concerns

The Demon bundle and its children currently fall back to `spell_warlock_demonbolt`; the Undead bundle and its children fall back to `inv_misc_steelweaponchain`. Both fallback paths are absent. This also affects Demon Lore, Raise Undead, Dismiss Undead and Undead Lore, even though their individual A52 spell icons are present. Dragonkin child fallbacks reuse the available red-drake package icon; this is a placeholder rather than their original A52 artwork. GetSpellInfo takes precedence when the client knows a spell, so runtime results may differ from the fallback.

Crimson Tempest, Summoner's Armor and Arcane Ward also have unavailable configured fallback textures matching their missing A52 icons. Mastery parent icons and Summon Imp have available A52 textures.

## Source and limits

Paths come from the Area 52 Spell.dbc SpellIconID and the extracted SpellIcon.dbc tables; distinct mappings are checked if tables disagree. Matching advancement-icon fallbacks are checked separately. The complete machine-readable evidence is in reference/package-icon-audit.json. This audit does not modify the game client or claim that an absent asset can be rendered.

Unresolved A52 icon mappings (not classified as missing assets): Essential Finishing Move Mastery.
