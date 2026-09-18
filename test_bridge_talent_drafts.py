from pathlib import Path
import contextlib,io
r=Path(__file__).resolve().parent;setup=(r/'test_ui.py').read_text().split('lua.execute("""',1)[0].replace("'Masteries.lua','AscensionAbilities.lua'","'Masteries.lua','StockAbilityLevels.lua','ProgressionRules.lua','AscensionAbilities.lua'");ctx={'__file__':str(r.resolve()/'test_ui.py')}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(setup,str(r/'test_ui.py'),'exec'),ctx)
lua=ctx['lua'];lua.execute("UnitClass=function()return 'Mage','MAGE'end;UnitLevel=function()return 80 end;GetTime=function()return 1 end;HeroFreePick.InstalledModes.ClassPlus=true;HeroFreePick.mode='ClassPlus';HeroFreePick.ServerPathEnrolled=true;HeroFreePick.Init();HeroFreePick.BeginPreparation();HeroFreePick.ShowPointWarning=function(s)lastWarning=s end")
for f in ['Catalog.lua','CommitTest.lua']:lua.execute((r/'profiles/HeroClassPlusCommitTest'/f).read_text())
lua.execute("""
local A=HeroFreePick
assert(A.SetLocalLearned(108,1))
assert(A.SetLocalLearned(401,1))
assert(not HeroFreePickPlans.previewLearned[401]and HeroFreePickPlans.previewLearned[20000029]==1)
assert(A.SetLocalLearned(401,0));assert(not HeroFreePickPlans.previewLearned[20000029])
assert(A.SetLocalLearned(398,1));assert(A.SetLocalLearned(398,2));assert(A.SetLocalLearned(398,1));assert(A.SetLocalLearned(398,0))
UnitLevel=function()return 9 end
assert(not A.SetLocalLearned(398,1));assert(lastWarning:find('level',1,true))
UnitLevel=function()return 10 end
assert(A.SetLocalLearned(398,1));assert(not A.SetLocalLearned(398,2));assert(lastWarning=='Not enough Talent Points.')
""")
print('PASS: talent ability aliases, passive talent draft add/remove, level and TP guards.')
