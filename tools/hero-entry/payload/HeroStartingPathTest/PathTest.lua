local A=HeroFreePick
-- Hide successful transport replies only from chat display. Our independent
-- CHAT_MSG_SYSTEM handlers still receive them; errors and player warnings stay visible.
local quietPath={['HF_PATH PENDING']=true,['HF_PATH CLASSIC']=true,
 ['HF_PATH CLASSPLUS']=true,['HF_PATH HERO']=true,['HF_PATH LEGACY_CLASSIC']=true}
ChatFrame_AddMessageEventFilter('CHAT_MSG_SYSTEM',function(_,_,message)
 if type(message)~='string'then return false end
 return message=='HF_RESET_OPEN'or message:match('^HF_RESET %d+ %d+ [01]$')~=nil or quietPath[message]or message:match('^HF_BUILD BEGIN %d+ %d+ %d+ %d+ %d+$')~=nil
  or message:match('^HF_BUILD PART %d+ %d+ [%d,%-]+$')~=nil
  or message:match('^HF_BUILD END %d+$')~=nil
end)
local function subject()return A.ServerPathEnrolled==true end
local function startLevel()local _,class=UnitClass('player');return class=='DEATHKNIGHT'and (UnitLevel('player')==1 and 1 or 55)or 1 end
local due=A.ModeChoiceDue
function A.ModeChoiceDue(level)
 if subject()and not HeroFreePickPlans.progressionChoice and (level or UnitLevel('player'))==startLevel()then return 'initial'end
 if subject()then return due(level)end
 return nil
end
-- The server snapshot, never a name or local saved variable, establishes enrollment.
if subject()then A.RegisterMode('ClassPlus');A.RegisterMode('Hero')end
local requestedMode
local choose=A.ChooseInitialMode
function A.ChooseInitialMode(mode)
 if A.ServerStartPending then return false,"The server is preparing your starting level and location."end
 if not subject()then return false,'Waiting for server enrollment. Existing unenrolled characters remain Classic.'end
 if UnitLevel('player')~=startLevel()then return false,'This test selection requires the starting level for your class.'end
 if mode~='Classic'and mode~='ClassPlus'and mode~='Hero'then return false,'Choose Classic, Class+ or Hero.'end
 if A.HasPendingChanges()or A.classicCommit then return false,'Finish or cancel pending changes first.'end
 requestedMode=mode
 SendChatMessage(mode=='Hero'and '.hfpath hero'or mode=='Classic'and '.hfpath classic'or '.hfpath classplus','SAY')
 return false,'Waiting for the server to confirm your starting path.'
end
local show=A.ShowModeChoice
function A.ShowModeChoice(level,reopen)
 if subject()then A.RegisterMode('ClassPlus');A.RegisterMode('Hero')end
 show(level,reopen)

end
local frame=CreateFrame('Frame')
frame:RegisterEvent('PLAYER_LOGIN');frame:RegisterEvent('CHAT_MSG_SYSTEM')
frame:SetScript('OnEvent',function(_,event,message)
 if event=='PLAYER_LOGIN'then A.ServerPathEnrolled=nil;SendChatMessage('.hfpath status','SAY');return end
 if message=='HF_PATH START_PENDING'then A.ServerStartPending=true;return end
 if message=='HF_PATH START_BLOCKED'then
  A.ShowPointWarning('Change your starting path before gaining XP or starting quests. Clear your build, leave combat, and leave space in your bank and bags.');return
 end
 if message=='HF_PATH CLASSIC'or (message=='HF_PATH CLASSPLUS'or message=='HF_PATH HERO')then A.ServerStartPending=nil end
 if message=='HF_PATH PENDING'or message=='HF_PATH CLASSIC'or (message=='HF_PATH CLASSPLUS'or message=='HF_PATH HERO')then A.ServerPathEnrolled=true;A.RegisterMode('ClassPlus');A.RegisterMode('Hero')end
 if message=='HF_PATH LEGACY_CLASSIC'then
  A.ServerPathEnrolled=false
  local ok,why=A.SelectMode('Classic')
  if not ok then A.ShowPointWarning(why or 'Cancel pending edits, then use .hfpath status.');return end
  HeroFreePickPlans.progressionChoice={mode='Classic'};HeroProgressionChoice:Hide();A.Refresh(true);return
 end
 if message=='HF_PATH PENDING'then
  HeroFreePickPlans.progressionChoice=nil;A.ShowModeChoice(nil,true)
 elseif message=='HF_PATH CLASSIC'or (message=='HF_PATH CLASSPLUS'or message=='HF_PATH HERO')then
  if A.HasPendingChanges()or A.classicCommit then
   A.ShowPointWarning('The server saved your path. Finish or cancel pending edits, then use .hfpath status to synchronize.');return
  end
  local mode=message=='HF_PATH HERO'and 'Hero'or message=='HF_PATH CLASSIC'and 'Classic'or 'ClassPlus'
  A.RegisterMode('ClassPlus');A.RegisterMode('Hero')
  local ok,why=A.SelectMode(mode)
  if ok then
   HeroFreePickPlans.progressionChoice={mode=mode};HeroProgressionChoice:Hide();A.Refresh(true)
   if requestedMode==mode and mode~='Classic'and A.QueueAdvancementOpen then A.QueueAdvancementOpen('choice')end
   requestedMode=nil
  else A.ShowPointWarning(why or 'Unable to synchronize the server path.')end
 elseif message=='HF_PATH ERROR'or message=='HF_PATH NOT_ENROLLED'then
  A.ShowPointWarning('The server could not verify enrollment or saved starting spells. No mode change was approved.')
 elseif message=='HF_PATH CHOICE_BLOCKED'then
  A.ShowPointWarning('Choose at your class starting level, out of combat.')
 end
end)
