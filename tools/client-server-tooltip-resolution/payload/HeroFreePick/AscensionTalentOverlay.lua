-- Reference-only presentation overlay. Never mutate catalogue identities or routes.
local A=HeroFreePick
local function reference(e)
 if A.mode=='Classic'or not e then return end
 return HeroAscensionTalentReferences and HeroAscensionTalentReferences[e.id]
end
function A.AscensionTalentIcon(e)
 local meta=reference(e);return meta and meta.icon
end
function A.AscensionTalentDescription(e,rank)
 if A.mode~='Classic'and e then
  local spell=e.spells and e.spells[math.min(rank or 1,#e.spells)]
  local resolved,details
  if A.ResolveServerTooltip then resolved,details=A.ResolveServerTooltip(spell)end
  if resolved then
   if e.purchaseOnly or e.serverPending or (e.importedTalent and e.serverDefinitionAvailable==false) then resolved='|cffffff00'..resolved:gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r','')..'|r'end
   return resolved,details
  end
  local current=HeroServerSpellDescriptions and HeroServerSpellDescriptions[spell]
  if current then
   local text=current.text:gsub('\\r',''):gsub('\\n','\n')
   -- Do not invent dynamic formulas or values missing auxiliary lookup tables.
   for _,token in ipairs(current.unresolved or {})do
    local pattern=token:gsub('([^%w])','%%%1');text=text:gsub(pattern,function()return '|cffffff00[value pending]|r'end)
   end
   if e.purchaseOnly or e.serverPending or (e.importedTalent and e.serverDefinitionAvailable==false) then text='|cffffff00'..text:gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r','')..'|r'end
   return text,{serverDefinition=true,unresolved=current.unresolved}
  end
  if e.importedTalent then return nil end
 end
 local meta=reference(e);if not meta then return end
 local desc=meta.ranks[rank or 1]
 if not desc or desc.missingRank then return nil,meta,'No matching reference rank; the current spell description is retained.'end
 local text=desc.display
 -- Preserve exact unresolved expressions in the export, not as misleading game values.
 if desc.unresolved and #desc.unresolved>0 then
  text=text:gsub('%$[^%s,]+','|cffffff00[value pending]|r')
 end
 return text,meta
end
function A.AddAscensionTalentNotes(e,rank)
 if A.mode~='Classic'and e.id==27001448 then
  local met=HeroFreePickPlans and HeroFreePickPlans.primaryStat=='Agility'
  GameTooltip:AddLine('Requires Primary Stat: Agility',met and .2 or 1,met and 1 or .2,.2,true)
 end
 local _,meta,missing=A.AscensionTalentDescription(e,rank)
 if A.mode~='Classic'and e.importedTalent then
  if not e.serverDefinitionAvailable then GameTooltip:AddLine('Unavailable: a server spell definition is missing.',1,.35,.3,true)
  elseif e.purchaseOnly then
   GameTooltip:AddLine('Purchasing supported after the matching server update. Custom effects still require implementation or verification.',1,.82,.3,true)
  else
   GameTooltip:AddLine('Imported talent: spell data is installed; custom effects still need gameplay verification.',1,.82,.3,true)
  end
 end
 if not meta then return end
 if meta.serverDefinition then
  if meta.unresolved and #meta.unresolved>0 then GameTooltip:AddLine('Yellow values remain unresolved; this may be a tooltip formula or missing server data.',1,1,0,true)end
  return
 end
 if meta.name~=e.name then GameTooltip:AddLine('Reference talent: '..meta.name,1,1,0,true)end
 if not meta.serverImplemented and meta.changed then GameTooltip:AddLine('Yellow text describes changes awaiting server implementation.',1,1,0,true)end
 if meta.rankCountChanged then GameTooltip:AddLine('Reference rank count differs. Current ranks and costs are unchanged.',1,1,0,true)end
 if missing then GameTooltip:AddLine(missing,1,1,0,true)end
 local desc=meta.ranks[rank or 1]
 if desc and desc.unresolved and #desc.unresolved>0 then GameTooltip:AddLine('Some reference values require additional formula handling.',1,1,0,true)end
end
-- New talents are available to the importer/review tooling, never silently placed
-- over native nodes or sent to a server under an unverified spell identity.
A.AscensionTalentImports=HeroAscensionNewTalents or {}
