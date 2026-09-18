local A,C=HeroFreePick,HeroCommitCatalog
local revision,confirmed,job,reply
local serial=math.floor((GetTime()or 0)*1000)%100000000
local function subject()return A.ServerPathEnrolled==true and A.mode=='ClassPlus'end
local function derive(state,level)
 if not state then return end
 level=level or UnitLevel('player')
 for id in pairs(state)do local e=A.byID[id];if e and (e.requiredMastery or e.requiredBundle)and not C.entries[id]then state[id]=nil end end
 for id,e in pairs(C.entries)do if e.parent~=0 then state[id]=(state[e.parent]and C.entries[e.parent]and level>=C.entries[e.parent].level and level>=e.level)and 1 or nil end end
end
local sync=A.SyncMasteryGrants
local members=A.MasteryTooltipMembers
if members then
 function A.MasteryTooltipMembers(m)
  local list=members(m);if not subject()then return list end
  for _,item in ipairs(list)do
   local available=false
   for id,e in pairs(C.entries)do if e.parent==m.id then
    for _,spell in ipairs((A.byID[id]or {}).spells or {})do if spell==item.spell then available=true end end
   end end
   if not available then item.name=item.name..' (unavailable in this server test)'end
  end
  return list
 end
end
function A.SyncMasteryGrants(level)
 sync(level)
 if not subject()or not HeroFreePickPlans then return end
 for _,key in ipairs({'entries','previewLearned'})do
  derive(HeroFreePickPlans[key],level)
  if HeroFreePickPlans.pendingBaseline then derive(HeroFreePickPlans.pendingBaseline[key],level)end
 end
end
local function encode(state)
 local ids={};local ap=0;local gems={0,0,0,0};local caps={11,16,13,7}
 for id,rank in pairs(state or {})do
  local e=C.entries[id]
  local talent=A.byID[id]
  if not e and talent and A.IsTalent(talent)then return nil,'Server talent applying is not implemented yet: '..talent.name..'. Remove the pending talent changes to apply abilities; your draft has been kept.'end
  if not e or rank~=1 then return nil,'Not supported by this server test: '..((A.byID[id]or {}).name or tostring(id))end
  if e.level>UnitLevel('player')then return nil,((A.byID[id]or {}).name or ('Ability '..id))..' requires level '..e.level..'.'end
  if e.parent~=0 then
   if not state[e.parent]then return nil,'Requires its controlling Mastery or bundle.'end
  else
   local _,token=UnitClass('player');if e.class:upper():gsub(' ','')~=token then return nil,'Class access denied.'end
   ids[#ids+1]=id;ap=ap+e.ap;if e.rarity>0 then gems[e.rarity]=gems[e.rarity]+e.gems end
  end
 end
 if ap>math.max(9,UnitLevel('player'))then return nil,'Not enough Ability Points.'end
 for i=1,4 do if gems[i]>caps[i]then return nil,'Rarity budget exceeded.'end end
 table.sort(ids);return #ids==0 and '-'or table.concat(ids,',')
end
local function parse(text)
 local state={};if text=='-'then return state end
 for value in text:gmatch('[^,]+')do
  if not value:match('^%d+$')then return end
  local id=tonumber(value);local e=C.entries[id]
  if not e or e.parent~=0 or state[id]then return end;state[id]=1
 end
 if encode(state)~=text then return end
 derive(state);return state
end
local function chunks(text)
 local out,part={},''
 for id in text:gmatch('[^,]+')do
  if #part+#id+1>140 then out[#out+1]=part;part=''end
  part=part==''and id or part..','..id
 end
 out[#out+1]=part;return out
end
local function requestStatus()SendChatMessage('.hfbuild status','SAY')end
local function finish(ok,why)
 job=nil;reply=nil;A.classicCommit=nil
 if A.ClassicCommitResult then A.ClassicCommitResult(ok,why)elseif not ok then A.ShowPointWarning(why)end
end
local function install(state)
 HeroFreePickPlans.previewLearned=state
 HeroFreePickPlans.modePreviews=HeroFreePickPlans.modePreviews or {}
 HeroFreePickPlans.modePreviews.ClassPlus=HeroFreePickPlans.modePreviews.ClassPlus or {}
 HeroFreePickPlans.modePreviews.ClassPlus.previewLearned=state
 HeroFreePickPlans.pendingBaseline=nil;A.BeginPreparation();A.Refresh(true)
end
local original=A.AcceptPreparation
function A.AcceptPreparation()
 if not subject()then return original()end
 if job or A.classicCommit then return false,'Waiting for server confirmation.'end
 if A.view=='architect'then return false,'Use Hero Advancement for this server test.'end
 if not revision then requestStatus();return false,'Synchronizing the server build. Retry after confirmation.'end
 local base=HeroFreePickPlans.pendingBaseline or {}
 for _,key in ipairs({'entries','primaryStat'})do
  local function same(a,b)
   if type(a)~='table'or type(b)~='table'then return a==b end
   for k,v in pairs(a)do if b[k]~=v then return false end end
   for k,v in pairs(b)do if a[k]~=v then return false end end;return true
  end
  if not same(HeroFreePickPlans[key],base[key])then return false,'Only ability changes are supported. Cancel other pending edits first.'end
 end
 local text,why=encode(HeroFreePickPlans.previewLearned);if not text then return false,why end
 if text==confirmed then return false,'No ability changes to apply.'end
 serial=serial+1;local parts=chunks(text)
 local queue={'.hfbuild start '..C.version..' '..revision..' '..serial..' '..#parts}
 for i,part in ipairs(parts)do queue[#queue+1]='.hfbuild part '..serial..' '..i..' '..part end
 queue[#queue+1]='.hfbuild apply '..serial
 job={text=text,age=0,revision=revision,token=serial,queue=queue,next=1,delay=0};A.classicCommit={heroBuild=true};return false
end
for _,key in ipairs({'SetLocalLearned','SetRank'})do
 local setter=A[key]
 A[key]=function(id,rank)
  if job then return false end
  if subject()then
   -- Resolve talent-tree ability aliases before the server ability allowlist.
   local entry=A.byID[id]
   local resolved=entry and A.AbilityForTalent(entry)or entry
   if resolved then id=resolved.id end
   -- Passive talents remain editable drafts; the commit encoder below explains
   -- their unsupported server state without blocking ordinary point planning.
   if tonumber(rank)and rank>0 and not C.entries[id]and not(resolved and A.IsTalent(resolved))then
    A.ShowPointWarning('Not available on this server: '..(resolved and resolved.name or tostring(id))..'.');return false
   end
  end
  local ok=setter(id,rank);if ok then A.SyncMasteryGrants()end;return ok
 end
end
local poll=A.PollClassicCommit
function A.PollClassicCommit(dt)
 if not job then return poll(dt)end
 job.age=job.age+dt;job.delay=job.delay+dt
 if job.age>55 then finish(false,'No server confirmation received. Use .hfbuild status before retrying. Your draft is retained.');return end
 if job.delay>=0.2 and job.queue[job.next]then
  local command=job.queue[job.next];job.next=job.next+1;job.delay=0;SendChatMessage(command,'SAY')
 end
end
local errors={MODE='Choose Class+ and wait for server enrollment confirmation first.',LEVEL='Required level not met.',COMBAT='Leave combat before applying changes.',VERSION='Client/server catalogs differ.',FORMAT='Invalid build format.',UNSUPPORTED='Selection unsupported by this test.',AP='Not enough Ability Points.',RARITY='Rarity budget exceeded.',CLASS='Class access denied.',STALE='Server build changed. Use .hfbuild status before retrying.',UPLOAD='Incomplete upload. Use .hfbuild status before retrying.',CLEAR_BUILD_FIRST='Remove purchased abilities before choosing Classic.',RECOVERY='Build saved but not fully applied. Use .hfbuild status to retry and keep the test logs.',DATABASE='Could not save the build.',SPELL_MISSING='Required server spell data is missing.'}
local frame=CreateFrame('Frame')
frame:RegisterEvent('PLAYER_LOGIN');frame:RegisterEvent('CHAT_MSG_SYSTEM')
frame:SetScript('OnEvent',function(_,event,message)
 if not subject()then return end
 if event=='PLAYER_LOGIN'or message=='HF_PATH CLASSPLUS'then requestStatus();return end
 if not message then return end
 local code=message:match('^HF_BUILD ERR (%u+[_%u]*)$')
 if code then local why=errors[code]or code;if job then finish(false,why)else A.ShowPointWarning(why)end;reply=nil;return end
 local v,rev,token,count=message:match('^HF_BUILD BEGIN (%d+) (%d+) (%d+) (%d+)$')
 if v then
  token=tonumber(token);rev=tonumber(rev);count=tonumber(count)
  if job and token~=job.token or not job and token~=0 then return end
  reply=nil
  if tonumber(v)~=C.version then if job then finish(false,errors.VERSION)else A.ShowPointWarning(errors.VERSION)end;return end
  if count<1 or count>64 or revision and rev<revision then return end
  reply={token=token,revision=rev,count=count,parts={},next=1};return
 end
 local t,index,part=message:match('^HF_BUILD PART (%d+) (%d+) ([%d,%-]+)$')
 if t then
  if not reply or tonumber(t)~=reply.token then return end
  if tonumber(index)~=reply.next or reply.next>reply.count or #part>140 then reply=nil;return end
  reply.parts[#reply.parts+1]=part;reply.next=reply.next+1;return
 end
 local done=message:match('^HF_BUILD END (%d+)$')
 if not done or not reply or tonumber(done)~=reply.token then return end
 local result=reply;reply=nil;if result.next~=result.count+1 then return end
 local text=table.concat(result.parts,',');local state=parse(text);if not state then return end
 if job and (text~=job.text or result.revision<job.revision)then return end
 revision=result.revision;confirmed=text
 if job then install(state);finish(true);return end
 if A.HasPendingChanges()then
  if HeroFreePickPlans.pendingBaseline then HeroFreePickPlans.pendingBaseline.previewLearned=state end
  A.ShowPointWarning('Server build synchronized. Your pending draft is unchanged.');return
 end
 install(state)
end)
