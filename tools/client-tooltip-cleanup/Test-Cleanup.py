from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parent
lua=LuaRuntime()
for p in (root/'payload').rglob('*.lua'):
    lua.execute('assert(loadstring(...))',p.read_text(encoding='utf-8'))
lua.execute('HeroFreePick={}')
lua.execute((root/'payload/HeroFreePick/TooltipPresentation.lua').read_text(encoding='utf-8'))
lua.execute(r"""
assert(HeroFreePick.TooltipParagraphs('Deals 1.5 damage. Lasts 2.5 sec.')=='Deals 1.5 damage.\n\nLasts 2.5 sec.')
""")
lua.execute(r'''
local A=HeroFreePick
local text='|cffffff00Missing effect.|r More detail! Still pending? Yes.'
local expected='|cffffff00Missing effect.|r\n\nMore detail!\n\nStill pending?\n\nYes.'
assert(A.TooltipParagraphs(text)==expected)
assert(A.TooltipParagraphs(expected)==expected)
assert(A.TooltipParagraphs('Spell ID: 880743')=='Spell ID: 880743')
A.mode='Hybrid';A.byID={[2]={name='Example Mastery'}}
A.IsTalent=function()return false end;A.NativeTalent=function()end
A.PendingRank=function()return 1 end;A.AbilityDisplayLevel=function()return 1 end
A.OtherClass=function()return false end
function UnitLevel()return 60 end
function hideMasteryTooltip()end
function rarityCost()return 'Rare' end
function essenceCost()return '2 AP' end
GameTooltip={lines={}}
function GameTooltip:SetOwner()self.lines={}end
function GameTooltip:SetText(s)self.lines[#self.lines+1]=s end
function GameTooltip:AddLine(s)self.lines[#self.lines+1]=s end
function GameTooltip:AddDoubleLine(a,b)self.lines[#self.lines+1]=a..': '..b end
function GameTooltip:GetName()return 'TestTooltip'end
function GameTooltip:NumLines()return 0 end
function GameTooltip:Show()end
function GetSpellInfo()return 'Example'end
''')
source=(root/'payload/HeroFreePick/HeroFreePick.lua').read_text(encoding='utf-8')
start=source.index('local function tooltip(self)')
end=source.index('-- Shared badge policy',start)
lua.execute('local A=HeroFreePick; '+source[start:end]+'\nTestTooltip=tooltip')
lua.execute(r'''
local A=HeroFreePick
local owner={entry={id=1,spells={674},name='Example',class='Rogue',spec='Combat',kind='Ability',quality='Rare',ae=2,referenceDescription='Deals damage. Adds an effect.',requiredMastery=2}}
A.TooltipDetailsExpanded=false;TestTooltip(owner)
local basic=table.concat(GameTooltip.lines,'\n')
assert(not basic:find('Spell ID',1,true)and not basic:find('Character Advancement ID',1,true))
assert(not basic:find('Example Mastery',1,true)and not basic:find('Left-click',1,true))
assert(not basic:find('server committing is unavailable',1,true))
A.TooltipDetailsExpanded=true;TestTooltip(owner)
local full=table.concat(GameTooltip.lines,'\n')
assert(full:find('Spell ID: 674',1,true)and full:find('Character Advancement ID: 1',1,true))
assert(full:find('Example Mastery',1,true)and full:find('Left-click',1,true))
owner.entry.serverPending=true;A.TooltipDetailsExpanded=false;TestTooltip(owner)
assert(table.concat(GameTooltip.lines,'\n'):find('Server implementation pending.',1,true))
''')
assert 'Browse grouping: recovered tags' not in source
print('PASS: Lua 5.1 syntax, collapsed/expanded metadata, retained pending warning, decimal-safe sentence spacing, color preservation and idempotence.')

