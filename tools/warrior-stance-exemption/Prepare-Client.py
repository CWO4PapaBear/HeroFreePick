"""Build and verify matching client MPQs without modifying the installed client."""
from pathlib import Path
import hashlib,json,sys
import Prepare as P
HERE=P.HERE
sys.path.insert(0,str(HERE.parents[1]/'work/github-upload/tools'))
from lib.mpq import MPQArchive,write_archive
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest={}
    for rel in ('Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'):
        src=CLIENT/rel;before=sha(src)
        with MPQArchive(src) as archive:
            names=archive.read_file('(listfile)').decode('utf-8').splitlines()
            files={n:archive.read_file(n) for n in names if n!='(listfile)'}
        keys=[n for n in files if n.replace('\\','/').lower()=='dbfilesclient/spell.dbc'];assert len(keys)==1
        key=keys[0];old=files[key];files[key]=P.transform(old)
        # Retain each client's own descriptions/imports; change only the reviewed fields.
        orig,_=P.read_dbc(old);changed,_=P.read_dbc(files[key]);changed={r[0]:r for r in changed}
        for r in orig:
            assert [i for i,(x,y) in enumerate(zip(r,changed[r[0]])) if x!=y]==([211] if r[0] in P.RANKS else [])
        dst=HERE/'client-candidate'/rel;dst.parent.mkdir(parents=True,exist_ok=True)
        write_archive(dst,files)
        with MPQArchive(dst) as check:
            assert set(check.read_file('(listfile)').decode().splitlines())==set(names)
            for n,data in files.items():assert check.read_file(n)==data,n
        assert sha(src)==before,'Installed archive changed during staging'
        manifest[rel]=dict(before=before,after=sha(dst),spellBefore=P.sha(old),spellAfter=P.sha(files[key]))
    (HERE/'client-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('CLIENT STAGED: both MPQs verified entry-by-entry. Installed client unchanged.')
if __name__=='__main__':main()
