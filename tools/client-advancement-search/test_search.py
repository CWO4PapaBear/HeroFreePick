"""Offline Lua 5.1 search/filter checks. Does not install client files."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
# Requires lupa with Lua 5.1 (pip install lupa).
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
client=HERE/'payload/HeroFreePick'
for name in ('AdvancementSearch.lua','HeroFreePick.lua','Adapter.lua','Organization.lua'):
    result=lua.eval('loadstring')((client/name).read_text(encoding='utf-8'))
    assert not isinstance(result,tuple),(name,result)
lua.execute('''
HeroFreePick={mode='Hero',class='Rogue',spec='All',quality='All',ownership='All',byID={}}
HeroFreePickPlans={entries={[1]=1},previewLearned={[1]=1,[2]=1}}
HeroFreePickCatalog={
 {id=1,name='Strike',class='Rogue',spec='Combat',kind='Ability',quality='Normal',level=1,description='Deals weapon damage',spells={}},
 {id=2,name='Vigor',class='Rogue',spec='Assassination',kind='Talent',quality='Rare',level=10,description='Retains combo points',spells={}},
 {id=3,name='Frostbolt',class='Mage',spec='Frost',kind='Ability',quality='Normal',level=1,description='Deals frost damage',spells={}}
}
for _,e in ipairs(HeroFreePickCatalog)do HeroFreePick.byID[e.id]=e end
''')
lua.execute((client/'AdvancementSearch.lua').read_text(encoding='utf-8'))
lua.execute('''
local A=HeroFreePick
A.tooltipQuery='damage';assert(#A.AdvancementSearchResults()==1)
A.isBrowse=true;assert(#A.AdvancementSearchResults()==2)
A.isBrowse=false;A.spec='Assassination';A.tooltipQuery='combo';assert(#A.AdvancementSearchResults()==1)
A.spec='Combat';assert(#A.AdvancementSearchResults()==0)
A.spec='All';A.tooltipQuery='';A.quality='Rare';assert(#A.AdvancementSearchResults()==1)
A.quality='All';A.ownership='Planned';assert(#A.AdvancementSearchResults()==1)
A.ownership='Not planned';assert(#A.AdvancementSearchResults()==1)
A.isBrowse=true;assert(#A.AdvancementSearchResults()==2)
A.EntryAvailableInMode=function(e)return e.id~=3 end;assert(#A.AdvancementSearchResults()==1)
A.EntryAvailableInMode=nil;A.summary=true;A.ownership='All'
A.LearnedEntries=function()return {A.byID[1],A.byID[2]}end
assert(#A.AdvancementSearchResults()==2)
assert(A.SearchContains('|cff00ff00Combo|r points','COMBO points'))
assert(A.SearchContains('100% [damage]','% [damage]'))
assert(not A.SearchContains('heals','damage'))
A.DisplayTalentName=function(e)return e.id==2 and 'Martial Fluidity'or e.name end
assert(A.SearchNameMatches(A.byID[2],'martial'))
assert(not A.SearchNameMatches(A.byID[2],'damage'))
''')
print('PASS: Lua 5.1 syntax; Overview/class/tree/summary scope; mode, rarity, ownership; talent names; literal tooltip matching.')
