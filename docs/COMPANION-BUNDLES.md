# Companion Bundles: interface testing and standalone module plan

## Current release: 0.32.0

Interface integration is complete for Tame Beast, Tame Dragonkin, Enslave Demon and Dominate Undead. Each package costs 4 Ability Points and 2 Epic gems. Its included skills are staged together at no additional cost. All package skills use level 1 as this implementation's explicit design rule, not a claim that every child spell's original Ascension level was recovered.

The parent has a Shift-expanded list with icons and separate ability previews. Child icons have a small parent badge. Clicking a child directs the player to add/remove the bundle rather than purchasing or refunding a component independently. Cancel Changes restores the previous local state. Selecting a bundle replaces matching independently planned native entries in that custom-mode plan; cancellation restores them. No native spell learning, taming or pet deletion occurs.

Classic excludes these packages. Class+ uses the source class; Hybrid uses its two chosen classes; Hero can use all four. Existing generic custom-mode pending budget behavior is unchanged. Server acceptance for custom modes remains unavailable.

## Hunter test

1. Install 0.32.0 and /reload. Use a Hunter in Class+ to test Tame Beast, or Hero to test every package. Classic deliberately does not show the custom bundles.
2. In Hunter abilities, find the level-1 Tame Beast purchase. Hold Shift over it: six included skills should appear (Tame Beast, Call Pet, Dismiss Pet, Feed Pet, Revive Pet, Beast Lore).
3. Add the package once: the local point total should increase by 4 and Epic usage by 2. All six skills should appear in the pending learned list with no additional cost.
4. Hover a child's bottom-right badge: it should show the parent package. Hold Shift and hover a listed icon to preview that skill. Missing custom client spells use catalog names/icons and an unavailable-description notice.
5. Remove the package: its six pending skills disappear and the package resources are refunded. Cancel Changes should restore the pre-edit plan.
6. Repeat in Hero for the five-skill Dragonkin, Demon and Undead packages. Buying multiple packages does not promise multiple active pets.
7. Confirm Classic has no custom packages or badges and still follows normal trainer/talent behavior.

This test verifies preparation UI only. It does not learn skills on the server, enable level-1 taming or prove pet persistence. No new server module has been deployed.

## Future standalone module

Working name: Companion Training.

Proposed description: Adds the ability to learn Beast Taming and Demon companion summoning at level 1, and introduces tameable Dragonkin, Demon and Undead companions.

Here, Demon companion summoning means recalling an enslaved Demon through this package. Ordinary Warlock Imp/Voidwalker/etc. progression is a separate feature and is not changed by this implementation.

Package boundaries:
- An independent server component owns purchases/grants, allowed creature entries, taming, saving, recall, dismissal, revival and safe removal of access.
- A standalone client component supplies the bundle catalog and companion presentation. Hero Advancement consumes the same definitions through a small integration adapter. Avoid requiring any progression mode addon for the standalone distribution.
- Optional compatible client spell/art data is versioned separately. Resolve ID collisions deliberately; do not ship extracted client archives wholesale.
- Default compatibility preserves Classic. Enabling early companion training outside Hero Advancement is an explicit standalone server configuration, not an accidental change to Classic mode.

Before release: validate one complete Beast lifecycle on Hunter and non-Hunter, then one allowlisted creature per new type; confirm costs, interrupted casts, existing-pet conflicts, logout/restart persistence, death/revive, dismiss/recall, stable behavior and removal/reacquisition. Determine whether the exact server revision exposes enough hooks to avoid core patches. The present server code has no authoritative companion transaction or pet implementation yet.
