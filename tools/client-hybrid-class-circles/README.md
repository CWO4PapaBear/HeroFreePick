# Hybrid second-class circles — local test overlay

Updates the level-10 second-class picker and Settings upgrade picker to use Hero Advancement class portraits and gold rings. Hover text uses stock character-creation class descriptions, preferring localized globals when available. These describe the stock class; they do not change server progression or starting levels.

The installed test client still contained red-button pickers despite the earlier advancement-search source overlay. This two-file repair is based on that installed client, not a wholesale reinstall of older staging. Apply only when both before hashes in manifest.json match; otherwise reconcile against the newer addon. Preserve all other files and saved variables.

Original class exclusion, level-10 checks, confirmation and server authority remain unchanged. No new Hero entry, poison, talent or server changes. Root build.py packages the older base addon and does not incorporate this overlay.

Test with `python tools/client-hybrid-class-circles/test_picker.py` using Lupa Lua 5.1. Offline syntax/tooltips/callback checks pass; in-game visual review pending. Test both entry paths, hover labels, selection/review/back navigation and different original classes. Source publication is not a launcher release.
