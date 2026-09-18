#include "StockRankLevels.h"
#include "ClassTrainerGate.h"
#include "PlayerScript.h"
#include "CommandScript.h"
#include "WorldScript.h"
#include "Player.h"
#include "Chat.h"
#include "WorldSession.h"
#include "DatabaseEnv.h"
#include "RBAC.h"
#include "Log.h"
#include "StartingSpells.h"
#include "CommitRules.h"
#include "GrantRules.h"
#include "SpellMgr.h"
#include "SpellInfo.h"
#include <vector>
#include <unordered_map>
#include <chrono>
#include <mutex>
using namespace Acore::ChatCommands;
namespace {
struct Spell { uint32 id; uint8 mask; bool held; };
struct Snapshot { int phase=-1; std::vector<Spell> spells; };
Snapshot Read(Player* p) {
    Snapshot result;
    auto q=CharacterDatabase.Query("SELECT phase,snapshot_count,held_count,account_id,class_id FROM hero_starting_path_test WHERE guid={}",
        p->GetGUID().GetCounter());
    if (!q) return result;
    result.phase=-2; // A present but invalid record is not a legacy Classic character.
    if(q->Fetch()[3].Get<uint32>()!=p->GetSession()->GetAccountId() || q->Fetch()[4].Get<uint8>()!=p->getClass())return result;
    int phase=q->Fetch()[0].Get<uint8>();
    uint32 count=q->Fetch()[1].Get<uint32>(), held=q->Fetch()[2].Get<uint32>(), actualHeld=0;
    auto rows=CharacterDatabase.Query("SELECT spell,spec_mask,withheld FROM hero_starting_path_spells_test WHERE guid={}",p->GetGUID().GetCounter());
    if (phase>2 || !rows || !count || !held) return result;
    do {
        auto f=rows->Fetch();Spell s{f[0].Get<uint32>(),f[1].Get<uint8>(),f[2].Get<uint8>()!=0};
        if (!s.mask || (s.held && !HeroStartingPath::Gated(p->getClass(),s.id))) return result;
        result.spells.push_back(s);actualHeld+=s.held;
    } while(rows->NextRow());
    if (result.spells.size()!=count || actualHeld!=held) return result;
    result.phase=phase;return result;
}
void PublishTrainerMode(Player* p,int phase){
 if(phase==-1){HeroTrainer::Forget(p->GetGUID().GetCounter());return;}
 HeroTrainer::PublishMode(p->GetGUID().GetCounter(),phase==1?HeroTrainer::Mode::Classic:phase==2?HeroTrainer::Mode::ClassPlus:HeroTrainer::Mode::Pending);
}
void Reply(Player* p,char const* text) { ChatHandler(p->GetSession()).SendSysMessage(std::string("HF_PATH ")+text); }
bool Commit(CharacterDatabaseTransaction t) { auto r=CharacterDatabase.AsyncCommitTransaction(t);return r.m_future.get(); }

using Clock=std::chrono::steady_clock;
struct Approved { bool valid=false; uint32 revision=0; HeroBuild::Build roots; };
struct Upload { uint32 revision=0,token=0,parts=0,next=1; HeroBuild::Build roots; Clock::time_point expires; };
std::unordered_map<uint32,Upload> uploads;
std::unordered_map<uint32,Clock::time_point> levelRefresh;
std::mutex stateMutex;
Approved LoadBuild(Player* p) {
 Approved out;auto q=CharacterDatabase.Query("SELECT revision,catalog,selections FROM hero_build_test WHERE guid={}",p->GetGUID().GetCounter());
 if(!q||q->Fetch()[1].Get<uint32>()!=HeroBuild::Version)return out;
 out.revision=q->Fetch()[0].Get<uint32>();
 out.valid=HeroBuild::Parse(q->Fetch()[2].Get<std::string>(),out.roots)&&HeroBuild::Validate(p->getClass(),p->GetLevel(),out.roots).empty();return out;
}
bool EnsureBuild(Player* p) {
 auto t=CharacterDatabase.BeginTransaction();t->Append("INSERT IGNORE INTO hero_build_test (guid,catalog) VALUES ({},{})",p->GetGUID().GetCounter(),HeroBuild::Version);return Commit(t);
}
bool Desired(Player* p,HeroBuild::Build const& roots,HeroBuild::Build& spells) {
 spells.clear();
 for(auto id:HeroBuild::Entries(roots,p->GetLevel())) {
  auto e=HeroBuild::Find(id);if(!e)return false;
  for(auto seed:e->spells) {
   unsigned first=sSpellMgr->GetFirstSpellInChain(seed);if(!first)first=seed;
   unsigned current=first;HeroBuild::Build visited;
   while(current) {
    if(!visited.insert(current).second||visited.size()>64)return false;
    auto info=sSpellMgr->GetSpellInfo(current);if(!info||!SpellMgr::CheckSpellValid(info,current,false))return false;
    // Custom unlock level controls first rank; later ranks use stock levels.
    unsigned rankLevel=e->klass==6?info->SpellLevel:HeroBuild::StockRankLevel(current,info->SpellLevel);
    if(current!=first&&(!rankLevel||rankLevel>p->GetLevel()))break;
    HeroGrant::NodeLookup lookup=[](unsigned id) {
     HeroGrant::Node node;auto child=sSpellMgr->GetSpellInfo(id);
     if(!child||!SpellMgr::CheckSpellValid(child,id,false))return node;
     node.valid=true;bool other=false;
     for(unsigned i=0;i<MAX_SPELL_EFFECTS;++i){
      auto const& effect=child->Effects[i];
      if(effect.Effect==SPELL_EFFECT_LEARN_SPELL)node.learns.push_back(effect.TriggerSpell);
      else if(effect.Effect)other=true;
     }
     node.mixed=other&&!node.learns.empty();return node;
    };
    HeroBuild::Build path;
    if(!HeroGrant::Expand(current,lookup,spells,path)){LOG_ERROR("server.loading","HERO_BUILD invalid teaching spell guid={} spell={}",p->GetGUID().GetCounter(),current);return false;}
    current=sSpellMgr->GetNextSpellInChain(current);
   }
  }
 }
 return true;
}
bool ApprovedSpell(Player* p,uint32 spell){auto b=LoadBuild(p);HeroBuild::Build wanted;return b.valid&&Desired(p,b.roots,wanted)&&wanted.count(spell);}
void BuildError(Player* p,std::string const& code){ChatHandler(p->GetSession()).SendSysMessage("HF_BUILD ERR "+code);}
void BuildReply(Player* p,Approved const& b,uint32 token=0){
 auto chunks=HeroBuild::Chunks(b.roots);ChatHandler h(p->GetSession());
 h.SendSysMessage("HF_BUILD BEGIN "+std::to_string(HeroBuild::Version)+" "+std::to_string(b.revision)+" "+std::to_string(token)+" "+std::to_string(chunks.size()));
 for(unsigned i=0;i<chunks.size();++i)h.SendSysMessage("HF_BUILD PART "+std::to_string(token)+" "+std::to_string(i+1)+" "+chunks[i]);
 h.SendSysMessage("HF_BUILD END "+std::to_string(token));
}
bool Sync(Player* p,Snapshot const& snapshot){
 if(snapshot.phase<0)return false;
 HeroBuild::Build wanted,keep,remove;
 for(auto const& s:snapshot.spells)if(!s.held||snapshot.phase==1)keep.insert(s.id);
 if(snapshot.phase==2){
  if(!EnsureBuild(p))return false;
  auto b=LoadBuild(p);if(!b.valid||!Desired(p,b.roots,wanted))return false;
  // Capture ownership before changing any spells, including level-up grants.
  auto t=CharacterDatabase.BeginTransaction();
  for(auto spell:wanted){
   bool held=false;for(auto const& s:snapshot.spells)if(s.id==spell&&s.held)held=true;
   t->Append("INSERT IGNORE INTO hero_build_spells_test (guid,spell,owned_before) VALUES ({},{},{})",p->GetGUID().GetCounter(),spell,uint32(!held&&p->HasSpell(spell)));
  }
  if(!wanted.empty()&&!Commit(t))return false;
  auto history=CharacterDatabase.Query("SELECT spell,owned_before FROM hero_build_spells_test WHERE guid={}",p->GetGUID().GetCounter());
  HeroBuild::Build recorded;
  if(history)do{auto f=history->Fetch();auto spell=f[0].Get<uint32>();recorded.insert(spell);
   if(f[1].Get<uint8>())keep.insert(spell);else if(!wanted.count(spell))remove.insert(spell);
  }while(history->NextRow());
  for(auto spell:wanted)if(!recorded.count(spell))return false;
 }
 for(auto const& s:snapshot.spells)if(s.held&&snapshot.phase!=1&&!wanted.count(s.id))remove.insert(s.id);
 for(auto spell:remove)if(!keep.count(spell)&&p->HasSpell(spell))p->removeSpell(spell,SPEC_MASK_ALL,false);
 // Removal can cascade up a native rank chain; repair desired and prior-owned
 // ranks afterward rather than deleting independently owned higher ranks.
 keep.insert(wanted.begin(),wanted.end());
 for(auto spell:keep)if(!p->HasSpell(spell))p->learnSpell(spell);
 for(auto spell:keep)if(!p->HasSpell(spell)){LOG_ERROR("server.loading","HERO_BUILD grant verification failed guid={} spell={}",p->GetGUID().GetCounter(),spell);return false;}
 for(auto spell:remove)if(!keep.count(spell)&&p->HasSpell(spell)){LOG_ERROR("server.loading","HERO_BUILD removal verification failed guid={} spell={}",p->GetGUID().GetCounter(),spell);return false;}
 auto save=CharacterDatabase.BeginTransaction();p->SaveToDB(save,false,false);return Commit(save);
}
bool BuildStatus(ChatHandler* h){
 auto p=h->GetSession()->GetPlayer();if(Read(p).phase!=2){BuildError(p,"MODE");return true;}
 if(p->IsInCombat()){BuildError(p,"COMBAT");return true;}
 if(!Sync(p,Read(p))){BuildError(p,"RECOVERY");return true;}
 auto b=LoadBuild(p);if(b.valid)BuildReply(p,b);else BuildError(p,"RECOVERY");return true;
}
bool BuildStart(ChatHandler* h,uint32 version,uint32 revision,uint32 token,uint32 parts){
 auto p=h->GetSession()->GetPlayer();auto guid=p->GetGUID().GetCounter();
 {std::lock_guard<std::mutex> lock(stateMutex);uploads.erase(guid);}
 if(Read(p).phase!=2){BuildError(p,"MODE");return true;}
 if(p->IsInCombat()){BuildError(p,"COMBAT");return true;}
 if(version!=HeroBuild::Version){BuildError(p,"VERSION");return true;}
 if(!token||!parts||parts>64){BuildError(p,"FORMAT");return true;}
 {std::lock_guard<std::mutex> lock(stateMutex);uploads[guid]={revision,token,parts,1,{},Clock::now()+std::chrono::seconds(45)};}return true;
}
bool BuildPart(ChatHandler* h,uint32 token,uint32 index,std::string text){
 std::lock_guard<std::mutex> lock(stateMutex);
 auto p=h->GetSession()->GetPlayer();auto guid=p->GetGUID().GetCounter();auto it=uploads.find(guid);
 if(it==uploads.end()||it->second.token!=token||it->second.next!=index||index>it->second.parts||Clock::now()>it->second.expires){uploads.erase(guid);BuildError(p,"UPLOAD");return true;}
 HeroBuild::Build part;
 if(text.size()>140||!HeroBuild::Parse(text,part)||(text=="-"&&it->second.parts!=1)){uploads.erase(it);BuildError(p,"FORMAT");return true;}
 for(auto id:part)if(!it->second.roots.insert(id).second){uploads.erase(it);BuildError(p,"FORMAT");return true;}
 if(it->second.roots.size()>512){uploads.erase(it);BuildError(p,"FORMAT");return true;}
 ++it->second.next;return true;
}
bool BuildApply(ChatHandler* h,uint32 token){
 Upload upload;
 {
 std::lock_guard<std::mutex> lock(stateMutex);
 auto p=h->GetSession()->GetPlayer();auto guid=p->GetGUID().GetCounter();auto it=uploads.find(guid);
 if(it==uploads.end()||it->second.token!=token||it->second.next!=it->second.parts+1||Clock::now()>it->second.expires){uploads.erase(guid);BuildError(p,"UPLOAD");return true;}
 upload=it->second;uploads.erase(it);
 }
 auto p=h->GetSession()->GetPlayer();auto guid=p->GetGUID().GetCounter();auto snapshot=Read(p);
 if(snapshot.phase!=2){BuildError(p,"MODE");return true;}
 if(p->IsInCombat()){BuildError(p,"COMBAT");return true;}
 auto error=HeroBuild::Validate(p->getClass(),p->GetLevel(),upload.roots);
 if(!error.empty()){BuildError(p,error);return true;}
 HeroBuild::Build spells;if(!Desired(p,upload.roots,spells)){BuildError(p,"SPELL_MISSING");return true;}
 if(!EnsureBuild(p)){BuildError(p,"DATABASE");return true;}
 auto prior=LoadBuild(p);if(!prior.valid){BuildError(p,"RECOVERY");return true;}
 bool retry=prior.revision>0&&upload.revision==prior.revision-1&&upload.roots==prior.roots;
 if(upload.revision!=prior.revision&&!retry){BuildError(p,"STALE");return true;}
 if(!retry&&upload.roots!=prior.roots){
  if(prior.revision==0xFFFFFFFFu){BuildError(p,"REVISION");return true;}
  auto t=CharacterDatabase.BeginTransaction();t->Append("UPDATE hero_build_test SET selections='{}',revision=revision+1 WHERE guid={} AND revision={}",HeroBuild::Encode(upload.roots),guid,prior.revision);
  if(!Commit(t)){BuildError(p,"DATABASE");return true;}
 }
 auto b=LoadBuild(p);if(!b.valid||b.roots!=upload.roots||!Sync(p,snapshot)){BuildError(p,"RECOVERY");return true;}
 LOG_INFO("server.loading","HERO_BUILD applied guid={} class={} level={} revision={} entries={}",guid,uint32(p->getClass()),p->GetLevel(),b.revision,HeroBuild::Encode(b.roots));
 BuildReply(p,b,token);return true;
}
char const* Label(int phase) { return phase==0?"PENDING":phase==1?"CLASSIC":"CLASSPLUS"; }
bool Status(ChatHandler* handler) {
    auto p=handler->GetSession()->GetPlayer();
    auto snapshot=Read(p);
    if (snapshot.phase<0) { Reply(p,snapshot.phase==-1?"LEGACY_CLASSIC":"ERROR");return true; }
    Reply(p,Sync(p,snapshot)?Label(snapshot.phase):"ERROR");return true;
}
bool Choose(ChatHandler* handler,uint8 phase) {
    auto p=handler->GetSession()->GetPlayer();

    if (!HeroStartingPath::CanChoose(p->GetLevel(),phase,p->getClass()) || p->IsInCombat()) { Reply(p,"CHOICE_BLOCKED");return true; }
    if (Read(p).phase<0) { Reply(p,"NOT_ENROLLED");return true; }
    if(phase==1) {
        auto build=LoadBuild(p);
        if(build.valid && !build.roots.empty()){BuildError(p,"CLEAR_BUILD_FIRST");return true;}
    }
    // Commit authority first; login/status safely retries an interrupted grant.
    auto t=CharacterDatabase.BeginTransaction();
    t->Append("UPDATE hero_starting_path_test SET phase={} WHERE guid={}",uint32(phase),p->GetGUID().GetCounter());
    if (!Commit(t)) { Reply(p,"ERROR");return true; }
    auto snapshot=Read(p);PublishTrainerMode(p,snapshot.phase);
    bool ok=snapshot.phase==phase && Sync(p,snapshot);
    LOG_INFO("server.loading","HERO_STARTING_PATH stage=choice guid={} phase={} saved={}",p->GetGUID().GetCounter(),uint32(phase),ok);
    Reply(p,ok?Label(phase):"ERROR");return true;
}
bool Classic(ChatHandler* h) { return Choose(h,1); }
bool ClassPlus(ChatHandler* h) { return Choose(h,2); }
class PathPlayer final:public PlayerScript {
public:
    PathPlayer():PlayerScript("HeroStartingPathTest",{PLAYERHOOK_ON_DELETE_FROM_DB,PLAYERHOOK_ON_CREATE,PLAYERHOOK_ON_LOGIN,PLAYERHOOK_CAN_LEARN_SPELL,PLAYERHOOK_ON_LEVEL_CHANGED,PLAYERHOOK_ON_UPDATE,PLAYERHOOK_ON_LOGOUT}){}
    void OnPlayerDeleteFromDB(CharacterDatabaseTransaction trans,uint32 guid) override {
        trans->Append("DELETE FROM hero_build_spells_test WHERE guid={}",guid);
        trans->Append("DELETE FROM hero_build_test WHERE guid={}",guid);
        trans->Append("DELETE FROM hero_starting_path_spells_test WHERE guid={}",guid);
        trans->Append("DELETE FROM hero_starting_path_test WHERE guid={}",guid);
    }
    void OnPlayerCreate(Player* p) override {
        if (!HeroStartingPath::Eligible(p->GetName(),p->getClass(),p->GetLevel())) return;
        std::vector<Spell> spells;uint32 held=0;
        for (auto const& entry:p->GetSpellMap()) {
            // Skill-rewarded starting spells use PLAYERSPELL_TEMPORARY in this
            // core and are rebuilt from skills on login. They are real starting
            // abilities, so snapshot them too (creation has no borrowed buffs).
            if (entry.second->State==PLAYERSPELL_REMOVED || !entry.second->specMask) continue;
            bool gate=HeroStartingPath::Gated(p->getClass(),entry.first);
            spells.push_back({entry.first,uint8(entry.second->specMask),gate});held+=gate;
        }
        if (!held) { LOG_ERROR("server.loading","HERO_STARTING_PATH no reviewed starting spells; enrollment refused");return; }
        auto t=CharacterDatabase.BeginTransaction();
        t->Append("INSERT INTO hero_starting_path_test (guid,account_id,character_name,class_id,phase,snapshot_count,held_count) VALUES ({},{},'{}',{},0,{},{})",
            p->GetGUID().GetCounter(),p->GetSession()->GetAccountId(),p->GetName(),uint32(p->getClass()),spells.size(),held);
        for (auto const& s:spells) t->Append("INSERT INTO hero_starting_path_spells_test (guid,spell,spec_mask,withheld) VALUES ({},{},{},{})",p->GetGUID().GetCounter(),s.id,uint32(s.mask),uint32(s.held));
        bool ok=Commit(t);
        if(ok)PublishTrainerMode(p,0);
        LOG_INFO("server.loading","HERO_STARTING_PATH stage=enroll guid={} class={} held={} protected={} saved={}",p->GetGUID().GetCounter(),uint32(p->getClass()),held,spells.size()-held,ok);
    }
    bool OnPlayerCanLearnSpell(Player* p,uint32 spell) override {
        if (!HeroStartingPath::Gated(p->getClass(),spell)) return true;
        auto snapshot=Read(p);
        if (snapshot.phase==-1 || snapshot.phase==1) return true;
        if (snapshot.phase==-2)return false;
        for (auto const& s:snapshot.spells) if (s.held && s.id==spell) return snapshot.phase==2 && ApprovedSpell(p,spell);
        return true;
    }

    void OnPlayerLevelChanged(Player* p,uint8) override {
        std::lock_guard<std::mutex> lock(stateMutex);
        if(HeroTrainer::Current(p)==HeroTrainer::Mode::ClassPlus)levelRefresh[p->GetGUID().GetCounter()]=Clock::now()+std::chrono::seconds(1);
    }
    void OnPlayerUpdate(Player* p,uint32) override {

        {
        std::lock_guard<std::mutex> lock(stateMutex);
        auto guid=p->GetGUID().GetCounter();auto it=levelRefresh.find(guid);
        if(it==levelRefresh.end()||Clock::now()<it->second||p->IsInCombat())return;
        levelRefresh.erase(it);
        }
        auto guid=p->GetGUID().GetCounter();auto snapshot=Read(p);if(snapshot.phase!=2)return;
        if(Sync(p,snapshot)){auto b=LoadBuild(p);BuildReply(p,b);LOG_INFO("server.loading","HERO_BUILD level-grants guid={} level={} verified=true",guid,p->GetLevel());}
        else BuildError(p,"RECOVERY");
    }
    void OnPlayerLogout(Player* p) override { std::lock_guard<std::mutex> lock(stateMutex);auto guid=p->GetGUID().GetCounter();uploads.erase(guid);levelRefresh.erase(guid); }
    void OnPlayerLogin(Player* p) override {

        auto snapshot=Read(p);PublishTrainerMode(p,snapshot.phase);if (snapshot.phase<0) { Reply(p,snapshot.phase==-1?"LEGACY_CLASSIC":"ERROR");return; }
        bool ok=Sync(p,snapshot);
        LOG_INFO("server.loading","HERO_STARTING_PATH stage=login guid={} phase={} baseline_verified={}",p->GetGUID().GetCounter(),snapshot.phase,ok);
        Reply(p,ok?Label(snapshot.phase):"ERROR");
    }
};
class PathCommands final:public CommandScript {
public:
    PathCommands():CommandScript("HeroStartingPathCommands"){}
    ChatCommandTable GetCommands() const override {
        static ChatCommandTable child={{"status",Status,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"classic",Classic,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"classplus",ClassPlus,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No}};
        static ChatCommandTable build={{"status",BuildStatus,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"start",BuildStart,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"part",BuildPart,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No},{"apply",BuildApply,rbac::RBAC_PERM_COMMAND_ACCOUNT,Console::No}};
        static ChatCommandTable root={{"hfpath",child},{"hfbuild",build}};return root;
    }
};
class PathWorld final:public WorldScript {
public:
    PathWorld():WorldScript("HeroStartingPathWorld",{WORLDHOOK_ON_STARTUP}){}
    void OnStartup() override {
        HeroTrainer::LoadTrainers();if(!HeroTrainer::Ready())return;
        if(!HeroBuild::SelfTest()||!HeroGrant::SelfTest()){LOG_ERROR("server.loading","HERO_BUILD policy self-test failed; deployment must roll back");return;}
        LOG_INFO("server.loading","HERO_STARTING_PATH ready v5.1; HERO_BUILD policy self-test passed; persistent ClassPlus enrollment");
    }
};
}
void Addmod_hero_starting_pathScripts() { new PathPlayer();new PathCommands();new PathWorld();new HeroTrainer::Gate();new HeroTrainer::Commands(); }
