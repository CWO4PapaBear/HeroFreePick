"""Read-only current PTR evidence for mode-scoped Warrior stance changes."""
from pathlib import Path
import datetime, hashlib, json, subprocess

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/dml/games/wow-server-classless-test')
WORLD='classless-test-worldserver'
def run(args,**kw):
    p=subprocess.run(args,capture_output=True,timeout=180,**kw)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
    return p.stdout
def main():
    state=json.loads(run(['docker','inspect',WORLD]))[0]
    labels=state['Config']['Labels']
    assert labels.get('com.docker.compose.project')=='classless-test'
    out=HERE/('baseline-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S-%f'))
    out.mkdir(parents=True)
    manifest=dict(status='collecting',image=state['Image'],activeConfig=labels['com.docker.compose.project.config_files'],ports=state['HostConfig']['PortBindings'],files={})
    def save(rel,data):
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        manifest['files'][rel]=hashlib.sha256(data).hexdigest()
    rels=['src/server/game/'+p for p in (
        'Entities/Player/Player.cpp','Entities/Player/Player.h',
        'Spells/Spell.cpp','Spells/SpellInfo.cpp','Spells/SpellInfo.h','Spells/SpellMgr.cpp',
        'Spells/Auras/SpellAuraEffects.cpp','Spells/Auras/SpellAuraDefines.h',
        'Scripting/ScriptDefines/PlayerScript.h')]
    rels+=['src/server/shared/DataStores/DBCStructure.h']
    for rel in rels:save(rel,(ROOT/rel).read_bytes())
    for p in (ROOT/'modules/mod-hero-starting-path').rglob('*'):
        if p.is_file() and p.suffix in ('.cpp','.h','.cmake','.txt','.dist'):
            save(p.relative_to(ROOT).as_posix(),p.read_bytes())
    # docker cp also works when the existing world container is stopped.
    for name in ('Spell','SpellDuration','SpellRange'):
        p=out/(name+'.dbc')
        run(['docker','cp',WORLD+':/azerothcore/env/dist/data/dbc/'+name+'.dbc',str(p)])
        manifest['files'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    for table in ('spell_dbc','spell_script_names'):
        sql='SELECT * FROM '+table+';'
        save(table+'.tsv',run(['docker','exec','-i','classless-test-database','sh','-c',
            'MYSQL_PWD="${MYSQL_ROOT_PASSWORD:-$MARIADB_ROOT_PASSWORD}" mysql --default-character-set=utf8mb4 -uroot --batch acore_world'],input=sql.encode()))
    manifest['status']='complete'
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (HERE/'latest-baseline.json').write_text(json.dumps({'path':out.name})+'\n')
    print('READ-ONLY WARRIOR STANCE SNAPSHOT COMPLETE:',out)
    print('No restart, source edits, live SQL writes or client installation.')
if __name__=='__main__':main()
