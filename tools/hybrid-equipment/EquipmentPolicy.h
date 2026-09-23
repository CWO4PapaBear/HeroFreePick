#pragma once
namespace HeroEquipment {
struct Proficiency { unsigned spell, skill, classes; bool weapon; };
// Stock SkillLineAbility masks; thrown uses SkillRaceClassInfo (13).
constexpr Proficiency Proficiencies[] = {
 {201,43,431,true},{196,44,111,true},{264,45,13,true},{266,46,13,true},
 {198,54,1147,true},{202,55,39,true},{227,136,1493,true},{199,160,1123,true},
 {197,172,103,true},{1180,173,1501,true},{2567,176,13,true},{5011,226,13,true},
 {5009,228,400,true},{200,229,1063,true},{15590,473,1101,true},
 {750,293,35,false},{8737,413,103,false},{9077,414,1135,false},
 {9078,415,1535,false},{9116,433,67,false}, {674,118,45,false}
};
inline bool Class(unsigned c){return c>=1&&c<=11&&c!=10;}
inline unsigned Bit(unsigned c){return Class(c)?1u<<(c-1):0;}
inline unsigned Mask(unsigned mode,unsigned own,unsigned second){
 return Bit(own)|((mode>=3&&mode<=4&&Class(second)&&own!=second)?Bit(second):0);
}
inline unsigned RequiredLevel(Proficiency const& p,unsigned c){
 if(p.skill==293)return 40; // custom level-one DK progression also withholds starter plate
 if(p.skill==229)return 20;
 if(p.skill==413)return c==3||c==7?40:1;
 if(p.skill==118)return c==6?1:c==4?10:20;
 return 1;
}
inline bool Available(Proficiency const& p,unsigned mask,unsigned level){
 for(unsigned c=1;c<=11;++c)if((mask&p.classes&Bit(c))&&level>=RequiredLevel(p,c))return true;
 return false;
}
inline Proficiency const* Skill(unsigned id){for(auto const& p:Proficiencies)if(p.skill==id)return &p;return nullptr;}
inline unsigned SkillClass(unsigned mask,unsigned own,unsigned skill){
 auto p=Skill(skill);if(!p||(p->classes&Bit(own)))return own;
 for(unsigned c=1;c<=11;++c)if(mask&p->classes&Bit(c))return c;
 return own;
}
}
