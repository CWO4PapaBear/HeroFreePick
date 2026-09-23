#include <set>
#include <map>
#include <cassert>
#include <algorithm>
#include "EquipmentPolicy.h"
namespace HeroBuild{using Build=std::set<unsigned>;}
struct Player{unsigned own=8,second=1,mode=3,level=10;std::set<unsigned> spells;std::map<unsigned,std::pair<unsigned,unsigned>> skills;
unsigned getClassMask(){return HeroEquipment::Bit(own);}unsigned GetLevel(){return level;}
bool HasSpell(unsigned s){return spells.count(s);}bool HasSkill(unsigned s){return skills.count(s);}
unsigned GetPureSkillValue(unsigned s){return skills.count(s)?skills[s].first:0;}unsigned GetPureMaxSkillValue(unsigned s){return skills.count(s)?skills[s].second:0;}
unsigned GetMaxSkillValueForLevel(){return level*5;}void SetSkill(unsigned s,unsigned,unsigned v,unsigned m){skills[s]={v,m};}};
unsigned HeroEquipmentClassMask(Player* p){return HeroEquipment::Mask(p->mode,p->own,p->second);}
