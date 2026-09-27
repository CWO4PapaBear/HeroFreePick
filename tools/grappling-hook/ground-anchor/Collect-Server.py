"""Read-only PTR Grappling Hook implementation baseline. Run inside WSL."""
from pathlib import Path
import datetime, hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path('/home/dml/games/wow-server-classless-test')
WORLD = 'classless-test-worldserver'

def run(args, **kwargs):
    p = subprocess.run(args, capture_output=True, timeout=180, **kwargs)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-1500:])
    return p.stdout

def main():
    state = json.loads(run(['docker', 'inspect', WORLD]))[0]
    labels = state['Config']['Labels']
    assert labels.get('com.docker.compose.project') == 'classless-test'
    out = HERE / ('baseline-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S-%f'))
    out.mkdir(parents=True)
    report = {'status': 'collecting', 'image': state['Image'],
              'activeConfig': labels['com.docker.compose.project.config_files'], 'files': {}}
    def save(rel, data):
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        report['files'][rel] = hashlib.sha256(data).hexdigest()
    # Source only; never copy module configuration, Docker environments or accounts.
    dirs = ['src/server/game/Spells', 'src/server/game/Movement',
            'src/server/game/Scripting', 'modules/mod-hero-starting-path',
            'modules/mod-hero-advancement', 'modules/mod-hero-classplus',
            'modules/mod-hero-hybrid', 'modules/mod-hero-freepick']
    for rel in dirs:
        for p in (ROOT / rel).rglob('*'):
            if p.is_file() and p.suffix in ('.h', '.cpp', '.cmake', '.txt'):
                save(p.relative_to(ROOT).as_posix(), p.read_bytes())
    for rel in ['src/server/game/Entities/Player/Player.cpp',
                'src/server/game/Entities/Player/Player.h',
                'src/server/game/Entities/Unit/Unit.h',
                'src/server/game/Entities/Unit/Unit.cpp',
                'src/server/scripts/Spells/spell_rogue.cpp',
                'src/server/shared/SharedDefines.h']:
        save(rel, (ROOT / rel).read_bytes())
    for name in ('Spell', 'SpellDuration', 'SpellRange', 'SpellCastTimes', 'SpellRadius'):
        save(name + '.dbc', run(['docker', 'exec', WORLD, 'cat',
             '/azerothcore/env/dist/data/dbc/' + name + '.dbc']))
    ids = '760056,760057,760058,760059,760078,760091,760092,760093,760094,760095,760096,760097'
    queries = {
        'anchor-models': 'SELECT * FROM creature_model_info;',
        'spell_dbc-schema': 'SHOW COLUMNS FROM spell_dbc;',
        'spell_dbc': 'SELECT * FROM spell_dbc;',
        'spell_script_names': 'SELECT * FROM spell_script_names;',
        'spell-linked': 'SELECT * FROM spell_linked_spell WHERE ABS(spell_trigger) IN (' + ids + ') OR ABS(spell_effect) IN (' + ids + ');',
        'anchor': 'SELECT * FROM creature_template WHERE entry=18721;',
        'anchor-ai': 'SELECT * FROM smart_scripts WHERE entryorguid=840057 AND source_type=0;',
    }
    for name, sql in queries.items():
        save(name + '.tsv', run(['docker', 'exec', '-i', 'classless-test-database', 'sh', '-c',
             'MYSQL_PWD="${MYSQL_ROOT_PASSWORD:-$MARIADB_ROOT_PASSWORD}" mysql -uroot --default-character-set=utf8mb4 --batch acore_world'], input=sql.encode()))
    report['status'] = 'complete'
    (out / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    (HERE / 'latest-baseline.json').write_text(json.dumps({'path': out.name}) + '\n')
    print('READ-ONLY GRAPPLING HOOK SNAPSHOT COMPLETE:', out)
    print('No restart, source edits, database writes or client installation.')

if __name__ == '__main__':
    main()
