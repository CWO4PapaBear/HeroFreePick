#!/usr/bin/env python3
"""Append filtered custom spell definitions to an existing client Spell.dbc."""
import argparse,hashlib,json,struct
from pathlib import Path
from convert import compatible_selection,TEXT_FIELDS
ROOT=Path(__file__).resolve().parent

def build(blob,records):
 magic,n,fields,stride,size=struct.unpack_from('<4s4I',blob)
 if magic!=b'WDBC' or fields!=234 or stride!=936 or len(blob)!=20+n*stride+size:raise ValueError('Unexpected Spell.dbc')
 original=blob[20:20+n*stride];existing={struct.unpack_from('<I',original,i*stride)[0] for i in range(n)}
 ids=[r['id']for r in records]
 if len(set(ids))!=len(ids)or existing&set(ids):raise ValueError('Spell ID collision')
 strings=bytearray(blob[20+n*stride:]);added=[]
 for r in sorted(records,key=lambda x:x['id']):
  row=list(r['rawUInt32Fields'])
  for i in sorted(TEXT_FIELDS):
   value=r['localizedStrings'][str(i)].encode()+b'\0';row[i]=len(strings);strings.extend(value)
  added.append(struct.pack('<234I',*row))
 return struct.pack('<4s4I',b'WDBC',n+len(added),234,936,len(strings))+original+b''.join(added)+strings

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Output already exists')
 ref=json.loads((ROOT/'data/spells.json').read_text());records,selection=compatible_selection(ref)
 before=a.input.read_bytes();after=build(before,records);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(after)
 print('Appended',len(records),'spell records; original records and strings preserved.')
if __name__=='__main__':main()
