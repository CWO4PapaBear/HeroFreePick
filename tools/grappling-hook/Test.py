"""Offline data preservation, acquisition policy and client overlay regression checks."""
from pathlib import Path
import json,os,struct,subprocess,sys
import Prepare as P
HERE=P.HERE;ROOT=HERE.parents[1]
base=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path']
old,_=P.dbc((base/'Spell.dbc').read_bytes());new,_=P.dbc((HERE/'candidate/Spell.dbc').read_bytes())
a={r[0]:r for r in old};b={r[0]:r for r in new}
assert b.keys()-a.keys()==P.IDS and not a.keys()-b.keys()
assert all(b[id]==r for id,r in a.items()),'Unrelated server record changed'
assert b[760056][29]==35000 and b[760056][16]==64 and b[760056][86]==28
assert b[760094][29]==0 and b[760094][86]==6
assert b[760095][95]==26 and b[760096][95]==4
assert all(r[5]&32 for id,r in b.items() if id in P.IDS),'Stealth flag missing'
assert all(not any(r[116:119]) for id,r in b.items() if id in P.IDS),'Unreviewed trigger'
for id in P.IDS:
    assert all(x<165 for x in b[id][71:74]) and all(x<317 for x in b[id][95:98])
def table(name):
    raw=(base/(name+'.dbc')).read_bytes();magic,n,f,z,ns=struct.unpack_from('<4s4I',raw)
    assert magic==b'WDBC'
    return {r[0]:r for r in struct.iter_unpack('<'+str(f)+'I',raw[20:20+n*z])}
d=table('SpellDuration');assert d[b[760096][40]][1]==3000 and d[b[760095][40]][1]==1000
r=table('SpellRange')
def fl(x):return struct.unpack('<f',struct.pack('<I',x))[0]
assert fl(r[b[760056][46]][3])==30 and fl(r[b[760094][46]][3])==10

# Compile and execute the actual server acquisition policy, not a Python rewrite.
test=HERE/'local-tests';test.mkdir(exist_ok=True)
source='''#include <cassert>
#include "CommitRules.h"
#include "HeroGrapplingHooks.h"
int main(){
 using namespace HeroBuild;Build root{26001633};
 assert(SelfTest());
 assert(Validate(4,28,root,1).empty());
 assert(Validate(4,27,root,1).find("LEVEL")==0);
 assert(Validate(7,28,root,1).find("CLASS")==0);
 assert(Validate(7,28,root,1,4).empty());
 assert(Validate(7,28,root,1,0,true).empty());
 assert(Validate(7,27,root,1,0,true).find("LEVEL")==0);
 auto e=Find(26001633);assert(e && e->ap==3 && e->rarity==4 && e->gems==2);
 assert(e->spells==std::vector<unsigned>{760056});
 for(unsigned id:{760056u,760094u,100u}){
  assert(HeroGrapplingHooks::Cast(nullptr,id)==id);
  assert(HeroGrapplingHooks::Action(nullptr,id)==id);
 }
}
'''
(test/'policy.cpp').write_text(source)
# CommitRules resolves its adjacent catalog, so stage an exact policy fixture.
for name in ('CommitRules.h','HybridPolicy.h'):
    (test/name).write_bytes((base/'modules/mod-hero-starting-path/src'/name).read_bytes())
(test/'GeneratedCatalog.h').write_bytes((HERE/'candidate/modules/mod-hero-starting-path/src/GeneratedCatalog.h').read_bytes())
compiler=ROOT/'work/login/compiler/ziglang/zig.exe'
subprocess.run([str(compiler),'c++','-std=c++17','-I',str(HERE),str(test/'policy.cpp'),'-o',str(test/'policy.exe')],check=True,
               env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(ROOT/'work/zig-cache')))
subprocess.run([str(test/'policy.exe')],check=True)

sys.path.insert(0,str(ROOT/'work/regalia/libs'))
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute('HeroFreePick={byID={[26001633]={serverPending=true}}}')
catalog=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test/Interface/AddOns/HeroClassPlusCommitTest/Catalog.lua')
lua.execute(catalog.read_text(encoding='utf8'))
lua.execute('oldVersion=HeroCommitCatalog.version; oldCount=0; oldEntries={}; for k,v in pairs(HeroCommitCatalog.entries) do oldCount=oldCount+1; oldEntries[k]=v end')
lua.execute((HERE/'GrapplingHook.lua').read_text())
lua.execute('''assert(HeroCommitCatalog.version==oldVersion)
for k,v in pairs(oldEntries) do assert(HeroCommitCatalog.entries[k]==v) end
assert(HeroCommitCatalog.entries[26001633].tokens[1]==26001633)
assert(HeroCommitCatalog.tokens[26001633].id==26001633)
assert(HeroCommitCatalog.excluded[26001633]==nil)
assert(not HeroFreePick.byID[26001633].serverPending)
assert(HeroCommitCatalog.entries[26001633].levels.Draenei==28)''')
print('PASS: unrelated DBC records preserved; native targets/timings; compiled acquisition policy and optional hooks; Lua 5.1 additive overlay.')
print('Full server build, private startup, action-bar behavior and movement/visual acceptance are separate checks.')
