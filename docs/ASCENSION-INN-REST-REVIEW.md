# Ascension inn-rest XP buff review

Confirmed in the local Area 52 Spell.dbc:

| Spell | Name | Evidence |
|---|---|---|
| 997614 | Rested Experience | Periodic trigger aura 23, interval 900,000 ms (15 minutes), triggers 997615. |
| 997615 | Resting | Duration index 347 = 900,000 ms (15 minutes). Tooltip says completion inside the inn grants the monster-kill XP buff. Dummy aura 4; no direct reward trigger encoded here. |
| 997616 | Well Rested | Duration index 367 = 7,200,000 ms (2 hours). Aura 200 (MOD_XP_PCT), base points 7 plus die sides 1 = 8%; misc value 1. Tooltip explicitly limits it to monster kills. |

SpellDuration.dbc entries agree in Ascension locale-enUS.MPQ and patch-enUS-3.MPQ. Separate spell 93206 is a different Well Rested entry; do not confuse it with this three-spell system.

GitHub reference fetched and checked: jealous-sound/azerothcore-wotlk-coa main, revision 47dd22ffe6d0a82e6886487f38acff7c5cfeb117. No matching spell-ID or named inn-timer implementation found in the searched source/modules/docs. Player.cpp contains ordinary rested-XP accounting. AscensionCompat.cpp has XP-aura compatibility handling, but not this timer/reward chain. The repository is an independent reconstruction, not Ascension's official backend.

The client data establishes the intended 15-minute Resting buff and 2-hour, 8% monster-kill reward. It does not prove how the server attaches the initial helper, handles leaving/re-entering an inn, offline time, death, refreshes or stacking. In particular, the periodic helper interval is not evidence to add a second mandatory 15-minute wait. Those lifecycle rules would need explicit implementation or further server evidence.

Read-only research only. No PTR, client, or launcher changes for this feature.
