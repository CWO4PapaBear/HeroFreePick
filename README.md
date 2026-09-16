# HeroFreePick

Character Advancement interface for World of Warcraft 3.3.5a (Interface 30300). Current version: **0.27.3**.

Browse abilities from ten class families, inspect native talent trees, plan ability selections.

## Features

- Class icons, specialization tabs, a learned-selection Summary, and native talent-tree artwork and dependency routes.
- Planned ability allowance: nine points at levels 1–9, then one additional point per level from level 10. Local selection costs reduce the available pool.
- Search and combined rarity, specialization, plan, and class/type filters for learned entries.
- Compact menu targeting effective scale 1 when the display can accommodate it.

## Current boundaries

This is a prototype, not a complete server-authoritative classless progression system. Ordinary-class talent learning uses the existing client/server talent API where supported. Cross-class abilities, primary-stat effects and local selection budgets do not implement server progression. Individual native talent refunds without a trainer are not implemented. Archetype Builder is disabled. The audit-only server foundation is excluded and is not required; see [server dependency review](docs/SERVER_DEPENDENCY.md).

## Install

Download a built addon ZIP and extract its `HeroFreePick` folder into your client's `Interface/AddOns`. Restart the client, enable the addon and run `/heropick`. The addon also supplies an optional N-key binding and menu integration.

For a source checkout, use Python 3.10+:

```sh
python build.py
python install.py --client "PATH/TO/WOW-CLIENT"
```

The selected client directory must contain `Wow.exe`. The installer verifies checksums and backs up an existing addon before replacement. It does not modify server files or SavedVariables. Updates that add Lua files require a full client restart; other updates can use `/reload`.

## Development

```sh
python -m pip install -r requirements-dev.txt
python test_ui.py
python build.py
```

Tests exercise Lua 5.1 loading, mock UI startup, all 30 talent trees and 122 dependencies, local point accounting, combined learned filters and geometry calculations. They do not emulate the game's rendering engine. CI builds an addon ZIP after validation.

## Repository status

Private repository: `CWO4PapaBear/HeroFreePick`. See `docs/PUBLICATION.md` for the remaining release decisions. No license has been selected yet.
