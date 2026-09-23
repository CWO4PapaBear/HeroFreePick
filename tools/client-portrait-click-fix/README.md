# Portrait click and drag follow-up

Staged client-only follow-up to PTR 0.2.1-test.1. In-game verification pending; not yet in the launcher release.

The 3.3.5 client SecureUnitButton_OnLoad uses the menu action, not togglemenu. Initialize custom player and primary pet buttons with the stock helper so right-click reaches the native pet menu. Normal pet eligibility controls which options are shown.

Player can be dragged from its portrait/name/resource bars while unlocked. Target and Focus each have right-click lock/unlock options, root and resource-bar dragging, combat protection and separate per-character saved positions. Classic is unchanged. Pet frames keep their own click actions.

Close WoW and run Install-Client.py --wow-closed. Use --client PATH for another client folder. Hash guards and backups are included. No MPQ, server or spellbook changes. Test with the game directly until promoted; the older launcher release can restore its published files.
