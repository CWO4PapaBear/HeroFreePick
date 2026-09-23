# Temporary starter skill rewards at login

The post-activation Roguetest export confirms the first fix is active and spell rows 1752/2098 are absent. The remaining code path is learnSkillRewardedSpells: while outside the world, it calls addSpell with temporary=true directly. That bypasses the normal learning gate and can recreate the starters from class skill rewards every login; temporary spells are not saved. Later build synchronization removes them and emits the alert.

This follow-up adds the existing verified starter-ownership check to that pre-world skill-reward grant path. It does not suppress chat or alter in-world learning. Purchased starters, Classic, unrelated skill rewards, and cases with uncertain ownership retain the established policy. Requires the already active starter-login module helper and Hybrid equipment core changes.

Policy and repeated temporary-grant regression tests pass. Full PTR compile and activation are pending. Build-Test.py stages only Player.cpp, builds without restart or database changes, and restores source. No client update or SQL migration is required. The source patch and hash manifest are published; character exports and full core files are excluded.

## Patch notes

Prevent withheld original-class starter spells from returning as temporary default-skill rewards on every login. This completes the earlier saved-row correction. Test two consecutive logins, approved starter purchases, unrelated skill rewards and Classic characters.
