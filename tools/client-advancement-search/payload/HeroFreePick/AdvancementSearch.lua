-- Search is presentation only: purchase and class eligibility remain authoritative.
local A=HeroFreePick
local function plain(text)
 return tostring(text or ''):gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r',''):gsub('|T.-|t',' '):gsub('|H.-|h(.-)|h','%1'):lower()
end
function A.SearchContains(text,query)
 text=plain(text)
 for word in plain(query):gmatch('%S+')do if not text:find(word,1,true)then return false end end
 return true
end
function A.SearchNameMatches(e,query)
 return A.SearchContains(A.DisplayTalentName and A.DisplayTalentName(e)or e.name,query)
end
local scanner,nativeCache=nil,{}
local function nativeText(id)
 if nativeCache[id]then return nativeCache[id]end
 if not CreateFrame or not id or id<=0 then return ''end
 scanner=scanner or CreateFrame('GameTooltip','HeroAdvancementSearchScanner',UIParent,'GameTooltipTemplate')
 scanner:SetOwner(UIParent,'ANCHOR_NONE');scanner:ClearLines()
 local ok=pcall(scanner.SetHyperlink,scanner,'spell:'..id)
 local parts={}
 if ok then for i=1,scanner:NumLines()do for _,side in ipairs({'Left','Right'})do
  local line=_G['HeroAdvancementSearchScannerText'..side..i]
  if line and line:GetText()then parts[#parts+1]=line:GetText()end
 end end end
 scanner:Hide()
 local text=table.concat(parts,' ')
 if text~=''then nativeCache[id]=text end -- missing client records can arrive later
 return text
end
function A.AdvancementSearchText(e)
 local parts={A.DisplayTalentName and A.DisplayTalentName(e)or e.name,e.class,e.spec,e.kind,e.quality}
 for _,key in ipairs({'description','bundleDescription','masteryDescription'})do
  if type(e[key])=='string'then parts[#parts+1]=e[key]end
 end
 for rank,id in ipairs(e.spells or {})do
  local description=A.AscensionTalentDescription and A.AscensionTalentDescription(e,rank)
  if description then parts[#parts+1]=description end
  parts[#parts+1]=nativeText(id)
  parts[#parts+1]='Spell ID '..id
 end
 parts[#parts+1]='Character Advancement ID '..(e.area52Entry or e.id)
 parts[#parts+1]='Requires Level '..(A.AbilityDisplayLevel and A.AbilityDisplayLevel(e)or e.level or 1)
 local parent=A.byID[e.requiredMastery or e.requiredBundle]
 if parent then parts[#parts+1]='Requires '..parent.name..' Automatically included at the required level; no additional cost.'end
 if A.mode=='Classic'and A.LearningSourceLines then
  for _,line in ipairs(A.LearningSourceLines(e))do parts[#parts+1]=line end
 end
 return table.concat(parts,' ')
end
function A.AdvancementSearchResults()
 local out={}
 local source=A.summary and A.LearnedEntries()or HeroFreePickCatalog
 for _,e in ipairs(source)do
  local context=A.summary or A.isBrowse or(e.class==A.class and(A.spec=='All'or e.spec==A.spec))
  local planned=HeroFreePickPlans and HeroFreePickPlans.entries and(HeroFreePickPlans.entries[e.id]or 0)>0
  local rarity=not A.quality or A.quality=='All'or e.quality==A.quality
  local ownership=not A.ownership or A.ownership=='All'or A.ownership=='Planned'and planned or A.ownership=='Not planned'and not planned
  if context and rarity and ownership and (not A.EntryAvailableInMode or A.EntryAvailableInMode(e))and
    A.SearchContains(A.AdvancementSearchText(e),A.tooltipQuery)then out[#out+1]=e end
 end
 table.sort(out,function(a,b)
  local al=A.AbilityDisplayLevel and A.AbilityDisplayLevel(a)or a.level or 1
  local bl=A.AbilityDisplayLevel and A.AbilityDisplayLevel(b)or b.level or 1
  if al~=bl then return al<bl end
  if a.name~=b.name then return a.name<b.name end
  return a.id<b.id
 end)
 return out
end
if CreateFrame then
 local events=CreateFrame('Frame')
 for _,event in ipairs({'PLAYER_ENTERING_WORLD','PLAYER_LEVEL_UP','SPELLS_CHANGED','UNIT_STATS','PLAYER_EQUIPMENT_CHANGED'})do events:RegisterEvent(event)end
 events:SetScript('OnEvent',function()nativeCache={}end)
end
