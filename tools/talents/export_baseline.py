"""Export current catalogue identities using the repository's Lua 5.1 harness.
Requires lupa.lua51. Does not execute the test scenarios or export saved character data.
"""
from pathlib import Path
import argparse,contextlib,io,json
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
root=Path(__file__).resolve().parents[2]
setup=(root/'test_ui.py').read_text().split('lua.execute("""',1)[0]
setup=setup.replace("'Masteries.lua','AscensionAbilities.lua'", "'Masteries.lua','StockAbilityLevels.lua','ProgressionRules.lua','AscensionAbilities.lua'")
context={'__file__':str(root/'test_ui.py')}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(setup,str(root/'test_ui.py'),'exec'),context)
keys=['id','name','class','spec','kind','spells','nativeTalent','talentOrigin','area52Entry','ae','te','level','requiredAE','requiredTE','requiredIDs','requiredMastery','requiredBundle']
entries=[]
for e in context['lua'].globals().HeroFreePickCatalog.values():
 row={}
 for k in keys:
  v=e[k]
  if v is not None:row[k]=list(v.values())if k=='spells'else v
 entries.append(row)
Path(args.output).write_text(json.dumps(entries,indent=2)+'\n')
print('Exported',len(entries),'current catalogue identities')
