# Repository instructions

This is the addon-only private repository for CWO4PapaBear/HeroFreePick.

- Never add the external LayoutEditor, its importer, personal layout presets, backups, extracted client archives or server module.
- The owner authorizes normal commits and pushes at completed development milestones. Run relevant tests and build.py, review the diff, and update the changelog first. Do not force-push.
- Preserve Lua 5.1 / Interface 30300 compatibility. Mock tests are not substitutes for in-game visual verification.
- Keep local MenuLayoutOverrides.lua values out of published changes unless explicitly requested.
