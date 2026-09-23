# PTR experimental shared progression

## Key balance change: rollback candidate

The owner approved PTR testing of both shared base attributes and the revised health/mana curve. If survival, resource availability, spell costs, or leveling balance test poorly, restore the prior class-based progression. Main server and Class+ must remain unchanged.

- Hero: shared progression from level 1.
- Hybrid: shared progression at the character's current level when selected at level 10 or later.
- All five base attributes: 20 + level, before existing racial offsets and other bonuses.
- Base health/mana: exact reviewed `../Hero_Hybrid_Stat_Review/proposed-curve.json` values, including 35/75 at level 1, 115/190 at level 10 and 7350/4050 at level 80. Faster growth begins after level 50.
- Preserve racial modifiers, Primary Stat bonuses, equipment and spell/talent effects.

## Required integration checks

Login, level-up, mode selection and reset/recalculation must agree. Resource refresh must not restore the old mana curve. Class+ and Classic must retain their existing values. Preserve race offsets using the actual server data representation, not assumptions from the reference dump. Check maximum/current health and mana handling, death/revival and mode transitions without repeated refill or duplicate stat bonuses.

## Rollback requirement

Retain the previous image, source hashes and compose configuration. Avoid rewriting shared class tables or permanent player attribute rows. Recalculation after rollback/relogin should restore prior class-based values while retaining earned levels, gear, talents and selected modes. Provide a verified rollback command alongside activation. Do not restore whole character databases to undo progression balance.

## Status

Implementation staged against baseline-20260923-171827-442281. Production helper compiled against isolated core doubles and passed mode/level eligibility, racial offsets, exact curve, idempotent refresh, no-refill, clamp, dead-character, disabled-policy and missing-race checks. Full PTR compile passed (image sha256:5afd1070972d92e8e0ff1348787a3616dca8b8e8eec7c9281d3b308bf2d04eb3); source restored without errors. Activation requested; not yet verified. Actual activation source restoration passed forward/rollback, added-file removal, drift refusal and corrupt-backup refusal checks. These local checks do not replace a full core build or gameplay testing. No client update is required.

## Activation and rollback (WSL)

After the build completes, first run:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Shared_Progression/Activate-Test.py --check
```

With all PTR players logged out, activate:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Shared_Progression/Activate-Test.py --activate --maintenance
```

If testing proves poor, with all PTR players logged out:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Shared_Progression/Activate-Test.py --rollback --maintenance
```

Activation verifies source hashes and image identity, starts privately without published ports, requires the experimental progression readiness marker and other installed modules, then restores the original PTR ports. Startup failure triggers rollback. Rollback refuses independently changed source or unexpected images. It must be reviewed before use if later unrelated server changes have been deployed.

## Testing priorities / rollback triggers

Compare Hero and Hybrid of different original classes at the same race, level and Primary Stat selection. Confirm base attributes and pools agree; racial differences still apply. Compare Class+ against its prior values. Test existing-character login twice, level-up, Hybrid selection, death/revival, and build/resource refresh without refills or stacking. Validate levels 10, 50, 51, 60 and 80.

Pay particular attention to survivability after level 50, mana availability, percentage-of-base-mana spell costs, and the effect of existing Primary Stat bonuses. Mark the change for rollback if these produce unacceptable balance. Race, gear, talents and Primary Stat effects mean visible totals will differ from base table values.

The startup-only setting `Hero.SharedProgression.Enable = 0` disables the new override and retains the old class behavior. The reviewed image/source rollback above remains the primary recovery procedure. No SQL migration or character database restore is needed.


## Source package

The original helpers and `integration.patch` belong to HeroFreePick. Full third-party core/module source and the private collected snapshot are excluded. Apply the patch to the matching server checkout and add the three SharedProgression files to `modules/mod-hero-starting-path/src/`, then rebuild. The pinned PTR scripts expect a local `overlay/` containing the six files identified in `source-manifest.json`; build backups and manifests are local-only. The owner workspace package already contains that overlay. Do not run activation against another server.

The isolated C++ test uses API doubles. Copy the three SharedProgression files into a temporary test directory alongside `tests/*`, then compile `SharedProgression.cpp test.cpp` with C++17 and run. A full AzerothCore build and in-game testing are also required.
