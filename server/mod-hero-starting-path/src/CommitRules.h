#pragma once
#include "GeneratedCatalog.h"
#include <array>
#include <set>
#include <string>
#include <algorithm>
namespace HeroBuild {
using Build=std::set<unsigned>;
inline Entry const* Find(unsigned id){for(auto const& e:Catalog())if(e.id==id)return &e;return nullptr;}
inline bool Parse(std::string const& text,Build& out){
 out.clear();if(text=="-")return true;if(text.empty()||text.size()>6144)return false;
 unsigned n=0,digits=0;
 for(char c:text+","){
  if(c==','){if(!digits||!n||!out.insert(n).second||out.size()>512)return false;n=0;digits=0;}
  else {if(c<'0'||c>'9'||++digits>9)return false;n=n*10+unsigned(c-'0');}
 }return true;
}
inline std::string Encode(Build const& roots){std::string s;for(auto id:roots){if(!s.empty())s+=',';s+=std::to_string(id);}return s.empty()?"-":s;}
inline std::vector<std::string> Chunks(Build const& roots){
 std::vector<std::string> out;std::string part;
 for(auto id:roots){auto s=std::to_string(id);if(part.size()+s.size()+1>140){out.push_back(part);part.clear();}if(!part.empty())part+=',';part+=s;}
 if(!part.empty())out.push_back(part);if(out.empty())out.push_back("-");return out;
}
inline std::string Validate(unsigned klass,unsigned level,Build const& roots){
 if(level<1)return "LEVEL";unsigned ap=0;std::array<unsigned,5> gems{};
 for(auto id:roots){auto e=Find(id);if(!e||e->parent)return "UNSUPPORTED";if(e->klass!=klass)return "CLASS";if(e->level>level)return "LEVEL";ap+=e->ap;gems[e->rarity]+=e->gems;}
 if(ap>std::max(9u,level))return "AP";constexpr unsigned caps[]={0,11,16,13,7};
 for(unsigned i=1;i<5;++i)if(gems[i]>caps[i])return "RARITY";return {};
}
inline Build Entries(Build const& roots,unsigned level){
 auto out=roots;for(auto const& e:Catalog())if(e.parent&&roots.count(e.parent)&&level>=e.level)out.insert(e.id);return out;
}
inline bool SelfTest(){
 Build b;if(!Parse("18,21092155",b)||!Validate(8,1,b).empty()||!Entries(b,1).count(21))return false;
 if(Validate(1,1,b)!="CLASS"||Validate(8,0,b)!="LEVEL"||Validate(8,1,Build{21})!="UNSUPPORTED")return false;
 Build overAP;unsigned ap=0;for(auto const& e:Catalog())if(e.klass==8&&!e.parent){overAP.insert(e.id);ap+=e.ap;}
 if(ap<=80||Validate(8,80,overAP)!="AP")return false;
 for(auto bad:{"",",18","18,","18,18","18;999","18:2","-1","9999999999"})if(Parse(bad,b))return false;
 for(auto const& e:Catalog()){
  if(e.rarity>4||!e.level||!e.klass||e.ap>80||e.gems>20)return false;
  if(e.parent){auto p=Find(e.parent);if(!p||!p->group||e.ap||e.gems)return false;}
  else if(!Validate(e.klass,std::max(80u,e.level),Build{e.id}).empty())return false;
 }
 Build many;for(auto const& e:Catalog())if(!e.parent)many.insert(e.id);
 Build assembled;for(auto const& chunk:Chunks(many)){Build part;if(chunk.size()>140||!Parse(chunk,part))return false;assembled.insert(part.begin(),part.end());}
 return assembled==many && Parse("-",b)&&b.empty();
}
}
