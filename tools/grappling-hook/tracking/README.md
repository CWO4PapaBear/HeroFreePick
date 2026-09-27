# Chain tracking experiment - local installation

The prior caster-side attachment test still trailed. This experiment changes only owned SpellVisualKit 15706 chain parameters at fields 25/29 to 1.0 (as in native Drain Life/Mind Flay) and owned SpellChainEffects 1181 flags from 449 to 320 (native Mind Flay chain 750). Texture and size are retained. The precise parameter semantics are not established; this is a runtime hypothesis, not a verified fix.

Installed locally with backups and hash verification. No server changes or launcher publication. Verify both ground-anchor and enemy-follow-up endpoints during movement and at arrival. If ineffective, restore this installation's backups before a different experiment.

Run from workspace outputs/Hero_Grappling_Hook_Tracking with existing MPQ tooling and the reviewed client baseline. Stage.py preserves all unrelated records and checks reconstructed archive entries. Close WoW before Install-Client.py. Binary assets and backups are not published.
