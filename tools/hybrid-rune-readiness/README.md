# Hybrid rune readiness candidate

Status: local compiled regression checks passed; full PTR build, activation and in-game verification pending. This is a proposed synchronization repair, not a confirmed root-cause finding.

Reported behavior: a Hybrid with DK access can spend runes initially. Natural recovery appears complete in the custom portrait, but casts fail with insufficient runes. Explicit rune-restoration abilities make them usable again.

The inspected server regenerates runes for custom DK access through its existing class-context hook. Natural recovery updates cooldown state without sending a readiness packet; the portrait separately estimates time from HF_RESOURCE snapshots. A non-native DK client may fail to advance its native rune state. The patch sends the existing SMSG_ADD_RUNE_POWER notification only when an authoritative cooldown transitions from positive to zero for a non-native DK with custom rune access. It neither grants extra runes nor changes cooldowns, costs, conversion, grace periods, or the native DK path.

Apply the narrow patch to the reviewed current PTR source, then run:

```bash
python3 tools/hybrid-rune-readiness/Test-Readiness.py --source /path/to/azerothcore/src/server/game/Entities/Player/Player.cpp --output /tmp/hero-rune-readiness-test
```

Tests compile the actual patched regeneration block with minimal state/packet doubles. They verify no early notifications, exact expiry, no repeated idle notification, repeated spending, native DK exclusion, ineligible exclusion and out-of-combat recovery. They cannot prove how the real 3.3.5 client handles the packet.

Build against the current PTR image and source. Preserve the previous image and source for rollback; validate startup privately before reopening existing ports. No SQL migration or client package is needed. Do not publish a launcher update for this server-only candidate.

In-game checks: spend all available relevant rune types, let them recover without a refresh ability, and repeat several times in and out of combat. Verify death-rune conversions and explicit reset abilities still work. Compare a native DK. If failure persists, capture server cooldowns and rejected spell identity before changing rune costs or regenerating more often.

Separate open issue: a newly created native DK received HF_PATH START_BLOCKED when selecting Class+. Its DK-start transition checks must be diagnosed separately; this patch does not bypass them.

## Initial native-DK mode selection

Read-only evidence identified level 55 with 560 XP, no quests, no build and an untouched mode journal. The zero-XP check rejected the first selection. The companion patch allows XP only when target_mode and applied_mode are both zero and level is 55. Quest, build, busy-state and inventory checks remain; later transitions still require zero XP. Class+ still resets to level 1 and zero XP. Source checked with compiled policy tests for the reported case and exclusions; full build and live test pending.

The combined local build package is Hero_DK_Rune_And_Start. It supersedes the rune-only build for the next activation. No client update or SQL migration.
