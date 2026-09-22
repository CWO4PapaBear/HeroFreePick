local A=HeroFreePick
local tabs,active,dirty={},false,true
local nativeInfo,nativeSlot=SpellBook_GetTabInfo,SpellBook_GetSpellID
local tabPage=0
local function enabled()return A and (A.mode=='Hybrid'or A.mode=='Hero')end
local function custom()return active and enabled()and SpellBookFrame.bookType==BOOKTYPE_SPELL end
local function rebuild()
 local old=tabs[SpellBookFrame.selectedSkillLine or 1];local oldKey=old and old.key;local oldPage=SPELLBOOK_PAGENUMBERS[SpellBookFrame.selectedSkillLine or 1]or 1
 tabs={{key='general',name=GENERAL or 'General',icon='Interface\\Icons\\INV_Misc_Book_09',slots={}}}
 local buckets,highest={},{}
 if not GetCVarBool('ShowAllSpellRanks')then
  for i=1,GetNumSpellTabs()do local _,_,_,_,offset,count=GetSpellTabInfo(i)
   for j=1,count or 0 do highest[GetKnownSlotFromHighestRankSlot(offset+j)]=true end
  end
 end
 local imported={}
 for _,e in pairs(A.byID or {})do
  for skill,t in pairs(HeroSpellbookTrees)do if t.class==e.class and t.name==e.spec then
   for _,id in ipairs(e.spells or {})do imported[id]=skill end
  end end
 end
 for i=1,GetNumSpellTabs()do
  local _,_,offset,count=GetSpellTabInfo(i)
  for slot=offset+1,offset+count do
   if GetCVarBool('ShowAllSpellRanks')or highest[slot]then
    local link=GetSpellLink(slot,BOOKTYPE_SPELL);local id=link and tonumber(link:match('spell:(%d+)'))
    local skill=id and (HeroSpellbookSpellTrees[id]or imported[id]);local tree=skill and HeroSpellbookTrees[skill]
    local bucket=tabs[1]
    if tree then
     if not buckets[skill]then buckets[skill]={key=tostring(skill),class=tree.class,name=tree.class..' - '..tree.name,icon=tree.icon or 'Interface\\Icons\\INV_Misc_Book_09',slots={}}end
     bucket=buckets[skill]
    end
    table.insert(bucket.slots,slot)
   end
  end
 end
 local sorted={};for _,v in pairs(buckets)do sorted[#sorted+1]=v end
 table.sort(sorted,function(a,b)return a.name<b.name end)
 for _,t in ipairs(sorted)do tabs[#tabs+1]=t end
 local selected=1
 for i,t in ipairs(tabs)do SPELLBOOK_PAGENUMBERS[i]=1;if t.key==oldKey then selected=i;SPELLBOOK_PAGENUMBERS[i]=math.max(1,math.min(oldPage,math.ceil(#t.slots/SPELLS_PER_PAGE)))end end
 SpellBookFrame.selectedSkillLine=selected;tabPage=math.min(tabPage,math.floor((#tabs-1)/8))
 active=true;dirty=false
end
function SpellBook_GetTabInfo(i)
 if not custom()then return nativeInfo(i)end
 local t=tabs[i]or tabs[1];return t.name,t.icon,0,#t.slots
end
function SpellBook_GetSpellID(button)
 if not custom()then return nativeSlot(button)end
 local index=SpellBookFrame.selectedSkillLine or 1;local t=tabs[index]or tabs[1]
 local pos=button+SPELLS_PER_PAGE*((SPELLBOOK_PAGENUMBERS[index]or 1)-1)
 return t.slots[pos]or MAX_SPELLS+1,pos
end
local pager=CreateFrame('Frame','HeroSpellbookTabPager',SpellBookFrame)
pager:SetSize(120,44);pager:SetPoint('TOPLEFT',SpellBookSkillLineTab8,'BOTTOMLEFT',0,-4);pager:Hide()
local pageText=pager:CreateFontString(nil,'OVERLAY','GameFontNormalSmall')
pageText:SetPoint('TOPLEFT',pager,'TOPLEFT',0,0)
local prevTabs=CreateFrame('Button','HeroSpellbookPreviousTabs',pager,'UIPanelButtonTemplate')
prevTabs:SetSize(56,22);prevTabs:SetPoint('TOPLEFT',pager,'TOPLEFT',0,-17);prevTabs:SetText('< Prev')
local nextTabs=CreateFrame('Button','HeroSpellbookNextTabs',pager,'UIPanelButtonTemplate')
nextTabs:SetSize(56,22);nextTabs:SetPoint('LEFT',prevTabs,'RIGHT',4,0);nextTabs:SetText('Next >')
local function buttons()
 if not custom()then pager:Hide();return end
 for i=1,8 do
  local button=_G['SpellBookSkillLineTab'..i];local index=tabPage*8+i;local t=tabs[index]
  if t then button:SetNormalTexture(t.icon);button.tooltip=t.name;button:SetChecked(SpellBookFrame.selectedSkillLine==index);button:Show()else button:Hide()end
 end
 if #tabs>8 then
  pager:Show();pageText:SetText('Trees '..(tabPage+1)..' / '..math.ceil(#tabs/8))
  if tabPage>0 then prevTabs:Enable()else prevTabs:Disable()end
  if (tabPage+1)*8<#tabs then nextTabs:Enable()else nextTabs:Disable()end
 else pager:Hide()end
 ShowAllSpellRanksCheckBox:Show()
end
prevTabs:SetScript('OnClick',function()tabPage=math.max(0,tabPage-1);buttons()end)
nextTabs:SetScript('OnClick',function()tabPage=math.min(math.ceil(#tabs/8)-1,tabPage+1);buttons()end)
for i=1,8 do
 local button=_G['SpellBookSkillLineTab'..i];local original=button:GetScript('OnClick');local index=i
 button:SetScript('OnClick',function(self,...)
  if custom()then local id=tabPage*8+index;if tabs[id]then SpellBookSkillLineTab_OnClick(self,id);UpdateSpells()end
  elseif original then original(self,...)end
 end)
end
hooksecurefunc('SpellBookFrame_Update',buttons)
local events=CreateFrame('Frame');events:RegisterEvent('SPELLS_CHANGED');events:RegisterEvent('PLAYER_ENTERING_WORLD');events:RegisterEvent('CVAR_UPDATE');events:RegisterEvent('CHAT_MSG_SYSTEM')
events:SetScript('OnEvent',function(_,event,message)if event~='CHAT_MSG_SYSTEM'or type(message)=='string'and (message:match('^HF_BUILD END')or message:match('^HF_MODE STATE'))then dirty=true end end)
SpellBookFrame:HookScript('OnShow',function()dirty=true end)
local elapsed=0
events:SetScript('OnUpdate',function(_,dt)
 elapsed=elapsed+dt;if elapsed<.2 then return end;elapsed=0
 if not enabled()then
  if active then active=false;SpellBookFrame.selectedSkillLine=1;SpellBookFrame_Update();UpdateSpells()end
  return
 end
 if dirty and SpellBookFrame:IsShown()and SpellBookFrame.bookType==BOOKTYPE_SPELL then
  rebuild();SpellBookSkillLineTab_OnClick(nil,SpellBookFrame.selectedSkillLine);UpdateSpells();buttons()
 end
end)
-- Onboarding must wait for server-confirmed build state, not temporary mode previews.
local prompt=A.PromptFirstAbilities
local queued,lastPrompt=false,-100
A.PromptFirstAbilities=function()queued=true end
local wait=0
local onboarding=CreateFrame('Frame')
onboarding:SetScript('OnUpdate',function(_,dt)
 if not queued then return end;wait=wait+dt;if wait<2 then return end
 if A.ServerBuildSyncRequired and not A.ServerBuildReady then return end
 queued=false;wait=0
 if GetTime()-lastPrompt<30 then return end
 for id,rank in pairs(HeroFreePickPlans and HeroFreePickPlans.previewLearned or {})do
  local e=A.byID[id];if rank>0 and e and not A.IsTalent(e)then return end
 end
 lastPrompt=GetTime();if prompt then prompt()end
end)
