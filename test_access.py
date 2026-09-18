from pathlib import Path
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute('''
local function frame()return {shown=false,Enable=function(s)s.enabled=true end,Show=function(s)s.shown=true end,Hide=function(s)s.shown=false end,SetPoint=function(s,...)s.point={...}end,SetScript=function()end,RegisterEvent=function()end}end
CreateFrame=frame;TalentMicroButton=frame();AchievementMicroButton=frame()
HeroFreePick={mode='Classic',Init=function()end,Refresh=function()end}
local level=1
function UpdateTalentButton()if level<10 then TalentMicroButton:Hide();AchievementMicroButton:SetPoint('BOTTOMLEFT',TalentMicroButton,'BOTTOMLEFT',0,0)else TalentMicroButton:Show()end end
function hooksecurefunc(t,k,f)
 if type(t)=='string'then f=k;k=t;t=_G end
 local old=t[k];t[k]=function(...)local ret=old(...);f(...);return ret end
end
function TestLevel(n)level=n end
''')
lua.execute((Path(__file__).parent/'HeroFreePick/Access.lua').read_text())
lua.execute('''
assert(not TalentMicroButton.shown)
for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
 HeroFreePick.mode=mode;HeroFreePick.Init()
 assert(TalentMicroButton.shown and TalentMicroButton.enabled)
 UpdateTalentButton();assert(TalentMicroButton.shown)
 assert(AchievementMicroButton.point[3]=='BOTTOMRIGHT')
end
HeroFreePick.mode='Classic';HeroFreePick.Refresh();assert(not TalentMicroButton.shown)
assert(AchievementMicroButton.point[3]=='BOTTOMLEFT')
TestLevel(10);UpdateTalentButton();assert(TalentMicroButton.shown)
''')
print('PASS: level 1 custom access, stock refresh persistence, mode changes, Classic level 1/10, neighboring button spacing')
