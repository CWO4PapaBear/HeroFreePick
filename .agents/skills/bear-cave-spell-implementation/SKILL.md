---
name: bear-cave-spell-implementation
description: Implement a new, missing, or incomplete Bear Cave server spell using Ascension or other client spell records and tooltip intent as evidence. Use for gameplay implementation, dependency repair, and matching advancement/client integration; use the server-tooltip-review skill for presentation-only corrections.
---

# Implement a spell from client evidence

Turn the approved behavior into a working, independently installable AzerothCore implementation. Client records explain intent and presentation; they do not contain the original server scripts. Never equate a valid imported row, resolved tooltip, or successful build with working gameplay.

Read the repository AGENTS.md and the adjacent [server tooltip review skill](../bear-cave-server-tooltip-review/SKILL.md). Use its effective-data reconstruction and provenance rules rather than repeating its numeric resolver. For talent changes, also use the adjacent [talent modification skill](../bear-cave-talent-modification/SKILL.md). These skills complement each other: tooltip review establishes what is known, this skill supplies missing mechanics, then tooltip review verifies the description against those mechanics.

## 1. Establish the behavior and current baseline

Identify the advancement entry, source spell ID, every rank, and existing acquisition requirements. Record an approved behavior contract: targets, range, resource cost, cast time, cooldown, duration, effects, stealth/form interactions, recast behavior, and mode eligibility. Distinguish directly decoded values, inferred behavior, and unresolved design decisions. Do not silently substitute retail behavior or simplify an approved mechanic.

Use the current HeroFreePick publication checkout (`outputs/HeroFreePick-Main-Publish`) and remote `main`; historical workspaces explain decisions but are not deployment baselines. Keep More Minions and launcher repositories separate. Verify the active PTR image, source, effective DBCs, SQL overrides and relevant script registrations with a fresh read-only export. Paths, exact commands, and the Grappling Hook example are in [references/resources-and-commands.md](references/resources-and-commands.md).

Capture hashes and missing-data failures. Source on disk is not automatically identical to the compiled image: correlate build/activation manifests. Do not collect account credentials or unrelated character data. If WSL is inaccessible, prepare a runnable read-only collector and ask the owner to run it while continuing independent client/reference work. Existing task authorization remains valid; the skill itself does not add an approval gate.

Consult the owner-designated [CoA development reference](../../../docs/COA-DEVELOPMENT-REFERENCE.md) for relevant implementations, SQL, extended-client research and tests. Pin its revision and account for CoA-specific classes/protocol/core hooks. An enum slot labelled unknown or a null handler is evidence of missing support, even if nearby spells have bespoke implementations.

## 2. Reconstruct the dependency graph

Trace more than numeric trigger references. Include:

- Main spell, ranks, auras, secondary/recast spells, proc spells, summoned creature or gameobject templates, and any AI/scripts they depend on.
- `spell_dbc`, `spell_script_names`, `spell_ranks`, `spell_linked_spell`, conditions and coefficient/proc tables when relevant. Inspect actual schemas before querying or generating SQL.
- Duration, range, radius, cast time, icon and visual DBC references; models, textures, sounds and particles used by those visuals.
- Server scripts that link otherwise disconnected records through hard-coded IDs, summon AI, dummy effects, events or aura handlers. A trigger-only importer will miss these.
- Client UI behavior needed to operate the mechanic: targeting, action-bar transitions, cooldown display, tooltip dependencies and spellbook visibility.

Decode against the actual source format and current core enums. The existing converter checks WotLK-compatible bounds; do not disable those checks to import Ascension extensions. Classify each dependency as reusable, missing, incompatible, scripted, or unverified. Search large generated Lua catalogs with bounded extraction rather than dumping an entire minified line.

## 3. Design the server implementation

Prefer a scoped SpellScript/AuraScript and original module code over broad core changes. Use the server as the authority for ownership, mode, resource/cooldown state, targets and rewards. If a core hook is necessary, keep it narrowly scoped, versioned where appropriate, and explain why module hooks cannot suffice.

Replace unsupported source effects with supported effects and explicit server logic. Do not allocate an unsupported aura enum merely to make the source record load. Preserve approved timing and targeting semantics and document intentional differences from the reference.

For movement spells, validate map, target, range, line of sight, destination height, movement restrictions and the travel path before committing the cast. Reject unusable or incomplete paths and do not turn path failure into an unrestricted teleport. Decide how interrupted travel, moving targets, transports and arrival effects behave; test the relevant cases. Apply roots/stuns through the core so immunity and diminishing-return behavior can work normally.

For temporary spell replacement/recasts, verify both the server authorization and native 3.3.5 client operation. An aura that exists in Ascension may have no equivalent here. Do not assume secure action-button attributes can be rewritten in combat. Test the selected native mechanism or secure UI approach before promising parity. Restore the ordinary button and cooldown on use, timeout, death, logout, mode/build changes and failed casts. Temporary abilities must not become permanent learned spells or stale saved action buttons.

Keep runtime state bounded and clean it up. Use durable, idempotent database operations only when the feature actually requires persistence; a short recast timer normally does not need a new character table.

## 4. Integrate acquisition and modes

Trace the current authoritative mode/build checks rather than testing the character's original class. Classic remains stock. Apply the approved Class+, Hybrid and Hero eligibility, including a non-native-class Hero. Do not assume every custom mode grants every spell automatically.

Preserve level, point, rarity and prerequisite costs unless the owner changes them. Update catalog generation, server grant validation, rank expansion, respec/removal and client availability together. Support spells should not appear as independently purchasable abilities unless intended. A client-only warning removal does not authorize a server grant.

Use an explicit compatibility contract for independently installable modules: required core hooks, module dependencies, configuration defaults, reserved IDs, SQL ownership and registration entry points. Reuse the existing spell's ID when appropriate; check collisions before reserving new IDs. Avoid coupling the feature to unrelated module internals or importing third-party module source into HeroFreePick.

## 5. Stage matched data and code

Build from the fresh baseline and preserve unrelated source/DBC/SQL changes. Hash raw bytes: `read_text()` newline normalization can falsely report baseline changes or alter source. On a mismatch, inspect and rebase the staged change; do not bypass the guard.

Produce deterministic server definitions, script bindings, client DBC/visual additions, advancement overlays and a manifest. A server SQL definition is not a client DBC installation. Confirm effective load/override order and that referenced assets exist in the client's effective archive order. Keep original artwork/DBC extracts and private exports out of source control.

Prepare exact apply/inverse SQL and backup/hash-checked source/client installation. For SQL, preserve pre-existing rows and bindings and guard expected values; do not broadly delete by ID range or script prefix. For archives, patch the latest cumulative client payload rather than replacing it with an old candidate.

## 6. Verify in layers

1. Run format/dependency checks and tests of the actual behavior contract, including rejection paths and cleanup. Validate Lua 5.1/Interface 30300 and current API availability.
2. Compile against the current PTR core. A helper compile or mock test is not a full server build. Record the image identity and source restoration result.
3. Test SQL apply/inverse on an isolated database and startup with the matching data. Confirm scripts are registered, bound and validated; distinguish harmless legacy logs from new failures using evidence.
4. Verify gameplay in eligible custom modes and Classic isolation. Include repeated casts, cooldowns/resources, interrupted/invalid casts, reconnect/respec, and the feature-specific cases above. Check visible animation and actual server outcome separately.

Do not remove implementation warnings until the corresponding implementation evidence exists. Label staged, compiled, activated and gameplay-tested states accurately. Resolve expected effects, ranges and durations back into tooltips with the tooltip review workflow; retain honest unresolved details.

## 7. Release within the authorized scope

Prepare a reviewed activation/rollback command that supports the server already being shut down. Zero players alone is not proof that concurrent changes cannot occur; pin the expected image, source, SQL and client payload. Preserve unrelated fixes and the previous image/backups. Perform activation only within the user's authorized deployment scope; do not infer maintenance approval from a request for a plan.

At a completed development milestone, run relevant repository checks/build, review the scoped diff, update notes, fetch/reconcile `origin/main`, commit, push without force, and verify the remote SHA. Keep source publication, server activation, local client installation, launcher asset publication/channel promotion and Discord announcements separate. Publish client releases or send announcements only when authorized. Include actual test status and known limitations in the handoff.
