# Ground anchor height adjustment - compiled, not activated

The aura-bound chain test was reported close to the desired behavior, with the initial endpoint above the ground circle. The initial cast uses temporary World Trigger 18721, an invisible humanoid helper. Set only that summoned instance's object scale to 0.01 before casting the visual, intending to reduce model attachment height near the exact selected ground point. Do not modify its shared template or enemy targets. Chain visual parameters, one-second aura, movement and follow-up are unchanged. In-game height and chain appearance remain unverified.

Full PTR build passed; original source restored without errors. No SQL or spell-data change. Current aura-bound client is already installed. Hook tip alignment remains separate, unverified work. No launcher publication.

Run from the established workspace outputs/Hero_Grappling_Hook_Ground_Anchor. Preflight:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Ground_Anchor/Activate-Test.py --check
```

After preflight and arranged maintenance:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Ground_Anchor/Activate-Test.py --activate --maintenance --client-ready
```

Rollback restores the previous image/source without removing Grappling Hook selections or changing SQL:

```bash
sudo python3 /mnt/c/Users/danie/Documents/Codex/2026-09-12/can/outputs/Hero_Grappling_Hook_Ground_Anchor/Activate-Test.py --rollback --maintenance
```
