# Progression redesign and Legendary audit

## Restore point

Before the progression redesign: commit `54a681b`, tag `restore-runes-budget-before-progression`. The output package `HeroFreePick-before-progression.zip` includes addon/source files and the test-server checkpoint. Its SHA-256 is supplied separately. This checkpoint includes Rune Mastery and expanded rarity bars, but not the AP/talent and stock-level redesign.

## Implemented rules

Latest adjustment: in Class+ and Hybrid, ability unlock requirements of levels 1–10 become level 1, including DK and Mastery/bundle members. Passive talent tiers, levels above 10, Classic, Hero and later-rank schedules are unchanged. The earliest-member rule automatically brings affected Masteries to level 1.

- Fixed caps: 11 Uncommon, 16 Rare, 13 Epic, 7 Legendary. Rarity limits still apply to Class+, Hybrid and Hero.
- Click a rarity bar to filter; right-click clears it. Sixteen gem positions fit before the count.
- Runeforging Mastery: 2 AP and 1 Rare gem, ten free weapon runes at level 20. Classic rune records remain separate.
- 151 native talent-entry aliases share a single purchasable ability entry in custom modes. AP is charged once, never TP. Imported AP and rarity costs are preserved; seven newly exposed entries use 2 AP, with the final-tier Legendary rule applied. Passive talents without an imported ability counterpart remain TP purchases, except final-tier entries, which are all represented as abilities.
- All 30 final-tier abilities: level 60, one Legendary gem. Other promoted abilities cannot precede their native talent tier.
- Class+/Hybrid use stock starting, trainer, quest and SpellLevel references for non-DK abilities. DK keeps the adjusted level-one plan. Hero retains custom unlocks with the new talent-tier minimums.
- Every Mastery/bundle follows its earliest member under the current mode; later members remain individually level-gated. Talent-derived paid choices are removed from free Mastery membership.
- Classic keeps original talent costs, prerequisite checks and native commits.
- 27 custom abilities have no stock unlock-level reference; retain their custom levels. See CUSTOM-LEVEL-EXCEPTIONS.json.
- Stock rank-level metadata is separate from first-rank unlocks. The test server uses those levels for non-DK rank upgrades; DK keeps its existing stock later-rank behavior.

## Legendary totals

Distinct purchasable abilities, no double counting the talent-tree presentation or free group members. Totals are potential catalog costs, not simultaneous legal builds: the selected budget cap remains 7. All listed Legendary ability AP totals are below 80. The requested comparison threshold is 8.

| Class | Potential Legendary gems | Below 8? |
|---|---:|---|
| Warrior | 5 | Yes |
| Paladin | 13 | No |
| Hunter | 9 | No |
| Rogue | 6 | Yes |
| Priest | 4 | Yes |
| DeathKnight | 11 | No |
| Shaman | 5 | Yes |
| Mage | 9 | No |
| Warlock | 5 | Yes |
| Druid | 7 | Yes |

Per-ability IDs, costs and levels: LEGENDARY-CLASS-AUDIT.json. Catalog availability is not proof of every spell mechanic on the test server.

## Validation

Lua 5.1 regression suite; fresh production load; all 30 trees; 3,108 custom-mode/draft level boundaries; 151 shared AP aliases; 30 Legendary capstones; Mastery grant gates; click-filter behavior. Standalone C++ catalog/commit/grant/rank policy tests compiled and passed with Zig. Deployment migration tested offline. Full AzerothCore rebuild and in-game visual/gameplay verification occur when the deployment is run.

## Test-server rollout

The all-class harness remains a Class+ ability-commit test. Hybrid/Hero UI policy is implemented; this does not introduce their full server commit transport.

Run `Hero_ClassPlus_All_Classes_Test/apply-progression-update.py` with sudo python3 in Ubuntu, with WoW closed. It installs the Rune/budget checkpoint first, then the progression update. Each stage snapshots its prior approved build ledger, addon files and server image. Purchases which become unavailable or under-level are removed and reported, returning their AP budget. Builds which would exceed AP or rarity caps abort before purchase changes; no arbitrary budget-based trimming occurs.

To roll back only the redesign, run `progression-update/deploy.py rollback` with WoW closed. This restores the checkpoint image/addon and approved-purchase snapshot. It rewinds approved purchases made since that deployment, while preserving spell provenance so the restored server can reconcile spells on login. Character levels and unrelated database data are not rewound. Do not reinstall only the old addon over a different server catalog.
