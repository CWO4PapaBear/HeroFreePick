local A=HeroFreePick
BINDING_HEADER_HERO_CHARACTER_ADVANCEMENT='Hero Advancement'
BINDING_NAME_HERO_CHARACTER_ADVANCEMENT='Toggle Hero Advancement'
local access=CreateFrame('Frame');access:RegisterEvent('PLAYER_LOGIN')
access:SetScript('OnEvent',function()
 A.Init()
 if not HeroFreePickPlans.defaultKeyInstalled and not InCombatLockdown() then
  if SetBinding('N','HERO_CHARACTER_ADVANCEMENT') then SaveBindings(GetCurrentBindingSet());HeroFreePickPlans.defaultKeyInstalled=true end
 end
end)
-- Add an option to the Escape menu, before the normal options button.
if GameMenuFrame and GameMenuButtonOptions then
 local option=CreateFrame('Button','HeroAdvancementGameMenuButton',GameMenuFrame,'GameMenuButtonTemplate')
 option:SetText('Hero Advancement');option:SetSize(GameMenuButtonOptions:GetWidth(),GameMenuButtonOptions:GetHeight())
 local point,relative,relativePoint,x,y=GameMenuButtonOptions:GetPoint(1)
 option:SetPoint(point,relative,relativePoint,x,y)
 GameMenuButtonOptions:ClearAllPoints();GameMenuButtonOptions:SetPoint('TOP',option,'BOTTOM',0,-1)
 GameMenuFrame:SetHeight(GameMenuFrame:GetHeight()+option:GetHeight()+1)
 option:SetScript('OnClick',function()HideUIPanel(GameMenuFrame);A.Toggle()end)
end

if TalentMicroButton then
 TalentMicroButton:SetScript('OnClick',function()A.Toggle()end)
 TalentMicroButton:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_RIGHT');GameTooltip:SetText('Hero Advancement |cffffff00(N)|r',1,1,1);GameTooltip:Show()end)
 TalentMicroButton:SetScript('OnLeave',function()GameTooltip:Hide()end)
 local function enableAdvancementButton()
  if A.mode~='ClassPlus'and A.mode~='Hybrid'and A.mode~='Hero'then return end
  TalentMicroButton:Show();TalentMicroButton:Enable()
  if AchievementMicroButton then AchievementMicroButton:SetPoint('BOTTOMLEFT',TalentMicroButton,'BOTTOMRIGHT',-2,0)end
 end
 function A.RefreshAdvancementButton()
  -- Restore stock visibility/spacing first, including when switching to Classic.
  if UpdateTalentButton then UpdateTalentButton()end
  enableAdvancementButton()
 end
 if UpdateTalentButton then hooksecurefunc('UpdateTalentButton',enableAdvancementButton)end
 if TalentMicroButton_Update then hooksecurefunc('TalentMicroButton_Update',enableAdvancementButton)end
 if A.Init then hooksecurefunc(A,'Init',A.RefreshAdvancementButton)end
 if A.Refresh then hooksecurefunc(A,'Refresh',A.RefreshAdvancementButton)end
 A.RefreshAdvancementButton()
end
