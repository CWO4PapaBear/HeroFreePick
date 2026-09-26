# Warrior stance exemptions — PTR test

Charge (100, 6178, 11578) and Thunder Clap (6343, 8198, 8204, 8205, 11580, 11581, 25264, 47501, 47502) no longer require a Warrior stance in Class+, Hybrid or Hero. Classic and pending/unselected modes retain their original rules. Spell ownership, combat restrictions, rage cost, range, cooldown and damage are unchanged. Bear, Cat and other non-Warrior forms are not exempted.

## Implementation

The Hero Advancement module maintains a hidden support aura, spell **9905301**, from validated server mode state. It is removed outside eligible modes/forms and restored after resurrection/login. It is not a learned spell or talent, costs no points, and has no proc or triggered effect. The existing twelve spells retain their original stance fields.

The native `SPELL_AURA_MOD_IGNORE_SHAPESHIFT` effect targets Warrior family word C bit 29 (`0x20000000`). The collector and preparation tools check this bit against both Spell.dbc and world `spell_dbc` overrides. Only the twelve named ranks receive the new bit. Existing family-mask relationships are preserved. Do not replace this mask with Charge's ordinary bit: it also matches unrelated creature abilities.

The aura is deliberately non-passive with infinite duration, hidden in the UI, and non-cancelable. A cast-only passive aura is not sent to the client, so it cannot reliably inform native client stance checks. Its hidden/stance properties prevent normal aura persistence; server mode publication and login/update also remove ineligible copies.

The original definition uses the existing effect 275 and native client support. No core patch, SQL migration, new catalog entry, or spell-rank replacement is needed. Install matching client Spell.dbc data before testing. The server mounts a separate reviewed Spell.dbc read-only; rollback restores the prior compose mounts without overwriting the underlying DBC volume.

## Commands on this workstation

From WSL:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Warrior_Stances/Collect-Server.py
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Warrior_Stances/Build-Test.py
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Warrior_Stances/Activate-Test.py --check
```

Collection is read-only. Preparation and tests run locally between collection and build. Build restores source and does not restart PTR. Preflight verifies the compiled source, current image/compose, spell data and SQL collisions; it does not activate.

After preflight passes, matching client installation is verified, and PTR maintenance has removed all players:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Warrior_Stances/Activate-Test.py --activate --maintenance --client-ready
```

Activation validates startup without published ports before restoring the existing ports. Failure attempts rollback and records logs. Stop for review if rollback fails.

Rollback during maintenance:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Warrior_Stances/Activate-Test.py --rollback --maintenance
```

From Windows PowerShell at the workspace root, with WoW closed:

```powershell
& 'C:/Users/danie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' outputs/Hero_Warrior_Stances/Install-Client.py --check
& 'C:/Users/danie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' outputs/Hero_Warrior_Stances/Install-Client.py
```

`Prepare.py` verifies the captured data and emits the source/DBC candidate. `Test.py` verifies exact data changes and compiles lifecycle tests for the production module header. `Prepare-Client.py` uses the existing offline MPQ helper at `work/github-upload/tools/lib/mpq.py`, preserves each archive's own data and checks every resulting entry. `Test-Installer.py` verifies interruption rollback and repeat installation. These helper/compiler dependencies are local tooling, not server dependencies. Generated client/server DBCs, database snapshots, MPQs and private deployment records do not belong in source Git history.

## In-game regression checklist

- Test Charge and Thunder Clap in no stance, Battle, Defensive and Berserker Stance in Class+, Hybrid (including secondary Warrior) and Hero (including a non-Warrior original class).
- Test Classic as the negative control: original stance requirements remain. Pending characters receive no exemption.
- Confirm native action buttons, spellbook casting, tooltips and normal macros agree. This is a native-aura approach; no tooltip-only workaround is installed.
- Confirm Charge remains blocked in combat unless an independently owned stock effect permits it; costs, cooldowns and range remain unchanged.
- Confirm unrelated stance abilities and non-Warrior forms are unaffected. Test death/resurrection, relogging and mode transitions.
- Test every rank, particularly newly learned/upgraded ranks. Keep the previous image, mounts and local client backups for rollback.

Offline tests and the full server compile passed. Server activation completed on PTR and matching client data is included in PTR 0.2.11-test.1. The full in-game regression matrix above remains unverified; continue testing it on PTR.
