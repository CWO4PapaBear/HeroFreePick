from pathlib import Path
import sys,struct,hashlib,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'work/github-upload/tools'))
from lib.mpq import MPQArchive,write_archive
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest={}
    for rel in ('Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'):
        source=CLIENT/rel;before=sha(source)
        with MPQArchive(source) as a:
            files={n:a.read_file(n) for n in a.read_file('(listfile)').decode().splitlines() if n!='(listfile)'}
        def update(table,id,edit):
            key=next(n for n in files if n.replace(chr(92),'/').lower()=='dbfilesclient/'+table.lower()+'.dbc')
            old=files[key];raw=bytearray(old);magic,n,f,z,strings=struct.unpack_from('<4s4I',raw)
            assert magic==b'WDBC'
            hits=0
            for i in range(n):
                offset=20+i*z
                if struct.unpack_from('<I',raw,offset)[0]!=id:continue
                hits+=1;beforeRow=bytes(raw[offset:offset+z]);row=bytearray(beforeRow);edit(row)
                raw[offset:offset+z]=row
                assert raw[:offset]==old[:offset] and raw[offset+z:]==old[offset+z:]
            assert hits==1;files[key]=bytes(raw)
        def kit(row):
            assert struct.unpack_from('<I',row,17*4)[0]==0
            assert struct.unpack_from('<f',row,21*4)[0]==1181
            # Native Drain Life/Mind Flay chain procedures use nonzero endpoint
            # parameters. Their exact semantics are not proven here: runtime test.
            for index in (25,29):
                assert struct.unpack_from('<f',row,index*4)[0]==0
                struct.pack_into('<f',row,index*4,1.0)
        def chain(row):
            assert struct.unpack_from('<I',row,32)[0]==449
            # Native Mind Flay chain 750 flags; preserve our chain texture/scale.
            struct.pack_into('<I',row,32,320)
        update('SpellVisualKit',15706,kit)
        update('SpellChainEffects',1181,chain)
        dest=HERE/'client-candidate'/rel;dest.parent.mkdir(parents=True,exist_ok=True);write_archive(dest,files)
        with MPQArchive(dest) as a:
            assert all(a.read_file(n)==b for n,b in files.items())
        assert sha(source)==before
        manifest[rel]={'before':before,'after':sha(dest)}
    (HERE/'client-manifest.json').write_text(json.dumps(manifest,indent=2))
    print('TRACKING EXPERIMENT STAGED. Two owned visual records changed; unrelated rows preserved. No server changes.')
if __name__=='__main__':main()
