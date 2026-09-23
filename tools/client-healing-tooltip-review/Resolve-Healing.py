"""Resolve reviewed healing base values from the current PTR export; no live writes."""
from pathlib import Path
import json,hashlib,importlib.util,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('resolver',ROOT/'outputs/Hero_Server_Tooltip_Resolution/Resolve.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
BASE=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path']
manifest=json.loads((BASE/'manifest.json').read_text());assert not manifest['missing']
for name,h in manifest['files'].items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h,name
# Keep the original evidence intact; adapt the old loader to the fresh export.
source=(ROOT/'outputs/Hero_Server_Tooltip_Resolution/Resolve.py').read_text();start=source.index('def load():');end=source.index('\ndef expression_tree',start)
loader=source[start:end].replace("BASE/'spell-overrides.tsv'","BASE/'spell_dbc-rows.tsv'").replace("ROOT/'outputs/Hero_Abomination_Test/live-baseline'/f'{name}.dbc'","BASE/f'{name}.dbc'")
r.BASE=BASE;exec(loader,r.__dict__);db,tables,overrides=r.load();variables=r.imp.DBC(BASE/'SpellDescriptionVariables.dbc')
client=r.CLIENT;lua=r.LuaRuntime();lua.execute((client/'ServerSpellDescriptions.lua').read_text());lua.execute((client/'ResolvedServerTooltips.lua').read_text())
def plain(v):
 if hasattr(v,'items'):
  d={k:plain(x) for k,x in v.items()}
  if d and all(isinstance(k,int) for k in d) and set(d)==set(range(1,len(d)+1)):return [d[k] for k in range(1,len(d)+1)]
  return d
 return v
existing=plain(lua.globals().HeroResolvedServerTooltips);audit=[];count=0
names={'Healing Touch','Renew','Regrowth','Rejuvenation','Lifebloom','Lightwell','Earth Shield','Earthliving Weapon','Mend Pet','Death Coil','Mana Tide Totem','Siphon Life'}
for sid,item in lua.globals().HeroServerSpellDescriptions.items():
 sid=int(sid);row=db.rows.get(sid)
 if not row:continue
 name=db.text(row[136]);text=db.text(row[170]);is_heal=any(e in (10,67,136) for e in row[71:74]) or any(a in (8,62) for a in row[95:98]) or bool(re.search(r'\bheal|restore.{0,60}health',text,re.I))
 if not is_heal:continue
 count+=1
 current=existing.get(sid,plain(item))
 if not current.get('unresolved') and '[value pending]' not in current.get('text',''):continue
 entry={'spell':sid,'name':name,'before':current,'source':'spell_dbc' if sid in overrides else 'Spell.dbc','variablesId':row[232]}
 if name not in names:
  entry['status']='unresolved: requires separate formula review';audit.append(entry);continue
 defs={}
 if row[232] in variables.rows:
  raw=variables.text(variables.rows[row[232]][1]);defs=dict(re.findall(r'^\$(\w+)=(.+)$',raw.replace('\r',''),re.M));entry['variableDefinitions']=defs
 def expand(value,seen=()):
  def named(m):
   key=m[1]
   if key in seen or len(seen)>20 or key not in defs:raise ValueError('Missing/cyclic variable '+key)
   return expand(defs[key],seen+(key,))
  # Explicitly base values: choose the no-talent/no-glyph branch and label it.
  value=re.sub(r'\$\?[sa]\d+\[([^\[\]]*)\]\[([^\[\]]*)\]',lambda m:m[2],value)
  value=re.sub(r'\$<([^>]+)>',named,value)
  for _ in range(30):
   old=value;value=re.sub(r'\$\{([^{}]+)\}',lambda m:'('+m[1]+')' if value[:m.start()].count('{')>value[:m.start()].count('}') else m[0],value)
   if old==value:break
  return value
 try:
  expanded=expand(text)
  # Flatten arithmetic wrappers inside a larger formula, retaining its outer wrapper.
  entry['expandedBaseDescription']=expanded
  original=db.rows[sid];strings=db.strings;tmp=list(original);tmp[170]=len(strings);db.strings+=expanded.encode()+b'\0';db.rows[sid]=tuple(tmp)
  try:new=r.resolve(db,tables,sid)
  finally:db.rows[sid]=original;db.strings=strings
  if new['unresolved']:entry['status']='unresolved after expansion';entry['attempt']=new
  else:
   if sid==47541:new['text']=new['text'].replace('250.5','250') # spell_dk_death_coil truncates damage * 1.5 to int32.
   new['text']+='\n\nBase rank values before level scaling, spell power, talents, glyphs and target modifiers.'
   existing[sid]=new;entry['status']='resolved base values';entry['after']=new
 except ValueError as e:entry['status']=str(e)
 audit.append(entry)
out=HERE/'payload/HeroFreePick';out.mkdir(parents=True,exist_ok=True)
f=out/'ResolvedServerTooltips.lua';f.write_text('-- Current PTR healing base values; unresolved entries retained.\nHeroResolvedServerTooltips='+r.imp.lua(existing)+'\n')
report={'image':manifest['image'],'healingDescriptionsReviewed':count,'resolved':sum(e['status']=='resolved base values' for e in audit),'entries':audit,'sources':manifest['files']};(HERE/'audit.json').write_text(json.dumps(report,indent=2))
rel='HeroFreePick/ResolvedServerTooltips.lua';(HERE/'client-manifest.json').write_text(json.dumps({rel:{'before':hashlib.sha256((client/'ResolvedServerTooltips.lua').read_bytes()).hexdigest(),'after':hashlib.sha256(f.read_bytes()).hexdigest()}},indent=2))
print('Healing descriptions reviewed:',count,'resolved:',report['resolved'])
for e in audit:print(e['spell'],e['name'],e['status'],e.get('after',{}).get('text',''))
