# One-yard ground-anchor offset - compiled, activation pending

The owner requested spawning the initial visual anchor below ground after reducing its scale did not lower the connection. This patch copies the selected destination to a separate Position and subtracts one yard from only its Z for the temporary helper spawn. Movement still uses the original validated path; enemy follow-up, visual aura lifetime, client files and database records are unchanged. The helper retains 1% scale.

Full server build passed and source restoration completed without errors. In-game height is not yet verified. No launcher publication. Source is a scoped supplement to the preceding ground-anchor package, not a standalone module.

Scripts run from workspace outputs/Hero_Grappling_Hook_Below_Ground. Its reviewed baseline derives from the preceding full snapshot, activated build and subsequent read-only source capture. Build rechecks every source hash and live image/compose identity rather than assuming the derived baseline is fresh.

Preflight:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Below_Ground/Activate-Test.py --check
```

After successful preflight and arranged maintenance:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Below_Ground/Activate-Test.py --activate --maintenance --client-ready
```

Rollback restores the previous image/source, preserving existing spell selections and SQL:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Below_Ground/Activate-Test.py --rollback --maintenance
```
