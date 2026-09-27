"""Stage isolated grapple chain/cast sound and icon; never edit installed archives."""
from pathlib import Path
import importlib.util,json,struct,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'work/github-upload/tools'))
from lib.mpq import MPQArchive
module=ROOT/'outputs/HeroFreePick-Main-Publish/server/spell-definitions'
spec=importlib.util.spec_from_file_location('visual',module/'stage_visual_dbc.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
V.PREFIX='HeroGrappling\\'
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
SOURCE=Path('D:/DML WOTLK Client Side/Ascension A52 Free Pick/ascension-live/ascension-live/Data')
def source(table):
    letter='M' if table.startswith('Sound') else 'S'
    p=ROOT/'work/spell-support-extract'/('ascension-live_Data_patch-'+letter+'.MPQ.'+table+'.dbc')
    data=p.read_bytes();f,z,rows,strings=V.dbc(data)
    return rows,strings,hashlib.sha256(data).hexdigest()
def row(table,id):
    rows,st,h=source(table);raw=rows[id]
    return list(struct.unpack('<'+'I'*(len(raw)//4),raw)),st
def text(st,offset):return st[offset:st.index(b'\0',offset)].decode('utf8')
def main():
    refs={t:{} for t in V.TABLES}
    for id in (22086,22087):refs['SpellVisual'][str(id)]=row('SpellVisual',id)[0]
    # Ascension points missile-targeting kit 34 at obsolete FreezingFinger .MDL
    # effects. The grappling rope is kit 21996, chain 200460; preserve that chain.
    assert refs['SpellVisual']['22086'][22]==34
    refs['SpellVisual']['22086'][22]=0
    for id in (171,21971,21996):refs['SpellVisualKit'][str(id)]=row('SpellVisualKit',id)[0]
    assert all(not any(r[3:15]) and not r[16] for r in refs['SpellVisualKit'].values())
    chain=source('SpellChainEffects');raw=chain[0][200460]
    texture=text(chain[1],struct.unpack_from('<I',raw,28)[0])
    refs['SpellChainEffects']['200460']={'hex':raw.hex(),'strings':{'28':texture}}
    sound,st=row('SoundEntries',71047)
    texts={str(i):text(st,sound[i]) for i in (2,*range(3,13),23)}
    refs['SoundEntries']['71047']={'rawFields':sound,'strings':texts}
    advanced=sound[29];refs['SoundEntriesAdvanced'][str(advanced)]=row('SoundEntriesAdvanced',advanced)[0]
    assert refs['SoundEntriesAdvanced'][str(advanced)][1]==71047
    # Effective locale DBCs: later locale patches override earlier ones. None of
    # the installed root patches may override these tables without reconciliation.
    baseline={};origins={}
    locale=CLIENT/'Data/enUS'
    order=['locale-enUS.MPQ','patch-enUS.MPQ']+['patch-enUS-'+str(i)+'.MPQ' for i in range(2,10)]+['patch-enUS-Z.MPQ']
    for name in order:
        p=locale/name
        if not p.is_file():continue
        with MPQArchive(p) as archive:
            for table in V.TABLES:
                try:data=archive.read_file('DBFilesClient\\'+table+'.dbc')
                except (KeyError,FileNotFoundError):continue
                baseline[table]=data;origins[table]=str(p)
    assert set(baseline)==set(V.TABLES)
    for p in (CLIENT/'Data').glob('*.MPQ'):
        with MPQArchive(p) as archive:
            for table in V.TABLES:
                try:data=archive.read_file('DBFilesClient\\'+table+'.dbc')
                except (KeyError,FileNotFoundError):continue
                if data!=baseline[table] and refs[table]:
                    _,_,rootRows,rootStrings=V.dbc(data)
                    _,_,localeRows,localeStrings=V.dbc(baseline[table])
                    assert table=='SpellVisualKitModelAttach' and all(localeRows.get(k)==v for k,v in rootRows.items()),'Conflicting root/locale rows: '+table
                    assert set(rootRows)<=set(localeRows),'Root table is not a preserved subset'
    assets={};assetOrigins={}
    wanted=[texture]+[texts['23']+'\\'+texts[str(i)] for i in range(3,13) if texts[str(i)]]
    archives=[]
    try:
        for p in sorted(SOURCE.rglob('*.MPQ'),key=lambda p:str(p).lower()):
            if p.is_file():archives.append((p,MPQArchive(p)))
        for name in wanted:
            variants={}
            for p,a in reversed(archives):
                try:b=a.read_file(name)
                except (KeyError,FileNotFoundError):continue
                variants.setdefault(hashlib.sha256(b).hexdigest(),(b,str(p)))
            assert variants,('Missing asset',name)
            if len(variants)>1:
                print('Asset variants (later archive selected):',name,[(h,p) for h,(_,p) in variants.items()])
            b,p=next(iter(variants.values()));assets[name.replace('\\','/')]=b;assetOrigins[name]=p
    finally:
        for _,a in archives:a.close()
    outputs,report=V.build(refs,baseline,assets)
    # Never override unrelated tables, including existing model-attachment overrides.
    for table,details in report.items():
        if not details['added']:outputs.pop('DBFilesClient/'+table+'.dbc',None)
    icon='Interface/Icons/ability_rogue_grapplinghook.blp'
    outputs[icon]=(CLIENT/'Interface/AddOns/HeroFreePick/Art/AscensionAbilities/ability_rogue_grapplinghook.blp').read_bytes()
    out=HERE/'visual-candidate';out.mkdir(exist_ok=True)
    for name,data in outputs.items():
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    audit=dict(tables=report,baselineSources=origins,assetSources=assetOrigins,
        files={n:hashlib.sha256(b).hexdigest() for n,b in outputs.items()},
        adaptation='Omit obsolete FreezingFinger missile-targeting kit 34; retain rope chain 200460, cast animation and four whoosh sounds.',
        status='staged; in-game rendering unverified')
    (HERE/'visual-manifest.json').write_text(json.dumps(audit,indent=2)+'\n')
    print('GRAPPLE VISUALS STAGED:',len(outputs),'files; original client tables retained.')
if __name__=='__main__':main()
