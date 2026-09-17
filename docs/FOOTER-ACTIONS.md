# Footer apply/reset controls

AP and TP widths follow measured text, reserving at least two digits (TP includes remaining/total). TP retains its prior right edge. Three controls occupy the gap: Apply Pending, Reset Pending, Reset Learned.

Classic enables Apply Pending Talents and Reset Pending Talents only. Other action choices are disabled. Custom modes can review the combined pending build and discard ability changes, talent changes, or both. Reset Pending restores the selected category from the preparation baseline; it does not erase applied ranks or actual spellbook ownership.

## Server integration still required

Reset Learned is disabled in all modes in this build. Custom Accept still requires the future commit handler. No client reset or gold deduction occurs.

For custom applied-talent resets, the server must compute the same price as its trainer reset path, using the character's reset history and server configuration. Return a quote for confirmation, revalidate it on acceptance, check funds, then perform the reset and charge atomically through the server's normal reset logic. Reject stale quotes and duplicate requests. The client must refresh authoritative ranks/resources only after success. Do not implement a hardcoded addon gold formula. Classic continues to visit a trainer.

Ability-only reset fees are not specified by the current request; do not infer one. Combined resets must include the normal talent reset charge whenever applied talents are reset.
