from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
# Install lupa (Lua 5.1 runtime) or provide it through PYTHONPATH.
from lupa.lua51 import LuaRuntime
l=LuaRuntime()
assert l.eval('function(s)return loadstring(s)~=nil end')((HERE/'HeroFreePick.lua').read_text())
l.execute('''
A={mode='Hero',class='Mage',spec='Fire',PackageSpellIcons={[1]='package'}}
HeroFreePickPlans={pending='unchanged'}
HeroFreePickCatalog={{spells={1},referenceIcon='custom'},{spells={1},referenceIcon='custom'}}
nativeBackgrounds={a='MageFire',b='MageFire'}
function icon(e)return 'stock'end
combat=false
function InCombatLockdown()return combat end
function CreateFrame()
 local f={scripts={},paths={}};worker=f
 setmetatable(f,{__index=function()return function()end end})
 function f:SetScript(k,v)self.scripts[k]=v end
 function f:CreateTexture()
  local t={};function t:SetAllPoints()end
  function t:SetTexture(p)f.paths[#f.paths+1]=p end;return t
 end
 return f
end
''')
l.execute((HERE/'Preload.lua').read_text())
l.execute('''
assert(A.MenuPreloadStatus.loaded==0)
worker.scripts.OnEvent(worker,'PLAYER_ENTERING_WORLD')
worker.scripts.OnUpdate(worker,.1);assert(#worker.paths==0)
combat=true;worker.scripts.OnUpdate(worker,1);assert(#worker.paths==0)
combat=false;worker.scripts.OnUpdate(worker,1);assert(#worker.paths==2)
for i=1,50 do if worker.scripts.OnUpdate then worker.scripts.OnUpdate(worker,.02)end end
assert(A.MenuPreloadStatus.complete and not A.MenuPreloadStatus.error)
assert(#worker.paths==7) -- four unique background pieces and three icon variants
assert(not worker.scripts.OnUpdate)
worker.scripts.OnEvent(worker,'PLAYER_ENTERING_WORLD');assert(#worker.paths==7)
assert(A.mode=='Hero'and A.class=='Mage'and A.spec=='Fire'and HeroFreePickPlans.pending=='unchanged')
''')
print('PASS: Lua 5.1 syntax; delayed start, bounded work, combat pause, deduplication, completion, no mode/view/draft changes.')
