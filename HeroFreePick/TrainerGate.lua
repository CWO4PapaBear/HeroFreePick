-- Class-trainer presentation. Server hooks remain the purchase authority.
local A=HeroFreePick
local function custom()return A.mode=='ClassPlus'or A.mode=='Hybrid'or A.mode=='Hero'end
function A.ClassTrainerDialogueText()
 local key=GetBindingKey and GetBindingKey('HERO_CHARACTER_ADVANCEMENT')
 local intro='For special heroes like you, abilities are learned through your Hero Advancement Menu. '
 if key then
  local label=GetBindingText and GetBindingText(key,'KEY_')or key
  return intro..'You can access that through the menu button or by pressing |cffffff00('..label..')|r.'
 end
 return intro..'You can access that through the menu button. No keyboard shortcut is currently assigned.'
end
local dialog=CreateFrame('Frame','HeroAdvancementTrainerDialogue',UIParent)
A.TrainerDialogue=dialog;dialog:SetSize(470,205);dialog:SetPoint('CENTER');dialog:SetFrameStrata('DIALOG');dialog:EnableMouse(true)
dialog:SetBackdrop({bgFile='Interface\\AddOns\\HeroFreePick\\Art\\StoneBackground',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',tile=true,tileSize=128,edgeSize=16,insets={left=4,right=4,top=4,bottom=4}})
dialog:SetBackdropColor(1,1,1,1);dialog:SetBackdropBorderColor(.65,.6,.5,1)
local title=dialog:CreateFontString(nil,'OVERLAY','GameFontNormalLarge');title:SetPoint('TOP',0,-18);title:SetText('Hero Advancement')
local message=dialog:CreateFontString(nil,'OVERLAY','GameFontHighlight');message:SetPoint('TOPLEFT',24,-50);message:SetWidth(422);message:SetJustifyH('LEFT')
local close=CreateFrame('Button',nil,dialog,'UIPanelCloseButton');close:SetPoint('TOPRIGHT',-3,-3)
close:SetScript('OnClick',function()dialog:Hide()end)
local open=CreateFrame('Button',nil,dialog,'UIPanelButtonTemplate');open:SetSize(195,26);open:SetPoint('BOTTOMLEFT',22,20);open:SetText('Open Hero Advancement')
open:SetScript('OnClick',function()dialog:Hide();if not HeroFreePickFrame:IsShown()then A.Toggle()end end)
local reset=CreateFrame('Button',nil,dialog,'UIPanelButtonTemplate');reset:SetSize(195,26);reset:SetPoint('BOTTOMRIGHT',-22,20);reset:SetText('Reset Talents...')
reset:SetScript('OnClick',function()if custom()then SendChatMessage('.hftrainer reset','SAY')end end)
reset:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_TOP');GameTooltip:SetText('Reset Talents');GameTooltip:AddLine('Your trainer will quote the current gold cost and ask you to confirm. No gold is charged until you accept.',1,1,1,true);GameTooltip:Show()end)
reset:SetScript('OnLeave',function()GameTooltip:Hide()end)
dialog:Hide();tinsert(UISpecialFrames,'HeroAdvancementTrainerDialogue')
local closing=false
local pending=false
local function greetingBlocked()
 local greeting=GetTrainerGreetingText and GetTrainerGreetingText()or ''
 return custom()and type(greeting)=='string'and greeting:find('HF_CLASS_TRAINER:',1,true)==1
end
function A.ShowClassTrainerDialogue()
 if not custom()then return false end
 closing=true
 if ClassTrainerFrame and HideUIPanel then HideUIPanel(ClassTrainerFrame)end
 if CloseTrainer then CloseTrainer()end
 closing=false;message:SetText(A.ClassTrainerDialogueText());dialog:Show();return true
end
local events=CreateFrame('Frame','HeroAdvancementTrainerEvents')
for _,event in ipairs({'TRAINER_SHOW','UPDATE_BINDINGS','PLAYER_LEAVING_WORLD','GOSSIP_SHOW'})do events:RegisterEvent(event)end
events:SetScript('OnEvent',function(_,event)
 if event=='TRAINER_SHOW'then pending=greetingBlocked();if pending then A.ShowClassTrainerDialogue()end
 elseif event=='UPDATE_BINDINGS'then if dialog:IsShown()then message:SetText(A.ClassTrainerDialogueText())end
 elseif not closing then pending=false;dialog:Hide()end
end)
-- The trainer frame can load after this addon. Catch its Show after Blizzard's handler.
if hooksecurefunc and ShowUIPanel then hooksecurefunc('ShowUIPanel',function(frame)if frame==ClassTrainerFrame and not closing and (pending or greetingBlocked())then A.ShowClassTrainerDialogue()end end)end

-- Finish after all TRAINER_SHOW handlers, regardless of addon event ordering.
events:SetScript('OnUpdate',function()if pending then pending=false;A.ShowClassTrainerDialogue()end end)
