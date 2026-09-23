from pathlib import Path
import shutil,subprocess,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
test=HERE/'local-tests/module';test.mkdir(parents=True,exist_ok=True)
for n in ('MartialFluidity.cpp','MartialFluidity.h'):shutil.copy2(HERE/n,test/n)
(test/'ClassTrainerGate.h').write_text(r'''
#pragma once
#include <cstdint>
#include <string>
#include <initializer_list>
#include <vector>
#include <mutex>
using uint32=std::uint32_t;
class Player;
class Unit {public:virtual ~Unit()=default;virtual Player* ToPlayer(){return nullptr;}virtual Player const* ToPlayer()const{return nullptr;}};
namespace HeroTrainer {enum class Mode{Classic,ClassPlus,Hybrid,Hero,Pending};}
struct Guid{uint32 GetCounter()const{return 1;}};
struct PlayerSetting{uint32 value;};
class Player:public Unit {public:
 bool talentKnown=false,known=false,world=true,alive=true,combat=false;HeroTrainer::Mode mode=HeroTrainer::Mode::Hero;
 unsigned points=0,native=0,saved=0,writes=0;
 Player* ToPlayer()override{return this;}Player const* ToPlayer()const override{return this;}
 bool HasActiveSpell(uint32)const{return known;} bool HasTalent(uint32,unsigned)const{return talentKnown;} unsigned GetActiveSpec()const{return 0;}bool IsInWorld()const{return world;}bool IsAlive()const{return alive;}bool IsInCombat()const{return combat;}
 void ClearTargetComboPoints(){native=0;}void SetMartialComboPoints(unsigned n){points=n;}unsigned GetMartialComboPoints()const{return points;}
 void UpdatePlayerSetting(char const*,unsigned,unsigned n){saved=n;++writes;}PlayerSetting GetPlayerSetting(char const*,unsigned){return {saved};}
 void* GetSession(){return nullptr;}Guid GetGUID()const{return {};}
};
namespace HeroTrainer {inline Mode Current(Player const* p){return p->mode;}}
inline std::vector<std::string> messages;
struct ChatHandler{explicit ChatHandler(void*){}void SendSysMessage(std::string const& s){messages.push_back(s);}};
struct World{bool enabled=true;bool getBoolConfig(int){return enabled;}};inline World world;inline World* sWorld=&world;
constexpr int CONFIG_PLAYER_SETTINGS_ENABLED=1;
struct TalentEntry{unsigned RankID[5]{};};
enum {PLAYERHOOK_CAN_LEARN_SPELL,PLAYERHOOK_CAN_LEARN_TALENT,PLAYERHOOK_ON_LEARN_SPELL,PLAYERHOOK_ON_FORGOT_SPELL,PLAYERHOOK_ON_UPDATE,PLAYERHOOK_ON_LOGOUT};
class PlayerScript{public:PlayerScript(char const*,std::initializer_list<int>){}virtual ~PlayerScript()=default;
 virtual bool OnPlayerCanLearnSpell(Player*,uint32){return true;}virtual bool OnPlayerCanLearnTalent(Player*,TalentEntry const*,uint32){return true;}
 virtual void OnPlayerLearnSpell(Player*,uint32){}virtual void OnPlayerForgotSpell(Player*,uint32){}virtual void OnPlayerUpdate(Player*,uint32){}virtual void OnPlayerLogout(Player*){}
};
#define LOG_INFO(...) ((void)0)
#define LOG_ERROR(...) ((void)0)
''')
(test/'test.cpp').write_text(r'''
#include "MartialFluidity.cpp"
#include <cassert>
int main(){
 HeroMartialFluidityLoad();MartialFluidityPlayer hooks;TalentEntry talent{{14983}};
 for(auto mode:{HeroTrainer::Mode::Classic,HeroTrainer::Mode::ClassPlus,HeroTrainer::Mode::Hybrid,HeroTrainer::Mode::Hero,HeroTrainer::Mode::Pending}){
  Player p;p.mode=mode;bool custom=mode!=HeroTrainer::Mode::Classic&&mode!=HeroTrainer::Mode::Pending;
  p.known=true;assert(HeroMartialFluidityEnabled(&p)==custom);p.combat=true;
  assert(hooks.OnPlayerCanLearnSpell(&p,14983)==!custom);assert(hooks.OnPlayerCanLearnTalent(&p,&talent,0)==!custom);
  assert(hooks.OnPlayerCanLearnSpell(&p,1752));p.combat=false;assert(hooks.OnPlayerCanLearnSpell(&p,14983));
  p.native=4;p.points=5;p.saved=5;hooks.OnPlayerLearnSpell(&p,14983);
  if(custom){assert(p.native==0&&p.points==0&&p.saved==0);p.saved=4;HeroMartialFluidityLogin(&p);assert(p.points==4);
   p.points=3;HeroMartialFluiditySend(&p);assert(p.saved==3);p.points=0;HeroMartialFluidityLogin(&p);assert(p.points==3);
   auto count=messages.size();hooks.OnPlayerUpdate(&p,2000);assert(messages.size()==count+1);
   p.known=false;hooks.OnPlayerForgotSpell(&p,14983);assert(p.points==0&&p.saved==0);
   p.known=true;p.saved=5;p.alive=false;HeroMartialFluidityLogin(&p);assert(p.points==0&&p.saved==0);
  }else{auto writes=p.writes;HeroMartialFluidityLogin(&p);assert(p.writes==writes&&p.native==4&&p.saved==5);}
 }
 Player native;native.talentKnown=true;assert(!native.HasActiveSpell(14983));assert(HeroMartialFluidityEnabled(&native));native.saved=4;HeroMartialFluidityLogin(&native);assert(native.points==4);native.talentKnown=false;hooks.OnPlayerUpdate(&native,1);assert(native.points==0);
 Player p;p.known=true;world.enabled=false;HeroMartialFluidityLoad();assert(!HeroMartialFluidityEnabled(&p));
}
''')
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(ROOT/'work/zig-cache'))
subprocess.run([str(ROOT/'work/login/compiler/ziglang/zig.exe'),'c++','-std=c++17','-Wall','-Wextra','-Werror',str(test/'test.cpp'),'-o',str(test/'test.exe')],check=True,env=env)
subprocess.run([str(test/'test.exe')],check=True)
print('PASS: production module mode/talent gates, combat denial, learning/removal clears, saved login count, dead login, Classic untouched and reload display refresh.')
