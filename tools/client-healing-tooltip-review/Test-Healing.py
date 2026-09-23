from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'work/regalia/libs'))
from lupa.lua51 import LuaRuntime
l=LuaRuntime(unpack_returned_tuples=True);l.execute('HeroFreePick={}')
f=HERE/'payload/HeroFreePick/ResolvedServerTooltips.lua';l.execute(f.read_text())
l.execute(Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test/Interface/AddOns/HeroFreePick/ServerTooltipValues.lua').read_text())
a=json.loads((HERE/'audit.json').read_text());assert a['resolved']==12
for entry in a['entries']:
 if entry['status']!='resolved base values':continue
 text,meta=l.globals().HeroFreePick.ResolveServerTooltip(entry['spell'])
 assert '[value pending]' not in text and '$<' not in text and len(meta['unresolved'])==0
 assert 'Base rank values before' in text
checks={5185:'37 to 51',139:'45 over 15 sec',8936:'another 98 over 21 sec',774:'40 over 15 sec',33763:'224 over 7 sec',724:'801 health over 6 sec',974:'for 150',136:'125 health over 15 sec',47541:'healing 250 damage'}
for sid,value in checks.items():assert value in l.globals().HeroFreePick.ResolveServerTooltip(sid)[0],sid
text,meta=l.globals().HeroFreePick.ResolveServerTooltip(760060);assert len(meta['unresolved']) and '|cffffff00' in text
l.execute('UnitRangedAttackPower=function()return 500,0,0 end');assert '120' in l.globals().HeroFreePick.ResolveServerTooltip(1978)[0]
print('PASS: Lua 5.1 and actual renderer; 12 resolved entries, base healing ranges/totals, Death Coil integer conversion, yellow unresolved Divine Star, Serpent Sting RAP regression.')
