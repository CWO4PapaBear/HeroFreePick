#pragma once
#include "ClassTrainerPolicy.h"
#include "ScriptMgr.h"
#include "Player.h"
#include "Creature.h"
#include "Trainer.h"
#include "NPCPackets.h"
#include "ObjectMgr.h"
#include "DatabaseEnv.h"
#include "Chat.h"
#include "World.h"
#include "Log.h"
#include "WorldSession.h"
#include "CommandScript.h"
#include "PlayerScript.h"
#include "RBAC.h"
#include <chrono>
#include <unordered_map>
#include <unordered_set>
#include <mutex>
namespace HeroTrainer {
// Publish only after an authoritative mode load/commit; never from an addon message.
inline std::mutex& Mutex(){static std::mutex m;return m;}
inline std::unordered_map<uint32,Mode>& Modes(){static std::unordered_map<uint32,Mode> m;return m;}
inline void PublishMode(uint32 guid,Mode mode){std::lock_guard<std::mutex> lock(Mutex());Modes()[guid]=mode;}
struct Visit{ObjectGuid npc;std::chrono::steady_clock::time_point expires;};
inline std::unordered_map<uint32,Visit>& Visits(){static std::unordered_map<uint32,Visit> visits;return visits;}
inline void Remember(Player* p,Creature* npc){std::lock_guard<std::mutex> lock(Mutex());Visits()[p->GetGUID().GetCounter()]={npc->GetGUID(),std::chrono::steady_clock::now()+std::chrono::minutes(2)};}
inline void Forget(uint32 guid){std::lock_guard<std::mutex> lock(Mutex());Modes().erase(guid);Visits().erase(guid);}
inline Mode Current(Player const* p){std::lock_guard<std::mutex> lock(Mutex());auto it=Modes().find(p->GetGUID().GetCounter());return it==Modes().end()?Mode::Classic:it->second;}
inline std::unordered_set<uint32>& ClassTrainerIds(){static std::unordered_set<uint32> ids;return ids;}
inline bool& Ready(){static bool ready=false;return ready;}
inline uint32 TalentResetPrice(Player const* p){return sWorld->getBoolConfig(CONFIG_NO_RESET_TALENT_COST)?0:p->resetTalentsCost();}
inline void LoadTrainers(){
 auto result=WorldDatabase.Query("SELECT Id FROM trainer WHERE Type=0");
 if(!result){LOG_ERROR("server.loading","HERO_TRAINER no class-trainer metadata; custom-mode trainer purchases fail closed");return;}
 do{ClassTrainerIds().insert(result->Fetch()[0].Get<uint32>());}while(result->NextRow());
 Ready()=true;
}
inline bool RequestReset(ChatHandler* h){
 auto p=h->GetSession()->GetPlayer();if(!Custom(Current(p)))return false;
 ObjectGuid guid;
 {std::lock_guard<std::mutex> lock(Mutex());auto it=Visits().find(p->GetGUID().GetCounter());if(it==Visits().end()||std::chrono::steady_clock::now()>it->second.expires){h->SendSysMessage("Speak to your class trainer first.");return true;}guid=it->second.npc;}
 auto npc=p->GetNPCIfCanInteractWith(guid,UNIT_NPC_FLAG_TRAINER);
 auto trainer=npc?sObjectMgr->GetTrainer(npc->GetEntry()):nullptr;
 if(!trainer||trainer->GetTrainerType()!=Trainer::Type::Class||!trainer->IsTrainerValidForPlayer(p)||p->IsInCombat()){h->SendSysMessage("You must be near your class trainer and out of combat.");return true;}
 // Native confirmation and reset charge use Player::resetTalentsCost(), including server configuration.
 // Never reset or debit gold before the player accepts the native confirmation.
 p->SendTalentWipeConfirm(guid);return true;
}
class Commands final:public CommandScript{
public:Commands():CommandScript("HeroAdvancementTrainerCommands"){}
 Acore::ChatCommands::ChatCommandTable GetCommands()const override{
  using namespace Acore::ChatCommands;
  static ChatCommandTable children={{"reset",RequestReset,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No}};
  static ChatCommandTable commands={{"hftrainer",children}};return commands;
 }
};
class Gate final:public PlayerScript {
public:
 Gate():PlayerScript("HeroAdvancementClassTrainerGate",{PLAYERHOOK_ON_BEFORE_RECEIVE_SPELL_LIST_FROM_TRAINER,PLAYERHOOK_ON_GET_TRAINER_SPELL_STATE,PLAYERHOOK_ON_LOGOUT}){}
 void OnPlayerGetTrainerSpellState(Player const* p,uint32 trainerId,uint32,Trainer::SpellState& state)override{
  if(Custom(Current(p))&&(!Ready()||ClassTrainerIds().count(trainerId)))state=Trainer::SpellState::Unavailable;
 }
 void OnPlayerBeforeReceiveSpellListFromTrainer(Player* p,Creature* npc,WorldPackets::NPC::TrainerList& list)override{
  if(!BlockPurchase(Current(p),unsigned(list.TrainerType)))return;
  Remember(p,npc);list.Spells.clear();
  // The marker identifies class-trainer responses; the addon substitutes its local key binding.
  list.Greeting="HF_CLASS_TRAINER: For special heroes like you, abilities are learned through your Hero Advancement Menu. You can access that through the menu button or your assigned Hero Advancement key.";
 }
 void OnPlayerLogout(Player* p)override{Forget(p->GetGUID().GetCounter());}
};
}
