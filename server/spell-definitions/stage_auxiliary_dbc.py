#!/usr/bin/env python3
"""Stage append-only SpellRange/SpellRadius DBC additions. Never writes into input directory."""
import argparse,hashlib,json,struct,subprocess,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def parse(blob):
    magic,n,fields,stride,size=struct.unpack_from('<4s4I',blob)
    if magic!=b'WDBC' or stride%4 or len(blob)!=20+n*stride+size:raise ValueError('Invalid WDBC')
    rows=[list(r) for r in struct.iter_unpack('<'+'I'*(stride//4),blob[20:20+n*stride])]
    if len({r[0] for r in rows})!=len(rows):raise ValueError('Duplicate DBC IDs')
    return fields,stride,rows,blob[20+n*stride:]

def patch(blob,table,reference):
    fields,stride,rows,strings=parse(blob)
    expected=160 if table=='SpellRange' else 16
    if stride!=expected:raise ValueError('Unexpected '+table+' width')
    existing={r[0] for r in rows};added=[];newstrings=bytearray(strings)
    for key,row in sorted(reference['rows'].items(),key=lambda x:int(x[0])):
        if int(key) in existing:raise ValueError('ID already exists: '+key+'; review rather than overwrite')
        row=list(row)
        if len(row)*4!=stride or row[0]!=int(key):raise ValueError('Invalid reference row')
        if table=='SpellRange':
            texts=reference['localizedStrings'][key]
            for i in list(range(6,22))+list(range(23,39)):
                text=texts[str(i)]
                row[i]=len(newstrings);newstrings.extend(text.encode('utf-8')+b'\0')
        added.append(row)
    packed=b''.join(struct.pack('<'+'I'*len(r),*r) for r in added)
    result=struct.pack('<4s4I',b'WDBC',len(rows)+len(added),fields,stride,len(newstrings))+blob[20:20+len(rows)*stride]+packed+bytes(newstrings)
    _,_,check,st=parse(result)
    assert check[:len(rows)]==rows and st[:len(strings)]==strings
    return result,[r[0] for r in added]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--input',type=Path,help='Existing server or client DBC directory')
    g.add_argument('--docker-container',help='Read originals from a running container, without modifying it')
    p.add_argument('--docker-dbc-path',default='/azerothcore/env/dist/data/dbc')
    p.add_argument('--output',type=Path,required=True,help='New staging directory (must not exist)')
    p.add_argument('--reference',type=Path,default=ROOT/'data/auxiliary-additions.json')
    a=p.parse_args()
    if a.output.exists():raise ValueError('Output directory must be new')
    if a.docker_container and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',a.docker_container):raise ValueError('Invalid container name')
    reference=json.loads(a.reference.read_text());prepared={};report={};originals={}
    for table,ref in reference['tables'].items():
        if a.docker_container:
            before=subprocess.run(['docker','exec',a.docker_container,'cat','--',a.docker_dbc_path.rstrip('/')+'/'+table+'.dbc'],check=True,capture_output=True).stdout
        else:before=(a.input/(table+'.dbc')).read_bytes()
        originals[table]=before
        after,ids=patch(before,table,ref)
        prepared[table]=after;report[table]={'addedIDs':ids,'beforeSHA256':hashlib.sha256(before).hexdigest(),'afterSHA256':hashlib.sha256(after).hexdigest()}
    a.output.mkdir(parents=True)
    (a.output/'originals').mkdir()
    for table,blob in originals.items():(a.output/'originals'/(table+'.dbc')).write_bytes(blob)
    for table,blob in prepared.items():(a.output/(table+'.dbc')).write_bytes(blob)
    (a.output/'manifest.json').write_text(json.dumps({'tables':report,'status':'Staged only; original files unchanged. Icons, visuals and spell installation remain separate.'},indent=2)+'\n')
    print('Staged four DBC additions in '+str(a.output)+'; originals unchanged.')
if __name__=='__main__':main()
