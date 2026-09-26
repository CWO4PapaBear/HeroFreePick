from pathlib import Path
import json,os,subprocess,struct
import Prepare as P
HERE=P.HERE
base=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path']
before=(base/'Spell.dbc').read_bytes();after=(HERE/'candidate/Spell.dbc').read_bytes()
old,_=P.read_dbc(before);new,_=P.read_dbc(after)
old={r[0]:r for r in old};new={r[0]:r for r in new}
assert new.keys()-old.keys()=={P.AURA} and not old.keys()-new.keys()
for id,row in old.items():
    delta=[i for i,(a,b) in enumerate(zip(row,new[id])) if a!=b]
    assert delta==([211] if id in P.RANKS else []),(id,delta)
# Existing effects retain exactly the same affected-spell relationships.
for source in old.values():
    if source[208]!=4:continue
    for e in range(3):
        mask=source[122+3*e:125+3*e]
        for id in P.RANKS:
            assert any(a&b for a,b in zip(mask,old[id][209:212]))==any(a&b for a,b in zip(mask,new[id][209:212]))
assert {id for id,r in new.items() if r[208]==4 and r[211]&P.FLAG}==P.RANKS
aura=new[P.AURA]
assert aura[71:74]==[6,0,0] and aura[95:98]==[275,0,0]
assert aura[116:119]==[0,0,0] and aura[34]==0 # No proc/trigger/combat permission.
assert not aura[4]&0x40 and aura[40]==21 # Cast-only passive auras are not sent to clients.
test=HERE/'local-tests';test.mkdir(exist_ok=True)
(test/'Player.h').write_text('''#pragma once
#include <cstdint>
using uint32=std::uint32_t;
struct Guid {unsigned value; unsigned GetCounter()const{return value;}};
struct Player {unsigned id=1,form=0,casts=0;bool world=true,alive=true,aura=false;
 Guid GetGUID()const{return {id};} unsigned GetShapeshiftForm()const{return form;}
 bool IsInWorld()const{return world;} bool IsAlive()const{return alive;}
 bool HasAura(unsigned)const{return aura;} void RemoveAurasDueToSpell(unsigned){aura=false;}
 void CastSpell(Player*,unsigned,bool){aura=true;++casts;}
};
''')
(test/'SpellInfo.h').write_text('''#pragma once
enum {SPELLFAMILY_WARRIOR=4,SPELL_ATTR2_ALLOW_WHILE_NOT_SHAPESHIFTED=0x80000,SPELL_EFFECT_APPLY_AURA=6,SPELL_AURA_MOD_IGNORE_SHAPESHIFT=275};
struct Effect {unsigned Effect=0,ApplyAuraName=0,SpellClassMask[3]={};};
struct SpellInfo {unsigned SpellFamilyName=4,Stances=0,AttributesEx2=0,SpellFamilyFlags[3]={};struct Effect Effects[3];};
'''.replace('struct Effect {','struct TestEffect {').replace('struct Effect Effects','TestEffect Effects'))
(test/'SpellMgr.h').write_text('''#pragma once
#include "SpellInfo.h"
#include <map>
struct Manager {std::map<unsigned,SpellInfo> spells;SpellInfo const* GetSpellInfo(unsigned id){auto it=spells.find(id);return it==spells.end()?nullptr:&it->second;}};
inline Manager manager;inline Manager* sSpellMgr=&manager;
''')
(test/'Log.h').write_text('#pragma once\n#define LOG_ERROR(...) ((void)0)\n#define LOG_INFO(...) ((void)0)\n')
(test/'test.cpp').write_text('''#include <cassert>
#include "../WarriorStances.h"
int main(){using namespace HeroWarriorStances;
 Player p;Load();Publish(&p,true);assert(!p.aura);
 auto &a=manager.spells[Aura];a.Stances=0x70000;a.AttributesEx2=0x80000;a.Effects[0].Effect=6;a.Effects[0].ApplyAuraName=275;a.Effects[0].SpellClassMask[2]=Flag;
 for(auto id:Ranks){auto &s=manager.spells[id];s.Stances=(id==100||id==6178||id==11578)?0x10000:0x30000;s.SpellFamilyFlags[2]=Flag;}
 Load();assert(ready);
 for(bool custom:{false,true})for(unsigned form:{0u,17u,18u,19u,1u,5u,8u,22u}){
   p.form=form;Publish(&p,custom);assert(p.aura==(custom&&AllowedForm(form)));
 }
 p.form=0;Publish(&p,true);auto n=p.casts;Sync(&p);assert(p.casts==n);
 p.alive=false;p.aura=false;Sync(&p);assert(!p.aura);p.alive=true;Sync(&p);assert(p.aura);
 Publish(&p,false);assert(!p.aura);Publish(&p,true);assert(p.aura);Forget(&p);Sync(&p);assert(!p.aura);
 p.world=false;Publish(&p,true);assert(!p.aura);p.world=true;Sync(&p);assert(p.aura);
 manager.spells[100].Stances=0;Load();Sync(&p);assert(!ready&&!p.aura);
}
''')
root=HERE.parents[1]
compiler=Path(os.environ.get('BEAR_CAVE_ZIG',str(root/'work/login/compiler/ziglang/zig.exe')))
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(root/'work/zig-cache'))
subprocess.run([str(compiler),'c++','-std=c++17','-Wall','-Wextra','-Werror','-I',str(test),str(test/'test.cpp'),'-o',str(test/'test.exe')],check=True,env=env)
subprocess.run([str(test/'test.exe')],check=True)
print('PASS: exact 12-rank data delta; existing mask relationships; isolated stance-only aura; compiled module lifecycle/form/readiness tests. Full core build and in-game client behavior remain unverified.')
