from pathlib import Path
import json
# Load the production file order into a fresh Lua 5.1 runtime.
source=(Path(__file__).parent/'test_ui.py').read_text()
setup=source.split('lua.execute("""\nlocal A=HeroFreePick;')[0]
setup=setup.replace("'Masteries.lua','NativeTalentRoutes.lua'", "'Masteries.lua','StockAbilityLevels.lua','ProgressionRules.lua','NativeTalentRoutes.lua'")
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
