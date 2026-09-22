-- Persistent position controls; secure frame movement is restricted to out of combat.
local function settings(key)
 HeroPortraitSettings=HeroPortraitSettings or {}
 HeroPortraitSettings[key]=HeroPortraitSettings[key] or {locked=true}
 return HeroPortraitSettings[key]
end
function HeroSavePortraitPosition(frame,key)
 local x,y=frame:GetLeft(),frame:GetTop();if not x or not y then return end
 local scale=frame:GetEffectiveScale()/UIParent:GetEffectiveScale()
 local s=settings(key);s.x=x*scale;s.y=y*scale-UIParent:GetHeight()
end
local function restore(frame,key)
 if InCombatLockdown()then return end
 local s=settings(key)
 local scale=frame:GetEffectiveScale()/UIParent:GetEffectiveScale()
 if type(s.x)=='number'and type(s.y)=='number'then
  frame:ClearAllPoints();frame:SetPoint('TOPLEFT',UIParent,'TOPLEFT',s.x/scale,s.y/scale)
 elseif key=='player'then frame:ClearAllPoints();frame:SetPoint('TOPLEFT',UIParent,'TOPLEFT',3/scale,-2/scale)end
end
local function entry(frame,key,level)
 if level and level~=1 then return end
 local info=UIDropDownMenu_CreateInfo()
 info.text=settings(key).locked and 'Unlock portrait position' or 'Lock portrait position'
 info.notCheckable=true;info.disabled=InCombatLockdown()
 info.func=function()
  if InCombatLockdown()then return end
  local s=settings(key);s.locked=not s.locked
  frame:StopMovingOrSizing();HeroSavePortraitPosition(frame,key)
 end
 UIDropDownMenu_AddButton(info,level or 1)
end
local function menu(name,initializer)
 local dropdown=CreateFrame('Frame',name,UIParent,'UIDropDownMenuTemplate')
 UIDropDownMenu_Initialize(dropdown,initializer,'MENU')
 return function()ToggleDropDownMenu(1,nil,dropdown,'cursor',0,0)end
end
local event=CreateFrame('Frame');event:RegisterEvent('PLAYER_LOGIN');event:RegisterEvent('PLAYER_REGEN_ENABLED')
local installed=false
event:SetScript('OnEvent',function()
 if InCombatLockdown()then return end
 local mode=HeroFreePick and HeroFreePick.mode
 if mode~='ClassPlus'and mode~='Class+'and mode~='Hybrid'and mode~='Hero'then return end
 local player=HeroIntegratedResourceTest
 if not player then return end
 if not installed then
  installed=true;settings('player');settings('target')
  player.menu=menu('HeroPlayerPortraitDropDown',function(self,level)
   UnitPopup_ShowMenu(self,'SELF','player');entry(player,'player',level)
  end)
  -- The stock dropdown belongs to the hidden stock PetFrame. Use a visible-root
  -- dropdown with the native pet menu rather than showing that hidden child.
  if HeroLivePet1 then
   HeroLivePet1.menu=menu('HeroPrimaryPortraitDropDown',function(self)
    UnitPopup_ShowMenu(self,'PET','pet')
   end)
  end
  if HeroLivePet2 then
   local open=menu('HeroSecondaryPortraitDropDown',function(_,level)
    if level and level~=1 then return end
    for _,action in ipairs({{'Attack','attack'},{'Follow','follow'},{'Stay','stay'},{'Aggressive','aggressive'},{'Defensive','defensive'},{'Passive','passive'},{'Dismiss','dismiss'}})do
     local command=action[2];local info=UIDropDownMenu_CreateInfo()
     info.text=action[1];info.notCheckable=true
     info.func=function()SendChatMessage('.demon '..command,'SAY')end
     UIDropDownMenu_AddButton(info)
    end
   end)
   HeroLivePet2:SetScript('OnMouseUp',function(_,button)if button=='RightButton'then open()end end)
  end
  if TargetFrame then
   TargetFrame:SetMovable(true);TargetFrame:SetClampedToScreen(true);TargetFrame:RegisterForDrag('LeftButton')
   TargetFrame:SetScript('OnDragStart',function(self)
    if not InCombatLockdown()and not settings('target').locked then self:StartMoving()end
   end)
   TargetFrame:SetScript('OnDragStop',function(self)
    if not InCombatLockdown()then self:StopMovingOrSizing();HeroSavePortraitPosition(self,'target')end
   end)
   TargetFrame.menu=menu('HeroTargetPortraitDropDown',function(self,level)
    TargetFrameDropDown_Initialize(self);entry(TargetFrame,'target',level)
   end)
   TargetFrame:SetUserPlaced(true)
  end
 end
 restore(player,'player');if TargetFrame then restore(TargetFrame,'target')end
end)

local elapsed=0
event:SetScript('OnUpdate',function(self,dt)
 if installed then self:SetScript('OnUpdate',nil);return end
 elapsed=elapsed+dt;if elapsed<1 then return end;elapsed=0
 self:GetScript('OnEvent')()
end)
