# Area 52 talent importer

This importer reads the supplied **Area 52** CharacterAdvancement and Spell DBCs, compares them with Hero Advancement and stock 3.3.5 spells, and generates a presentation overlay plus a server implementation reference. It never writes a spell database, changes an existing talent ID/rank/cost, or grants an ability.

Current review: 994 source records, 965 matched records, 29 unmatched records representing 27 distinct class/name pairs, 971 mapped catalogue entries including aliases, and 855 entries with different descriptions. All 671 distinct icons were recovered. 184 rank descriptions retain unresolved formulas and use explicit pending-value placeholders in game.

## Run

1. Export the current baseline (requires `lupa.lua51`):
   `python tools/talents/export_baseline.py --output baseline.json`
2. Run the importer (standard Python only):

```text
python tools/talents/import_area52_talents.py --advancement AREA52_CharacterAdvancement.dbc --spells AREA52_Spell.dbc --stock-spells STOCK_Spell.dbc --metadata CharacterAdvancementData.json --baseline baseline.json --tables lookup-dbc-folder --icon-dbcs spell-icon-dbc-folder --icons extracted-icon-folder --output review-folder
```

The tables folder contains SpellDuration.dbc, SpellRadius.dbc and SpellRange.dbc. The icon-dbcs folder contains only the reference SpellIcon DBC versions, ordered by patch precedence; the icons folder contains the BLP assets extracted from the supplied archives. Source archives are not redistributed by this tool. The local `Area52_Talent_Import/RunImport.ps1` is preconfigured for this workspace's extracted data.

Add `--talents AREA52_Talent.dbc` to retain source talent nodes, rank lists and prerequisite links in `talent-topology.json`. The local runner includes this option.

Add `--install-addon path/to/HeroFreePick` to install the generated data, icons and presentation overlay. It validates known insertion points before writing and keeps the original UI/TOC in the output's `pre-import-backup` folder. Rerunning is idempotent. Classic's native talent tooltip remains unchanged.

## Matching and preserved behavior

Matches are scoped to class, then name or shared spell identity. Multiple presentation aliases can point to one talent. Existing advancement identity takes precedence when reference variants disagree; unresolved target conflicts are excluded and reported. Exact raw-function candidates with a different name/identity are review candidates, not automatically asserted equivalents. To approve a mapping, use `--matches matches.json` with `{ "sourceAdvancementID": [existingEntryID] }`.

No catalogue field, native tree node, connector route, prerequisite predicate, pending-rank function, cost or server transport is replaced. The hook changes only the description/icon and appends reference notices. Existing prerequisite red/green behavior and Classic native commit paths remain intact. A different reference rank count is reported; ranks missing in the reference fall back to the current native tooltip rather than reusing the wrong rank.

New talents are imported into `HeroAscensionNewTalents` / `HeroFreePick.AscensionTalentImports` with stable reserved import IDs and all source metadata. They are **staged**, not automatically inserted over existing tree nodes or made purchasable. This avoids inventing node placement or server connectors. Review those mappings before enabling them in the live tree.

## Yellow text and implementation confirmation

Word-level additions/replacements versus stock are yellow. Deleted text is not shown. The tooltip warns that changed effects are not yet implemented; matching wording remains white. Unresolved formula values are explicitly marked pending, with the original expression preserved in the export. Source text colors are stripped so they cannot override this state.

`--confirmed implemented.json` accepts `{ "sourceAdvancementID": "referenceHash" }`. Copy the hash from review.json only after implementing and verifying the corresponding server behavior. Confirmation suppresses pending highlighting for that exact data revision. An ID alone, stale hash, or installed client spell does not mark the effect implemented. Rank-layout mismatches still require review.

## Outputs for server work

- `REPORT.md`: new talents and changed existing entries.
- `review.json`: source records, matching evidence, explicit source costs/levels/ranks, row/column hints, raw advancement fields, icons and provenance hashes.
- `tooltip-changes.json`: rank-by-rank stock and reference text plus highlighted text.
- `server-effects.json`: complete numeric Spell.dbc records, decoded names/rank/aura text, named effect fields, and transitive trigger/aura/tooltip spell references with duration/range/radius records.
- `AscensionTalentData.lua` and `icons/`: generated client presentation/staging data.

The client data cannot establish server-script implementation, all proc conditions or required database scripts. Raw string offsets are reference offsets, not portable server records. Do not insert raw records directly into a stock server. No server implementation or live deployment is claimed here.
