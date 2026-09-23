            if (!IsInWorld())
            {
                // Default skills can award temporary starters even without a saved spell row.
                // Reuse verified starter ownership before the initial client spell list.
                if (HeroShouldSkipSavedStarter(this, pAbility->Spell))
                    continue;
                addSpell(pAbility->Spell, SPEC_MASK_ALL, true, true);
            }
            else
            {
                learnSpell(pAbility->Spell, true, true);
            }