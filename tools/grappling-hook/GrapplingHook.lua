-- Matched server implementation required. Only this additive entry is enabled.
local A,C=HeroFreePick,HeroCommitCatalog
if not A or not C then return end
local id=26001633
local levels={}
for _,race in ipairs({"Human","Orc","Dwarf","NightElf","Scourge","Tauren","Gnome","Troll","BloodElf","Draenei"}) do levels[race]=28 end
C.entries[id]={class="Rogue",name="Grappling Hook",group=false,level=28,ap=3,tp=0,
 rarity=4,gems=2,parent=0,maxRank=1,tokens={id},levels=levels}
C.tokens[id]={id=id,rank=1}
if C.excluded then C.excluded[id]=nil end
local entry=A.byID and A.byID[id]
if entry then
 entry.serverPending=false
 entry.referenceDescription="Launch a grappling hook and pull yourself to the target location. For 3 sec after using it you can recast it, pulling yourself to an enemy and rooting them for 1 sec. Does not break stealth."
end
