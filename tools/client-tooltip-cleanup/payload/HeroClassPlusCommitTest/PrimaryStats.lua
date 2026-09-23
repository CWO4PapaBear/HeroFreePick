local A=HeroFreePick
local details={
 Strength={summary='This primary stat focuses on dealing heavy hits and armor piercing attacks, and is especially beneficial for Plate armor users.\n\nGrants bonus Strength, Attack Power and Parry.',stats={
 {'Strength','Grants 2 bonus Strength per character level.'},
 {'Attack Power','Grants 1 additional melee and ranged Attack Power per point of total Strength, plus 1 melee and ranged Attack Power per character level. These bonuses are added to normal class Attack Power.'},
 {'Parry','Converts 25% of total Strength into additional parry-rating equivalent, rounded down. For example, 400 Strength grants the equivalent of 100 parry rating, not 100% parry chance. Normal rating conversion, parry eligibility and diminishing returns apply; this does not teach Parry.'},
 }},
 Agility={summary='This primary stat focuses on dealing rapid attacks and critical strikes, and is especially beneficial for Leather and Mail armor users.\n\nGrants bonus Agility and Attack Power, with weapon bonuses for faster abilities or stronger critical hits.',stats={
 {'Agility','Grants 2 bonus Agility per character level.'},
 {'Attack Power','Grants 1 additional melee and ranged Attack Power per point of total Agility, plus 1 melee and ranged Attack Power per character level. These bonuses are added to normal class Attack Power.'},
 {'Critical Strike Chance','Agility uses your normal class- and level-based critical chance conversion. This selection adds no separate fixed critical-chance percentage.'},
 {'Critical Strike Damage','Fatal Wounds grants 20% more melee/ranged ability critical-damage bonus while wielding a two-handed main-hand weapon. A normal 200% critical hit becomes 220%. No additional per-point Agility critical-damage conversion is enabled.'},
 },pending='Additional custom critical conversions are not implemented and remain disabled.'},
 Intellect={summary='This primary stat focuses on empowering spell damage, increasing mana pool, and is especially beneficial for Cloth armor users.\n\nGrants bonus Intellect and Spirit, and increases the spell-damage power gained from eligible Spell Power.',stats={
 {'Intellect and Spirit','Grants 2 bonus Intellect and 1 bonus Spirit per character level.'},
 {'Spell Power','Each 1 point of eligible Spell Power grants 1 additional point of spell-damage power. For example, 100 eligible Spell Power contributes 200 spell-damage power in total. This does not double healing or final spell damage; normal spell coefficients apply.'},
 {'Eligible Spell Power','Includes equipment Spell Power and the shared portion of all-magic damage/healing buffs on the same aura. Damage-only, healing-only, school-specific and stat-conversion bonuses are excluded.'},
 }},
 Spirit={summary='Spirit enables you to fulfill the |cFFFFFFFFHealer Role|r. This primary stat increases your Healing Power.\n\nGrants bonus Intellect and Spirit, and each point of eligible Spell Power also increases your Healing Power.',stats={
 {'Spirit and Intellect','Grants 2 bonus Spirit and 1 bonus Intellect per character level.'},
 {'Healing Power','Each 1 point of eligible Spell Power grants 1 additional point of healing power. For example, 100 eligible Spell Power contributes 200 healing power in total. This does not double spell damage or final healing; normal spell coefficients apply.'},
 {'Eligible Spell Power','Includes equipment Spell Power and the shared portion of all-magic damage/healing buffs on the same aura. Damage-only, healing-only, school-specific and stat-conversion bonuses are excluded.'},
 }},
}
local function line(text)GameTooltip:AddLine(text,1,.82,0,true)end
local function space()GameTooltip:AddLine(' ')end
local function effect(name,description)
 GameTooltip:AddLine(name,1,1,1,true);line(description);space()
end
function A.ServerPrimaryStatTooltip(owner)
 if not A.ServerPathEnrolled or (A.mode~='ClassPlus'and A.mode~='Hybrid'and A.mode~='Hero')then return false end
 local d=details[owner.primaryStatKey];local original=A.PrimaryStats and A.PrimaryStats[owner.primaryStatKey]
 if not d or not original then return false end
 GameTooltip:SetOwner(owner,'ANCHOR_LEFT');GameTooltip:SetText('Primary Stat: '..owner.primaryStatKey)
 line(d.summary)
 if A.TooltipDetailsExpanded then
  space()
  for _,v in ipairs(d.stats)do effect(v[1],v[2])end
  for _,v in ipairs(original.bonuses)do effect(v.name,v.description..' Granted while the required weapon type is equipped in your main hand.')end
  if d.pending then GameTooltip:AddLine(d.pending,1,1,0,true);space()end
  GameTooltip:AddLine('Source Spell ID: '..original.spell,.65,.65,.65)
  GameTooltip:AddLine('Character Advancement ID: '..original.advancement,.65,.65,.65)
 else GameTooltip:AddLine('Tap SHIFT for stat details and weapon bonuses.',.2,.85,1,true)end
 GameTooltip:AddLine('Applied when you Accept Changes.',.65,.65,.65,true)
 A.ShowAdvancementTooltip(GameTooltip);return true
end
-- Clarify visible test helper auras without changing their effects or hiding them.
local helpers={[9905201]='Strength',[9905211]='Strength',[9905202]='Agility',[9905212]='Agility'}
if hooksecurefunc and GameTooltip.SetUnitAura and UnitAura then
 hooksecurefunc(GameTooltip,'SetUnitAura',function(_,unit,index,filter)
  if (A.mode~='ClassPlus'and A.mode~='Hybrid'and A.mode~='Hero')or not A.ServerPathEnrolled then return end
  local id=select(11,UnitAura(unit,index,filter));local stat=helpers[id]
  if not stat then return end
  space();GameTooltip:AddLine('Primary Stat: '..stat..' â€” test helper',1,.82,0,true)
  line('This icon shows one part of the package. Your selected Primary Stat grants both melee and ranged attack power; see Hero Advancement for all effects.')
  A.ShowAdvancementTooltip(GameTooltip)
 end)
end
