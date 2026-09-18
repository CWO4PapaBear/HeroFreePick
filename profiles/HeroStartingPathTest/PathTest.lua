local A=HeroFreePick
local function subject()return A.ServerPathEnrolled==true end
local function startLevel()local _,class=UnitClass('player');return class=='DEATHKNIGHT'and 55 or 1 end
local due=A.ModeChoiceDue
function A.ModeChoiceDue(level)
 if subject()and not HeroFreePickPlans.progressionChoice and (level or UnitLevel('player'))==startLevel()then return 'initial'end
 if subject()then return due(level)end
 return nil
end
-- The server snapshot, never a name or local saved variable, establishes enrollment.
if subject()then A.RegisterMode('ClassPlus')end
local choose=A.ChooseInitialMode
function A.ChooseInitialMode(mode)
 if not subject()then return false,'Waiting for server enrollment. Existing unenrolled characters remain Classic.'end
 if UnitLevel('player')~=startLevel()then return false,'This test selection requires the starting level for your class.'end
 if mode~='Classic'and mode~='ClassPlus'then return false,'This test supports Classic and Class+ only.'end
 if A.HasPendingChanges()or A.classicCommit then return false,'Finish or cancel pending changes first.'end
 SendChatMessage(mode=='Classic'and '.hfpath classic'or '.hfpath classplus','SAY')
 return false,'Waiting for the server to confirm your starting path.'
end
local show=A.ShowModeChoice
function A.ShowModeChoice(level,reopen)
 if subject()then A.RegisterMode('ClassPlus')end
 show(level,reopen)
 if subject()and UnitLevel('player')==startLevel()then
  for i=3,4 do local b=A.ProgressionChoiceButtons[i];if b then b:Disable();b:SetScript('OnClick',nil)end end
 end
end
local frame=CreateFrame('Frame')
frame:RegisterEvent('PLAYER_LOGIN');frame:RegisterEvent('CHAT_MSG_SYSTEM')
frame:SetScript('OnEvent',function(_,event,message)
 if event=='PLAYER_LOGIN'then A.ServerPathEnrolled=nil;SendChatMessage('.hfpath status','SAY');return end
 if message=='HF_PATH PENDING'or message=='HF_PATH CLASSIC'or message=='HF_PATH CLASSPLUS'then A.ServerPathEnrolled=true;A.RegisterMode('ClassPlus')end
 if message=='HF_PATH LEGACY_CLASSIC'then
  A.ServerPathEnrolled=false
  local ok,why=A.SelectMode('Classic')
  if not ok then A.ShowPointWarning(why or 'Cancel pending edits, then use .hfpath status.');return end
  HeroFreePickPlans.progressionChoice={mode='Classic'};HeroProgressionChoice:Hide();A.Refresh(true);return
 end
 if message=='HF_PATH PENDING'then
  HeroFreePickPlans.progressionChoice=nil;A.ShowModeChoice(nil,true)
 elseif message=='HF_PATH CLASSIC'or message=='HF_PATH CLASSPLUS'then
  if A.HasPendingChanges()or A.classicCommit then
   A.ShowPointWarning('The server saved your path. Finish or cancel pending edits, then use .hfpath status to synchronize.');return
  end
  local mode=message=='HF_PATH CLASSIC'and 'Classic'or 'ClassPlus'
  A.RegisterMode('ClassPlus')
  local ok,why=A.SelectMode(mode)
  if ok then
   HeroFreePickPlans.progressionChoice={mode=mode};HeroProgressionChoice:Hide();A.Refresh(true)
  else A.ShowPointWarning(why or 'Unable to synchronize the server path.')end
 elseif message=='HF_PATH ERROR'or message=='HF_PATH NOT_ENROLLED'then
  A.ShowPointWarning('The server could not verify enrollment or saved starting spells. No mode change was approved.')
 elseif message=='HF_PATH CHOICE_BLOCKED'then
  A.ShowPointWarning('Choose at your class starting level, out of combat.')
 end
end)
