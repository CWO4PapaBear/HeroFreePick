from pathlib import Path
import hashlib,importlib.util,json,uuid
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('installer',HERE/'Install-Client.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=HERE/'local-tests'/('installer-'+uuid.uuid4().hex);client=root/'client';source=root/'source'
records={}
for rel in ('Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'):
 for base,data in ((client,b'before'),(source,b'after')):
  p=base/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 records[rel]={'before':m.sha(client/rel),'after':m.sha(source/rel)}
calls=0
def interrupt():
 global calls
 calls+=1
 if calls==5:raise RuntimeError('simulated game launch')
try:m.install(client,source,records,root/'failed-backup',interrupt)
except RuntimeError as e:assert str(e)=='simulated game launch'
else:raise AssertionError('Expected interruption')
assert all(m.sha(client/rel)==h['before'] for rel,h in records.items())
assert not list(client.rglob('*.warrior-new'))
assert len(m.install(client,source,records,root/'backup',lambda:None))==2
assert m.install(client,source,records,root/'repeat',lambda:None)==[]
assert all(m.sha(client/rel)==h['after'] for rel,h in records.items())
print('PASS: interrupted two-file install rolls back; temporary files cleaned; repeat installation is a no-op.')
