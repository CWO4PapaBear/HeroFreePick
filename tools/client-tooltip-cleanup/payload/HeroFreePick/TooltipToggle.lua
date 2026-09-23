-- Hero Advancement only: Shift toggles tooltip detail, without changing the
-- physical modifier APIs used by chat links, spellbook, or other addons.
local A=HeroFreePick
A.TooltipDetailsExpanded=false
local held={}
function A.HandleTooltipModifier(key,state,visible)
 if key~='LSHIFT'and key~='RSHIFT'and key~='SHIFT'then return false end
 local wasDown=held.LSHIFT or held.RSHIFT or held.SHIFT
 local down=tonumber(state)==1
 held[key]=down
 if visible and down and not wasDown then
  A.TooltipDetailsExpanded=not A.TooltipDetailsExpanded
  return true
 end
 return false
end
