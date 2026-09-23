# Hybrid equipment access

Hybrid characters gain the weapon and armor proficiencies of both selected classes when their selection is committed. Existing Hybrids are reconciled on login, and level changes unlock the appropriate upgrades. Equipment eligibility recognizes either selected class; existing weapon skill values are preserved, and newly learned weapon skills start at 1.

Classic and Class+ retain their existing equipment rules. A Hybrid upgrading to Hero retains the selected pair's equipment access; this patch does not introduce a separate all-class Hero policy. Professions, item level, race, reputation, required spells and other item requirements remain enforced.

## Level rules

- Plate: level 40, including custom level-one Death Knight progression.
- Hunter/Shaman mail: level 40. Warrior, Paladin and Death Knight mail: level 1.
- Polearms: level 20; existing learned skills are not removed.
- Ordinary Dual Wield: Rogue 10, Warrior/Hunter 20, Death Knight 1. Shaman Dual Wield remains talent-gated.
- Other supported weapon types, shields and lighter armor: available with the committed class pair.

The class masks were checked against stock WotLK SkillLineAbility and SkillRaceClassInfo records; level rules were checked against the PTR trainer export and existing custom DK startup policy. The authoritative class pair is loaded before character skills, spells and inventory, so secondary-class skills survive reconnects.

## Validation and deployment status

Compiled C++ policy tests cover all 90 ordered class pairs, level boundaries, unchanged Classic/profession behavior and the actual staged grant functions. They verify that a trained weapon skill keeps its value when its cap increases. Full PTR compilation and in-game testing are still required. No activation, SQL migration or client update has occurred for this package.

The local Build-Test.py verifies the reviewed source hashes, builds an isolated image and restores the source, including removal of its newly added header. It does not restart the server. Activation follows review of the build result.

The published source package contains a minimal patch against the reviewed PTR source, its SHA-256 manifest and standalone tests. It intentionally excludes full exported core files and database records. Apply only against matching source; do not bypass failed patch or hash checks.

```bash
git apply --check hybrid-equipment.patch
git apply hybrid-equipment.patch
python3 Test-Equipment.py
```

Those commands are for a development checkout with the matching PTR integrations, not an unmodified AzerothCore installation. A C++17 compiler is required; CXX may select another compiler.

## PTR checks after activation

1. Commit a second class and equip weapons, shields and armor that only that class permits.
2. Repeat with an existing Hybrid after reconnecting; verify skill progress and equipped items survive a second reconnect.
3. Check the level-20 and level-40 gates, including a class pair with different mail access.
4. Confirm a Classic character and professions retain their existing restrictions.
5. Test class-restricted equipment as well as ordinary items. The stock client may still describe the original class in some tooltips; report any client-side refusal separately from server eligibility.

## Draft patch notes

Hybrid characters can use the weapons and armor available to either selected class. Proficiencies are granted automatically after choosing the second class and reconciled for existing Hybrids at login. Normal level gates still apply, and trained weapon skill progress is preserved. Please test equipment from both classes, reconnect persistence, and mail/plate unlocks at level 40.
