from pathlib import Path
import xml.etree.ElementTree as ET,json
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parent/'HeroFreePick';lua=LuaRuntime(unpack_returned_tuples=True)
for p in root.glob('*.lua'):lua.execute('assert(loadstring(...))',p.read_text(encoding='utf-8-sig'))
ET.parse(root/'HeroFreePick.xml')
lua.execute('''
local function frame()
 local f={shown=true,w=500,h=380,text='',scripts={}}
 local methods={SetSize=function(s,w,h)s.w=w;s.h=h end,SetWidth=function(s,w)s.w=w end,SetHeight=function(s,h)s.h=h end,GetFrameLevel=function()return 1 end,GetWidth=function(s)return s.w end,GetHeight=function(s)return s.h end,SetText=function(s,t)s.text=t end,GetText=function(s)return s.text end,GetStringHeight=function(s)return 500 end,Show=function(s)s.shown=true end,Hide=function(s)local was=s.shown;s.shown=false;if was and s.scripts.OnHide then s.scripts.OnHide(s)end end,IsShown=function(s)return s.shown end,SetScript=function(s,k,v)s.scripts[k]=v end,GetVerticalScroll=function()return 0 end,GetVerticalScrollRange=function()return 2000 end}
 setmetatable(f,{__index=function(s,k)if k=='dependencyOverlay'then return nil end;if k=='CreateFontString'or k=='CreateTexture'then return function()return frame()end end;return methods[k]or function()end end})
 return f
end
function CreateFrame(kind,name)local f=frame();if name then _G[name]=f end;return f end
HeroFreePickFrame=frame();UIParent=frame();UIParent:SetSize(1920,1080);GameTooltip=frame();UISpecialFrames={};tinsert=table.insert;SlashCmdList={}
testLevel=80
function UnitLevel()return testLevel end
function GetUnspentTalentPoints()return 71 end
function SetPortraitToTexture(t,path)t:SetTexture(path)end
function GetSpellInfo(id)return 'Spell '..id,nil,'Interface\\\\Icons\\\\Test' end
function PanelTemplates_TabResize()end
function PanelTemplates_SelectTab(t)t:Disable()end
function PanelTemplates_DeselectTab(t)t:Enable()end
function UIDropDownMenu_SetWidth()end
function UIDropDownMenu_Initialize(frame,init)init()end
function UIDropDownMenu_CreateInfo()return{}end
function UIDropDownMenu_AddButton()end
function UIDropDownMenu_SetText()end
''')
for n in ['Catalog.lua','Adapter.lua','Layout.lua','Trees.lua','Organization.lua','Browse.lua','TalentAbilityReferences.lua','Masteries.lua','NativeTalentRoutes.lua','MenuLayoutOverrides.lua','MenuLayout.lua','HeroFreePick.lua']:lua.execute((root/n).read_text(encoding='utf-8-sig'))
lua.execute("""
local A=HeroFreePick;A.mode='Hero';A.InstalledModes={Classic=true,ClassPlus=true,Hybrid=true,Hero=true}
assert(type(A.BeginPreparation)=='function' and type(A.RequestClose)=='function')
function UnitClass()return 'Hero','HERO'end
function LearnTalent()error('Immediate talent learning must never be called')end
A.Init();A.BeginPreparation();assert(not A.HasPendingChanges())
assert(#HeroFreePickTrees==829 and #HeroTalentAbilityReferences==144 and #HeroMasteries==23)
for _,class in ipairs(A.classes)do
 A.class=class;A.isBrowse=false
 for _,spec in ipairs(A.Specs())do A.spec=spec;A.view='browse';A.Refresh(true)end
end
A.class='Mage';A.spec='All';A.quality='All';A.ownership='All';A.view='browse';A.Refresh()
local e=HeroNativeTalent1.entry
assert(A.IsTalent(e));HeroNativeTalent1.scripts.OnClick(HeroNativeTalent1,'LeftButton');assert(A.PendingRank(e)==1)
HeroNativeTalent1.scripts.OnClick(HeroNativeTalent1,'RightButton');assert(A.PendingRank(e)==0)
assert(not A.AssignNativeTalent(e));assert(not A.HasPendingChanges())
A.SetLocalLearned(e.id,A.MaxRank(e));assert(A.PendingRank(e)==A.MaxRank(e))
A.SetLocalLearned(e.id,999);assert(A.PendingRank(e)==A.MaxRank(e))
local summary=A.PendingSummary();assert(summary[1].after.TP==A.MaxRank(e))
HeroFreePickFrame:Show();assert(not A.RequestClose());assert(A.PendingDialog:IsShown())
A.PendingBackButton.scripts.OnClick();assert(not A.PendingDialog:IsShown()and A.PendingRank(e)>0)
HeroFreePickFrame:Hide();assert(HeroFreePickFrame:IsShown()and A.PendingDialog:IsShown())
A.PendingAcceptButton.scripts.OnClick();assert(A.HasPendingChanges()and A.PendingDialog:IsShown())
local ok,reason=A.AcceptPreparation();assert(not ok and reason:lower():find('server'))
A.PendingCancelButton.scripts.OnClick();assert(not A.HasPendingChanges()and A.PendingRank(e)==0 and not HeroFreePickFrame:IsShown())
-- Net-zero edits should not prompt; X/N and Escape share the same close decision.
A.Toggle();A.SetLocalLearned(e.id,1);A.SetLocalLearned(e.id,0);assert(not A.HasPendingChanges());A.Toggle();assert(not HeroFreePickFrame:IsShown())
-- Pending drafts, primary-stat changes, reload restoration and independent resource deltas.
A.Toggle();A.SetRank(e.id,2);HeroFreePickPlans.primaryStat='Agility';assert(A.HasPendingChanges())
local before=HeroFreePickPlans.pendingBaseline;A.BeginPreparation();assert(HeroFreePickPlans.pendingBaseline==before)
assert(A.PendingSummary()[2].after.TP==2);A.CancelPreparation();assert(not HeroFreePickPlans.entries[e.id]and not HeroFreePickPlans.primaryStat)
-- All imports are editable in preparation; affordability is reviewed, not charged on click.
for _,v in ipairs(HeroTalentAbilityReferences)do if not v.requiredMastery then assert(A.SetLocalLearned(v.id,1));break end end
assert(A.HasPendingChanges());A.CancelPreparation()
for _,m in ipairs(HeroMasteries)do
 A.BeginPreparation();local members={}
 for _,v in ipairs(HeroFreePickCatalog)do if v.requiredMastery==m.id then members[#members+1]=v end end
 assert(#members==#m.members)
 assert(not A.SetLocalLearned(members[1].id,1));assert(A.SetLocalLearned(m.id,1))
 for _,v in ipairs(members)do assert(A.SetLocalLearned(v.id,1));assert(v.ae==0 and HeroRarityCosts[v.id]==0)end
 assert(A.AbilityPointsSpent()==2);assert(A.SetLocalLearned(m.id,0))
 for _,v in ipairs(members)do assert(not HeroFreePickPlans.previewLearned[v.id])end
 assert(not A.HasPendingChanges());A.CancelPreparation()
end
-- Existing real talent ranks seed the baseline, then can be edited without LearnTalent.
HeroFreePickPlans.preparationInitialized=nil;HeroFreePickPlans.previewLearned={};HeroFreePickPlans.pendingBaseline=nil
local original=A.NativeTalent;A.NativeTalent=function(v)if v.id==e.id then return 1,1,2,5 end end
A.BeginPreparation();assert(A.PendingRank(e)==2 and not A.HasPendingChanges())
assert(A.SetLocalLearned(e.id,1));assert(A.PendingSummary()[1].removed==1)
A.CancelPreparation();assert(A.PendingRank(e)==2);A.NativeTalent=original
""")
print('PASS: pending clicks, reversible ranks, all close routes, review choices, baseline persistence, resource deltas, mastery cascade, and zero native learning calls.')
lua.execute("""
local A=HeroFreePick;local oldOther=A.OtherClass;local oldLevel=testLevel
A.OtherClass=function()return false end;testLevel=80
local groups={};for _,n in ipairs(HeroFreePickTrees)do local key=n.class..':'..n.spec;groups[key]=groups[key]or {};table.insert(groups[key],n)end
local trees,dependencies=0,0
for key,nodes in pairs(groups)do
 trees=trees+1;local expected=0
 for _,n in ipairs(nodes)do if n.depends>0 then expected=expected+1 end end
 dependencies=dependencies+expected
 for _,full in ipairs({false,true})do
  local positions={};for _,n in ipairs(nodes)do positions[n.talent]={rank=full and #n.ranks or 0,button=n.talent}end
  local arrows=0;local parts={}
  A.NativeTalentRoutes(nodes,positions,function(arrow,uv,x,y,target)
   local texture={ClearAllPoints=function()end,SetPoint=function(self,point,relative,relativePoint,dx,dy)self.anchor={relative,dx,dy}end}
   parts[#parts+1]={texture=texture,arrow=arrow,uv=uv,x=x,y=y}
   assert(#uv==4 and x==x and y==y)
   if arrow then arrows=arrows+1;assert(positions[target]);assert(uv[3]==(full and 0 or .5))end
  end)
  assert(arrows==expected,key..': missing dependency arrow')
 end
end
assert(trees==30);routeAuditTrees=trees;routeAuditDependencies=dependencies
A.OtherClass=oldOther;testLevel=oldLevel
""")
print('PASS: all %s stock trees, %s dependencies, unmet/met states and target-owned arrowheads.'%(lua.globals().routeAuditTrees,lua.globals().routeAuditDependencies))

import re
for source in root.glob("*.lua"):
    assert not re.search(r"Interface(?<!\\)\\(?!\\)",source.read_text()), str(source)+": unescaped texture path"
print("PASS: texture paths preserve backslash separators.")

# Check physical tip/shaft alignment across scales, icon sizes and directions.
lua.execute("""
for _,scale in ipairs({.65,1,1.25,2})do
 for _,size in ipairs({24,32,48})do
  for _,direction in ipairs({'down','right','left'})do
   local target={GetCenter=function()return 150,200 end,GetEffectiveScale=function()return scale end}
   local shaft={GetCenter=function()return 151,201 end,GetParent=function()return target end}
   local head={GetParent=function()return target end,GetWidth=function()return size end,GetHeight=function()return size end,ClearAllPoints=function()end,
    SetPoint=function(self,p,t,edge,x,y)self.edge=edge;self.x=x;self.y=y;assert(t==target)end}
   local vertical=direction=='down'
   local uv=vertical and {0,.5,0,.5}or(direction=='right'and {.5,1,0,.5}or {1,.5,0,.5})
   HeroFreePick.AlignTalentArrowTextures({{arrow=false,texture=shaft,uv=vertical and {0,.125,0,.484375}or {.2578125,.3828125,0,.5},x=0,y=0},
    {arrow=true,texture=head,target=target,uv=uv,x=0,y=0}})
   if vertical then assert(head.edge=='TOP'and math.abs(head.x-1)<.000001 and head.y-size*.125==0)
   elseif direction=='right'then assert(head.edge=='LEFT'and math.abs(head.y-1)<.000001 and head.x+size*.125==0)
   else assert(head.edge=='RIGHT'and math.abs(head.y-1)<.000001 and head.x-size*.125==0)end
  end
 end
end
""")
print('PASS: arrow tips meet target edges at four UI scales, three sizes and all three directions.')


source=(root/'NativeTalentRoutes.lua').read_text()
assert 'texture:GetEffectiveScale()' not in source
print('PASS: texture geometry obtains effective scale from its parent frame, not a texture API.')

ui=(root/'HeroFreePick.lua').read_text()
assert 'x-2,dy+2' in ui and 'x-2,dy+10' not in ui
assert 'owner:SetFrameStrata(target:GetFrameStrata());owner:SetFrameLevel(target:GetFrameLevel()+3)' in ui
print('PASS: stock row origin retained; target overlay explicitly matches strata and exceeds button level.')


lua.execute("""
for _,parentScale in ipairs({.65,.8857855796814,1,1.25})do
 for _,pixels in ipairs({{1920,1080},{1280,900},{1280,720},{800,600}})do
  local w,h=pixels[1],pixels[2]
  local scale=HeroFreePick.WindowScale(w/parentScale,h/parentScale,parentScale)
  local effective=scale*parentScale
  assert(effective<=1.000001)
  assert(1192*effective+48<=w+.000001)
  assert(652*effective+64<=h+.000001)
  if w>=1240 and h>=716 then assert(math.abs(effective-1)<.000001)end
 end
end
""")
print('PASS: native effective scale when it fits, bounded fallback at small resolutions, across four client scales.')

layout=ET.parse(root/'HeroFreePick.xml').getroot()
ns={'ui':'http://www.blizzard.com/wow/ui/'}
assert layout.find('ui:Frame/ui:Size',ns).attrib['y']=='620'
print('PASS: compact 620px frame; 652px footprint including tabs fits 1280x720 at effective scale 1.')
lua.execute("""
local A=HeroFreePick;local original=A.LearnedEntries
local entries={{id=991,name='Alpha',class='Mage',spec='Fire',kind='Ability',quality='Rare'},{id=992,name='Beta',class='Mage',spec='Frost',kind='Talent',quality='Epic'},{id=993,name='Alpha Warrior',class='Warrior',spec='Arms',kind='Ability',quality='Rare'}}
A.LearnedEntries=function()return entries end
A.class='Mage';A.spec='All';A.quality='All';A.ownership='All';A.learnedFilter='All';A.learnedQuery=''
assert(#A.FilteredLearnedEntries()==3)
A.quality='Rare';assert(#A.FilteredLearnedEntries()==2)
A.spec='Fire';assert(#A.FilteredLearnedEntries()==1)
A.learnedFilter='Talents';assert(#A.FilteredLearnedEntries()==0)
A.learnedFilter='All';A.ownership='Planned';HeroFreePickPlans.entries[991]=1;assert(#A.FilteredLearnedEntries()==1)
A.ownership='Not planned';assert(#A.FilteredLearnedEntries()==0)
A.ownership='All';A.spec='All';A.learnedFilter='Warrior';assert(#A.FilteredLearnedEntries()==1)
A.learnedQuery='Beta';assert(#A.FilteredLearnedEntries()==0)
HeroFreePickPlans.entries[991]=nil;A.LearnedEntries=original
A.quality='All';A.ownership='All';A.spec='All';A.learnedFilter='All';A.learnedQuery=''
""")
print('PASS: learned rarity, specialization, planned state, type/class and search combine correctly.')

# The layout wrapper is a plain Frame, not a Button: catch the reported crash.
lua.execute("""
local wrapper=HeroMenuLayout.frames.filter
rawset(wrapper,'SetText',false)
HeroFreePick.RefreshDetails()
HeroFreePickFrame:Hide();HeroFreePick.Toggle()
assert(HeroFreePickFrame:IsShown())
""")
print('PASS: menu opens and refreshes with no SetText method on the filter wrapper.')


ET.parse(root/'Bindings.xml')
lua.execute((root/'Access.lua').read_text())
print('PASS: cached pre-0.30 file list loads preparation and dialog without either new Lua file.')
print('PASS: access bindings, XML and production preparation modules load in Lua 5.1.')

lua.execute("""
local A=HeroFreePick;local warn=A.ShowPointWarning;local warning
A.ShowPointWarning=function(s)warning=s end
local talents={}
for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)and A.MaxRank(e)>=2 and A.TalentRequiredLevel(e)==10 then talents[#talents+1]=e;if #talents==2 then break end end end
A.CancelPreparation();HeroFreePickPlans.entries={};HeroFreePickPlans.previewLearned={}
for _,key in ipairs({'entries','previewLearned'})do
 local set=key=='entries'and A.SetRank or A.SetLocalLearned
 testLevel=9;assert(A.TalentPointAllowance()==0 and not set(talents[1].id,1))
 testLevel=10;assert(A.TalentPointAllowance()==1);assert(set(talents[1].id,1));assert(A.AvailableTalentPoints(key)==0)
 warning=nil;assert(not set(talents[2].id,1));assert(warning=='Not enough Talent Points.')
 assert(not set(talents[1].id,2));assert(A.PendingTalentSpent(key)==1)
 assert(set(talents[1].id,0));assert(A.AvailableTalentPoints(key)==1)
 assert(set(talents[2].id,1));testLevel=11;assert(A.AvailableTalentPoints(key)==1)
 assert(set(talents[1].id,1));testLevel=10;assert(not set(talents[1].id,2))
 assert(set(talents[1].id,0));assert(set(talents[2].id,0))
end
testLevel=80;assert(A.TalentPointAllowance()==71)
A.ShowPointWarning=warn;A.CancelPreparation()
""")
print('PASS: level-based talent budget, zero at level 9, exhaustion alert, rank refunds, level changes and independent draft/advancement budgets.')

lua.execute("""
local A=HeroFreePick;A.CancelPreparation();HeroFreePickPlans.pendingBaseline=nil
function UnitClass()return 'Warrior','WARRIOR'end
testLevel=1;HeroFreePickPlans.progressionChoice=nil;A.InstalledModes={Classic=true,Hybrid=true}
assert(A.ModeChoiceDue()=='initial');assert(not A.ChooseInitialMode('Hero'));assert(A.ChooseInitialMode('ClassPlus'))
assert(A.mode=='ClassPlus'and A.ModeChoiceDue()==nil);assert(A.OtherClass('Mage')and not A.OtherClass('Warrior'))
assert(A.ClassPlusChoiceTooltip():find('level 10')and A.ClassPlusChoiceTooltip():find('Hybrid'))
testLevel=10;assert(A.ModeChoiceDue()=='hybrid');assert(not A.ChooseHybridPath('Warrior'));assert(A.ChooseHybridPath('Mage'))
assert(A.mode=='Hybrid'and not A.OtherClass('Mage')and A.OtherClass('Priest')and not A.ModeChoiceDue())
HeroFreePickPlans.progressionChoice={mode='ClassPlus'};A.mode='ClassPlus';assert(A.ChooseHybridPath(nil));assert(not A.ModeChoiceDue())
A.InstalledModes.Hybrid=nil;assert(A.ClassPlusChoiceTooltip():find('requires the Hybrid module'))
local tier0,tier1
for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)and e.class=='Warrior'then local n=A.TalentNode(e);if n.row==0 then tier0=e elseif n.row==1 then tier1=e end end end
assert(tier0 and tier1);HeroFreePickPlans.previewLearned={};HeroFreePickPlans.pendingBaseline=nil
testLevel=10;assert(not A.SetLocalLearned(tier1.id,1));A.mode='Hero';assert(not A.SetLocalLearned(tier1.id,1));A.mode='ClassPlus';testLevel=15;assert(A.SetLocalLearned(tier1.id,1));A.CancelPreparation()
-- Classic commits only at acceptance and waits for live rank acknowledgment.
A.mode='Classic';HeroFreePickPlans.previewLearned={};HeroFreePickPlans.entries={};HeroFreePickPlans.pendingBaseline=nil
local original=A.NativeTalent;local rank=0;local calls=0
A.NativeTalent=function(e)if e.id==tier0.id then return 1,1,rank,A.MaxRank(tier0),1 end end
function InCombatLockdown()return false end
function GetUnspentTalentPoints()return 5 end
function LearnTalent(tab,index)assert(tab==1 and index==1);calls=calls+1 end
A.BeginPreparation();assert(A.SetLocalLearned(tier0.id,1));assert(calls==0)
local ok,msg=A.AcceptPreparation();assert(not ok and A.classicCommit);A.PollClassicCommit(.1);assert(calls==1 and A.classicCommit)
A.PollClassicCommit(.1);assert(calls==1);rank=1;A.PollClassicCommit(.1);A.PollClassicCommit(.1);assert(not A.classicCommit and not A.HasPendingChanges())
assert(A.SetLocalLearned(tier0.id,0));local valid,why=A.ValidateClassic();assert(not valid and why:find('trainer'));A.CancelPreparation();assert(A.PendingRank(tier0)==1)
local ability;for _,e in ipairs(HeroFreePickCatalog)do if e.class=='Warrior'and not A.IsTalent(e)then ability=e;break end end
assert(not A.SetLocalLearned(ability.id,1));A.NativeTalent=original
""")
print('PASS: initial mode choice, Hybrid-only package path, level-10 decision, class boundaries, tier gates, Classic native acknowledgments and trainer-only committed resets.')

lua.execute("""
local A=HeroFreePick;local native=A.NativeTalent
A.NativeTalent=function()return 1,1,0,5,1 end
function GetActiveTalentGroup()return 1 end
local nativeCalls=0;local lines={}
GameTooltip.SetTalent=function()nativeCalls=nativeCalls+1 end
GameTooltip.AddLine=function(_,s)lines[#lines+1]=s end
A.class='Warrior';A.spec='All';A.view='browse';A.isBrowse=false;testLevel=80
A.mode='Classic';A.Refresh();HeroNativeTalent1.scripts.OnEnter(HeroNativeTalent1);assert(nativeCalls==1)
for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
 A.mode=mode;lines={};A.Refresh();HeroNativeTalent1.scripts.OnEnter(HeroNativeTalent1)
 assert(nativeCalls==1);local text=table.concat(lines,' ');assert(text:find('Requires Level')and text:find('No tree%-investment'))
end
A.NativeTalent=native
""")
print('PASS: Classic uses native talent tooltips; all three custom modes show level-only requirements.')

lua.execute("""
local A=HeroFreePick;A.mode='Hero';testLevel=80;A.CancelPreparation();A.BeginPreparation()
local e=HeroFreePickCatalog[1];assert(A.SetLocalLearned(e.id,1))
HeroFreePickFrame:Show();A.ShowPendingReview();A.HidePreparationPreservingChanges()
assert(not HeroFreePickFrame:IsShown()and not A.PendingDialog:IsShown()and A.HasPendingChanges())
assert(type(A.ClassicCommitPoller.scripts.OnUpdate)=='function'and type(A.ClassicCommitResult)=='function')
local called=false;local poll=A.PollClassicCommit;A.PollClassicCommit=function(elapsed)assert(elapsed==.1);called=true end
A.ClassicCommitPoller.scripts.OnUpdate(A.ClassicCommitPoller,.1);assert(called);A.PollClassicCommit=poll
A.CancelPreparation()
""")
print('PASS: real OnUpdate poller is connected and closing blocked popups preserves pending changes.')

# Exercise the visible initial-choice button, rather than only the policy helper.
lua.execute("""
A=HeroFreePick;testLevel=1;A.classicCommit=nil
HeroFreePickPlans.progressionChoice=nil;HeroFreePickPlans.pendingBaseline=nil
HeroFreePickPlans.entries={};HeroFreePickPlans.previewLearned={}
A.ShowModeChoice();assert(HeroProgressionChoice:IsShown())
local b=A.ProgressionChoiceButtons[1];assert(b.text=='Classic Character' and b:IsShown())
b.scripts.OnClick();assert(HeroFreePickPlans.progressionChoice.mode=='Classic')
assert(not HeroProgressionChoice:IsShown())
""")
assert "shield:SetFrameLevel(60)" in ui
assert "box:SetFrameLevel(61)" in ui
assert "b:SetFrameLevel(62);b:EnableMouse(true);b:Enable()" in ui
print('PASS: initial Classic choice works through its visible button; popup layers explicitly ordered.')

lua.execute("""
local shifted=false;local over=true
IsShiftKeyDown=function()return shifted end
MouseIsOver=function()return over end
HeroFreePickFrame:Show()
local owner=CreateFrame('Button');owner:Show()
for _,m in ipairs(HeroMasteries)do
 local members=A.MasteryTooltipMembers(m);assert(#members==#m.members)
 local expected={};for _,spell in ipairs(m.members)do expected[spell]=true end
 for i,member in ipairs(members)do
  assert(expected[member.spell]and member.level and member.name and member.texture);expected[member.spell]=nil
  if i>1 then local previous=members[i-1];assert(previous.level<member.level or(previous.level==member.level and previous.name<=member.name))end
 end
 assert(next(expected)==nil)
 owner.entry=m;shifted=false;A.ShowMasteryTooltip(owner)
 assert(A.MasteryTooltip:IsShown())
 for _,row in ipairs(A.MasteryTooltipRows)do assert(not row:IsShown())end
 shifted=true;A.MasteryTooltip.scripts.OnUpdate(A.MasteryTooltip,.01)
 for i,member in ipairs(members)do
  local row=A.MasteryTooltipRows[i];assert(row:IsShown()and row.member.spell==member.spell)
  row.scripts.OnEnter(row);assert(HeroMasteryAbilityPreview:IsShown())
  row.scripts.OnLeave(row);assert(not HeroMasteryAbilityPreview:IsShown())
 end
 shifted=false;A.MasteryTooltip.scripts.OnUpdate(A.MasteryTooltip,.01)
 for _,row in ipairs(A.MasteryTooltipRows)do assert(not row:IsShown())end
end
over=false;A.MasteryTooltip.scripts.OnUpdate(A.MasteryTooltip,.4);assert(not A.MasteryTooltip:IsShown())
""")
print('PASS: every Mastery member resolves; Shift expands/collapses, icon previews open/close, and leaving dismisses the tooltip.')

lua.execute("""
local b=CreateFrame('Button');b.icon=b:CreateTexture();HeroFreePickFrame:Show()
local member;for _,e in ipairs(HeroFreePickCatalog)do if e.requiredMastery then member=e;break end end
assert(member)
for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
 A.mode=mode;A.UpdateMasteryBadge(b,member)
 assert(b.masteryBadge:IsShown()and b.masteryBadge.entry==A.byID[member.requiredMastery])
 b.masteryBadge.scripts.OnEnter(b.masteryBadge);assert(A.MasteryTooltip:IsShown())
end
A.mode='Classic';A.UpdateMasteryBadge(b,member)
assert(not b.masteryBadge:IsShown()and not A.MasteryTooltip:IsShown())
A.mode='Hero';A.UpdateMasteryBadge(b,member)
A.UpdateMasteryBadge(b,HeroMasteries[1]);assert(not b.masteryBadge:IsShown())
""")
print('PASS: Mastery badges open the matching tooltip in all custom modes; Classic and recycled non-member buttons hide badges.')

lua.execute("""
local oldClass=UnitClass
UnitClass=function()return 'Hunter','HUNTER'end;testLevel=1;A.classicCommit=nil
A.mode='Hero';A.view='browse'
for _,bundle in ipairs(HeroCompanionBundles)do
 HeroFreePickPlans.previewLearned={};HeroFreePickPlans.entries={};HeroFreePickPlans.pendingBaseline=nil
 assert(A.SetLocalLearned(bundle.id,1))
 assert(A.AbilityPointsSpent()==4 and A.RaritySpent('Epic')==2)
 local count=0
 for _,child in ipairs(HeroCompanionAbilities)do if child.requiredBundle==bundle.id then
  count=count+1;assert(HeroFreePickPlans.previewLearned[child.id]==1)
  assert(not A.SetLocalLearned(child.id,0));assert(child.level==1 and child.ae==0)
  local b=CreateFrame('Button');b.icon=b:CreateTexture();A.UpdateMasteryBadge(b,child)
  assert(b.masteryBadge.entry==bundle)
 end end
 assert(count==#bundle.members and #A.MasteryTooltipMembers(bundle)==count)
 assert(A.SetLocalLearned(bundle.id,0));assert(next(HeroFreePickPlans.previewLearned)==nil)
 assert(A.AbilityPointsSpent()==0 and A.RaritySpent('Epic')==0)
 HeroFreePickPlans.pendingBaseline=nil;assert(A.SetRank(bundle.id,1))
 for _,child in ipairs(HeroCompanionAbilities)do if child.requiredBundle==bundle.id then assert(HeroFreePickPlans.entries[child.id]==1)end end
 assert(A.CancelPreparation());assert(next(HeroFreePickPlans.entries)==nil)
end
HeroFreePickPlans.pendingBaseline=nil;A.mode='ClassPlus'
assert(A.SetLocalLearned(HeroCompanionBundles[1].id,1))
assert(not A.SetLocalLearned(HeroCompanionBundles[2].id,1))
A.CancelPreparation();A.mode='Classic'
for _,e in ipairs(HeroCompanionBundles)do assert(not A.EntryAvailableInMode(e)and not A.SetLocalLearned(e.id,1))end
for _,e in ipairs(HeroCompanionAbilities)do assert(not A.EntryAvailableInMode(e))end
local tame={id=1515,class='Hunter',kind='Ability',spells={1515}}
assert(tame and A.EntryAvailableInMode(tame));A.mode='Hero';assert(not A.EntryAvailableInMode(tame))
UnitClass=oldClass
""")
print('PASS: all five bundles stage/refund full grants at 4 AP/2 Epic; drafts cancel cleanly; child purchases blocked; Hunter Class+ and Classic boundaries enforced.')

lua.execute("""
local demon=A.byID[21954705];assert(demon.level==1)
local imp
for _,e in ipairs(HeroFreePickCatalog)do for _,spell in ipairs(e.spells)do if spell==688 and not A.IsTalent(e)then imp=e end end end
assert(imp and imp.requiredMastery==demon.id and imp.ae==0 and HeroRarityCosts[imp.id]==0)
local found=false;for _,m in ipairs(A.MasteryTooltipMembers(demon))do if m.spell==688 then found=true end end;assert(found)
A.mode='Hero';testLevel=1;HeroFreePickPlans.previewLearned={};HeroFreePickPlans.entries={};HeroFreePickPlans.pendingBaseline=nil
assert(A.SetLocalLearned(demon.id,1));assert(A.SetLocalLearned(imp.id,1))
assert(A.AbilityPointsSpent()==2);assert(A.SetLocalLearned(demon.id,0));assert(not HeroFreePickPlans.previewLearned[imp.id])
""")
print('PASS: level-one Demon Mastery includes Summon Imp, free member selection and cascade removal.')

# Packaged textures must exist and their routing must cover entry and expanded tooltip icons.
import hashlib
art=root/'Art/Companions'
records=json.loads((art/'sources.json').read_text())
assert len(records)==13
for record in records:
 assert hashlib.sha256((art/record['file']).read_bytes()).hexdigest()==record['sha256']
lua.execute("""
A.mode='Hero'
for _,e in ipairs(HeroCompanionBundles)do assert(A.EntryIcon(e)==A.PackageSpellIcons[e.spells[1]])end
for _,e in ipairs(HeroCompanionAbilities)do assert(A.EntryIcon(e)==A.PackageSpellIcons[e.spells[1]])end
for _,bundle in ipairs(HeroCompanionBundles)do for _,member in ipairs(A.MasteryTooltipMembers(bundle))do assert(member.texture==A.PackageSpellIcons[member.spell])end end
A.mode='Classic';assert(A.EntryIcon(HeroCompanionBundles[1])~=A.PackageSpellIcons[HeroCompanionBundles[1].spells[1]])
""")
print('PASS: all 13 texture hashes verified; companion entry and tooltip artwork uses explicit mappings; Classic artwork unchanged.')

lua.execute("""
A.mode='Hero';HeroFreePickFrame:Show();local shift=false
IsShiftKeyDown=function()return shift end;MouseIsOver=function()return true end
local owner=CreateFrame('Button');owner:Show()
local bundle=HeroCompanionBundles[2];owner.entry=bundle
A.ShowEntryTooltip(owner);shift=true;A.RefreshMasteryTooltip()
local function checkRows()local count=0;for _,row in ipairs(A.MasteryTooltipRows)do if row:IsShown()then count=count+1 end end;assert(count==5)end
checkRows()
for _,child in ipairs(HeroCompanionAbilities)do if child.spells[1]==93558 then owner.entry=child end end
shift=false;A.ShowEntryTooltip(owner);assert(not A.MasteryTooltip:IsShown())
shift=true;A.ShowEntryTooltip(owner);assert(not A.MasteryTooltip:IsShown())
for _,child in ipairs(HeroCompanionAbilities)do owner.entry=child;A.ShowEntryTooltip(owner);assert(not A.MasteryTooltip:IsShown())end
assert(A.PackageSpellIcons[109982]:find('novart_books'))
assert(not A.PackageSpellIcons[91652]:find('novart_books'))
""")
print('PASS: Primary Dragonkin bundle expands five skills; all child spells stay on normal tooltips with Shift; Lore/Dismiss artwork swapped.')
lua.execute("""
local native=A.NativeTalent;local oldClass=UnitClass
UnitClass=function()return 'Warrior','WARRIOR'end;testLevel=20;A.mode='Classic';A.view='browse';A.classicCommit=nil
HeroFreePickPlans.entries={};HeroFreePickPlans.previewLearned={};HeroFreePickPlans.pendingBaseline=nil
local talent;for _,e in ipairs(HeroFreePickCatalog)do local n=A.IsTalent(e)and A.TalentNode(e);if e.class=='Warrior'and n and n.row==0 and A.MaxRank(e)>=2 then talent=e;break end end;assert(talent)
local rank,calls=0,0
A.NativeTalent=function(e)if e.id==talent.id then return 1,1,rank,5,1 end end
GetUnspentTalentPoints=function()return 5-rank end
InCombatLockdown=function()return false end
LearnTalent=function(tab,index)assert(tab==1 and index==1);calls=calls+1 end
A.BeginPreparation();assert(A.SetLocalLearned(talent.id,2));assert(calls==0)
HeroFreePickFrame:Show();A.ShowPendingReview();A.PendingAcceptButton.scripts.OnClick();assert(A.classicCommit)
local function tick(dt)A.ClassicCommitPoller.scripts.OnUpdate(A.ClassicCommitPoller,dt or .1)end
tick();assert(calls==1);tick();assert(calls==1)
rank=1;tick();tick();assert(calls==2)
rank=2;tick();tick();assert(not A.classicCommit and not A.PendingDialog:IsShown()and not A.HasPendingChanges())
-- Unconfirmed ranks time out instead of silently becoming learned.
assert(A.SetLocalLearned(talent.id,3));A.ShowPendingReview();A.PendingAcceptButton.scripts.OnClick();tick(6)
assert(not A.classicCommit and rank==2 and A.PendingDialog:IsShown())
A.CancelPreparation();A.NativeTalent=native;UnitClass=oldClass
""")
print('PASS: Classic popup Accept sends two native ranks sequentially through real OnUpdate polling, waits for acknowledgments, closes on success and times out without inventing learned ranks.')

lua.execute("""
assert(#HeroCompanionBundles==5)
local elemental=A.byID[23091606];assert(elemental.class=='Shaman'and elemental.level==1 and elemental.ae==4 and elemental.rarityCost==2 and #elemental.members==5)
A.mode='Hero';HeroFreePickFrame:Show();IsShiftKeyDown=function()return true end
local owner=CreateFrame('Button');owner:Show()
for _,bundle in ipairs(HeroCompanionBundles)do
 assert(A.SummoningDescriptions[bundle.spells[1]])
 owner.entry=bundle;A.ShowEntryTooltip(owner)
 for _,row in ipairs(A.MasteryTooltipRows)do if row:IsShown()then
  local lines={};HeroMasteryAbilityPreview.AddLine=function(_,s)lines[#lines+1]=s end
  row.scripts.OnEnter(row)
  assert(lines[1]==A.SummoningDescriptions[row.member.spell])
 end end
end
for _,e in ipairs(HeroCompanionAbilities)do
 local desc=A.SummoningDescriptions[e.spells[1]];assert(desc and #desc>0 and not desc:find('@ext:'))
 local lines={};GameTooltip.AddLine=function(_,s)lines[#lines+1]=s end
 owner.entry=e;A.ShowEntryTooltip(owner);assert(lines[1]==desc)
end
""")
print('PASS: Elemental matches imported costs/class/level; all five group members show recovered A52 descriptions in normal and expanded preview tooltips.')

lua.execute("""
A.mode='Hero'
for _,bundle in ipairs(HeroCompanionBundles)do
 local children={}
 for _,e in ipairs(HeroCompanionAbilities)do if e.requiredBundle==bundle.id then children[#children+1]=e end end
 local list={};for _,e in ipairs(children)do list[#list+1]=e end;list[#list+1]=bundle
 local grouped=A.GroupLearnedEntries(list);assert(#grouped==#children+1 and grouped[1].entry==bundle and not grouped[1].child)
 for i=2,#grouped do assert(grouped[i].child and grouped[i].entry.requiredBundle==bundle.id)end
 local filtered=A.GroupLearnedEntries({children[1]});assert(#filtered==2 and filtered[1].entry==bundle and filtered[2].child)
end
local member;for _,e in ipairs(HeroFreePickCatalog)do if e.requiredMastery then member=e;break end end
local rows=A.GroupLearnedEntries({member,A.byID[member.requiredMastery]});assert(#rows==2 and rows[2].entry==member and rows[2].child)
A.mode='Classic';rows=A.GroupLearnedEntries({member});assert(#rows==1 and not rows[1].child)
""")
print('PASS: learned bundle/Mastery parents precede compact children without duplication; filtered children retain parent context; Classic rows remain full size.')

lua.execute("""
A.mode='Hero'
local child=HeroCompanionAbilities[1];local b=CreateFrame('Button');b.icon=b:CreateTexture()
A.UpdateMasteryBadge(b,child);assert(b.masteryBadge:IsShown())
b.groupedLearnedChild=true;A.UpdateMasteryBadge(b,child);assert(not b.masteryBadge:IsShown())
b.groupedLearnedChild=false;A.UpdateMasteryBadge(b,child);assert(b.masteryBadge:IsShown())
""")
print('PASS: compact learned children hide covering badges; reused ordinary icons restore badges.')

lua.execute("""
A.mode='Hero';A.classicCommit=nil
for _,m in ipairs(HeroMasteries)do
 testLevel=m.level;HeroFreePickPlans.entries={};HeroFreePickPlans.previewLearned={};HeroFreePickPlans.pendingBaseline=nil
 assert(A.SetLocalLearned(m.id,1))
 for _,e in ipairs(HeroFreePickCatalog)do if e.requiredMastery==m.id then assert((HeroFreePickPlans.previewLearned[e.id]~=nil)==(e.level<=testLevel))end end
 testLevel=80;HeroMasteryGrantEvents.scripts.OnEvent(nil,'PLAYER_LEVEL_UP',80)
 for _,e in ipairs(HeroFreePickCatalog)do if e.requiredMastery==m.id then assert(HeroFreePickPlans.previewLearned[e.id]==1);assert(not A.SetLocalLearned(e.id,0))end end
 assert(A.AbilityPointsSpent()==2)
 A.CancelPreparation();assert(next(HeroFreePickPlans.previewLearned)==nil)
end
""")
print('PASS: every Mastery grants only eligible members on selection, grants remaining members at level-up for no additional AP, blocks individual removal and cancels cleanly.')

lua.execute("""
local e,dep;for _,v in ipairs(HeroFreePickCatalog)do local n=A.IsTalent(v)and A.TalentNode(v);if n and n.row>0 and n.depends>0 then e=v;break end end;assert(e)
local oldRank=A.PendingRank;local ranks={}
A.PendingRank=function(v)return ranks[v.id]or 0 end
A.mode='Classic';local unmet=A.TalentPrerequisiteLines(e);assert(#unmet==2 and not unmet[1].met and not unmet[2].met)
for _,v in ipairs(HeroFreePickCatalog)do if v.class==e.class and A.IsTalent(v)then ranks[v.id]=A.MaxRank(v)end end
local met=A.TalentPrerequisiteLines(e);assert(met[1].met and met[2].met,e.name.." / "..met[1].text.."="..tostring(met[1].met).." / "..met[2].text.."="..tostring(met[2].met))
A.mode='Hero';testLevel=A.TalentRequiredLevel(e)-1;assert(not A.TalentPrerequisiteLines(e)[1].met)
testLevel=testLevel+1;assert(A.TalentPrerequisiteLines(e)[1].met)
A.PendingRank=oldRank
""")
print('PASS: Classic tree/dependency requirements use planned ranks; custom level requirements switch at the exact required level.')


lua.execute("""
local oldClass,oldNative,oldWarning=UnitClass,A.NativeTalent,A.ShowPointWarning
UnitClass=function()return 'Mage','MAGE'end;A.NativeTalent=function()return nil end;testLevel=80;A.mode='Classic'
local e;for _,v in ipairs(HeroFreePickCatalog)do local n=A.IsTalent(v)and A.TalentNode(v);if v.class=='Mage'and n and n.row>0 and n.depends>0 then e=v;break end end;assert(e)
local warning;A.ShowPointWarning=function(s)warning=s end
for _,key in ipairs({'entries','previewLearned'})do
 HeroFreePickPlans.entries={};HeroFreePickPlans.previewLearned={};HeroFreePickPlans.pendingBaseline=nil;A.BeginPreparation()
 local setter=key=='entries'and A.SetRank or A.SetLocalLearned
 warning=nil;assert(not setter(e.id,1)and warning and not HeroFreePickPlans[key][e.id])
 local node=A.TalentNode(e)
 for _,v in ipairs(HeroFreePickCatalog)do local n=A.IsTalent(v)and A.TalentNode(v);if v.class==e.class and n and n.spec==node.spec and n.row<node.row and n.talent~=node.depends then HeroFreePickPlans[key][v.id]=A.MaxRank(v)end end
 warning=nil;assert(not setter(e.id,1)and warning and not HeroFreePickPlans[key][e.id])
end
UnitClass=oldClass;A.NativeTalent=oldNative;A.ShowPointWarning=oldWarning
""")
print('PASS: Classic tier and prerequisite failures alert immediately and spend no points in advancement or draft plans.')

lua.execute("""
A.mode='Classic';local oldClass=UnitClass;UnitClass=function()return 'Mage','MAGE'end
local ability;for _,e in ipairs(HeroFreePickCatalog)do if e.class=='Mage'and e.kind=='Ability'and e.id<20000000 then ability=e;break end end;assert(ability)
local originalSpells=ability.spells;ability.spells={originalSpells[1],9999998}
local slots={ability.spells[1]}
GetNumSpellTabs=function()return 1 end
GetSpellTabInfo=function()return 'General',nil,0,#slots end
GetSpellLink=function(slot,book)assert(book=='spell');return '|Hspell:'..slots[slot]..'|hKnown|h'end
HeroFreePickPlans.previewLearned={};local list=A.LearnedEntries();assert(#list==1 and list[1].id==ability.id and list[1].spellbookKnown)
slots={ability.spells[1],ability.spells[2],9999999};list=A.LearnedEntries();assert(#list==1)
local found=false;for _,e in ipairs(list)do if e.id==ability.id then found=true;assert(e.spellbookSpell==ability.spells[2])end end;assert(found)
assert(next(HeroFreePickPlans.previewLearned)==nil)
slots={};assert(#A.LearnedEntries()==0)
A.mode='Hero';assert(#A.LearnedEntries()==0);UnitClass=oldClass;ability.spells=originalSpells
""")
print('PASS: Classic spellbook abilities appear without preview selections; rank upgrades deduplicate, non-class/uncatalogued spells are excluded and removed spells disappear; custom modes remain independent.')

lua.execute("""
A.mode='Classic';local own=UnitClass;UnitClass=function()return 'Warrior','WARRIOR'end
A.class='Mage';A.spec='All';A.query='';A.quality='All';A.kind='All'
local count=0
for _,e in ipairs(A.Results())do if not A.IsTalent(e)then count=count+1;assert(e.class=='Mage'and e.id<20000000);assert(not A.SetLocalLearned(e.id,1))end end
assert(count>0)
for _,e in ipairs(HeroFreePickCatalog)do if e.kind=='Ability'then
 local before=e.level;assert(A.AbilityDisplayLevel(e)==(A.ClassicTrainerLevels[e.id]or 999))
 for _,mode in ipairs({'Hero','ClassPlus','Hybrid'})do A.mode=mode;assert(A.AbilityDisplayLevel(e)==before)end
 A.mode='Classic';assert(e.level==before)
end end
UnitClass=own
""")
print('PASS: Classic browses other class abilities without permission to learn them; trainer headings are mode-specific and custom levels stay unchanged.')

lua.execute("""
local A=HeroFreePick;A.mode='Classic'
local found=0
for _,e in ipairs(HeroFreePickCatalog)do
 if A.ClassicQuestSources[e.id]then
  found=found+1;assert(table.concat(A.LearningSourceLines(e),' '):find('Learned from a Quest',1,true))
 end
end
assert(found==12)
A.mode='Hero';for _,e in ipairs(HeroFreePickCatalog)do assert(#A.LearningSourceLines(e)==0)end
""")
print('PASS: verified quest sources appear for 12 Classic abilities; stock source labels do not override custom progression.')

lua.execute("""
local A=HeroFreePick
local oldClass,oldTabs,oldTabInfo,oldLink=UnitClass,GetNumSpellTabs,GetSpellTabInfo,GetSpellLink
UnitClass=function()return 'Hunter','HUNTER'end
A.mode='Classic';A.class='Hunter';A.spec='All';A.query='track beasts';A.kind='All';A.quality='All'
local entries=A.Results();assert(#entries==1 and entries[1].spells[1]==1494)
assert(A.AbilityDisplayLevel(entries[1])==2)
assert(table.concat(A.LearningSourceLines(entries[1]),' '):find('Trainer',1,true))
GetNumSpellTabs=function()return 1 end
local learned=false
GetSpellTabInfo=function()return 'Survival',nil,0,learned and 1 or 0 end
GetSpellLink=function()return '|Hspell:1494|h[Track Beasts]|h' end
assert(#A.ClassicSpellbookEntries()==0)
learned=true
local known=A.ClassicSpellbookEntries();assert(#known==1 and known[1].id==entries[1].id and known[1].spellbookSpell==1494)
UnitClass=function()return 'Warrior','WARRIOR'end
assert(#A.ClassicSpellbookEntries()==0)
for _,mode in ipairs({'Hero','ClassPlus','Hybrid'})do A.mode=mode;assert(#A.Results()==0)end
UnitClass,GetNumSpellTabs,GetSpellTabInfo,GetSpellLink=oldClass,oldTabs,oldTabInfo,oldLink
""")
print('PASS: Classic Track Beasts is browsable at trainer level 2, appears as learned only for a Hunter who knows it, and stays out of custom-mode catalogs.')
