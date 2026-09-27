# Resources, commands and worked example

Commands below are historical workstation examples verified during the Grappling Hook investigation. Inspect paths and script behavior before reuse. Read-only collectors write local exports; they do not authorize activation. Put commands in separate copyable code boxes for the owner.

## Resource map

| Resource | Use |
|---|---|
| `CWO4PapaBear/HeroFreePick`, `outputs/HeroFreePick-Main-Publish` | Advancement catalogs, original server modules, converter, tests and skills; publish to `main` |
| `CWO4PapaBear/More-Minions` | Pet implementation dependencies, maintained separately |
| `CWO4PapaBear/Bear-Cave-Launcher`, `outputs/Bear-Cave-Launcher` | Cumulative client release, asset hashes and PTR channel |
| `jealous-sound/azerothcore-wotlk-coa`, `work/coa-core-reference` | Owner-designated world/system reference; see `docs/COA-DEVELOPMENT-REFERENCE.md` for pinned revision and subsystem index |
| `/home/dml/games/wow-server-classless-test` | PTR source; compare with active image and build manifests |
| Docker `classless-test-worldserver` | Active image and `/azerothcore/env/dist/data/dbc`; resolve configured data path and bind mounts |
| Docker `classless-test-database`, `acore_world` | Effective spell overrides, script bindings, rank/linked spells, creatures and AI |
| `acore_characters` | Mode/build ownership or durable state only when required; inspect current schemas |
| `work/area52-review/spell-extract/ascension-live_Data_area-52_patch-D.MPQ.Spell.dbc` | Local Ascension reference, 234-field format in this export; not proof of server behavior |
| `server/spell-definitions/convert.py` and `data/` | Field mapping, compatibility/dependency checks, supporting DBC rows and visual provenance |
| `D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test` | Owner's installed client; preserve latest patches and local settings |

## Collect and inspect

The Grappling Hook collector exists in the task workspace, not this repository. It exports spell/movement/scripting source, relevant Hero modules, current DBCs, spell overrides/bindings and anchor data. Run in WSL:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook/Collect-Server.py
```

It verifies the compose project, records the active image/configuration path and hashes all exported files. Follow `latest-baseline.json` to `manifest.json`; require `status: complete`. The collector uses `docker exec ... cat` for active DBCs because `docker cp` previously failed on a read-only per-file bind mount. If the container is stopped, resolve its inspected mount sources and read them without starting the server; do not presume the active-container command will work.

Extract the twelve reference spell records locally in PowerShell, from the workspace root:

```powershell
& 'C:/Users/danie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' outputs/Hero_Grappling_Hook/Inspect-Ascension.py
```

This writes `ascension-reference.json`, verifies the WDBC header/record size, and includes the source SHA-256. Source hash observed during this investigation: `5e85f10ccb861e8463e838caaa46630050bd8f6b73bc5ddf6378eb879f69c263`. A different hash requires inspection, not automatic rejection of newer data.

Read-only SQL example inside WSL; credentials stay inside the database container and are not printed:

```bash
docker exec -i classless-test-database sh -c 'MYSQL_PWD="${MYSQL_ROOT_PASSWORD:-$MARIADB_ROOT_PASSWORD}" mysql -uroot --default-character-set=utf8mb4 --batch acore_world' <<'SQL'
SHOW COLUMNS FROM spell_dbc;
SELECT * FROM spell_dbc WHERE ID IN (760056,760057,760058,760059,760078,760091,760092,760093,760094,760095,760096,760097);
SELECT * FROM spell_script_names WHERE ABS(spell_id) IN (760056,760057,760058,760059,760078,760091,760092,760093,760094,760095,760096,760097);
SELECT * FROM creature_template WHERE entry=840057;
SQL
```

Do not assume world SQL contains every effective spell: combine it with the loaded `Spell.dbc` and SpellMgr corrections. Parse MySQL batch rows using literal LF/tab separators before decoding escapes, as described in the tooltip review skill.

Bounded source discovery, from the publication checkout:

```powershell
rg -n 'Grappling|760056|760096' server --glob '*.cpp' --glob '*.h' --glob '*.py' --max-columns 240 --max-columns-preview
```

Inspect converter command options before running a generation command:

```powershell
& 'C:/Users/danie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' server/spell-definitions/convert.py --help
```

## Grappling Hook: verified reference, not a completed implementation

| Evidence | Decoded result |
|---|---|
| Main spell `760056` | Ground destination; 35-second recovery; range index 4 resolves to 30 yards |
| Main tooltip | Recast after the first grapple, pull to an enemy and root; does not break stealth |
| Recast aura `760096` | Duration index 27 resolves to 3 seconds; aura 337 is unsupported by the reviewed core |
| Follow-up `760094` | Enemy-targeted; range index 7 resolves to 10 yards; references `760097` and `760095` |
| Root `760095` | Aura 26; duration index 36 resolves to 1 second |
| Summon misc value | Creature entry `840057`; this is not a spell-ID dependency |
| Additional named records | `760057–760059`, `760078`, `760091–760093`, `760097` contain movement/visual/sound or dummy behavior requiring investigation |
| Sound helper `760059` | Effect 168 is outside the reviewed converter's supported effect range |
| Installed client catalog | Entry `26001633` reports missing server definition `760056` |

These records show why importing only the root and tooltip references is insufficient. Do not treat similarly named legacy/NPC Grappling Hook records as the Rogue ability. Do not assume the exact original server sequencing can be recovered from names alone.

The subsequent aura survey found 59 records using 337, including explicit action-bar-transform descriptions. CoA still leaves its handler null, but implements `Player::SetTemporarySpellReplacement` plus cast routing and ability-specific cleanup elsewhere. Use that as a scoped implementation reference, not proof of a generic 337 port. Grappling Hook's recast row has zero base points, so its replacement ID must be supplied from corroborating records/logic.

The approved target behavior preserves the timings above, eligibility in Rogue Class+, Rogue-containing Hybrid and Hero, and Classic isolation. Implementation and in-game acceptance remain separate work; this reference does not certify the spell as working.

## Build, activation and publication command conventions

Use task-specific reviewed scripts. At creation of this skill, Grappling Hook has **only** the collection/reference scripts above; do not invent or invoke nonexistent build/activation helpers. When those helpers are implemented, add their actual invocation, side effects, expected success output and rollback behavior here.

Established examples to inspect for implementation patterns, not run against Grappling Hook unchanged:

- `outputs/Hero_Warrior_Stances/Prepare.py`: matching spell-data transform, source manifests and collision guards.
- `outputs/Hero_Warrior_Stances/Build-Test.py`: baseline-pinned full build and source restoration. Its historical `docker cp` assumption needs reconciliation with current bind mounts.
- `outputs/BattlePass_Spin_Integration/Build-Test.py`: raw-byte source preservation after a CRLF mismatch; source restoration must succeed.
- `outputs/BattlePass_Spin_Integration/Activate-Test.py`: separate check/activation/rollback operations; adapt only relevant checks rather than importing Battle Pass schema requirements.

Validate this skill locally:

```powershell
& 'C:/Users/danie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'C:/Users/danie/.codex/skills/.system/skill-creator/scripts/quick_validate.py' .agents/skills/bear-cave-spell-implementation
```

## Implemented Grappling Hook staging workflow

The reviewed source and exact build, preflight, maintenance activation and rollback commands are in [tools/grappling-hook/README.md](../../../../tools/grappling-hook/README.md). The package includes the original module, optional core hooks, additive client catalog, source integration diff, collision-checked DBC staging, isolated visual dependencies, backup client installer and offline regression checks. Read the status before use: compilation/preflight and local installation do not establish server activation or in-game acceptance. Do not import proprietary local archive outputs into Git.
