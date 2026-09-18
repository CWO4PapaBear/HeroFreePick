"""Import Area 52 talent references without replacing live spell or talent identities.
Python 3.10+, standard library. Inputs are extracted, locally supplied client data.
"""
from pathlib import Path
import argparse, collections, difflib, hashlib, json, re, struct, shutil

CLASSES={'Warrior','Paladin','Hunter','Rogue','Priest','DeathKnight','Shaman','Mage','Warlock','Druid'}
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def lua(v):
 if v is None:return 'nil'
 if isinstance(v,bool):return str(v).lower()
 if isinstance(v,(int,float)):return str(v)
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 return '{'+','.join('['+lua(k)+']='+lua(x)for k,x in v.items())+'}'
class DBC:
 def __init__(self,path,width=None):
  self.path=Path(path);b=self.path.read_bytes();magic,n,fields,stride,size=struct.unpack_from('<4s4I',b)
  if magic!=b'WDBC'or stride%4 or len(b)!=20+n*stride+size:raise ValueError('Invalid DBC '+str(path))
  if width and stride!=width*4:raise ValueError('Unexpected record width '+str(path))
  self.rows={r[0]:r for r in struct.iter_unpack('<'+'I'*(stride//4),b[20:20+n*stride])};self.strings=b[20+n*stride:]
 def text(self,offset):
  if not 0<=offset<len(self.strings):raise ValueError('Invalid string offset')
  return self.strings[offset:self.strings.index(b'\0',offset)].decode('utf-8')
def signed(v):return v if v<2**31 else v-2**32
def float32(v):return struct.unpack('<f',struct.pack('<I',v))[0]
def plain(text):return re.sub(r'\s+',' ',text).strip()
def render(db,sid,tables):
 """Conservative offline rendering. Unknown formulas remain explicit, never invented."""
 row=db.rows.get(sid)
 if not row:return '',['missing-spell']
 text=db.text(row[170])or db.text(row[187]);text=text.replace('\r','').replace('@ext:','').replace(':ext@','')
 text=re.sub(r'\|c[0-9a-fA-F]{8}|\|r','',text)
 text=re.sub(r'@s:(\d+):\d+@',lambda m:db.text(db.rows[int(m[1])][136])if int(m[1])in db.rows else m[0],text)
 unresolved=[]
 def token(m):
  q=db.rows.get(int(m[1])if m[1]else sid);kind=m[2];i=int(m[3]or 1)-1
  if q:
   if kind in ['s','S','m','M']and 0<=i<3:return '%g'%abs(signed(q[80+i])+signed(q[74+i]))
   if kind=='t'and 0<=i<3:return '%g'%(q[98+i]/1000)
   if kind=='i':return str(q[212])
   if kind=='n':return str(q[36])
   if kind=='o'and 0<=i<3 and q[40]in tables.get('SpellDuration',{})and q[98+i]:return '%g'%(abs(signed(q[80+i])+signed(q[74+i]))*max(0,signed(tables['SpellDuration'][q[40]][1]))/q[98+i])
   if kind=='u':return str(q[49])
   if kind=='h':return str(q[35])
   if kind=='d'and q[40]in tables.get('SpellDuration',{}):
    value=signed(tables['SpellDuration'][q[40]][1]);return 'until canceled'if value<0 else '%g sec'%(value/1000)
   if kind in ['a','A']and 0<=i<3 and q[92+i]in tables.get('SpellRadius',{}):return '%g'%float32(tables['SpellRadius'][q[92+i]][1])
   if kind=='r'and q[46]in tables.get('SpellRange',{}):return '%g'%float32(tables['SpellRange'][q[46]][3])
  return m[0]
 def arithmetic(m):
  value=token(re.match(r'(\d*)([sSmM])(\d*)',m[3]+m[4]+m[5]))
  try:return '%g'%(float(value)/float(m[2])if m[1]=='/'else float(value)*float(m[2]))
  except (ValueError,ZeroDivisionError):return m[0]
 text=re.sub(r'\$([/*])([0-9.]+);(\d*)([sSmM])([123])',arithmetic,text)
 text=re.sub(r'\$(\d*)([sSmMtaAduhrnoi])(\d*)\b',token,text)
 # Keep both conditional branches, explicitly labelled; do not assume a capstone is learned.
 def bracket(start):
  depth=0
  for end in range(start,len(text)):
   if text[end]=='[':depth+=1
   elif text[end]==']':
    depth-=1
    if depth==0:return end
  return -1
 for _ in range(20):
  match=re.search(r'\$\?s(\d+)\[',text)
  if not match:break
  opening=match.end()-1;end=bracket(opening)
  if end<0 or text[end+1:end+2]!='[':break
  last=bracket(end+1)
  if last<0:break
  spell=int(match[1]);name=db.text(db.rows[spell][136])if spell in db.rows else 'spell '+str(spell)
  yes=text[opening+1:end];no=text[end+2:last]
  replacement=('When '+name+' is active: '+yes if yes else '')+('\nOtherwise: '+no if no else '')
  text=text[:match.start()]+replacement+text[last+1:]
 text=re.sub(r'@req:(\d+)@',lambda m:'[Reference prerequisite '+m[1]+']',text)
 text=re.sub(r'\$l([^:;]+):([^;]+);',r'\2',text)
 # Preserve unresolved syntax in the reference export. The tooltip labels it.
 unresolved=sorted(set(re.findall(r'\$[^\s,]+|@[^\s]+',text)))
 return text.strip(),unresolved

def highlight(old,new):
 a=re.findall(r'\s+|[^\s]+',old);b=re.findall(r'\s+|[^\s]+',new);out=[]
 for op,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
  text=''.join(b[k:l]);out.append(text if op=='equal'else '|cffffff00'+text+'|r'if text else '')
 return ''.join(out)

def effect_signature(r):
 # Exact raw mechanics only, not a claim that server scripts are equivalent.
 return tuple(r[1:131])+tuple(r[204:234])

def run(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 adv=DBC(args.advancement,173);spells=DBC(args.spells,234);stock=DBC(args.stock_spells,234)
 meta={e['ID']:e for e in json.loads(Path(args.metadata).read_text())}
 baseline=json.loads(Path(args.baseline).read_text());baseline=[e for e in baseline if e.get('class')in CLASSES and e.get('spells')]
 confirmed=json.loads(Path(args.confirmed).read_text())if args.confirmed else {}
 overrides=json.loads(Path(args.matches).read_text())if args.matches else {}
 tables={};lookupfiles=[]
 for name in ['SpellDuration','SpellRadius','SpellRange']:
  path=Path(args.tables)/(name+'.dbc')
  if path.exists():tables[name]=DBC(path).rows;lookupfiles.append(path)
 talent_db=DBC(args.talents,23)if getattr(args,'talents',None)else None
 topology={}
 if talent_db:
  for tid,t in talent_db.rows.items():topology[tid]={'talentID':tid,'tab':t[1],'row':t[2],'column':t[3],'ranks':[x for x in t[4:13]if x],'dependencies':list(t[13:16]),'dependencyRanks':list(t[16:19]),'rawFields':list(t)}
 icons={}
 for path in sorted(Path(args.icon_dbcs).glob('*.dbc')):
  db=DBC(path,2)
  for id,row in db.rows.items():icons[id]=db.text(row[1])
 iconfiles={norm(p.stem):p for p in sorted(Path(args.icons).rglob('*.blp'))}
 byname=collections.defaultdict(list);byspell=collections.defaultdict(list);byfunction=collections.defaultdict(list)
 for e in baseline:
  byname[e['class'],norm(e['name'])].append(e)
  for sid in e['spells']:
   byspell[e['class'],sid].append(e)
  if e['spells'] and e['spells'][0]in stock.rows:byfunction[e['class'],effect_signature(stock.rows[e['spells'][0]])].append(e)
 records=[];skipped=[];assets={};required=set();target_candidates=collections.defaultdict(list)
 for id,r in sorted(adv.rows.items()):
  q=meta.get(id);kind=adv.text(r[1])
  if kind not in ('Talent','TalentAbility'):continue
  if not q or q.get('Class')not in CLASSES or q.get('Flags',0)&9:
   skipped.append({'id':id,'reason':'not a visible standard-class talent'});continue
  ranks=[x for x in r[5:14]if x];required.update(ranks)
  names=byname[q['Class'],norm(q['Name'])]
  shared={e['id']:e for sid in ranks for e in byspell[q['Class'],sid]}
  matches={e['id']:e for e in names};matches.update(shared);method='name/spell-identity'if matches else 'none'
  if not matches and ranks and ranks[0]in spells.rows:
   exact=byfunction[q['Class'],effect_signature(spells.rows[ranks[0]])]
   # A unique native talent plus its ability aliases is safe as a candidate only;
   # function-only mappings require explicit human approval.
   function_candidates=sorted({e['id']for e in exact})
  else:function_candidates=[]
  if str(id)in overrides:
   wanted=overrides[str(id)];matches={e['id']:e for e in baseline if e['id']in wanted}
   if sorted(matches)!=sorted(wanted):raise ValueError('Invalid explicit target '+str(id))
   method='reviewed-override'
  path=q.get('Icon')or icons.get(spells.rows.get(ranks[0],(0,)*234)[133],'')if ranks else ''
  asset=iconfiles.get(norm(path.split('\\')[-1]))
  icon=None
  if asset:
   name=norm(asset.stem)+'.blp';dest=out/'icons'/name;dest.parent.mkdir(exist_ok=True);blob=asset.read_bytes();dest.write_bytes(blob)
   if blob[:4]not in (b'BLP1',b'BLP2'):raise ValueError('Invalid BLP '+str(asset))
   icon='Interface\\AddOns\\HeroFreePick\\Art\\AscensionTalents\\'+name[:-4]
   assets[name]={'source':path,'sha256':digest(asset),'file':name}
  descriptions=[]
  for sid in ranks:
   text,tokens=render(spells,sid,tables)
   descriptions.append({'spell':sid,'text':text,'raw':spells.text(spells.rows[sid][170])if sid in spells.rows else '', 'unresolved':tokens})
  rec={'sourceID':id,'name':q['Name'],'class':q['Class'],'spec':q.get('Tab','All'),'kind':kind,'ranks':ranks,'ap':r[14],'tp':r[15],'quality':adv.text(r[16]),'gems':r[17],'level':r[26],'row':r[31],'column':r[30],'sourceMetadata':q,'rawAdvancementFields':list(r),'matches':sorted(matches),'matchMethod':method,'functionCandidates':function_candidates,'icon':icon,'sourceIcon':path,'descriptions':descriptions,'importID':27000000+id,'serverPending':True,'status':'matched'if matches else 'review-function'if function_candidates else 'new','serverImplemented':False}
  # Confirmation is pinned to the complete reference data, never to a reused ID.
  rec['sourceTalentNodes']=[tid for tid,node in topology.items()if set(node['ranks'])&set(ranks)]
  rec['referenceHash']=hashlib.sha256(json.dumps({'ranks':descriptions,'spellRows':[spells.rows.get(s)for s in ranks]},sort_keys=True).encode()).hexdigest()
  rec['serverImplemented']=confirmed.get(str(id))==rec['referenceHash']
  records.append(rec)
  for target in matches:target_candidates[target].append(rec)
 overlays={};conflicts=[]
 for target,variants in sorted(target_candidates.items()):
  e=next(e for e in baseline if e['id']==target)
  # Prefer the exact established advancement identity, otherwise require identical reference content.
  exact=[v for v in variants if v['sourceID']in (target,e.get('talentOrigin'),e.get('area52Entry'))]
  choices=exact or variants
  unique={(tuple(v['ranks']),tuple(d['text']for d in v['descriptions']))for v in choices}
  if len(unique)>1:conflicts.append({'target':target,'sources':[v['sourceID']for v in choices]});continue
  v=min(choices,key=lambda v:v['sourceID']);ranks=[];changed=False
  for index,sid in enumerate(e['spells']):
   before,tokens=render(stock,sid,tables)
   desc=next((d for d in v['descriptions']if d['spell']==sid),None)
   if desc is None and index<len(v['descriptions']):desc=v['descriptions'][index]
   if not desc:ranks.append({'missingRank':True});continue
   different=plain(before)!=plain(desc['text']);changed|=different
   ranks.append({'text':desc['text'],'display':desc['text']if v['serverImplemented']else highlight(before,desc['text']),'changed':different,'unresolved':desc['unresolved'],'sourceSpell':desc['spell'],'stockText':before})
  overlays[target]={'sourceID':v['sourceID'],'name':v['name'],'icon':v['icon'],'ranks':ranks,'changed':changed,'serverImplemented':v['serverImplemented'],'referenceHash':v['referenceHash'],'rankCountChanged':len(e['spells'])!=len(v['ranks'])}
 # Retain transitive trigger dependencies plus full raw records for later server work.
 queue=list(required);dependencies={};missing=[]
 while queue:
  sid=queue.pop()
  if sid in dependencies:continue
  row=spells.rows.get(sid)
  if not row:missing.append(sid);continue
  dependencies[sid]={'name':spells.text(row[136]),'description':spells.text(row[170]),'rankText':spells.text(row[153]),'auraDescription':spells.text(row[187]),'iconID':row[133],'durationRecord':tables.get('SpellDuration',{}).get(row[40]),'rangeRecord':tables.get('SpellRange',{}).get(row[46]),'radiusRecords':[tables.get('SpellRadius',{}).get(row[92+i])for i in range(3)],'rawFields':list(row),'stockExists':sid in stock.rows,'effects':[{'effect':row[71+i],'basePoints':signed(row[80+i]),'aura':row[95+i],'triggerSpell':row[116+i],'miscValue':signed(row[110+i]),'miscValueB':signed(row[113+i])}for i in range(3)]}
  raw_description=spells.text(row[170])+' '+spells.text(row[187])
  referenced=set(row[116:119])|set(row[24:28])
  referenced.update(int(x)for x in re.findall(r'\$(\d+)[a-zA-Z]',raw_description)if x)
  referenced.update(int(value)for pair in re.findall(r'@s:(\d+):|\$\?s(\d+)',raw_description)for value in pair if value)
  referenced.discard(0);dependencies[sid]['referencedSpells']=sorted(referenced)
  for child in referenced:
   if child not in dependencies:queue.append(child)
 report={'sourceHashes':{Path(p).name:digest(p)for p in [args.advancement,args.spells,args.stock_spells,args.metadata,args.baseline,*lookupfiles]},'records':records,'conflicts':conflicts,'skipped':skipped,'assets':list(assets.values()),'missingDependencies':sorted(set(missing)),'dependencyCount':len(dependencies),'limitations':['DBC effects do not include server-side scripts, proc conditions, SQL dependencies or confirmed behavior.','Exact spell IDs and name matches preserve connectors; they do not prove equivalent behavior.','Unresolved tooltip formulas remain explicit reference text.','New talents are staged separately until tree placement and server mappings are reviewed.']}
 (out/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 if talent_db:
  report['sourceHashes']['Talent.dbc']=digest(args.talents)
  (out/'talent-topology.json').write_text(json.dumps(topology,indent=2)+'\n')
  (out/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 (out/'tooltip-changes.json').write_text(json.dumps(overlays,indent=2)+'\n',encoding='utf8')
 (out/'server-effects.json').write_text(json.dumps(dependencies,indent=2)+'\n',encoding='utf8')
 new=[v for v in records if v['status']!='matched']
 code='-- Generated by tools/talents/import_area52_talents.py; presentation data only.\nHeroAscensionTalentReferences='+lua(overlays)+'\nHeroAscensionNewTalents='+lua(new)+'\n'
 (out/'AscensionTalentData.lua').write_text(code,encoding='utf8')
 counts=collections.Counter(v['status']for v in records)
 summary=['# Area 52 talent comparison','',f"Reviewed {len(records)} visible standard-class source records: {dict(counts)}.",f"{len(overlays)} existing catalogue entries mapped; {sum(v['changed']for v in overlays.values())} have changed descriptions; {len(conflicts)} unresolved target conflicts.",f"{len(assets)} icons packaged; {sum(not v['icon']for v in records)} records lack a packaged icon; {sum(bool(d['unresolved'])for v in records for d in v['descriptions'])} rank descriptions retain unresolved formulas.",'','Existing IDs, spell lists, ranks, costs, prerequisites, server mappings and connectors are not rewritten. Yellow text marks changed reference wording until a matching reference hash is confirmed. New records are imported into a staging registry, not inserted into guessed tree positions.','','Detailed rank-by-rank old/new descriptions are in `tooltip-changes.json`; full source evidence is in `review.json` and `server-effects.json`.','','## New or function-only candidates','','| Source ID | Class | Talent | Status | Level |','|---|---|---|---|---|']
 summary +=[f"| {v['sourceID']} | {v['class']} | {v['name']} | {v['status']} | {v['level']} |"for v in new]
 summary+=['','## Changed existing entries','','| Entry | Current name | Area 52 name | Source |','|---|---|---|---|']
 names={e['id']:e['name']for e in baseline}
 summary +=[f"| {id} | {names[id]} | {v['name']} | {v['sourceID']} |"for id,v in overlays.items()if v['changed']]
 (out/'REPORT.md').write_text('\n'.join(summary)+'\n',encoding='utf8')
 if args.install_addon:install(out,Path(args.install_addon))
 print('\n'.join(summary[2:5]))
 return report,overlays

def install(out,addon):
 """Idempotent presentation-only installation; strict anchors refuse unfamiliar UI versions."""
 ui=addon/'HeroFreePick.lua';toc=addon/'HeroFreePick.toc';text=ui.read_text()
 icon_anchor="local function icon(e)\n"
 icon_patch=" if A.AscensionTalentIcon then local ref=A.AscensionTalentIcon(e);if ref then return ref end end\n"
 description_anchor=" local description=A.mode~='Classic'and(e.referenceDescription or(A.SummoningDescriptions and A.SummoningDescriptions[id]))"
 description_patch=" if A.AscensionTalentDescription then description=A.AscensionTalentDescription(e,rank)or description end"
 notes_anchor=" GameTooltip:AddLine(' ');GameTooltip:AddLine(e.class"
 notes_patch=" if A.AddAscensionTalentNotes then A.AddAscensionTalentNotes(e,rank)end\n"
 if icon_patch not in text:
  if text.count(icon_anchor)!=1:raise ValueError('Unrecognized icon hook; no files installed')
  text=text.replace(icon_anchor,icon_anchor+icon_patch)
 if description_patch not in text:
  if text.count(description_anchor)!=1:raise ValueError('Unrecognized tooltip hook; no files installed')
  text=text.replace(description_anchor,description_anchor+'\n'+description_patch)
 if notes_patch not in text:
  if text.count(notes_anchor)!=1:raise ValueError('Unrecognized tooltip notes hook; no files installed')
  text=text.replace(notes_anchor,notes_patch+notes_anchor)
 toc_text=toc.read_text();anchor='AscensionAbilities.lua\n'
 if 'AscensionTalentData.lua'not in toc_text:
  if toc_text.count(anchor)!=1:raise ValueError('Unrecognized TOC; no files installed')
  toc_text=toc_text.replace(anchor,anchor+'AscensionTalentData.lua\nAscensionTalentOverlay.lua\n')
 # Backups are output artifacts, deliberately outside the published addon.
 backup=out/'pre-import-backup';backup.mkdir(exist_ok=True)
 for src in [ui,toc]:
  if not(backup/src.name).exists():shutil.copyfile(src,backup/src.name)
 shutil.copyfile(out/'AscensionTalentData.lua',addon/'AscensionTalentData.lua')
 shutil.copyfile(Path(__file__).with_name('AscensionTalentOverlay.lua'),addon/'AscensionTalentOverlay.lua')
 shutil.copytree(out/'icons',addon/'Art/AscensionTalents',dirs_exist_ok=True)
 ui.write_text(text);toc.write_text(toc_text)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['advancement','spells','stock-spells','metadata','baseline','tables','icon-dbcs','icons','output']:p.add_argument('--'+name,required=True)
 p.add_argument('--talents',help='Optional Area 52 Talent.dbc to retain source node/prerequisite topology')
 p.add_argument('--install-addon',help='Optional addon directory; only installs presentation metadata/hooks, never server spells')
 p.add_argument('--confirmed');p.add_argument('--matches');run(p.parse_args())
