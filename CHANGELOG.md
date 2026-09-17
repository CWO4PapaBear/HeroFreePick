# Changelog

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
