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
