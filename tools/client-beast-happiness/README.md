# Stable current-pet portrait

The live-primary compatibility test now displays the Abomination model and purchase controls, but its placeholder icon is a whistle. Replace only that missing-icon fallback with SetPortraitTexture using the active pet. Existing native family icons remain unchanged. No stable transaction or server changes.

Close WoW and run Install-Client.py --wow-closed. The installer pins and backs up the currently installed compatibility file. Reference UI checks include the current-pet portrait texture. In-game storage/retrieval acceptance and launcher publication remain pending.

Happiness/diet controls are hidden for non-Beasts in the native stable, native pet frame and pet paperdoll. The HeroFreePick portrait hides its happiness control using the same Beast-only criterion. This changes display only, not server pet stats. Stable storage remains unresolved and is not claimed fixed by this UI package.
