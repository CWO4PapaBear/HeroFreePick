# CoA reference for Bear Cave development

Owner-designated reference: https://github.com/jealous-sound/azerothcore-wotlk-coa

Reviewed revision: `47dd22ffe6d0a82e6886487f38acff7c5cfeb117` (`main`). A complete shallow reference checkout is available locally at `work/coa-core-reference` under the workspace root. It includes all tracked files at that revision, not the full commit history, external clients, or untracked runtime data. Fetch and record the revision before a future review; do not silently change the basis of an existing comparison.

The repository describes itself as an independent reconstruction. It is a useful implementation reference, not Ascension's official backend or proof of gameplay parity. Our active PTR, Hero mode rules, stock 3.3.5 client and current patches remain the integration baseline. Do not merge the whole fork or bootstrap its world package into PTR as a shortcut.

## Where to look

| Area | Reference paths |
|---|---|
| Project overview and compatibility scope | `docs/coa/README.md`, root `README.md`, `AGENTS.md` |
| Custom classes, progression, collections, protocol and resources | `src/server/coa/`; older instructions may call this `modules/mod-ascension-compat`, but that is not its current location |
| Generic spell/aura/movement behavior | `src/server/game/Spells/`, `Entities/`, `Handlers/`, `Movement/` |
| World, quests, creatures, instances and class scripts | `src/server/scripts/`, `src/server/game/`, `data/sql/` |
| World data and schema provenance | `data/coa-world/baseline.json`, `data/coa-world/coa-world-20260912.zip`, `apps/coa-world/README.md` |
| Historical CoA migrations | `modules/mod-ascension/data/sql/`; preserve migration filenames/hashes |
| New migration examples | `data/sql/updates/pending_db_*/` |
| Other optional systems | `modules/`, including the Destiny Weaver scaling implementation; inspect dependencies/configuration separately |
| Class implementation notes and unresolved work | `docs/coa/*-completion.md`, follow-up documents, `verification.md`, `local-release-state.md` |
| World scaling and progression | `docs/coa/restoration-map.md`, `level-scaling.md`, `level-scaling-vs-main.md`, `src/server/game/Miscellaneous/LocalLevelScaling.h` |
| NPC restoration | `docs/coa/npc-restoration.md` |
| Client data extraction/analysis tools | `apps/coa-dbc/`, `apps/coa-spells/`, `apps/coa-mechanics/` |
| Focused tests and in-game harness | `apps/coa-tests/`, `apps/coa-gameplay-test/`, `src/test/` |
| Spell calculations and extended client tables | `.agents/docs/systems/ascension-spell-parity.md` |
| Character creation and talents | `.agents/docs/systems/ascension-character-creation.md`, `ascension-talents.md` |
| Build, SQL and script conventions | `.agents/docs/`, `CMakeLists.txt`, `conf/dist/`, `src/server/coa/conf/` |
| Supporting architecture decisions/tools | `docs/adr/`, `apps/`, `tools/` |

This is a navigation index, not a claim that every subsystem has been audited. Read the relevant code, SQL, tests and status documents together. Source-complete, compiled, deployed and gameplay-verified are distinct states even where a document says “completion.”

## Reuse procedure

1. Pin the source commit and relevant files; record the active PTR counterpart and differences.
2. Check whether the example depends on the extended Ascension client, CoA custom class IDs, its protocol adapters, SQL schema, core hooks, or other components.
3. Extract the smallest applicable design. Keep Bear Cave's Class+/Hybrid/Hero authorization based on the persisted play style/build rather than a CoA class-number check.
4. Preserve license notices and attribution for reused code. Inspect source-file notices as well as the root license; the repository documents differing inherited notices.
5. Adapt into the appropriate independently installable Bear Cave module, with a minimal versioned core hook only where necessary. Do not publish this entire reference checkout or its bundled database in HeroFreePick.
6. Test against our current core/client; use isolated databases for world comparisons and migrations. Never apply an empty-world bootstrap command to populated PTR.

Read-only local commands (PowerShell, workspace root):

```powershell
git -C work/coa-core-reference rev-parse HEAD
```

```powershell
git -C work/coa-core-reference ls-files
```

```powershell
rg -n 'SetTemporarySpellReplacement|GetTemporarySpellReplacement' work/coa-core-reference/src/server
```

## Grappling Hook and aura 337 findings

The Ascension Spell.dbc reviewed for Grappling Hook contains **59 spell records** using aura 337. Several explicitly describe an action-bar transform. Examples: `272186` transforms Blink into Time Warp, and `274938` transforms Lesser Healing Wave into Tidal Shield. Other records pair the original spell in `EffectMiscValue` with a replacement-like value in `EffectBasePoints`; this pattern is evidence, not a fully decoded universal field contract.

Grappling Hook's `760096` has aura 337, original spell `760056` in its first misc value, and duration index 27 (3 seconds). Its base points are zero, so it does **not** directly encode follow-up `760094` there. Additional script/runtime knowledge is needed to supply that mapping. The linked follow-up's description and related records identify the intended second action.

At the pinned CoA revision:

- `src/server/game/Spells/Auras/SpellAuraEffects.cpp` maps 337 to `nullptr`, labelled unknown Ascension aura. There is no generic implemented 337 handler to port.
- `Player::SetTemporarySpellReplacement` and `GetTemporarySpellReplacement`, in `src/server/game/Entities/Player/Player.cpp`, keep an in-memory replacement map and send `SMSG_SUPERCEDED_SPELL`. The setter requires both original and replacement to be active spells.
- `src/server/game/Handlers/SpellHandler.cpp` routes an original cast request through that replacement before queue handling.
- `src/server/coa/AscensionBloodmageHemostasis.cpp` demonstrates a temporary follow-up window and restoration, with tests in `apps/coa-tests/bloodmage_hemostasis/`.

This supplies a concrete architectural reference for our WotLK-compatible recast implementation, not a drop-in Grappling Hook implementation. Port only the required behavior and verify cooldown retention, targeting, ownership, cleanup and saved action buttons with our client. No generic aura-337 support or Grappling Hook gameplay has been activated by this review.
