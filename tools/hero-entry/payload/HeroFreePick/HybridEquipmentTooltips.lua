-- Only equipment class requirements are changed; the server controls eligibility.
local tokens={[1]='WARRIOR',[2]='PALADIN',[3]='HUNTER',[4]='ROGUE',
 [5]='PRIEST',[6]='DEATHKNIGHT',[7]='SHAMAN',[8]='MAGE',[9]='WARLOCK',[11]='DRUID'}
local second,hero
local function plain(text)
 return (text or ''):gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r','')
end
local function allowed(text)
 if (not second and not hero)or not ITEM_CLASSES_ALLOWED then return false end
 local template=ITEM_CLASSES_ALLOWED
 local start,finish=template:find('%%s')
 if not start then return false end
 local prefix,suffix=template:sub(1,start-1),template:sub(finish+1)
 text=plain(text)
 if text:sub(1,#prefix)~=prefix then return false end
 if #suffix>0 and text:sub(-#suffix)~=suffix then return false end
 local names=text:sub(#prefix+1,#text-#suffix)
 local male=LOCALIZED_CLASS_NAMES_MALE or {}
 local female=LOCALIZED_CLASS_NAMES_FEMALE or {}
 for name in names:gmatch('[^,]+')do
  name=name:match('^%s*(.-)%s*$')
  if hero then for _,token in pairs(tokens)do if name==male[token]or name==female[token]then return true end end
  elseif name==male[second]or name==female[second]then return true end
 end
 return false
end
local function update(tip)
 if (not second and not hero)or not tip.GetItem then return end
 local _,link=tip:GetItem()
 if not link then return end
 local equip=select(9,GetItemInfo(link))
 if not hero and (not equip or equip=='')then return end
 local name=tip:GetName()
 if not name then return end
 for i=1,tip:NumLines()do
  local line=_G[name..'TextLeft'..i]
  if line and allowed(line:GetText())then
   -- The whole requirement is satisfied by either class, just as in stock UI.
   line:SetText(plain(line:GetText()))
   line:SetTextColor(1,1,1)
  end
 end
end
local frame=CreateFrame('Frame')
frame:RegisterEvent('PLAYER_LOGIN')
frame:RegisterEvent('CHAT_MSG_SYSTEM')
frame:SetScript('OnEvent',function(_,event,message)
 if event=='PLAYER_LOGIN'then second=nil;hero=false;return end
 if message=='HF_PATH PENDING'then second=nil;hero=false;return end
 if type(message)~='string'then return end
 local mode,id=message:match('^HF_MODE STATE ([1-4]) [01] (%d+)$')
 if not mode then return end
 mode,id=tonumber(mode),tonumber(id);hero=mode==4
 local _,own=UnitClass('player')
 second=(mode==3 or mode==4)and tokens[id]~=own and tokens[id]or nil
 for _,name in ipairs({'GameTooltip','ItemRefTooltip','ShoppingTooltip1','ShoppingTooltip2',
  'ItemRefShoppingTooltip1','ItemRefShoppingTooltip2'})do
  local tip=_G[name];if tip and tip:IsShown()then update(tip)end
 end
end)
for _,name in ipairs({'GameTooltip','ItemRefTooltip','ShoppingTooltip1','ShoppingTooltip2',
 'ItemRefShoppingTooltip1','ItemRefShoppingTooltip2'})do
 local tip=_G[name]
 if tip then tip:HookScript('OnTooltipSetItem',update);tip:HookScript('OnShow',update)end
end
