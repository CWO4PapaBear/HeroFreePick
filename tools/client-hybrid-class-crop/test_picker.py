from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
# Requires Lupa Lua 5.1.
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
for p in (HERE/'payload').rglob('*.lua'):
    compiled=lua.eval('loadstring')(p.read_text())
    assert not isinstance(compiled,tuple),(p,compiled)
source=(HERE/'payload/HeroFreePick/HeroFreePick.lua').read_text()
helper=source[source.index('local badges='):source.index("for i,name in ipairs({'Browse'")]
lua.execute('''
HeroFreePick={}; A=HeroFreePick
local noop=function()end
function CreateFrame()
 local b={scripts={}}
 setmetatable(b,{__index=function(_,key)return noop end})
 b.CreateTexture=CreateFrame;b.CreateFontString=CreateFrame
 function b:SetScript(name,fn)self.scripts[name]=fn end
 return b
end
GameTooltip={lines={}}
function GameTooltip:SetOwner(owner)self.owner=owner;self.lines={}end
function GameTooltip:SetText(text)self.title=text end
function GameTooltip:AddLine(text)table.insert(self.lines,text)end
function GameTooltip:Show()self.shown=true end
function GameTooltip:Hide()self.shown=false end
function GameTooltip:IsOwned(owner)return self.owner==owner end
''')
lua.execute(helper)
lua.execute('''
for _,class in ipairs({'Warrior','Paladin','Hunter','Rogue','Priest','DeathKnight','Shaman','Mage','Warlock','Druid'})do
 local clicked=false
 local b=A.CreateClassChoiceButton({},class,function()clicked=true end)
 b.scripts.OnEnter(b);assert(#GameTooltip.lines>=5,class)
 assert(GameTooltip.shown)
 b.scripts.OnClick();assert(clicked)
 b.scripts.OnHide();assert(not GameTooltip.shown)
end
CLASS_INFO_WARRIOR0='Localized warrior role'
local b=A.CreateClassChoiceButton({},'Warrior',function()end)
b.scripts.OnEnter(b);assert(GameTooltip.lines[1]=='Localized warrior role')
''')
assert 'A.ChooseHybridPath(selected)' in source
assert "string.upper(c)~=own" in source
upgrade=(HERE/'payload/HeroClassPlusCommitTest/GameModeUI.lua').read_text()
assert "UnitLevel('player')<10" in upgrade and 'name:upper()~=own' in upgrade
assert 'second=selected;review()' in upgrade
print('PASS: Lua 5.1 syntax, ten class tooltips, localized text, clicks and tooltip cleanup. Eligibility/confirmation paths retained. Visual checks pending.')
