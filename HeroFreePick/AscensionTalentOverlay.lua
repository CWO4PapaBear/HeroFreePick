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
 local _,meta,missing=A.AscensionTalentDescription(e,rank)
 if not meta then return end
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
