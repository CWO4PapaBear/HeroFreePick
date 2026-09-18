from pathlib import Path
from lupa.lua51 import LuaRuntime
r=Path(__file__).parent;lua=LuaRuntime()
lua.execute('''
local A;HeroFreePick={};A=HeroFreePick
HeroFreePickPlans={};HeroProgressionChoice={Hide=function()end};local level=1
function UnitLevel()return level end
function UnitClass()return 'Mage','MAGE'end
function SendChatMessage(s)lastCommand=s end
function CreateFrame()return {RegisterEvent=function()end,SetScript=function(_,_,f)handler=f end}end
A.ModeChoiceDue=function()return 'initial'end;A.RegisterMode=function()end
A.ChooseInitialMode=function()error('Must use server choice')end
A.HasPendingChanges=function()return false end
A.ShowModeChoice=function()shown=true end;A.ProgressionChoiceButtons={}
A.SelectMode=function(m)A.mode=m;return true end;A.Refresh=function()end;A.ShowPointWarning=function(s)warning=s end
''')
lua.execute((r/'profiles/HeroStartingPathTest/PathTest.lua').read_text())
lua.execute('''
local A=HeroFreePick
handler(nil,'PLAYER_LOGIN');assert(lastCommand=='.hfpath status');assert(not A.ModeChoiceDue())
assert(not A.ChooseInitialMode('ClassPlus'));assert(lastCommand=='.hfpath status')
handler(nil,'CHAT_MSG_SYSTEM','HF_PATH PENDING');assert(A.ServerPathEnrolled and shown)
A.ChooseInitialMode('ClassPlus');assert(lastCommand=='.hfpath classplus')
handler(nil,'CHAT_MSG_SYSTEM','HF_PATH CLASSPLUS');assert(A.mode=='ClassPlus'and HeroFreePickPlans.progressionChoice.mode=='ClassPlus')
handler(nil,'PLAYER_LOGIN');assert(A.ServerPathEnrolled==nil)
handler(nil,'CHAT_MSG_SYSTEM','HF_PATH CLASSPLUS');assert(A.ServerPathEnrolled and A.mode=='ClassPlus')
handler(nil,'CHAT_MSG_SYSTEM','HF_PATH LEGACY_CLASSIC');assert(not A.ServerPathEnrolled and A.mode=='Classic'and not A.ModeChoiceDue())
''')
for p in (r/'profiles').rglob('*.lua'):lua.execute('assert(loadstring(...))',p.read_text(encoding='utf-8-sig'))
source=(r/'server/mod-hero-starting-path/src/StartingPath.cpp').read_text()
assert 'Hfstart' not in source and 'Candidate(' not in source
assert 'OnPlayerDeleteFromDB' in source and 'result.phase=-2' in source
assert 'Read(p).phase!=2' in source and 'HeroBuild::Validate' in source
print('PASS: arbitrary-name enrollment policy; server-confirmed selection, relog synchronization, legacy Classic isolation, bridge syntax.')
