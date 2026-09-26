#pragma once
#include "Player.h"
#include "SpellMgr.h"
#include "SpellInfo.h"
#include "Log.h"
#include <mutex>
#include <unordered_set>

namespace HeroWarriorStances {
constexpr uint32 Aura = 9905301;
constexpr uint32 Flag = 0x20000000; // Warrior SpellFamilyFlags word C, bit 29.
constexpr uint32 Ranks[] = {100,6178,11578,6343,8198,8204,8205,11580,11581,25264,47501,47502};
inline bool ready = false;
inline std::mutex mutex;
inline std::unordered_set<uint32> eligible;
inline bool AllowedForm(uint32 form) { return form==0 || form==17 || form==18 || form==19; }
inline void Sync(Player* p) {
    bool allowed;
    { std::lock_guard<std::mutex> lock(mutex); allowed=eligible.count(p->GetGUID().GetCounter())!=0; }
    if (!ready || !allowed || !AllowedForm(p->GetShapeshiftForm())) {
        p->RemoveAurasDueToSpell(Aura);
        return;
    }
    if (p->IsInWorld() && p->IsAlive() && !p->HasAura(Aura))
        p->CastSpell(p, Aura, true);
}
inline void Publish(Player* p, bool validCustomMode) {
    { std::lock_guard<std::mutex> lock(mutex);
      if (validCustomMode) eligible.insert(p->GetGUID().GetCounter());
      else eligible.erase(p->GetGUID().GetCounter()); }
    // OnLoadFromDB publishes before aura loading. Login/Update synchronizes afterward.
    if (p->IsInWorld()) Sync(p);
}
inline void Forget(Player* p) {
    std::lock_guard<std::mutex> lock(mutex);
    eligible.erase(p->GetGUID().GetCounter());
}
inline void Load() {
    ready=false;
    auto aura=sSpellMgr->GetSpellInfo(Aura);
    if (!aura || aura->SpellFamilyName!=SPELLFAMILY_WARRIOR ||
        aura->Stances!=0x70000 || !(aura->AttributesEx2 & SPELL_ATTR2_ALLOW_WHILE_NOT_SHAPESHIFTED) ||
        aura->Effects[0].Effect!=SPELL_EFFECT_APPLY_AURA ||
        aura->Effects[0].ApplyAuraName!=SPELL_AURA_MOD_IGNORE_SHAPESHIFT ||
        aura->Effects[0].SpellClassMask[0] || aura->Effects[0].SpellClassMask[1] ||
        aura->Effects[0].SpellClassMask[2]!=Flag || aura->Effects[1].Effect || aura->Effects[2].Effect) {
        LOG_ERROR("server.loading","HERO_WARRIOR_STANCES validation failed: support aura; must rollback"); return;
    }
    for (uint32 id: Ranks) {
        auto spell=sSpellMgr->GetSpellInfo(id);
        bool charge=id==100 || id==6178 || id==11578;
        if (!spell || spell->SpellFamilyName!=SPELLFAMILY_WARRIOR ||
            !(spell->SpellFamilyFlags[2]&Flag) || spell->Stances!=(charge?0x10000u:0x30000u)) {
            LOG_ERROR("server.loading","HERO_WARRIOR_STANCES validation failed: rank {}; must rollback",id); return;
        }
    }
    ready=true;
    LOG_INFO("server.loading","HERO_WARRIOR_STANCES v1 ready; 12 ranks; Class+/Hybrid/Hero only; Classic unchanged");
}
}
