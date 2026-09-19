# Optional spell definition reference package

This package converts the 179 missing spell IDs with exact Area 52 source records into the exported AzerothCore `spell_dbc` schema. ID **901018 is excluded**. It is independent of the Classic addon and is not automatically installed or loaded by the server.

## Generate definition candidates

Python 3.10+ and its standard library are sufficient. No Ascension installation, live export, database credentials or network connection is needed by future installers:

```sh
python3 convert.py --output generated
python3 convert.py --include-dependencies --output generated-with-dependencies
```

For a fresh collision check against the installer's actual server DBC, add:

```sh
--server-spell-dbc /path/to/server/data/dbc/Spell.dbc
```

The default converts **179 roots**. The second command converts **320 records**: those roots plus **141 non-stock reference dependencies**. These variants overlap: do not apply both. Tooltip-only dependencies are preserved for reference and may not need a server record. Existing stock spell dependencies are not copied or overwritten.

## Current status: conversion complete, installation blocked pending adaptation

The generated `rows.json` retains the source values in SQL-compatible types. `apply.review.sql` contains the candidate inserts, schema validation, collision checks and transaction handling. It intentionally raises an error before any DDL or spell insertion when the selected data contains effects, auras or targets outside stock core enum ranges. **Do not remove that guard to install the raw batch.**

Six root records have out-of-range values: Colossus Smash, Flame Ascendance, Roll the Bones, Light of Dawn, Sundering and Smoke Bomb. The dependency-inclusive report identifies additional affected records. The raw source is retained unchanged so future implementation can map those functions to supported effects and module scripts. In-range values are not proof that a spell works: dummy effects, proc behavior, summons, references to custom creatures/items, and existing stock dependencies with modified Ascension behavior still require review.

A full client spell patch, cast times/visual assets, server proc/target/script bindings and gameobject/creature/item definitions are **not** produced here. AP/rarity/level rules and menu purchase routes are unchanged. Ascension server code cannot be recovered from these client records.

## Generated files

- `rows.json`: all 234 mapped SQL columns per selected record.
- `compatibility.json`: out-of-range effect/aura/target records; limits 165/317/111 are exclusive.
- `summary.json`: selection, reference hashes, batch identity, collision-check status and required schema widening.
- `schema-required.review.sql`: separate prerequisite for five Power of the Elements records whose aura description is 624 characters. It expands `AuraDescription_Lang_enUS` from the upstream 550-character width to 624 without truncating the reference. It refuses an unexpected schema.
- `apply.review.sql`: guarded candidate installation, no REPLACE/IGNORE/upsert. Any ID already present in `spell_dbc` aborts the batch. A same-schema receipt table stores exactly the inserted rows in the same transaction.
- `rollback.sql`: removes only the batch recorded in its receipt; refuses if imported rows are missing or have changed. It clears the receipt but leaves the empty table for review. It does not unlearn spells from characters or restore client files.
- `schema-restore.review.sql`: optional after row rollback; refuses to shrink the field if any other row would be truncated.

These SQL routines have not been executed against a test database in this environment. Before any future installation, finish compatibility adaptation, back up the world database, stop the worldserver and other writers, verify the actual client/server DBC ID space, and test on a copy. Use the MySQL client against the explicitly selected world database, without `--force`. Routines require CREATE ROUTINE and the listed schema changes require ALTER/CREATE privileges. DDL is outside the row transaction; a failed import can leave an empty receipt table or the separate text-field expansion. Inspect those rather than assuming DDL was rolled back.

## Packaged reference data

`data/spells.json` preserves raw 234-word records, all 16 locale slots for name/rank/description/aura description, root IDs and explicit references. Raw string offsets are meaningful only in the original DBC; use the separately decoded strings. Float and signed integer words remain available for bit-exact audit.

`data/schema.json` records live exported column names/order/data types. The live collector did not capture signedness or varchar widths; those are derived from the [AzerothCore base schema](https://github.com/azerothcore/azerothcore-wotlk/blob/master/data/sql/base/db_world/spell_dbc.sql) and rechecked by generated SQL before writes. Effect class masks are explicitly transposed from DBC effect-major order to SQL mask-major order.

`data/dependencies.json` traces explicit trigger, aura prerequisite and tooltip spell links. All those non-stock IDs were found in the supplied source. This is not an exhaustive runtime dependency graph.

`data/supporting-data.json` includes the referenced duration/range/radius rows and available icon path variants with source hashes. It does not guess which conflicting icon archive wins. These supporting rows are reference data and are not installed automatically; icon image binaries and animation assets are not bundled in this definition converter.

`data/manifest.json` hashes the portable inputs. No full client archive, server dump, credentials, account/character records or personal layout files are included. Source game data remains reference material from the supplied client, not newly authored server implementation code or a claim to ownership of those assets.

## Maintainer regeneration and tests

```sh
python3 prepare_reference.py --spells SOURCE_Spell.dbc --live-export LIVE_EXPORT.zip --missing missing-spells.json --tables SUPPORT_DBC_DIRECTORY --icon-dbcs ICON_DBC_DIRECTORY --output data
python3 test_convert.py
```

The reference preparation step needs the maintainer's local source files; conversion by future installers uses only packaged data. Regeneration excludes 901018, refuses root ID collisions, traces dependencies, checks field types, and records hashes. Tests cover signed/float/string conversion, all-record bit round trips, mask ordering, exclusions, invalid inputs and generated collision/rollback/enum guards. They are not an in-game effect or live SQL test.

## Filtered candidate batch

`python3 convert.py --compatible-only --output filtered` excludes out-of-range records and roots referencing them, then includes the remaining non-stock reference closure. Current result: 156 roots plus 110 dependencies; 23 roots are held back. This conservatively includes tooltip links when deciding exclusions. `selection.json` identifies exclusions. Passing this filter is not a full compatibility test: validate auxiliary DBC references and behavior before applying the SQL or restarting the server.

## Auxiliary DBC staging

`stage_auxiliary_dbc.py --input ORIGINAL_DBC_DIRECTORY --output NEW_STAGING_DIRECTORY` stages the four missing supporting records: SpellRange 212/217/222 and SpellRadius 193. The output directory must be new. It refuses conflicting IDs, preserves existing row bytes/string offsets and appends rebased localized range strings. It never installs the output or writes to the input directory. Run it independently against the actual server and actual client baselines; do not assume those files are identical.

`data/auxiliary-additions.json` contains these four records with decoded strings and source hashes. `data/visual-icon-review.json` contains candidate source rows for all 79 missing visual IDs and path candidates for all 83 missing icon IDs. These visual rows are NOT yet a usable client patch: nested visual kits, model attachments, missile paths, textures and actual assets still need compatibility/availability checks, and archive precedence must be resolved before writing conflicting variants. Original server spells and gameplay rules remain unchanged.

Run `python3 test_auxiliary_dbc.py` for preservation, string-rebasing and collision checks. Tests use synthetic destination files with the real four source additions; actual live-file staging remains a separate validation.

## Resolved icons and visual staging

All 83 missing icon IDs now have verified BLP files in `icon-assets` and mappings in `data/resolved-icons.json`. `stage_icon_dbc.py --input SpellIcon.dbc --output NEW_DIRECTORY` adds the records while preserving original rows/strings. Imported assets use the separate `HeroAdvancement` path prefix; native icon paths are not overwritten.

`data/resolved-visuals.json` and `visual-assets` contain 79 visual roots and their selected dependency records/assets. `stage_visual_dbc.py --input CLIENT_DBC_DIRECTORY --output NEW_DIRECTORY` clones dependent kits, effect names, attachments, motion records, sounds, advanced sounds and chains into new IDs. Existing records remain byte-identical. The top-level missing visual IDs are retained for the new spell definitions; a conflicting top-level ID aborts staging. M2 texture filenames and DBC asset paths are redirected to an isolated `HeroAdvancement` directory. These outputs must be merged into the final client patch; dropping a staging directory into the game is not an installer.

Compatibility repairs are explicitly recorded, not described as exact Ascension rendering:

- Elemental Blast: nonexistent left-hand effect 2287 uses the verified right-hand elemental precast effect 113935.
- Arcing Light: disable only its dangling chain-effect 2436 reference; keep its other visual components. The missing beam is not recreated.
- Missing sound record 1493 is disabled only in imported clones. Earth-elemental loop uses the available same-name WAV. Seven absent sound-file slots (including test placeholders) are removed; available slots remain.
- Shared/conflicting texture references use the existing test client's available asset bytes. All selected files are included with checksums; this does not require future installers to have that test client.

Asset resolution used the supplied Area 52 patch-S visual tables and patch-M sound tables, with the known 3.3.5 client as a fallback for files absent or conflicting in the supplied patches. All newly staged files have separate paths, so those fallback choices do not replace existing assets. Tests verify hashes, row/string preservation, ID remapping and collision refusal. In-game rendering, sound timing, missile scripts and gameplay effects are still untested. Native 3.3.5 layouts were checked against [WoWDBDefs](https://github.com/wowdev/WoWDBDefs/tree/master/definitions).

The tools use only the packaged curated records and assets plus the installer's own baseline DBCs. No MPQ reader, complete extracted archive, unrelated client addon or third-party server module is bundled. `test_assets.py` exercises the portable staging code.
