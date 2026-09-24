from pathlib import Path
from lupa.lua51 import LuaRuntime
s=(Path(__file__).parent/'payload/HeroFreePick/HeroFreePick.lua').read_text(encoding='utf-8')
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('assert(loadstring(...))',s)
lua.execute("""
function frame()return {shown=true,Hide=function(self)local was=self.shown;self.shown=false;if was and self.OnHide then self.OnHide()end end,Show=function(self)self.shown=true end,IsShown=function(self)return self.shown end,SetScript=function(self,k,v)self[k]=v end,SetPoint=function()end}end
window=frame();f=window;dialog=frame();box=frame();title={SetText=function()end};GameTooltip=frame();HeroProgressionChoice=frame()
CreateFrame=function()return frame()end;button=function()return frame()end;hideMasteryTooltip=function()end
combat=false;InCombatLockdown=function()return combat end
A={ValidatePrimaryStatSelection=function()return false,'Choose a stat'end,HasPendingChanges=function()return true end,ShowPointWarning=function()error('Combat must not prompt')end,BeginPreparation=function()end,Refresh=function()end,FitWindow=function()end,AlertSoundsEnabled=function()return false end}
""")
a=s.index('local closing=false');b=s.index('A.ClassicCommitResult=',a)
lua.execute(s[a:b])
lua.execute(next(x for x in s.splitlines() if x.startswith('function A.Toggle()')))
lua.execute(next(x for x in s.splitlines() if x.startswith("f:SetScript('OnEvent',function(self,event,key,state)")))
lua.execute("""
for _,mode in ipairs({'Classic','ClassPlus','Hybrid','Hero'})do
 A.mode=mode;HeroFreePickPlans={previewLearned={[14983]=1},primaryStat='Agility',pendingBaseline={original=true}}
 local saved=HeroFreePickPlans;local baseline=saved.pendingBaseline
 window:Show();dialog:Show();HeroProgressionChoice:Show();combat=true
 f.OnEvent(f,'PLAYER_REGEN_DISABLED')
 assert(not window.shown and not dialog.shown and not HeroProgressionChoice.shown)
 assert(saved==HeroFreePickPlans and saved.pendingBaseline==baseline and saved.previewLearned[14983]==1 and saved.primaryStat=='Agility')
 A.Toggle();A.ShowPendingReview();assert(not window.shown and not dialog.shown)
 window:Show();window:Hide();assert(not window.shown,'OnHide must not restore combat UI')
 combat=false;assert(not window.shown);A.Toggle();assert(window.shown and saved.pendingBaseline==baseline)
end
""")
print('PASS: actual PTR combat event, all modes, primary-stat bypass, overlays, draft/baseline preservation, blocked combat reopen and post-combat resume.')
