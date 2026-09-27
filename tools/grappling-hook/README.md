# Grappling Hook — staged PTR implementation

Full PTR compilation and activation preflight passed. Matching client files were installed locally with verified backups. **Server activation and in-game acceptance are pending. No launcher release is included.**

Available at level 28 for Rogue Class+, Hybrid containing Rogue, and Hero. Costs 3 ability points and 2 Legendary rarity gems. Classic remains unchanged. The additive catalog entry retains the current catalog version, so existing builds do not require migration/reset.

The initial ground cast reaches up to 30 yards with a 35-second cooldown. A temporary action-button replacement permits one hostile-target follow-up within 10 yards for three seconds. The follow-up roots its target for one second. Native spell flags allow stealth. Movement follows a validated navigation path; blocked paths, water, vehicles, transports, flight, falling and movement-control states are rejected. This conservative implementation is not a teleport and may reject cliff shortcuts.

## Package and integration

These are original source overlays and the exact local staging tools, not a standalone blind installer. Copy this folder into the established workspace at `outputs/Hero_Grappling_Hook` before using the commands. Collect a fresh baseline and review differences. The tools require the current Hero starting-path module, existing workspace MPQ utilities, authorized local client/reference data and Docker PTR configuration. No extracted archives, credentials, database exports or binary artwork are distributed here.

`integration.patch` shows only the four changes to existing source files. Install `HeroGrapplingHooks.h` under `src/server/game/Spells`, and `GrapplingHook.cpp` under `modules/mod-hero-starting-path/src`. The two core hooks are inert when the module does not register callbacks. The spell script relies on the existing authoritative Hero ownership policy. Do not replace the entire core or import the CoA fork.

Spell IDs: 760056 initial, 760094 follow-up, 760095 root, 760096 temporary window, 760058 tether. Entry/token 26001633. All collisions are checked. SQL adds only three owned script bindings. Stock World Trigger 18721 supplies the temporary anchor. Definitions use supported WotLK dummy/root effects instead of unsupported Ascension aura 337.

Client staging preserves unrelated spell records/archive entries. Visual dependencies are cloned under isolated IDs/paths, preserving the original chain and whoosh sounds. Obsolete FreezingFinger missile-targeting kit 34 is omitted. Unchanged visual tables are not overridden, preserving existing model-attachment differences. SpellIcon 5827 is added after collision checks. Native action-bar replacement still requires gameplay verification.

## Exact operator commands

Read-only snapshot (WSL):

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Collect-Server.py
```

Read-only cast/action persistence supplement (WSL):

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Collect-Cast-Routing.py
```

After reviewing the snapshot, stage with `Prepare.py`, run `Test.py`, then `Prepare-Visuals.py` and `Prepare-Client.py` using Windows Python. These preserve the installed client. Close WoW before `Install-Client.py`; that installer checks baseline hashes, backs up all replaced files, verifies copies and restores them on failure.

Full build; current source restored afterward (WSL):

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Build-Test.py
```

Preflight; supports a stopped worldserver (WSL):

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Activate-Test.py --check
```

Only during arranged maintenance with zero players and matching local client installed:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Activate-Test.py --activate --maintenance --client-ready
```

Activation checks private startup before reopening existing PTR ports. Failure attempts rollback of owned bindings, source, image and DBC mounts. Main is untouched. Unlearn Grappling Hook through the advancement menu before intentional rollback; rollback refuses to invalidate existing selections.

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Activate-Test.py --rollback --maintenance
```

## Acceptance before tester publication

- Learn at level 28 with sufficient AP/gems; reject level 27, ineligible Class+/Hybrid and Classic.
- Check ground-target cursor, range, cooldown, path rejection, stealth preservation, rope/icon/sound and movement.
- Verify the same action button becomes the follow-up for three seconds, allows one hostile cast within 10 yards and then restores the initial spell. Check the one-second root and no extra initial cooldown charge.
- Test expiry, death, logout/relogin, unlearning, dragging the temporary button and reconnecting during the window. The follow-up must never persist as a learned permanent spell or saved action ID.
- Check transports, water, walls, cliffs and crowd control; invalid casts must not move the player.
- Regression-check prior rune recovery, Battle Pass spins, warrior stance changes, portraits and existing visual fixes. Mock tests and a successful build do not prove in-game behavior.
