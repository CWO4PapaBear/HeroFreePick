# Starter spell login reconciliation

Roguetest's export retained Sinister Strike (1752) and Eviscerate (2098) in character_spell while the enrollment snapshot marked both withheld. The selected build no longer includes those starters. The saved-spell loader admits them through the ordinary skill check, bypassing the existing learnSpell gate, and the later build synchronization removes them after the initial client spell list.

The patch checks held starter ownership during saved-spell loading. Confirmed unselected starters follow the existing rejected-row cleanup before the client receives its initial list. Purchased starters remain allowed. Classic, unrelated spells, missing/corrupt ownership data and pending migrations are not rejected by this new check. Existing build validation still applies. No chat-message filters are added.

The export also reported a missing obsolete BuildCatalog.h; current generated catalog reference is available in the preceding equipment baseline. The two modified source files were freshly exported from the active equipment image.

Compiled tests exercise the actual new policy function. Full PTR compilation and in-game validation are pending. Build-Test.py verifies baseline hashes, builds a separate image and restores source; it does not restart or modify the database. Activation will require a restart. No client update is required. During subsequent logins, the normal server cleanup removes obsolete saved starter rows; no bulk database migration is staged.

The GitHub package contains the minimal source patch and test fixture, not exported core or private character records. Apply starter-login.patch only to the matching reviewed PTR source; source-manifest.json identifies the required file hashes.

## Patch notes

Fixed a login path that could reload withheld original-class starter spells and immediately report them as unlearned. Approved purchased spells remain available. Please reconnect twice with a custom-mode character and confirm both the alerts and unwanted starters stay absent, then check that purchased starters and Classic characters remain unaffected.
