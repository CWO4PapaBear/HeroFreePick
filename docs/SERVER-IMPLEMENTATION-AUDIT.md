# Hero Advancement server implementation audit

Interface 0.41.1; recorded server catalogue 37033160.

Audited **1665 current catalogue entries**, **4 primary-stat choices**, and **29 staged talent records**. Catalogue entries include aliases and group members; these are not counts of unique spells.

This is a read-only audit of saved stock/Area 52 DBCs, current module code, the recorded deployment and historical test results. **No fresh live server query was possible in this session.** No entry is labelled fully gameplay-verified merely because its spell ID exists.

The local deployed-module mirror matches all hashes in the latest deployment record. This establishes artifact consistency, not current process/database state.

## Classification

| Status | Entries |
|---|---:|
| ALIAS_EXISTING_PURCHASE | 151 |
| CLASSIC_ONLY | 94 |
| COMPANION_SYSTEM_PENDING | 24 |
| GROUP_PARTIAL | 4 |
| GROUP_STOCK_GRANTS_SUPPORTED | 22 |
| MISSING_STOCK_DEFINITION | 73 |
| NEW_TALENT_STAGED | 29 |
| PRIMARY_STAT_SYSTEM_PENDING | 4 |
| REFERENCE_BEHAVIOR_REVIEW | 582 |
| STOCK_PURCHASE_PATH_SUPPORTED | 9 |
| TALENT_COMMIT_PENDING | 53 |
| TALENT_EFFECTS_AND_COMMIT_PENDING | 625 |
| TRAVEL_SYSTEM_PENDING | 28 |

## Findings

- 617 server catalogue entries have a Class+ stock-grant path (513 purchasable roots and 104 free members). This does not prove their Area 52 effects are implemented.
- 678 catalogue talent entries require the custom talent transaction path; Classic still uses native talent application.
- 855 entries carry changed Area 52 tooltip text; changes must be implemented or explicitly reconciled before clearing yellow markers.
- 180 distinct required/preview spell IDs are absent from the stock baseline. Group-only reference IDs are excluded from this count when the server uses an entitlement instead.
- 0 interface/server level, AP, rarity or controlling-group discrepancies were found.

## Recommended implementation order

1. Add server-authoritative talent rank transactions, removals/reset pricing and persistent recovery. Resolve existing aliases; do not duplicate AP-priced talent abilities.
2. Resolve ID/name conflicts and Area 52 effect changes before treating current stock purchases as matching the new descriptions.
3. Implement missing ordinary spells and rank chains in reviewed groups, including client records where absent.
4. Complete Mastery members, primary-stat mechanics, More Minions, independent Mage travel and DK-specific resources.
5. Implement Hybrid/Hero ownership and class-access rules on the server, followed by per-effect gameplay verification.

Use `AUDIT.html` to filter every entry and inspect its blockers. `implementation-catalogue.json` retains field-level evidence and mode scope.

## Incomplete groups

| Group | Omitted catalogue members |
|---|---|
| Essential Finishing Move Mastery (21006002) | 22954809, 22954553 |
| Warlock Armor Mastery (21092166) | 22701521 |
| Ward Mastery (21092170) | 22092171, 22760210, 22760204 |
| Advanced Finishing Move Mastery (21954708) | 22965425, 22965426 |
| Portal Mastery (21818045) | 22010059, 22011416, 22011417, 22011418, 22011419, 22011420, 22032266, 22032267, 22033691, 22035717, 22053142, 22903018, 22903090 |
| Teleport Mastery (21818046) | 22003561, 22003562, 22003563, 22003565, 22003566, 22003567, 22032271, 22032272, 22033690, 22035715, 22053140, 22901018, 22901090 |
| Tame Dragonkin (23091634) | 25093558, 25091631, 25091652, 25091633, 25109982 |
| Enslave Demon (23000890) | 25000896, 25000884, 25000892, 25000887, 25109981 |
| Dominate Undead (23000891) | 25000899, 25000885, 25000893, 25000889, 25109980 |
| Tether Elemental (23091606) | 25093569, 25091602, 25091651, 25091605, 25109983 |

## Class breakdown

Counts below exclude aliases from talent work; missing definitions are entry counts, not unique spell IDs.

| Class | Passive talent commit work | Missing-definition entries | Reference review entries | Staged records |
|---|---:|---:|---:|---:|
| All | 0 | 0 | 0 | 0 |
| DeathKnight | 65 | 1 | 59 | 0 |
| Druid | 70 | 9 | 71 | 1 |
| Hunter | 68 | 2 | 68 | 5 |
| Mage | 70 | 13 | 53 | 3 |
| Paladin | 64 | 5 | 57 | 3 |
| Priest | 67 | 6 | 50 | 4 |
| Rogue | 70 | 10 | 46 | 0 |
| Shaman | 65 | 11 | 68 | 4 |
| Warlock | 68 | 8 | 57 | 2 |
| Warrior | 71 | 8 | 53 | 7 |

## Metadata differences

| Entry | Findings |
|---|---|
