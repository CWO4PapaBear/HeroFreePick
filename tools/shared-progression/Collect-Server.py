"""Read-only PTR source snapshot for shared Hero/Hybrid progression."""
from pathlib import Path
import datetime, hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path('/home/dml/games/wow-server-classless-test')

def main():
    def run(args):
        return subprocess.run(args, check=True, capture_output=True, timeout=180).stdout
    world = json.loads(run(['docker', 'inspect', 'classless-test-worldserver']))[0]
    labels = world['Config']['Labels']
    assert labels.get('com.docker.compose.project') == 'classless-test'
    out = HERE / ('baseline-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S-%f'))
    out.mkdir(parents=True)
    paths = [ROOT / p for p in (
        'src/server/game/Entities/Player/Player.cpp',
        'src/server/game/Entities/Player/Player.h',
        'src/server/game/Entities/Unit/StatSystem.cpp',
        'src/server/game/Globals/ObjectMgr.cpp',
        'src/server/game/Globals/ObjectMgr.h',
        'src/server/game/Scripting/ScriptDefines/PlayerScript.h',
        'src/server/game/Scripting/ScriptMgr.cpp',
        'src/server/game/Scripting/ScriptMgr.h',
    )]
    module = ROOT / 'modules/mod-hero-starting-path'
    paths += [p for p in module.rglob('*') if p.is_file() and p.suffix in ('.cpp', '.h', '.conf', '.dist', '.txt', '.cmake')]
    manifest = dict(image=world['Image'], ports=world['HostConfig']['PortBindings'], activeConfig=labels['com.docker.compose.project.config_files'], files={})
    for src in paths:
        rel = src.relative_to(ROOT).as_posix()
        data = src.read_bytes()
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest['files'][rel] = hashlib.sha256(data).hexdigest()
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    (HERE / 'latest-baseline.json').write_text(json.dumps({'path': out.name}, indent=2))
    print('READ-ONLY PROGRESSION SNAPSHOT COMPLETE:', out)
    print('No restart, database writes, client changes or activation performed.')

if __name__ == '__main__':
    main()
