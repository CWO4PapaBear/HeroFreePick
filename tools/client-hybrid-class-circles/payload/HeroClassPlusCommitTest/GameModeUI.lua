local A=HeroFreePick
local labels={Classic='Classic',ClassPlus='Class+',Hybrid='Hybrid',Hero='Hero'}
local names={'Warrior','Paladin','Hunter','Rogue','Priest','DeathKnight','Shaman','Mage','Warlock','Druid'}
local statNames={'Strength','Agility','Intellect','Spirit'}
local function stone(parent,w,h)
 local f=CreateFrame('Frame',nil,parent);f:SetSize(w,h);f:EnableMouse(true)
 f:SetBackdrop({bgFile='Interface\\DialogFrame\\UI-DialogBox-Background',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',tile=true,tileSize=16,edgeSize=16,insets={left=4,right=4,top=4,bottom=4}})
 f:SetBackdropColor(.12,.12,.12,1)
 local t=f:CreateTexture(nil,'BACKGROUND');t:SetPoint('TOPLEFT',6,-6);t:SetPoint('BOTTOMRIGHT',-6,6);t:SetTexture('Interface\\PaperDollInfoFrame\\UI-Character-General-TopLeft');t:SetTexCoord(80/256,250/256,38/256,67/256)
 return f
end
local function text(parent,font,x,y,width)
 local t=parent:CreateFontString(nil,'OVERLAY',font);t:SetPoint('TOPLEFT',x,y);t:SetWidth(width);t:SetJustifyH('LEFT');return t
end
local function button(parent,label,x,y,width,fn)
 local b=CreateFrame('Button',nil,parent,'UIPanelButtonTemplate');b:SetSize(width,28);b:SetPoint('TOPLEFT',x,y);b:SetText(label);b:SetScript('OnClick',fn);return b
end
local hint=CreateFrame('Frame',nil,A.SettingsButton);hint:SetPoint('TOPLEFT',-3,3);hint:SetPoint('BOTTOMRIGHT',3,-3);hint:SetFrameLevel(A.SettingsButton:GetFrameLevel()+3)
 hint:SetBackdrop({edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',edgeSize=12});hint:SetBackdropBorderColor(1,1,0,1);hint:Hide()
 local phase=0
hint:SetScript('OnUpdate',function(self,elapsed)phase=phase+elapsed;self:SetAlpha(.35+.65*math.abs(math.sin(phase*4)))end)
local function clearHint()HeroFreePickPlans.modeSettingsHintLevel=nil;hint:Hide()end
function A.FlashModeSettings()HeroFreePickPlans.modeSettingsHintLevel=UnitLevel('player');hint:Show()end
A.SettingsMenu:HookScript('OnShow',clearHint)
local events=CreateFrame('Frame');events:RegisterEvent('PLAYER_LEVEL_UP');events:RegisterEvent('PLAYER_LOGIN')
events:SetScript('OnEvent',function(_,event)
 if event=='PLAYER_LEVEL_UP'then clearHint()elseif HeroFreePickPlans.modeSettingsHintLevel==UnitLevel('player')then hint:Show()end
end)
local box=stone(UIParent,560,410);box:SetPoint('CENTER');box:SetFrameStrata('FULLSCREEN_DIALOG');box:Hide();A.ModeUpgradeDialog=box
box:HookScript('OnShow',function(self) self:SetFrameLevel(math.max(HeroFreePickFrame:GetFrameLevel()+100,100));self:Raise() end)
local title=text(box,'GameFontNormalLarge',22,-22,505)
local note=text(box,'GameFontHighlight',22,-58,510);note:SetHeight(100);A.ModeUpgradeMessage=note
local close=CreateFrame('Button',nil,box,'UIPanelCloseButton');close:SetPoint('TOPRIGHT',-6,-6);close:SetScript('OnClick',function()box:Hide()end)
local rows={};local target,second,primary
local function clear()for _,b in ipairs(rows)do b:Hide()end;rows={}end
local function add(label,x,y,w,fn)local b=button(box,label,x,y,w,fn);rows[#rows+1]=b;return b end
local reviewing=false
local strip=CreateFrame('Frame',nil,HeroFreePickFrame)
strip:SetSize(550,32);strip:SetPoint('BOTTOM',HeroFreePickFrame,'TOP',0,4)
strip:SetFrameStrata('FULLSCREEN_DIALOG');strip:Hide()
local function pulse(b)
 local border=CreateFrame('Frame',nil,b);border:SetPoint('TOPLEFT',-3,3);border:SetPoint('BOTTOMRIGHT',3,-3)
 border:SetFrameLevel(b:GetFrameLevel()+1);border:EnableMouse(false)
 border:SetBackdrop({edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',edgeSize=12});border:SetBackdropBorderColor(1,1,0,1)
 local t=0;border:SetScript('OnUpdate',function(self,dt)t=t+dt;self:SetAlpha(.35+.65*math.abs(math.sin(t*4)))end)
end
local function endReview()reviewing=false;strip:Hide()end
local stay=button(strip,'Continue as Class+ ('..UnitClass('player')..')',0,0,300,function()
 if A.ModeChoiceDue()~='hybrid' then HeroFreePickPlans.hybridPrimaryReview=nil;endReview();A.FlashModeSettings();return end
 local ok,why=A.ChooseHybridPath(nil)
 if ok then endReview()elseif why then A.ShowPointWarning(why)end
end)
local become=button(strip,'Become Hybrid',310,0,240,function()A.ShowModeUpgrade('Hybrid')end)
pulse(stay);pulse(become)
strip:SetScript('OnUpdate',function()
 if (A.ServerApprovedMode or A.mode)~='ClassPlus' then endReview()end
end)
local reply=CreateFrame('Frame');reply:RegisterEvent('CHAT_MSG_SYSTEM')
reply:SetScript('OnEvent',function(_,_,message)if type(message)=='string' and message:match('^HF_MODE STATE [1-4] 1 %d+$')then if message:match('^HF_MODE STATE 2 ')then HeroFreePickPlans.hybridPrimaryReview=nil end;endReview()end end)
local originalChoice=A.ShowModeChoice
function A.ShowModeChoice(level,reopen)
 if reviewing and not reopen and (A.ServerApprovedMode or A.mode)=='ClassPlus' then
  if HeroProgressionChoice then HeroProgressionChoice:Hide()end
  strip:Show();return
 end
 return originalChoice(level,reopen)
end
local function returnToReview()
 box:Hide();reviewing=target=='Hybrid' and (A.ServerApprovedMode or A.mode)=='ClassPlus'
 if HeroProgressionChoice then HeroProgressionChoice:Hide()end
 if not HeroFreePickFrame:IsShown()then A.BeginPreparation()end
 A.Refresh(true);A.FitWindow();HeroFreePickFrame:Show()
 strip:SetFrameLevel(HeroFreePickFrame:GetFrameLevel()+80)
 if reviewing then strip:Show()else strip:Hide()end
end
local function review()
 clear();title:SetText('Upgrade to '..labels[target])
 note:SetText('Game Mode can only move upward. '..(second and ('Your second class will be '..second..'. ')or '')..'Confirm your current build if it fits the new limits, or refund all allocated Ability and Talent Points and rebuild. This upgrade refund is free and does not use your first free reset or add a reset counter. '..(target=='Hybrid' and '' or 'Choose your Primary Stat:'))
 if target~='Hybrid' then
 for i,name in ipairs(statNames)do local code=i;local b
  b=add((primary==i and '|cffffff00' or '')..name..(primary==i and '|r'or ''),22+(i-1)*130,-172,125,function()primary=code;review()end)
 end
 end
 local function submit(reset)
  if target=='Hybrid' then
   primary=nil;for i,name in ipairs(statNames)do if HeroFreePickPlans.primaryStat==name then primary=i end end
  end
  local ok,why=A.RequestModeUpgrade(target,second,reset,primary)
  if not ok then note:SetText(why)else box:Hide()end
 end
 local y=target=='Hybrid' and -172 or -230
 add('Confirm Current Build',22,y,250,function()submit(false)end)
 add('Refund All Points and Rebuild',286,y,250,function()submit(true)end)
 add('Return to Hero Advancement Menu to Review',22,y-42,514,returnToReview)
 box:SetHeight(-y+90);box:Show()
end
function A.ShowModeUpgrade(mode,class)
 target=mode;second=class;primary=nil
 if mode=='Hybrid' then HeroFreePickPlans.hybridPrimaryReview=true end
 for i,name in ipairs(statNames)do if HeroFreePickPlans.primaryStat==name then primary=i end end
 A.SettingsMenu:Hide()
 if target=='Hybrid'and not second then
  if UnitLevel('player')<10 then A.ShowPointWarning('Hybrid becomes available at level 10.');return end
  clear();title:SetText('Choose one additional class');note:SetText('Keep your original class and add one other class. Both share your Ability Points, Talent Points and rarity budgets.')
  local _,own=UnitClass('player');local i=0
  for _,name in ipairs(names)do if name:upper()~=own then local selected=name;i=i+1;local b=A.CreateClassChoiceButton(box,name,function()second=selected;review()end);b:SetPoint('TOPLEFT',20+((i-1)%5)*105,-166-math.floor((i-1)/5)*86);rows[#rows+1]=b end end
  box:SetHeight(370);box:Show()
 else review()end
end
local menu=A.SettingsMenu;menu:SetHeight(112)
local options={}
local modeText=text(menu,'GameFontNormal',14,-82,216);modeText:SetText('Game Mode')
menu:HookScript('OnShow',function()
 for _,b in ipairs(options)do b:Hide()end;options={}
 local list=A.ModeUpgradeOptions()
 for i,mode in ipairs(list)do local selected=mode;local label=labels[mode]
  if mode=='Hybrid'and UnitLevel('player')<10 then label=label..' (Level 10)'end
  local b=button(menu,label,14,-103-(i-1)*33,220,function()A.ShowModeUpgrade(selected)end);options[#options+1]=b
  if mode=='Hybrid'and UnitLevel('player')<10 then b:Disable()end
 end
 modeText:SetText('Game Mode: '..labels[A.ServerApprovedMode or A.mode])
 menu:SetHeight(115+#list*33)
end)

-- Clear only after the server acknowledges an applied Hybrid build, not a status sync.
local previousCommitResult=A.ClassicCommitResult
function A.ClassicCommitResult(ok,why)
 if ok and (A.ServerApprovedMode or A.mode)=='Hybrid' then HeroFreePickPlans.hybridPrimaryReview=nil end
 if previousCommitResult then return previousCommitResult(ok,why)end
end
