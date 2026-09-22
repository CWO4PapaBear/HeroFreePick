-- Live custom-mode player frame. Classic uses the untouched stock layout.
local A=HeroFreePick
local mask,runes,received=0,{},0
local showAll=false
local demo=false
local f=CreateFrame('Button','HeroIntegratedResourceTest',UIParent,'SecureUnitButtonTemplate')
f.menu=function()ToggleDropDownMenu(1,nil,PlayerFrameDropDown,'cursor',0,0)end
f:SetAttribute('unit','player');f:SetAttribute('type1','target');f:SetAttribute('type2','togglemenu');f:RegisterForClicks('AnyUp')
f:SetSize(240,180);f:SetPoint('TOPLEFT',UIParent,'TOPLEFT',3,-2)
f:SetMovable(true);f:SetClampedToScreen(true)
local panel=CreateFrame('Frame',nil,f);panel:SetPoint('TOPLEFT',80,0);panel:SetWidth(153)
local classic='Interface\\TargetingFrame\\UI-TargetingFrame'
-- Mirror the clean outer corner for matching rounded ends.
local headerBg=panel:CreateTexture(nil,'BACKGROUND');headerBg:SetPoint('TOPLEFT',3,-3);headerBg:SetSize(147,15);headerBg:SetTexture(.12,.12,.12,.65)
for side=1,2 do
 local cap=panel:CreateTexture(nil,'BORDER');cap:SetSize(76.5,20);cap:SetPoint(side==1 and 'TOPLEFT'or 'TOPRIGHT')
 cap:SetTexture(classic);cap:SetTexCoord(side==1 and 28/256 or 90/256,side==1 and 90/256 or 28/256,20/128,42/128)
end
local header=CreateFrame('Frame',nil,f);header:SetPoint('TOPLEFT');header:SetSize(254,26);header:EnableMouse(true);header:RegisterForDrag('LeftButton')
header:SetScript('OnDragStart',function()if not InCombatLockdown()and HeroPortraitSettings and HeroPortraitSettings.player and not HeroPortraitSettings.player.locked then f:StartMoving()end end);header:SetScript('OnDragStop',function()if not InCombatLockdown()then f:StopMovingOrSizing();if HeroSavePortraitPosition then HeroSavePortraitPosition(f,'player')end end end)
header:SetScript('OnMouseUp',function(_,button)if button=='RightButton'and f.menu then f.menu()end end)
local portraitFrame=CreateFrame('Frame',nil,f);portraitFrame:SetSize(80,80);portraitFrame:SetPoint('TOPLEFT',0,0)
local portrait=portraitFrame:CreateTexture(nil,'ARTWORK');portrait:SetSize(74,74);portrait:SetPoint('CENTER')
-- Two native semicircle slices avoid baking the old lower-left level badge in.
local topRim=portraitFrame:CreateTexture(nil,'OVERLAY');topRim:SetPoint('TOPLEFT');topRim:SetSize(80,40);topRim:SetTexture(classic);topRim:SetTexCoord(217/256,149/256,10/128,44/128)
local bottomRim=portraitFrame:CreateTexture(nil,'OVERLAY');bottomRim:SetPoint('BOTTOMLEFT');bottomRim:SetSize(80,40);bottomRim:SetTexture(classic);bottomRim:SetTexCoord(217/256,149/256,44/128,10/128)
local levelFrame=CreateFrame('Frame',nil,portraitFrame);levelFrame:SetSize(26,26);levelFrame:SetPoint('TOPLEFT',-2,0)
-- Opaque circular backing: no portrait texture or square behind the badge.
for row=0,19 do
 local y=row+.5-10;local width=2*math.sqrt(100-y*y)
 local bg=levelFrame:CreateTexture(nil,'BACKGROUND');bg:SetTexture(.035,.035,.035,1);bg:SetSize(width,1);bg:SetPoint('TOP',0,-3-row)
end
-- Mirror the clean upper-right portrait rim quadrant; the stock level crop
-- also contains part of the portrait and cannot be used as a detached badge.
for q=1,4 do
 local rim=levelFrame:CreateTexture(nil,'ARTWORK');rim:SetSize(13,13)
 local right=q%2==0;local bottom=q>2
 rim:SetPoint(bottom and (right and 'BOTTOMRIGHT'or 'BOTTOMLEFT')or (right and 'TOPRIGHT'or 'TOPLEFT'))
 rim:SetTexture(classic);rim:SetTexCoord(right and 183/256 or 217/256,right and 217/256 or 183/256,bottom and 44/128 or 10/128,bottom and 10/128 or 44/128)
end
local level=levelFrame:CreateFontString(nil,'OVERLAY','GameFontNormalSmall');level:SetPoint('CENTER',0,0)
local name=panel:CreateFontString(nil,'OVERLAY','GameFontNormalSmall');name:SetPoint('TOP',0,-5)
local definitions={{-1,'Health',.15,.8,.2},{0,'Mana',.2,.45,1},{1,'Rage',.9,.15,.1},{3,'Energy',1,.85,.1},{6,'Runic Power',.1,.8,1}}
local bars={}
local function textVisible(b)
 local visible=b.hover or GetCVar('playerStatusText')=='1'
 if visible then b.label:Show();b.value:Show()else b.label:Hide();b.value:Hide()end
end
for _,d in ipairs(definitions)do
 local b=CreateFrame('StatusBar',nil,f);b:SetSize(143,11);b:SetStatusBarTexture('Interface\\TargetingFrame\\UI-StatusBar');b:SetStatusBarColor(d[3],d[4],d[5])
 local edge=b:CreateTexture(nil,'OVERLAY');edge:SetPoint('TOPLEFT',-5,2);edge:SetSize(153,15);edge:SetTexture(classic);edge:SetTexCoord(151/256,28/256,40/128,54/128)
 local bg=b:CreateTexture(nil,'BACKGROUND');bg:SetAllPoints();bg:SetTexture(.12,.12,.12,.65)
 b.label=b:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');b.label:SetPoint('LEFT',4,0);b.label:SetText(d[2])
 b.value=b:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');b.value:SetPoint('RIGHT',-4,0);bars[d[1]]=b
 b:EnableMouse(true);b:SetScript('OnEnter',function(self)self.hover=true;textVisible(self)end);b:SetScript('OnLeave',function(self)self.hover=false;textVisible(self)end)
end
local combo={}
-- Native red gems follow the portrait's lower arc.
local points={{5,-66},{19,-73},{34,-76},{49,-73},{63,-66}}
for i=1,5 do
 local c=CreateFrame('Frame','HeroResourceCombo'..i,portraitFrame,'ComboPointTemplate')
 c:SetPoint('TOPLEFT',points[i][1],points[i][2]);c.highlight=_G[c:GetName()..'Highlight'];c.shine=_G[c:GetName()..'Shine']
 c.highlight:SetAlpha(0);c.shine:SetAlpha(0);combo[i]=c
end
local lastTarget,lastPoints=nil,0
local runeRow=CreateFrame('Frame',nil,f);runeRow:SetSize(153,30);runeRow.cells={}
local runeTextures={'Blood','Unholy','Frost','Death'}
-- Keep slot identity stable when a rune temporarily becomes a Death rune.
local runeOrder={1,2,5,6,3,4}
for i=1,6 do
 local c=CreateFrame('Frame',nil,runeRow);c:SetSize(24,24);c:SetPoint('LEFT',(i-1)*25,0)
 c.icon=c:CreateTexture(nil,'ARTWORK');c.icon:SetAllPoints()
 -- Native RuneButtonIndividualTemplate proportions and layering, scaled 1.25x.
 -- The border must be ABOVE the cooldown child, not a texture underneath it.
 c.icon:ClearAllPoints();c.icon:SetSize(30,30);c.icon:SetPoint('CENTER',0,-1.25)
 c.cooldown=CreateFrame('Cooldown',nil,c);c.cooldown:SetSize(18.75,18.75);c.cooldown:SetPoint('CENTER',0,-1.25);c.cooldown:SetDrawEdge(true)
 local border=CreateFrame('Frame',nil,c);border:SetAllPoints();border:SetFrameLevel(c.cooldown:GetFrameLevel()+1)
 c.ring=border:CreateTexture(nil,'OVERLAY');c.ring:SetSize(30,30);c.ring:SetPoint('CENTER',0,-1.25);c.ring:SetTexture('Interface\\PlayerFrame\\UI-PlayerFrame-Deathknight-Ring');c.ring:SetVertexColor(.6,.6,.6,1)
 c.text=c:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');c.text:SetPoint('CENTER');runeRow.cells[i]=c
end
-- The primary pet uses the native pet unit. The secondary companion is a
-- guardian, not a second pet unit; its authoritative snapshot comes from server.
local secondary,lastSecondary=nil,0
local pets={}
for i=1,2 do
 local card=CreateFrame(i==1 and 'Button' or 'Frame','HeroLivePet'..i,f,i==1 and 'SecureUnitButtonTemplate' or nil)
 card:SetSize(125,34);card:SetPoint('TOPLEFT',(i-1)*133,-96)
 if i==1 then card.menu=function()ToggleDropDownMenu(1,nil,PetFrameDropDown,'cursor',0,0)end;card:SetAttribute('unit','pet');card:SetAttribute('type1','target');card:SetAttribute('type2','togglemenu');card:RegisterForClicks('AnyUp');RegisterUnitWatch(card)end
 card.face=card:CreateTexture(nil,'ARTWORK');card.face:SetSize(31,31);card.face:SetPoint('TOPLEFT',0,-1)
 for half=1,2 do
  local rim=card:CreateTexture(nil,'OVERLAY');rim:SetSize(34,17);rim:SetPoint(half==1 and 'TOPLEFT'or 'BOTTOMLEFT')
  rim:SetTexture(classic);rim:SetTexCoord(217/256,149/256,half==1 and 10/128 or 44/128,half==1 and 44/128 or 10/128)
 end
 local body=CreateFrame('Frame',nil,card);body:SetPoint('TOPLEFT',32,-1);body:SetSize(93,31)
 body:SetBackdrop({bgFile='Interface\\Tooltips\\UI-Tooltip-Background',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',tile=true,tileSize=16,edgeSize=8,insets={left=2,right=2,top=2,bottom=2}});body:SetBackdropColor(.12,.12,.12,.8)
 card.name=body:CreateFontString(nil,'OVERLAY','GameFontNormalSmall');card.name:SetPoint('TOP',0,-2);card.name:SetWidth(87)
 card.bars={}
 for row=1,2 do
  local bar=CreateFrame('StatusBar',nil,body);bar:SetPoint('TOPLEFT',3,-13-(row-1)*8);bar:SetSize(87,6);bar:SetStatusBarTexture('Interface\\TargetingFrame\\UI-StatusBar')
  local bg=bar:CreateTexture(nil,'BACKGROUND');bg:SetAllPoints();bg:SetTexture(.12,.12,.12,.65)
  card.bars[row]=bar
 end
 card:EnableMouse(true)
 card:SetScript('OnEnter',function(self)
  GameTooltip:SetOwner(self,'ANCHOR_RIGHT')
  if i==1 then GameTooltip:SetUnit('pet')else GameTooltip:SetText(secondary and secondary.name or 'Secondary Companion');GameTooltip:AddLine('Use the secondary companion action bar for commands.',1,1,1,true)end
  if self.health then GameTooltip:AddLine('Health: '..self.health..' / '..self.maxHealth,1,1,1)end
  GameTooltip:Show()
 end)
 card:SetScript('OnLeave',function()GameTooltip:Hide()end)
 if i==1 then
  card.happy=CreateFrame('Button',nil,card);card.happy:SetSize(14,14);card.happy:SetPoint('BOTTOMLEFT',22,-2)
  card.happy.icon=card.happy:CreateTexture(nil,'OVERLAY');card.happy.icon:SetAllPoints();card.happy.icon:SetTexture('Interface\\PetPaperDollFrame\\UI-PetHappiness')
  card.happy:SetScript('OnEnter',function(self)
   local h,damage,loyalty=GetPetHappiness();if not h then return end
   GameTooltip:SetOwner(self,'ANCHOR_RIGHT');GameTooltip:SetText(_G['PET_HAPPINESS'..h]or ({'Unhappy','Content','Happy'})[h])
   if damage then GameTooltip:AddLine('Damage: '..damage..'%',1,1,1)end
   GameTooltip:AddLine('Feed your beast suitable food when happiness drops.',1,1,1,true);GameTooltip:Show()
  end);card.happy:SetScript('OnLeave',function()GameTooltip:Hide()end)
 else card:Hide()end
 pets[i]=card
end
local function petValues(card,h,m,p,pm,kind)
 card.health=h;card.maxHealth=m
 card.bars[1]:SetMinMaxValues(0,math.max(1,m));card.bars[1]:SetValue(h);card.bars[1]:SetStatusBarColor(.15,.8,.2)
 local color=PowerBarColor and PowerBarColor[kind]or {r=.2,g=.45,b=1}
 card.bars[2]:SetStatusBarColor(color.r,color.g,color.b);card.bars[2]:SetMinMaxValues(0,math.max(1,pm));card.bars[2]:SetValue(p)
end
local function updatePets(y)
 if not InCombatLockdown()then
  for i,card in ipairs(pets)do card:ClearAllPoints();card:SetPoint('TOPLEFT',(i-1)*133,-y)end
 end
 local card=pets[1]
 if UnitExists('pet')then
  SetPortraitTexture(card.face,'pet');card.name:SetText(UnitName('pet')or 'Pet')
  local power=UnitPowerType('pet');petValues(card,UnitHealth('pet'),UnitHealthMax('pet'),UnitPower('pet',power),UnitPowerMax('pet',power),power)
  local happiness=GetPetHappiness()
  if happiness and happiness>=1 and happiness<=3 then
   local left=({.375,.1875,0})[happiness];card.happy.icon:SetTexCoord(left,left+.1875,0,.359375);card.happy:Show()
  else card.happy:Hide()end
 end
 card=pets[2]
 if secondary and GetTime()-lastSecondary<5 then
  card.name:SetText(secondary.name);petValues(card,secondary.health,secondary.maxHealth,secondary.power,secondary.maxPower,secondary.kind)
  local portraitUnit
  for _,unit in ipairs({'target','focus','mouseover','targettarget'})do
   local guid=UnitGUID(unit)
   if guid and tonumber(guid:sub(-8),16)==secondary.guid and UnitIsFriend('player',unit)then portraitUnit=unit;break end
  end
  if portraitUnit then SetPortraitTexture(card.face,portraitUnit)else
   local _,_,icon=GetSpellInfo(secondary.spell);SetPortraitToTexture(card.face,icon or 'Interface\\Icons\\INV_Misc_QuestionMark')
  end
  card:Show()
 else card:Hide()end
end
local stockRuneParent
local stockRuneHolder=CreateFrame('Frame',nil,UIParent);stockRuneHolder:Hide()
local replacement=false
local function setReplacement(wanted)
 if InCombatLockdown()or wanted==replacement then return end
 replacement=wanted
 if wanted then
  if RuneFrame then stockRuneParent=RuneFrame:GetParent();RuneFrame:SetParent(stockRuneHolder)end
  RegisterStateDriver(PlayerFrame,'visibility','[vehicleui] show; hide');RegisterStateDriver(PetFrame,'visibility','hide')
  RegisterStateDriver(f,'visibility','[vehicleui] hide; show')
 else
  if RuneFrame and stockRuneParent then RuneFrame:SetParent(stockRuneParent);stockRuneParent=nil end
  UnregisterStateDriver(f,'visibility');f:Hide()
  UnregisterStateDriver(PlayerFrame,'visibility');PlayerFrame:Show()
  UnregisterStateDriver(PetFrame,'visibility');if UnitExists('pet')then PetFrame:Show()end
 end
end
local function has(id)return math.floor(mask/2^id)%2==1 end
local function update()
 local custom=A.mode=='Hybrid'or A.mode=='Hero'or A.mode=='ClassPlus'or A.mode=='Class+'
 setReplacement(custom)
 if not custom or UnitHasVehicleUI and UnitHasVehicleUI('player')then return end
 SetPortraitTexture(portrait,'player');name:SetText(UnitName('player')or 'Player');level:SetText(UnitLevel('player'))
 local _,own=UnitClass('player');local active=UnitPowerType('player')
 -- Center the name/resource stack on the 80px portrait until it fills it.
 -- Runes remain attached outside the stack and do not move its center.
 local count=0
 for _,d in ipairs(definitions)do if d[1]==-1 or has(d[1])or d[1]==active or showAll then count=count+1 end end
 local offset=math.max(0,(80-(20+count*13))/2)
 panel:ClearAllPoints();panel:SetPoint('TOPLEFT',80,-offset)
 header:ClearAllPoints();header:SetPoint('TOPLEFT',80,-offset);header:SetSize(153,20)
 local y=offset+20
 for _,d in ipairs(definitions)do
  local id=d[1];local b=bars[id];local enabled=id==-1 or has(id)or id==active
  if enabled or showAll then
   local max=id==-1 and UnitHealthMax('player')or UnitPowerMax('player',id)
   local value=id==-1 and UnitHealth('player')or UnitPower('player',id)
   b:ClearAllPoints();b:SetPoint('TOPLEFT',85,-y);b:SetMinMaxValues(0,math.max(1,max or 0));b:SetValue(demo and math.max(1,max or 0)or enabled and (value or 0)or 0)
   local display='--'
   if enabled and max and max>0 then display=GetCVar('statusTextPercentage')=='1' and (math.floor((value or 0)/max*100+.5)..'%')or ((value or 0)..' / '..max)end
   b.value:SetText(display);textVisible(b);b:Show();y=y+13
  else b:Hide()end
 end
 local useCombo=A.mode=='Hero'or own=='ROGUE'or own=='DRUID'or A.secondClass=='Rogue'or A.secondClass=='Druid'
 local target=UnitGUID('target');local points=demo and 5 or target and (GetComboPoints('player','target')or 0)or 0
 if demo then useCombo=true end
 if target~=lastTarget then lastPoints=0;lastTarget=target;for _,c in ipairs(combo)do c.gained=nil end end
 for i,c in ipairs(combo)do
  if useCombo or showAll then c:Show()else c:Hide()end
  if useCombo and i<=points then
   if i>lastPoints then c.gained=GetTime()end
   local age=c.gained and GetTime()-c.gained or 2
   c.highlight:SetAlpha(math.min(1,age/.4))
   c.shine:SetAlpha(age>=.4 and age<1.1 and math.sin((age-.4)/.7*math.pi)or 0)
  else c.highlight:SetAlpha(0);c.shine:SetAlpha(0);c.gained=nil end
 end
 lastPoints=points
 local panelBottom=y+2
 if has(8)or own=='DEATHKNIGHT'or showAll then
  runeRow:ClearAllPoints();runeRow:SetPoint('TOPLEFT',80,-y+2);runeRow:Show();y=y+38
  for display,c in ipairs(runeRow.cells)do
   local i=runeOrder[display]
   local kind,remaining
   if own=='DEATHKNIGHT' then
    kind=GetRuneType(i);local start,duration,ready=GetRuneCooldown(i)
    if kind then remaining=ready and 0 or math.max(0,(start or 0)+(duration or 0)-GetTime());kind=kind-1 end
   elseif runes[i]then kind=runes[i][1];remaining=math.max(0,runes[i][2]-(GetTime()-received))end
   if demo then kind=i<=2 and 0 or i<=4 and 1 or 2;remaining=0 end
   local symbol=kind and runeTextures[kind+1]
   c.icon:SetTexture(symbol and ('Interface\\PlayerFrame\\UI-PlayerFrame-Deathknight-'..symbol)or 'Interface\\PlayerFrame\\UI-PlayerFrame-Deathknight-Ring')
   c.icon:SetAlpha(1)
   c.text:SetText(not remaining and '--' or remaining>0 and math.ceil(remaining)or '')
   local expiry=not demo and remaining and (own=='DEATHKNIGHT' and GetTime()+remaining or received+runes[i][2])or 0
   if remaining and remaining>0 then
    if not c.expiry or math.abs(c.expiry-expiry)>.15 then
     c.expiry=expiry;CooldownFrame_SetTimer(c.cooldown,GetTime(),remaining,1)
    end
    c.cooldown:Show()
   else c.expiry=nil;c.cooldown:Hide()end
  end
 else runeRow:Hide()end
 panel:SetHeight(panelBottom-offset-5)
 updatePets(math.max(96,y-9))
end
local events=CreateFrame('Frame');events:RegisterEvent('CHAT_MSG_SYSTEM');events:RegisterEvent('PLAYER_ENTERING_WORLD');events:RegisterEvent('PLAYER_TARGET_CHANGED');events:RegisterEvent('UNIT_COMBO_POINTS');events:RegisterEvent('CVAR_UPDATE')
local age=0;events:SetScript('OnUpdate',function(_,dt)age=age+dt;if age>=.1 then age=0;update()end end)
events:SetScript('OnEvent',function(_,event,message)
 if event=='PLAYER_ENTERING_WORLD'then secondary=nil;lastSecondary=0 end
 if event~='CHAT_MSG_SYSTEM'then update();return end
 if type(message)~='string'then return end
 local guid,spell,h,m,p,pm,kind,petName=message:match('^MM_FRAME (%d+) (%d+) (%d+) (%d+) (%d+) (%d+) (%d+) (.+)$')
 if guid then
  secondary={guid=tonumber(guid),spell=tonumber(spell),health=tonumber(h),maxHealth=tonumber(m),power=tonumber(p),maxPower=tonumber(pm),kind=tonumber(kind),name=petName:gsub('|','')};lastSecondary=GetTime();update();return
 elseif message=='MM_FRAME 0'then secondary=nil;update();return end
 local bits,tail=message:match('^HF_RESOURCE (%d+)(.*)$');bits=tonumber(bits);if not bits or bits>331 then return end
 local nextRunes={};for kind,seconds in tail:gmatch(' (%d+):(%d+)')do
  kind=tonumber(kind);seconds=tonumber(seconds);if kind>3 or seconds>120 then return end
  nextRunes[#nextRunes+1]={kind,seconds}
 end
 if #nextRunes~=0 and #nextRunes~=6 then return end
 mask=bits;runes=nextRunes;received=GetTime();update()
end)
ChatFrame_AddMessageEventFilter('CHAT_MSG_SYSTEM',function(_,_,message)return type(message)=='string'and message:match('^MM_FRAME ')~=nil end)
SLASH_HERORESOURCEPREVIEW1='/hfresources'
SlashCmdList.HERORESOURCEPREVIEW=function(arg)
 arg=(arg or ''):lower()
 if arg=='all'then showAll=true elseif arg=='auto'then showAll=false else
  DEFAULT_CHAT_FRAME:AddMessage('/hfresources all - show all resources; /hfresources auto - show permitted resources. Drag the name header out of combat.');return
 end
 update()
end
f:Hide()
