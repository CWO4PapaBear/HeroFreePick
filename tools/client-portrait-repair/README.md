# PTR portrait repair

Reviewed overlay for the current PTR client, not a replacement for the older complete profile in this source repository. Close WoW, then run Install-Client.py --wow-closed. Use --client PATH for a different WoW folder. Hash guards reject unrelated client versions; backups are retained beside the installer.

Restores the portrait-controls load entry and per-character saved settings, hides leftover stock Death Knight runes while using the custom frame, shortens resource bars by 20 pixels, and starts the player frame near the top-left corner. Right-click player/target for lock controls; drag the player name header or target frame while unlocked and out of combat. Existing saved positions are retained.

Primary pet uses the native pet menu. Secondary companion uses a matching dropdown with its own attack, follow, stay, stance and dismiss commands. Pet happiness remains available.

No server, SQL, MPQ, or spellbook changes. Source publication does not publish a launcher update. In-game visual testing remains required.

Validation: Test-Repair.py uses lupa.lua51 and tests delayed mode setup, pet menu routing, movement locks, combat checks, scaled saved positions, installation, idempotence and drift rejection. Test directories are retained locally for inspection.
