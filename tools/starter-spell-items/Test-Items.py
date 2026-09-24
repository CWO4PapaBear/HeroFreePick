from pathlib import Path
import shutil,subprocess,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;t=HERE/'local-tests';t.mkdir(exist_ok=True)
shutil.copy2(HERE/'StarterSpellItems.cpp',t/'StarterSpellItems.cpp')
common=r"""
#pragma once
#include <cstdint>
#include <map>
#include <set>
#include <vector>
#include <string>
using uint32=std::uint32_t;
class Totem; // Match the real core declaration that exposed the helper collision.
struct Item{};using ItemPosCountVec=std::vector<unsigned>;
constexpr int NULL_BAG=0,NULL_SLOT=0,EQUIP_ERR_OK=0,CONFIG_PLAYER_SETTINGS_ENABLED=0;
namespace HeroTrainer{enum class Mode{Classic,ClassPlus,Hybrid,Hero,Pending};}
struct Setting{unsigned value;};
struct Player{HeroTrainer::Mode mode=HeroTrainer::Mode::Hybrid;std::set<unsigned> spells,talents;std::map<unsigned,unsigned> items,ledger;bool full=false;unsigned itemId=0,amount=0;
 bool HasSpell(unsigned n){return spells.count(n);}bool HasTalent(unsigned n,unsigned){return talents.count(n);}unsigned GetActiveSpec(){return 0;}bool HasItemTotemCategory(unsigned){return false;}
 Setting GetPlayerSetting(char const*,unsigned n){return {ledger[n]};}void UpdatePlayerSetting(char const*,unsigned n,unsigned v){ledger[n]=v;}unsigned GetItemCount(unsigned n,bool){return items[n];}unsigned GetLevel(){return 80;}unsigned getRaceMask(){return 1;}
 int CanStoreNewItem(int,int,ItemPosCountVec&,unsigned n,unsigned c){itemId=n;amount=c;return full?1:0;}Item* StoreNewItem(ItemPosCountVec const&,unsigned n,bool){items[n]+=amount;static Item i;return &i;}void SendNewItem(Item*,unsigned,bool,bool){}
};
namespace HeroTrainer{inline Mode Current(Player* p){return p->mode;}}
struct Entry{std::vector<unsigned> spells;};namespace HeroBuild{inline std::vector<Entry> rows={{{100,101,102,103}}};inline auto const& Catalog(){return rows;}}
struct SpellInfo{unsigned TotemCategory[2]{},Totem[2]{};int Reagent[8]{},ReagentCount[8]{};};
struct SM{std::map<unsigned,SpellInfo> rows;SpellInfo* GetSpellInfo(unsigned n){return &rows[n];}};inline SM sm;inline SM* sSpellMgr=&sm;
struct Template{unsigned RequiredLevel=0,AllowableRace=~0u;unsigned GetMaxStackSize(){return 20;}};
struct OM{Template* GetItemTemplate(unsigned){static Template t;return &t;}};inline OM om;inline OM* sObjectMgr=&om;
struct World{bool getBoolConfig(int){return true;}};inline World w;inline World* sWorld=&w;
#define LOG_ERROR(...) ((void)0)
#define LOG_INFO(...) ((void)0)
"""
(t/'common.h').write_text(common)
for name in ('ClassTrainerGate.h','GeneratedCatalog.h','SpellMgr.h','SpellInfo.h','Item.h'):(t/name).write_text('#include "common.h"\n')
(t/'test.cpp').write_text(r"""
#include "StarterSpellItems.cpp"
#include <cassert>
int main(){HeroStarterSpellItemsLoad();sm.rows[100].TotemCategory[0]=2;sm.rows[101].Reagent[0]=17056;sm.rows[101].ReagentCount[0]=1;sm.rows[102].Reagent[0]=99999;sm.rows[102].ReagentCount[0]=1;
for(auto mode:{HeroTrainer::Mode::ClassPlus,HeroTrainer::Mode::Hybrid,HeroTrainer::Mode::Hero}){Player p;p.mode=mode;p.spells={75,100,101,102};HeroStarterSpellItemsGrant(&p);assert(p.items[5175]==1&&p.items[17056]==20&&p.items[2512]==200&&p.items[2516]==200&&!p.items[99999]);p.items[17056]=0;HeroStarterSpellItemsGrant(&p);assert(!p.items[17056]);}
for(auto mode:{HeroTrainer::Mode::Classic,HeroTrainer::Mode::Pending}){Player p;p.mode=mode;p.spells={75,100};HeroStarterSpellItemsGrant(&p);assert(p.items.empty()&&p.ledger.empty());}
Player full;full.spells={100};full.full=true;HeroStarterSpellItemsGrant(&full);assert(!full.items[5175]&&!full.ledger[5175]);full.full=false;HeroStarterSpellItemsGrant(&full);assert(full.items[5175]==1);
Player owned;owned.spells={101};owned.items[17056]=25;HeroStarterSpellItemsGrant(&owned);assert(owned.items[17056]==25&&owned.ledger[17056]);
Player native;native.talents={100};HeroStarterSpellItemsGrant(&native);assert(native.items[5175]==1);
}
""")
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(ROOT/'work/zig-cache'));subprocess.run([str(ROOT/'work/login/compiler/ziglang/zig.exe'),'c++','-std=c++17','-Wall','-Wextra','-Werror',str(t/'test.cpp'),'-o',str(t/'test.exe')],check=True,env=env);subprocess.run([str(t/'test.exe')],check=True);print('PASS: production grant helper, custom modes, Classic/pending isolation, requirements, no refill, full bags/retry, existing ownership and native talent path.')
