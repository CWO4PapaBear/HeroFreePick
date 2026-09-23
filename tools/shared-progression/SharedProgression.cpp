// Experimental PTR balance policy. No writes to class tables or character builds.
#include "SharedProgression.h"
#include "ClassTrainerGate.h"
#include "Config.h"
#include <array>
#include <map>
#include <algorithm>

namespace {
std::map<unsigned, std::array<int, 5>> raceOffsets;
bool enabled = false;
}

void HeroSharedProgressionLoad() {
    enabled = false;
    raceOffsets.clear();
    if (!sConfigMgr->GetOption<bool>("Hero.SharedProgression.Enable", true)) {
        LOG_INFO("server.loading", "HERO_SHARED_PROGRESSION disabled; original class progression retained");
        return;
    }
    auto result = WorldDatabase.Query("SELECT Race, Strength, Agility, Stamina, Intellect, Spirit FROM player_race_stats");
    if (!result) {
        LOG_ERROR("server.loading", "HERO_SHARED_PROGRESSION validation failed: missing race modifiers; must rollback");
        return;
    }
    do {
        auto f = result->Fetch();
        std::array<int, 5> offsets{};
        for (unsigned i = 0; i < 5; ++i) offsets[i] = f[i+1].Get<int16>();
        raceOffsets.emplace(f[0].Get<uint8>(), offsets);
    } while (result->NextRow());
    for (unsigned race : {1u,2u,3u,4u,5u,6u,7u,8u,10u,11u}) {
        auto it = raceOffsets.find(race);
        if (it == raceOffsets.end() || std::any_of(it->second.begin(), it->second.end(), [](int n){return n < -20 || n > 1000;})) {
            LOG_ERROR("server.loading", "HERO_SHARED_PROGRESSION validation failed: race {}; must rollback", race);
            return;
        }
    }
    enabled = true;
    LOG_INFO("server.loading", "HERO_SHARED_PROGRESSION v1 ready; EXPERIMENTAL ROLLBACK CANDIDATE; Hero 1-80 Hybrid 10-80; Class+ unchanged");
}

bool HeroSharedProgressionApply(Player const* p, unsigned level, PlayerLevelInfo& info, PlayerClassLevelInfo& pools) {
    if (!enabled || !p) return false;
    auto mode = HeroTrainer::Current(p);
    if (!HeroSharedCurve::Eligible(mode == HeroTrainer::Mode::Hero, mode == HeroTrainer::Mode::Hybrid, level)) return false;
    auto race = raceOffsets.find(p->getRace(true));
    if (race == raceOffsets.end()) return false;
    for (unsigned i = 0; i < 5; ++i) info.stats[i] = 20 + level + race->second[i];
    pools.basehealth = HeroSharedCurve::Pools[level-1].health;
    pools.basemana = HeroSharedCurve::Pools[level-1].mana;
    return true;
}

bool HeroSharedProgressionRefresh(Player* p) {
    PlayerLevelInfo info{};
    PlayerClassLevelInfo pools{};
    if (!HeroSharedProgressionApply(p, p->GetLevel(), info, pools)) return false;
    bool changed = p->GetCreateHealth() != pools.basehealth || p->GetCreateMana() != pools.basemana;
    for (unsigned i = 0; i < 5; ++i) changed = changed || p->GetCreateStat(Stats(i)) != info.stats[i];
    if (!changed) return true;
    // Recompute only base values; retain gear/auras and never refill on refresh.
    auto health = p->GetHealth();
    auto mana = p->GetPower(POWER_MANA);
    for (unsigned i = 0; i < 5; ++i) p->SetCreateStat(Stats(i), info.stats[i]);
    p->SetCreateHealth(pools.basehealth);
    p->SetCreateMana(pools.basemana);
    p->UpdateAllStats();
    p->SetHealth(std::min(health, p->GetMaxHealth()));
    p->SetPower(POWER_MANA, std::min(mana, p->GetMaxPower(POWER_MANA)));
    return true;
}
