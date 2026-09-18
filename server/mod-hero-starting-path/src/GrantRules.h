#pragma once
#include <functional>
#include <set>
#include <vector>
namespace HeroGrant {
struct Node { bool valid=false,mixed=false; std::vector<unsigned> learns; };
using NodeLookup=std::function<Node(unsigned)>;
inline bool Expand(unsigned id,NodeLookup const& lookup,std::set<unsigned>& spells,std::set<unsigned>& path){
 if(!id||path.size()>=32||!path.insert(id).second)return false;
 auto node=lookup(id);if(!node.valid||node.mixed)return false;
 if(node.learns.empty())spells.insert(id);
 else for(auto child:node.learns)if(!Expand(child,lookup,spells,path))return false;
 path.erase(id);return true;
}
inline bool SelfTest(){
 NodeLookup lookup=[](unsigned id){
  if(id==49377)return Node{true,false,{16979,49376}};
  if(id==65139)return Node{true,false,{33891,5420}};
  if(id==33917)return Node{true,false,{33878,33876}};
  if(id==59672)return Node{true,false,{47241,50581,59673}};
  if(id==1)return Node{true,false,{1}};
  if(id==2)return Node{true,true,{5487}};
  if(id==3)return Node{true,false,{0}};
  if(id==4)return Node{};
  if(id==5)return Node{true,false,{49377,5487}};
  return Node{true,false,{}};
 };
 std::set<unsigned> result,path;
 if(!Expand(49377,lookup,result,path)||result!=std::set<unsigned>{16979,49376})return false;
 if(!Expand(5487,lookup,result,path)||!result.count(5487))return false;
 for(auto id:{1u,2u,3u,4u}){result.clear();path.clear();if(Expand(id,lookup,result,path))return false;}
 result.clear();path.clear();
 return Expand(5,lookup,result,path)&&result==std::set<unsigned>{16979,49376,5487}&&path.empty();
}
}
