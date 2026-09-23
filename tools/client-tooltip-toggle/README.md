# Hero Advancement tooltip toggle

HeroFreePick owns the shared TooltipToggle.lua state. Tap either Shift key while Hero Advancement is visible to toggle expanded ability/talent/Mastery and Primary Stat tooltips. Releasing Shift does not collapse them. The state persists across hovered entries and menu reopening for the current UI session; it starts collapsed after login/reload. Other addons and physical Shift APIs are unchanged.

Close WoW and run Install-Client.py --wow-closed. Optional --client PATH selects the client root. The guarded installer preserves portrait and spellbook files and backs up the affected files. No server or MPQ changes. In-game acceptance and launcher publication pending.

Test-Toggle.py uses Lua 5.1 through lupa to check repeated key events, both Shift keys, closed-menu behavior and syntax of the integrated tooltip renderers.
