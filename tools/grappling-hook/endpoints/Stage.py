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
        key=next(n for n in files if n.replace(chr(92),'/').lower()=='dbfilesclient/spellvisual.dbc')
        old=files[key];raw=bytearray(old);magic,n,f,z,strings=struct.unpack_from('<4s4I',raw)
        assert magic==b'WDBC' and f==32 and z==128
        hits=0
        for i in range(n):
            offset=20+i*z
            if struct.unpack_from('<I',raw,offset)[0]!=22086:continue
            hits+=1
            assert struct.unpack_from('<I',raw,offset+8)[0]==0
            kit=struct.unpack_from('<I',raw,offset+16)[0];assert kit==15706
            struct.pack_into('<I',raw,offset+8,kit) # CastKit: caster toward explicit target
            struct.pack_into('<I',raw,offset+16,0) # no target-side persistent chain
        assert hits==1
        files[key]=bytes(raw)
        changed=[i for i,(a,b) in enumerate(zip(old,raw)) if a!=b]
        assert len(changed)==4
        dest=HERE/'client-candidate'/rel;dest.parent.mkdir(parents=True,exist_ok=True);write_archive(dest,files)
        with MPQArchive(dest) as a:
            assert all(a.read_file(n)==b for n,b in files.items())
        assert sha(source)==before
        manifest[rel]={'before':before,'after':sha(dest)}
    (HERE/'client-manifest.json').write_text(json.dumps(manifest,indent=2))
    print('ENDPOINT VISUAL TEST STAGED. Only owned visual CastKit/PersistentKit changed. No server changes.')
if __name__=='__main__':main()
