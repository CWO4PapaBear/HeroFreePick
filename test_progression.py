from pathlib import Path
import json
# Load the production file order into a fresh Lua 5.1 runtime.
source=(Path(__file__).parent/'test_ui.py').read_text()
setup=source.split('lua.execute("""\nlocal A=HeroFreePick;')[0]
setup=setup.replace("'Masteries.lua','AscensionAbilities.lua','NativeTalentRoutes.lua'", "'Masteries.lua','StockAbilityLevels.lua','ProgressionRules.lua','AscensionAbilities.lua','NativeTalentRoutes.lua'")
exec(setup)
lua.execute("""
local A=HeroFreePick
A.InstalledModes={Classic=true,ClassPlus=true,Hybrid=true,Hero=true}
A.ShowPointWarning=function(message)assert(type(message)=='string'and #message>0)end
local count=0
for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
 A.mode=mode
 for _,e in ipairs(HeroFreePickCatalog)do
  UnitClass=function()return e.class,string.upper(e.class)end
  if not A.IsTalent(e)and A.EntryAvailableInMode(e)and not e.requiredMastery and not e.requiredBundle then
   local level=A.AbilityDisplayLevel(e)
   if e.isMastery or e.isBundle then
    local minimum
    for _,child in ipairs(HeroFreePickCatalog)do if child.requiredMastery==e.id or child.requiredBundle==e.id then local l=A.AbilityDisplayLevel(child);minimum=minimum and math.min(minimum,l)or l end end
    if minimum then assert(level==minimum,e.name..' controller must follow earliest member')end
   end
   for _,key in ipairs({'entries','previewLearned'})do
    HeroFreePickPlans={version=1,catalog='stock-335-v1',entries={},previewLearned={},preparationInitialized=true}
    local setter=key=='entries'and A.SetRank or A.SetLocalLearned
    testLevel=level-1;assert(not setter(e.id,1),mode..' accepted below level: '..e.name)
    assert(not HeroFreePickPlans[key][e.id])
    testLevel=level;assert(setter(e.id,1),mode..' rejected at level: '..e.name)
    if e.isMastery or e.isBundle then
     for _,child in ipairs(HeroFreePickCatalog)do if child.requiredMastery==e.id or child.requiredBundle==e.id then
      local granted=(HeroFreePickPlans[key][child.id]or 0)>0
      assert(granted==(A.AbilityDisplayLevel(child)<=level and A.PortalDestinationVisible(child)),e.name..' incorrectly granted '..child.name)
     end end
    end
    count=count+1
   end
  end
 end
end
A.mode='Hero';testLevel=80;UnitClass=function()return 'Hero','HERO'end
HeroFreePickPlans={version=1,catalog='stock-335-v1',entries={},previewLearned={},preparationInitialized=true}
for _,class in ipairs(A.classes)do
 A.class=class;A.spec='All';A.isBrowse=false
 for _,spec in ipairs(A.Specs())do
  A.spec=spec;A.Refresh(true)
  for i=1,40 do local button=_G['HeroNativeTalent'..i]
   if button and button:IsShown()and button.entry.talentOrigin then assert(button.alpha==1,'Paid tree ability incorrectly dimmed: '..button.entry.name)end
  end
 end
end
A.mode='ClassPlus'
assert(HeroStockAbilityLevels[133]==1 and HeroStockAbilityLevels[143]==6 and HeroStockAbilityLevels[145]==12)
print('PASS: fresh production startup, all 30 trees, '..count..' mode/draft unlock boundaries and automatic grants; stock Fireball ranks 1/6/12.')
""")

lua.execute("""
local A=HeroFreePick
for _,mode in ipairs({'ClassPlus','Hybrid'})do
 A.mode=mode
 assert(A.AbilityDisplayLevel(A.byID[184])==24)
 assert(A.AbilityDisplayLevel(A.byID[21092158])==1)
 for _,e in ipairs(HeroFreePickCatalog)do if not A.IsTalent(e)and A.EntryAvailableInMode(e)then
  local level=A.AbilityDisplayLevel(e);assert(level==1 or level>10,e.name..' still has an early unlock')
 end end
end
A.mode='Classic';assert(A.AbilityDisplayLevel(A.byID[19001494])==2)
A.mode='Hero';assert(A.AbilityDisplayLevel(A.byID[1167])==10)
assert(HeroStockAbilityLevels[143]==6) -- later-rank training remains stock
print('PASS: Class+/Hybrid early unlocks and group grants move to 1; Classic, Hero and later-rank schedules remain unchanged.')
""")

lua.execute("""
local A=HeroFreePick
local custom=A.byID[24000075];local classic=A.byID[19200000]
assert(custom.spells[1]==75 and custom.ae==2 and custom.te==0 and custom.quality=='Normal')
for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
 A.mode=mode;testLevel=1;UnitClass=function()return 'Hunter','HUNTER'end
 assert(A.EntryAvailableInMode(custom) and not A.EntryAvailableInMode(classic))
 assert(A.AbilityDisplayLevel(custom)==1)
 HeroFreePickPlans={version=1,catalog='stock-335-v1',entries={},previewLearned={},preparationInitialized=true}
 assert(A.SetRank(custom.id,1));assert(A.AbilityPointsSpent('entries')==2)
 assert(A.SetRank(custom.id,0));assert(A.AbilityPointsSpent('entries')==0)
 local allowance=A.AbilityPointAllowance;A.AbilityPointAllowance=function()return 1 end
 assert(not A.SetRank(custom.id,1));assert(not HeroFreePickPlans.entries[custom.id])
 A.AbilityPointAllowance=allowance
end
A.mode='Classic';assert(not A.EntryAvailableInMode(custom) and A.EntryAvailableInMode(classic))
assert(classic.ae==0 and A.AbilityDisplayLevel(classic)==1)
print('PASS: Auto Shot is a refundable level-one 2 AP custom purchase; Classic creation grant stays unchanged.')
""")
