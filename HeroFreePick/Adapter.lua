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
 if A.ModeChoiceDue()~='initial'or id=='Hybrid'then return false,'Initial choice is only available on first arrival at level 1.'end
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
