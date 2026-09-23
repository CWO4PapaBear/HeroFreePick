local A=HeroFreePick
local function stat(key)
 if key=='AP'or key=='RAP'then
  local api=key=='AP'and UnitAttackPower or UnitRangedAttackPower
  if not api then return nil end
  local base,pos,neg=api('player')
  if not base then return nil end
  return math.max(0,base+(pos or 0)+(neg or 0))
 elseif key=='SPI'and UnitStat then
  local _,effective=UnitStat('player',5);return effective
 end
end
local function evaluate(node,depth)
 depth=(depth or 0)+1;if depth>30 then return nil end
 if type(node)=='number'then return node end
 if type(node)=='string'then return stat(node)end
 if type(node)~='table'then return nil end
 local left,right=evaluate(node[2],depth),evaluate(node[3],depth)
 if not left or not right then return nil end
 local op=node[1]
 if op=='+'then return left+right elseif op=='-'then return left-right
 elseif op=='*'then return left*right elseif op=='/'and right~=0 then return left/right end
end
function A.ResolveServerTooltip(spell)
 local entry=HeroResolvedServerTooltips and HeroResolvedServerTooltips[spell]
 if not entry then return nil end
 local text=entry.text;local unresolved={}
 for _,token in ipairs(entry.unresolved)do unresolved[#unresolved+1]=token end
 for key,tree in pairs(entry.formulas)do
  local value=evaluate(tree)
  local replacement
  if value and value==value and math.abs(value)<1e15 then
   replacement=tostring(math.floor(value+0.5))
  else replacement='[value pending]';unresolved[#unresolved+1]=key end
  text=text:gsub(key,function()return replacement end)
 end
 if #unresolved>0 then
  text='|cffffff00'..text:gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r','')..'|r'
 end
 return text,{serverDefinition=true,unresolved=unresolved}
end
