-- Custom progression overlays. Native Classic records remain untouched.
local A=HeroFreePick
A.TalentAbilityMap={}
local byTalent={}
for _,e in ipairs(HeroTalentAbilityReferences)do byTalent[e.talentOrigin]=e end
for _,node in ipairs(HeroFreePickTrees)do
 local native=A.byID[node.entries[1]]
 if native and (native.kind=='TalentAbility' or byTalent[native.id] or node.row==10)then
  local ability=byTalent[native.id]
  if not ability then
   ability={id=20000000+node.talent,name=native.name,class=native.class,spec=native.spec,kind='Ability',quality='Normal',spells={node.ranks[1]},ae=2,te=0,level=10+5*node.row,rarityCost=0,talentOrigin=native.id,categories={6},order=0}
   HeroTalentAbilityReferences[#HeroTalentAbilityReferences+1]=ability
   HeroFreePickCatalog[#HeroFreePickCatalog+1]=ability;A.byID[ability.id]=ability
   HeroBrowseAssignment[ability.id]={categories={6},order=0,direct=false}
  end
  ability.level=math.max(ability.level or 1,10+5*node.row)
  ability.ae=ability.talentAbilityAP or (ability.ae and ability.ae>0 and ability.ae)or 2;ability.te=0
  ability.rarityCost=ability.talentAbilityRarityCost or ability.rarityCost or 0
  ability.requiredMastery=nil;ability.requiredBundle=nil
  ability.requiredAE=0;ability.requiredTE=0;ability.requiredIDs=''
  ability.talentTier=node.row;ability.talentSpellRanks=node.ranks
  ability.displayOnly=nil
  if node.row==10 then ability.level=60;ability.quality='Legendary';ability.rarityCost=1 end
  HeroRarityCosts[ability.id]=ability.rarityCost or 0
  for _,id in ipairs(node.entries)do A.TalentAbilityMap[id]=ability.id end
 end
end
-- A talent ability is a paid choice, not an automatic free Mastery grant.
local paidSpells={}
for _,e in ipairs(HeroTalentAbilityReferences)do for _,spell in ipairs(e.spells)do paidSpells[spell]=true end end
for _,mastery in ipairs(HeroMasteries)do
 local members={};for _,spell in ipairs(mastery.members)do if not paidSpells[spell]then members[#members+1]=spell end end;mastery.members=members
end
function A.AbilityForTalent(e)
 if A.mode~='Classic'and e and A.TalentAbilityMap[e.id]then return A.byID[A.TalentAbilityMap[e.id]]end
 return e
end
local function remap(state)
 if type(state)~='table'then return end
 for old,new in pairs(A.TalentAbilityMap)do if (state[old]or 0)>0 then state[new]=1;state[old]=nil end end
end
local begin=A.BeginPreparation
function A.BeginPreparation()
 local result=begin()
 if A.mode~='Classic'and HeroFreePickPlans then
  for _,key in ipairs({'entries','previewLearned'})do
   remap(HeroFreePickPlans[key]);if HeroFreePickPlans.pendingBaseline then remap(HeroFreePickPlans.pendingBaseline[key])end
  end
 end
 return result
end
for _,key in ipairs({'SetRank','SetLocalLearned'})do
 local original=A[key]
 A[key]=function(id,rank)
  if A.mode~='Classic'then id=A.TalentAbilityMap[id]or id end
  return original(id,rank)
 end
end
local pending=A.PendingRank
function A.PendingRank(e)return pending(A.AbilityForTalent(e))end
local originalLevel=A.AbilityDisplayLevel
local function stockLevel(e)
 local level
 for _,spell in ipairs(e.spells or {})do local value=HeroStockAbilityLevels[spell];if value and(not level or value<level)then level=value end end
 return level
end
function A.AbilityDisplayLevel(e)
 if A.mode=='Classic'then return originalLevel(e)end
 if e.talentOrigin then return e.level end
 -- A controller follows its earliest member under the current mode's rules.
 if e.isMastery or e.isBundle then
  local minimum
  for _,child in ipairs(HeroFreePickCatalog)do
   if child.requiredMastery==e.id or child.requiredBundle==e.id then
    local level=A.AbilityDisplayLevel(child)
    if level and(not minimum or level<minimum)then minimum=level end
   end
  end
  return minimum or originalLevel(e)
 end
 -- DK retains its level-one redesign in every custom mode.
 if (A.mode=='ClassPlus'or A.mode=='Hybrid')and e.class~='DeathKnight'then
  return stockLevel(e)or originalLevel(e)
 end
 return originalLevel(e)
end
-- Both entry points share one purchase; the tree retains its original geometry.
local available=A.EntryAvailableInMode
function A.EntryAvailableInMode(e)
 if A.mode~='Classic'and A.TalentAbilityMap[e.id]then return false end
 return available(e)
end
