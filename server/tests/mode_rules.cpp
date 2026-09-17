#include "../mod-hero-advancement/src/ModeRules.h"
#include <cassert>
using namespace HeroAdvancement;
int main(){
 RegisterMode(Mode::Hybrid);assert(CanChooseInitial(Mode::ClassPlus,1,false));assert(!CanChooseInitial(Mode::Hero,1,false));assert(!CanChooseInitial(Mode::ClassPlus,2,false));
 Character c{Mode::ClassPlus,10,1,0};Budget b;Catalog cat;
 cat[1]={1,1,5,0,1,0,1,0,0,0,true};cat[2]={2,2,1,0,1,2,0,2,2,0,false};
 assert(Validate(c,cat,{{1,1}},b).empty());assert(!Validate(c,cat,{{1,2}},b).empty());assert(!Validate(c,cat,{{2,1}},b).empty());
 cat[1].tier=1;assert(!Validate(c,cat,{{1,1}},b).empty());c.level=15;assert(Validate(c,cat,{{1,1}},b).empty());
 assert(CanChooseHybrid(c,2,false));assert(!CanChooseHybrid(c,999,false));assert(!CanChooseHybrid(c,1,false));assert(!CanChooseHybrid(c,2,true));
 c.mode=Mode::Hybrid;c.secondClass=2;assert(Validate(c,cat,{{2,1}},b).empty());c.secondClass=3;assert(!Validate(c,cat,{{2,1}},b).empty());
 c.mode=Mode::Hero;c.level=10;assert(!Validate(c,cat,{{1,1}},b).empty());c.level=15;assert(Validate(c,cat,{{1,1}},b).empty());
 cat[3]={3,2,1,0,1,2,0,3,2,0,false};cat[2].mastery=3;assert(!Validate(c,cat,{{2,1}},b).empty());assert(Validate(c,cat,{{2,1},{3,1}},b).empty());assert(b.ability==2 && b.gems[3]==2 && b.gems[2]==0);
 assert(!Validate(c,cat,{{999,1}},b).empty());assert(!Validate(c,cat,{{1,99}},b).empty());
}
