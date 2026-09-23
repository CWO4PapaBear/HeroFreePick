from pathlib import Path
import importlib.util,json,sys
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'work/regalia/libs'))
from lupa.lua51 import LuaRuntime
spec=importlib.util.spec_from_file_location('resolver',HERE/'Resolve.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
db,tables,_=r.load()
serpent=r.resolve(db,tables,1978)
assert not serpent['unresolved'] and 'over 15 sec' in serpent['text']
assert r.resolve(db,tables,54037)['text'].find('reduced by 2 sec')>=0
assert '3 targets' in r.resolve(db,tables,2643)['text']
assert '10 rage' in r.resolve(db,tables,29834)['text']
assert '300%' in r.resolve(db,tables,6789)['text']
assert r.resolve(db,tables,8936)['unresolved'] # missing named multiplier stays explicit
for invalid in ('__import__("os")','AP.real','AP**2','[1]','unknown+2'):
    try:r.expression_tree(invalid)
    except (ValueError,SyntaxError):pass
    else:raise AssertionError('Unsafe expression accepted')
lua=LuaRuntime()
for path in (HERE/'payload').rglob('*.lua'):lua.execute('assert(loadstring(...))',path.read_text(encoding='utf-8'))
lua.execute('HeroFreePick={};testAP=0;testRAP=0;function UnitAttackPower()return testAP,0,0 end;function UnitRangedAttackPower()return testRAP,0,0 end;function UnitStat()return 10,10 end')
for name in ('ResolvedServerTooltips.lua','ServerTooltipValues.lua','AscensionTalentOverlay.lua'):
    lua.execute((HERE/'payload/HeroFreePick'/name).read_text(encoding='utf-8'))
lua.execute(r'''
local A=HeroFreePick
local text,meta=A.ResolveServerTooltip(1978)
assert(text:find('20 Nature damage over 15 sec',1,true)and #meta.unresolved==0)
testRAP=500;text=A.ResolveServerTooltip(1978)
assert(text:find('120 Nature damage over 15 sec',1,true))
testRAP=1000;text=A.ResolveServerTooltip(1978)
assert(text:find('220 Nature damage over 15 sec',1,true))
testAP=100;text=A.ResolveServerTooltip(703)
assert(text:find('162 damage over 18 sec',1,true))
text,meta=A.ResolveServerTooltip(8936)
assert(text:sub(1,10)=='|cffffff00'and #meta.unresolved>0 and text:find('[value pending]',1,true))
UnitRangedAttackPower=nil;text,meta=A.ResolveServerTooltip(1978)
assert(text:find('[value pending]',1,true)and #meta.unresolved>0)
function UnitRangedAttackPower()return 500,50,-20 end
text=A.ResolveServerTooltip(1978);assert(text:find('126 Nature',1,true))
A.mode='Hybrid'
local e={id=1,spells={1978}}
text,meta=A.AscensionTalentDescription(e,1)
assert(text:find('126 Nature',1,true)and meta.serverDefinition)
e.serverPending=true;text=A.AscensionTalentDescription(e,1)
assert(text:sub(1,10)=='|cffffff00')
A.mode='Classic';assert(A.AscensionTalentDescription(e,1)==nil)
for id,entry in pairs(HeroResolvedServerTooltips)do
 text,meta=A.ResolveServerTooltip(id)
 assert(not text:find('HFVALUE',1,true)and not text:find('HFUNKNOWN',1,true))
 if #entry.unresolved>0 then assert(text:sub(1,10)=='|cffffff00')end
end
''')
report=json.loads((HERE/'audit.json').read_text())
assert report['affected']==report['fullyResolved']+report['stillUnresolved']
print('PASS: Lua 5.1, server field resolution, 15-second totals, live AP/RAP changes, signed cooldowns, cross-spell ticks, safe arithmetic, unresolved highlighting, implementation warnings and Classic isolation.')
