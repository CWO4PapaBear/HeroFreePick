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
