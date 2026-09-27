"""Stage a local chain-size/hook visual experiment; no installed client writes."""
from pathlib import Path
import hashlib,importlib.util,json,struct,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('previous',ROOT/'outputs/Hero_Grappling_Hook/Prepare-Visuals.py')
P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
sys.path.insert(0,str(ROOT/'work/github-upload/tools'))
from lib.mpq import MPQArchive,write_archive
V=P.V;V.PREFIX='HeroGrapplingHookRepair\\'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    baseline={}
    order=['locale-enUS.MPQ','patch-enUS.MPQ']+['patch-enUS-'+str(i)+'.MPQ' for i in range(2,10)]+['patch-enUS-Z.MPQ']
    for name in order:
        path=P.CLIENT/'Data/enUS'/name
        if not path.exists():continue
        with MPQArchive(path) as a:
            for table in V.TABLES:
                try:baseline[table]=a.read_file('DBFilesClient\\'+table+'.dbc')
                except (KeyError,FileNotFoundError):pass
    assets={}
    with MPQArchive(P.SOURCE/'patch-N.MPQ') as a:
        model='SPELLS/Monk_GrappleWeapon_Missile.M2';b=a.read_file(model.replace('/','\\'))
        assert b[:8]==b'MD20\x08\x01\x00\x00'
        assets[model]=b;assets[model[:-3]+'00.skin']=a.read_file((model[:-3]+'00.skin').replace('/','\\'))
        assert assets[model[:-3]+'00.skin'][:4]==b'SKIN'
        n,o=struct.unpack_from('<II',b,80)
        for i in range(n):
            typ,flags,length,offset=struct.unpack_from('<4I',b,o+16*i)
            assert typ==0,'Unexpected replaceable model texture'
            name=b[offset:offset+length].rstrip(b'\0').decode()
            assets[name.replace('\\','/')]=a.read_file(name)
    refs={t:{} for t in V.TABLES}
    fields,_=P.row('SpellVisualEffectName',4733)
    fields[3]=struct.unpack('<I',struct.pack('<f',0.75))[0]
    fields[4]=fields[3]
    refs['SpellVisualEffectName']['4733']={'rawFields':fields,'name':'Bear Cave grapple hook test','model':model}
    added,report=V.build(refs,baseline,assets)
    added={n:b for n,b in added.items() if not n.startswith('DBFilesClient/') or report[Path(n).stem]['added']}
    effect=report['SpellVisualEffectName']['mapping'][4733]
    def patch(table,id,change):
        data=baseline[table];f,z,rows,strings=V.dbc(data);before=rows[id];raw=bytearray(before);change(raw)
        result=bytearray(data);n=struct.unpack_from('<I',data,4)[0]
        index=list(rows).index(id);result[20+index*z:20+(index+1)*z]=raw
        _,_,after,_=V.dbc(result)
        assert all(after[k]==v for k,v in rows.items() if k!=id)
        added['DBFilesClient/'+table+'.dbc']=bytes(result)
        return dict(id=id,before=before.hex(),after=raw.hex())
    chainID=json.loads((ROOT/'outputs/Hero_Grappling_Hook/visual-manifest.json').read_text())['tables']['SpellChainEffects']['mapping']['200460']
    def chain(raw):
        # Abomination Hook (59395): visual 11055, kit 10198, chain 502.
        # Keep its native repeated-link settings, with a smaller player-scale width.
        reference=V.dbc(baseline['SpellChainEffects'])[2][502]
        originalID=struct.unpack_from('<I',raw,0)[0]
        textureOffset=struct.unpack_from('<I',raw,28)[0]
        raw[:]=reference
        struct.pack_into('<I',raw,0,originalID)
        struct.pack_into('<I',raw,28,textureOffset)
        struct.pack_into('<f',raw,8,0.10)
        struct.pack_into('<f',raw,169,1.0)
        struct.pack_into('<I',raw,161,0)
    changes={'SpellChainEffects':patch('SpellChainEffects',chainID,chain),
      'SpellVisual':patch('SpellVisual',22086,lambda raw:struct.pack_into('<I',raw,8*4,effect))}
    manifest={}
    for rel in ('Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'):
        source=P.CLIENT/rel;before=sha(source.read_bytes())
        with MPQArchive(source) as a:
            names=a.read_file('(listfile)').decode().splitlines()
            files={n:a.read_file(n) for n in names if n!='(listfile)'}
        originals=dict(files);replaced=set()
        for n,b in added.items():
            key=next((k for k in files if k.replace('\\','/').lower()==n.lower()),n.replace('/','\\'))
            if key in files and n.startswith('DBFilesClient/'):
                assert files[key]==baseline[Path(n).stem],'Root/locale baseline mismatch'
            files[key]=b;replaced.add(key)
        assert all(files[n]==b for n,b in originals.items() if n not in replaced)
        dest=HERE/'client-candidate'/rel;dest.parent.mkdir(parents=True,exist_ok=True);write_archive(dest,files)
        with MPQArchive(dest) as a:
            assert set(a.read_file('(listfile)').decode().splitlines())==set(files)|{'(listfile)'}
            assert all(a.read_file(n)==b for n,b in files.items())
        assert sha(source.read_bytes())==before
        manifest[rel]={'before':before,'after':sha(dest.read_bytes())}
    (HERE/'client-manifest.json').write_text(json.dumps(manifest,indent=2))
    (HERE/'visual-repair.json').write_text(json.dumps(dict(status='staged visual experiment; in-game acceptance required',changes=changes,effect=effect,assets={n:sha(b) for n,b in assets.items()},schema='https://github.com/wowdev/WoWDBDefs/blob/master/definitions/SpellChainEffects.dbd'),indent=2))
    print('VISUAL REPAIR STAGED. Two archives verified; existing Spell.dbc and unrelated entries unchanged.')
if __name__=='__main__':main()
