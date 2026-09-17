# Elementals, Wild Imps and summoning descriptions — 0.33.0

## Tether Elemental

Imported A52 advancement 1615 (duplicate realm variant 34824): bundle spell 91606, Shaman / Elemental, level 1, 4 Ability Essence mapped to Ability Points, Epic quality and 2 gems. Included abilities: Tether Elemental 93569, Raise Elemental 91602, Dismiss Elemental 91651, Revive Elemental 91605 and Elemental Lore 109983. The wrapper description links the current tame action 93569; older variant 91603 is not imported.

Uses the existing bundle purchase, automatic local child grants, refund/cancel, parent badges and parent-only Shift expansion. Classic excludes the custom package. Custom server learning and actual pet behavior remain unimplemented.

Five spell textures already exist in the test client. Elemental Lore's spell_shaman_bindelemental texture was extracted from A52 patch-I and bundled with source metadata. Dragonkin's requested Lore/Dismiss artwork swap remains intact.

## Wild Imp findings

No matching taming/companion-management bundle was found in the reviewed A52 spell/advancement records. Hand of Gul'dan (spell 954611, advancement 1206 / realm variant 34756) describes summoning temporary Wild Imps to attack its target. Master Summoner explicitly references extending Wild Imp duration from Hand of Gul'dan. Other records include Wild Imp damage/scaling passives and Demon Scroll: Wild Imp (83141), which changes the appearance of an Imp and is a vanity unlock.

Consequently no invented Wild Imp bundle was added. Hand of Gul'dan would be an individual combat-ability integration, not the taming bundle requested conditionally here. This conclusion is based on extracted client records, not live-server behavior.

## Descriptions

Added the recovered descriptions for every imported companion bundle and all of their included skills. Also supplied the A52 descriptions for Demon Mastery and its five summon members, including Imp. Normal skill tooltips and expanded-list previews prefer this text in custom modes so absent or conflicting stock spell IDs cannot silently substitute an unrelated description. Classic retains native tooltips.

A52-only display directives and embedded spell links are stripped. Runtime placeholders such as percentage/duration values are shown as [spell value] because this importer does not evaluate spell formulas. They are not fabricated numeric values. Original strings remain in reference/elemental-wild-imp-review.json. Group tooltips distinguish recovered A52 text from our purchase rules. Tooltip description height adapts to its text.

Sources: extracted Area 52 patch-D Spell.dbc and CharacterAdvancement.dbc; shared CharacterAdvancementData.json; extracted SpellIcon.dbc mappings; client patch-I textures. No server files changed. Lua tests cover five-bundle costs, grants/removal and all normal/expanded member descriptions; in-game rendering still requires verification.
