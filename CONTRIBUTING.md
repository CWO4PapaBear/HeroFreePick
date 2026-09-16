# Contributing

Use Python 3.10+ and install requirements-dev.txt. Run `python test_ui.py` and `python build.py` before submitting a change. Lua must remain compatible with Lua 5.1 and WoW interface 30300.

Describe the behavior change and in-game checks in pull requests. Mock tests cannot verify frame strata, texture appearance, secure UI behavior or native client API compatibility. Test affected controls in-game, including switching classes, reopening the menu and reloading.

Do not commit client installations, extracted MPQs/DBCs, account SavedVariables, server credentials, personal presets, backups or generated release archives. Keep layout changes separate from talent routing changes where practical.
