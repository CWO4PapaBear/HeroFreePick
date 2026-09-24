---
name: bear-cave-talent-modification
description: Use for any talent modification in the Bear Cave AzerothCore/WotLK Hero Advancement system, including creating a talent from scratch, changing its mechanics, name, tooltip, ranks, level requirements, costs, tree placement, prerequisites, or availability in Classic, Class+, Hybrid, and Hero. Covers client UI, authoritative server logic, required data migrations, testing, rollback, and release delivery.
---

# Bear Cave talent modification

Apply this workflow to every talent change. Scale the work to the change: a presentation-only edit does not require a server rebuild or database migration. A new mechanic requires authoritative server implementation, not just an addon tooltip. User instructions and current repository instructions take precedence over this guide.

## 1. Establish the intended behavior

Capture a concise implementation contract before editing:

- Name, icon, description, active/passive behavior, number of ranks, effects and values per rank.
- Minimum character level for each rank; talent/ability costs; required prior selections; tree, row, column and prerequisite links.
- Eligible modes and classes, including how Hybrid's original and second class affect eligibility.
- Learning, removal, respec, specialization change, death, target change/death, combat transitions, zoning and logout behavior where the mechanic has state.
- Stacking, caps, refunds, resource costs, cooldowns, forms, pets and vehicles where relevant.
- Whether existing owners automatically gain the change, require a build migration, or receive a refund/reselection.

Use existing decisions instead of asking again. Ask only for unresolved choices that materially change behavior. Do not infer that a tooltip rename authorizes changing costs, rank progression, or Classic gameplay.

Write a mode matrix and test against it:

| Mode | Default project expectation | Implementation obligation |
|---|---|---|
| Classic | Stock class/trainer progression and native talent behavior | Preserve unless explicitly included; avoid global DBC changes that silently alter it |
| Class+ | Custom progression for the selected original class | Check its actual talent acquisition and commit path |
| Hybrid | Eligible options from the chosen classes | Use authoritative selected classes, not only the character's native class |
| Hero | Free-pick policy | Respect current access rules; do not assume native class restricts the talent |
| Pending/unselected | No established custom entitlement | Do not grant custom effects merely because the mode is not Classic |

## 2. Find the current source of truth

Read applicable AGENTS.md files. Check repository branches, uncommitted changes, active server image/configuration, installed client files and the currently promoted PTR manifest.

Locate the live catalog, its generator inputs, server ownership/commit code, client renderer and mode policy. In this project useful search anchors include:

- `HeroFreePick/Catalog.lua`, profile catalogs, `HeroFreePick.lua`, `AscensionTalentOverlay.lua`, and addon TOC load order.
- `mod-hero-starting-path`, `GeneratedCatalog.h`, `StartingPath.cpp`, `ClassTrainerGate.h`, and `ClassTrainerPolicy.h`.
- `HeroBuild::Version`, rank `previous`/`next`, `native`, `spells`, `levels`, and menu identifiers.
- Existing integration packages in `tools/`, especially `tools/martial-fluidity`.

These are discovery anchors, not proof that a particular checkout is current. The older repository catalog and the live PTR catalog have had different schemas and versions. Never regenerate or deploy from an older profile without reconciling the live version.

For server work, collect a read-only, timestamped snapshot of affected current source and relevant schema/configuration; record hashes and the active image. Preserve recent unrelated fixes. If WSL cannot be accessed directly, prepare a bounded collector for the user to run. Do not substitute historical exports or weaken access controls.

## 3. Allocate identities and define a new talent

For a new talent, distinguish these identities explicitly:

1. Advancement/menu entry ID.
2. Server selection ID, including separate rank-node IDs when used.
3. Spell ID(s) implementing the effects and any triggered spells/auras.
4. Native talent ID, if integrating with native talent storage or native trees.
5. Catalog version and migration relationship to the previous catalog.

Search current client data, server spell definitions, catalogs and database overrides for collisions. Follow the repository's allocator and reserved ranges; do not invent an unused-looking ID or copy an example's IDs. A custom advancement talent does not automatically need a new native Talent.dbc row: choose the acquisition/storage route deliberately.

Prefer an existing, verified spell when its full behavior matches the request. Otherwise define the new spell and its dependencies: effect/aura types, targets, attributes, family masks, values, duration, periodic amplitude, range, costs, cooldown, visuals, icon, localization and triggered spell IDs. Validate referenced records exist. Imported Ascension identifiers or descriptions do not prove that stock WotLK implements their mechanics.

Update the maintained generator inputs and regenerate both client and server catalogs. Do not hand-edit only a generated header. For each rank, set its level requirement, cost, parent/prerequisites, previous/next links, menu mapping and effect spells. Validate acyclic prerequisites, reachable rank progression, unique IDs and sufficient point budgets at the intended unlock level.

Enforce the level and prerequisites on the server at commit/learn time. A greyed-out client button is not enforcement. Test level L-1, L and L+1, including requests sent without using the UI. Decide how already-owned talents behave if requirements change.

## 4. Implement server ownership and mechanics

Trace the actual learn/remove routes, not just the method names that seem appropriate. Native talents, learned spells, passive auras and advancement ledger selections are distinct forms of state.

**Martial Fluidity lesson:** Vigor's passive energy effect was active, but `HasActiveSpell(14983)` returned false because native talent ownership was held in `m_talents`. The corrected eligibility check considered `HasTalent(spell, GetActiveSpec())` as well as the intended learned-spell path. Confirm which routes are legitimate for the new talent before accepting them; do not universally replace ownership checks with `HasAura`.

- Gate custom effects using authoritative server mode/class/build state. Never trust addon-supplied entitlement.
- Respect the active specialization; a talent stored only in an inactive spec must not enable the effect.
- Trace direct `addTalent`, `addSpell`, learn, forget, reset and login reconstruction paths. Hooks for `learnSpell` may not cover native talent commits or direct mutations.
- Clear or preserve state exactly as specified on each lifecycle transition. A periodic check may help synchronization but is not a substitute for atomic removal/learning rules: same-tick remove/relearn can evade polling.
- Keep counters or resources separate when the native core reuses them. Stock combo machinery also serves Overpower; broad changes to clear/add/read paths can break other class mechanics.
- Inspect target-holder cleanup, death, duel completion, reactive timers, finishers, miss/refund ordering, aura expiry, logout and map removal when altering combo behavior.
- Register scripts and hooks in the actual loader/build, and add an identifiable readiness marker. Compilation alone does not prove registration or runtime eligibility.

For persistence, prefer an existing appropriate API and verify its configuration and schema on PTR. Martial Fluidity required `EnablePlayerSettings=1` (`AC_ENABLE_PLAYER_SETTINGS=1`); the first activation rolled back because it was disabled. Preserve previous settings in rollback configuration. Do not disable a readiness check to conceal a missing dependency.

## 5. Determine database and client-data changes

Inspect the actual database schema before producing SQL. Relevant existing tables may include `hero_build_test`, `hero_build_spells_test`, `hero_hybrid_choice`, `character_spell`, native talent storage, character settings, and world spell overrides. Their presence and columns must be verified; the list is not a migration template.

| Change | Data work to evaluate |
|---|---|
| Name/tooltip only | Mode-aware addon presentation; no SQL by default |
| Existing spell plus new server behavior | C++/script registration and configuration; SQL only for actual data dependencies |
| New spell or changed spell definition | Client Spell.dbc/related records and matching server DBC or `spell_dbc` override, according to the existing pipeline |
| Native tree integration | Talent/TalentTab and prerequisite/rank records where required by the chosen client/server path |
| New selection/rank or changed requirements | Client/server catalog regeneration and explicit compatibility/migration for saved selections |
| New persistent state | Existing supported settings API, or a narrowly scoped schema/data migration when necessary |

Server overrides do not automatically give the client a valid tooltip, icon or animation. Conversely, client DBC entries do not make the server effect functional. Establish which side reads each record and package all required dependencies.

When SQL is needed:

- Separate world and character migrations; pin expected old rows and back up only the affected data.
- Make repeat application detectable and safe. Validate schema and prerequisites before writing.
- Match table/column collations when comparing text. A previous activation failed on mixed `utf8mb4_unicode_ci` and `utf8mb4_0900_ai_ci`; fix the comparison or intended schema narrowly, not by converting the entire database.
- Test forward migration and rollback in a disposable database before touching live rows. Account for DDL that is not transactionally reversible.
- Preserve unrelated selections, earned levels, equipment and character progress. Do not roll back an entire character database to undo a talent change.
- Handle invalidated selections explicitly with a reviewed migration/refund policy; avoid login loops that repeatedly learn/unlearn spells and print alerts.

## 6. Integrate the user interface

Update the relevant mode/profile, not just the first catalog match. Check:

- Talent name, correct icon, tree grouping, row/column, prerequisites and route drawing.
- Rank controls, point costs, locked/learned states, level requirement text, search results, review dialog and accepted-build rendering.
- Tooltip name/body in Hero Advancement and native spell tooltips where applicable; spellbook/action-bar display if the talent grants an active ability.
- Existing Shift-toggle expanded details. Put technical IDs, advancement IDs, mastery inclusion and click instructions there according to current UI conventions.
- Resolve values from the effective server spell data, including tick count and total periodic damage. Do not invent values to fill placeholders. Keep genuinely unresolved mechanics highlighted in yellow; retain the current blue styling for resolved key numbers/times where that convention applies.
- Use paragraph spacing between complete tooltip sentences where requested by the current project style. Remove obsolete “server committing unavailable” text only where the mechanic is actually functional.
- Keep custom names/effects out of Classic when Classic is excluded. A global DBC rename or API override can leak into it.
- Maintain Lua 5.1 / Interface 30300 compatibility and correct TOC order.

For resource displays, specify which frames should show state. Shared player points may be valid without a target, but target-attached visuals must not float when the target frame has no target. Martial Fluidity should show points in both places with a target, and only on the player portrait without one. Preserve vehicles and native behavior outside the feature's scope.

If wrapping a native API, audit every consumer and preserve unrelated unit tokens/modes. Test target removal, reacquisition, target death, `/reload`, login, and mode changes. Synchronize authoritative state even when no new resource event occurs. Do not confuse hidden visuals with server-side loss of points.

## 7. Verify the complete feature

Use focused tests of real implementation paths, then in-game acceptance. Mocks must represent native talent storage separately from learned spells; the first Martial Fluidity tests missed this distinction.

Cover applicable cases:

- Each allowed mode; Classic and unselected modes as negative cases.
- Original and secondary Hybrid class, plus a Hero whose native class differs from the talent's class.
- Each rank's level boundary, prerequisites, cost, rank replacement, insufficient points and combat learning restrictions.
- Existing owner, newly learned talent, remove/relearn, respec, spec switch and login reconstruction.
- Gameplay outcomes rather than only tooltip changes: resource gain/spend, target switching/death, player death, Vanish/combat exit, refunds, aura expiry, zoning and relogging as relevant.
- UI placement, click/review flow, tooltip values, icons, resource visibility and stock frame interactions.

Run required repository checks/build.py and the full server compile when C++ changes. Record exactly what passed and what remains untested. Do not describe a mocked check or successful compiler run as in-game verification.

## 8. Build, activate and recover

Prepare hash-pinned source/client manifests, backups, an activation check and rollback before deployment. A build-only script must restore current source, report restoration errors and leave the running image/database/client unchanged.

If source changes after a build, rebuild before activation. Verify the built manifest matches the reviewed source. Fail closed on unexpected image, source, ports or compose configuration drift; investigate instead of deleting assertions.

Use the existing authorized PTR maintenance workflow. Verify players are offline before a restart. Validate the candidate privately before publishing normal ports, check all required module readiness markers and retain the previous image/configuration. Stop and investigate a failed validation; after rollback, verify the restored image and server readiness before another attempt.

For client installation, use the current installed client as the baseline, preserve unrelated fixes and back up changed files. Follow the existing closed-client installer and process check. A server-only repair does not require a new client download; a client-only display correction does not require a server rebuild.

## 9. Publish and report distinct outcomes

Follow existing authorization and repository policy for source commits/pushes. Keep HeroFreePick, More Minions and the launcher in their own repositories. Commit original code, maintained inputs/generators, narrow integration patches, tests and notes; exclude credentials, personal layouts, databases, proprietary baselines and generated binaries from source history.

Do not assume a source push publishes a client update. When launcher publication is requested or already authorized:

1. Start with the last promoted cumulative PTR candidate; overlay only reviewed client changes.
2. Compare every managed file with the working owner client and review additions, changes and removals. Preserve personal settings and unrelated addons.
3. Build versioned manifests, component archives, checksums and accurate patch notes; record the active compatible server build.
4. Test upgrade from the prior package, repeat installation, and personal-file preservation.
5. Push/verify source, upload release assets, verify remote checksums, publish the release, then commit/push the PTR channel pointer.
6. Verify the public updater resolves the intended version and hashes. Check any already-authorized Discord patch-note workflow; never expose webhook secrets or embed them in the client.

Keep Main unchanged unless explicitly included. Announce only verified outcomes: source commit/branch, build status, active PTR image, local client installation, in-game acceptance, launcher version/promotion, and patch-note result. Include rollback instructions and remaining limitations when material. A source directory containing the final payload is not proof that the repository's default build packages it; verify the actual release pipeline used.
