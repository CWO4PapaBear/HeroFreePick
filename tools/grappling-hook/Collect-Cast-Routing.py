"""Read-only supplement for native temporary spell replacement and persistence."""
from pathlib import Path
import importlib.util,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('collect',HERE/'Collect-Server.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
base=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path']
manifest=json.loads((base/'manifest.json').read_text())
state=json.loads(c.run(['docker','inspect',c.WORLD]))[0]
assert state['Image']==manifest['image'],'Active image changed; collect a fresh baseline first'
out=HERE/'cast-routing';out.mkdir(exist_ok=True)
report={'image':state['Image'],'files':{}}
for rel in ['src/server/game/Handlers/SpellHandler.cpp',
            'src/server/game/Handlers/MiscHandler.cpp',
            'src/server/game/Entities/Object/Object.h',
            'src/server/game/Entities/Player/PlayerStorage.cpp']:
    data=(c.ROOT/rel).read_bytes();p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    report['files'][rel]=c.hashlib.sha256(data).hexdigest()
(out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
print('READ-ONLY CAST ROUTING SNAPSHOT COMPLETE. No restart or live changes.')
