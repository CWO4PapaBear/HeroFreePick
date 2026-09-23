
#include "ClassTrainerGate.h"
#include "Config.h"
#include "SharedProgression.h"
#include <cassert>
int main(){
 HeroSharedProgressionLoad();
 for(auto mode:{HeroTrainer::Mode::Classic,HeroTrainer::Mode::ClassPlus,HeroTrainer::Mode::Hybrid,HeroTrainer::Mode::Hero,HeroTrainer::Mode::Pending})
 for(unsigned level=0;level<=81;++level){
  Player p;p.mode=mode;p.level=level;
  PlayerLevelInfo i{};PlayerClassLevelInfo c{};i.stats[0]=999;c.basehealth=999;
  bool expected=level>=1&&level<=80&&(mode==HeroTrainer::Mode::Hero||(mode==HeroTrainer::Mode::Hybrid&&level>=10));
  assert(HeroSharedProgressionApply(&p,level,i,c)==expected);
  if(expected){assert(i.stats[0]==21+level);assert(i.stats[1]==18+level);assert(i.stats[2]==23+level);assert(c.basehealth==HeroSharedCurve::Pools[level-1].health);}
  else{assert(i.stats[0]==999&&c.basehealth==999);}
 }
 Player p;p.level=80;assert(HeroSharedProgressionRefresh(&p));assert(p.basehealth==7350&&p.basemana==4050&&p.stats[0]==101);
 assert(p.health==25&&p.mana==30&&p.gear==17);auto count=p.updates;
 assert(HeroSharedProgressionRefresh(&p)&&p.updates==count); // idempotent; no refill
 p.level=10;p.health=99999;p.mana=99999;assert(HeroSharedProgressionRefresh(&p));assert(p.basehealth==115&&p.basemana==190);assert(p.health==p.maxhealth&&p.mana==p.maxmana);
 p.health=0;p.level=11;assert(HeroSharedProgressionRefresh(&p)&&p.health==0); // dead remains dead
 p.race=99;assert(!HeroSharedProgressionRefresh(&p));
 configEnabled=false;HeroSharedProgressionLoad();p.race=1;assert(!HeroSharedProgressionRefresh(&p));
 configEnabled=true;missingRace=true;HeroSharedProgressionLoad();assert(!HeroSharedProgressionRefresh(&p));
}
