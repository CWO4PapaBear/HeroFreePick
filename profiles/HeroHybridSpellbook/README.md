# Expanded spellbook tabs

Install this folder as Interface/AddOns/HeroHybridSpellbook with WoW closed. Enable Hero Hybrid Spellbook. Requires HeroFreePick and HeroClassPlusCommitTest.

Hybrid and Hero keep individual learned class/tree tabs. More than eight tabs use Previous/Next buttons beneath the tab column and a Trees page counter. General counts as a tab. Native spell slots are preserved for casting, dragging and tooltips. Classic and the pet book are unchanged.

Run tools/test_spellbook_paging.py with Python and lupa (Lua 5.1). Regression tests cover 31 tabs across four pages, page persistence, shrinking builds, and native fallbacks. In-game visual validation is pending. This addon does not grant abilities or change server records.

Launcher publication is separate from source publication.
