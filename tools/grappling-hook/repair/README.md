# Grappling Hook acceptance repair

Original Grappling Hook was activated. Testing reported oversized chain links, no hook projectile and follow-up "No Path Available" on open ground.

Full repair server build passed and current source was restored with no errors. Matching visual archives installed locally with hash-verified backups. Repair server activation and gameplay acceptance remain pending; no launcher publication.

Path repair reserves endpoint/rounding capacity in the core's four-yard point-budget conversion, then checks actual geometric path length. The targeted follow-up uses the core Charge height helper with an absolute five-yard bound and a combat-reach endpoint tolerance. Ground-target strictness, line of sight, failed/partial/shortcut paths, movement state and authorization checks remain. This addresses identified overly strict checks; live retesting must establish whether it resolves the reported case.

Visual reference: Abomination Hook 59395 -> visual 11055 -> cast kit 10198 -> chain 502. Clone its repeating-link settings into only our chain record, width 0.10 and texture length 1.0. Add an isolated WotLK-compatible Monk grapple-weapon projectile with its skin/textures; this is an adapted test visual, not a claim to reproduce the original Ascension hook. Unrelated archive entries and Spell.dbc remain unchanged. Packed chain field layout: https://github.com/wowdev/WoWDBDefs/blob/master/definitions/SpellChainEffects.dbd

These scripts run from the established workspace `outputs/Hero_Grappling_Hook_Repair`, depend on the prior `outputs/Hero_Grappling_Hook` tooling, and require a fresh reviewed snapshot. Do not run from this publication folder. Binary assets and private exports are intentionally excluded.

Preflight in WSL:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Repair/Activate-Test.py --check
```

After preflight, arrange maintenance and ensure the matching local client is installed:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Repair/Activate-Test.py --activate --maintenance --client-ready
```

Existing bindings are checked and preserved; no SQL writes. Rollback restores the previous Grappling Hook image/source and retains learned selections:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Repair/Activate-Test.py --rollback --maintenance
```

Test chain scale/projectile rendering locally, then enemy follow-up at short and near-10-yard ranges after server activation. Also verify walls, elevations, initial ground cast, cooldown, stealth and temporary action-button restoration.
