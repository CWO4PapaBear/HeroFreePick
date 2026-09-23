// Vigor keeps its existing energy aura; custom modes unlock a separate CP pool.
#include "MartialFluidity.h"
#include "ClassTrainerGate.h"
#include <algorithm>
#include <unordered_map>

namespace {
constexpr uint32 TalentSpell = 14983;
char const* SettingsSource = "hero_martial_fluidity_v1";
bool ready = false;
bool CustomMode(Player const* p) {
    auto mode = HeroTrainer::Current(p);
    return mode == HeroTrainer::Mode::ClassPlus || mode == HeroTrainer::Mode::Hybrid || mode == HeroTrainer::Mode::Hero;
}
void Reset(Player* p) {
    p->ClearTargetComboPoints();
    p->SetMartialComboPoints(0);
    p->UpdatePlayerSetting(SettingsSource, 0, 0);
    HeroMartialFluiditySend(p);
}
}

bool HeroMartialFluidityEnabled(Unit const* unit) {
    auto p = unit ? unit->ToPlayer() : nullptr;
    return ready && p && CustomMode(p) && (p->HasTalent(TalentSpell, p->GetActiveSpec()) || p->HasActiveSpell(TalentSpell));
}

void HeroMartialFluiditySend(Unit* unit) {
    auto p = unit ? unit->ToPlayer() : nullptr;
    if (!p || !p->IsInWorld() || !CustomMode(p)) return;
    bool shared = HeroMartialFluidityEnabled(p);
    unsigned points = shared ? p->GetMartialComboPoints() : 0;
    if (shared) p->UpdatePlayerSetting(SettingsSource, 0, points);
    ChatHandler(p->GetSession()).SendSysMessage("HF_COMBO " + std::to_string(shared ? 1 : 0) + " " + std::to_string(points));
}

void HeroMartialFluidityLogin(Player* p) {
    if (!CustomMode(p)) return;
    unsigned saved = p->GetPlayerSetting(SettingsSource, 0).value;
    p->SetMartialComboPoints(HeroMartialFluidityEnabled(p) && p->IsAlive() ? std::min(saved, 5u) : 0);
    p->UpdatePlayerSetting(SettingsSource, 0, p->GetMartialComboPoints());
    HeroMartialFluiditySend(p);
}

void HeroMartialFluidityLoad() {
    ready = sWorld->getBoolConfig(CONFIG_PLAYER_SETTINGS_ENABLED);
    if (!ready) {
        LOG_ERROR("server.loading", "HERO_MARTIAL_FLUIDITY validation failed: PlayerSettings disabled; must rollback");
        return;
    }
    LOG_INFO("server.loading", "HERO_MARTIAL_FLUIDITY v1 ready; Vigor custom modes; player pool 5; death clears; energy unchanged");
}

class MartialFluidityPlayer final : public PlayerScript {
    std::unordered_map<uint32, uint32> ages;
    std::mutex ageMutex;
public:
    MartialFluidityPlayer() : PlayerScript("HeroMartialFluidity", {PLAYERHOOK_CAN_LEARN_SPELL, PLAYERHOOK_CAN_LEARN_TALENT, PLAYERHOOK_ON_LEARN_SPELL, PLAYERHOOK_ON_FORGOT_SPELL, PLAYERHOOK_ON_UPDATE, PLAYERHOOK_ON_LOGOUT}) {}
    bool OnPlayerCanLearnSpell(Player* p, uint32 spell) override {
        return spell != TalentSpell || !CustomMode(p) || !p->IsInCombat();
    }
    bool OnPlayerCanLearnTalent(Player* p, TalentEntry const* talent, uint32) override {
        return !talent || talent->RankID[0] != TalentSpell || !CustomMode(p) || !p->IsInCombat();
    }
    void OnPlayerLearnSpell(Player* p, uint32 spell) override {
        if (spell == TalentSpell && CustomMode(p)) Reset(p);
    }
    void OnPlayerForgotSpell(Player* p, uint32 spell) override {
        if (spell == TalentSpell && CustomMode(p)) Reset(p);
    }
    void OnPlayerLogout(Player* p) override { std::lock_guard<std::mutex> lock(ageMutex); ages.erase(p->GetGUID().GetCounter()); }
    void OnPlayerUpdate(Player* p, uint32 diff) override {
        // Covers spec changes and other addSpell/removeSpell bypasses.
        if (p->GetMartialComboPoints() && (!HeroMartialFluidityEnabled(p) || !p->IsAlive())) Reset(p);
        // Re-establish the authoritative display after /reload, even without a new builder.
        if (HeroMartialFluidityEnabled(p)) {
            bool send = false;
            {
                std::lock_guard<std::mutex> lock(ageMutex);
                auto& age = ages[p->GetGUID().GetCounter()];
                age += diff;
                if (age >= 2000) { age = 0; send = true; }
            }
            if (send) HeroMartialFluiditySend(p);
        }
    }
};
void AddHeroMartialFluidityScripts() { new MartialFluidityPlayer(); }
