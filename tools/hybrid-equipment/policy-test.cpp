int main(){
using namespace HeroEquipment;
for(unsigned a=1;a<=11;++a)for(unsigned b=1;b<=11;++b){if(!Class(a)||!Class(b)||a==b)continue;
assert(Mask(3,a,b)==Mask(3,b,a));assert(Mask(1,a,b)==Bit(a));assert(Mask(2,a,b)==Bit(a));
for(unsigned level:{10u,19u,20u,39u,40u,80u})for(auto const& p:Proficiencies){
assert(Available(p,Mask(3,a,b),level)==(Available(p,Bit(a),level)||Available(p,Bit(b),level)));
unsigned c=SkillClass(Mask(3,a,b),a,p.skill);assert(c==a||c==b);
}}
assert(!Available(*Skill(293),Mask(3,8,1),39));assert(Available(*Skill(293),Mask(3,8,1),40));
assert(!Available(*Skill(413),Mask(3,8,3),39));assert(Available(*Skill(413),Mask(3,8,3),40));
assert(Available(*Skill(413),Mask(3,8,1),10));assert(!Available(*Skill(118),Mask(3,8,7),80));
assert(Available(*Skill(118),Mask(3,8,4),10));assert(!Available(*Skill(118),Mask(3,8,1),19));
assert(!Skill(164));assert(SkillClass(Mask(3,8,1),8,164)==8); // professions unchanged
Player p;HeroBuild::Build keep;KeepHybridEquipment(&p,keep);assert(keep.count(9116)&&keep.count(5009)&&!keep.count(750));
p.spells=keep;p.skills[43]={37,50};assert(VerifyHybridEquipment(&p));assert(p.skills[43].first==37);assert(p.skills[44].first==1);
p.level=40;KeepHybridEquipment(&p,keep);p.spells=keep;assert(keep.count(750)&&VerifyHybridEquipment(&p));assert(p.skills[43].first==37&&p.skills[43].second==200);
p.mode=1;keep.clear();KeepHybridEquipment(&p,keep);assert(keep.empty());
}
