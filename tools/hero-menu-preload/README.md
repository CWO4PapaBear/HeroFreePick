# Background menu asset preload

Apply HeroFreePick.lua only against the before SHA256 in manifest.json (activated Hero entry client). Preload.lua is the embedded implementation; no new TOC entry is needed. Starts half a second after PLAYER_ENTERING_WORLD, warms all 30 talent backgrounds and catalog icon variants, deduplicates and retains texture references, and pauses in combat/loading screens. At most two work units per frame, with a soft 1 ms budget between units. Individual native texture loads cannot be interrupted; the budget is not a hard frame-time guarantee. Completion removes the update handler. No menu rendering, mode changes, purchases or pending-state changes occur.

Lua 5.1 mocked tests pass: run `python Test.py` with lupa installed. Local client installed with backup; real-client first-visit timing remains unverified. If delay remains, profile the class refresh path before adding broader preload work. Server unchanged; launcher release pending. Background cache is per session, not SavedVariables.

Local dependency repair: include AdvancementSearch.lua and ensure the TOC loads it before HeroFreePick.lua. The local client had the new search UI but an older TOC and missing implementation. Both are now repaired; installed-client search filter checks pass. Preserve existing TOC entries when updating a different baseline.
