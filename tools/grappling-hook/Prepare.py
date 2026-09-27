"""Stage scoped Grappling Hook source, DBC and SQL candidates; no live writes."""
from pathlib import Path
import hashlib,json,struct
HERE=Path(__file__).resolve().parent
IDS={760056,760058,760094,760095,760096}
def sha(data):return hashlib.sha256(data).hexdigest()
def dbc(data):
    magic,n,f,size,ns=struct.unpack_from('<4s4I',data)
    assert magic==b'WDBC' and f==234 and size==936 and len(data)==20+n*size+ns
    return [list(r) for r in struct.iter_unpack('<234I',data[20:20+n*size])],data[20+n*size:]
def definitions():
    rows={}
    for id in sorted(IDS):
        r=[0]*234;r[0]=id;r[4]=16;r[5]=32;r[28]=1;r[68]=0xffffffff
        r[74]=1;r[208]=8;r[216:219]=[0x3f800000]*3
        r[71]=3;r[46]=13;r[86]=1;r[133]=5827
        rows[id]=r
    r=rows[760056];r[29]=35000;r[39]=28;r[46]=4;r[16]=64;r[86]=28;r[131]=22087;r[214]=2
    r=rows[760094];r[46]=7;r[86]=6;r[131]=22087;r[214]=2
    r=rows[760095];r[3]=7;r[40]=36;r[46]=7;r[71]=6;r[86]=6;r[95]=26
    r=rows[760096];r[40]=27;r[71]=6;r[95]=4;r[133]=1
    r=rows[760058];r[40]=36;r[71]=6;r[86]=25;r[95]=4;r[131]=22086;r[133]=1
    return rows
TEXT={
760056:('Grappling Hook','Launch a grappling hook and pull yourself to the target location. For $760096d after using it you can recast it, pulling yourself to an enemy and rooting them for $760095d. Does not break stealth.'),
760094:('Grappling Hook Follow-Up','Pull yourself towards an enemy and root them for $760095d. Usable for $760096d after using Grappling Hook.'),
760095:('Grappling Hook','Rooted.'),760096:('Grappling Hook recast','Grappling Hook can be recast.'),760058:('Grappling Hook visual','')}
def transform(data,server=False):
    rows,strings=dbc(data);old={r[0]:r for r in rows}
    if server:assert not IDS&old.keys(),'Server spell-ID collision'
    new=definitions()
    for id,r in new.items():
        for field,text in ((136,TEXT[id][0]),(170,TEXT[id][1])):
            r[field]=len(strings);strings+=text.encode('utf8')+b'\0'
    result=[new.get(r[0],r) for r in rows]+[new[id] for id in sorted(IDS-old.keys())]
    return struct.pack('<4s4I',b'WDBC',len(result),234,936,len(strings))+b''.join(struct.pack('<234I',*r) for r in result)+strings
def replace_once(data,old,new):
    assert data.count(old)==1,old[:100]
    return data.replace(old,new)
def main():
    base=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path']
    bm=json.loads((base/'manifest.json').read_text());extra=HERE/'cast-routing';em=json.loads((extra/'manifest.json').read_text())
    assert bm['status']=='complete' and bm['image']==em['image']
    for root,m in ((base,bm),(extra,em)):
        for rel,h in m['files'].items():assert sha((root/rel).read_bytes())==h,rel
    sql=(base/'spell_dbc.tsv').read_bytes().decode('utf8').split('\n')
    assert not any(int(line.split('\t')[0]) in IDS for line in sql[1:] if line)
    out=HERE/'candidate';out.mkdir(exist_ok=True);manifest={}
    def save(rel,data,source=None):
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        manifest[rel]={'before':sha(source) if source is not None else None,'after':sha(data)}
    rel='src/server/game/Spells/HeroGrapplingHooks.h';save(rel,(HERE/'HeroGrapplingHooks.h').read_bytes())
    rel='modules/mod-hero-starting-path/src/GrapplingHook.cpp';save(rel,(HERE/'GrapplingHook.cpp').read_bytes())
    rel='modules/mod-hero-starting-path/src/StartingPath.cpp';old=(base/rel).read_bytes()
    new=b'void AddHeroGrapplingScripts();\n'+old
    new=replace_once(new,b'AddHeroMartialFluidityScripts(); }',b'AddHeroMartialFluidityScripts();AddHeroGrapplingScripts(); }');save(rel,new,old)
    rel='src/server/game/Handlers/SpellHandler.cpp';old=(extra/rel).read_bytes()
    marker=b'void WorldSession::HandleCastSpellOpcode(WorldPacket& recvPacket)'
    assert marker in old
    first,body=old.split(marker,1)
    before=b'    SpellInfo const* spellInfo = sSpellMgr->GetSpellInfo(spellId);'
    body=body.replace(before,b'    if (mover == _player)\n        spellId = HeroGrapplingHooks::Cast(_player, spellId);\n\n'+before,1)
    save(rel,b'#include "HeroGrapplingHooks.h"\n'+first+marker+body,old)
    rel='src/server/game/Entities/Player/Player.cpp';old=(base/rel).read_bytes()
    needle=b'ActionButton* Player::addActionButton(uint8 button, uint32 action, uint8 type)'
    index=old.index(needle);start=old.index(b'{',index)+1
    new=old[:start]+b'\n    if (type == ACTION_BUTTON_SPELL)\n        action = HeroGrapplingHooks::Action(this, action);\n'+old[start:]
    save(rel,b'#include "HeroGrapplingHooks.h"\n'+new,old)
    rel='modules/mod-hero-starting-path/src/GeneratedCatalog.h';old=(base/rel).read_bytes()
    assert b'26001633' not in old and b'760056' not in old
    # Additive entry only: preserve current and legacy catalog versions/migration.
    entry=b'\n{26001633,26001633,4,28,3,4,2,0,0,1,0,0,0,false,{760056},{0,28,28,28,28,28,28,28,28,0,28,28}},'
    new=replace_once(old,b'const rows={',b'const rows={'+entry);save(rel,new,old)
    original=(base/'Spell.dbc').read_bytes();updated=transform(original,server=True);(out/'Spell.dbc').write_bytes(updated)
    bindings={760056:'spell_hero_grapple',760094:'spell_hero_grapple',760096:'aura_hero_grapple_window'}
    current=(base/'spell_script_names.tsv').read_text(encoding='utf8')
    for line in current.splitlines()[1:]:
        if line:assert abs(int(line.split('\t')[0])) not in IDS,'Existing binding collision'
    (out/'world-apply.sql').write_text('START TRANSACTION;\n'+''.join("INSERT INTO spell_script_names(spell_id,ScriptName) VALUES (%d,'%s');\n"%(i,n) for i,n in bindings.items())+'COMMIT;\n')
    (out/'world-rollback.sql').write_text('START TRANSACTION;\n'+''.join("DELETE FROM spell_script_names WHERE spell_id=%d AND ScriptName='%s';\n"%(i,n) for i,n in bindings.items())+'COMMIT;\n')
    (HERE/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps(dict(baseline=base.name,image=bm['image'],spellBefore=sha(original),spellAfter=sha(updated),ids=sorted(IDS),status='staged; not built or activated'),indent=2)+'\n')
    print('GRAPPLING HOOK STAGED. No live source, database or client changes.')
if __name__=='__main__':main()
