#include "ScriptMgr.h"
#include "Log.h"
#include "ModeRules.h"
class HeroAdvancementWorld final:public WorldScript {
public:
 HeroAdvancementWorld():WorldScript("HeroAdvancementWorld",{WORLDHOOK_ON_STARTUP}){}
 void OnStartup()override {
  LOG_INFO("server.loading","Hero Advancement policy foundation loaded: {} custom profiles registered. Player mutation/transport is not implemented.",HeroAdvancement::InstalledModes().size());
 }
};
void Addmod_hero_advancementScripts(){new HeroAdvancementWorld();}
