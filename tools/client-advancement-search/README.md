# PTR advancement UI overlay — 0.2.10-test.1

Original addon source overlay for the cumulative PTR 0.2.9-test.1 client. The root addon/profile packages predate this runtime; do not replace them wholesale or install this overlay on an arbitrary older profile.

Compare each existing file against `manifest.json` before applying `payload` under `Interface/AddOns`. A null before hash means the file must be absent. Preserve personal settings and layout overrides. The launcher release packages this overlay on the verified cumulative baseline; prefer that supported installation path.

Adds learned ability/talent name search and tooltip-text search scoped to Overview, selected class/tree, Summary, rarity and ownership. Adds circular Hybrid class choices with stock class descriptions and removes Hero selected-class glow. No server changes or new Hero enrollment path are included. Poisons Mastery and Warrior stance changes remain unfinished.

Run `python tools/client-advancement-search/test_search.py` with Lupa Lua 5.1 installed. Checks cover Lua syntax and search/filter logic, not in-game layout. The repository's `python build.py` checks the existing default packages; it does not incorporate this newer overlay. Client visual testing remains required.
