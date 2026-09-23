---
name: bear-cave-server-tooltip-review
description: Use whenever a Bear Cave Hero Advancement tooltip needs checking against the server, including missing healing or damage values, unresolved formula placeholders, incorrect ranks, durations, totals, or claims that a functional spell is unimplemented. Trace effective PTR spell data and scripts before changing client descriptions; preserve unresolved yellow warnings where evidence is insufficient.
---

# Server-backed tooltip review

Review presentation against effective server behavior. An unresolved tooltip formula is not evidence of an unimplemented spell. Conversely, a populated spell record or plausible number is not proof that the full mechanic works.

## Locate the current resources

Read repository AGENTS.md instructions. Confirm current paths and branches; these are project discovery anchors, not immutable deployment facts.

| Resource | Purpose |
|---|---|
| GitHub `CWO4PapaBear/HeroFreePick` | Authoritative project source for advancement UI, tooltip generators and custom player mechanics; inspect the current development branch, historically `fix/spellbook-tab-pages` |
| Local `outputs/HeroFreePick-Spellbook-Publish` | Publication checkout; older root/profile artifacts may differ from the active client/server |
| GitHub `CWO4PapaBear/More-Minions` | Pet-family spell definitions and scripts when reviewing pet tooltips; do not move those mechanics into HeroFreePick |
| GitHub `CWO4PapaBear/Bear-Cave-Launcher` | Cumulative client packaging, release assets and `channels/ptr.json`; source push and client promotion are separate |
| WSL `/home/dml/games/wow-server-classless-test` | PTR source/configuration; verify it matches the running image |
| Docker `classless-test-worldserver` | Running PTR image and actual DBC files, commonly `/azerothcore/env/dist/data/dbc`; confirm configured data location |
| Docker `classless-test-database`, database `acore_world` | `spell_dbc`, `spell_bonus_data`, `spell_script_names`, `spell_ranks`; inspect schema before use |
| Database `acore_characters` | Only if character-specific mode, ownership, rank or spec explains a mismatch: inspect relevant character/talent/build records narrowly; no broad account export |
| Owner client `D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test/Interface/AddOns/HeroFreePick` | Actual loaded tooltip files; hash before editing and compare with launcher candidate |
| `tools/client-server-tooltip-resolution/Resolve.py`, `Test-Resolution.py`, `audit.json` | Previous resolver, renderer tests and provenance; inspect rather than assume the old export is current |
| `tools/client-tooltip-blue-values`, `tools/client-tooltip-cleanup` | Existing colors, expanded-detail placement and paragraph formatting |
| `server/spell-definitions/convert.py`, `tools/talents/import_area52_talents.py` | Field mapping, DBC reader and tooltip rendering helpers; reconcile versions with current schema |

Local historical packages include `outputs/Hero_Server_Tooltip_Resolution` and `outputs/Hero_Abomination_Test/npc-audit-3`. They can explain past decisions but cannot independently validate today's PTR definitions.

Client files to trace include `ServerSpellDescriptions.lua`, `ResolvedServerTooltips.lua`, `ServerTooltipValues.lua`, `AscensionTalentOverlay.lua`, `TooltipPresentation.lua`, catalogs, `HeroFreePick.lua` and TOC load order. Follow the renderer actually used on hover, including rank selection and later overrides. Merely changing an unused source table will not repair the displayed tooltip.

## 1. Inventory the problem

Collect spell IDs and ranks from the active catalogs and tooltip tables. Scan for raw `$` expressions, named variables, `[value pending]`, `[value unavailable]`, unsupported conditionals and implementation warnings. Include affected triggered spells and all ranks, not only the first example reported.

For healing, include direct healing, periodic healing, triggered/proc healing, group/channel heals and mixed damage/healing abilities. Classify by actual effects and references as well as names. Do not interpret every unresolved numeric token as healing.

Record the current text, rendered result, mode and provenance. Separate these findings:

- Missing server record or unresolved dependency.
- Existing record with unsupported tooltip syntax.
- Values changed by SQL overrides or compiled scripts.
- Formula needing character stats, talents, glyphs or target context.
- Suspected gameplay defect requiring a separate implementation task.

## 2. Capture a fresh read-only baseline

Export the running image identity, relevant DBC files, world table schemas/rows and applicable source/script bindings with timestamps and SHA-256 hashes. Do not export Docker environments or credentials. If direct WSL access is unavailable, provide a read-only collector for the user and continue independent inspection while awaiting its result.

Required evidence depends on the tooltip:

- `Spell.dbc`; `SpellDuration.dbc`, `SpellRadius.dbc`, `SpellRange.dbc`, `SpellCastTimes.dbc` as referenced.
- `SpellDescriptionVariables.dbc` when available and relevant to named variables. A missing table is a recorded limitation, not permission to assume its values.
- `acore_world.spell_dbc`, `spell_bonus_data`, `spell_script_names`, and `spell_ranks`.
- `SpellMgr.cpp` corrections/loading logic, `SpellInfo.cpp`, `SpellEffects.cpp`, `SpellAuraEffects.cpp`, relevant `Unit.cpp` healing calculations, class spell scripts and affected custom modules.

Use the established credentials inside the database container without printing them. Use `mysql --default-character-set=utf8mb4 --batch`; retain raw output. Its escaped tab/newline fields are not CSV quoting. Split records on LF and columns on literal tabs, validate widths, then decode MySQL escapes. Flag invalid encoding; do not silently discard bytes. Earlier audits failed on invalid UTF-8 and on CSV parsers interpreting embedded description characters.

Check all missing-file/query failures before drawing conclusions. Do not silently combine fresh Spell.dbc with old duration/range tables. If reusing a prior artifact, verify its identity/hash against current data.

## 3. Reconstruct the effective spell

Trace actual load/override order in the running core: client-compatible base spell records, server SQL overrides, SpellMgr corrections, script bindings and custom handlers. Do not assume `spell_dbc` is a sparse overlay—inspect loader semantics and the converter's field mapping.

Validate record layout and field count. The prior WotLK reader expected 234 Spell fields; do not apply those offsets blindly to Ascension or another client build. Interpret signed integers, floats and string offsets correctly.

Resolve references transitively with cycle/depth limits. Distinguish the selected rank, trigger spell, proc heal, periodic aura and final bloom. Ensure a script named in SQL is compiled and registered before treating it as effective behavior.

Ascension/client archives and official stock data can clarify formula syntax or missing descriptions. They are secondary evidence, not authoritative proof of PTR behavior. Never copy a retail or Ascension healing amount over a different server implementation.

## 4. Resolve the amount with the correct meaning

For each number, identify what is being displayed: base min/max, per tick, total over duration, per target, total channel, final bloom, percent of health, or a stat-scaled estimate.

- Reproduce the effective core's base-point/die-side semantics; do not universally add one or take absolute values inside arithmetic.
- For periodic totals, verify duration, amplitude, tick timing and effect index. Do not copy a hard-coded tick count from an imported description when the server differs.
- For direct healing, preserve min/max ranges and any level scaling. Do not collapse a random range into a single formula operand.
- Inspect `spell_bonus_data` and the core/script path for direct, periodic, AP and healing coefficients. Zero, negative/sentinel and absent coefficient values may have different meanings.
- Do not add spell power twice if it is already represented in the imported expression or applied by a scripted formula.
- Resolve named variables such as `$<min>`, `$<max>`, `$<total>`, `$<heal>` and `$<mult>` from definitions or demonstrably equivalent server calculations. Never replace every multiplier with 1.
- Distinguish healing power from school-specific damage power. Verify the actual 3.3.5 client API and server school semantics before mapping `$SP`, `$SPH` or similar symbols.
- Evaluate supported character-dependent values at hover/refresh time. Handle API failure explicitly rather than displaying zero as a real answer.
- Model relevant talent/glyph conditions only when supported by evidence. If displaying base spell data rather than fully modified combat output, make that scope clear; actual healing can differ due to target modifiers, crits and overhealing.

Use restricted arithmetic parsing, supported operators/operands, recursion bounds and safe division. Never evaluate imported formula text as arbitrary Python or Lua code. Preserve unresolved expressions in the audit even when the UI replaces them with readable placeholders.

Examples from the previous audit: Healing Touch had `$<min>`/`$<max>`, Renew had `$<total>`, Earth Shield had `$<heal>`, and Regrowth/Rejuvenation/Lifebloom/Lightwell had multiplier expressions. These identify investigation targets, not approved substitutions.

## 5. Change only what evidence supports

Prefer correcting the generator/resolver and regenerating supported entries over hand-writing isolated tooltip numbers. Keep a per-spell audit containing ID/rank, original text, effective source, relevant fields/scripts, formula, replacement text and unresolved reasons.

Preserve all existing resolved entries and later UI fixes. Work from the currently installed client; do not overwrite it with an older package. Check Classic separately: custom-mode tooltip overlays must not leak into stock presentation. If the request changes talent behavior rather than presentation, also apply the talent-modification skill.

Maintain existing light-blue resolved values, yellow unresolved warnings, Shift-toggle technical details and paragraph spacing. Remove an implementation warning only when implementation evidence supports removal. A resolved formula alone does not establish functional gameplay.

If an expression cannot be justified, leave it yellow and name the missing evidence in the audit. If only base data can be established, show an honestly labelled base value where appropriate rather than a falsely precise prediction.

## 6. Test and deliver

Test Lua 5.1 syntax and the actual renderer path, including multiple ranks, min/max healing, periodic totals, trigger references, stat changes, conditional branches, unsupported expressions, missing APIs, division by zero and Classic isolation. Include non-healing regression examples such as Serpent Sting if shared parsing changes.

Compare representative values with independently calculated effective records. Test with zero and nonzero healing power, different levels and relevant talents where supported. Check in-game text and, when verifying mechanics, distinguish combat-log effective healing from nominal healing and overheal.

Report counts as descriptions/ranks versus unique abilities, and distinguish fully resolved, partially resolved and still unverified. Do not claim all spells are functional based on tooltip parsing.

Stage an exact manifest and backed-up closed-client install when needed. Pure tooltip corrections normally need neither SQL nor a server restart. Do not modify spell mechanics or database values merely to make a description easier to render.

Update HeroFreePick source/audit notes and run required repository checks. Keep raw proprietary DBCs, database exports, credentials and personal client settings out of Git. Follow existing authorization for commits/pushes. Publish client assets and promote the launcher only when requested or already authorized; verify package parity, upgrade/repeat-install behavior, remote hashes and the public channel. Explicitly distinguish local installation, source push and launcher availability.
