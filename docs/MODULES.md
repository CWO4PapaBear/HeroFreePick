# Hero Advancement modular release 0.31.0

## Status

Classic is client-only and uses stock LearnTalent requests only after Accept. Its menu and acknowledgment flow pass mocked Lua 5.1 tests; in-game confirmation is still required. The other profiles are usable local previews. Their server packages are policy foundations, not finished playable progression modules. WSL access was denied in the build environment; no AzerothCore binary was compiled or server deployment performed.

## Independent downloads

- Classic-addon: install HeroFreePick in Interface/AddOns. No server module, database change, client DBC patch, or core-source modification.
- ClassPlus-preview-addon: install HeroAdvancement_ClassPlus alongside HeroFreePick. Its server policy package requires server-foundation only.
- Hybrid-preview-addon: install HeroAdvancement_Hybrid alongside HeroFreePick. Includes the Class+ starting path, so the separate Class+ profile/module is not required. Its server policy package requires server-foundation only.
- Hero-preview-addon: install HeroAdvancement_Hero alongside HeroFreePick. Its server policy package requires server-foundation only.
- complete-development-bundle: contains all client and server packages. Addon folders belong in Interface/AddOns; mod-* folders belong in AzerothCore/modules. Do not place the entire bundle in either location.

The separate original server policy modules use the Player/World script style present in the local AzerothCore export. Rebuild is required; hook compatibility with other core revisions is unverified. No core patch is included.

## Choices

On first arrival at level 1, a non-dismissible selection panel offers Classic, Class+, and Hero only where installed. Installing Hybrid alone also offers the Class+ starting path. Hybrid is not an initial choice. At level 10 (or the next login above 10), Class+ characters with Hybrid installed choose either Continue as Class+ or Become Hybrid, then choose a second class distinct from the original. Continue records the decision and does not repeatedly prompt. Class+ hover text explicitly explains the level-10 opportunity and states when the Hybrid module is missing.

Choice persistence is currently local SavedVariables and is NOT server enforcement. The addon can present a required choice, but cannot prevent an addon-disabled player from bypassing it. Characters already above level 1 without a saved choice remain Classic; migration needs a server-owned policy. No new character-creation classes are introduced.

## Rules

| Mode | Classes | Talent requirements | Commitment |
|---|---|---|---|
| Classic | Original | Stock tree investment, prerequisites, ranks and server points | Standard native requests after Accept; trainer reset |
| Class+ | Original | Level 10 + 5 per tier; point budget | Preview; server integration pending |
| Hybrid | Original + chosen second at 10 | Same level-only tiers; point budget | Preview; server integration pending |
| Hero | All | Same level-only tiers; point budget | Preview; server integration pending |

Classic abilities stay trainer-learned. Classic talent tooltips use native GetTalent tooltip data, with pending editing instructions. Custom talent tooltips show spell effects, tier-required level and pending ranks, without claiming tree investment is required. All custom modes retain free-pick AP/TP, rarity and Mastery costs. Resource-over-budget ability preparation remains editable; server validation must refuse an invalid final build.

Classic commits are a sequence of ordinary learning requests, not an atomic transaction. Every rank waits for a server-reported rank change. Combat or rejection stops the sequence; already confirmed ranks remain learned and require a trainer reset. While a commit is running, editing/cancelling is disabled. On cancellation after a partial failure, the local baseline is re-read from the server rather than pretending confirmed ranks were undone.

## Server work still required

- Authenticated addon protocol with bounded requests, revisions, idempotency and confirmations.
- Server-owned initial/Hybrid choices, immutable class eligibility and database persistence.
- Canonical ability/talent catalog with stock spell compatibility checks and duplicate identity handling.
- Atomic build application/refunds and persistence, reset price validation and money deductions.
- Cross-class equipment, power types, forms, pets, resource bars and spell mechanics compatibility.
- Compilation and end-to-end tests against a stock supported AzerothCore revision.

ModeRules.h accepts only server-owned character/catalog data. The current startup module registers profiles and explicitly logs that mutation is not implemented. It never grants spells or changes an existing character.

## Validation

Run `python test_ui.py`, then `python build.py`. Portable C++ policy tests: `g++ -std=c++17 -Wall -Wextra -pedantic server/tests/mode_rules.cpp -o mode-rules-test && ./mode-rules-test`. CI includes this test; it has not been executed locally because no C++ compiler is available here.

Local development installer: `python3 .../Hero_Classless_UI/install.py` installs all three optional preview addons by default. Use `--modes` with no following values to install only the shared addon (already installed profiles are not deleted). Restart the client to detect optional addons. Release users should extract only desired addon ZIPs into Interface/AddOns.

## Optional persistent Class+ runtime

The ClassPlus-enrollment-runtime package is separate from Classic and the policy-only modules. Read `server/mod-hero-starting-path/README.md` before installation. Do not combine its trainer hooks with the separate foundation module. Existing `_test` table and addon folder names are retained for upgrade compatibility; no character-name prefix is required. Full server compilation and in-game enrollment verification are pending deployment.
