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

## 0.27.3 — initial repository candidate

- Character Advancement UI with class and specialization tabs, native talent tree art and dependency routes.
- Available ability points follow the planned level allowance and local selection costs.
- Learned-list search and combined rarity, specialization, class/type and plan filters.
- Compact layout with native effective scale when the display can fit it.
- Fix menu-opening failure caused by a button-only text call after converting the Filter control to a dropdown.

This repository candidate includes the current addon. In-game validation is still required after layout changes. Server-owned cross-class progression and individual native talent refunds are not implemented.
