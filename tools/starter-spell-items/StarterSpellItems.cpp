#include "ClassTrainerGate.h"
#include "GeneratedCatalog.h"
#include "SpellMgr.h"
#include "SpellInfo.h"
#include "Item.h"
#include <algorithm>
#include <map>

namespace {
char const* Ledger = "hero_starter_spell_items_v1";
bool Enabled = false;
// Only class spell supplies, never profession materials or quest objectives.
bool Supply(uint32 id) {
    switch (id) {
        case 5140: case 5565: case 6265: case 17020: case 17028: case 17029:
        case 17030: case 17031: case 17032: case 17033: case 17034: case 17035:
        case 17036: case 17037: case 17038: case 17056: case 17057: case 17058:
        case 20748: case 21177: case 22147: case 22148: case 37201: case 44605:
        case 44614: case 44615: return true;
        default: return false;
    }
}
uint32 StarterTotemItemForCategory(uint32 category) {
    switch(category) {case 2:return 5175;case 3:return 5178;case 4:return 5176;case 5:return 5177;default:return 0;}
}
}
void HeroStarterSpellItemsLoad() {
    Enabled = sWorld->getBoolConfig(CONFIG_PLAYER_SETTINGS_ENABLED);
    if (!Enabled) { LOG_ERROR("server.loading", "HERO_STARTER_ITEMS validation failed: PlayerSettings disabled; must rollback"); return; }
    for (uint32 id : {5175u,5176u,5177u,5178u,2512u,2516u})
        if (!sObjectMgr->GetItemTemplate(id)) { Enabled=false; LOG_ERROR("server.loading", "HERO_STARTER_ITEMS validation failed: missing item {}; must rollback",id); return; }
    LOG_INFO("server.loading", "HERO_STARTER_ITEMS v1 ready; ability-based initial supplies; no automatic refill");
}
// Called inside the existing build save: items and ledger share SaveToDB's transaction.
void HeroStarterSpellItemsGrant(Player* p) {
    auto mode=HeroTrainer::Current(p);
    if (!Enabled || (mode!=HeroTrainer::Mode::ClassPlus && mode!=HeroTrainer::Mode::Hybrid && mode!=HeroTrainer::Mode::Hero)) return;
    std::map<uint32,uint32> wanted;
    for (auto const& e : HeroBuild::Catalog()) for (auto id : e.spells) {
        if (!p->HasSpell(id) && !p->HasTalent(id,p->GetActiveSpec())) continue;
        auto info=sSpellMgr->GetSpellInfo(id);if (!info) continue;
        for (unsigned i=0;i<2;++i) {
            uint32 item=StarterTotemItemForCategory(info->TotemCategory[i]);
            if (item && !p->HasItemTotemCategory(info->TotemCategory[i])) wanted[item]=1;
            if (info->Totem[i]>=5175 && info->Totem[i]<=5178) wanted[info->Totem[i]]=1;
        }
        for (unsigned i=0;i<8;++i) if (info->Reagent[i]>0 && Supply(uint32(info->Reagent[i]))) {
            uint32 item=uint32(info->Reagent[i]);auto t=sObjectMgr->GetItemTemplate(item);if (!t) continue;
            uint32 count=std::min<uint32>(20,t->GetMaxStackSize());
            if (uint32(info->ReagentCount[i])>count) continue; // No partial cast kit.
            wanted[item]=std::max(wanted[item],count);
        }
    }
    // Auto Shot supports both ammunition-consuming weapon types. No forced equip.
    if (p->HasSpell(75)) { wanted[2512]=200;wanted[2516]=200; }
    for (auto const& supply : wanted) {
        uint32 id=supply.first,count=supply.second;
        if (p->GetPlayerSetting(Ledger,id).value) continue;
        uint32 owned=p->GetItemCount(id,true); // Includes bank: do not duplicate owned supplies.
        if (owned>=count) {p->UpdatePlayerSetting(Ledger,id,1);continue;}
        auto t=sObjectMgr->GetItemTemplate(id);
        if (!t || t->RequiredLevel>p->GetLevel() || !(t->AllowableRace&p->getRaceMask())) continue;
        ItemPosCountVec dest;
        if (p->CanStoreNewItem(NULL_BAG,NULL_SLOT,dest,id,count-owned)!=EQUIP_ERR_OK) continue;
        if (Item* item=p->StoreNewItem(dest,id,true)) {
            p->SendNewItem(item,count-owned,true,false);
            p->UpdatePlayerSetting(Ledger,id,1);
        }
    }
}
