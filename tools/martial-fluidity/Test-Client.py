from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'work/regalia/libs'))
from lupa.lua51 import LuaRuntime
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''HeroFreePick={mode='Hybrid',AscensionTalentDescription=function()return 'stock description'end,AddAscensionTalentNotes=function()return 'stock notes'end}
native=2;GetComboPoints=function(unit,target)return native end
CreateFrame=function()return {RegisterEvent=function()end,SetScript=function(self,event,fn)self[event]=fn end}end
ChatFrame_AddMessageEventFilter=function(event,fn)filter=fn end
GameTooltip={HookScript=function()end}
targetExists=false;UnitExists=function(unit)return unit=='target'and targetExists end
PlayerFrame={unit='player'}
ComboFrame={shown=false,Hide=function(self)self.shown=false end,HookScript=function(self,_,fn)self.onshow=fn end,Show=function(self)self.shown=true;if self.onshow then self.onshow()end end}
ComboFrame_Update=function()if GetComboPoints('player','target')>0 then ComboFrame:Show()else ComboFrame:Hide()end end
hooksecurefunc=function(name,fn)local old=_G[name];_G[name]=function(...)old(...);fn(...)end end
''')
lua.execute((HERE/'payload/HeroFreePick/MartialFluidity.lua').read_text())
lua.execute('''local A=HeroFreePick;local e={name='Vigor',spells={14983}}
assert(A.DisplayTalentName(e)=='Martial Fluidity')
assert(A.AscensionTalentDescription(e):find('switching targets.\n\nIncreases',1,true))
assert(GetComboPoints('player','target')==2)
assert(filter(nil,nil,'HF_COMBO 1 4'));assert(GetComboPoints('player',nil)==4);assert(GetComboPoints('vehicle','target')==2);ComboFrame_Update();assert(not ComboFrame.shown);assert(GetComboPoints('player',nil)==4);targetExists=true;ComboFrame_Update();assert(ComboFrame.shown);targetExists=false;ComboFrame_Update();assert(not ComboFrame.shown);assert(GetComboPoints('player',nil)==4)
assert(not filter(nil,nil,'HF_COMBO 1 99'));assert(GetComboPoints('player','target')==4)
A.mode='Classic';assert(A.DisplayTalentName(e)=='Vigor');assert(A.AscensionTalentDescription(e)=='stock description');assert(GetComboPoints('player','target')==2)
A.mode='Hybrid';assert(filter(nil,nil,'HF_COMBO 0 0'));assert(GetComboPoints('player','target')==2);ComboFrame_Update();assert(ComboFrame.shown)
'''.replace("targets.\n\nIncreases","targets.\\n\\nIncreases"))
for p in (HERE/'payload').rglob('*.lua'):
    lua.execute('assert(loadstring(...))',p.read_text())
print('PASS: Lua 5.1 syntax, talent presentation and Classic isolation, server-authoritative shared count without target, vehicle fallback, invalid count rejection and removal.')
