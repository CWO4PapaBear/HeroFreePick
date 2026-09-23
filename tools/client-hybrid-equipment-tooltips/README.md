# Hybrid equipment tooltip correction

The stock client colors class requirements using the original class. HeroFreePick now displays a satisfied class requirement in white when the equipment allows the server-confirmed second class. Ordinary hover, chat-linked item and comparison tooltips are supported. Other unmet requirements remain red. Classic and Class+ behavior is unchanged. Hero retains the confirmed pair, matching server equipment policy.

Only exact localized class names in the class restriction line are matched. No item requirements, class identity or server permissions are changed. A new login starts unconfirmed and waits for the server mode response.

Close WoW and run Install-Client.py --wow-closed from WSL. This installs HeroFreePick/HybridEquipmentTooltips.lua and adds it to the reviewed current addon TOC. The installer verifies hashes and keeps backups. No server restart or MPQ change is needed. Launcher publication is separate and has not occurred.

Lua 5.1 regression checks passed for class lists, embedded color codes, unsupported classes, all six native tooltip surfaces, localization and preservation of level/profession warnings. Installer staging/idempotency checks passed. In-game visual acceptance is pending. Third-party custom tooltip renderers need separate testing.

## Patch notes

Hybrid equipment tooltips now recognize both classes: an allowed secondary-class requirement displays in white instead of misleading red text. Unmet level and other requirements remain red. Please test inventory items, chat links and item comparisons.
