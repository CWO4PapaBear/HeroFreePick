# Hero Advancement tooltip cleanup

Staged for local client testing. No server, spell database, MPQ or launcher channel changes.

- Removes the obsolete blanket server-commit warning. Specific missing definitions and unfinished mechanics retain their warnings.
- Moves spell and advancement IDs, Mastery membership and click instructions into the existing tap-Shift details view.
- Removes internal recovered-tag browse provenance from player tooltips.
- Adds blank lines between sentences in Hero Advancement tooltip bodies, preserving decimal values and warning colors.

Close WoW and run `python3 Install-Client.py --wow-closed`. The installer validates reviewed hashes and backs up changed files. Test collapsed and expanded ability, talent, Mastery and Primary Stat tooltips in game. Visual layout requires in-game review.

Source belongs to HeroFreePick. This package is not a launcher release.
