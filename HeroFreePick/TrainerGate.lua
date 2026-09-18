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
-- Use Blizzard's actual NPC dialogue frame and option template.
-- Separate option children leave Blizzard quest/option click handlers untouched.
local active,closing,pending=false,false,false
local options={}
local function clear()
 active=false;pending=false
 for _,b in ipairs(options)do b:Hide()end
end
local function setup()
 if options[1]then return end
 local labels={'Open Hero Advancement','Reset Talents...'}
 for i,label in ipairs(labels)do
  local b=CreateFrame('Button','HeroAdvancementTrainerOption'..i,GossipGreetingScrollChildFrame,'GossipTitleButtonTemplate')
  b:SetText(label)
  b:SetPoint('TOPLEFT',i==1 and GossipGreetingText or options[i-1],i==1 and 'BOTTOMLEFT' or 'BOTTOMLEFT',i==1 and -10 or 0,i==1 and -20 or -12)
  options[i]=b
 end
 options[1]:SetScript('OnClick',function()
  if not active then return end
  HideUIPanel(GossipFrame)
  if not HeroFreePickFrame:IsShown()then A.Toggle()end
 end)
 options[2]:SetScript('OnClick',function()
  if active and custom()then SendChatMessage('.hftrainer reset','SAY')end
 end)
 GossipFrame:HookScript('OnHide',clear)
end
local function greetingBlocked()
 local greeting=GetTrainerGreetingText and GetTrainerGreetingText()or ''
 return custom()and type(greeting)=='string'and greeting:find('HF_CLASS_TRAINER:',1,true)==1
end
function A.ShowClassTrainerDialogue()
 if not custom()or not GossipFrame then return false end
 setup()
 -- Capture the NPC before closing the training interaction.
 local name=UnitName('npc')or ''
 SetPortraitTexture(GossipFramePortrait,'npc')
 closing=true
 if ClassTrainerFrame then HideUIPanel(ClassTrainerFrame)end
 if CloseTrainer then CloseTrainer()end
 closing=false
 ShowUIPanel(GossipFrame)
 active=true
 GossipFrameNpcNameText:SetText(name)
 GossipGreetingText:SetText(A.ClassTrainerDialogueText())
 for i=1,(NUMGOSSIPBUTTONS or 32)do local b=_G['GossipTitleButton'..i];if b then b:Hide()end end
 for _,b in ipairs(options)do if GossipResize then GossipResize(b)end;b:Show()end
 GossipSpacerFrame:ClearAllPoints();GossipSpacerFrame:SetPoint('TOP',options[2],'BOTTOM',0,0);GossipSpacerFrame:Show()
 GossipGreetingScrollFrame:SetVerticalScroll(0)
 return true
end
local events=CreateFrame('Frame','HeroAdvancementTrainerEvents')
for _,event in ipairs({'TRAINER_SHOW','UPDATE_BINDINGS','PLAYER_LEAVING_WORLD','GOSSIP_SHOW'})do events:RegisterEvent(event)end
events:SetScript('OnEvent',function(_,event)
 if event=='TRAINER_SHOW'then pending=greetingBlocked()
 elseif event=='UPDATE_BINDINGS'then if active then GossipGreetingText:SetText(A.ClassTrainerDialogueText())end
 elseif not closing then
  local wasActive=active;clear()
  if event=='PLAYER_LEAVING_WORLD'and wasActive then HideUIPanel(GossipFrame)end
 end
end)
-- Run after Blizzard's TRAINER_SHOW handlers; they may load/show the trainer frame.
events:SetScript('OnUpdate',function()if pending then pending=false;A.ShowClassTrainerDialogue()end end)
-- An ordinary gossip refresh restores its own quests/options and removes ours,
-- irrespective of which GOSSIP_SHOW event handler runs first.
if hooksecurefunc and GossipFrameUpdate then hooksecurefunc('GossipFrameUpdate',clear)end
