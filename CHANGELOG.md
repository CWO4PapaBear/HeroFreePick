## Staged light-blue tooltip values

Resolved numbers and percentages now use light blue in Hero Advancement. Yellow warnings remain distinct; Shift details and paragraph spacing are preserved. Client visual review and launcher publication pending.

## Staged server spell tooltip resolution

Audited 2,955 descriptions; resolved 110 of 175 affected spell/rank descriptions from exported PTR fields and supported formulas. Serpent Sting displays its 15-second total using current ranged attack power. The remaining 65 descriptions stay yellow. Existing implementation warnings and Classic behavior are preserved. Client-only installer and renderer checks passed; in-game review and launcher publication pending.

## Staged tooltip cleanup

Hero Advancement now keeps IDs, Mastery inclusion and click controls in tap-Shift details. Removed stale blanket commit-unavailable text and internal browse provenance; genuine implementation warnings remain. Tooltip sentences have paragraph spacing. Lua 5.1 and renderer checks pass; in-game visual review and launcher publication pending.

## Development - tap Shift tooltip details

- Hero Advancement expanded tooltips now toggle on a Shift press rather than requiring the key to remain held. Applies to ability/talent, Mastery and Primary Stat views; updated hints say Tap SHIFT. Other interfaces keep their normal Shift behavior.
- Lua 5.1 regression checks pass. Client installer staged; in-game acceptance and launcher publication pending.

## Development - portrait menu and drag follow-up

- Correct primary pet/player secure menu setup to the native 3.3.5 menu action. Add player portrait/resource drag surfaces and target/focus bar dragging with per-character lock and position persistence.
- Client-only patch staged and regression checked. In-game verification and launcher promotion pending.

## Development - shared weapon proficiency

- Display Dual Wield (674) under General in the Hybrid/Hero spellbook, regardless of its Warrior catalogue assignment. It no longer creates a Warrior tree tab by itself. No learned spells or server records change.

## Development - spellbook refresh isolation

- Use dedicated tree-tab buttons inside the normal spellbook so stock refreshes cannot replace their icons and tab identities. Reconcile visible controls after refreshes and retain the selected tree/page.
- Always show the tree-page counter in custom mode. Add /hfspellbook for concise runtime mode, tab and spell counts when diagnosing client behavior.
- Regression checks now simulate repeated native refreshes and delayed stock tab repainting. In-game confirmation pending.

## Development - PTR portrait repair

- Restore portrait control loading, saved player/target locks and positions, pet right-click menus, narrower resource bars and stock DK rune hiding. Preserve pet happiness and keep spellbook changes separate.
- Reviewed client-only overlay includes hash guards, backups and rollback on installation failure. Lua 5.1 and installer regression checks pass; in-game visuals and launcher publication pending.

## Development - expanded spellbook tree pages

- Keep individual learned class/tree tabs in Hybrid and Hero, including builds with more than eight tabs. Add Previous/Next controls and a tree-page count, preserving native spell slots for casting, dragging and tooltips.
- Preserve page navigation during spell refreshes; clamp pages when a build loses trees. Classic and pet spellbooks keep native behavior.
- Lua 5.1 regression test covers all 30 trees plus General across four pages. In-game visual testing and launcher publication remain pending.

## Development - client Spell.dbc staging

- Add append-only client Spell.dbc staging for 266 filtered definitions, preserving baseline records and UTF-8 localized strings. Prepared an isolated test installation package; live SQL and startup validation run during deployment.

## Development - isolated icon and visual assets

- Resolve and package 83 icons and 837 visual support assets; add isolated icon/visual DBC staging with cloned dependent IDs and rewritten asset paths. Preserve existing client records.
- Record explicit cosmetic repairs for missing Elemental Blast, Arcing Light and sound references. Offline validation passed; client rendering and gameplay remain untested.

## Development - auxiliary spell references

- Add append-only staging tool for three missing SpellRange records and one SpellRadius record, preserving destination rows and rebuilding localized string offsets.
- Preserve source candidates for all 79 missing visual IDs and 83 missing icon IDs; nested visual assets remain under review. No deployment or gameplay changes.

## Development - filtered spell candidates

- Add conservative dependency-aware selection: retain 156 roots and 110 reference dependencies; hold 23 roots affected by unsupported enums or references. Auxiliary DBC validation remains required before deployment.

## Development - optional spell definition reference

- Package 179 missing Area 52 spell roots (excluding 901018) and 141 non-stock reference dependencies with localized text, source hashes, support-table rows and icon references.
- Add offline typed spell_dbc conversion, explicit effect-mask mapping, collision/schema checks, receipt-based rollback candidates and lossless aura-text schema expansion.
- Block raw SQL installation for unsupported core enum values; preserve all source records for later module effect adaptation. No server deployment or Classic addon changes.

## Development audit — server coverage

- Inventory all 1,665 current entries, four primary-stat choices and 29 staged talent records against stock/Area 52 spell data and recorded server routes. Distinguish aliases, supported purchases, changed effects and missing systems. No gameplay or deployment changes. Live database verification remains pending because WSL access is denied.

## 0.41.1

- Fix Class+ talent clicks: resolve talent-tree ability aliases before the purchase allowlist and permit passive talent drafts while preserving level/TP limits. Server application of passive talents remains unsupported and now reports the affected talent explicitly.

## 0.41.0

- Add reproducible Area 52 talent importer, rank-level tooltip comparisons and packaged icons. Preserve existing native identities, routes, costs and prerequisite color logic; Classic keeps stock tooltips.
- Highlight changed wording yellow until the exact reference revision is explicitly confirmed implemented. Unresolved formula values remain visibly pending.
- Stage 29 unmatched source records (27 distinct class/name pairs) separately for future tree/server integration; export complete effect and dependency references without applying server changes.

## 0.40.3

- Add optional persistent Class+ enrollment runtime and matching bridges without character-name restrictions. Preserve existing enrolled builds, keep unenrolled characters Classic, validate account/class identity independently of names, and clean up ownership records on deletion. Full core build and live verification pending deployment.

## 0.40.2

- Show and enable the Hero Advancement micro-menu button from level 1 in Class+, Hybrid, and Hero. Hook the actual 3.3.5 talent-button refresh and restore neighboring button spacing; Classic retains stock visibility.

## 0.40.1

- Display custom-mode class trainer guidance in the standard NPC gossip window with portrait, NPC name, parchment, Goodbye, and native-style dialogue options. Preserve server purchase blocking and reset confirmation.

# 0.40.0

- Add 65 missing Ascension class abilities as custom-mode planning entries, with source levels, AP/rarity costs, descriptions and packaged icons. Keep Classic and established progression/Mastery overrides intact.
- Add missing-client description/icon fallbacks for 11 existing custom entries; preserve dynamic scaling as readable formulas in offline previews.
- Add class-trainer guidance with the current Hero Advancement key binding and a native talent-reset confirmation action.
- Add authoritative trainer-state blocking for server-published custom modes. The staged Class+ test connects persisted mode to the gate; Hybrid/Hero production persistence integration remains required. Profession/riding trainers remain available.
- New Ascension abilities are previews until server spell implementation; the supported server purchase catalog is unchanged. Native trainer resets use the existing server price; remote custom-build resets remain unimplemented.

# 0.39.10

- Add Hunter Auto Shot as a level 1, 2 AP custom-mode choice using native spell 75; retain the Classic creation-grant entry.
- Audit stock starting abilities and extracted Ascension level-one paid choices; preserve paid Mastery membership and the approved DK progression.

## Unreleased â€” Class+ server inventory

- Make ability unlocks through level 10 available at level 1 in Class+ and Hybrid, including DK and free group members; Masteries follow their earliest member. Preserve Classic/Hero, passive talent tiers, higher unlocks and later-rank schedules.
- Unify 151 talent-origin choices as AP purchases across both menu locations; set all 30 capstones to level 60 and one Legendary gem. Apply stock non-DK Class+/Hybrid unlocks and rank references, preserve DK level-one progression, and derive each Mastery unlock from its earliest member. Preserve Classic.
- Add level-20 Runeforging Mastery and ten free rune enchants; expand rarity budgets to 11 Uncommon / 16 Rare / 13 Epic / 7 Legendary. Rarity bars filter on left-click and clear on right-click.
- Block ability additions that exceed a rarity budget immediately in either draft, using the shared alert. Change custom Death Grip from Epic to Legendary; retain existing budgets pending the level-80 budget decision.
- Set custom Dark Command to level 65 and promoted Corpse Explosion to level 20; preserve Classic talent prerequisites and existing resource costs.
- Set custom Presence Mastery to level 1 by explicit design choice; its free Blood/Frost/Unholy grants remain level 1/10/28.
- Apply 48 Death Knight custom ability unlock levels from the shared patch-M/Dawnrise candidate reference. Preserve Classic trainer/starting levels, native talents, costs and stock rank chains; unresolved level-71 entries remain explicit exceptions.
- Audit all custom-mode ability level boundaries across both drafts (3,042 cases); enforce controller/member levels for automatic Mastery and bundle grants (142 members). Remove stale ineligible automatic grants.
- Reject below-level ability selections immediately in both drafts using the raid-warning alert, with the ability name and required level. Name the blocking ability in final validation too.
- Update the shared pending-change confirmation to warn that changing talents after confirmation costs Gold; fit the message on two lines.
- Prompt new Class+, Hybrid and Hero selections with a screen-wide raid warning to open Hero Advancement and choose initial abilities. Respect muted alert sounds and avoid reminders on ordinary mode synchronization.
- Reject ability additions immediately when the active draft lacks enough Ability Points, using the existing alert. Applies to both advancement and Archetype drafts.
- Custom-mode learned lists retain Mastery and bundle headings, with their active member abilities nested beneath them. Ordinary passive rows remain hidden; Classic filtering is unchanged.
- Audit the effective Class+ catalog across all classes and both factions against the saved stock 3.3.5 Spell.dbc. Record 66 missing IDs, 120 stock/reference name-review flags and one catalog-only placeholder.
- Separate entitlement wrappers, More Minions dependencies, travel references and Class+ mechanics. No spell definitions, server data or gameplay behavior changed.

## 0.39.9

- Move level-one Pick Again out of Settings into a matching 22px title-bar box to the left of the gear. Use the verified native red pass/prohibition icon at 16px and explain mode reselection on hover.

## 0.39.8

- Add Change Mode to Settings for level-1 characters only. Reopen initial progression choices without clearing the existing choice; retain installed-mode and pending-change validation.
- Give the progression popup the main interface opaque stone background.

## 0.39.7

- Classic-only new-character selection now shows disabled Class+, Hero and Hybrid (Level 10) buttons with an optional-module update note. Classic stays selectable; installed custom-mode flows are unchanged.

## 0.39.6

- Show GitHub URL and installed addon version in the information tooltip. Clicking information opens a selectable URL for copying to a browser.
- No automatic update checker is included; stock 3.3.5 addons cannot query GitHub directly.

## 0.39.5

- Extend the main header bar to the right edge behind the compact settings, information and close controls. Keep title text clear of the controls.

## 0.39.4

- Remove the redundant Close for now button from pending confirmation. Retain the X action and reduce popup height to 84, with 14 pixels below the remaining button row.

## 0.39.3

- Separate compact close/info boxes from the title bar and add a matching gear button with a Settings menu.
- Add a per-character Alert sounds preference, enabled by default. It controls point/prerequisite warnings and pending-confirmation raid warnings for all character types, independently of pending build edits.

## 0.39.2

- Move pending-confirmation buttons directly beneath the heading and reduce popup height from 140 to 112. Keep the secondary close button inside the stone border.

## 0.39.1

- Simplify the pending-close confirmation for every character type to the header "You have unapplied changes." and its existing buttons. Use the main interface's opaque stone texture, a red border and a compact height. Play RaidWarning once when the confirmation opens.
- Preserve all accept/back/cancel/close behavior. Failed commits still report through the existing warning alert instead of adding text to the confirmation.

## 0.39.0

- Split Teleport Mastery from Portal Mastery, with independent purchases/grants and Teleport: Dalaran artwork. Add neutral teleport previews alongside existing neutral portals; preserve Classic and faction/race level rules.
- Record all 160 eligible Rune destinations (excluding Acherus), zone-based levels, exact faction/arrival restrictions and separate Mage ownership in a machine-readable integration specification.
- Specify no reagent consumption and one corresponding reagent generated after successful caster travel. Server spell definitions, reward handling and the custom build commit bridge remain unimplemented; no server behavior is changed by this release.

## 0.38.1

- Tracking Mastery starts at level 1. Portal Mastery starts at 10 and grants racial capital spells at 10, faction capitals at 15, Ratchet/Booty Bay Retreat portals at 25, faction Shattrath spells at 62, and Dalaran at 72.
- Reuse saved Runes of Retreat portal IDs 903090/903018; these still require the existing travel package and server authorization. Remove unscheduled Theramore/Stonard custom members; Classic is unchanged.
- Reconcile portal grants by race/faction/level, removing previously premature preview grants.

## 0.38.0

- Import Tracking Mastery (Hunter level 10, six members) and Portal Mastery (Mage level 20, 26 stock prerequisite-linked spells). Each costs 2 AP and one Uncommon gem; members follow custom automatic level-based grants with zero additional costs. Classic remains separate.
- Exclude Portal: Azzar Faire by request; classify both imported Masteries as passive for Learned Abilities filtering. Imported A52 portal member levels are 1, so our grant policy unlocks them with level-20 Portal Mastery.

## 0.37.3

- Grey learned abilities in the left ability menu using the same ownership list as Learned Abilities (Classic spellbook/custom selections). Preserve hover tooltips and pending-edit interactions.

## 0.37.2

- Disable apply and pending-reset controls without relevant changes. Gate each reset category independently and reject stale reset/apply callbacks.

## 0.37.1

- Fix startup failure by naming all footer MENU dropdown frames as required by the 3.3.5 UI. Extend the UI mock to reject unnamed MENU dropdowns and verify Toggle initializes.

## 0.37.0

- Compact AP/TP boxes around measured text with two-digit capacity; retain the TP right edge. Add Apply Pending, Reset Pending, and disabled Reset Learned controls between them.
- Pending resets restore only the chosen category from its preparation baseline. Classic only permits pending talent apply/reset.
- Learned resets remain disabled pending server integration: applied talent reset quotes and charges must use the authoritative trainer price.

## 0.36.6

- Default the rarity panel to hidden for Classic characters, preserving explicit saved toggle preferences and custom-mode defaults.

## 0.36.5

- Place the stock bronze lock icon directly below the talent panelâ€™s level-10 lock message.

## 0.36.4

- Hide passive spells and talents from Learned Abilities in every mode, including passive grouping parents. Keep ownership, planning and resource accounting intact.

## 0.36.3

- Correct Classic Rogue Dual Wield to level 1 and character-creation source. Audit shared starting skills as well as class-named skills; retain Warrior/Hunter level-20 trainer progression.

## 0.36.2

- Identify 28 starting class ability groups across all ten classes, add three missing entries, and display character-creation sources. Preserve stock Death Knight starting level 55. Exclude Classic supplements from Mastery membership.

- Restore 89 missing Classic class ability groups using stock class trainer and quest teaching records, including level-10 Tame Beast and its pet-management abilities. Keep supplements out of custom modes.
- Use plain Level headings; retain acquisition sources in tooltips.

## 0.36.1

- Add the missing Classic Hunter Track Beasts catalog entry (spell 1494, trainer level 2), allowing it to appear in the ability menu and match learned spellbook entries. Keep the supplement out of custom-mode catalogs.

## 0.36.0

- Use Spell_Holy_PowerInfusion for the Primary Stat Spirit icon.

- Show Classic ability headings and tooltip levels from the stock AzerothCore trainer reference (369 catalog matches); group unmatched entries under Other learning sources. Custom level data remains unchanged.
- Allow Classic to browse other classes from the top menu without granting cross-class learning or changing the own-class spellbook list.

## 0.35.5

- Limit Classic spellbook-derived learned entries to the character's class catalog. Exclude unmatched general, racial and profession spells; retain native-name matching for class spell ranks.

## 0.35.4

- Populate Classic learned abilities from the player spellbook, refreshing on spell-learning events. Deduplicate catalog rank groups and include uncatalogued spellbook skills.
- Display actual learned spell tooltips without free-pick costs; keep pending talents separate and custom-mode ownership unchanged.

## 0.35.3

- Reject Classic talent additions immediately when tier investment or dependency ranks are missing, using the existing points warning alert and the selected plan state. Custom level gates retain the same alert behavior.

## 0.35.2

- Add 2px of vertical padding above and below learned-row content so borders wrap around icons instead of touching them.

## 0.35.1

- Color talent prerequisites red when unmet and green when met. Classic tree investment/dependencies use pending ranks, including drafts; custom talents use their tier level. Refresh hovered talent tooltips as selections change.

## 0.35.0

- Automatically include Mastery members at their required character levels in both preparation and archetype plans. Synchronize on selection, level-up and login; preserve cancel baselines and prevent independent member removal.
- Keep Classic unchanged. These are local preview grants; custom server learning remains unavailable.

## 0.34.4

- Hide the parent badge on indented learned child rows so it cannot cover their smaller individual ability icons. Keep parent badges in other views and preserve child tooltips.

## 0.34.3

- Keep learned child text/costs at full scale; shrink only icons and tighten row height (16px minimum to fit full-size cost symbols). Preserve indentation and aligned endpoints.
- Combine gems then AP/TP in one horizontal cost label. Add original A52 Talent Essence artwork for Talent Points in learned rows, talent tooltips and the available-points display.

## 0.34.2

- Correct learned icon size to 75% of 34px (25.5px), with child icons at half that size (12.75px). Preserve indentation and aligned bar endpoints.

## 0.34.1

- Size learned icons to 76% of the standard 34px ability icon (25.84px); child icons remain half-size (12.92px).
- Preserve the 18px child indent and extend child row backgrounds to the parent right edge; adapt text and costs to row width.

## 0.34.0

- Use selected A52 backflip icon for primary Agility.
- Tighten primary-stat title/icons, lift search/filter controls and expand the learned viewport upward; reduce gap before the next ability level header.
- Group learned Mastery/companion abilities under their controlling entry; indent and scale child rows/icons to 50%, preserving hover and click scripts. Keep parent context when filters match a child.
- Learned normal icons remain 38px versus 34px in the ability grid; grouped child icons are 19px.

## 0.33.3

- Use Spell_Arcane_MindMastery for the Intellect primary-stat icon.

## 0.33.2

- Use the native flexing-arm Spell_Nature_Strength icon for Strength in Choose Primary Stat.

## 0.33.1

- Remove the A52 attribution prefix from displayed group descriptions, retaining the description text.

## 0.33.0

- Add the A52 Tether Elemental bundle and its five companion skills, preserving level 1 / 4 AP / 2 Epic configuration. Bundle the missing Elemental Lore texture.
- Show recovered A52 descriptions for imported companion and Demon Mastery summoning abilities in normal and expanded preview tooltips. Mark unresolved spell values explicitly.
- Review Wild Imps: found temporary Hand of Gul'dan summons and vanity/passive records, not a corresponding taming bundle; no invented package added.

## 0.32.4

- Restrict connected-ability expansion to primary Mastery/bundle tooltips and their parent badges. Individual child spells retain normal tooltips even while Shift is held.

## 0.32.3

- Swap Dragonkin Lore/Dismiss icons; expand connected groups from same-named tame actions and Shift-hovered bundle children.
- Tighten ability level-header spacing from 24 to 17 UI units.
- Review Summoner's Armor and all 23 imported Mastery descriptions against local rules.
- Verify Classic Accept through the actual popup callback and frame poller with sequential mocked native acknowledgments and timeout handling; live verification remains required.

## 0.32.2

- Bundle the 12 missing A52 textures inside the addon and map affected abilities and companion tooltip icons to explicit artwork.
- Give companion child abilities individual spell icons instead of inherited parent fallbacks. Classic artwork is unchanged; no server changes.
- Verify BLP decoding, asset hashes and entry/tooltip routing; retain asset source metadata.

## 0.32.1

- Add Summon Imp to Demon Mastery and make Demon Mastery available at level 1; retain its 2 AP and existing gem cost.
- Audit recent companion/Mastery icon paths against the test client and document missing A52 assets without substituting artwork.

## 0.32.0

- Integrate all four companion bundles as custom-mode preview purchases with 4 AP / 2 Epic cost and automatic level-one child grants.
- Add bundle lists, skill previews, parent badges, reversible bundle removal and duplicate native-entry replacement. Classic excludes bundle content.
- Test all bundles, resource accounting, cancellation and mode boundaries; document Hunter tests and the future standalone Companion Training module. Server learning and pet support remain unimplemented.

## 0.31.5

- Add small bottom-right Mastery badges to member ability icons across ability, learned, summary and browse views. Hover opens the interactive Mastery tooltip.
- Explicitly hide badges in Classic and clear badges when pooled buttons are reused.

## 0.31.4

- Sort connected Mastery abilities by required level, then name; unknown levels appear last. Verify ordering and membership for all Masteries.

## 0.31.3

- All Mastery tooltips explain level-based access and zero additional member resource costs.
- Hold Shift to reveal all linked ability icons, names and required levels; hover icons for a separate spell preview with a missing-client-data fallback.
- Test membership coverage, live Shift expansion/collapse, preview lifecycle and dismissal for every Mastery. In-game visual verification remains pending.

## 0.31.2

- Keep modal shields below their panels and progression buttons using bounded frame levels. Explicitly enable reused progression buttons.
- Exercise initial Classic selection through the popup button in the Lua harness; live client verification remains required.

# Changelog

- Classic tooltips include verified stock trainer/quest sources, including learned spellbook entries. Fixed a syntax error in the cross-class browsing gate.

## 0.31.1 - unblock review popups

- Attach the missing Classic commit poller and completion callback so confirmation/timeout restores popup controls.
- Add Close for now and close buttons that retain pending changes and hide both modal overlays.
- Unresolved progression choices reappear when reopening the menu.

## 0.31.0 - independent progression profiles

- Add client-only Classic, optional Class+, Hybrid and Hero preview packages.
- Prompt for level-1 progression and the Class+ level-10 Hybrid/continue decision; explain Hybrid in the Class+ tooltip.
- Use native Classic talent tooltips/commit acknowledgments and level-only custom talent tiers/tooltips.
- Add independent server policy source packages; custom-mode learning/refunds and server-owned choices remain unimplemented.
- Generate separate release archives and a complete development bundle. See docs/MODULES.md for status and installation.

## 0.30.2 - pending talent point budget

- Show remaining/total Talent Points for the active preparation view, using one point per level starting at 10.
- Reject allocations beyond that budget with the existing point-warning alert; removing ranks returns points.
- Apply the same limit independently to Hero Advancement and Archetype drafts.

## 0.30.1 - cached file-list compatibility

- Embed preparation and review code in existing addon files so an older cached TOC cannot leave BeginPreparation or RequestClose undefined.
- Retain harmless compatibility placeholders for the two newly introduced files.
- Test the complete workflow while omitting those two files from the loader.

## 0.30.0 - pending advancement review

- Replace immediate native talent learning with reversible pending ranks; left-click adds and right-click removes.
- Add close review with before/after resource totals and Accept Changes, Go Back, and Cancel Changes.
- Accept remains blocked until server committing is implemented; pending changes persist across reloads.
- Permit resource-over-budget preparation; removing a Mastery removes its pending members.
- Full client restart required for two new Lua files. See docs/PENDING_CHANGES.md.

## 0.29.1 - Hero Advancement labels

- Rename the menu header, micro-menu tooltip, Escape-menu entry and binding labels to Hero Advancement.
- Render (N) in yellow in the micro-menu tooltip.

## 0.29.0 - mastery prerequisites and costs

- Add 23 Masteries as abilities costing 2 AP, preserving raw Area 52 rarity and gem costs.
- Import nine missing member abilities; all mastery members cost zero AP/gems and require their Mastery in the same learned/draft state.
- Block mastery removal until member selections are removed; back up and clear prior orphan member selections on load.
- Enable local selection for talent-origin ability copies that belong to a Mastery; native talent trees remain unchanged.
- Sentry Totem lacks an advancement record in this export; its explicit membership is imported with the Air Totem Mastery level as a documented fallback.
- Full client restart required for the new Lua file. Server learning remains unavailable.

## 0.28.0 - talent-origin ability references

- Add 144 Area 52 talent-origin abilities to the ability pane and Browse, with recorded Ability Essence and rarity costs.
- Keep these entries read-only while retaining all 829 native talent nodes and existing learning behavior.
- Document alternate Area 52 cost records and category fallbacks in docs/TALENT_ABILITY_REVIEW.md.
- Require a full client restart after installation to load the new catalog file.

## 0.27.3 â€” initial repository candidate

- Character Advancement UI with class and specialization tabs, native talent tree art and dependency routes.
- Available ability points follow the planned level allowance and local selection costs.
- Learned-list search and combined rarity, specialization, class/type and plan filters.
- Compact layout with native effective scale when the display can fit it.
- Fix menu-opening failure caused by a button-only text call after converting the Filter control to a dropdown.

This repository candidate includes the current addon. In-game validation is still required after layout changes. Server-owned cross-class progression and individual native talent refunds are not implemented.
