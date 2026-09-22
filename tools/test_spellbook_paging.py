"""Lua 5.1 regression tests: all 30 trees, pagination and native spell slots."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
root = Path(__file__).resolve().parents[1] / 'profiles/HeroHybridSpellbook'
lua = LuaRuntime()
lua.execute('''
frames={}; hooks={}; _G=_G or {}; local methods={}
function methods:SetScript(k,v)self.scripts[k]=v end
function methods:GetScript(k)return self.scripts[k]end
function methods:HookScript(k,v)self.scripts[k]=v end
function methods:Show()self.shown=true end
function methods:Hide()self.shown=false end
function methods:IsShown()return self.shown end
function methods:Enable()self.enabled=true end
function methods:Disable()self.enabled=false end
function methods:SetText(t)self.text=t end
function methods:SetChecked(v)self.checked=v end
local function obj()return setmetatable({scripts={},shown=true},{__index=function(t,k)
 if methods[k]then return methods[k]end
 if k:match('^Set')or k:match('^Register')then return function()end end
end})end
function methods:CreateFontString()local x=obj();self.label=x;return x end
function CreateFrame(_,name,parent)local f=obj();f.parent=parent;frames[#frames+1]=f;if name then _G[name]=f end;return f end
function hooksecurefunc(name,fn)hooks[name]=fn end
HeroFreePick={mode='Hero',byID={},PromptFirstAbilities=function()end}
BOOKTYPE_SPELL='spell';BOOKTYPE_PET='pet';MAX_SPELLS=1024;SPELLS_PER_PAGE=12;SPELLBOOK_PAGENUMBERS={}
SpellBookFrame=CreateFrame('Frame');SpellBookFrame.bookType='spell';SpellBookFrame.selectedSkillLine=1
for i=1,8 do CreateFrame('Button','SpellBookSkillLineTab'..i)end
ShowAllSpellRanksCheckBox=CreateFrame('Frame')
function SpellBook_GetTabInfo()return 'native','icon',0,1 end
function SpellBook_GetSpellID(i)return i,i end
ids={};allRanks=true
function GetNumSpellTabs()return 1 end
function GetSpellTabInfo()return 'General','icon',0,#ids,0,#ids end
function GetCVarBool()return allRanks end
function GetKnownSlotFromHighestRankSlot(i)return i end
function GetSpellLink(i)return '|Hspell:'..ids[i]..'|h'end
function SpellBookFrame_Update()if hooks.SpellBookFrame_Update then hooks.SpellBookFrame_Update()end end
function SpellBookSkillLineTab_OnClick(_,i)SpellBookFrame.selectedSkillLine=i;SpellBookFrame_Update()end
function UpdateSpells()end
''')
lua.execute((root/'TreeMap.lua').read_text())
lua.execute('''
-- Supply one learned native slot per tree, plus an unmapped General spell.
ids[1]=999999
for skill in pairs(HeroSpellbookTrees)do
 for id,tree in pairs(HeroSpellbookSpellTrees)do
  if tree==skill then ids[#ids+1]=id;break end
 end
end
assert(#ids==31)
''')
lua.execute((root/'HybridSpellbook.lua').read_text())
lua.execute('''
local events=frames[#frames-1]
local function refresh()events.scripts.OnEvent(events,'SPELLS_CHANGED');events.scripts.OnUpdate(events,.3)end
refresh()
assert(HeroSpellbookTabPager.shown and HeroSpellbookTabPager.label.text=='Trees 1 / 4')
local seen={}
for page=1,4 do
 for i=1,8 do
  local button=_G['SpellBookSkillLineTab'..i]
  if button.shown then
   button.scripts.OnClick(button)
   local slot=SpellBook_GetSpellID(1)
   assert(slot>=1 and slot<=31 and not seen[slot]);seen[slot]=true
   assert(SpellBook_GetSpellID(2)==1025)
  end
 end
 if page<4 then HeroSpellbookNextTabs.scripts.OnClick()end
end
for i=1,31 do assert(seen[i],'Lost native slot '..i)end
assert(not HeroSpellbookNextTabs.enabled)
refresh();assert(HeroSpellbookTabPager.label.text=='Trees 4 / 4')
HeroSpellbookPreviousTabs.scripts.OnClick();assert(HeroSpellbookTabPager.label.text=='Trees 3 / 4')
-- Hidden-rank mode still uses real native slots.
allRanks=false;refresh();assert(HeroSpellbookTabPager.label.text=='Trees 3 / 4')
-- Shrinking learned build clamps the page and selection safely.
ids={999999};refresh();assert(not HeroSpellbookTabPager.shown and SpellBook_GetSpellID(1)==1)
SpellBookFrame.bookType='pet';SpellBookFrame_Update();assert(SpellBook_GetTabInfo(1)=='native')
HeroFreePick.mode='Classic';SpellBookFrame.bookType='spell';SpellBookFrame_Update()
assert(not HeroSpellbookTabPager.shown and SpellBook_GetTabInfo(1)=='native')
''')
print('PASS: 31 tabs across four pages; every native slot reachable exactly once; page persistence, rank mode, shrink, pet and Classic fallback.')

