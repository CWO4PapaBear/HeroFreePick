from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
root=Path(__file__).resolve().parent
lua=LuaRuntime()
for p in (root/'payload').rglob('*.lua'):
    source=p.read_text(encoding='utf-8-sig')
    lua.execute('assert(loadstring(...))',source)
    assert 'IsShiftKeyDown' not in source
lua.execute('HeroFreePick={}')
lua.execute((root/'payload/HeroFreePick/TooltipToggle.lua').read_text(encoding='utf-8'))
lua.execute('''
local A=HeroFreePick;local f=A.HandleTooltipModifier
assert(not A.TooltipDetailsExpanded)
assert(f('LSHIFT',1,true) and A.TooltipDetailsExpanded)
assert(not f('LSHIFT',1,true) and A.TooltipDetailsExpanded)
assert(not f('LSHIFT',0,true) and A.TooltipDetailsExpanded)
assert(f('RSHIFT',1,true) and not A.TooltipDetailsExpanded)
assert(not f('LSHIFT',1,true));assert(not f('RSHIFT',0,true));assert(not f('LSHIFT',0,true))
assert(not f('LCTRL',1,true))
assert(not f('LSHIFT',1,false));assert(not f('LSHIFT',0,false))
assert(f('LSHIFT','1',true) and A.TooltipDetailsExpanded)
assert(not f('LSHIFT','0',true))
''')
print('PASS: Lua 5.1 syntax; one toggle per Shift press, release preserves state, repeat/dual Shift and non-Shift handling, closed menu ignored.')
