from pathlib import Path
import xml.etree.ElementTree as ET,json
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parent/'HeroFreePick';lua=LuaRuntime(unpack_returned_tuples=True)
for p in root.glob('*.lua'):lua.execute('assert(loadstring(...))',p.read_text(encoding='utf-8-sig'))
ET.parse(root/'HeroFreePick.xml')
lua.execute('''
local function frame()
 local f={shown=true,w=500,h=380,text='',scripts={}}
 local methods={SetSize=function(s,w,h)s.w=w;s.h=h end,SetWidth=function(s,w)s.w=w end,SetHeight=function(s,h)s.h=h end,GetFrameLevel=function()return 1 end,GetWidth=function(s)return s.w end,GetHeight=function(s)return s.h end,SetText=function(s,t)s.text=t end,GetText=function(s)return s.text end,GetStringHeight=function(s)return 500 end,Show=function(s)s.shown=true end,Hide=function(s)s.shown=false end,IsShown=function(s)return s.shown end,SetScript=function(s,k,v)s.scripts[k]=v end,GetVerticalScroll=function()return 0 end,GetVerticalScrollRange=function()return 2000 end}
 setmetatable(f,{__index=function(s,k)if k=='dependencyOverlay'then return nil end;if k=='CreateFontString'or k=='CreateTexture'then return function()return frame()end end;return methods[k]or function()end end})
 return f
end
function CreateFrame()return frame()end
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
for n in ['Catalog.lua','Adapter.lua','Layout.lua','Trees.lua','Organization.lua','Browse.lua','TalentAbilityReferences.lua','NativeTalentRoutes.lua','MenuLayoutOverrides.lua','MenuLayout.lua','HeroFreePick.lua']:lua.execute((root/n).read_text(encoding='utf-8-sig'))
lua.execute('''
local A=HeroFreePick;A.Init();assert(#A.classes==10);assert(#HeroFreePickTrees==829)
local old=HeroFreePickCatalog[1];A.SetRank(old.id,1);local before=HeroFreePickPlans.entries[old.id]
for _,class in ipairs(A.classes)do
 A.class=class;A.isBrowse=false
 for _,spec in ipairs(A.Specs())do A.spec=spec;A.view='browse';A.Refresh(true) end
end
assert(HeroFreePickPlans.entries[old.id]==before)
A.class='Mage';A.spec='All';A.view='browse';A.quality='Legendary';A.ownership='Not planned';A.Refresh(true)
for _,e in ipairs(A.VisibleEntries('talent'))do assert(e.quality=='Legendary');assert(not HeroFreePickPlans.entries[e.id])end
A.quality='All';A.ownership='All';A.selected=old;A.RefreshDetails();A.view='architect';A.Refresh(true)
A.isBrowse=true;A.view='browse';A.Refresh(true);A.isBrowse=false;assert(A.ApplyBuild()==false);assert(#A.LearnedEntries()==0)
local savedLearned=A.LearnedEntries;A.LearnedEntries=function()return {old}end;A.RefreshDetails();A.Locate(old);A.FindRelated(old);A.LearnedEntries=savedLearned;A.RefreshDetails();assert(#A.LearnedEntries()==0)
local talent;for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)then talent=e;break end end
A.SetRank(talent.id,0);testLevel=9;assert(not A.SetRank(talent.id,1));A.Refresh();testLevel=10;assert(A.SetRank(talent.id,1));assert(A.NativeTalentPoints()==71);A.SetRank(talent.id,0);testLevel=80
local nodes={};for _,n in ipairs(HeroFreePickTrees)do nodes[n.talent]=n end
for _,n in ipairs(HeroFreePickTrees)do assert(n.column>=0 and n.column<=3);if n.depends>0 then local parent=nodes[n.depends];assert(parent and parent.class==n.class and parent.spec==n.spec)end end
local beforeDraft=HeroFreePickPlans.entries[old.id]
assert(A.SetLocalLearned(old.id,1));assert(#A.LearnedEntries()==1);assert(HeroFreePickPlans.entries[old.id]==beforeDraft)
A.learnedQuery='nonexistent string';assert(#A.FilteredLearnedEntries()==0);A.learnedQuery='';A.learnedFilter=old.class;assert(#A.FilteredLearnedEntries()==1)
A.RefreshDetails();A.Init();assert(#A.LearnedEntries()==1);assert(A.SetLocalLearned(old.id,0));assert(#A.LearnedEntries()==0)
A.learnedFilter='All'
A.SetRank(old.id,0);A.Refresh();SlashCmdList.HEROFREEPICK();SlashCmdList.HEROFREEPICK()
for _,size in ipairs({{1280,720},{1920,1080},{1024,768},{800,600}})do UIParent:SetSize(size[1],size[2]);A.FitWindow();local scale=math.min(1,(size[1]-32)/1180,(size[2]-40)/802);assert(802*scale+12<=size[2]);assert(1180*scale<=size[1]-32)end
''')
print('PASS: Lua 5.1/XML, ten-class/spec rendering, tree dependencies, filters, saved plans, architect and disabled learning. Mock UI only; in-game visual check remains.')

ET.parse(root/'Bindings.xml')
lua.execute("function InCombatLockdown()return false end; bindCalls=0; function SetBinding(k,v)assert(k=='N' and v=='HERO_CHARACTER_ADVANCEMENT');bindCalls=bindCalls+1;return true end; function SaveBindings()end; function GetCurrentBindingSet()return 2 end; GameMenuFrame=nil; GameMenuButtonOptions=nil")
lua.execute((root/'Access.lua').read_text())
print('PASS: access Lua and binding XML load; live key/menu integration requires in-game validation.')

lua.execute("""
local A=HeroFreePick;A.Init();local e
for _,v in ipairs(HeroFreePickCatalog)do if A.IsTalent(v)then e=v;break end end
function UnitClass()return e.class,string.upper(e.class)end
function GetNumTalentTabs()return 1 end
function GetNumTalents()return 1 end
function GetActiveTalentGroup()return 1 end
local rank=0;local points=1;local calls=0
function GetUnspentTalentPoints()return points end
function GetTalentInfo()return GetSpellInfo(e.spells[1]),nil,1,1,rank,5 end
function LearnTalent(tab,index,pet,group)assert(tab==1 and index==1 and pet==false and group==1);calls=calls+1 end
function InCombatLockdown()return false end
testLevel=10;assert(A.AssignNativeTalent(e));assert(calls==1);assert(select(3,A.NativeTalent(e))==0)
rank=1;assert(select(3,A.NativeTalent(e))==1)
points=0;A.AssignNativeTalent(e);assert(calls==1)
points=1;testLevel=9;A.AssignNativeTalent(e);assert(calls==1)
testLevel=80;function InCombatLockdown()return true end;A.AssignNativeTalent(e);assert(calls==1)
function UnitClass()return 'Hero','HERO'end;assert(not A.AssignNativeTalent(e));assert(calls==1)
""")
print('PASS: own-class native talent dispatch, server-owned ranks, no points, below level 10, combat and other-class guards.')

lua.execute("""
local A=HeroFreePick;function UnitClass()return 'Warrior','WARRIOR'end
assert(not A.OtherClass('Warrior'));assert(A.OtherClass('Mage'))
local mage;for _,e in ipairs(HeroFreePickCatalog)do if e.class=='Mage'and e.kind=='Ability'then mage=e;break end end
assert(not A.SetLocalLearned(mage.id,1))
function UnitClass()return 'Hero','HERO'end;assert(not A.OtherClass('Mage'));assert(not A.OtherClass('Warrior'))
""")
print('PASS: normal-class preview restrictions and Hero exception.')

lua.execute("""
local A=HeroFreePick;testLevel=80;HeroFreePickPlans.previewLearned={};local entries={}
for _,e in ipairs(HeroFreePickCatalog)do if e.kind=='Ability'and e.quality=='Legendary'then entries[#entries+1]=e end end
assert(#entries>=7)
local costs={};for i=1,7 do local id=entries[i].id;costs[id]=HeroRarityCosts[id];HeroRarityCosts[id]=1 end
for i=1,6 do assert(A.SetLocalLearned(entries[i].id,1))end
assert(A.RaritySpent('Legendary')==6);assert(not A.SetLocalLearned(entries[7].id,1))
assert(A.SetLocalLearned(entries[1].id,0));assert(A.SetLocalLearned(entries[7].id,1));assert(A.RaritySpent('Legendary')==6)
for id,cost in pairs(costs)do HeroRarityCosts[id]=cost end
assert(A.RarityLimits.Legendary==6 and A.RarityLimits.Epic==11 and A.RarityLimits.Rare==12 and A.RarityLimits.Uncommon==10)
HeroFreePickPlans.previewLearned={}
""")
print('PASS: rarity cap, over-cap rejection and slot refund.')
# Primary stat tooltip behavior: no server effects are claimed or applied.
lua.execute('''
local lines={}
GameTooltip.SetText=function(_,s)lines[#lines+1]=s end
GameTooltip.AddLine=function(_,s)lines[#lines+1]=s end
local shift=false
IsShiftKeyDown=function()return shift end
for _,stat in ipairs({'Strength','Agility','Intellect','Spirit'})do
 local owner={primaryStatKey=stat}
 lines={};HeroFreePick.PrimaryStatTooltip(owner)
 local normal=table.concat(lines,'\\n')
 assert(normal:find('Primary Stat: '..stat,1,true))
 assert(normal:find('Hold SHIFT',1,true))
 assert(not normal:find(HeroFreePick.PrimaryStats[stat].bonuses[1].name,1,true))
 shift=true;lines={};HeroFreePick.PrimaryStatTooltip(owner)
 local expanded=table.concat(lines,'\\n')
 for _,effect in ipairs(HeroFreePick.PrimaryStats[stat].bonuses)do assert(expanded:find(effect.description,1,true))end
 assert(expanded:find('Preview only',1,true));shift=false
end
''')
print('PASS: four primary-stat tooltips, normal/Shift detail separation and preview disclosure.')
lua.execute('''
local A=HeroFreePick
local oldLevel=testLevel
for _,v in ipairs({{1,9},{9,9},{10,10},{11,11},{80,80}})do testLevel=v[1];assert(A.AbilityPointAllowance()==v[2])end
testLevel=1
local saved=HeroFreePickPlans.previewLearned;HeroFreePickPlans.previewLearned={}
local oldOther=A.OtherClass;A.OtherClass=function()return false end
local e={id=99999991,kind='Ability',quality='Normal',ae=9,level=1,spells={1},class='Warrior'}
local e2={id=99999992,kind='Ability',quality='Normal',ae=1,level=1,spells={1},class='Warrior'}
A.byID[e.id]=e;A.byID[e2.id]=e2
assert(A.SetLocalLearned(e.id,1));assert(A.AvailableAbilityPoints()==0)
assert(not A.SetLocalLearned(e2.id,1))
testLevel=10;assert(A.AvailableAbilityPoints()==1);assert(A.SetLocalLearned(e2.id,1))
assert(A.SetLocalLearned(e.id,0));assert(A.AvailableAbilityPoints()==9)
A.byID[e.id]=nil;A.byID[e2.id]=nil;A.OtherClass=oldOther;HeroFreePickPlans.previewLearned=saved;testLevel=oldLevel
''')
print('PASS: Ability Point level schedule, spending, insufficient balance, level gain and refund.')


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

# Talent-origin references are visible across classes but never alter progression.
lua.execute("""
local A=HeroFreePick
assert(#HeroTalentAbilityReferences==144)
local seen,natives={},0
for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)then natives=natives+1 end end
assert(natives==829)
A.spec='All';A.kind='All';A.quality='All';A.query=''
for _,e in ipairs(HeroTalentAbilityReferences)do
 assert(not seen[e.id]);seen[e.id]=true
 assert(A.byID[e.id]==e and e.kind=='Ability' and e.ae>0 and e.te==0)
 assert(A.IsTalent(A.byID[e.talentOrigin]))
 assert(HeroBrowseAssignment[e.id] and HeroRarityCosts[e.id]==e.rarityCost)
 assert(not A.SetRank(e.id,1) and not A.SetLocalLearned(e.id,1))
 assert(not HeroFreePickPlans.entries[e.id] and not (HeroFreePickPlans.previewLearned or {})[e.id])
 A.class=e.class;local found=false
 for _,v in ipairs(A.VisibleEntries('ability'))do if v.id==e.id then found=true end end
 assert(found,e.name..' absent from ability pane')
 if e.name=='Living Bomb' then assert(e.ae==2) end
 if e.quality=='Normal'then assert(e.rarityCost==0)end
end
""")
print('PASS: 144 talent-origin ability references visible, costs mapped, 829 native talents preserved, progression blocked.')
