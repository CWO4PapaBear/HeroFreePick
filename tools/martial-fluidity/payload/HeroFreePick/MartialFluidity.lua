-- Server-authoritative custom-mode Vigor presentation and shared combo display.
local A=HeroFreePick
local spell=14983
local function custom()return A.mode=='Class+'or A.mode=='ClassPlus'or A.mode=='Hybrid'or A.mode=='Hero'end
local function talent(e)
 if not e or not e.spells then return false end
 for _,id in ipairs(e.spells)do if id==spell then return true end end
 return false
end
function A.DisplayTalentName(e)
 if custom()and talent(e)then return 'Martial Fluidity'end
 return e and e.name
end
local description='Combo points are retained even when switching targets.\n\nIncreases your maximum energy by 10.'
local originalDescription=A.AscensionTalentDescription
function A.AscensionTalentDescription(e,rank)
 if custom()and talent(e)then return description,{serverDefinition=true,unresolved={}}end
 if originalDescription then return originalDescription(e,rank)end
end
local originalNotes=A.AddAscensionTalentNotes
function A.AddAscensionTalentNotes(e,rank)
 if custom()and talent(e)then return end
 if originalNotes then return originalNotes(e,rank)end
end
local originalCombo=GetComboPoints
local shared,points=false,0
function A.HasSharedComboPoints()return custom()and shared end
function GetComboPoints(unit,target)
 if unit=='player'and A.HasSharedComboPoints()then return points end
 return originalCombo(unit,target)
end
-- Keep both displays, but never leave target points floating without a target.
local function hideSharedTargetPoints()
 if A.HasSharedComboPoints()and ComboFrame and not UnitExists('target')and(not PlayerFrame or PlayerFrame.unit=='player')then
  ComboFrame:Hide()
 end
end
if ComboFrame then ComboFrame:HookScript('OnShow',hideSharedTargetPoints)end
if ComboFrame_Update then hooksecurefunc('ComboFrame_Update',hideSharedTargetPoints)end
local function receive(message)
 if type(message)~='string'then return false end
 local enabled,count=message:match('^HF_COMBO ([01]) (%d+)$')
 count=tonumber(count)
 if not enabled or not count or count>5 then return false end
 local wasShared=A.HasSharedComboPoints()
 shared=enabled=='1';points=shared and count or 0
 hideSharedTargetPoints()
 if wasShared and not A.HasSharedComboPoints()and ComboFrame_Update then ComboFrame_Update()end
 return true
end
local events=CreateFrame('Frame')
events:RegisterEvent('CHAT_MSG_SYSTEM')
events:RegisterEvent('PLAYER_ENTERING_WORLD')
events:RegisterEvent('PLAYER_DEAD')
events:SetScript('OnEvent',function(_,event,message)
 if event=='CHAT_MSG_SYSTEM'then receive(message)
 elseif event=='PLAYER_DEAD'then points=0 end
 -- Do not clear on zoning: server state is refreshed every two seconds.
end)
ChatFrame_AddMessageEventFilter('CHAT_MSG_SYSTEM',function(_,_,message)return receive(message)end)
-- Match the spell's native tooltip as well as the advancement card; Classic stays stock.
local replacing=false
GameTooltip:HookScript('OnTooltipSetSpell',function(self)
 if replacing or not custom()then return end
 local _,id=self:GetSpell();if id~=spell then return end
 replacing=true
 self:ClearLines();self:SetText('Martial Fluidity');self:AddLine(description,1,1,1,true)
 replacing=false
end)
