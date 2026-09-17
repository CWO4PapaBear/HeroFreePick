from pathlib import Path
import struct,json,hashlib,runpy,contextlib,io,re
from collections import Counter
import argparse
repo=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Audit Class+ catalog IDs against local stock and reference 3.3.5 Spell.dbc files; writes documentation only.')
parser.add_argument('--stock',type=Path,required=True)
parser.add_argument('--reference',type=Path,required=True)
args=parser.parse_args();stockPath=args.stock;areaPath=args.reference
def read(p):
 b=p.read_bytes();magic,n,f,size,strings=struct.unpack_from('<4s4I',b)
 assert magic==b'WDBC' and f==234 and size==936 and len(b)==20+n*size+strings
 st=b[20+n*size:];rows={}
 for row in struct.iter_unpack('<234I',b[20:20+n*size]):
  offset=row[136];assert offset<len(st)
  rows[row[0]]={'name':st[offset:st.index(b'\0',offset)].decode('utf-8')}
 return rows,hashlib.sha256(b).hexdigest()
stock,stockHash=read(stockPath);area,areaHash=read(areaPath)
assert stockHash=='d5cce1a83550dcfa9eb2f0251dbb11fd24c272534b2b1a9b230924a44d817ab3','Baseline differs from reviewed stock data; explicitly review and update the baseline before using this generator.'
with contextlib.redirect_stdout(io.StringIO()):state=runpy.run_path(str(repo/'test_ui.py'))
lua=state['lua'];g=lua.globals();a=g.HeroFreePick
lua.execute("HeroFreePick.mode='ClassPlus';UnitFactionGroup=function()return 'Alliance'end")
entries=[]
for _,e in g.HeroFreePickCatalog.items():
 # Include both factions, while honoring retired bundle duplicates and Classic exclusions.
 visible=a.EntryAvailableInMode(e)
 if not visible:
  lua.execute("UnitFactionGroup=function()return 'Horde'end")
  visible=a.EntryAvailableInMode(e)
  lua.execute("UnitFactionGroup=function()return 'Alliance'end")
 if not visible:continue
 entries.append({'entry':e['id'],'name':e['name'],'class':e['class'],'kind':e['kind'],'spells':[v for _,v in e['spells'].items()],
 'group':'mastery'if e['isMastery']else 'companion-wrapper'if e['isBundle']else 'companion-member'if e['requiredBundle']else 'mastery-member'if e['requiredMastery']else 'talent'if a.IsTalent(e)else 'ability',
 'catalogOnly':bool(e['catalogOnly']),'parent':e['requiredBundle']or e['requiredMastery']})
for stat,e in a.PrimaryStats.items():
 entries.append({'entry':'primary-stat-'+stat,'name':'Primary Stat: '+stat,'class':'All','kind':'PrimaryStat','spells':[e['spell']],'group':'primary-stat','catalogOnly':False,'parent':None})
rows=[]
for e in entries:
 for sid in e.pop('spells'):
  s=stock.get(sid);r=area.get(sid)
  if e['catalogOnly']or sid==0:status='catalog-only'
  elif not s:status='absent-from-stock'
  elif r and s['name'].casefold()!=r['name'].casefold():status='stock-id-name-conflict'
  elif s['name'].casefold()!=e['name'].casefold():status='stock-present-label-review'
  else:status='stock-present'
  route=('More Minions'if e['group'].startswith('companion')or e['parent']==21954705 or e['name']=='Demon Mastery'else
    'Mage travel'if e['name'].startswith(('Portal:','Teleport:'))else
    'Entitlement/grant rules'if e['group']=='mastery'else 'Class+ spell mechanics')
  rows.append(dict(e,spell=sid,stockName=s['name']if s else None,referenceName=r['name']if r else None,status=status,implementationOwner=route))
summary=Counter(x['status']for x in rows)
result={'scope':'All Class+ source classes, both factions, all referenced ranks plus primary stat choices. Retired companion duplicates and Classic-only supplements excluded.',
 'limitations':'Stock client DBC presence is a baseline, not a live AzerothCore SpellMgr check. Same ID/name does not prove same mechanics. Dependencies/effects, SQL-only server spells and runtime support still need review. Do not install these records as spell definitions.',
 'stockSource':{'file':stockPath.name,'sha256':stockHash,'records':len(stock)},'referenceSource':{'file':areaPath.name,'sha256':areaHash,'records':len(area)},
 'sourceAddonVersion':'0.39.9','summary':dict(summary),'uniqueMissingSpells':len({x['spell']for x in rows if x['status']=='absent-from-stock'}),'records':rows}
(repo/'docs/classplus-spell-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
report=['# Class+ spell availability audit','','This is the first server-integration inventory, not installable spell SQL or a client patch. It compares the effective FreePick catalog against the saved stock 3.3.5 Spell.dbc (hash matched to the earlier stock catalog). No live server has been queried.','','## Coverage','',result['scope'],'',f"{len(entries)} catalog/stat entries; {len(rows)} spell references; {len({x['spell'] for x in rows if x['spell']})} distinct nonzero IDs.",'','| Classification | References |','|---|---:|']
report += [f'| {k} | {v} |'for k,v in sorted(summary.items())]
report += ['',f"**{result['uniqueMissingSpells']} distinct referenced spell IDs are absent from the stock baseline.** These are candidates for new definitions, not a count of new records ultimately needed: wrappers can be server entitlements, stock equivalents may be reusable, and triggered/dependent spells can add requirements.",'','## Implementation rules','','1. Reuse stock spell IDs when the intended mechanics match. Unavailable training/access is not the same as a missing spell.','2. Never overwrite an existing stock ID with an imported ability. Name conflicts require a mechanic comparison and, when different, new namespaced IDs.','3. Mastery wrappers can be authoritative purchase/grant entitlements without a castable spell record. Teleport Mastery currently uses UI-only spell 0.','4. Pet behavior belongs to More Minions; Mage travel needs independent IDs and its agreed reagent-generation handlers. Reference IDs in the current UI are not finished server definitions.','5. For genuinely new castable abilities, define matching client/server records, effects, triggered dependencies, required hooks, scaling, ranks, visuals and ownership rules. Spell records alone do not implement unsupported effects.','6. Pin the actual target core and audit its DBC/SQL/SpellMgr data before reserving IDs or generating install/uninstall SQL. Preserve Classic records unchanged.','','## Missing and conflicting references','','Names and IDs only; no extracted binary or full spell definitions are shipped here. A52 presence is evidence for research, not a working implementation.','','| Class | Entry | Ability | Spell | Status | Stock name | Reference name | Owner |','|---|---|---|---:|---|---|---|---|']
for x in sorted(rows,key=lambda x:(x['class'],x['name'],x['spell'])):
 if x['status']in ('stock-present','stock-present-label-review'):continue
 vals=[x['class'],str(x['entry']),x['name'],str(x['spell']),x['status'],x['stockName']or '—',x['referenceName']or '—',x['implementationOwner']]
 report.append('| '+' | '.join(str(v).replace('|','/')for v in vals)+' |')
report += ['','## Next implementation milestone','','Review the missing/conflicting queue by class; separate actual combat spells from wrapper entitlements, pet-module dependencies and travel-module dependencies. Resolve each ability\'s intended mechanics and dependency graph before producing any client patch or server insert. The JSON retains all references, including stock-present label mismatches, for that review.']
(repo/'docs/CLASSPLUS-SPELL-AUDIT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items()if k in ('summary','uniqueMissingSpells')},indent=2))
print('entries',len(entries),'references',len(rows))
