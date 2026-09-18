"""Read-only implementation audit. No server commands, imports, or gameplay mutations.
Requires lupa.lua51 for the existing repository harness; all other modules are stdlib.
"""
from pathlib import Path
import argparse,collections,contextlib,datetime,hashlib,html,importlib.util,io,json,re

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def plain(v):
 if hasattr(v,'items'):
  d=dict(v.items())
  if d and set(d)==set(range(1,len(d)+1)):return [plain(d[i])for i in range(1,len(d)+1)]
  return {str(k):plain(x)for k,x in d.items()if hasattr(x,'items')or not callable(x)}
 return v

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workspace',required=True);parser.add_argument('--output',required=True);args=parser.parse_args()
 ws=Path(args.workspace).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);repo=Path(__file__).resolve().parents[2];base=ws/'outputs/Hero_ClassPlus_All_Classes_Test'
 spec=importlib.util.spec_from_file_location('talent_import',repo/'tools/talents/import_area52_talents.py');imp=importlib.util.module_from_spec(spec);spec.loader.exec_module(imp)
 stock_path=ws/'work/regalia/dbc_sources/enUS_patch-enUS-3_Spell.dbc';area_path=ws/'work/area52-review/spell-extract/ascension-live_Data_area-52_patch-D.MPQ.Spell.dbc'
 stock=imp.DBC(stock_path,234);area=imp.DBC(area_path,234)
 setup=(repo/'test_ui.py').read_text().split('lua.execute("""',1)[0].replace("'Masteries.lua','AscensionAbilities.lua'","'Masteries.lua','StockAbilityLevels.lua','ProgressionRules.lua','AscensionAbilities.lua'")
 ctx={'__file__':str(repo/'test_ui.py')}
 with contextlib.redirect_stdout(io.StringIO()):exec(compile(setup,str(repo/'test_ui.py'),'exec'),ctx)
 lua=ctx['lua'];g=lua.globals();a=g.HeroFreePick
 lua.execute("UnitLevel=function()return 80 end;UnitClass=function()return 'Mage','MAGE'end;UnitRace=function()return 'Human','Human'end;UnitFactionGroup=function()return 'Alliance'end")
 for name in ['AscensionTalentData.lua','AscensionTalentOverlay.lua']:lua.execute((repo/'HeroFreePick'/name).read_text())
 catalog=json.loads((base/'catalog.json').read_text());supported={e['id']:e for e in catalog['entries']};excluded={e['id']:e['reason']for e in catalog['excluded']}
 history=(base/'all-class-test-complete.log').read_text();historical=set()
 for text in re.findall(r'entries=([0-9,]+)',history):historical.update(map(int,text.split(',')))
 for line in history.splitlines():
  parts=line.split('\t')
  if len(parts)==7 and re.fullmatch(r'[0-9,]+',parts[-1]):historical.update(map(int,parts[-1].split(',')))
 deployment=json.loads((base/'deployment.json').read_text());mismatches=[]
 for rel,digest in deployment['package'].items():
  p=base/'mod-hero-starting-path'/rel
  if not p.exists()or sha(p)!=digest:mismatches.append(rel)
 refs=plain(g.HeroAscensionTalentReferences);entries=[]
 groups=collections.defaultdict(list)
 for e in g.HeroFreePickCatalog.values():
  parent=e['requiredMastery']or e['requiredBundle']
  if parent:groups[int(parent)].append(int(e['id']))
 fields=[('attributes',range(1,28)),('cast_cooldown_interrupt',range(28,34)),('procs',range(34,37)),('native_levels',range(37,40)),('duration_power_range',range(40,50)),('reagents_equipment',range(50,71)),('effects_targets_masks',range(71,131)),('family_scaling_rules',range(204,234))]
 def spell_detail(sid,reference_sid=None):
  s=stock.rows.get(sid);ref=area.rows.get(reference_sid or sid);diff=[]
  if s and ref:
   for category,indices in fields:
    changes=[{'field':i,'stock':s[i],'reference':ref[i]}for i in indices if s[i]!=ref[i]]
    if changes:diff.append({'category':category,'changes':changes})
  return {'id':sid,'stockPresent':s is not None,'stockName':stock.text(s[136])if s else None,'referenceID':reference_sid or sid,'referencePresent':ref is not None,'referenceName':area.text(ref[136])if ref else None,'numericDifferences':diff,'nameConflict':bool(s and ref and stock.text(s[136]).casefold()!=area.text(ref[136]).casefold())}
 def inspect(e,staged=False,primary=False):
  id=e['id'];spells=e.get('spells',[]);c=supported.get(id);ref=refs.get(str(id),{});alias=e.get('canonicalID')!=id
  details=[]
  for i,sid in enumerate(spells):
   rd=(ref.get('ranks')or[]);source=rd[i].get('sourceSpell')if i<len(rd)else None
   if sid:details.append(spell_detail(sid,source))
  group=bool(e.get('isMastery')or e.get('isBundle'));runtime=(c['spells']if c and group else []if group else spells)
  missing=[sid for sid in runtime if sid and sid not in stock.rows]
  zero=0 in runtime
  mechanics=any(any(d['category']!='native_levels'for d in s['numericDifferences'])for s in details)
  text_changed=bool(ref.get('changed'));reference_pending=bool((text_changed or mechanics)and not ref.get('serverImplemented'))
  children=groups.get(id,[]);unsupported_members=[i for i in children if i not in supported]
  if staged:status='NEW_TALENT_STAGED';owner='Talent placement and custom effects'
  elif primary:status='PRIMARY_STAT_SYSTEM_PENDING';owner='Primary-stat entitlement and effects'
  elif alias:status='ALIAS_EXISTING_PURCHASE';owner='Use canonical entry'
  elif e.get('classicOnly'):status='CLASSIC_ONLY';owner='Native Classic progression'
  elif e.get('portalCity')or e.get('travelKind')or id in (21818045,21818046):status='TRAVEL_SYSTEM_PENDING';owner='Independent Mage travel'
  elif (e.get('isBundle')or e.get('requiredBundle'))and id not in supported:status='COMPANION_SYSTEM_PENDING';owner='More Minions'
  elif e.get('effectiveTalent'):
   status='TALENT_EFFECTS_AND_COMMIT_PENDING'if reference_pending or missing else 'TALENT_COMMIT_PENDING';owner='Talent transaction and effects'
  elif group:
   status=('GROUP_PARTIAL'if unsupported_members else 'GROUP_STOCK_GRANTS_SUPPORTED')if c else 'GROUP_ROUTE_PENDING';owner='Mastery/bundle grants'
  elif missing or zero:status='MISSING_STOCK_DEFINITION';owner='Spell definitions and custom effects'
  elif reference_pending:status='REFERENCE_BEHAVIOR_REVIEW';owner='Modified stock behavior review'
  elif c:status='STOCK_PURCHASE_PATH_SUPPORTED';owner='Regression verification'
  elif not any(m!='Classic'for m in e.get('visibleModes',[])):status='CLASSIC_OR_HIDDEN_REFERENCE';owner='Native progression/catalogue review'
  else:status='STOCK_PURCHASE_ROUTE_MISSING';owner='Purchase metadata and rules'
  blockers=[]
  if alias:blockers.append('Tree alias: resolve through canonical entry '+str(e['canonicalID'])+'; do not allocate a second spell or charge twice.')
  if missing:blockers.append('Referenced runtime IDs absent from the saved stock baseline; verify live overrides before allocating new IDs.')
  if zero:blockers.append('Placeholder spell 0 is not a castable spell.')
  if e.get('effectiveTalent'):blockers.append('Class+ talent ranks can be drafted, but server rank validation/commit/reset support is absent.')
  if reference_pending:blockers.append('Area 52 text and/or numeric fields differ. Existing stock purchase support does not implement those differences.')
  if unsupported_members:blockers.append('Group omits '+str(len(unsupported_members))+' catalogue members from current server grants.')
  if e.get('serverPending'):blockers.append('Interface explicitly marks this entry serverPending.')
  if ref.get('rankCountChanged'):blockers.append('Area 52 and current rank counts differ; preserve current ranks until a migration is designed.')
  if e.get('customServerRequired'):blockers.append('Custom server behavior explicitly required by interface.')
  if id in excluded:blockers.append(excluded[id])
  if c and not alias:
   if c['level']!=e.get('customLevel',c['level']):blockers.append('Interface/server unlock levels differ: '+str(e.get('customLevel'))+' versus '+str(c['level']))
   if c['ap']!=e.get('ae',c['ap']):blockers.append('Interface/server AP costs differ.')
   if c['gems']!=e.get('effectiveRarityCost',c['gems']):blockers.append('Interface/server rarity gem costs differ.')
   if c['rarity']!={'Normal':0,'Uncommon':1,'Rare':2,'Epic':3,'Legendary':4}.get(e.get('quality'),c['rarity']):blockers.append('Interface/server rarity types differ.')
   if c['parent']!=(e.get('requiredMastery')or e.get('requiredBundle')or 0):blockers.append('Interface/server controlling group differs.')
  result={**e,'status':status,'implementationOwner':owner,'stockPurchaseRoute':id in supported,'canonicalStockPurchaseRoute':e.get('canonicalID')in supported,'serverMetadata':c,'spellDetails':details,'runtimeSeedSpells':runtime,'missingStockRuntimeIDs':missing,'sourceWrapperIDs':spells if group else [],'referenceTextChanged':text_changed,'referenceNumericChanged':mechanics,'referenceImplemented':bool(ref.get('serverImplemented')),'referenceSourceID':ref.get('sourceID'),'rankCountChanged':bool(ref.get('rankCountChanged')),'unsupportedMembers':unsupported_members,'historicalCommitObserved':id in historical,'evidenceScope':'Historical representative commits only; no per-effect proof or fresh live SpellMgr query.','blockers':blockers,'staged':staged,'primaryStat':primary,'modeCommitSupport':{'Classic':'native talent commit'if e.get('nativeTalent')else 'native progression; custom entries excluded','ClassPlus':'canonical ability route'if e.get('canonicalID')in supported else 'not implemented for this entry','Hybrid':'no authoritative commit implementation','Hero':'no authoritative commit implementation'}}
  entries.append(result)
 for le in g.HeroFreePickCatalog.values():
  e=plain(le);e['effectiveRarityCost']=0 if e['quality']=='Normal'else int(g.HeroRarityCosts[e['id']]if g.HeroRarityCosts[e['id']]is not None else 1);a.mode='ClassPlus';canonical=a.AbilityForTalent(le);e['canonicalID']=canonical['id'];e['effectiveTalent']=bool(a.IsTalent(canonical));e['customLevel']=int(a.TalentRequiredLevel(le)if a.IsTalent(canonical)else a.AbilityDisplayLevel(canonical));e['visibleModes']=[]
  for mode in ['Classic','ClassPlus','Hybrid','Hero']:
   a.mode=mode;visible=False
   for faction in ['Alliance','Horde']:
    lua.globals().auditFaction=faction;lua.execute("UnitFactionGroup=function()return auditFaction end")
    if a.EntryAvailableInMode(le):visible=True
   if visible:e['visibleModes'].append(mode)
  # Native tree aliases remain reachable through their tree node, not Results().
  e['treeReachable']=bool(e.get('nativeTalent'));inspect(e)
 for stat,value in a.PrimaryStats.items():
  e=plain(value);inspect({'id':'primary-'+stat,'canonicalID':'primary-'+stat,'name':'Primary Stat: '+stat,'class':'All','kind':'PrimaryStat','spells':[e['spell']],'bonuses':e.get('bonuses',[]),'visibleModes':['ClassPlus','Hybrid','Hero']},primary=True)
 for raw in g.HeroAscensionNewTalents.values():
  v=plain(raw);inspect({'id':v['importID'],'canonicalID':v['importID'],'sourceID':v['sourceID'],'name':v['name'],'class':v['class'],'spec':v['spec'],'kind':v['kind'],'spells':v['ranks'],'ae':v['ap'],'te':v['tp'],'quality':v['quality'],'level':v['level'],'customLevel':v['level'],'serverPending':True,'sourceTalentNodes':v.get('sourceTalentNodes',[]),'visibleModes':[]},staged=True)
 assert len({e['id']for e in entries})==len(entries)
 counts=collections.Counter(e['status']for e in entries);active=[e for e in entries if not e['staged']and not e['primaryStat']]
 metadata_drift=[e for e in entries if any('Interface/server'in b for b in e['blockers'])]
 result={'generatedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'interfaceVersion':re.search(r'## Version: (.+)',(repo/'HeroFreePick/HeroFreePick.toc').read_text())[1],'scope':'Every current catalogue entry, native tree aliases, four primary-stat choices, and separately staged Area 52 talents. Both factions considered at level 80; eligibility remains mode/class/race/level dependent.','liveServerQueried':False,'deploymentRecordPhase':deployment['phase'],'deploymentModuleHashMismatches':mismatches,'serverCatalogVersion':catalog['version'],'historicalCatalogVersions':[118119328],'sources':{str(p.relative_to(ws)):{'sha256':sha(p)}for p in [stock_path,area_path,base/'catalog.json',base/'deployment.json',base/'all-class-test-complete.log',repo/'HeroFreePick/AscensionTalentData.lua',repo/'HeroFreePick/Catalog.lua',repo/'HeroFreePick/Masteries.lua',repo/'HeroFreePick/ProgressionRules.lua']},'summary':dict(counts),'entryCount':len(entries),'currentCatalogueCount':len(active),'primaryStatCount':4,'stagedRecordCount':len(entries)-len(active)-4,'metadataDriftCount':len(metadata_drift),'orphanServerEntries':sorted(set(supported)-{e['id']for e in entries}),'records':entries,'limitations':['A stock DBC record is evidence of baseline presence, not proof of behavior on the running server.','Numeric differences flag work for review; unused fields or equivalent IDs can differ without a gameplay change.','Historical purchase/login logs validate representative transaction paths, not every spell rank, proc or effect.','Hybrid/Hero authoritative commit implementations remain absent; Classic uses native progression.','Rune-derived 160-portal/160-teleport design is tracked separately from the smaller currently imported city catalogue.','Higher ranks discovered through live spell_ranks/SpellMgr require a live database check; this inventory covers explicit interface spell references.','No server/client gameplay files are changed by this audit.']}
 (out/'implementation-catalogue.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
 spell_ids=sorted({s['id']for e in entries for s in e['spellDetails']})
 missing_catalog={}
 for e in entries:
  for sid in e['missingStockRuntimeIDs']:
   ref=area.rows.get(sid);item=missing_catalog.setdefault(sid,{'spell':sid,'referenceName':area.text(ref[136])if ref else None,'entries':[]})
   item['entries'].append({'id':e['id'],'name':e['name'],'staged':e['staged']})
 (out/'missing-spells.json').write_text(json.dumps(list(missing_catalog.values()),indent=2)+'\n')
 (out/'spell-ids.json').write_text(json.dumps(spell_ids)+'\n')
 report=['# Hero Advancement server implementation audit','',f"Interface {result['interfaceVersion']}; recorded server catalogue {catalog['version']}.",'',f"Audited **{len(active)} current catalogue entries**, **4 primary-stat choices**, and **{result['stagedRecordCount']} staged talent records**. Catalogue entries include aliases and group members; these are not counts of unique spells.",'','This is a read-only audit of saved stock/Area 52 DBCs, current module code, the recorded deployment and historical test results. **No fresh live server query was possible in this session.** No entry is labelled fully gameplay-verified merely because its spell ID exists.','',f"The local deployed-module mirror {'matches'if not mismatches else 'DOES NOT match'} all hashes in the latest deployment record. This establishes artifact consistency, not current process/database state.",'','## Classification','','| Status | Entries |','|---|---:|']
 report +=[f'| {k} | {v} |'for k,v in sorted(counts.items())]
 report+=['','## Findings','',f"- {len(supported)} server catalogue entries have a Class+ stock-grant path ({sum(not e['parent']for e in supported.values())} purchasable roots and {sum(bool(e['parent'])for e in supported.values())} free members). This does not prove their Area 52 effects are implemented.",f"- {sum(e['effectiveTalent']for e in active)} catalogue talent entries require the custom talent transaction path; Classic still uses native talent application.",f"- {sum(e['referenceTextChanged']for e in entries)} entries carry changed Area 52 tooltip text; changes must be implemented or explicitly reconciled before clearing yellow markers.",f"- {len({sid for e in entries for sid in e['missingStockRuntimeIDs']})} distinct required/preview spell IDs are absent from the stock baseline. Group-only reference IDs are excluded from this count when the server uses an entitlement instead.",f"- {len(metadata_drift)} interface/server level, AP, rarity or controlling-group discrepancies were found.",'','## Recommended implementation order','','1. Add server-authoritative talent rank transactions, removals/reset pricing and persistent recovery. Resolve existing aliases; do not duplicate AP-priced talent abilities.','2. Resolve ID/name conflicts and Area 52 effect changes before treating current stock purchases as matching the new descriptions.','3. Implement missing ordinary spells and rank chains in reviewed groups, including client records where absent.','4. Complete Mastery members, primary-stat mechanics, More Minions, independent Mage travel and DK-specific resources.','5. Implement Hybrid/Hero ownership and class-access rules on the server, followed by per-effect gameplay verification.','','Use `AUDIT.html` to filter every entry and inspect its blockers. `implementation-catalogue.json` retains field-level evidence and mode scope.','','## Incomplete groups','','| Group | Omitted catalogue members |','|---|---|']
 report +=[f"| {e['name']} ({e['id']}) | {', '.join(map(str,e['unsupportedMembers']))} |"for e in entries if e['unsupportedMembers']]
 report+=['','## Class breakdown','','Counts below exclude aliases from talent work; missing definitions are entry counts, not unique spell IDs.','','| Class | Passive talent commit work | Missing-definition entries | Reference review entries | Staged records |','|---|---:|---:|---:|---:|']
 for klass in sorted({e['class']for e in entries}):
  subset=[e for e in entries if e['class']==klass]
  report.append('| '+klass+' | '+' | '.join(str(sum(predicate(e)for e in subset))for predicate in [lambda e:e.get('effectiveTalent',False),lambda e:e['status']=='MISSING_STOCK_DEFINITION',lambda e:e['status']=='REFERENCE_BEHAVIOR_REVIEW',lambda e:e['staged']])+' |')
 report+=['','## Metadata differences','','| Entry | Findings |','|---|---|']+[f"| {e['name']} ({e['id']}) | {'; '.join(b for b in e['blockers']if 'Interface/server'in b)} |"for e in metadata_drift]
 (out/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf8')
 data=json.dumps(entries,ensure_ascii=False).replace('<','\\u003c')
 page='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Hero Advancement implementation audit</title><style>body{font:15px system-ui;margin:30px;background:#161a20;color:#e9edf2}h1{margin-bottom:8px}p{max-width:1100px;color:#bdc7d3}input,select{padding:10px;margin:5px;background:#252d38;color:white;border:1px solid #596777;border-radius:5px}table{border-collapse:collapse;width:100%;margin-top:20px}th,td{text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid #39414c}th{position:sticky;top:0;background:#252d38}.warning{color:#ffd965}summary{cursor:pointer}pre{white-space:pre-wrap;max-width:900px;font-size:12px}a{color:#89c8ff}</style><h1>Hero Advancement — server implementation audit</h1><p>Saved-data and source-code audit. Stock presence and purchase support do not prove that Area 52 effects work. No live server query. Staged talents are not active tree nodes.</p><p><a href="REPORT.md">Summary report</a> · <a href="implementation-catalogue.json">Complete evidence</a></p><input id="query" placeholder="Search name, ID, spell or blocker" size="42"><select id="klass"><option value="">All classes</option></select><select id="status"><option value="">All classifications</option></select><select id="scope"><option value="">All entries</option><option value="staged">Staged only</option><option value="active">Current catalogue only</option><option value="supported">Stock purchase path</option><option value="changed">Changed reference behavior/text</option></select><p id="count"></p><table><thead><tr><th>Entry</th><th>Class / kind</th><th>Classification</th><th>Evidence and blockers</th></tr></thead><tbody id="rows"></tbody></table><script>const data=DATA;const $=id=>document.getElementById(id);for(const [id,key]of [['klass','class'],['status','status']])for(const v of [...new Set(data.map(x=>x[key]))].sort()){$(id).add(new Option(v,v));}function td(tr,text){let d=document.createElement('td');d.textContent=text;tr.append(d);return d;}function render(){let q=$('query').value.toLowerCase();let filtered=data.filter(e=>(!$('klass').value||e.class===$('klass').value)&&(!$('status').value||e.status===$('status').value)&&(!q||JSON.stringify(e).toLowerCase().includes(q))&&(!$('scope').value||({'staged':e.staged,'active':!e.staged&&!e.primaryStat,'supported':e.stockPurchaseRoute,'changed':e.referenceTextChanged||e.referenceNumericChanged})[$('scope').value]));$('count').textContent=filtered.length+' of '+data.length+' entries';$('rows').replaceChildren();for(const e of filtered){let tr=document.createElement('tr');td(tr,e.name+' ['+e.id+']');td(tr,e.class+' / '+e.kind);td(tr,e.status);let cell=td(tr,'');let p=document.createElement('p');p.textContent=e.blockers.join(' ')||'No additional blocker identified in saved data; live effect verification remains required.';if(e.blockers.length)p.className='warning';cell.append(p);let details=document.createElement('details');let s=document.createElement('summary');s.textContent='Inspect IDs, ranks, modes and field differences';let pre=document.createElement('pre');pre.textContent=JSON.stringify(e,null,2);details.append(s,pre);cell.append(details);$('rows').append(tr);}}for(const id of ['query','klass','status','scope'])$(id).addEventListener('input',render);render();</script></html>'''.replace('DATA',data)
 (out/'AUDIT.html').write_text(page,encoding='utf8')
 print(json.dumps({'entries':len(entries),'current':len(active),'classifications':counts,'metadataDrift':len(metadata_drift),'moduleHashMismatches':mismatches},indent=2))
if __name__=='__main__':main()
