#!/usr/bin/env python3
"""Stage isolated visual DBC clones/assets; no installed files are written."""
import argparse,copy,hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREFIX='HeroAdvancement\\'
TABLES=['SpellVisual','SpellVisualKit','SpellVisualEffectName','SpellVisualKitModelAttach','SpellMissileMotion','SoundEntries','SoundEntriesAdvanced','SpellChainEffects']

def path_key(s):return s.replace('/','\\').lower()
def isolate(s):return PREFIX+s.replace('/','\\')
def dbc(blob):
 magic,n,f,z,l=struct.unpack_from('<4s4I',blob)
 if magic!=b'WDBC' or len(blob)!=20+n*z+l:raise ValueError('Invalid DBC')
 rows={struct.unpack_from('<I',blob,20+i*z)[0]:blob[20+i*z:20+(i+1)*z] for i in range(n)}
 if len(rows)!=n:raise ValueError('Duplicate IDs')
 return f,z,rows,blob[20+n*z:]

def build(reference,baselines,assets):
 ref=copy.deepcopy(reference);maps={};parsed={t:dbc(baselines[t])for t in TABLES}
 for t in TABLES:
  source=ref[t];existing=parsed[t][2];mapping={}
  if t=='SpellVisual':
   for i in source:
    if int(i) in existing:raise ValueError('Visual ID collision '+i)
    mapping[int(i)]=int(i)
  else:
   start=max(existing,default=0)+1
   for j,i in enumerate(sorted(map(int,source))):mapping[i]=start+j
  maps[t]=mapping
 def remap(t,i):
  if not i:return 0
  if i not in maps[t]:raise ValueError('Unresolved '+t+' '+str(i))
  return maps[t][i]
 additions={t:[] for t in TABLES}
 for t in TABLES:
  for key,record in ref[t].items():
   sid=int(key);texts={}
   if t=='SpellChainEffects':raw=bytearray.fromhex(record['hex']);texts={int(i):v for i,v in record['strings'].items()};texts[28]=isolate(texts[28]) if texts[28] else '';struct.pack_into('<I',raw,0,remap(t,sid))
   else:
    row=list(record['rawFields'] if isinstance(record,dict) else record);row[0]=remap(t,sid)
    if isinstance(record,dict):texts={4*int(i):v for i,v in record.get('strings',{}).items()}
    if t=='SpellVisual':
     for i in [1,2,3,4,5,6,14,15,22,23,24,25]:row[i]=remap('SpellVisualKit',row[i])
     row[8]=remap('SpellVisualEffectName',row[8]);row[21]=remap('SpellMissileMotion',row[21])
     for i in [11,12]:row[i]=remap('SoundEntries',row[i])
    elif t=='SpellVisualKit':
     for i in range(3,15):row[i]=remap('SpellVisualEffectName',row[i])
     row[15]=remap('SoundEntries',row[15])
     if row[16]:raise ValueError('Unresolved camera shake')
     for slot in range(4):
      if row[17+slot]==0:
       old=int(struct.unpack('<f',struct.pack('<I',row[21+slot]))[0])
       if old:row[21+slot]=struct.unpack('<I',struct.pack('<f',remap('SpellChainEffects',old)))[0]
    elif t=='SpellVisualEffectName':texts={4:record['name'],8:isolate(record['model'].replace('.mdx','.m2').replace('.MDX','.m2')) if record['model'] else ''}
    elif t=='SpellVisualKitModelAttach':row[1]=remap('SpellVisualKit',row[1]);row[2]=remap('SpellVisualEffectName',row[2])
    elif t=='SoundEntries':row[29]=remap('SoundEntriesAdvanced',row[29]);texts[23*4]=isolate(texts[23*4])
    elif t=='SoundEntriesAdvanced':row[1]=remap('SoundEntries',row[1])
    raw=bytearray(struct.pack('<'+'I'*len(row),*row))
   additions[t].append((raw,texts))
 outputs={};report={}
 for t in TABLES:
  f,z,old,strings=parsed[t];tail=bytearray(strings);new=[]
  for raw,texts in additions[t]:
   if len(raw)!=z:raise ValueError('Row width mismatch '+t)
   for offset,text in texts.items():struct.pack_into('<I',raw,offset,len(tail));tail.extend(text.encode()+b'\0')
   new.append(bytes(raw))
  before=baselines[t];n=len(old)
  result=struct.pack('<4s4I',b'WDBC',n+len(new),f,z,len(tail))+before[20:20+n*z]+b''.join(new)+tail
  assert result[20:20+n*z]==before[20:20+n*z]
  outputs['DBFilesClient/'+t+'.dbc']=result;report[t]={'added':len(new),'beforeSHA256':hashlib.sha256(before).hexdigest(),'afterSHA256':hashlib.sha256(result).hexdigest(),'mapping':maps[t]}
 # Rewrite embedded texture strings in WotLK M2 files into the isolated asset namespace.
 for path,blob in assets.items():
  data=bytearray(blob)
  if path.lower().endswith('.m2'):
   if data[:4]!=b'MD20' or struct.unpack_from('<I',data,4)[0]!=264:raise ValueError('Unsupported M2 '+path)
   count,offset=struct.unpack_from('<II',data,80)
   if offset+count*16>len(data):raise ValueError('Bad texture array')
   for i in range(count):
    at=offset+i*16;typ,flags,n,pos=struct.unpack_from('<4I',data,at)
    if typ==0 and n:
     if pos+n>len(data):raise ValueError('Bad texture name')
     name=data[pos:pos+n].rstrip(b'\0').decode()
     if path_key(name) not in {path_key(k)for k in assets}:raise ValueError('Missing model texture '+name)
     value=isolate(name).encode()+b'\0';struct.pack_into('<II',data,at+8,len(value),len(data));data.extend(value)
  outputs[isolate(path).replace('\\','/')]=bytes(data)
 return outputs,report

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True,help='Actual client baseline DBC directory');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Output must be a new directory')
 ref=json.loads((ROOT/'data/resolved-visuals.json').read_text());assets={}
 for path,digest in ref['assetFiles'].items():
  f=Path(path)
  if f.is_absolute()or '..'in f.parts or ':' in path:raise ValueError('Unsafe path')
  b=(ROOT/'visual-assets'/f).read_bytes()
  if hashlib.sha256(b).hexdigest()!=digest:raise ValueError('Asset checksum mismatch')
  assets[path]=b
 baseline={t:(a.input/(t+'.dbc')).read_bytes()for t in TABLES}
 outputs,report=build(ref,baseline,assets)
 a.output.mkdir(parents=True)
 for name,b in outputs.items():
  p=a.output/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 (a.output/'manifest.json').write_text(json.dumps({'tables':report,'repairs':ref['repairs'],'audioRepairs':ref['audioRepairs'],'files':{p:hashlib.sha256(b).hexdigest()for p,b in outputs.items()},'status':'Staged client data only. Requires client runtime rendering validation; not installed.'},indent=2)+'\n')
 print('Staged',len(outputs),'files. Original client records retained; visual dependencies cloned.')
if __name__=='__main__':main()
