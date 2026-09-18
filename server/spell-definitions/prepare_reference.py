#!/usr/bin/env python3
"""Maintainer tool: create portable reference subset from supplied client DBC and live export."""
import argparse,base64,hashlib,json,re,struct,zipfile
from pathlib import Path
from convert import TEXT_FIELDS,FLOAT_FIELDS,SIGNED_FIELDS,field_index

class DBC:
    def __init__(self,path):
        self.path=Path(path);b=self.path.read_bytes()
        magic,n,fields,stride,size=struct.unpack_from('<4s4I',b)
        if magic!=b'WDBC' or stride%4 or len(b)!=20+n*stride+size:raise ValueError('Invalid DBC')
        self.rows={r[0]:list(r) for r in struct.iter_unpack('<'+'I'*(stride//4),b[20:20+n*stride])}
        self.strings=b[20+n*stride:];self.hash=hashlib.sha256(b).hexdigest()
    def text(self,offset):
        if not 0<=offset<len(self.strings):raise ValueError('Bad string offset')
        return self.strings[offset:self.strings.index(b'\0',offset)].decode('utf-8')

def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spells',type=Path,required=True);p.add_argument('--live-export',type=Path,required=True)
    p.add_argument('--missing',type=Path,required=True);p.add_argument('--tables',type=Path,required=True)
    p.add_argument('--icon-dbcs',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    db=DBC(a.spells)
    with zipfile.ZipFile(a.live_export) as z:
        live=json.loads(z.read('live-evidence.json'));b=z.read(next(n for n in z.namelist() if n.endswith('-Spell.dbc')))
    magic,n,fields,stride,size=struct.unpack_from('<4s4I',b)
    if magic!=b'WDBC' or stride!=936 or len(b)!=20+n*stride+size:raise ValueError('Invalid live DBC')
    existing={struct.unpack_from('<I',b,20+i*stride)[0] for i in range(n)}|{int(r['ID']) for r in live['tables']['spell_dbc']}
    roots=sorted({x['spell'] for x in json.loads(a.missing.read_text())}-{901018})
    if any(s not in db.rows for s in roots):raise ValueError('Missing source root')
    if set(roots)&existing:raise ValueError('Requested IDs already exist')
    queue=list(roots);records={};edges=[];unresolved=[]
    while queue:
        sid=queue.pop()
        if sid in records or sid==901018:continue
        if sid not in db.rows:unresolved.append(sid);continue
        row=db.rows[sid]
        if len(row)!=234:raise ValueError('Expected 234-field Spell.dbc')
        strings={str(i):db.text(row[i]) for i in TEXT_FIELDS}
        deps=[('trigger',v) for v in row[116:119] if v]+[('auraRequirement',v) for v in row[24:28] if v]
        for text in strings.values():
            deps += [('tooltip',int(m[0] or m[1])) for m in re.findall(r'\$(\d+)[A-Za-z]|@s:(\d+):',text)]
        deps=sorted(set(deps))
        records[sid]={'id':sid,'name':db.text(row[136]),'rawUInt32Fields':row,'localizedStrings':strings,'dependencies':[{'kind':k,'id':v,'presentInBaseline':v in existing} for k,v in deps]}
        edges.extend({'from':sid,'kind':k,'to':v,'presentInBaseline':v in existing} for k,v in deps)
        queue.extend(v for k,v in deps if v not in existing)
    schema=[]
    for i,c in enumerate(live['schemas']['spell_dbc']):
        name=c['COLUMN_NAME'];idx=field_index(name,i);t=c['DATA_TYPE']
        if (idx in TEXT_FIELDS)!=(t in ('varchar','text')) or (idx in FLOAT_FIELDS)!=(t=='float'):raise ValueError('Schema type mismatch '+name)
        limit=None
        if t=='varchar':limit=100 if idx<170 or name.endswith('_Unk') else 550
        schema.append({'name':name,'sourceField':idx,'dataType':t,'unsigned':idx not in SIGNED_FIELDS,'maxLength':limit})
    save(a.output/'schema.json',{'provenance':'Column names/order/data types from live export; signedness and varchar widths from AzerothCore base spell_dbc schema. Generated SQL rechecks these before writing.','upstreamSchema':'https://raw.githubusercontent.com/azerothcore/azerothcore-wotlk/master/data/sql/base/db_world/spell_dbc.sql','columns':schema})
    save(a.output/'spells.json',{'sourceSHA256':db.hash,'rootIDs':roots,'excludedIDs':[901018],'records':[records[s] for s in sorted(records)]})
    support={};needed={'SpellDuration':{r['rawUInt32Fields'][40] for r in records.values()},'SpellRange':{r['rawUInt32Fields'][46] for r in records.values()},'SpellRadius':{v for r in records.values() for v in r['rawUInt32Fields'][92:95]}}
    for table,ids in needed.items():
        file=a.tables/(table+'.dbc')
        if not file.exists():support[table]={'unavailable':True};continue
        d=DBC(file);found={str(i):d.rows[i] for i in sorted(ids) if i and i in d.rows}
        # Range has localized name offsets. Decode only referenced fields; no unrelated strings.
        texts={sid:{str(i):d.text(row[i]) for i in list(range(6,22))+list(range(23,39))} for sid,row in found.items()} if table=='SpellRange' else {}
        support[table]={'sourceSHA256':d.hash,'rows':found,'localizedStrings':texts,'missingIDs':sorted(ids-{0}-d.rows.keys())}
    iconids={v for r in records.values() for v in r['rawUInt32Fields'][133:135] if v};iconvariants={}
    for path in sorted(a.icon_dbcs.glob('*.dbc')):
        d=DBC(path)
        for sid in sorted(iconids&d.rows.keys()):
            iconvariants.setdefault(str(sid),[]).append({'path':d.text(d.rows[sid][1]),'source':path.name,'sourceSHA256':d.hash})
    save(a.output/'supporting-data.json',{'tables':support,'iconCandidates':iconvariants,'missingIconIDs':sorted(iconids-{int(x) for x in iconvariants}),'notPackaged':['Cast times','Visuals and their effect assets','Rune costs','Area groups','Creature/gameobject/item definitions','Ascension server scripts','Client patch'],'note':'Raw support rows and icon paths are reference data, not installed DBC records. Icon variants retain provenance; no load order is guessed.'})
    save(a.output/'dependencies.json',{'edges':edges,'unresolvedSpellIDs':sorted(set(unresolved)),'note':'Trace covers explicit trigger/aura requirement/tooltip references. Misc values, scripts, procs and auxiliary table dependencies require separate review.'})
    files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(a.output.glob('*.json')) if f.name!='manifest.json'}
    save(a.output/'manifest.json',{'formatVersion':1,'sourceName':a.spells.name,'sourceSHA256':db.hash,'liveDBC_SHA256':hashlib.sha256(b).hexdigest(),'rootCount':len(roots),'recordCount':len(records),'excludedIDs':[901018],'files':files})
    print('Packaged',len(roots),'roots and',len(records)-len(roots),'reference dependencies')
if __name__=='__main__':main()
