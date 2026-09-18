from pathlib import Path
import contextlib,io,importlib.util,tempfile,shutil
ROOT=Path(__file__).resolve().parent
setup=(ROOT/'test_ui.py').read_text().split('lua.execute("""',1)[0]
setup=setup.replace("'Masteries.lua','AscensionAbilities.lua'", "'Masteries.lua','StockAbilityLevels.lua','ProgressionRules.lua','AscensionAbilities.lua'")
context={'__file__':str(ROOT/'test_ui.py')}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(setup,str(ROOT/'test_ui.py'),'exec'),context)
lua=context['lua'];addon=ROOT/'HeroFreePick'
lua.execute('''
local function stamp(e)
 return table.concat({e.id,e.name,e.class,e.spec,e.kind,table.concat(e.spells,','),e.nativeTalent or '-',e.ae or '-',e.te or '-',e.level or '-',e.requiredIDs or '-',e.requiredMastery or '-',e.requiredBundle or '-'},'|')
end
snapshot={};for _,e in ipairs(HeroFreePickCatalog)do snapshot[e.id]=stamp(e)end
checkIdentities=function()for _,e in ipairs(HeroFreePickCatalog)do assert(snapshot[e.id]==stamp(e))end end
originalRoutes=HeroFreePick.NativeTalentRoutes;originalRequirements=HeroFreePick.TalentPrerequisiteLines;originalSetRank=HeroFreePick.SetRank
''')
lua.execute((addon/'AscensionTalentData.lua').read_text())
lua.execute((addon/'AscensionTalentOverlay.lua').read_text())
lua.execute('''
checkIdentities();local A=HeroFreePick
assert(A.NativeTalentRoutes==originalRoutes and A.TalentPrerequisiteLines==originalRequirements and A.SetRank==originalSetRank)
local changed,missing=0,0
for id,meta in pairs(HeroAscensionTalentReferences)do
 local e=A.byID[id];assert(e)
 A.mode='Classic';assert(A.AscensionTalentDescription(e,1)==nil and A.AscensionTalentIcon(e)==nil)
 A.mode='ClassPlus'
 for rank,d in ipairs(meta.ranks)do
  local text,ref,note=A.AscensionTalentDescription(e,rank)
  if d.missingRank then assert(text==nil and note);missing=missing+1
  elseif d.changed then changed=changed+1;assert(ref.serverImplemented==false);assert(text==d.display or #d.unresolved>0)end
 end
end
assert(changed>0 and missing>0 and #A.AscensionTalentImports==29)
for _,e in ipairs(A.AscensionTalentImports)do assert(not A.byID[e.importID])end
local e=A.byID[406];A.mode='ClassPlus';UnitClass=function()return 'Mage','MAGE'end
local level=10;UnitLevel=function()return level end
local lines={};GameTooltip.AddLine=function(_,text,r,g,b)lines[#lines+1]={text,r,g,b}end
A.ShowEntryTooltip({entry=e});local red=false
for _,line in ipairs(lines)do if line[1]:match('^Requires Level')then red=line[2]==1 and line[3]==.15 end end
assert(red)
level=80;lines={};A.ShowEntryTooltip({entry=e});local green=false
for _,line in ipairs(lines)do if line[1]:match('^Requires Level')then green=line[2]==.1 and line[3]==1 end end
assert(green)
''')
spec=importlib.util.spec_from_file_location('importer',ROOT/'tools/talents/import_area52_talents.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.highlight('Raises damage by 5%.','Raises damage by 10%.')=='Raises damage by |cffffff0010%.|r'
assert m.highlight('Same text','Same text')=='Same text'
# Installation is idempotent and does not alter the catalogue or native routes.
scratch=Path.cwd()/'work'/('talent-import-test-'+__import__('uuid').uuid4().hex);scratch.mkdir(parents=True)
with contextlib.nullcontext(str(scratch))as td:
 target=Path(td)/'addon';target.mkdir();out=Path(td)/'out';out.mkdir();(out/'icons').mkdir()
 for name in ['HeroFreePick.lua','HeroFreePick.toc','Catalog.lua','Trees.lua','NativeTalentRoutes.lua']:shutil.copyfile(addon/name,target/name)
 shutil.copyfile(addon/'AscensionTalentData.lua',out/'AscensionTalentData.lua')
 before={p.name:p.read_bytes()for p in target.iterdir()}
 m.install(out,target);m.install(out,target)
 for name,blob in before.items():assert(target/name).read_bytes()==blob,name
print('PASS: identity/routing preservation, Classic isolation, rank mismatch fallback, prerequisite red/green, yellow delta and idempotent installation.')
