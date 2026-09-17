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
for n in ['Catalog.lua','Adapter.lua','Layout.lua','Trees.lua','Organization.lua','Browse.lua','TalentAbilityReferences.lua','Masteries.lua','PendingChanges.lua','NativeTalentRoutes.lua','MenuLayoutOverrides.lua','MenuLayout.lua','HeroFreePick.lua','PendingDialog.lua']:lua.execute((root/n).read_text(encoding='utf-8-sig'))
lua.execute("""
local A=HeroFreePick
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
local ok,reason=A.AcceptPreparation();assert(not ok and reason:find('Server'))
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
print('PASS: access bindings, XML and production preparation modules load in Lua 5.1.')
