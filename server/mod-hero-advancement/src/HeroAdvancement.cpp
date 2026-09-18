#include "ScriptMgr.h"
#include "WorldScript.h"
#include "Log.h"
#include "ModeRules.h"
#include "ClassTrainerGate.h"
class HeroAdvancementWorld final:public WorldScript {
public:
 HeroAdvancementWorld():WorldScript("HeroAdvancementWorld",{WORLDHOOK_ON_STARTUP}){}
 void OnStartup()override {
  HeroTrainer::LoadTrainers();
  LOG_INFO("server.loading","Hero Advancement policy foundation loaded: {} custom profiles registered. Player mutation/transport is not implemented.",HeroAdvancement::InstalledModes().size());
 }
};
void Addmod_hero_advancementScripts(){new HeroAdvancementWorld();new HeroTrainer::Gate();new HeroTrainer::Commands();}
