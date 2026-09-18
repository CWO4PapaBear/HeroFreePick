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
    local seen,out={All=true}, {'All'}
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
function A.TalentPointAllowance()
 return math.max(0,(UnitLevel('player')or 1)-9)
end
function A.PendingTalentSpent(key)
 local spent=0
 for id,rank in pairs(HeroFreePickPlans[key or A.PendingKey()]or {})do
  local e=A.byID[id];if e and A.IsTalent(e)and rank>0 then spent=spent+rank*(e.te or 1)end
 end
 return spent
end
function A.AvailableTalentPoints(key)return A.TalentPointAllowance()-A.PendingTalentSpent(key)end
local function set(id,rank,key)
 local e=A.byID[id];rank=tonumber(rank)
 if not e or not rank or rank~=rank or A.OtherClass(e.class)then return false end
 A.BeginPreparation()
 rank=math.max(0,math.min(math.floor(rank),A.MaxRank(e)))
 local state=HeroFreePickPlans[key]or {};HeroFreePickPlans[key]=state
 local oldRank=state[id]or 0
 if not A.IsTalent(e)and rank>0 and oldRank<=0 and (e.ae or 0)>A.AvailableAbilityPoints(key)then
  A.ShowPointWarning('Not enough Ability Points.');return false
 end
 if A.IsTalent(e)and rank>oldRank and (rank-oldRank)*(e.te or 1)>A.AvailableTalentPoints(key)then
  A.ShowPointWarning('Not enough Talent Points.');return false
 end
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
  if cost.TP>A.TalentPointAllowance()then return false,'Not enough Talent Points. Go Back to adjust your selections.'end
  if cost.AP>A.AbilityPointAllowance()then return false,'Not enough Ability Points. Go Back to adjust your selections.'end
  for q,limit in pairs(A.RarityLimits)do if cost[q]>limit then return false,q..' rarity limit exceeded. Go Back to adjust your selections.'end end
  for id,rank in pairs(state)do local e=A.byID[id]
   if e and rank>0 then
    if A.OtherClass(e.class)then return false,'A selection belongs to another class.'end
    if e.requiredMastery and (state[e.requiredMastery]or 0)<1 then return false,'A required Mastery is missing.'end
    if not A.IsTalent(e)and UnitLevel('player')<A.AbilityDisplayLevel(e)then return false,'Required level not met for '..e.name..'.'end
   end
  end
 end
 return true
end
function A.AcceptPreparation()
 return false,'Server committing is unavailable. Your pending changes have been retained.'
end

end


-- Independent progression profiles. Optional addons register preview modes; Classic is stock-safe.
do
local A=HeroFreePick
A.ModeDefinitions={Classic={name='Classic Character',classes=1,classic=true},ClassPlus={name='Class+',classes=1,tierLevels=true},Hybrid={name='Hybrid',classes=2,tierLevels=true},Hero={name='Hero',classes=10,tierLevels=true}}
A.InstalledModes={Classic=true}
A.mode='Classic'
function A.RegisterMode(id)if A.ModeDefinitions[id]then A.InstalledModes[id]=true end end
function A.Mode()return A.ModeDefinitions[A.mode]or A.ModeDefinitions.Classic end
local function ownClass()
 local _,token=UnitClass('player');for _,c in ipairs(A.classes)do if string.upper(c)==token then return c end end
 return nil
end
function A.OtherClass(class)
 if A.mode=='Hero'then return false end
 local own=ownClass();if class==own then return false end
 return not(A.mode=='Hybrid'and UnitLevel('player')>=10 and class==A.secondClass)
end
function A.SelectMode(id,second)
 if A.HasPendingChanges()or A.classicCommit then return false,'Finish or cancel pending changes before switching modes.'end
 if not A.InstalledModes[id]and not(id=='ClassPlus'and A.InstalledModes.Hybrid)then return false,'That mode package is not installed.'end
 if id=='Hybrid'and second then
  local found=false;for _,c in ipairs(A.classes)do if c==second then found=true end end
  if not found or second==ownClass()or UnitLevel('player')<10 then return false,'Choose a different second class at level 10 or later.'end
 end
 A.mode=id;A.secondClass=second
 -- Each optional mode has isolated local preview state; switching never grants server spells.
 HeroFreePickPlans.modePreviews=HeroFreePickPlans.modePreviews or {}
 local state=HeroFreePickPlans.modePreviews[id]or {entries={},previewLearned={}}
 HeroFreePickPlans.entries=state.entries;HeroFreePickPlans.previewLearned=state.previewLearned
 HeroFreePickPlans.modePreviews[id]=state;HeroFreePickPlans.pendingBaseline=nil
 A.BeginPreparation();return true,id=='Classic'and 'Classic: trainer abilities and native talent commit.'or 'Preview only: server commit is not enabled.'
end
local results=A.Results
function A.Results()
 local out={};for _,e in ipairs(results())do
  if A.mode~='Classic'or A.IsTalent(e)or(e.id<20000000 and not e.isMastery)then out[#out+1]=e end
 end;return out
end
function A.TalentNode(e)
 for _,node in ipairs(HeroFreePickTrees or {})do if node.talent==e.nativeTalent then return node end end
end
local begin=A.BeginPreparation
function A.BeginPreparation()
 A.Init()
 if A.mode=='Classic'and not HeroFreePickPlans.pendingBaseline then
  HeroFreePickPlans.previewLearned={}
  for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)then local _,_,rank=A.NativeTalent(e);if rank and rank>0 then HeroFreePickPlans.previewLearned[e.id]=rank end end end
 end
 begin()
end
function A.TalentRequiredLevel(e)local node=A.TalentNode(e);return node and (10+5*node.row)or 80 end
local setRank,setLearned=A.SetRank,A.SetLocalLearned
local function permitted(id,rank,key)
 local e=A.byID[id];if not e then return false end
 if A.classicCommit then A.ShowPointWarning('Waiting for the server to confirm talent learning.');return false end
 if A.mode=='Classic'and not A.IsTalent(e)then A.ShowPointWarning('Classic abilities are learned from trainers.');return false end
 if A.mode=='Classic'and A.IsTalent(e)and rank>((HeroFreePickPlans[key]or {})[id]or 0)then
  A.BeginPreparation()
  if UnitLevel('player')<10 then A.ShowPointWarning('Talents require level 10.');return false end
  local node=A.TalentNode(e)
  if not node then A.ShowPointWarning('This talent is unavailable.');return false end
  local state=HeroFreePickPlans[key]or {};local lower,dependencyRank,dependencyName=0,0,'prerequisite talent'
  for _,other in ipairs(HeroFreePickCatalog)do if other.class==e.class and A.IsTalent(other)then
   local n=A.TalentNode(other)
   if n then
    if n.spec==node.spec and n.row<node.row then lower=lower+(state[other.id]or 0)end
    if n.talent==node.depends then dependencyRank=state[other.id]or 0;dependencyName=other.name end
   end
  end end
  if lower<node.row*5 then A.ShowPointWarning('Requires '..node.row*5 ..' points in lower tiers of '..e.spec..'.');return false end
  if node.depends>0 and dependencyRank<math.max(1,node.dependsRank)then A.ShowPointWarning('Requires '..math.max(1,node.dependsRank)..' points in '..dependencyName..'.');return false end
 end
 if A.Mode().tierLevels and A.IsTalent(e)and rank>((HeroFreePickPlans[key]or {})[id]or 0)then
  local node=A.TalentNode(e)
  if not node or UnitLevel('player')<10+5*node.row then A.ShowPointWarning('This talent tier requires level '..(node and 10+5*node.row or '?')..'.');return false end
 end
 return true
end
function A.SetRank(id,rank)if not permitted(id,rank,'entries')then return false end;return setRank(id,rank)end
function A.SetLocalLearned(id,rank)if not permitted(id,rank,'previewLearned')then return false end;return setLearned(id,rank)end
function A.ValidateClassic()
 if InCombatLockdown and InCombatLockdown()then return false,'Cannot commit talents during combat.'end
 local state=HeroFreePickPlans.previewLearned or {};local total=0;local current=0;local nodes={};local ranks={};local queue={}
 for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)and not A.OtherClass(e.class)then
  local tab,index,rank,maxRank=A.NativeTalent(e);rank=rank or 0
  local wanted=state[e.id]or 0
  if wanted<rank then return false,'Committed talents must be reset at a trainer.'end
  if wanted>0 then
   local node=A.TalentNode(e);if not node or not tab or wanted>(maxRank or A.MaxRank(e))then return false,'Talent is unavailable in the stock client.'end
   nodes[node.talent]=node;ranks[node.talent]=wanted;total=total+wanted
   for nextRank=rank+1,wanted do queue[#queue+1]={entry=e,tab=tab,index=index,rank=nextRank,row=node.row}end
  end
  current=current+rank
 end end
 if total-current>A.NativeTalentPoints()then return false,'Not enough unspent native Talent Points.'end
 for id,node in pairs(nodes)do
  local lower=0;for other,n in pairs(nodes)do if n.spec==node.spec and n.row<node.row then lower=lower+ranks[other]end end
  if lower<node.row*5 then return false,'Classic talents require five points in lower tiers per row.'end
  if node.depends>0 and (ranks[node.depends]or 0)<math.max(1,node.dependsRank) then return false,'A Classic talent prerequisite is missing.'end
 end
 table.sort(queue,function(a,b)if a.row~=b.row then return a.row<b.row end;if a.entry.id~=b.entry.id then return a.entry.id<b.entry.id end;return a.rank<b.rank end)
 return true,queue
end
function A.AcceptPreparation()
 if A.mode~='Classic'then return false,'This mode is a local preview. The server learning/refund integration is not enabled yet.'end
 if A.view=='architect'then return false,'Archetype Builder is a separate draft. Set the desired ranks in Hero Advancement to learn them.'end
 local ok,queue=A.ValidateClassic();if not ok then return false,queue end
 if #queue==0 then return false,'No new native talent ranks to learn. Committed ranks require a trainer reset.'end
 if A.classicCommit then return false,'Waiting for server confirmation.'end
 A.classicCommit={queue=queue,index=1,elapsed=0,sent=false}
 return false,'Learning talents; waiting for the server to confirm each rank.'
end
function A.PollClassicCommit(elapsed)
 local job=A.classicCommit;if not job then return end
 local item=job.queue[job.index]
 if not item then
  A.classicCommit=nil;HeroFreePickPlans.pendingBaseline=nil;A.BeginPreparation()
  if A.ClassicCommitResult then A.ClassicCommitResult(true,'Talents confirmed by the server.')end;return
 end
 local tab,index,rank=A.NativeTalent(item.entry)
 if not tab or (InCombatLockdown and InCombatLockdown())then
  A.classicCommit=nil;if A.ClassicCommitResult then A.ClassicCommitResult(false,'Commit interrupted. Any ranks already confirmed remain learned; visit a trainer to reset them.')end;return
 end
 if rank>=item.rank then job.index=job.index+1;job.elapsed=0;job.sent=false;return end
 if not job.sent then LearnTalent(tab,index);job.sent=true end
 job.elapsed=job.elapsed+elapsed
 if job.elapsed>5 then A.classicCommit=nil;if A.ClassicCommitResult then A.ClassicCommitResult(false,'The server did not confirm the talent. Earlier confirmed ranks remain learned; verify your character before retrying.')end end
end
local cancel=A.CancelPreparation
function A.CancelPreparation()
 if A.classicCommit then return false end
 cancel()
 if A.mode=='Classic'then HeroFreePickPlans.pendingBaseline=nil;A.BeginPreparation()end
 return true
end
end

do
local A=HeroFreePick
function A.ClassPlusChoiceTooltip()
 local text='Choose abilities and talents from your original class within free-pick resource limits.'
 if A.InstalledModes.Hybrid then return text..' At level 10, you may continue as Class+ or become Hybrid and choose a second class.'end
 return text..' The option to become Hybrid at level 10 requires the Hybrid module.'
end
function A.ModeChoiceDue(level)
 level=level or UnitLevel('player')
 if not HeroFreePickPlans.progressionChoice and level==1 then return 'initial'end
 local choice=HeroFreePickPlans.progressionChoice
 if choice and choice.mode=='ClassPlus'and level>=10 and not choice.hybridDecision and A.InstalledModes.Hybrid then return 'hybrid'end
end
function A.ChooseInitialMode(id)
 if UnitLevel('player')~=1 or id=='Hybrid'then return false,'Progression mode can only be changed at level 1.'end
 local ok,why=A.SelectMode(id);if not ok then return false,why end
 HeroFreePickPlans.progressionChoice={mode=id};return true
end
function A.ChooseHybridPath(second)
 if A.ModeChoiceDue()~='hybrid'then return false,'Hybrid selection is not available.'end
 if second then
  local _,own=UnitClass('player');local valid=false
  for _,class in ipairs(A.classes)do if class==second and string.upper(class)~=own then valid=true end end
  if not valid then return false,'Choose a different second class.'end
  if A.classicCommit then return false,'Wait for the current commit to finish.'end
  -- Hybrid expands the same build; preserve pending edits instead of trapping the choice behind a review.
  A.mode='Hybrid';A.secondClass=second
  HeroFreePickPlans.modePreviews=HeroFreePickPlans.modePreviews or {}
  HeroFreePickPlans.modePreviews.Hybrid={entries=HeroFreePickPlans.entries,previewLearned=HeroFreePickPlans.previewLearned}
  HeroFreePickPlans.progressionChoice={mode='Hybrid',secondClass=second,hybridDecision=true}
 else HeroFreePickPlans.progressionChoice.hybridDecision=true end
 return true
end
end

do
local A=HeroFreePick
local allowance=A.TalentPointAllowance
function A.TalentPointAllowance()
 if A.mode~='Classic'then return allowance()end
 local total=A.NativeTalentPoints()
 for _,e in ipairs(HeroFreePickCatalog)do if A.IsTalent(e)and not A.OtherClass(e.class)then local _,_,rank=A.NativeTalent(e);total=total+(rank or 0)end end
 return total
end
end

-- Classic learned abilities are read from the player's spellbook, never from preview ownership.
function A.ClassicSpellbookEntries()
 local out,seen={},{}
 if not GetNumSpellTabs or not GetSpellTabInfo or not GetSpellLink then return out end
 local bySpell,byName={},{}
 for _,e in ipairs(HeroFreePickCatalog)do
  if e.id<20000000 and not e.isMastery and not A.OtherClass(e.class)then
   for _,spell in ipairs(e.spells)do bySpell[spell]=e;local name=GetSpellInfo(spell);if name then byName[name]=e end end
  end
 end
 for tab=1,GetNumSpellTabs()do
  local _,_,offset,count=GetSpellTabInfo(tab)
  for slot=(offset or 0)+1,(offset or 0)+(count or 0)do
   local link=GetSpellLink(slot,BOOKTYPE_SPELL or 'spell')
   local spell=link and tonumber(link:match('spell:(%d+)'))
   if spell then
    local known=bySpell[spell]or byName[GetSpellInfo(spell)]
    if known and not A.IsTalent(known)and not seen[known.id]then
     local copy={};for k,v in pairs(known)do copy[k]=v end
     copy.spellbookKnown=true;copy.spellbookSpell=spell
     out[#out+1]=copy;seen[known.id]=copy
    elseif known and seen[known.id]then seen[known.id].spellbookSpell=spell end
   end
  end
 end
 return out
end
local plannedLearned=A.LearnedEntries
function A.LearnedEntries()
 if A.mode~='Classic'then return plannedLearned()end
 local out=A.ClassicSpellbookEntries()
 for _,e in ipairs(plannedLearned())do if A.IsTalent(e)then out[#out+1]=e end end
 table.sort(out,function(a,b)if a.name==b.name then return a.id<b.id end;return a.name<b.name end)
 return out
end

-- Stock AzerothCore trainer_spell reference; presentation only, never custom-mode requirements.
A.ClassicTrainerLevels={[1]=20,[2]=6,[3]=4,[4]=68,[6]=12,[8]=10,[10]=4,[11]=8,[12]=26,[13]=10,[14]=22,[15]=12,[16]=22,[17]=26,[19]=12,[20]=8,[22]=4,[23]=8,[25]=8,[26]=3,[28]=12,[30]=30,[31]=32,[32]=20,[33]=1,[34]=6,[35]=68,[36]=18,[37]=6,[38]=16,[39]=18,[40]=14,[41]=20,[42]=28,[43]=32,[44]=30,[46]=8,[47]=6,[48]=12,[49]=4,[50]=30,[51]=60,[52]=12,[53]=30,[54]=10,[56]=34,[57]=18,[60]=1,[61]=14,[63]=18,[64]=16,[66]=20,[67]=4,[68]=14,[69]=28,[71]=30,[72]=12,[73]=28,[74]=20,[75]=18,[76]=4,[77]=4,[78]=16,[79]=20,[80]=16,[81]=20,[82]=8,[83]=28,[84]=20,[85]=4,[86]=30,[87]=8,[88]=14,[89]=18,[90]=10,[91]=26,[92]=18,[93]=40,[94]=16,[95]=20,[96]=20,[97]=30,[98]=10,[100]=1,[101]=6,[102]=8,[103]=14,[104]=26,[105]=1,[106]=14,[107]=6,[108]=1,[109]=20,[110]=30,[111]=32,[112]=16,[113]=20,[114]=40,[115]=14,[116]=12,[117]=32,[118]=36,[119]=34,[120]=26,[121]=8,[122]=50,[123]=22,[125]=12,[126]=6,[127]=1,[128]=16,[129]=24,[130]=26,[131]=30,[132]=26,[133]=22,[134]=40,[135]=20,[136]=30,[137]=20,[138]=16,[139]=4,[140]=10,[141]=12,[143]=20,[144]=66,[145]=34,[146]=22,[148]=16,[149]=6,[150]=24,[151]=36,[154]=6,[155]=16,[156]=18,[157]=18,[158]=16,[159]=10,[160]=24,[161]=50,[162]=70,[163]=24,[165]=26,[166]=68,[167]=22,[168]=20,[169]=20,[170]=22,[172]=12,[173]=10,[174]=36,[175]=22,[176]=6,[177]=26,[178]=70,[180]=64,[181]=42,[182]=8,[183]=16,[184]=24,[185]=8,[186]=10,[189]=28,[190]=14,[191]=20,[192]=24,[193]=22,[194]=12,[195]=22,[196]=8,[197]=24,[198]=30,[200]=40,[202]=4,[203]=26,[204]=18,[205]=16,[206]=8,[207]=20,[208]=8,[209]=70,[210]=34,[211]=22,[212]=26,[213]=14,[214]=10,[215]=32,[216]=6,[217]=20,[218]=48,[219]=28,[221]=38,[222]=14,[223]=1,[224]=10,[225]=32,[226]=42,[229]=46,[230]=16,[232]=12,[234]=20,[235]=1,[236]=10,[237]=20,[238]=4,[239]=10,[240]=20,[242]=10,[243]=10,[244]=14,[245]=24,[246]=18,[247]=38,[248]=30,[249]=24,[250]=28,[251]=26,[252]=28,[253]=30,[254]=32,[255]=14,[256]=18,[257]=4,[258]=12,[260]=28,[261]=36,[262]=20,[263]=24,[264]=30,[265]=20,[266]=40,[267]=30,[268]=4,[269]=10,[270]=16,[271]=28,[272]=34,[273]=30,[274]=20,[275]=20,[276]=10,[277]=18,[278]=40,[279]=32,[282]=60,[283]=4,[284]=14,[285]=22,[286]=20,[287]=30,[288]=60,[289]=28,[290]=10,[291]=24,[292]=32,[293]=36,[294]=46,[295]=22,[296]=30,[297]=38,[298]=20,[299]=20,[300]=30,[302]=20,[303]=30,[304]=12,[306]=32,[307]=62,[308]=44,[309]=36,[310]=64,[311]=40,[312]=44,[313]=16,[314]=20,[315]=64,[316]=70,[317]=62,[318]=40,[319]=64,[320]=66,[321]=68,[322]=70,[323]=64,[324]=66,[325]=62,[326]=66,[327]=14,[328]=64,[329]=70,[330]=62,[332]=62,[333]=64,[334]=62,[335]=68,[336]=66,[337]=64,[338]=70,[340]=66,[341]=20,[342]=6,[343]=66,[344]=70,[345]=68,[346]=30,[347]=75,[348]=70,[349]=75,[350]=30,[351]=75,[352]=80,[354]=75,[355]=80,[356]=12,[357]=75,[358]=80,[359]=20,[360]=80,[361]=30,[362]=20,[363]=75,[364]=75,[365]=71,[366]=28,[367]=12,[368]=75,[369]=80,[370]=71,[371]=80,[372]=75,[373]=50,[374]=80,[375]=75,[376]=16,[377]=80,[378]=74,[379]=71,[380]=16,[381]=40,[382]=80,[383]=71,[384]=80,[385]=80,[386]=30,[387]=40,[388]=50,[1154]=61,[1155]=80,[1156]=60,[1159]=58,[1160]=64,[1162]=56,[1163]=59,[1164]=57,[1166]=75,[1167]=57,[1168]=70,[1170]=68,[1171]=58,[1172]=66,[1173]=62,[1174]=61,[1177]=56,[1178]=56,[1180]=65,[1181]=67,[1182]=65,[1184]=72,[2663]=4}
function A.AbilityDisplayLevel(e)
 if A.mode=="Classic"and not A.IsTalent(e)then return A.ClassicStartingLevels[e.id]or (A.ClassicSupplementSources[e.id]and A.ClassicSupplementSources[e.id].level)or A.ClassicTrainerLevels[e.id]or 999 end
 return A.MasteryMemberLevel and A.MasteryMemberLevel(e)or e.level
end

-- Quest reward display-spell matches from the stock world database.
A.ClassicQuestSources={[60]={1470,1485,1598,1599,8344},[62]={1795},[65]={1471,1504,1689,9619},[70]={1474,1513,1739},[99]={7603},[169]={5644,5646,5679},[179]={1527,9555},[199]={96,9509},[217]={5641,5645,5647,10377},[231]={1785,1788,9600,9685},[241]={1518,1521,9451},[280]={7583}}
function A.LearningSourceLines(e)
 local lines={}
 if A.mode~='Classic'or A.IsTalent(e)then return lines end
 if A.ClassicStartingLevels[e.id]then return {'Learned at character creation.','Stock learning-source reference; server changes may differ.'}end
 if A.ClassicSupplementSources[e.id]then
  return {'Learned from '..A.ClassicSupplementSources[e.id].label..'.','Stock learning-source reference; server changes may differ.'}
 end
 if A.ClassicTrainerLevels[e.id]then lines[#lines+1]='Learned from a Trainer (level '..A.ClassicTrainerLevels[e.id]..').'end
 local quests=A.ClassicQuestSources[e.id]
 if quests then lines[#lines+1]='Learned from a Quest.'end
 if #lines>0 then lines[#lines+1]='Stock learning-source reference; server changes may differ.'end
 return lines
end

A.ClassicTrainerLevels[19001494]=2

A.ClassicSupplementSources={[19100000]={level=55,label="Class Quest"},
[19100001]={level=55,label="Class Quest"},
[19100002]={level=55,label="Trainer"},
[19100003]={level=60,label="Trainer"},
[19100004]={level=55,label="Trainer"},
[19100005]={level=57,label="Trainer"},
[19100006]={level=57,label="Trainer"},
[19100007]={level=63,label="Trainer"},
[19100008]={level=63,label="Trainer"},
[19100009]={level=70,label="Trainer"},
[19100010]={level=72,label="Trainer"},
[19100011]={level=72,label="Trainer"},
[19100012]={level=40,label="Trainer"},
[19100013]={level=40,label="Trainer"},
[19100014]={level=50,label="Trainer"},
[19100015]={level=70,label="Class Quest / Trainer"},
[19100016]={level=32,label="Trainer"},
[19100017]={level=24,label="Trainer"},
[19100018]={level=10,label="Class Quest"},
[19100019]={level=10,label="Class Quest"},
[19100020]={level=20,label="Trainer"},
[19100021]={level=10,label="Class Quest"},
[19100022]={level=40,label="Trainer"},
[19100023]={level=8,label="Trainer"},
[19100024]={level=10,label="Class Quest"},
[19100025]={level=10,label="Class Quest"},
[19100026]={level=32,label="Trainer"},
[19100027]={level=50,label="Trainer"},
[19100028]={level=26,label="Trainer"},
[19100029]={level=40,label="Trainer"},
[19100030]={level=18,label="Trainer"},
[19100031]={level=56,label="Trainer"},
[19100032]={level=30,label="Trainer"},
[19100033]={level=74,label="Trainer"},
[19100034]={level=50,label="Trainer"},
[19100035]={level=40,label="Trainer"},
[19100036]={level=40,label="Trainer"},
[19100037]={level=40,label="Trainer"},
[19100038]={level=65,label="Trainer"},
[19100039]={level=40,label="Trainer"},
[19100040]={level=35,label="Trainer"},
[19100041]={level=40,label="Trainer"},
[19100042]={level=35,label="Trainer"},
[19100043]={level=50,label="Trainer"},
[19100044]={level=40,label="Trainer"},
[19100045]={level=71,label="Class Quest / Trainer"},
[19100046]={level=30,label="Trainer"},
[19100047]={level=20,label="Trainer"},
[19100048]={level=20,label="Trainer"},
[19100049]={level=20,label="Trainer"},
[19100050]={level=60,label="Trainer"},
[19100051]={level=20,label="Trainer"},
[19100052]={level=20,label="Trainer"},
[19100053]={level=20,label="Trainer"},
[19100054]={level=20,label="Trainer"},
[19100055]={level=30,label="Trainer"},
[19100056]={level=20,label="Trainer"},
[19100057]={level=40,label="Class Quest / Trainer"},
[19100058]={level=60,label="Trainer"},
[19100059]={level=52,label="Trainer"},
[19100060]={level=60,label="Trainer"},
[19100061]={level=54,label="Trainer"},
[19100062]={level=8,label="Trainer"},
[19100063]={level=40,label="Trainer"},
[19100064]={level=66,label="Trainer"},
[19100065]={level=20,label="Class Quest / Trainer"},
[19100066]={level=40,label="Class Quest / Trainer"},
[19100067]={level=20,label="Class Quest / Trainer"},
[19100068]={level=20,label="Class Quest / Trainer"},
[19100069]={level=40,label="Trainer"},
[19100070]={level=16,label="Trainer"},
[19100071]={level=70,label="Trainer"},
[19100072]={level=48,label="Trainer"},
[19100073]={level=56,label="Trainer"},
[19100074]={level=60,label="Trainer"},
[19100075]={level=10,label="Trainer"},
[19100076]={level=12,label="Trainer"},
[19100077]={level=70,label="Trainer"},
[19100078]={level=40,label="Trainer"},
[19100079]={level=34,label="Trainer"},
[19100080]={level=20,label="Trainer"},
[19100081]={level=80,label="Trainer"},
[19100082]={level=40,label="Class Quest / Trainer"},
[19100083]={level=20,label="Class Quest / Trainer"},
[19100084]={level=24,label="Trainer"},
[19100085]={level=20,label="Trainer"},
[19100086]={level=6,label="Trainer"},
[19100087]={level=40,label="Trainer"},
[19100088]={level=20,label="Trainer"}}

A.ClassicStartingLevels={[21]=1,[18]=1,[7]=1,[152]=1,[124]=1,[171]=1,[142]=1,[45]=1,[19200000]=1,[147]=1,[59]=1,[24]=1,[29]=1,[188]=1,[187]=1,[58]=1,[55]=1,[305]=1,[1161]=55,[1169]=55,[1175]=55,[1158]=55,[19200001]=55,[1183]=55,[1157]=55,[1165]=55,[1176]=55,[19200002]=55}

-- Shared starting skill 118: class mask 40 includes Rogue and Death Knight.
-- Creation ownership takes precedence over redundant trainer records.
A.ClassicStartingLevels[19100075]=1 -- Rogue Dual Wield (spell 674)

-- Footer actions restore draft baselines; they never erase confirmed server ownership.
function A.HasPendingSelection(kind)
 local base=HeroFreePickPlans and HeroFreePickPlans.pendingBaseline
 if not base then return false end
 for _,key in ipairs({'previewLearned','entries'})do
  local state=HeroFreePickPlans[key]or {};local original=base[key]or {};local ids={}
  for id in pairs(state)do ids[id]=true end;for id in pairs(original)do ids[id]=true end
  for id in pairs(ids)do local e=A.byID[id]
   if e and(kind=='All'or(A.IsTalent(e)and kind=='Talents')or(not A.IsTalent(e)and kind=='Abilities'))and(state[id]or 0)~=(original[id]or 0)then return true end
  end
 end
 return false
end
function A.ResetPendingSelection(kind)
 if A.classicCommit then return false,'Wait for the talent application to finish.'end
 if A.mode=='Classic'and kind~='Talents'then return false,'Classic characters can only reset pending talents.'end
 if kind~='Abilities'and kind~='Talents'and kind~='All'then return false,'Unknown reset selection.'end
 if not A.HasPendingSelection(kind)then return false,'No pending changes in this category.'end
 A.BeginPreparation()
 local base=HeroFreePickPlans.pendingBaseline
 for _,key in ipairs({'previewLearned','entries'})do
  local state=HeroFreePickPlans[key]or {};local original=base[key]or {};local ids={}
  for id in pairs(state)do ids[id]=true end;for id in pairs(original)do ids[id]=true end
  for id in pairs(ids)do local e=A.byID[id]
   if e and(kind=='All'or(A.IsTalent(e)and kind=='Talents')or(not A.IsTalent(e)and kind=='Abilities'))then state[id]=original[id]end
  end
  HeroFreePickPlans[key]=state
 end
 if A.SyncMasteryGrants then A.SyncMasteryGrants()end
 return true
end
function A.FooterActions(action)
 local classic=A.mode=='Classic';local busy=A.classicCommit~=nil
 if action=='Apply'then
  return {{label='Apply Pending Talents',enabled=classic and not busy and A.HasPendingSelection('Talents'),run=function()if A.HasPendingSelection('Talents')and not A.classicCommit then A.ShowPendingReview()end end},
   {label='Accept Pending Abilities and Talents',enabled=not classic and not busy and A.HasPendingChanges(),run=function()if A.HasPendingChanges()and not A.classicCommit then A.ShowPendingReview()end end}}
 elseif action=='Pending'then
  local out={}
  for _,kind in ipairs({'Abilities','Talents','All'})do local selection=kind
   out[#out+1]={label='Reset Pending '..(kind=='All'and 'Abilities and Talents'or kind),enabled=not busy and(not classic or kind=='Talents')and A.HasPendingSelection(kind),run=function()
    local ok,why=A.ResetPendingSelection(selection);if not ok then A.ShowPointWarning(why)else A.Refresh()end
   end}
  end
  return out
 end
 return {{label='Reset Learned Abilities',enabled=false},{label='Reset Learned Talents (trainer price)',enabled=false},{label='Reset Learned Abilities and Talents',enabled=false}}
end
