-- Original implementation. Local planning only; no transport or native extensions.
HeroFreePick = {class='Mage', spec='All', kind='All', quality='All', query='', page=1, selected=nil}
local A=HeroFreePick
A.classes={'Warrior','Paladin','Hunter','Rogue','Priest','DeathKnight','Shaman','Mage','Warlock','Druid'}
A.byID={}
for _,entry in ipairs(HeroFreePickCatalog or {}) do A.byID[entry.id]=entry end
function A.MaxRank(e)
    return (e.kind=='Talent' or e.kind=='TalentAbility') and math.max(1,#e.spells) or 1
end
function A.Init()
    if type(HeroFreePickPlans)=='table' and HeroFreePickPlans.catalog~='stock-335-v1' then
        HeroFreePickPlanBackup=HeroFreePickPlans
        local entries={}
        for id,rank in pairs(type(HeroFreePickPlans.entries)=='table' and HeroFreePickPlans.entries or {})do entries[id]=rank end
        HeroFreePickPlans={version=1,catalog='stock-335-v1',name=HeroFreePickPlans.name or 'My build',entries=entries}
    end
    if type(HeroFreePickPlans)~='table' or HeroFreePickPlans.version~=1 then
        HeroFreePickPlans={version=1,catalog='stock-335-v1',name='My build',entries={}}
    end
    if type(HeroFreePickPlans.entries)~='table' then HeroFreePickPlans.entries={} end
    for id,rank in pairs(HeroFreePickPlans.entries) do
        local e=A.byID[id]
        if not e or type(rank)~='number' or rank~=rank or rank<1 then
            HeroFreePickPlans.entries[id]=nil
        else HeroFreePickPlans.entries[id]=math.min(math.floor(rank),A.MaxRank(e)) end
    end
 if A.ValidateMasterySelections then A.ValidateMasterySelections()end
end
function A.Specs()
    local seen,out={}, {'All'}
    for _,e in ipairs(HeroFreePickCatalog) do
        if e.class==A.class and not seen[e.spec] then seen[e.spec]=true;out[#out+1]=e.spec end
    end
    table.sort(out,function(x,y) if x=='All' then return true elseif y=='All' then return false end return x<y end)
    return out
end
function A.Results()
    local out={};local query=string.lower(A.query or '')
    for _,e in ipairs(HeroFreePickCatalog) do
        if (e.class==A.class) and (A.spec=='All' or e.spec==A.spec)
            and (A.kind=='All' or e.kind==A.kind) and (A.quality=='All' or e.quality==A.quality)
            and string.find(string.lower(e.name),query,1,true) then out[#out+1]=e end
    end
    table.sort(out,function(x,y) if x.name==y.name then return x.id<y.id end return x.name<y.name end)
    return out
end
function A.IsTalent(e) return e.kind=='Talent' or e.kind=='TalentAbility' end
function A.TalentsUnlocked() return UnitLevel and UnitLevel('player')>=10 end
function A.NativeTalentPoints() return GetUnspentTalentPoints and GetUnspentTalentPoints() or 0 end
function A.AbilityPointAllowance()
 return math.max(9,UnitLevel('player') or 1)
end
function A.AbilityPointsSpent(key)
 local spent=0
 for id,rank in pairs(HeroFreePickPlans[key or 'previewLearned']or {})do
  local e=A.byID[id];if e and rank>0 and not A.IsTalent(e)then spent=spent+(e.ae or 0)end
 end
 return spent
end
function A.AvailableAbilityPoints(key)
 return A.AbilityPointAllowance()-A.AbilityPointsSpent(key)
end
local function canAfford(e,rank,key)
 if A.IsTalent(e)or rank<=0 or (HeroFreePickPlans[key]or {})[e.id]then return true end
 if (e.ae or 0)<=A.AvailableAbilityPoints(key)then return true end
 if A.ShowPointWarning then A.ShowPointWarning('Not enough Ability Points.')elseif UIErrorsFrame then UIErrorsFrame:AddMessage('Not enough Ability Points.',1,.2,.2)end
 return false
end
function A.SetRank(id,rank)
    local e=A.byID[id];if not e or e.displayOnly then return false end
    rank=tonumber(rank);if not rank or rank~=rank then return false end
    rank=math.max(0,math.min(math.floor(rank),A.MaxRank(e)))
    if not A.IsTalent(e) and rank>(HeroFreePickPlans.entries[id]or 0) and UnitLevel('player')<(e.level or 1) then return false end
    if A.IsTalent(e) and rank>(HeroFreePickPlans.entries[id]or 0) and not A.TalentsUnlocked() then return false end
    if A.MasteryAllowed and not A.MasteryAllowed(e,rank,'entries')then return false end
    if not canAfford(e,rank,'entries')then return false end
    HeroFreePickPlans.entries[id]=rank>0 and rank or nil
    return true
end
function A.Totals()
    local ae,te,count=0,0,0
    for id,rank in pairs(HeroFreePickPlans.entries) do
        local e=A.byID[id]
        if e then ae=ae+e.ae*rank;te=te+e.te*rank;count=count+1 end
    end
    return ae,te,count
end
-- Fail closed. The future authoritative backend replaces this method.
function A.ApplyBuild() return false,'Learning is unavailable: this is a local plan only.' end

-- No server-owned learned state exists in this read-only build. Never infer ownership from draft selections or native class spells.
-- Local prototype state, separate from Archetype drafts and real character spells.
A.RarityLimits={Legendary=6,Epic=11,Rare=12,Uncommon=10}
function A.RaritySpent(quality)
 local spent=0
 for id,rank in pairs(HeroFreePickPlans.previewLearned or {})do local e=A.byID[id];if e and rank>0 and not A.IsTalent(e) and e.quality==quality then spent=spent+((HeroRarityCosts or {})[id]or 1)end end
 return spent
end
function A.SetLocalLearned(id,rank)
 local e=A.byID[id];if not e or e.displayOnly or A.OtherClass(e.class)then return false end
 HeroFreePickPlans.previewLearned=HeroFreePickPlans.previewLearned or {}
 rank=math.max(0,math.min(rank,A.MaxRank(e)))
 if A.MasteryAllowed and not A.MasteryAllowed(e,rank,'previewLearned')then return false end
 if rank>0 and not HeroFreePickPlans.previewLearned[id] and not A.IsTalent(e) then
  local limit=A.RarityLimits[e.quality];local cost=(HeroRarityCosts or {})[id]or 1
  if limit and A.RaritySpent(e.quality)+cost>limit then
   if UIErrorsFrame then UIErrorsFrame:AddMessage(e.quality..' rarity slots are full.',1,.2,.2)end
   return false
  end
 end
 if rank>(HeroFreePickPlans.previewLearned[id]or 0) and (A.IsTalent(e) and not A.TalentsUnlocked() or not A.IsTalent(e) and UnitLevel('player')<(e.level or 1))then return false end
 if not canAfford(e,rank,'previewLearned')then return false end
 HeroFreePickPlans.previewLearned[id]=rank>0 and rank or nil;return true
end
function A.LearnedEntries()
 local out={}
 for id,rank in pairs(HeroFreePickPlans.previewLearned or {})do local e=A.byID[id];if e and rank>0 then out[#out+1]=e end end
 table.sort(out,function(x,y)if x.name==y.name then return x.id<y.id end;return x.name<y.name end);return out
end
function A.FilteredLearnedEntries()
 local out={}
 for _,e in ipairs(A.LearnedEntries())do
  local planned=HeroFreePickPlans and HeroFreePickPlans.entries and (HeroFreePickPlans.entries[e.id]or 0)>0
  local rarity=not A.quality or A.quality=='All' or e.quality==A.quality
  local plan=not A.ownership or A.ownership=='All' or A.ownership=='Planned'and planned or A.ownership=='Not planned'and not planned
  local spec=not A.spec or A.spec=='All' or (e.spec==A.spec and e.class==A.class)
  local kind=not A.learnedFilter or A.learnedFilter=='All' or A.learnedFilter=='Abilities'and not A.IsTalent(e) or A.learnedFilter=='Talents'and A.IsTalent(e) or e.class==A.learnedFilter
  if rarity and plan and spec and kind and string.find(string.lower(e.name),string.lower(A.learnedQuery or ''),1,true)then out[#out+1]=e end
 end
 return out
end

-- Normal-class talents use the native client API and authoritative server ranks.
function A.NativeTalent(e)
 if not UnitClass or not GetNumTalentTabs or not A.IsTalent(e) then return end
 local _,class=UnitClass('player');if string.upper(e.class)~=class then return end
 local expected=GetSpellInfo(e.spells[1])
 for tab=1,GetNumTalentTabs(false,false)do for index=1,GetNumTalents(tab,false,false)do
  local name,texture,tier,column,rank,maxRank=GetTalentInfo(tab,index,false,false,GetActiveTalentGroup())
  if name==expected then return tab,index,rank,maxRank,tier end
 end end
end
function A.AssignNativeTalent(e)
 local tab,index,rank,maxRank=A.NativeTalent(e)
 if not tab then return false end
 if A.TalentsUnlocked() and A.NativeTalentPoints()>0 and rank<maxRank and not InCombatLockdown()then LearnTalent(tab,index,false,GetActiveTalentGroup())end
 return true
end

function A.OtherClass(class)
 if not UnitClass then return false end
 local _,own=UnitClass('player');return own and own~='HERO' and string.upper(class)~=own
end

-- Preparation support is embedded for clients with a cached addon file list.
do
-- Reversible local preparation. No spell or talent learning APIs are called here.
local A=HeroFreePick
local keys={'entries','previewLearned','primaryStat'}
local function copy(v)
 if type(v)~='table'then return v end
 local out={};for k,x in pairs(v)do out[k]=copy(x)end;return out
end
local function equal(a,b)
 if type(a)~=type(b)then return false end
 if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not equal(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end
 return true
end
local function snapshot()
 local out={};for _,key in ipairs(keys)do out[key]=copy(HeroFreePickPlans[key])end;return out
end
function A.BeginPreparation()
 A.Init()
 if HeroFreePickPlans.pendingBaseline then return end
 HeroFreePickPlans.previewLearned=HeroFreePickPlans.previewLearned or {}
 -- Initial local baseline includes existing real talent ranks, once per character.
 if not HeroFreePickPlans.preparationInitialized then
  for _,e in ipairs(HeroFreePickCatalog)do
   if A.IsTalent(e)then local _,_,rank=A.NativeTalent(e);if rank and rank>0 then HeroFreePickPlans.previewLearned[e.id]=rank end end
  end
  HeroFreePickPlans.preparationInitialized=true
 end
 HeroFreePickPlans.pendingBaseline=snapshot()
end
function A.HasPendingChanges()
 local base=HeroFreePickPlans and HeroFreePickPlans.pendingBaseline
 return base and not equal(base,snapshot())or false
end
function A.PendingKey()return A.view=='architect'and 'entries'or 'previewLearned'end
function A.PendingRank(e)return ((HeroFreePickPlans or {})[A.PendingKey()]or {})[e.id]or 0 end
local function set(id,rank,key)
 local e=A.byID[id];rank=tonumber(rank)
 if not e or not rank or rank~=rank or A.OtherClass(e.class)then return false end
 A.BeginPreparation()
 rank=math.max(0,math.min(math.floor(rank),A.MaxRank(e)))
 local state=HeroFreePickPlans[key]or {};HeroFreePickPlans[key]=state
 if rank>0 and e.requiredMastery and (state[e.requiredMastery]or 0)<1 then
  A.ShowPointWarning('Requires '..A.byID[e.requiredMastery].name..'.');return false
 end
 if rank==0 and e.isMastery then
  for member in pairs(state)do if A.byID[member]and A.byID[member].requiredMastery==e.id then state[member]=nil end end
 end
 state[id]=rank>0 and rank or nil;return true
end
function A.SetRank(id,rank)return set(id,rank,'entries')end
function A.SetLocalLearned(id,rank)return set(id,rank,'previewLearned')end
function A.AdjustPending(e,delta)
 local fn=A.view=='architect'and A.SetRank or A.SetLocalLearned
 local ok=fn(e.id,A.PendingRank(e)+delta);A.Refresh();return ok
end
function A.AssignNativeTalent()return false end
local function totals(state)
 local out={AP=0,TP=0,Uncommon=0,Rare=0,Epic=0,Legendary=0}
 for id,rank in pairs(state or {})do local e=A.byID[id]
  if e and rank>0 then
   if A.IsTalent(e)then out.TP=out.TP+(e.te or 1)*rank
   else out.AP=out.AP+(e.ae or 0);if out[e.quality]then out[e.quality]=out[e.quality]+((HeroRarityCosts or {})[id]or 1)end end
  end
 end
 return out
end
function A.PendingTalentSpent()return totals(HeroFreePickPlans[A.PendingKey()]).TP end
function A.PendingSummary()
 local base=HeroFreePickPlans.pendingBaseline or snapshot();local sections={}
 for _,key in ipairs({'previewLearned','entries'})do
  local before=totals(base[key]);local after=totals(HeroFreePickPlans[key]);local added,removed=0,0
  local ids={};for id in pairs(base[key]or {})do ids[id]=true end;for id in pairs(HeroFreePickPlans[key]or {})do ids[id]=true end
  for id in pairs(ids)do local d=((HeroFreePickPlans[key]or {})[id]or 0)-((base[key]or {})[id]or 0);if d>0 then added=added+d else removed=removed-d end end
  sections[#sections+1]={key=key,before=before,after=after,added=added,removed=removed}
 end
 return sections
end
function A.CancelPreparation()
 local base=HeroFreePickPlans.pendingBaseline
 if base then for _,key in ipairs(keys)do HeroFreePickPlans[key]=copy(base[key])end end
 HeroFreePickPlans.pendingBaseline=nil
end
function A.ValidatePreparation()
 for _,key in ipairs({'previewLearned','entries'})do
  local state=HeroFreePickPlans[key]or {};local cost=totals(state)
  if cost.AP>A.AbilityPointAllowance()then return false,'Not enough Ability Points. Go Back to adjust your selections.'end
  for q,limit in pairs(A.RarityLimits)do if cost[q]>limit then return false,q..' rarity limit exceeded. Go Back to adjust your selections.'end end
  for id,rank in pairs(state)do local e=A.byID[id]
   if e and rank>0 then
    if A.OtherClass(e.class)then return false,'A selection belongs to another class.'end
    if e.requiredMastery and (state[e.requiredMastery]or 0)<1 then return false,'A required Mastery is missing.'end
    if not A.IsTalent(e)and UnitLevel('player')<(e.level or 1)then return false,'Required level not met for '..e.name..'.'end
   end
  end
 end
 return true
end
function A.AcceptPreparation()
 return false,'Server committing is unavailable. Your pending changes have been retained.'
end

end
