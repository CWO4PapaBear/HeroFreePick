#include "../mod-hero-starting-path/src/StartingSpells.h"
#include <cassert>
int main(){for(auto name:{"Alice","Hfstartmage","Renamed"})for(unsigned c:{1,2,3,4,5,6,7,8,9,11}){unsigned l=c==6?55:1;assert(HeroStartingPath::Eligible(name,c,l));assert(!HeroStartingPath::Eligible(name,c,l+1));assert(HeroStartingPath::CanChoose(l,2,c));assert(!HeroStartingPath::CanChoose(l+1,2,c));assert(!HeroStartingPath::CanChoose(l,3,c));}assert(!HeroStartingPath::Eligible("Alice",10,1));}
