# Pending Hero Advancement changes (0.30.0)

Hero Advancement now prepares changes without calling LearnTalent. Left-click adds a rank and right-click removes a rank in the ability list, talent trees and selection list. Ranks are bounded by the entry maximum. Resource limits no longer block edits; no actual resources are spent. Mastery prerequisites still apply; removing a Mastery also removes its pending member abilities.

The X button, N toggle, slash toggle and Escape close route open a review when selections, draft ranks or the primary stat differ from the starting state. The review lists ranks added/removed and before/after/net Ability Points, Talent Points and each gem rarity, separately for Hero Advancement and the Archetype draft.

- Accept Changes retains the changes and explains that server committing is unavailable. It does not close, save an approved build, spend resources or learn anything. Server implementation is the next stage.
- Go Back keeps pending changes and resumes editing.
- Cancel Changes restores the original selections and primary stat, then closes.
- Net-zero changes close without a prompt. Filters, search and window geometry are not class changes.

The pending baseline is stored in SavedVariables so reloading does not turn unapproved changes into an approved baseline. Existing native talent ranks seed the local baseline once when this feature is first used. Actual game state remains authoritative; reconciliation, server validation, atomic commit/refund and acknowledgments still need a backend. Archetype and Hero Advancement states remain separate.

Install then fully restart the client to load both new Lua files. Mock checks cover all 30 tree layouts, rank editing, blocked native learning, close routes, resource deltas, Cancel/Go Back/Accept behavior, persisted pending baselines, and mastery removal. In-game visual validation remains necessary.
