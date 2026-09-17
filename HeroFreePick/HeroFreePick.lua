local A=HeroFreePick
local f=HeroFreePickFrame
local L=HeroMenuLayout
local pointWarning=CreateFrame('Frame',nil,UIParent)
pointWarning:SetFrameStrata('TOOLTIP');pointWarning:SetFrameLevel(200);pointWarning:SetSize(760,70);pointWarning:SetPoint('TOP',f,'TOP',0,-78);pointWarning:EnableMouse(false)
local warningText=pointWarning:CreateFontString(nil,'OVERLAY');warningText:SetAllPoints(pointWarning);warningText:SetFont(STANDARD_TEXT_FONT or 'Fonts\\FRIZQT__.TTF',26,'THICKOUTLINE');warningText:SetTextColor(1,.3,.12);warningText:SetShadowColor(0,0,0,1);warningText:SetShadowOffset(2,-2);warningText:SetJustifyH('CENTER')
pointWarning:Hide()
local remaining=0
pointWarning:SetScript('OnUpdate',function(self,elapsed)remaining=remaining-elapsed;if remaining<=0 or not f:IsShown()then self:Hide()else self:SetAlpha(math.min(1,remaining))end end)
local lastWarningSound=-100
function A.ShowPointWarning(message)
 warningText:SetText(message);remaining=3;pointWarning:SetAlpha(1);pointWarning:Show()
 local now=GetTime and GetTime()or 0
 if PlaySound and now-lastWarningSound>=1 then PlaySound('RaidWarning');lastWarningSound=now end
end

local GOLD={1,.82,.3};local colors={Normal='ffffff',Uncommon='1eff00',Rare='0070dd',Epic='a335ee',Legendary='ff8000'}
local function essenceCost(value)
 return '|TInterface\\AddOns\\HeroFreePick\\Art\\AbilityEssence:16:16:0:0|t '..tostring(value or 0)
end
local function talentCost(value)
 return '|TInterface\\AddOns\\HeroFreePick\\Art\\TalentEssence:16:16:0:0|t '..tostring(value or 0)
end
A.TalentCostMarkup=talentCost
local function rarityCost(e)
 if A.IsTalent(e) or e.quality=='Normal' then return '' end
 local gem='|TInterface\\AddOns\\HeroFreePick\\Art\\Rarity'..e.quality..':14:12:0:0|t'
 return string.rep(gem,(HeroRarityCosts or {})[e.id]or 1)
end
A.EssenceCostMarkup=essenceCost
A.RarityCostMarkup=rarityCost
local function txt(parent,value,x,y,w,font)
 local t=parent:CreateFontString(nil,'OVERLAY',font or 'GameFontHighlightSmall');t:SetPoint('TOPLEFT',x,y);t:SetWidth(w);t:SetJustifyH('LEFT');t:SetText(value);return t
end
local function btn(parent,label,x,y,w,fn)
 local b=CreateFrame('Button',nil,parent,'UIPanelButtonTemplate');b:SetSize(w,25);b:SetPoint('TOPLEFT',x,y);b:SetText(label);b:SetScript('OnClick',fn);return b
end
local function panel(parent,x,y,w,h)
 local p=CreateFrame('Frame',nil,parent);p:SetPoint('TOPLEFT',x,y);p:SetSize(w,h)
 p:SetBackdrop({bgFile='Interface\\Tooltips\\UI-Tooltip-Background',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',tile=true,tileSize=16,edgeSize=12,insets={left=3,right=3,top=3,bottom=3}})
 p:SetBackdropColor(.035,.035,.035,1);p:SetBackdropBorderColor(.43,.43,.40,1);return p
end
local function scroll(parent,name,x,y,w,h)
 local s=CreateFrame('ScrollFrame',name,parent,'UIPanelScrollFrameTemplate');s:SetPoint('TOPLEFT',x,y);s:SetSize(w,h)
 local c=CreateFrame('Frame',nil,s);c:SetSize(w,1);s:SetScrollChild(c)
 s:EnableMouseWheel(true);s:SetScript('OnMouseWheel',function(self,delta)self:SetVerticalScroll(math.max(0,math.min(self:GetVerticalScroll()-delta*45,self:GetVerticalScrollRange())))end)
 return s,c
end
local function icon(e)
 local packaged=A.mode~='Classic'and A.PackageSpellIcons and A.PackageSpellIcons[e.spells[1]];if packaged then return packaged end
 local _,_,texture=GetSpellInfo(e.spells[1]);if texture then return texture end
 local path=(HeroFreePickLayout[e.id]or{}).icon
 if path and path~='' then return 'Interface\\Icons\\'..path end
 return 'Interface\\Icons\\INV_Misc_QuestionMark'
end

-- Interactive mastery tooltip: real icon buttons support a separate spell preview.
A.EntryIcon=icon
local masteryTip=panel(UIParent,0,0,370,164)
masteryTip:SetFrameStrata('TOOLTIP');masteryTip:SetFrameLevel(20);masteryTip:SetClampedToScreen(true);masteryTip:EnableMouse(true)
local masteryTitle=txt(masteryTip,'',12,-12,346,'GameFontNormalLarge')
local masteryDescription=txt(masteryTip,'Learning this Mastery unlocks access to every connected ability when your character reaches that ability\'s required level. Connected abilities cost no additional Ability Points, Talent Points, or rarity gems.',12,-38,346)
masteryDescription:SetHeight(70)
local masteryCost=txt(masteryTip,'',12,-112,346)
local masteryHint=txt(masteryTip,'',12,-140,346,'GameFontNormalSmall')
local masteryPreview=CreateFrame('GameTooltip','HeroMasteryAbilityPreview',UIParent,'GameTooltipTemplate')
masteryPreview:SetFrameStrata('TOOLTIP');masteryPreview:SetFrameLevel(30);masteryPreview:SetClampedToScreen(true)
local masteryRows={}
A.MasteryTooltip=masteryTip;A.MasteryTooltipRows=masteryRows
function A.MasteryTooltipMembers(m)
 local out={}
 for _,spell in ipairs(m.members or {})do
  local entry
  for _,candidate in ipairs(HeroFreePickCatalog)do
   if (candidate.requiredMastery==m.id or candidate.requiredBundle==m.id) then
    for _,id in ipairs(candidate.spells)do if id==spell then entry=candidate;break end end
   end
   if entry then break end
  end
  local name,_,texture=GetSpellInfo(spell)
  out[#out+1]={spell=spell,name=entry and entry.name or name or ('Spell '..spell),level=entry and entry.level,texture=(A.mode~='Classic'and A.PackageSpellIcons and A.PackageSpellIcons[spell])or texture or(entry and icon(entry))or 'Interface\\Icons\\INV_Misc_QuestionMark'}
 end
 table.sort(out,function(a,b)
  local al,bl=a.level or math.huge,b.level or math.huge
  if al~=bl then return al<bl end
  if a.name~=b.name then return a.name<b.name end
  return a.spell<b.spell
 end)
 return out
end
local masteryOwner,masteryEntry,masteryExpanded,masteryAway
local function hideMasteryTooltip()
 masteryTip:Hide();masteryPreview:Hide();masteryOwner=nil;masteryEntry=nil
end
local function showMasteryTooltip(owner)
 local e=owner.entry;masteryOwner=owner;masteryEntry=e;masteryAway=0
 if not e.isMastery and not e.isBundle then hideMasteryTooltip();return end
 masteryExpanded=IsShiftKeyDown and IsShiftKeyDown()or false
 GameTooltip:Hide();masteryPreview:Hide()
 masteryTitle:SetText(e.name)
 masteryDescription:SetText(e.isBundle and 'This companion bundle includes all listed abilities at level 1 for one purchase. Included abilities cost no additional points or rarity gems. Preview only: server learning and custom pets are not implemented.'or 'Learning this Mastery unlocks access to every connected ability when your character reaches its required level. Connected abilities are automatically included at their required levels, with no additional cost.')
 masteryCost:SetText((e.isBundle and 'Bundle cost: 'or 'Mastery cost: ')..rarityCost(e)..'  '..essenceCost(e.ae))
 masteryHint:SetText(masteryExpanded and 'Release SHIFT to hide. Hover an ability icon to preview.'or 'Hold SHIFT to show connected abilities.')
 for _,row in ipairs(masteryRows)do row:Hide()end
 local original=A.SummoningDescriptions and A.SummoningDescriptions[e.spells[1]]
 if original then masteryDescription:SetText(original..'\n\n'..(e.isBundle and 'Bundle: 4 Ability Points and 2 Epic gems; included skills have no additional cost. Server learning is not enabled.'or 'Our rules: purchase this Mastery first; its level-eligible members are automatically included at no additional cost.'))end
 masteryDescription:SetHeight(0)
 local descriptionHeight=math.max(70,masteryDescription:GetStringHeight())
 masteryDescription:SetHeight(descriptionHeight)
 masteryCost:ClearAllPoints();masteryCost:SetPoint('TOPLEFT',12,-42-descriptionHeight)
 masteryHint:ClearAllPoints();masteryHint:SetPoint('TOPLEFT',12,-70-descriptionHeight)
 local listTop=96+descriptionHeight
 local members=A.MasteryTooltipMembers(e)
 if masteryExpanded then
  for i,member in ipairs(members)do
   local row=masteryRows[i]
   if not row then
    row=CreateFrame('Button',nil,masteryTip);row:SetFrameLevel(21);row:SetSize(28,28);row:EnableMouse(true)
    row.texture=row:CreateTexture(nil,'ARTWORK');row.texture:SetAllPoints(row)
    row.label=txt(row,'',36,-1,298);row.label:SetHeight(28)
    row:SetScript('OnEnter',function(self)
     local m=self.member;masteryPreview:SetOwner(self,'ANCHOR_RIGHT')
     local description=A.SummoningDescriptions and A.SummoningDescriptions[m.spell]
     if description then masteryPreview:SetText(m.name);masteryPreview:AddLine(description,1,1,1,true)elseif GetSpellInfo(m.spell)then masteryPreview:SetHyperlink('spell:'..m.spell)else masteryPreview:SetText(m.name);masteryPreview:AddLine('Spell description is unavailable in this client.',1,.7,.3,true)end
     masteryPreview:AddLine(m.level and ('Requires Level '..m.level)or 'Required level unavailable',1,.82,.3)
     masteryPreview:AddLine('Requires '..(masteryEntry.requiredBundle and A.byID[masteryEntry.requiredBundle].name or masteryEntry.name),1,.82,.3,true)
     masteryPreview:AddLine('No additional points or rarity gems.',.7,.85,1,true);masteryPreview:Show()
    end)
    row:SetScript('OnLeave',function()masteryPreview:Hide()end)
    masteryRows[i]=row
   end
   row.member=member;row:SetPoint('TOPLEFT',masteryTip,'TOPLEFT',12,-listTop-(i-1)*34);row.texture:SetTexture(member.texture)
   row.label:SetText(member.name..'\n|cffffd100'..(member.level and ('Level '..member.level)or 'Level unavailable')..'|r');row:Show()
  end
 end
 masteryTip:SetHeight(listTop+(masteryExpanded and (#members*34+8)or 0))
 masteryTip:ClearAllPoints();masteryTip:SetPoint('TOPLEFT',owner,'TOPRIGHT',0,0);masteryTip:Show()
end
A.ShowMasteryTooltip=showMasteryTooltip
function A.RefreshMasteryTooltip()
 if masteryOwner and masteryTip:IsShown()then showMasteryTooltip(masteryOwner);return true end
 return false
end
masteryTip:SetScript('OnUpdate',function(_,elapsed)
 if not masteryOwner or not masteryOwner:IsShown()or masteryOwner.entry~=masteryEntry or not f:IsShown()then hideMasteryTooltip();return end
 local expanded=IsShiftKeyDown and IsShiftKeyDown()or false
 if expanded~=masteryExpanded then showMasteryTooltip(masteryOwner)end
 if MouseIsOver(masteryOwner)or MouseIsOver(masteryTip)then masteryAway=0 else
  masteryAway=(masteryAway or 0)+elapsed;if masteryAway>.3 then hideMasteryTooltip()end
 end
end)
masteryTip:Hide();masteryPreview:Hide()
local function leaveEntryTooltip(self)
 if not self.entry or not (self.entry.isMastery or self.entry.isBundle) then GameTooltip:Hide()end
end


function A.TalentPrerequisiteLines(e)
 local out={}
 if A.mode~='Classic'then return {{text='Requires Level '..A.TalentRequiredLevel(e),met=UnitLevel('player')>=A.TalentRequiredLevel(e),kind='level'}}end
 local node=A.TalentNode(e);if not node then return out end
 local lower,dependency=0,nil
 for _,candidate in ipairs(HeroFreePickCatalog)do if candidate.class==e.class and A.IsTalent(candidate)then
  local n=A.TalentNode(candidate)
  if n then
   if n.spec==node.spec and n.row<node.row then lower=lower+A.PendingRank(candidate)end
   if n.talent==node.depends then dependency=candidate end
  end
 end end
 if node.row>0 then out[#out+1]={text='Requires '..node.row*5 ..' points in '..e.spec..' Talents',met=lower>=node.row*5,kind='tree'}end
 if node.depends>0 then local needed=math.max(1,node.dependsRank);out[#out+1]={text='Requires '..needed..' points in '..(dependency and dependency.name or 'prerequisite talent'),met=dependency and A.PendingRank(dependency)>=needed or false,kind='dependency'}end
 return out
end
local function prerequisiteColor(met)if met then return .1,1,.1 end;return 1,.15,.15 end
local function classicPrerequisites(e)
 local requirements=A.TalentPrerequisiteLines(e);local replaced={}
 local lineCount=GameTooltip:NumLines()
 for i=1,(tonumber(lineCount)or 0)do
  local line=_G['GameTooltipTextLeft'..i]
  local text=line and line:GetText()
  if text then
   text=text:gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r','')
   if text:match('^Requires %d+ points? in ')then
    local kind=text:find('Talents',1,true)and 'tree'or 'dependency'
    for j,req in ipairs(requirements)do if req.kind==kind then line:SetText(req.text);line:SetTextColor(prerequisiteColor(req.met));replaced[j]=true;break end end
   end
  end
 end
 for j,req in ipairs(requirements)do if not replaced[j]then GameTooltip:AddLine(req.text,prerequisiteColor(req.met))end end
end

local function tooltip(self)
 local e=self.entry;if not e then return end
 if e.isMastery or e.isBundle then showMasteryTooltip(self);return end
 hideMasteryTooltip()
 if A.IsTalent(e) and not A.TalentsUnlocked() then GameTooltip:Hide();return end
 GameTooltip:SetOwner(self,'ANCHOR_RIGHT')
 local nativeTab,nativeIndex=A.NativeTalent(e)
 if A.mode=='Classic'and nativeTab then GameTooltip:SetTalent(nativeTab,nativeIndex,false,false,GetActiveTalentGroup());classicPrerequisites(e);GameTooltip:AddLine('Pending rank: '..A.PendingRank(e)..'/'..A.MaxRank(e),1,.82,.3);GameTooltip:AddLine('Left-click adds a point. Right-click removes a point. Changes are pending until reviewed.',1,.82,.3,true);GameTooltip:Show();return end
 local rank=math.max(1,A.PendingRank(e));local id=e.spells[math.min(rank,#e.spells)]
 local description=A.mode~='Classic'and A.SummoningDescriptions and A.SummoningDescriptions[id]
 if description then GameTooltip:SetText(e.name);GameTooltip:AddLine(description,1,1,1,true)elseif GetSpellInfo(id)then GameTooltip:SetHyperlink('spell:'..id)else GameTooltip:SetText(e.name);GameTooltip:AddLine('Spell data is absent from this client.',1,.35,.3,true)end
 GameTooltip:AddLine(' ');GameTooltip:AddLine(e.class..' / '..e.spec..' / '..e.kind,1,.82,.3)
 local grouping=HeroBrowseAssignment[e.id];if grouping and not grouping.direct then GameTooltip:AddLine('Browse grouping: recovered tags (no direct A52 category).',1,.7,.3,true)end
 local requiredLevel=A.IsTalent(e)and A.mode~='Classic'and A.TalentRequiredLevel(e)or(e.level or 1)
 local locked=A.OtherClass(e.class)or UnitLevel('player')<requiredLevel
 if A.IsTalent(e)and A.mode~='Classic'then
  GameTooltip:AddLine('Requires Level '..requiredLevel,prerequisiteColor(UnitLevel('player')>=requiredLevel))
  GameTooltip:AddLine('Pending rank: '..A.PendingRank(e)..'/'..A.MaxRank(e),1,.82,.3)
  GameTooltip:AddLine('Talent tiers unlock every 5 levels from level 10. No tree-investment or prerequisite talent requirement.',.7,.85,1,true)
 else GameTooltip:AddLine(e.quality..' | Requires Level '..requiredLevel,1,locked and .15 or .82,locked and .15 or .3)end
 if not A.IsTalent(e)then
  GameTooltip:AddLine(rarityCost(e)..'  '..essenceCost(e.ae),1,1,1)
 else GameTooltip:AddDoubleLine('Talent Point Cost',talentCost(e.te),1,.82,.3,1,1,1)end
 GameTooltip:AddDoubleLine('Spell ID',tostring(id),.75,.75,.75,1,1,1)
 GameTooltip:AddDoubleLine('Character Advancement ID',tostring(e.area52Entry or e.id),.75,.75,.75,1,1,1)
 if e.isMastery then GameTooltip:AddLine('Mastery: 2 Ability Points. Member abilities cost no points or rarity gems.',.7,.85,1,true)end
 if A.mode=='Classic'and not A.IsTalent(e)then GameTooltip:AddLine('Learn this ability from a trainer through normal Classic progression.',1,.82,.3,true);GameTooltip:Show();return end
 if e.requiredBundle then GameTooltip:AddLine('Included with '..A.byID[e.requiredBundle].name..'. Add or remove the bundle to change these abilities. No additional cost.',1,.82,.3,true)end
 if e.requiredMastery then GameTooltip:AddLine('Requires '..A.byID[e.requiredMastery].name..' selected first. Automatically included at the required level; no additional cost.',1,.82,.3,true)end
 if IsShiftKeyDown and IsShiftKeyDown()then
  GameTooltip:AddLine('Costs use the selected non-random client record. Ability Points are deducted from the local selection budget.',.7,.85,1,true)
 else GameTooltip:AddLine('Hold SHIFT for more information',.2,.85,1)end
 if self.learned then GameTooltip:AddLine('Left-click adds a pending rank; right-click removes one.',1,.82,.3);GameTooltip:Show();return end
 GameTooltip:AddLine('Left-click adds a pending rank. Right-click removes a pending rank.',.5,.9,.8,true)
 GameTooltip:AddLine('Pending preparation only. Closing opens a change review; server committing is unavailable.',1,.6,.3,true);GameTooltip:Show()
end

-- Shared badge policy for every ability view; Classic never displays Mastery UI.
local function updateMasteryBadge(b,e)
 local badge=rawget(b,'masteryBadge')
 local mastery=A.mode~='Classic'and not A.IsTalent(e)and (e.requiredMastery or e.requiredBundle) and A.byID[e.requiredMastery or e.requiredBundle]
 if not mastery or rawget(b,'groupedLearnedChild')then
  if badge then if masteryOwner==badge then hideMasteryTooltip()end;badge.entry=nil;badge:Hide()end
  return
 end
 if not badge then
  badge=CreateFrame('Button',nil,b);b.masteryBadge=badge
  badge:SetSize(13,13);badge:SetFrameLevel(b:GetFrameLevel()+3);badge:EnableMouse(true)
  badge:SetPoint('BOTTOMRIGHT',b.icon,'BOTTOMRIGHT',0,0)
  badge.texture=badge:CreateTexture(nil,'ARTWORK');badge.texture:SetAllPoints(badge)
  badge:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square')
  badge:SetScript('OnEnter',tooltip);badge:SetScript('OnLeave',leaveEntryTooltip)
 end
 badge.entry=mastery;badge.texture:SetTexture(icon(mastery));badge:Show()
end
A.UpdateMasteryBadge=updateMasteryBadge

A.ShowEntryTooltip=tooltip
local prerequisiteRefresh=CreateFrame('Frame')
local prerequisiteElapsed=0
prerequisiteRefresh:SetScript('OnUpdate',function(_,elapsed)
 prerequisiteElapsed=prerequisiteElapsed+elapsed;if prerequisiteElapsed<.15 then return end;prerequisiteElapsed=0
 local owner=GameTooltip:GetOwner()
 if GameTooltip:IsShown()and owner and owner.entry and A.IsTalent(owner.entry)and MouseIsOver(owner)then tooltip(owner)end
end)
local function selectEntry(e)A.selected=e;A.AdjustPending(e,1)end
local function entryButton(parent,w,h)
 local b=CreateFrame('Button',nil,parent);b:SetSize(w,h);b:RegisterForClicks('LeftButtonUp','RightButtonUp')
 b:SetBackdrop({bgFile='Interface\\Tooltips\\UI-Tooltip-Background',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',edgeSize=8,insets={left=2,right=2,top=2,bottom=2}});b:SetBackdropColor(.065,.045,.025,.84);b:SetBackdropBorderColor(.32,.25,.13,.8)
 b:SetHighlightTexture('Interface\\QuestFrame\\UI-QuestTitleHighlight')
 b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetSize(32,32);b.icon:SetPoint('TOPLEFT',5,-5)
 b.name=txt(b,'',43,-5,w-48);b.name:SetHeight(29);b.name:SetJustifyV('TOP')
 b.rank=txt(b,'',43,-44,w-48,'GameFontNormalSmall');b.rank:SetHeight(24)
 b.name:SetHeight(38)
 if w<135 then
  b.icon:ClearAllPoints();b.icon:SetPoint('TOP',0,-3)
  b.name:ClearAllPoints();b.name:SetPoint('TOPLEFT',3,-39);b.name:SetWidth(w-6);b.name:SetHeight(38);b.name:SetJustifyH('CENTER')
  b.rank:ClearAllPoints();b.rank:SetPoint('TOPLEFT',3,-80);b.rank:SetWidth(w-6);b.rank:SetJustifyH('CENTER')
 end
 b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip)
 b:SetScript('OnClick',function(self,mouse)A.AdjustPending(self.entry,mouse=='RightButton'and -1 or 1) end)
 return b
end
local function fill(b,e,showClass)
 b.entry=e;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e);b.name:SetText('|cff'..(colors[e.quality]or'ffffff')..e.name..'|r')
 local rank=HeroFreePickPlans.entries[e.id]or 0
 b.rank:SetText((showClass and e.class..'  -  ' or '')..rank..'/'..A.MaxRank(e)..' planned')
 if rank>0 then b.rank:SetTextColor(.3,1,.4)else b.rank:SetTextColor(.7,.7,.7)end
 b:Show()
end
f:RegisterForDrag('LeftButton');f:SetScript('OnDragStart',f.StartMoving);f:SetScript('OnDragStop',f.StopMovingOrSizing);tinsert(UISpecialFrames,'HeroFreePickFrame')
-- Use native 3.3.5 window artwork rather than external addon textures.
f:SetAlpha(1);f:SetFrameStrata('FULLSCREEN_DIALOG')
f:SetBackdrop({bgFile='Interface\\DialogFrame\\UI-DialogBox-Background',edgeFile='Interface\\DialogFrame\\UI-DialogBox-Border',tile=true,tileSize=32,edgeSize=32,insets={left=11,right=11,top=11,bottom=11}})
f:SetBackdropColor(1,1,1,1);f:SetBackdropBorderColor(1,1,1,1)
local stone=f:CreateTexture(nil,'ARTWORK',nil,-7);stone:SetPoint('TOPLEFT',11,-11);stone:SetPoint('BOTTOMRIGHT',-11,6)
stone:SetTexture('Interface\\PaperDollInfoFrame\\UI-Character-General-TopLeft');stone:SetTexCoord(80/256,250/256,38/256,67/256);stone:SetVertexColor(1,1,1,1);stone:SetAlpha(1)
local outerBorder=CreateFrame('Frame',nil,f);outerBorder:SetAllPoints(f);outerBorder:SetFrameLevel(f:GetFrameLevel()+1);outerBorder:EnableMouse(false)
outerBorder:SetBackdrop({edgeFile='Interface\\DialogFrame\\UI-DialogBox-Border',edgeSize=32});outerBorder:SetBackdropBorderColor(1,1,1,1)


local header=panel(f,48,-7,1124,29)
local title=txt(header,'Hero Advancement',8,-7,1048,'GameFontNormal');title:SetJustifyH('CENTER')
local closeBox=panel(f,1143,-7,29,29)
local infoBox=panel(f,1114,-7,29,29)
if HeroFreePickFrameClose then HeroFreePickFrameClose:SetParent(closeBox);HeroFreePickFrameClose:ClearAllPoints();HeroFreePickFrameClose:SetPoint('CENTER',closeBox,'CENTER',0,0);HeroFreePickFrameClose:SetSize(28,28);HeroFreePickFrameClose:SetScript('OnClick',function()f:Hide()end)end
local infoButton=CreateFrame('Button',nil,infoBox);infoButton:SetAllPoints(infoBox)
local infoLabel=txt(infoButton,'i',0,-6,29,'GameFontNormalLarge');infoLabel:SetJustifyH('CENTER')
infoButton:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square')
local function showModuleInfo(self)GameTooltip:SetOwner(self,'ANCHOR_BOTTOM');GameTooltip:SetText('Hero Advancement');GameTooltip:AddLine('Hero class development and ability planning.',1,1,1,true);GameTooltip:AddLine('Module GitHub link coming soon.',1,.82,.3,true);GameTooltip:Show()end
infoButton:SetScript('OnEnter',showModuleInfo);infoButton:SetScript('OnClick',showModuleInfo);infoButton:SetScript('OnLeave',function()GameTooltip:Hide()end)

local emblem=CreateFrame('Frame',nil,f);emblem:SetFrameLevel(f:GetFrameLevel()+10);emblem:SetSize(66,66);emblem:SetPoint('TOPLEFT',-12,18)
local well=CreateFrame('Frame',nil,emblem);well:SetSize(64,64);well:SetPoint('CENTER')
-- Circular clipping with native texture coordinates (3.3.5 has no mask textures).
for y=0,63 do
 local dy=math.max(math.abs(y-32),math.abs(y+1-32));local half=math.sqrt(math.max(0,32*32-dy*dy));local left=32-half
 if half>0 then local strip=well:CreateTexture(nil,'ARTWORK');strip:SetTexture('Interface\\Icons\\Ability_Paladin_BeaconOfLight');strip:SetPoint('TOPLEFT',left,-y);strip:SetSize(half*2,1);strip:SetTexCoord(.08+.84*left/64,.08+.84*(64-left)/64,.08+.84*y/64,.08+.84*(y+1)/64)end
end
local rim=well:CreateTexture(nil,'OVERLAY');rim:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing');rim:SetSize(80,80);rim:SetPoint('CENTER',well,'CENTER',0,0)
emblem:EnableMouse(true);emblem:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_RIGHT');GameTooltip:SetText('Hero Advancement');GameTooltip:AddLine('Atonement',1,.82,.3);GameTooltip:Show()end);emblem:SetScript('OnLeave',function()GameTooltip:Hide()end)

local mode=txt(f,'',700,-139,425,'GameFontNormalSmall');mode:Hide()
A.isBrowse=true
if UnitClass then local _,own=UnitClass('player');for _,class in ipairs(A.classes)do if string.upper(class)==own then A.class=class;A.isBrowse=false;A.spec='All';break end end end
local function spent(class,spec)
 local total=0
 for _,e in ipairs(A.LearnedEntries())do if not A.IsTalent(e) and (not class or e.class==class) and (not spec or e.spec==spec)then total=total+(e.ae or 0)end end
 return total
end
local function badge(parent)
 local b=CreateFrame('Frame',nil,parent);b:SetSize(20,20);b:SetPoint('TOPRIGHT',-1,-1)
 -- Layered scanlines create a shaded spherical face without new client assets.
 local function disc(radius,cx,cy,layer,color)
  for y=0,19 do local dy=y+.5-cy
   if math.abs(dy)<radius then local w=2*math.sqrt(radius*radius-dy*dy);local t=b:CreateTexture(nil,layer);t:SetSize(w,1);t:SetPoint('TOPLEFT',cx-w/2,-y);t:SetTexture(color(y))end
  end
 end
 disc(9.7,10.7,11,'BACKGROUND',function()return 0,0,0,.8 end)
 disc(9.1,10,9.5,'ARTWORK',function(y)local light=1-y/24;return .30*light,.43*light,.62*light,1 end)
 disc(7.7,10,9.5,'ARTWORK',function(y)local light=math.max(0,1-y/18);return .025+.10*light,.075+.20*light,.20+.40*light,1 end)
 disc(5.4,9,6.7,'ARTWORK',function(y)local alpha=math.max(0,.28-y*.035);return .6,.8,1,alpha end)
 b.value=txt(b,'',0,-3,20,'GameFontHighlightSmall');b.value:SetJustifyH('CENTER');b.value:SetShadowColor(0,0,0,1);b.value:SetShadowOffset(1,-1)

 return b
end
local function setBadge(b,n)b.value:SetText(n);if n>0 then b:Show()else b:Hide()end end
local classButtons={}
local badges={Browse='INV_Misc_Spyglass_03',Warrior='Ability_Warrior_SavageBlow',Paladin='Spell_Holy_SealOfMight',Hunter='INV_Weapon_Bow_07',Rogue='Ability_BackStab',Priest='Spell_Holy_PowerWordShield',DeathKnight='Spell_Deathknight_ClassIcon',Shaman='Spell_Nature_Lightning',Mage='Spell_Fire_FireBolt02',Warlock='Spell_Shadow_ShadowBolt',Druid='Ability_Druid_Maul'}
for i,name in ipairs({'Browse',unpack(A.classes)})do
 local c=name;local b=CreateFrame('Button',nil,f);b:SetSize(100,63);b:SetPoint('TOPLEFT',25+(i-1)*102,-43)
 local tex=b:CreateTexture(nil,'ARTWORK');tex:SetSize(42,42);tex:SetPoint('TOP',0,-2)
 if SetPortraitToTexture then SetPortraitToTexture(tex,'Interface\\Icons\\'..badges[c])else tex:SetTexture('Interface\\Icons\\'..badges[c])end
 local ring=b:CreateTexture(nil,'OVERLAY');ring:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing');ring:SetSize(59,59);ring:SetPoint('CENTER',tex,'CENTER',0,0);b.ring=ring
 local shadow=b:CreateTexture(nil,'BACKGROUND');shadow:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing');shadow:SetSize(66,66);shadow:SetPoint('CENTER',tex,'CENTER',2,-3);shadow:SetVertexColor(0,0,0,.85)
 local inner=b:CreateTexture(nil,'OVERLAY');inner:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing');inner:SetSize(52,52);inner:SetPoint('CENTER',tex,'CENTER',0,0)
 b.label=txt(b,c=='DeathKnight'and'Death Knight'or c,0,-44,100,'GameFontNormal');b.label:SetFont(STANDARD_TEXT_FONT or 'Fonts\\FRIZQT__.TTF',14,'OUTLINE');b.label:SetJustifyH('CENTER');b.label:SetDrawLayer('OVERLAY',7);b.label:SetShadowColor(0,0,0,1);b.label:SetShadowOffset(2,-2)
 b:SetScript('OnClick',function()A.summary=false;A.isBrowse=c=='Browse';if not A.isBrowse then A.class=c end;A.spec='All';A.query='';A.learnedQuery='';A.quality='All';A.ownership='All';A.learnedFilter='All';if A.ClearSearch then A.ClearSearch()end;A.selected=nil;A.view='browse';A.Refresh(true)end)
 b:SetScript('OnEnter',function(self)self.ring:SetVertexColor(1,.82,.3)end)
 b:SetScript('OnLeave',function(self)A.Refresh() end)
 b.glows={}
 for j=1,4 do local g=b:CreateTexture(nil,'OVERLAY');g:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing');g:SetSize(57+j*2,57+j*2);g:SetPoint('CENTER',tex,'CENTER',0,0);g:SetVertexColor(1,.9,.12,(5-j)*.22);g:SetBlendMode('ADD');g:Hide();b.glows[j]=g end
 b.portrait=tex;b.spentBadge=badge(b);b.spentBadge:ClearAllPoints();b.spentBadge:SetPoint('CENTER',ring,'RIGHT',-1,0);classButtons[c]=b;L.Bind('class'..i,b)
end
-- Native character-sheet tabs, with inherited CharacterFrame handlers replaced.
local function navigationTab(name,label,x,view)
 local tab=CreateFrame('Button',name,f,'CharacterFrameTabButtonTemplate')
 tab:SetText(label);tab:SetPoint('TOPLEFT',f,'BOTTOMLEFT',x,5)
 tab:SetScript('OnClick',function()A.view=view;A.Refresh(true)end)
 tab:SetScript('OnShow',function(self)PanelTemplates_TabResize(self,16);if A.view==view then PanelTemplates_SelectTab(self)else PanelTemplates_DeselectTab(self)end end)
 PanelTemplates_TabResize(tab,16)
 return tab
end
local browseTab=navigationTab('HeroBuilderDevelopmentTab','Hero Advancement',20,'browse')
local architectTab=navigationTab('HeroBuilderArchetypeTab','Archetype Builder',215,'architect')
architectTab:ClearAllPoints();architectTab:SetPoint('TOPLEFT',browseTab,'TOPRIGHT',-8,0)
local function disableArchitectTab()
 PanelTemplates_DeselectTab(architectTab);architectTab:Disable();architectTab:SetDisabledFontObject(GameFontDisableSmall)
end
architectTab:SetScript('OnClick',nil)
architectTab:SetScript('OnShow',function(self)PanelTemplates_TabResize(self,16);disableArchitectTab()end)
disableArchitectTab()



local toolbar=CreateFrame('Frame',nil,f);toolbar:SetAllPoints(f)
local search=CreateFrame('EditBox',nil,toolbar,'InputBoxTemplate');search:SetSize(225,23);search:SetPoint('TOPLEFT',38,-154);search:SetAutoFocus(false)
search:SetScript('OnEscapePressed',function(self)self:ClearFocus()end)
search:SetScript('OnTextChanged',function(self)A.query=self:GetText();if A.Refresh then A.Refresh(true)end end)
txt(toolbar,'Search abilities',35,-180,220,'GameFontDisableSmall')
local dropdowns={}
local function dropdown(key,title,x,w,options)
 local d=CreateFrame('Frame','HeroBuilderFilter'..key,toolbar,'UIDropDownMenuTemplate');d:SetPoint('TOPLEFT',x,-150);UIDropDownMenu_SetWidth(d,w)
 UIDropDownMenu_Initialize(d,function()for _,v in ipairs(options)do local value=v;local info=UIDropDownMenu_CreateInfo();info.text=v;info.checked=A[key]==v;info.func=function()A[key]=value;A.Refresh(true)end;UIDropDownMenu_AddButton(info)end end)
 txt(toolbar,title,x+18,-180,w,'GameFontDisableSmall');dropdowns[key]=d
end
txt(toolbar,'Stock 3.3.5 catalogue',295,-155,160,'GameFontNormalSmall')
 txt(toolbar,'Client rarity / level references',295,-180,160,'GameFontDisableSmall')
dropdown('ownership','Plan selection',446,155,{'All','Planned','Not planned'})
local rarityLabel=txt(toolbar,'Ability rarity',655,-180,155,'GameFontDisableSmall')
local rarity=CreateFrame('Frame','HeroBuilderRarity',toolbar,'UIDropDownMenuTemplate');rarity:SetPoint('TOPLEFT',637,-150);UIDropDownMenu_SetWidth(rarity,145)
UIDropDownMenu_Initialize(rarity,function()for _,q in ipairs({'All','Normal','Uncommon','Rare','Epic','Legendary'})do local value=q;local info=UIDropDownMenu_CreateInfo();info.text=q;info.checked=A.quality==q;info.func=function()A.quality=value;A.Refresh(true)end;UIDropDownMenu_AddButton(info)end end)
dropdowns.quality=rarity
local specs={}
for i=1,4 do
 local idx=i;local b=CreateFrame('Button','HeroSpecializationTab'..i,f);b:SetSize(i==4 and 150 or 110,31);b:SetPoint('TOPLEFT',i==4 and 25 or (483+(i-1)*112),-106);b:SetFrameLevel(f:GetFrameLevel()+10)
 b.tabPieces={}
 for j=1,3 do local t=b:CreateTexture(nil,'BACKGROUND');b.tabPieces[j]=t;t:SetHeight(32)
 local width=i==4 and 150 or 110
 t:SetWidth(j==2 and width-40 or 20);t:SetPoint('TOPLEFT',j==1 and 0 or(j==2 and 20 or width-20),0)
 local left=({0,.15625,.84375})[j];local right=({.15625,.84375,1})[j];t:SetTexCoord(left,right,1,0)
 end
 b.caption=txt(b,'',4,-8,i==4 and 142 or 102,'GameFontNormalSmall');b.caption:SetJustifyH('CENTER');b.SetText=function(self,value)self.caption:SetText(value)end
 b.bridge=b:CreateTexture(nil,'OVERLAY');b.bridge:SetTexture(.055,.049,.034,1);b.bridge:SetPoint('TOPLEFT',20,-30);b.bridge:SetPoint('TOPRIGHT',-20,-30);b.bridge:SetHeight(3);b.bridge:Hide()

 b:SetScript('OnShow',function()end)
 b:SetScript('OnClick',function()local names=A.Specs();A.summary=idx==4;if not A.summary then A.isBrowse=false;A.spec=names[idx+1]end;A.Refresh(true)end);b:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_TOP');GameTooltip:SetText('Click Class Icon to Clear Filters');GameTooltip:Show()end);b:SetScript('OnLeave',function()GameTooltip:Hide()end);b.spentBadge=badge(b);specs[i]=b
end
local spellsPanel=panel(f,25,-135,451,433);local talentsPanel=panel(f,483,-135,334,433);local side=panel(f,828,-106,326,462)
local function parchment(p)
 p:SetBackdrop({bgFile='Interface\\AchievementFrame\\UI-Achievement-Parchment-Horizontal',edgeFile='Interface\\DialogFrame\\UI-DialogBox-Border',tile=false,edgeSize=16,insets={left=7,right=7,top=7,bottom=7}})
 p:SetBackdropColor(.9,.80,.63,1);p:SetBackdropBorderColor(1,1,1,1)
 local band=p:CreateTexture(nil,'BORDER');band:SetTexture(.055,.049,.034,.95);band:SetPoint('TOPLEFT',8,-8);band:SetPoint('TOPRIGHT',-8,-8);band:SetHeight(28)
end
parchment(spellsPanel);parchment(talentsPanel)
local spellTitle=txt(spellsPanel,'Abilities',14,-13,340,'GameFontNormalLarge');local talentTitle=txt(talentsPanel,'Talents',14,-13,306,'GameFontNormalLarge')
local essenceIndicator=txt(spellsPanel,'',14,-36,340,'GameFontNormalSmall');local talentIndicator=txt(talentsPanel,'',14,-36,306,'GameFontNormalSmall')
local spellScroll,spellContent=scroll(spellsPanel,'HeroBuilderAbilities',10,-39,409,373)
local talentScroll,talentContent=scroll(talentsPanel,'HeroBuilderTalents',8,-39,292,373)
-- Keep the native scrollbar inside the panel, independent of viewport width.
local talentBar=_G['HeroBuilderTalentsScrollBar']
if talentBar then
 talentBar:ClearAllPoints()
 talentBar:SetPoint('TOPRIGHT',talentsPanel,'TOPRIGHT',-10,-55)
 talentBar:SetPoint('BOTTOMRIGHT',talentsPanel,'BOTTOMRIGHT',-10,37)
 talentBar:SetWidth(16)
end
local talentLock=CreateFrame('Frame',nil,talentsPanel)
talentLock:SetPoint('TOPLEFT',8,-8);talentLock:SetPoint('BOTTOMRIGHT',-8,8)
talentLock:SetFrameLevel(talentScroll:GetFrameLevel()+20);talentLock:EnableMouse(true)
local talentShade=talentLock:CreateTexture(nil,'BACKGROUND');talentShade:SetAllPoints(talentLock);talentShade:SetTexture(0,0,0,.68)
local talentLockText=talentLock:CreateFontString(nil,'OVERLAY','GameFontNormalLarge');talentLockText:SetPoint('CENTER',0,0);talentLockText:SetText('Unlocks at Level 10');talentLockText:SetTextColor(1,.2,.15)
talentLock:SetScript('OnEnter',function()GameTooltip:Hide()end)
A.TalentLockOverlay=talentLock

local architect=panel(f,25,-135,792,433);parchment(architect)
txt(architect,'Archetype Builder',16,-15,740,'GameFontNormalLarge');txt(architect,'All classes in your draft  -  grouped by reference level, not a validated learning order',16,-41,742,'GameFontHighlightSmall')
local archScroll,archContent=scroll(architect,'HeroBuilderArchitect',12,-70,744,348)
local pools={}
local function renderGroups(parent,entries,cols,width)
 local pool=pools[parent]or{buttons={},headers={}};pools[parent]=pool
 for _,b in ipairs(pool.buttons)do b:Hide()end;for _,t in ipairs(pool.headers)do t:Hide()end
 local y=0;local n=0;local step=cols==3 and 108 or 80
 for gi,g in ipairs(A.LevelGroups(entries))do
  local header=pool.headers[gi]or txt(parent,'',0,0,width,'GameFontNormal');pool.headers[gi]=header;header:ClearAllPoints();header:SetPoint('TOPLEFT',5,-y);header:SetText('Level '..g.level);header:SetTextColor(.23,.12,.045);header:Show();y=y+26
  for j,e in ipairs(g.entries)do
   n=n+1;local w=math.floor(width/cols);local b=pool.buttons[n]or entryButton(parent,w-5,step-2);pool.buttons[n]=b;b:ClearAllPoints();b:SetPoint('TOPLEFT',((j-1)%cols)*w,-y-math.floor((j-1)/cols)*step);fill(b,e,parent==archContent)
  end
  y=y+math.ceil(#g.entries/cols)*step+12
 end
 if #entries==0 then local t=pool.headers[1]or txt(parent,'',5,0,width-10);pool.headers[1]=t;t:ClearAllPoints();t:SetPoint('TOPLEFT',5,-10);t:SetText(parent==archContent and 'Your draft is empty. Select an ability or talent, then add a planned rank.' or 'No entries match these filters.');t:Show();y=70 end
 parent:SetHeight(math.max(1,y))
end
local nativeBackgrounds={["Mage:Arcane"]="MageArcane",["Warrior:Arms"]="WarriorArms",["Rogue:Assassination"]="RogueAssassination",["Priest:Discipline"]="PriestDiscipline",["Shaman:Elemental"]="ShamanElementalCombat",["Druid:Balance"]="DruidBalance",["Warlock:Affliction"]="WarlockCurses",["Hunter:BeastMastery"]="HunterBeastMastery",["Paladin:Holy"]="PaladinHoly",["DeathKnight:Blood"]="DeathKnightBlood",["Mage:Fire"]="MageFire",["Warrior:Fury"]="WarriorFury",["Rogue:Combat"]="RogueCombat",["Priest:Holy"]="PriestHoly",["Shaman:Enhancement"]="ShamanEnhancement",["Druid:FeralCombat"]="DruidFeralCombat",["Warlock:Demonology"]="WarlockSummoning",["Hunter:Marksmanship"]="HunterMarksmanship",["Paladin:Protection"]="PaladinProtection",["DeathKnight:Frost"]="DeathKnightFrost",["Mage:Frost"]="MageFrost",["Warrior:Protection"]="WarriorProtection",["Rogue:Subtlety"]="RogueSubtlety",["Priest:Shadow"]="PriestShadow",["Shaman:Restoration"]="ShamanRestoration",["Druid:Restoration"]="DruidRestoration",["Warlock:Destruction"]="WarlockDestruction",["Hunter:Survival"]="HunterSurvival",["Paladin:Retribution"]="PaladinCombat",["DeathKnight:Unholy"]="DeathKnightUnholy"}
local treePools={buttons={},headers={},lines={},arrows={}}
local treeBackgrounds={}
local talentArrowLayer=CreateFrame('Frame',nil,talentContent);talentArrowLayer:SetAllPoints(talentContent);talentArrowLayer:SetFrameLevel(talentContent:GetFrameLevel()+10);talentArrowLayer:EnableMouse(false)
local extras=CreateFrame('Frame',nil,talentContent);extras:SetSize(363,1)
local function renderTrees()
 local names=A.Specs();local activeSpec=A.spec=='All' and names[2]or A.spec
 A.talentPositions={}
 for _,set in pairs(treeBackgrounds)do for _,t in ipairs(set)do t:Hide()end end
 for _,b in ipairs(treePools.buttons)do b:Hide()end
 for _,h in ipairs(treePools.headers)do h:Hide()end
 for _,l in ipairs(treePools.lines)do l:Hide()end
 for _,l in ipairs(treePools.arrows)do l:Hide()end
 local allowed={};for _,e in ipairs(A.VisibleEntries('talent'))do allowed[e.id]=true end
 local used={};local groups={};local order={}
 for _,node in ipairs(HeroFreePickTrees)do
  if node.class==A.class and activeSpec==node.spec then
   if not groups[node.spec]then groups[node.spec]={};order[#order+1]=node.spec end
   groups[node.spec][#groups[node.spec]+1]=node
  end
 end
 local y=0;local count=0;local lineCount=0;local arrowCount=0
 for gi,spec in ipairs(order)do
  y=8
  local positions={};local maxRow=0
  for _,node in ipairs(groups[spec])do maxRow=math.max(maxRow,node.row)end
  local base=nativeBackgrounds[A.class..':'..spec]
  if base then
   local pieces=treeBackgrounds[gi]or {};treeBackgrounds[gi]=pieces
   local height=talentsPanel:GetHeight()-47;local artWidth=talentsPanel:GetWidth()-16
   for j,part in ipairs({'TopLeft','TopRight','BottomLeft','BottomRight'})do
    local t=pieces[j]or talentsPanel:CreateTexture(nil,'ARTWORK');pieces[j]=t
    local right=j==2 or j==4;local bottom=j>=3
    t:SetTexture('Interface\\TalentFrame\\'..base..'-'..part);t:ClearAllPoints();t:SetPoint('TOPLEFT',8+(right and artWidth*256/300 or 0),-39-(bottom and height*256/331 or 0));t:SetSize(artWidth*(right and 44 or 256)/300,height*(bottom and 75 or 256)/331);t:SetTexCoord(0,right and .6875 or 1,0,bottom and .5859375 or 1);t:SetDesaturated(A.OtherClass(A.class));t:Show()
   end
  end
  for _,node in ipairs(groups[spec])do
   count=count+1;local b=treePools.buttons[count]
   if not b then
    b=CreateFrame('Button','HeroNativeTalent'..count,talentContent,'TalentButtonTemplate');b:SetSize(32,32);b:RegisterForClicks('LeftButtonUp','RightButtonUp')
    b.icon=_G['HeroNativeTalent'..count..'IconTexture']or b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints(b)
    b.rank=_G['HeroNativeTalent'..count..'Rank']or txt(b,'',18,-24,28,'GameFontNormalSmall');b.rank:SetJustifyH('CENTER')
    local nativeRankBorder=_G['HeroNativeTalent'..count..'RankBorder'];if nativeRankBorder then nativeRankBorder:Hide()end
    local rankBox=CreateFrame('Frame',nil,b);rankBox:SetSize(30,17);rankBox:SetPoint('CENTER',b,'BOTTOMRIGHT',-2,0);rankBox:SetFrameLevel(b:GetFrameLevel()+1)
    rankBox:SetBackdrop({bgFile='Interface\\Tooltips\\UI-Tooltip-Background',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',edgeSize=7,insets={left=2,right=2,top=2,bottom=2}});rankBox:SetBackdropColor(0,0,0,1);rankBox:SetBackdropBorderColor(.7,.65,.35,1)
    b.rank:SetParent(rankBox);b.rank:ClearAllPoints();b.rank:SetPoint('CENTER',rankBox,'CENTER',0,0);b.rank:SetWidth(28);b.rank:SetHeight(14);treePools.buttons[count]=b
    b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip)
    b:SetScript('OnClick',function(self,mouse)A.AdjustPending(self.entry,mouse=='RightButton'and -1 or 1)end)
   end
   local e=A.byID[node.entries[1]]
   for _,id in ipairs(node.entries)do if allowed[id]then e=A.byID[id];break end end
   if e then used[e.id]=true else
    e={id=-node.talent,name=GetSpellInfo(node.ranks[1])or('Talent '..node.talent),class=node.class,spec=node.spec,spells=node.ranks,kind='Talent',quality='Normal',level=10+node.row*5,ae=0,te=1,requiredAE=0,requiredTE=0,requiredIDs='',unavailable=true}
   end
   b.entry=e;b.node=node;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e);local planned=A.PendingRank(e);b.rank:SetText(planned..'/'..A.MaxRank(e));b.rank:SetTextColor(planned>0 and 0 or 1,1,0);b:SetBackdropBorderColor(planned>0 and .3 or .8,planned>0 and 1 or .65,.25,1)
   local x=35+node.column*63;local ny=y+node.row*63;b:ClearAllPoints();b:SetPoint('TOPLEFT',x,-ny);b.icon:SetDesaturated(A.OtherClass(e.class));b:SetAlpha(not A.OtherClass(e.class)and allowed[e.id]and A.TalentsUnlocked()and 1 or .38);b:Show();positions[node.talent]={x=x+16,y=ny,rank=planned,button=b};A.talentPositions[e.id]=ny;maxRow=math.max(maxRow,node.row)
  end
  local highest=talentContent:GetFrameLevel()
  for _,button in ipairs(treePools.buttons)do highest=math.max(highest,button:GetFrameLevel()+2)end
  talentArrowLayer:SetFrameLevel(highest+1)
  local routeTextures={}
  A.NativeTalentRoutes(groups[spec],positions,function(arrow,uv,x,dy,target)
   local pool,index,owner
   if arrow then
    arrowCount=arrowCount+1;pool=treePools.arrows;index=arrowCount
    if not target.dependencyOverlay then
     target.dependencyOverlay=CreateFrame('Frame',nil,target)
     target.dependencyOverlay:SetAllPoints(target);target.dependencyOverlay:EnableMouse(false)
    end
    owner=target.dependencyOverlay
    owner:SetFrameStrata(target:GetFrameStrata());owner:SetFrameLevel(target:GetFrameLevel()+3)
   else lineCount=lineCount+1;pool=treePools.lines;index=lineCount;owner=talentContent end
   local t=pool[index]
   if not t then t=owner:CreateTexture(nil,arrow and 'OVERLAY' or 'BORDER');pool[index]=t elseif arrow then t:SetParent(owner)end
   t:SetDrawLayer(arrow and 'OVERLAY' or 'BORDER',arrow and 7 or 0)
   t:SetTexture(arrow and 'Interface\\TalentFrame\\UI-TalentArrows' or 'Interface\\TalentFrame\\UI-TalentBranches');t:SetTexCoord(unpack(uv));t:SetSize(32,32)
   t:ClearAllPoints();t:SetPoint('TOPLEFT',talentContent,'TOPLEFT',x-2,dy+2);t:SetVertexColor(1,1,1,1);t:Show()
   routeTextures[#routeTextures+1]={texture=t,arrow=arrow,uv=uv,x=x,y=dy,target=target}
  end)
  A.AlignTalentArrowTextures(routeTextures)
  y=y+maxRow*63+44
 end
 extras:Hide()
 talentContent:SetHeight(math.max(y,380))
end

local sideTabs={}
for i,label in ipairs({'Abilities','Specs','Loadouts'})do
 local tab=panel(side,10+(i-1)*101,-8,99,26);sideTabs[i]=tab;tab:SetBackdropColor(i==1 and .22 or .07,i==1 and .16 or .07,.04,1);local caption=txt(tab,label,3,-7,93,i==1 and 'GameFontNormalSmall' or 'GameFontDisableSmall');caption:SetJustifyH('CENTER')
end
local statTitle=txt(side,'Choose a Primary Stat',14,-40,292,'GameFontNormal');statTitle:SetJustifyH('CENTER')
-- Recovered from current Area 52 Spell.dbc; reference effects, not active server bonuses.
A.PrimaryStats={
["Strength"]={spell=84864,advancement=1149,summary="This primary stat focuses on dealing heavy hits and armor piercing attacks, and is especially beneficial for Plate armor users.\n\nGrants you bonus Strength, and each point of Strength now also increases your |cFFFFFFFFAttack Power|r and |cFFFFFFFFParry|r.",bonuses={
{name="Devastating Strikes",description="When wielding a One-Handed Weapon, your Armor Penetration is increased by 20%."},
{name="Heavy Swings",description="When wielding a Two-Handed weapon your melee and ranged physical abilities deal 10% more damage."},
}},
["Agility"]={spell=84865,advancement=1150,summary="This primary stat focuses on dealing rapid attacks and critical strikes, and is especially beneficial for Leather and Mail armor users.\n\nGrants you bonus Agility, and each point of Agility now also increases your |cFFFFFFFFAttack Power|r, |cFFFFFFFFCritical Strike Chance|r, and |cFFFFFFFFCritical Strike Damage|r.",bonuses={
{name="Agile Strikes",description="When wielding a One-Handed weapon, your damaging melee and ranged abilities global cooldown and cost is reduced by 8%."},
{name="Fatal Wounds",description="When wielding a Two-Handed weapon, your melee and ranged ability critical strike damage bonus is increased by 20%."},
}},
["Intellect"]={spell=84866,advancement=1151,summary="This primary stat focuses on empowering spell damage, increasing mana pool, and is especially beneficial for Cloth armor users.\n\nGrants you bonus |cFFFFFFFFSpell Power|r, Intellect, Spirit, and |cFFFFFFFFSpell Power|r gained from items and effects is doubled.",bonuses={
{name="Magic Acceleration",description="When wielding a Two-Handed weapon, your spell haste is increased by 12%."},
{name="Devastating Spells",description="When wielding a One-Handed weapon, your spell damage is increased by 5%."},
}},
["Spirit"]={spell=84867,advancement=1152,summary="Spirit enables you to fulfill the |cFFFFFFFFHealer Role|r. This primary stat increases your Healing Power and allows you to use unique powerful Healer spells.\n\nGrants you bonus |cFFFFFFFFHealing Power|r, |cFFFFFFFFIntellect|r, |cFFFFFFFFSpirit|r, and each point of |cFFFFFFFFSpell Power|r now also increases your |cFFFFFFFFHealing Power|r.",bonuses={
{name="Spiritual Acceleration",description="When wielding a Two-Handed weapon, your spell haste is increased by 10% and spell critical strike chance by 3%."},
{name="Empowered Mending",description="When wielding a One-Handed weapon, your healing is increased by 5%."},
}},
}
function A.PrimaryStatTooltip(owner)
 local d=A.PrimaryStats[owner.primaryStatKey];if not d then return end
 GameTooltip:SetOwner(owner,'ANCHOR_LEFT');GameTooltip:SetText('Primary Stat: '..owner.primaryStatKey)
 GameTooltip:AddLine(d.summary,1,.82,0,true)
 if IsShiftKeyDown() then
  GameTooltip:AddLine(' ')
  for _,effect in ipairs(d.bonuses)do
   GameTooltip:AddLine(effect.name,1,1,1,true)
   GameTooltip:AddLine(effect.description,1,.82,0,true);GameTooltip:AddLine(' ')
  end
  GameTooltip:AddLine('Source Spell ID: '..d.spell,.65,.65,.65)
  GameTooltip:AddLine('Character Advancement ID: '..d.advancement,.65,.65,.65)
 else GameTooltip:AddLine('Hold SHIFT for weapon bonuses.',0.2,.85,1,true)end
 GameTooltip:AddLine('Preview only: selection does not change character stats yet.',.65,.65,.65,true)
 GameTooltip:Show()
end

local statButtons={}
local statIcons={Strength='Spell_Nature_Strength',Agility='Interface\\AddOns\\HeroFreePick\\Art\\PrimaryStats\\ability_demonhunter_vengefulretreat2',Intellect='Spell_Arcane_MindMastery',Spirit='Spell_Holy_SealOfWisdom'}
for i,stat in ipairs({'Strength','Agility','Intellect','Spirit'})do
 local b=CreateFrame('Button',nil,side);b:SetSize(36,36);b:SetPoint('TOPLEFT',35+(i-1)*67,-60)
 b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints(b);b.icon:SetTexture(statIcons[stat]:find('Interface',1,true)and statIcons[stat]or('Interface\\Icons\\'..statIcons[stat]));b:SetBackdrop({edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',edgeSize=12});b:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square')
 b:SetScript('OnClick',function()if A.mode=='Classic'then A.ShowPointWarning('Classic primary stats use normal class progression.');return end;A.BeginPreparation();HeroFreePickPlans.primaryStat=stat;A.RefreshDetails()end)
 b.glow=b:CreateTexture(nil,'OVERLAY');b.glow:SetTexture('Interface\\Buttons\\UI-ActionButton-Border');b.glow:SetBlendMode('ADD');b.glow:SetVertexColor(1,.85,.1,1);b.glow:SetSize(64,64);b.glow:SetPoint('CENTER',b,'CENTER',0,0);b.glow:Hide()
 b.primaryStatKey=stat;b:SetScript('OnEnter',A.PrimaryStatTooltip);b:SetScript('OnLeave',function()GameTooltip:Hide()end);statButtons[stat]=b
end
local searchBox=panel(side,12,-100,192,25)
local learnedSearch=CreateFrame('EditBox',nil,searchBox);learnedSearch:SetFontObject(GameFontHighlightSmall);learnedSearch:SetSize(159,20);learnedSearch:SetPoint('LEFT',27,0);learnedSearch:SetAutoFocus(false)
local hint=txt(searchBox,'Search',27,-7,152,'GameFontDisableSmall')
-- Keep the magnifier in a scalable child frame; the editor controls its box.
local searchIcon=CreateFrame('Frame',nil,searchBox);searchIcon:SetSize(18,18)
searchIcon:SetPoint('LEFT',searchBox,'LEFT',6,0)
for y=0,11 do for x=0,11 do local d=(x-5.5)^2+(y-5.5)^2;if d>=17 and d<=29 then local t=searchIcon:CreateTexture(nil,'ARTWORK');t:SetTexture(.65,.65,.65,1);t:SetSize(1,1);t:SetPoint('TOPLEFT',x,-y)end end end
for i=0,4 do local t=searchIcon:CreateTexture(nil,'ARTWORK');t:SetTexture(.65,.65,.65,1);t:SetSize(2,2);t:SetPoint('TOPLEFT',9+i,-9-i)end
learnedSearch:SetScript('OnTextChanged',function(self)A.learnedQuery=self:GetText();A.query=A.learnedQuery;if A.learnedQuery==''then hint:Show()else hint:Hide()end;if A.Refresh then A.Refresh(true)end end)
A.ClearSearch=function()learnedSearch:SetText('')end
learnedSearch:SetScript('OnEscapePressed',function(self)self:ClearFocus()end)
local learnedFilter=CreateFrame('Frame',nil,side);learnedFilter:SetSize(104,25);learnedFilter:SetPoint('TOPLEFT',208,-100)
local filterMenu=CreateFrame('Frame','HeroBuilderLearnedFilterMenu',learnedFilter,'UIDropDownMenuTemplate')
filterMenu:SetPoint('TOPLEFT',-16,3);UIDropDownMenu_SetWidth(filterMenu,80);UIDropDownMenu_SetText(filterMenu,'Filter')
UIDropDownMenu_Initialize(filterMenu,function(self,level)
 level=level or 1
 local sections={{'Ability rarity','quality',{'All','Normal','Uncommon','Rare','Epic','Legendary'}},{'Plan selection','ownership',{'All','Planned','Not planned'}},{'Specialization','spec',A.Specs()},{'Pending selections','learnedFilter',{'All','Abilities','Talents',unpack(A.classes)}}}
 for _,section in ipairs(sections)do
  if level==1 then
   local info=UIDropDownMenu_CreateInfo();info.text=section[1];info.hasArrow=true;info.notCheckable=true;info.value=section[2];UIDropDownMenu_AddButton(info,level)
  elseif UIDROPDOWNMENU_MENU_VALUE==section[2]then
   for _,value in ipairs(section[3])do
    local key,choice=section[2],value;local info=UIDropDownMenu_CreateInfo();info.text=choice;info.checked=(A[key]or 'All')==choice
    info.func=function()A[key]=choice;UIDropDownMenu_SetText(filterMenu,choice=='All'and 'Filter'or choice);A.Refresh(true)end
    UIDropDownMenu_AddButton(info,level)
   end
  end
 end
 if level==1 then local info=UIDropDownMenu_CreateInfo();info.text='Reset filters';info.notCheckable=true
  info.func=function()A.quality='All';A.ownership='All';A.spec='All';A.learnedFilter='All';learnedSearch:SetText('');UIDropDownMenu_SetText(filterMenu,'Filter');A.Refresh(true)end
  UIDropDownMenu_AddButton(info,level)
 end
end)
local learnedScroll,learnedContent=scroll(side,'HeroBuilderLearned',12,-128,274,188)
local rarityRows={}
local rarityColors={Legendary={1,.5,0},Epic={.64,.21,.93},Rare={0,.44,.87},Uncommon={.12,1,0}}
for i,q in ipairs({'Legendary','Epic','Rare','Uncommon'})do
 local row=panel(side,10,-329-(i-1)*29,302,28);row.label=txt(row,q,8,-7,88,'GameFontNormalSmall');row.label:SetTextColor(unpack(rarityColors[q]));row.count=txt(row,'0',266,-7,34);row.gems={};rarityRows[q]=row
 row:EnableMouse(true);row:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_LEFT');GameTooltip:SetText(q..' slots used');GameTooltip:AddLine('Rarity slots used by local selections. Limits: 6 Legendary, 11 Epic, 12 Rare, 10 Uncommon.',1,1,1,true);GameTooltip:Show()end);row:SetScript('OnLeave',function()GameTooltip:Hide()end)
 for j=1,12 do
  local gem=CreateFrame('Frame',nil,row);gem:SetSize(12,18);gem:SetPoint('TOPLEFT',94+(j-1)*14,-5);gem.parts={}
  for y=0,15 do local width=math.max(1,10*(1-math.abs(y-7.5)/8));local t=gem:CreateTexture(nil,'ARTWORK');t:SetPoint('TOPLEFT',(12-width)/2,-y);t:SetSize(width,1);t:SetTexture(1,1,1,1);gem.parts[#gem.parts+1]=t end
  row.gems[j]=gem
 end
end
local rarityDivider=side:CreateTexture(nil,'OVERLAY');rarityDivider:SetTexture(.45,.42,.35,1);rarityDivider:SetPoint('TOPLEFT',10,-322);rarityDivider:SetSize(302,2)
local rarityToggle=btn(f,'Hide Rarities',838,-575,306,function()HeroFreePickPlans.hideRarities=not HeroFreePickPlans.hideRarities;A.Refresh()end)
local function refreshRarities()
 local hidden=HeroFreePickPlans.hideRarities
 rarityToggle:SetText(hidden and 'Show Rarities' or 'Hide Rarities')
 learnedScroll:SetHeight(hidden and 314 or 188)
 if hidden then rarityDivider:Hide()else rarityDivider:Show()end
 for _,row in pairs(rarityRows)do if hidden then row:Hide()else row:Show()end end
 local used={}
 for _,e in ipairs(A.LearnedEntries())do if not A.IsTalent(e)then used[e.quality]=(used[e.quality]or 0)+((HeroRarityCosts or {})[e.id]or 1)end end
 for q,row in pairs(rarityRows)do local count=used[q]or 0;row.count:SetText(count..'/'..A.RarityLimits[q]);for j,g in ipairs(row.gems)do
  if j<=A.RarityLimits[q]then g:Show()else g:Hide()end;g:SetAlpha(j<=count and 1 or .3);for y,t in ipairs(g.parts)do local c=j<=count and rarityColors[q]or {.3,.3,.3};local light=y<8 and 1 or .6;t:SetVertexColor(c[1]*light,c[2]*light,c[3]*light)end
 end end
end
local learnedPool={}
local spellMenu=CreateFrame('Frame','HeroBuilderSpellMenu',UIParent,'UIDropDownMenuTemplate')
local abilityPool={};local abilityHeaders={};A.iconPositions={}
local function renderAbilityIcons(entries)
 local columns=math.max(1,math.floor((spellScroll:GetWidth()-10)/40))
 for _,b in ipairs(abilityPool)do b:Hide()end
 A.iconPositions={}
 for _,h in ipairs(abilityHeaders)do h:Hide()end
 local currentLevel,y,column,headerCount=nil,5,0,0
 for i,e in ipairs(entries)do
  if currentLevel~=e.level then
   if currentLevel then y=y+math.ceil(column/columns)*40+3 end
   currentLevel=e.level;column=0;headerCount=headerCount+1
   local h=abilityHeaders[headerCount]or txt(spellContent,'',5,0,350,'GameFontNormal');abilityHeaders[headerCount]=h;h:ClearAllPoints();h:SetPoint('TOPLEFT',5,-y);h:SetText('Level '..currentLevel);h:SetTextColor(.23,.12,.045);h:Show();y=y+17
  end
  local b=abilityPool[i]
  if not b then
   b=CreateFrame('Button',nil,spellContent);b:SetSize(34,34);b:RegisterForClicks('LeftButtonUp','RightButtonUp')
   b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints(b)
   b:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square')
   b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip)
   b:SetScript('OnClick',function(self,mouse)A.AdjustPending(self.entry,mouse=='RightButton'and -1 or 1) end)
   abilityPool[i]=b
  end
  b.entry=e;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e);local locked=A.OtherClass(e.class) or UnitLevel('player')<(e.level or 1);b.icon:SetDesaturated(locked);b.icon:SetVertexColor(locked and .4 or 1,locked and .4 or 1,locked and .4 or 1);b:ClearAllPoints();local rowY=y+math.floor(column/columns)*40;b:SetPoint('TOPLEFT',5+(column%columns)*40,-rowY);b:Show();A.iconPositions[e.id]=rowY;column=column+1
 end
 spellContent:SetHeight(math.max(380,y+math.ceil(column/columns)*40+3))
end
function A.Locate(e)
 A.isBrowse=false;A.class=e.class;A.spec=e.spec;A.query='';A.quality='All';A.ownership='All';A.view='browse';search:SetText('');A.Refresh(true)
 local y=A.iconPositions[e.id]
 if y then spellScroll:SetVerticalScroll(math.min(math.max(0,y-10),spellScroll:GetVerticalScrollRange()))elseif A.talentPositions and A.talentPositions[e.id]then talentScroll:SetVerticalScroll(math.min(math.max(0,A.talentPositions[e.id]-10),talentScroll:GetVerticalScrollRange()))end
end
function A.FindRelated(e)
 -- Category relationship only; effect/proc relationships will be supplied later.
 A.Locate(e)
end
local function showSpellMenu(e)
 local menu={
  {text=e.name,isTitle=true,notCheckable=true},
  {text='Remove pending selection',notCheckable=true,func=function()A.SetLocalLearned(e.id,0);A.Refresh()end},
  {text='Locate',notCheckable=true,func=function()A.Locate(e)end},
  {text='Find Related',notCheckable=true,tooltipTitle='Related category',tooltipText='Show abilities from the same class and specialization. Effect relationships are not available yet.',tooltipOnButton=true,func=function()A.FindRelated(e)end},
  {text='Close',notCheckable=true,func=function()CloseDropDownMenus()end}}
 EasyMenu(menu,spellMenu,'cursor',0,0,'MENU')
end
function A.RefreshDetails()
 refreshRarities()
 for _,b in ipairs(learnedPool)do b:Hide()end
 for stat,b in pairs(statButtons)do local selected=HeroFreePickPlans.primaryStat==stat;b.icon:SetDesaturated(not selected);if selected then b.glow:Show()else b.glow:Hide()end;b:SetBackdropBorderColor(selected and 1 or .4,selected and .82 or .4,selected and .1 or .4,1)end
 UIDropDownMenu_SetText(filterMenu,A.learnedFilter and A.learnedFilter~='All' and A.learnedFilter or 'Filter')
 local visible=A.GroupLearnedEntries(A.FilteredLearnedEntries());local rowY=0
 for i,item in ipairs(visible)do
  local e=item.entry
  local b=learnedPool[i]
  if not b then
   b=CreateFrame('Button',nil,learnedContent);b:SetSize(272,46);b:RegisterForClicks('LeftButtonUp','RightButtonUp');b.learned=true;b:SetBackdrop({bgFile='Interface\\Tooltips\\UI-Tooltip-Background',edgeFile='Interface\\Tooltips\\UI-Tooltip-Border',edgeSize=8});b:SetBackdropColor(.02,.02,.02,1)
   b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetSize(34*.75,34*.75);b.icon:SetPoint('LEFT',4,0);b.name=txt(b,'',48,-7,154,'GameFontNormalSmall');b.name:SetHeight(31);b.cost=txt(b,'',203,-6,64);b.rarityCost=txt(b,'',203,-25,64);b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip)
   b:SetScript('OnClick',function(self,mouse)A.SetLocalLearned(self.entry.id,((HeroFreePickPlans.previewLearned or {})[self.entry.id]or 0)+(mouse=='RightButton'and -1 or 1));A.Refresh()end);learnedPool[i]=b
  end
  b.entry=e;b.groupedLearnedChild=item.child;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e);b.name:SetText(e.name)
  b.cost:SetText(rarityCost(e)..' '..(A.IsTalent(e)and talentCost(e.te)or essenceCost(e.ae)))
  b.rarityCost:Hide();b:ClearAllPoints()
  local indent=item.child and 18 or 0;local iconSize=34*.75*(item.child and .5 or 1)
  local width=math.max(1,learnedScroll:GetWidth()-2-indent)
  local height=math.max(16,iconSize)+4
  b:SetScale(1);b:SetSize(width,height);b.icon:SetSize(iconSize,iconSize)
  local costWidth=36+(A.IsTalent(e)and 0 or e.quality=='Normal'and 0 or((HeroRarityCosts or {})[e.id]or 1)*12)
  b.cost:ClearAllPoints();b.cost:SetPoint('RIGHT',-3,0);b.cost:SetWidth(costWidth);b.cost:SetHeight(16);b.cost:SetJustifyH('RIGHT')
  b.name:ClearAllPoints();b.name:SetPoint('LEFT',iconSize+8,0);b.name:SetWidth(math.max(1,width-iconSize-costWidth-14));b.name:SetHeight(16)
  b:SetPoint('TOPLEFT',learnedContent,'TOPLEFT',indent,-rowY);b:Show();rowY=rowY+height+3
 end
 learnedContent:SetHeight(math.max(learnedScroll:GetHeight(),rowY))
end
local pointsBox=panel(f,25,-573,265,30);local pointText=txt(pointsBox,'',9,-9,249,'GameFontNormalSmall')
pointsBox:EnableMouse(true);pointsBox:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_TOP');GameTooltip:SetText('Available Ability Points');GameTooltip:AddLine('9 points at levels 1-9, then 1 per level starting at 10. Selected ability costs are subtracted; unlearning refunds them. Local prototype balance.',1,1,1,true);GameTooltip:Show()end);pointsBox:SetScript('OnLeave',function()GameTooltip:Hide()end)
local talentsBox=panel(f,640,-573,177,30);local pointsTalentText=txt(talentsBox,'',8,-9,163,'GameFontNormalSmall')
talentsBox:EnableMouse(true);talentsBox:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_TOP');GameTooltip:SetText('Pending Talent Points');GameTooltip:AddLine('Remaining / total for your level. One point per level starting at level 10. Pending talent ranks use this budget; removing a rank returns its points.',1,1,1,true);GameTooltip:Show()end);talentsBox:SetScript('OnLeave',function()GameTooltip:Hide()end)
local function resetSelection(talents)
 A.BeginPreparation()
 for _,key in ipairs({'previewLearned','entries'})do
  for id in pairs(HeroFreePickPlans[key]or {})do local e=A.byID[id];if e and A.IsTalent(e)==talents then HeroFreePickPlans[key][id]=nil end end
 end
 A.Refresh()
end
local function resetButton(label,x,talents)
 local b
 b=btn(f,label,x,-575,167,function(self)
  if not self.confirmReset then self.confirmReset=true;self:SetText('Confirm reset');return end
  self.confirmReset=nil;self:SetText(label);resetSelection(talents)
 end)
 b:SetScript('OnLeave',function(self)self.confirmReset=nil;self:SetText(label);GameTooltip:Hide()end)
 b:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_TOP');GameTooltip:SetText(label);GameTooltip:AddLine(talents and 'Removes pending talent points. Cancel Changes restores your starting selections.' or 'Removes pending abilities and their costs. Cancel Changes restores your starting selections.',1,1,1,true);GameTooltip:Show()end)
 return b
end
local resetAbilitiesButton=resetButton('Reset All Abilities',297,false)
local resetTalentsButton=resetButton('Reset All Talents',468,true)
local allPanel=panel(f,25,-135,792,433);parchment(allPanel)
local allTitle=txt(allPanel,'Browse - All Abilities',14,-13,720,'GameFontNormalLarge')
local browseEssenceIndicator=txt(allPanel,'',14,-36,720,'GameFontNormalSmall')
local allScroll,allContent=scroll(allPanel,'HeroBuilderBrowseAll',10,-62,750,350)
local summarySort=CreateFrame('Frame','HeroBuilderSummarySort',allPanel,'UIDropDownMenuTemplate');summarySort:SetPoint('TOPRIGHT',-8,-9);UIDropDownMenu_SetWidth(summarySort,180)
UIDropDownMenu_Initialize(summarySort,function()
 for _,value in ipairs({'Class Origin','Level','Ability Point Cost','Rarity Cost'})do local choice=value;local info=UIDropDownMenu_CreateInfo();info.text=choice;info.checked=((HeroFreePickPlans and HeroFreePickPlans.summarySort)or 'Class Origin')==choice;info.func=function()A.Init();HeroFreePickPlans.summarySort=choice;A.Refresh(true)end;UIDropDownMenu_AddButton(info)end
end)
local summaryButtons,summaryHeaders={},{}
local function renderSummary()
 local sort=HeroFreePickPlans.summarySort or 'Class Origin';UIDropDownMenu_SetText(summarySort,sort)
 local groups,keys={},{}
 for _,e in ipairs(A.LearnedEntries())do
  local key=e.class
  if sort=='Level'then key=e.level or 1 elseif sort=='Ability Point Cost'then key=A.IsTalent(e)and 0 or(e.ae or 0) elseif sort=='Rarity Cost'then key=({Legendary=1,Epic=2,Rare=3,Uncommon=4,Normal=5,Common=5})[e.quality]or 5 end
  if not groups[key]then groups[key]={};keys[#keys+1]=key end;table.insert(groups[key],e)
 end
 table.sort(keys);local y,n=0,0
 for gi,key in ipairs(keys)do
  local label=tostring(key)
  if sort=='Level'then label='Level '..key elseif sort=='Ability Point Cost'then label='Ability Points: '..key elseif sort=='Rarity Cost'then label=({'Legendary','Epic','Rare','Uncommon','Common'})[key]end
  local h=summaryHeaders[gi]or txt(allContent,'',6,0,720,'GameFontNormal');summaryHeaders[gi]=h;h:SetText(label);h:SetTextColor(.23,.12,.045);h:ClearAllPoints();h:SetPoint('TOPLEFT',6,-y);h:Show();y=y+27
  table.sort(groups[key],function(x,y)if sort=='Rarity Cost'and (x.ae or 0)~=(y.ae or 0)then return (x.ae or 0)<(y.ae or 0)end;if x.name==y.name then return x.id<y.id end;return x.name<y.name end)
  for j,e in ipairs(groups[key])do
   n=n+1;local b=summaryButtons[n]
   if not b then b=CreateFrame('Button',nil,allContent);b:SetSize(34,34);b:RegisterForClicks('LeftButtonUp','RightButtonUp');b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints(b);b:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square');b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip);b:SetScript('OnClick',function(self,mouse)if mouse=='RightButton'then showSpellMenu(self.entry)end end);summaryButtons[n]=b end
   b.entry=e;b.learned=true;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e);b:ClearAllPoints();b:SetPoint('TOPLEFT',6+((j-1)%16)*45,-y-math.floor((j-1)/16)*42);b:Show()
  end
  y=y+math.ceil(#groups[key]/16)*42+15
 end
 allContent:SetHeight(math.max(1,y))
end

local allButtons,allHeaders={},{}
local browseEmpty=txt(allContent,'No abilities match your filters.',6,-6,710,'GameFontNormal');browseEmpty:Hide()
local function renderBrowse()
 browseEmpty:Hide()
 for _,b in ipairs(allButtons)do b:Hide()end;for _,h in ipairs(allHeaders)do h:Hide()end
 local grouped={};for _,c in ipairs(HeroBrowseCategories)do grouped[c.id]={}end
 for _,e in ipairs(HeroFreePickCatalog)do
  local planned=(HeroFreePickPlans.entries[e.id]or 0)>0
  if A.EntryAvailableInMode(e) and e.kind=='Ability' and (A.quality=='All' or e.quality==A.quality) and string.find(string.lower(e.name),string.lower(A.query or''),1,true)
   and (A.ownership=='All' or A.ownership=='Planned'and planned or A.ownership=='Not planned'and not planned)then
   for _,id in ipairs((HeroBrowseAssignment[e.id]or {categories={6}}).categories)do table.insert(grouped[id]or grouped[6],e)end
  end
 end
 local y,count=0,0
 for i,c in ipairs(HeroBrowseCategories)do
  local entries=grouped[c.id];table.sort(entries,function(a,b)local x=HeroBrowseAssignment[a.id];local y=HeroBrowseAssignment[b.id];if a.level~=b.level then return a.level<b.level end;if x.order~=y.order then return x.order<y.order end;if a.name==b.name then return a.id<b.id end;return a.name<b.name end)
  if #entries>0 then
  local h=allHeaders[i]
  if not h then h=CreateFrame('Button',nil,allContent);h:SetSize(720,28);h.label=txt(h,'',4,-4,710,'GameFontNormal');allHeaders[i]=h;h:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_RIGHT');GameTooltip:SetText(self.category.name);GameTooltip:AddLine(self.category.description,1,1,1,true);GameTooltip:AddLine('A52 category definitions and level order. Spell tooltips identify fallback assignments.',1,.8,.3,true);GameTooltip:Show()end);h:SetScript('OnLeave',function()GameTooltip:Hide()end)end
  h.category=c;h:ClearAllPoints();h:SetPoint('TOPLEFT',0,-y);h.label:SetText(c.name..' - Level '..c.referenceLevel..' ('..#entries..')');h.label:SetTextColor(.23,.12,.045);h:Show();y=y+32
  for j,e in ipairs(entries)do
   count=count+1;local b=allButtons[count]
   if not b then b=CreateFrame('Button',nil,allContent);b:SetSize(34,34);b:RegisterForClicks('LeftButtonUp','RightButtonUp');b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints(b);b:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square');b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip);b:SetScript('OnClick',function(self,mouse)A.AdjustPending(self.entry,mouse=='RightButton'and -1 or 1) end);allButtons[count]=b end
   if not rawget(b,'classBadge') then
    b.classBadge=b:CreateTexture(nil,'OVERLAY');b.classBadge:SetSize(16,16);b.classBadge:SetPoint('BOTTOMRIGHT',b,'BOTTOMRIGHT',4,-4)
    b.classRing=b:CreateTexture(nil,'OVERLAY',nil,1);b.classRing:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing');b.classRing:SetSize(20,20);b.classRing:SetPoint('CENTER',b.classBadge,'CENTER',0,0)
   end
   local classTexture='Interface\\Icons\\'..(badges[e.class]or'INV_Misc_QuestionMark')
   if SetPortraitToTexture then SetPortraitToTexture(b.classBadge,classTexture)else b.classBadge:SetTexture(classTexture)end
   b.entry=e;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e);b.icon:SetDesaturated(A.OtherClass(e.class) or UnitLevel('player')<(e.level or 1));b:ClearAllPoints();b:SetPoint('TOPLEFT',6+((j-1)%16)*45,-y-math.floor((j-1)/16)*42);b:Show()
  end
  y=y+math.ceil(#entries/16)*42+12
  end
 end
 if count==0 then browseEmpty:Show()end
 allContent:SetHeight(math.max(y,417))
end
function A.Refresh(resetScroll)
 title:SetText('Hero Advancement - '..A.Mode().name..(A.mode~='Classic'and ' (preview)'or ''))
 L.Apply()
 A.Init();summarySort:Hide();for _,b in ipairs(summaryButtons)do b:Hide()end;for _,h in ipairs(summaryHeaders)do h:Hide()end;A.kind='All';allPanel:Hide();allTitle:SetText(A.summary and 'Summary' or 'Browse - All Abilities')
 for _,b in ipairs(allButtons)do b:Hide()end;for _,h in ipairs(allHeaders)do h:Hide()end
 local previous=pools[allContent];if previous then for _,b in ipairs(previous.buttons)do b:Hide()end;for _,h in ipairs(previous.headers)do h:Hide()end end
 for key,d in pairs(dropdowns)do UIDropDownMenu_SetText(d,A[key])end
 for c,b in pairs(classButtons)do b:Enable();local other=c~='Browse' and A.OtherClass(c);b.portrait:SetDesaturated(other);b.portrait:SetAlpha(other and .4 or 1);local _,own;if UnitClass then _,own=UnitClass('player')end;if (own and own~='HERO' and string.upper(c)==own)or((not own or own=='HERO')and ((A.isBrowse and c=='Browse')or(not A.isBrowse and c==A.class)))then for _,g in ipairs(b.glows)do g:Show()end;b.ring:SetVertexColor(1,.82,.25);b.label:SetTextColor(1,.9,.4)else for _,g in ipairs(b.glows)do g:Hide()end;b.ring:SetVertexColor(.7,.7,.67);b.label:SetTextColor(other and .4 or .8,other and .4 or .7,other and .4 or .42)end end
 if A.TalentsUnlocked()then talentLock:Hide()else talentLock:Show()end
 local names=A.Specs();for i,b in ipairs(specs)do
 local name=i==4 and 'Summary' or names[i+1]
 if name then b:SetText(name=='BeastMastery' and 'Beast Mastery' or name=='FeralCombat' and 'Feral Combat' or name);b:Show();local selected=(i==4 and A.summary)or(not A.summary and not A.isBrowse and (A.spec==name or(A.spec=='All' and i==1)))
 for _,t in ipairs(b.tabPieces)do t:SetTexture(selected and 'Interface\\PaperDollInfoFrame\\UI-Character-ActiveTab' or 'Interface\\PaperDollInfoFrame\\UI-Character-InActiveTab')end;if selected then b.bridge:Show();b.caption:SetTextColor(1,.9,.4)else b.bridge:Hide();b.caption:SetTextColor(.8,.7,.42)end;b:Enable()
 setBadge(b.spentBadge,i==4 and spent()or spent(A.class,name))
 else b:Hide()end end
 for class,b in pairs(classButtons)do setBadge(b.spentBadge,spent(class~='Browse' and class or nil))end
 essenceIndicator:Hide();browseEssenceIndicator:Hide();talentIndicator:Hide();pointText:SetText('Ability Points: '..essenceCost(A.AvailableAbilityPoints(A.view=='architect' and 'entries' or 'previewLearned')));pointsTalentText:SetText('Talent Points: '..talentCost(math.max(0,A.AvailableTalentPoints()))..'/'..A.TalentPointAllowance())
 if A.view=='architect'then toolbar:Hide();spellsPanel:Hide();talentsPanel:Hide();architect:Show();PanelTemplates_DeselectTab(browseTab);PanelTemplates_SelectTab(architectTab);renderGroups(archContent,A.PlannedEntries(),2,744);mode:SetText('Archetype Builder - local draft')
 elseif A.summary then toolbar:Hide();spellsPanel:Hide();talentsPanel:Hide();architect:Hide();allPanel:Show();summarySort:Show();renderSummary()
 elseif A.isBrowse then toolbar:Hide();spellsPanel:Hide();talentsPanel:Hide();architect:Hide();allPanel:Show();PanelTemplates_SelectTab(browseTab);PanelTemplates_DeselectTab(architectTab);mode:SetText('Browse - All Abilities');renderBrowse()
 else toolbar:Hide();spellsPanel:Show();talentsPanel:Show();architect:Hide();PanelTemplates_SelectTab(browseTab);PanelTemplates_DeselectTab(architectTab);local abilities=A.VisibleEntries('ability');local talents=A.VisibleEntries('talent');spellTitle:SetText('Abilities');talentTitle:SetText('Talents');renderAbilityIcons(abilities);renderTrees();mode:SetText(A.class..'  -  '..A.spec)end
 if resetScroll then allScroll:SetVerticalScroll(0);spellScroll:SetVerticalScroll(0);talentScroll:SetVerticalScroll(0);learnedScroll:SetVerticalScroll(0);archScroll:SetVerticalScroll(0)end
 disableArchitectTab()
 A.RefreshDetails()
 L.Apply()
end
L.AfterApply=function()
 local iconScale=math.max(.1,math.min(1,(searchBox:GetHeight()-6)/18,(searchBox:GetWidth()-12)/18))
 searchIcon:SetScale(iconScale)
 local inset=6+18*iconScale+5
 learnedSearch:ClearAllPoints();learnedSearch:SetPoint('LEFT',searchBox,'LEFT',inset,0)
 learnedSearch:SetSize(math.max(1,searchBox:GetWidth()-inset-6),math.max(1,searchBox:GetHeight()-4))
 hint:ClearAllPoints();hint:SetPoint('LEFT',searchBox,'LEFT',inset,0);hint:SetWidth(math.max(1,searchBox:GetWidth()-inset-6))
 UIDropDownMenu_SetWidth(filterMenu,math.max(20,learnedFilter:GetWidth()-24))
 for _,entry in ipairs({{browseTab,'HeroBuilderDevelopmentTab','bottomHero'},{architectTab,'HeroBuilderArchetypeTab','bottomBuilder'}})do
  local tab,name,id=unpack(entry)
  local text=_G[name..'Text']
  if text then text:ClearAllPoints();text:SetPoint('CENTER',tab,'CENTER',0,2);text:SetJustifyH('CENTER')end
  if L.overrides[id]then
   for _,suffix in ipairs({'Middle','MiddleDisabled'})do
    local texture=_G[name..suffix];if texture then texture:SetWidth(math.max(1,tab:GetWidth()-40))end
   end
  end
 end
 spellContent:SetWidth(spellScroll:GetWidth());talentContent:SetWidth(talentScroll:GetWidth());learnedContent:SetWidth(learnedScroll:GetWidth())
 for i,b in ipairs(specs)do if L.overrides['spec'..i]then
  local width=b:GetWidth()
  for j,t in ipairs(b.tabPieces)do t:SetWidth(j==2 and math.max(1,width-40)or 20);t:ClearAllPoints();t:SetPoint('TOPLEFT',j==1 and 0 or(j==2 and 20 or width-20),0)end
  b.caption:SetWidth(math.max(1,width-8))
 end end
end
L.Bind('window',f)
L.Bind('header',header)
L.Bind('close',closeBox)
L.Bind('info',infoBox)
L.Bind('abilities',spellsPanel)
L.Bind('talents',talentsPanel)
L.Bind('side',side)
L.Bind('abilitiesTitle',spellTitle)
L.Bind('talentsTitle',talentTitle)
L.Bind('abilitiesScroll',spellScroll)
L.Bind('talentsScroll',talentScroll)
L.Bind('talentsBar',talentBar)
L.Bind('learnedScroll',learnedScroll)
L.Bind('primaryTitle',statTitle)
L.Bind('searchBox',searchBox)
L.Bind('filter',learnedFilter)
L.Bind('points',pointsBox)
L.Bind('talentPoints',talentsBox)
L.Bind('rarityToggle',rarityToggle)
L.Bind('resetAbilities',resetAbilitiesButton)
L.Bind('resetTalents',resetTalentsButton)
L.Bind('bottomHero',browseTab)
L.Bind('bottomBuilder',architectTab)
L.Bind('spec1',specs[1])
L.Bind('spec2',specs[2])
L.Bind('spec3',specs[3])
L.Bind('spec4',specs[4])
L.Bind('sideTab1',sideTabs[1])
L.Bind('sideTab2',sideTabs[2])
L.Bind('sideTab3',sideTabs[3])
L.Bind('statStrength',statButtons['Strength'])
L.Bind('statAgility',statButtons['Agility'])
L.Bind('statIntellect',statButtons['Intellect'])
L.Bind('statSpirit',statButtons['Spirit'])
L.Bind('rarityLegendary',rarityRows['Legendary'])
L.Bind('rarityEpic',rarityRows['Epic'])
L.Bind('rarityRare',rarityRows['Rare'])
L.Bind('rarityUncommon',rarityRows['Uncommon'])
L.Apply()
-- Include the protruding tabs in the fitted footprint; never reuse an off-screen drag position on open.
-- Prefer native effective scale; compensate for the client's global UI scale.
-- Only use fractional scaling when the complete window cannot fit.
function A.WindowScale(width,height,parentScale)
 return math.min(1/parentScale,(width-48/parentScale)/1192,(height-64/parentScale)/652)
end
function A.FitWindow()
 L.Apply()
 local parentScale=UIParent:GetEffectiveScale()or 1
 local scale=math.min(1/parentScale,(UIParent:GetWidth()-48/parentScale)/(f:GetWidth()+12),(UIParent:GetHeight()-64/parentScale)/(f:GetHeight()+32))
 f:SetScale(scale);f:ClearAllPoints();f:SetPoint('TOP',UIParent,'TOP',0,-32/(scale*parentScale))
 f:SetClampedToScreen(true);f:SetClampRectInsets(0,0,0,-32)
end
f:RegisterEvent('DISPLAY_SIZE_CHANGED');f:RegisterEvent('UI_SCALE_CHANGED');f:RegisterEvent('CHARACTER_POINTS_CHANGED');f:RegisterEvent('PLAYER_TALENT_UPDATE');f:RegisterEvent('PLAYER_LEVEL_UP');f:RegisterEvent('MODIFIER_STATE_CHANGED')
f:SetScript('OnEvent',function(self,event)if event=='MODIFIER_STATE_CHANGED' then if A.RefreshMasteryTooltip()then return end;local owner=GameTooltip:GetOwner();if owner and rawget(owner,'primaryStatKey') then A.PrimaryStatTooltip(owner)elseif owner and owner.entry then tooltip(owner)end;return end;if f:IsShown()then A.FitWindow();A.Refresh()end end)
SLASH_HEROFREEPICK1='/heropick'
function A.Toggle()if f:IsShown()then A.RequestClose()else A.BeginPreparation();A.Refresh(true);A.FitWindow();f:Show();if A.ShowModeChoice then A.ShowModeChoice()end end end

SlashCmdList.HEROFREEPICK=A.Toggle

-- Preparation support is embedded for clients with a cached addon file list.
do
local A=HeroFreePick
local window=HeroFreePickFrame
local dialog=CreateFrame('Frame','HeroPendingChangesDialog',UIParent)
A.PendingDialog=dialog
-- Full-window mouse shield keeps the review modal while preserving the pending menu.
dialog:SetAllPoints(UIParent);dialog:SetFrameStrata('FULLSCREEN_DIALOG');dialog:SetFrameLevel(40);dialog:EnableMouse(true)
local box=CreateFrame('Frame',nil,dialog);box:SetFrameLevel(41);box:SetSize(650,440);box:SetPoint('CENTER');box:EnableMouse(true)
box:SetBackdrop({bgFile='Interface\\DialogFrame\\UI-DialogBox-Background',edgeFile='Interface\\DialogFrame\\UI-DialogBox-Border',tile=true,tileSize=32,edgeSize=32,insets={left=11,right=11,top=11,bottom=11}})
local title=box:CreateFontString(nil,'OVERLAY','GameFontNormalLarge');title:SetPoint('TOP',0,-24);title:SetText('Pending Hero Advancement Changes')
local body=box:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');body:SetPoint('TOPLEFT',26,-58);body:SetSize(598,295);body:SetJustifyH('LEFT');body:SetJustifyV('TOP')
local message=box:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');message:SetPoint('BOTTOMLEFT',26,65);message:SetSize(598,38);message:SetTextColor(1,.65,.2);message:SetJustifyH('LEFT')
local function button(text,x,fn)
 local b=CreateFrame('Button',nil,box,'UIPanelButtonTemplate');b:SetSize(185,26);b:SetPoint('BOTTOMLEFT',x,26);b:SetText(text);b:SetScript('OnClick',fn);return b
end
local closing=false
function A.HidePreparationPreservingChanges()
 closing=true;dialog:Hide()
 if HeroProgressionChoice then HeroProgressionChoice:Hide()end
 window:Hide();closing=false
end
local dismiss=CreateFrame('Button',nil,box,'UIPanelCloseButton');dismiss:SetPoint('TOPRIGHT',-6,-6);dismiss:SetScript('OnClick',A.HidePreparationPreservingChanges)
local closeForNow=CreateFrame('Button',nil,box,'UIPanelButtonTemplate');closeForNow:SetSize(150,22);closeForNow:SetPoint('BOTTOM',0,0);closeForNow:SetText('Close for now');closeForNow:SetScript('OnClick',A.HidePreparationPreservingChanges)
local function finish()
 closing=true;dialog:Hide();window:Hide();closing=false
end
function A.ShowPendingReview()
 if A.classicCommit then dialog:Show();return end
 local lines={'Review the proposed resources below. No changes have been learned.',''}
 for _,section in ipairs(A.PendingSummary())do
  lines[#lines+1]=(section.key=='entries'and 'Archetype draft'or 'Hero Advancement')..': +'..section.added..' / -'..section.removed..' ranks'
  for _,q in ipairs({'AP','TP','Uncommon','Rare','Epic','Legendary'})do
   local before=section.before[q];local after=section.after[q];local delta=after-before
   lines[#lines+1]=(q=='AP'and 'Ability Points'or q=='TP'and 'Talent Points'or q)..': '..before..' -> '..after..' ('..(delta>=0 and '+'or '')..delta..')'
  end
  lines[#lines+1]=''
 end
 local base=HeroFreePickPlans.pendingBaseline
 if base and base.primaryStat~=HeroFreePickPlans.primaryStat then lines[#lines+1]='Primary stat: '..tostring(base.primaryStat or 'None')..' -> '..tostring(HeroFreePickPlans.primaryStat or 'None')end
 body:SetText(table.concat(lines,'\n'))
 message:SetText(A.mode=='Classic'and 'Accept learns new talent ranks using the stock server. Confirmed ranks require a trainer to reset.'or 'Preview only. Custom-mode server committing is not available yet.')
 dialog:Show()
end
function A.RequestClose()
 if A.classicCommit then A.ShowPendingReview();return false end
 if A.HasPendingChanges()then A.ShowPendingReview();return false end
 if HeroFreePickPlans then HeroFreePickPlans.pendingBaseline=nil end
 finish();return true
end
A.PendingAcceptButton=button('Accept Changes',27,function()
 local ok,reason=A.AcceptPreparation()
 if A.classicCommit then A.PendingAcceptButton:Disable();A.PendingBackButton:Disable();A.PendingCancelButton:Disable()end
 if ok then finish()else message:SetText(reason)end
end)
A.PendingBackButton=button('Go Back',232,function()if A.classicCommit then return end;dialog:Hide();window:Show()end)
A.PendingCancelButton=button('Cancel Changes',437,function()if A.classicCommit then return end;A.CancelPreparation();A.Refresh();finish()end)
if HeroFreePickFrameClose then HeroFreePickFrameClose:SetScript('OnClick',A.RequestClose)end
-- Escape and inherited close actions use Hide directly; intercept them as well.
window:SetScript('OnHide',function()
 if closing then return end
 if A.HasPendingChanges()then window:Show();A.ShowPendingReview()
 elseif HeroFreePickPlans then HeroFreePickPlans.pendingBaseline=nil end
end)
A.ClassicCommitResult=function(ok,reason)
 A.PendingAcceptButton:Enable();A.PendingBackButton:Enable();A.PendingCancelButton:Enable();message:SetText(reason)
 A.Refresh();if ok then finish()end
end
local poll=CreateFrame('Frame','HeroClassicCommitPoller');A.ClassicCommitPoller=poll
poll:SetScript('OnUpdate',function(_,elapsed)A.PollClassicCommit(elapsed)end)
dialog:Hide()

end

do
local A=HeroFreePick
local shield=CreateFrame('Frame','HeroProgressionChoice',UIParent);shield:SetAllPoints(UIParent);shield:SetFrameStrata('FULLSCREEN_DIALOG');shield:SetFrameLevel(60);shield:EnableMouse(true)
local box=CreateFrame('Frame',nil,shield);box:SetFrameLevel(61);box:SetSize(590,370);box:SetPoint('CENTER');box:SetBackdrop({bgFile='Interface\\DialogFrame\\UI-DialogBox-Background',edgeFile='Interface\\DialogFrame\\UI-DialogBox-Border',tile=true,tileSize=32,edgeSize=32});box:EnableMouse(true)
local title=box:CreateFontString(nil,'OVERLAY','GameFontNormalLarge');title:SetPoint('TOP',0,-24)
local note=box:CreateFontString(nil,'OVERLAY','GameFontHighlight');note:SetPoint('TOPLEFT',24,-55);note:SetSize(542,65);note:SetJustifyH('LEFT')
local closeChoice=CreateFrame('Button',nil,box,'UIPanelCloseButton');closeChoice:SetPoint('TOPRIGHT',-6,-6);closeChoice:SetScript('OnClick',A.HidePreparationPreservingChanges)
local buttons={};A.ProgressionChoiceButtons=buttons
local function clear()for _,b in ipairs(buttons)do b:Hide()end end
local function choice(label,index,description,fn)
 local b=buttons[index]
 if not b then b=CreateFrame('Button',nil,box,'UIPanelButtonTemplate');b:SetSize(255,30);buttons[index]=b end
 b:SetFrameStrata('FULLSCREEN_DIALOG');b:SetFrameLevel(62);b:EnableMouse(true);b:Enable();b:ClearAllPoints();b:SetPoint('TOPLEFT',25+((index-1)%2)*280,-125-math.floor((index-1)/2)*40);b:SetText(label)
 b:SetScript('OnClick',fn);b:SetScript('OnEnter',function(self)GameTooltip:SetOwner(self,'ANCHOR_RIGHT');GameTooltip:SetText(label);GameTooltip:AddLine(description,1,1,1,true);GameTooltip:Show()end);b:SetScript('OnLeave',function()GameTooltip:Hide()end);b:Show()
end
local function finish(ok,why)
 if not ok then note:SetText(why);return end
 shield:Hide();A.Refresh(true)
end
local function secondClass()
 clear();title:SetText('Choose your second class');note:SetText('Your original class remains available. Choose one additional class for Hybrid. Custom modes are currently local previews.')
 local _,own=UnitClass('player');local i=0
 for _,c in ipairs(A.classes)do if string.upper(c)~=own then local selected=c;i=i+1;choice(c,i,'Unlock abilities and talents from '..c..' alongside your original class.',function()finish(A.ChooseHybridPath(selected))end)end end
end
function A.ShowModeChoice(level)
 local due=A.ModeChoiceDue(level);if not due then shield:Hide();return end
 clear();shield:Show()
 if due=='initial'then
  title:SetText('Choose your progression');note:SetText('Choose how this character will progress. Classic uses the stock server. Installed custom modes are local previews until server integration is complete.')
  choice('Classic Character',1,'Learn abilities from trainers. Preview talents here; committed talents require a trainer reset.',function()finish(A.ChooseInitialMode('Classic'))end)
  if A.InstalledModes.ClassPlus or A.InstalledModes.Hybrid then choice('Class+',2,A.ClassPlusChoiceTooltip(),function()finish(A.ChooseInitialMode('ClassPlus'))end)end
  if A.InstalledModes.Hero then choice('Hero',3,'Full free-pick preparation across all classes within resource limits.',function()finish(A.ChooseInitialMode('Hero'))end)end
 else
  title:SetText('Continue as Class+ or become Hybrid');note:SetText('You have reached level 10. Continue with your original class, or choose a second class. This one-time choice is saved locally until server integration is available.')
  choice('Continue as Class+',1,'Keep your original class only.',function()finish(A.ChooseHybridPath(nil))end)
  choice('Become Hybrid',2,'Choose one additional class. Both classes share your point and rarity budgets.',secondClass)
 end
end
shield:Hide()
local events=CreateFrame('Frame');events:RegisterEvent('PLAYER_LOGIN');events:RegisterEvent('PLAYER_LEVEL_UP')
events:SetScript('OnEvent',function(_,event,level)
 A.Init()
 if event=='PLAYER_LOGIN'then
  local saved=HeroFreePickPlans.progressionChoice
  if saved then
   local available=saved.mode=='Classic'or A.InstalledModes[saved.mode]or(saved.mode=='ClassPlus'and A.InstalledModes.Hybrid)
   if available then A.mode=saved.mode;A.secondClass=saved.secondClass end
  end
 end
 A.ShowModeChoice(event=='PLAYER_LEVEL_UP'and tonumber(level)or nil)
end)
end
