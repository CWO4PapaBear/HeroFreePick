# Repository instructions

This is the modular Hero Advancement private repository for CWO4PapaBear/HeroFreePick.

- Never add the external LayoutEditor, its importer, personal layout presets, backups, extracted client archives or extracted third-party server modules.
- Optional original server packages are now authorized. Keep Classic client-only and document uncompiled/unfinished server integrations honestly.
- The owner authorizes normal commits and pushes at completed development milestones. Run relevant tests and build.py, review the diff, and update the changelog first. Do not force-push.
- Preserve Lua 5.1 / Interface 30300 compatibility. Mock tests are not substitutes for in-game visual verification.
- Keep local MenuLayoutOverrides.lua values out of published changes unless explicitly requested.

- Classic remains stock class/trainer progression: exclude custom Masteries, their badges and custom unlock requirements. Apply new free-pick features only to custom modes unless explicitly requested for Classic.

## Talent modifications

For any talent modification, including new talents, mechanics, tooltips, ranks, level gates, costs, prerequisites, or mode availability, read and apply [the talent modification skill](.agents/skills/bear-cave-talent-modification/SKILL.md). Follow the current user request and repository instructions if they differ from the skill.
