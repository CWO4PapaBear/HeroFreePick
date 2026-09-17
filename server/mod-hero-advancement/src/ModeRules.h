#pragma once
#include <array>
#include <cstdint>
#include <map>
#include <set>
#include <string>
namespace HeroAdvancement {
enum class Mode { Classic, ClassPlus, Hybrid, Hero };
struct Character { Mode mode=Mode::Classic; unsigned level=1, originalClass=0, secondClass=0; };
struct Entry { unsigned id=0, classId=0, maxRank=1, tier=0, level=1, abilityCost=0, talentCost=0, rarity=0, gems=0, mastery=0; bool talent=false; };
struct Budget { unsigned ability=0,talent=0; std::array<unsigned,5> gems{}; };
using Catalog=std::map<unsigned,Entry>;
using Build=std::map<unsigned,unsigned>;
inline bool ValidClass(unsigned c){return c>=1 && c<=11 && c!=10;}
inline bool ClassAllowed(Character const& c,unsigned classId) {
 return c.mode==Mode::Hero || classId==c.originalClass || (c.mode==Mode::Hybrid && c.level>=10 && classId==c.secondClass);
}
// Character mode, level, classes and the catalog MUST come from trusted server state.
inline std::string Validate(Character const& c,Catalog const& catalog,Build const& build,Budget& spent) {
 spent={};
 if(!ValidClass(c.originalClass))return "Invalid original class";
 if(c.mode==Mode::Classic)return "Classic uses stock validation";
 if(c.mode==Mode::Hybrid && (c.level<10 || !ValidClass(c.secondClass) || c.secondClass==c.originalClass))return "Invalid second class";
 if(build.size()>2048)return "Too many entries";
 for(auto const& selection:build) {
  auto it=catalog.find(selection.first);if(it==catalog.end())return "Unknown entry";
  auto const& e=it->second;auto rank=selection.second;
  if(!rank || rank>e.maxRank)return "Invalid rank";
  if(!ClassAllowed(c,e.classId))return "Class unavailable";
  if(e.talent) {
   if(c.level<10+5*e.tier)return "Talent tier locked";
   spent.talent+=rank*e.talentCost;
  } else {
   if(c.level<e.level)return "Ability level locked";
   if(e.mastery && !build.count(e.mastery))return "Mastery required";
   spent.ability+=e.mastery?0:e.abilityCost;
   if(e.rarity>4)return "Invalid rarity";
   if(e.rarity && !e.mastery)spent.gems[e.rarity]+=e.gems;
  }
 }
 if(spent.ability>(c.level<10?9:c.level))return "Ability budget exceeded";
 if(spent.talent>(c.level<10?0:c.level-9))return "Talent budget exceeded";
 std::array<unsigned,5> caps{0,10,12,11,6};for(unsigned i=1;i<5;++i)if(spent.gems[i]>caps[i])return "Rarity budget exceeded";
 return {};
}
inline std::set<Mode>& InstalledModes(){static std::set<Mode> modes;return modes;}
inline void RegisterMode(Mode mode){InstalledModes().insert(mode);}
// One-time choices are validated server-side by the future persistence/commit integration.
inline bool CanChooseInitial(Mode choice,unsigned level,bool alreadyChosen) {
 return level==1 && !alreadyChosen && (choice==Mode::Classic || (choice!=Mode::Hybrid && InstalledModes().count(choice)) || (choice==Mode::ClassPlus && InstalledModes().count(Mode::Hybrid)));
}
inline bool CanChooseHybrid(Character const& c,unsigned second,bool alreadyDecided) {
 return !alreadyDecided && c.mode==Mode::ClassPlus && c.level>=10 && ValidClass(second) && second!=c.originalClass && InstalledModes().count(Mode::Hybrid);
}
}
