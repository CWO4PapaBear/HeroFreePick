from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute('''
ITEM_CLASSES_ALLOWED='Classes: %s'
LOCALIZED_CLASS_NAMES_MALE={DEATHKNIGHT='Death Knight',ROGUE='Rogue',MAGE='Mage'}
LOCALIZED_CLASS_NAMES_FEMALE={DEATHKNIGHT='Death Knight',ROGUE='Rogue',MAGE='Mage'}
function UnitClass()return 'Rogue','ROGUE'end
function GetItemInfo()return 'Item','link',4,80,80,'Armor','Plate',1,'INVTYPE_LEGS'end
function CreateFrame()local f={};function f:RegisterEvent()end;function f:SetScript(e,fn)self[e]=fn end;eventFrame=f;return f end
function makeTip(name)
 local t={hooks={}};_G[name]=t
 function t:GetItem()return 'Item','link'end
 function t:GetName()return name end
 function t:NumLines()return 3 end
 function t:IsShown()return true end
 function t:HookScript(e,fn)self.hooks[e]=fn end
 for i=1,3 do
  local l={text='',r=1,g=0,b=0};_G[name..'TextLeft'..i]=l
  function l:GetText()return self.text end
  function l:SetText(s)self.text=s end
  function l:SetTextColor(r,g,b)self.r=r;self.g=g;self.b=b end
 end
 return t
end
for _,n in ipairs({'GameTooltip','ItemRefTooltip','ShoppingTooltip1','ShoppingTooltip2','ItemRefShoppingTooltip1','ItemRefShoppingTooltip2'})do makeTip(n)end
function state(s)eventFrame.OnEvent(eventFrame,'CHAT_MSG_SYSTEM',s)end
function check(text,white)
 local l=GameTooltipTextLeft1;l.text=text;l.g=0
 GameTooltipTextLeft2.text='Requires Level 80';GameTooltipTextLeft2.g=0
 GameTooltipTextLeft3.text='Requires Blacksmithing (400)';GameTooltipTextLeft3.g=0
 GameTooltip.hooks.OnTooltipSetItem(GameTooltip)
 assert(l.g==(white and 1 or 0),text)
 assert(GameTooltipTextLeft2.g==0 and GameTooltipTextLeft3.g==0)
end
''')
lua.execute((Path(__file__).parent/'payload/HeroFreePick/HybridEquipmentTooltips.lua').read_text())
lua.execute('''
check('Classes: Death Knight',false)
state('HF_MODE STATE 3 1 6')
check('Classes: Death Knight',true)
check('Classes: Mage, Death Knight',true)
check('Classes: |cffff2020Death Knight|r',true)
assert(GameTooltipTextLeft1.text=='Classes: Death Knight')
check('Classes: Mage',false)
check('Classes: Death Knight Apprentice',false)
check('Requires Death Knight',false)
for _,t in ipairs({ItemRefTooltip,ShoppingTooltip1,ShoppingTooltip2,ItemRefShoppingTooltip1,ItemRefShoppingTooltip2})do
 local l=_G[t:GetName()..'TextLeft1'];l.text='Classes: Death Knight';l.g=0
 t.hooks.OnTooltipSetItem(t);assert(l.g==1)
end
state('HF_MODE STATE 1 1 0');check('Classes: Death Knight',false)
state('HF_MODE STATE 2 1 6');check('Classes: Death Knight',false)
state('HF_MODE STATE 3 1 99');check('Classes: Death Knight',false)
state('HF_MODE STATE 4 1 6');check('Classes: Death Knight',true)
ITEM_CLASSES_ALLOWED='Klassen: %s';LOCALIZED_CLASS_NAMES_MALE.DEATHKNIGHT='Todesritter'
check('Klassen: Todesritter',true)
state('HF_PATH PENDING');check('Klassen: Todesritter',false)
state('HF_MODE STATE 3 1 6');eventFrame.OnEvent(eventFrame,'PLAYER_LOGIN');check('Klassen: Todesritter',false)
''')
print('PASS Lua 5.1: class lists, color codes, locales, tooltip surfaces, server confirmation and unrelated red requirements.')
