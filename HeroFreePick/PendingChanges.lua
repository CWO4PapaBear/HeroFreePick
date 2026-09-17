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
