# Classic trainer-level display

Matched 369 existing catalog abilities to stock AzerothCore trainer records. Classic ability headings and tooltips use these levels; unmatched abilities appear under Other learning sources. Custom mode levels and source catalog entries are unchanged. This is a stock reference; server-specific trainer edits may differ.

Source: https://github.com/azerothcore/azerothcore-wotlk/blob/master/data/sql/base/db_world/trainer_spell.sql

Retrieved September 17, 2026. SHA-256: 18f3e7fcedcfc9bed4d47551d014c1b009dc359bb003e6415d3f59c66f5690b4

## Learning sources
Classic ability tooltips (including known spellbook entries) show verified trainer and quest sources. Quest sources match RewardDisplaySpell against catalog spells in the stock [quest_template](https://github.com/azerothcore/azerothcore-wotlk/blob/master/data/sql/base/db_world/quest_template.sql). Twelve catalog abilities matched. Unknown sources are not guessed. These references are not a live query of the installed server; custom-mode acquisition is unchanged. Quest IDs are retained in ClassicQuestSources for auditing.
