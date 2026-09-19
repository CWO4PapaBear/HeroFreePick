#!/usr/bin/env python3
"""Stage verified icon DBC additions/assets without editing the installed client."""
import argparse,hashlib,json,struct
from pathlib import Path
from stage_auxiliary_dbc import parse
ROOT=Path(__file__).resolve().parent

def build(blob,icons):
 fields,stride,rows,strings=parse(blob)
 if stride!=8:raise ValueError('Expected 2-field SpellIcon.dbc')
 known={r[0]:r for r in rows};tail=bytearray(strings);add=[]
 for sid,v in sorted(icons.items(),key=lambda x:int(x[0])):
  sid=int(sid);path='HeroAdvancement\\'+v['dbcPath'].replace('/','\\')
  if sid in known:
   off=known[sid][1];old=strings[off:strings.index(b'\0',off)].decode()
   if old.lower()!=path.lower():raise ValueError('Icon ID collision: '+str(sid))
   continue
  add.append([sid,len(tail)]);tail.extend(path.encode()+b'\0')
 result=struct.pack('<4s4I',b'WDBC',len(rows)+len(add),fields,8,len(tail))+blob[20:20+8*len(rows)]+b''.join(struct.pack('<II',*r)for r in add)+tail
 return result,[r[0]for r in add]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Output directory must be new')
 icons=json.loads((ROOT/'data/resolved-icons.json').read_text());blobs={}
 for v in icons.values():
  rel=Path(v['file'])
  if rel.is_absolute()or '..'in rel.parts:raise ValueError('Unsafe path')
  b=(ROOT/'icon-assets'/rel).read_bytes()
  if hashlib.sha256(b).hexdigest()!=v['sha256']or b[:4]not in (b'BLP1',b'BLP2'):raise ValueError('Icon integrity check failed')
  blobs[v['file']]=b
 before=a.input.read_bytes();after,ids=build(before,icons);a.output.mkdir(parents=True)
 for path,b in blobs.items():
  dest=a.output/'HeroAdvancement'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 (a.output/'DBFilesClient').mkdir();(a.output/'DBFilesClient/SpellIcon.dbc').write_bytes(after)
 (a.output/'manifest.json').write_text(json.dumps({'addedIconIDs':ids,'assetCount':len(blobs),'beforeSHA256':hashlib.sha256(before).hexdigest(),'afterSHA256':hashlib.sha256(after).hexdigest(),'status':'Staged; no installed client files modified. Merge into the final client patch after collision checks.'},indent=2)+'\n')
 print('Staged',len(ids),'icon records and',len(blobs),'verified BLP files')
if __name__=='__main__':main()
