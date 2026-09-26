"""Prepare hash-pinned stance-only server/client spell data and original module changes."""
from pathlib import Path
import hashlib,json,struct
HERE=Path(__file__).resolve().parent
RANKS={100,6178,11578,6343,8198,8204,8205,11580,11581,25264,47501,47502}
AURA=9905301
FLAG=0x20000000
def sha(data):return hashlib.sha256(data).hexdigest()
def read_dbc(data):
    magic,count,fields,size,ns=struct.unpack_from('<4s4I',data)
    assert magic==b'WDBC' and fields==234 and size==936 and len(data)==20+count*size+ns
    return [list(r) for r in struct.iter_unpack('<234I',data[20:20+count*size])],data[20+count*size:]
def transform(data):
    rows,strings=read_dbc(data);byid={r[0]:r for r in rows}
    assert AURA not in byid,'Support spell ID collision'
    assert RANKS <= byid.keys()
    # Reserve only a bit absent from every current Warrior spell and modifier.
    assert not any(r[208]==4 and any(r[i]&FLAG for i in (211,124,127,130)) for r in rows),'Family-mask collision'
    for id in RANKS:
        r=byid[id]
        assert r[208]==4 and r[12]==(65536 if id in (100,6178,11578) else 196608)
        r[211]|=FLAG
    aura=byid[57499].copy();aura[0]=AURA
    # A cast-only passive aura is not sent to clients. Use a permanent non-passive
    # hidden aura so native client stance/usable checks receive effect 275.
    aura[4]=(aura[4]&~0x40)|0x80000000
    aura[5]|=0x10000000 # Hidden aura icon, still sent to the client.
    aura[6]|=0x80000 # Allow unshifted as well as the three Warrior stances.
    aura[40]=21 # Verified SpellDuration: -1 / 0 / -1.
    aura[12:16]=[0x70000,0,0,0]
    aura[71:131]=[0]*60
    aura[71]=6;aura[74]=1;aura[86]=1;aura[95]=275;aura[124]=FLAG
    aura[131:133]=[0,0];aura[209:212]=[0,0,0]
    for start in (136,153,170,187):aura[start:start+16]=[0]*16
    for field,text in ((136,'Hero Warrior Stance Access'),(170,'Allows Charge and Thunder Clap without a Warrior stance in custom advancement modes.')):
        aura[field]=len(strings);strings+=text.encode()+b'\0'
    rows.append(aura);rows.sort(key=lambda r:r[0])
    return struct.pack('<4s4I',b'WDBC',len(rows),234,936,len(strings))+b''.join(struct.pack('<234I',*r) for r in rows)+strings
def patch_source(text):
    replacements={
      '#include "StockRankLevels.h"':'#include "StockRankLevels.h"\n#include "WarriorStances.h"',
      'auto resources=ReadHybrid(p);HeroResourcesPublish(p,phase==2&&resources.valid?resources.mode:1,resources.second);':'auto resources=ReadHybrid(p);HeroResourcesPublish(p,phase==2&&resources.valid?resources.mode:1,resources.second);\n HeroWarriorStances::Publish(p,phase==2&&resources.valid&&resources.mode>=2&&resources.mode<=4);',
      'void OnPlayerUpdate(Player* p,uint32) override {':'void OnPlayerUpdate(Player* p,uint32) override {\n        HeroWarriorStances::Sync(p);',
      'void OnPlayerLogout(Player* p) override { HeroDKStart::Forget(p);':'void OnPlayerLogout(Player* p) override { HeroWarriorStances::Forget(p); HeroDKStart::Forget(p);',
      'HeroSharedProgressionLoad();':'HeroSharedProgressionLoad();\n        HeroWarriorStances::Load();',
    }
    for old,new in replacements.items():
        assert text.count(old)==1,old
        text=text.replace(old,new)
    return text
def main():
    base=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path']
    m=json.loads((base/'manifest.json').read_text());assert m['status']=='complete'
    for rel,h in m['files'].items():assert sha((base/rel).read_bytes())==h,rel
    lines=(base/'spell_dbc.tsv').read_bytes().decode('utf-8').split('\n');columns=lines[0].split('\t')
    for line in lines[1:]:
        if not line:continue
        cells=line.split('\t');assert len(cells)==len(columns)
        row=dict(zip(columns,cells));assert int(row['ID']) not in RANKS|{AURA},'Reconcile SQL override'
        if int(row['SpellClassSet'])==4:
            for key in ('SpellClassMask_3','EffectSpellClassMaskC_1','EffectSpellClassMaskC_2','EffectSpellClassMaskC_3'):
                assert not int(row[key])&FLAG,'SQL mask collision'
    source=base/'Spell.dbc';result=transform(source.read_bytes())
    out=HERE/'candidate';out.mkdir(exist_ok=True);(out/'Spell.dbc').write_bytes(result)
    files={}
    for rel,data in {
      'modules/mod-hero-starting-path/src/StartingPath.cpp':patch_source((base/'modules/mod-hero-starting-path/src/StartingPath.cpp').read_text()).encode(),
      'modules/mod-hero-starting-path/src/WarriorStances.h':(HERE/'WarriorStances.h').read_bytes(),
    }.items():
        target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        files[rel]={'before':sha((base/rel).read_bytes()) if (base/rel).exists() else None,'after':sha(data)}
    (HERE/'source-manifest.json').write_text(json.dumps(files,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps(dict(baseline=base.name,image=m['image'],spellBefore=sha(source.read_bytes()),spellAfter=sha(result),aura=AURA,ranks=sorted(RANKS),family=4,maskWord=2,maskBit=29,status='staged; not built or activated'),indent=2)+'\n')
    print('STAGED: original module changes and Spell.dbc candidate; no live changes.')
if __name__=='__main__':main()
