"""Stage cumulative matching client archives/addon; installed client is read-only."""
from pathlib import Path
import json,sys,hashlib,struct
import Prepare as P
HERE=P.HERE
sys.path.insert(0,str(HERE.parents[1]/'work/github-upload/tools'))
from lib.mpq import MPQArchive,write_archive
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest={};out=HERE/'client-candidate'
    visual=json.loads((HERE/'visual-manifest.json').read_text())
    additions={n:(HERE/'visual-candidate'/n).read_bytes() for n in visual['files']}
    assert all(hashlib.sha256(b).hexdigest()==visual['files'][n] for n,b in additions.items())
    for rel in ('Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'):
        src=CLIENT/rel;before=sha(src)
        with MPQArchive(src) as archive:
            names=archive.read_file('(listfile)').decode('utf8').splitlines()
            files={n:archive.read_file(n) for n in names if n!='(listfile)'}
        keys=[n for n in files if n.replace('\\','/').lower()=='dbfilesclient/spell.dbc'];assert len(keys)==1
        original=dict(files)
        key=keys[0];old=files[key];files[key]=P.transform(old)
        iconKey=next(n for n in files if n.replace('\\','/').lower()=='dbfilesclient/spellicon.dbc')
        data=files[iconKey];magic,count,fields,size,strings=struct.unpack_from('<4s4I',data)
        assert magic==b'WDBC' and fields==2 and size==8
        rows=data[20:20+count*size];blob=data[20+count*size:]
        assert not any(struct.unpack_from('<I',rows,i*size)[0]==5827 for i in range(count))
        name=b'Interface\\Icons\\ability_rogue_grapplinghook\0'
        files[iconKey]=struct.pack('<4s4I',magic,count+1,fields,size,strings+len(name))+rows+struct.pack('<II',5827,len(blob))+blob+name
        for n,data in additions.items():
            existing=next((k for k in files if k.replace('\\','/').lower()==n.lower()),None)
            assert existing is None or files[existing]==data,'Existing visual override requires reconciliation: '+n
            files[existing or n.replace('/','\\')]=data
        assert all(files[n]==data for n,data in original.items() if n not in (key,iconKey))
        # Every unrelated record and archive entry must survive byte-for-byte.
        a,_=P.dbc(old);b,_=P.dbc(files[key]);b={r[0]:r for r in b}
        assert all(r==b[r[0]] for r in a if r[0] not in P.IDS)
        dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);write_archive(dst,files)
        with MPQArchive(dst) as check:
            assert set(check.read_file('(listfile)').decode().splitlines())==set(files)|{'(listfile)'}
            for n,data in files.items():assert check.read_file(n)==data,n
        assert sha(src)==before
        manifest[rel]={'before':before,'after':sha(dst)}
    addon='Interface/AddOns/HeroClassPlusCommitTest/'
    for rel in (addon+'GrapplingHook.lua',addon+'HeroClassPlusCommitTest.toc'):
        src=CLIENT/rel;before=sha(src) if src.exists() else None
        if rel.endswith('.lua'):
            assert before is None,'New addon file already exists; reconcile first'
            data=(HERE/'GrapplingHook.lua').read_bytes()
        else:
            old=src.read_bytes();assert old.count(b'Catalog.lua')==1
            data=old.replace(b'Catalog.lua',b'Catalog.lua\nGrapplingHook.lua')
        dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
        manifest[rel]={'before':before,'after':sha(dst)}
    (HERE/'client-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('GRAPPLING CLIENT STAGED. Every archive entry verified; installed client unchanged.')
if __name__=='__main__':main()
