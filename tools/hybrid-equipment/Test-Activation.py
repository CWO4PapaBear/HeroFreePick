"""Exercise source install/rollback without Docker or live server access."""
from pathlib import Path
import importlib.util,os,uuid

here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('activation',here/'Activate-Test.py')
activation=importlib.util.module_from_spec(spec);spec.loader.exec_module(activation)
out=Path(os.environ.get('HERO_TEST_DIR',str(here/'test-output')))/('activation-'+uuid.uuid4().hex)
root=out/'source';work=out/'backup'
for folder in (root,work/'before',work/'after'):folder.mkdir(parents=True,exist_ok=True)
(root/'existing.cpp').write_bytes(b'old')
(work/'before/existing.cpp').write_bytes(b'old')
(work/'after/existing.cpp').write_bytes(b'new')
(work/'after/EquipmentPolicy.h').write_bytes(b'policy')
files={name:{version:activation.sha(work/version/name) for version in ('before','after')} for name in ('existing.cpp','EquipmentPolicy.h')}
activation.restore_sources(root,work,files,'after')
assert (root/'existing.cpp').read_bytes()==b'new'
assert (root/'EquipmentPolicy.h').read_bytes()==b'policy'
activation.restore_sources(root,work,files,'before')
assert (root/'existing.cpp').read_bytes()==b'old'
assert not (root/'EquipmentPolicy.h').exists()
# An unrelated edit must stop the entire operation before any mutation.
(root/'EquipmentPolicy.h').write_bytes(b'foreign')
try:activation.restore_sources(root,work,files,'after')
except RuntimeError:pass
else:raise AssertionError('Foreign source was accepted')
assert (root/'existing.cpp').read_bytes()==b'old'
assert (root/'EquipmentPolicy.h').read_bytes()==b'foreign'
print('PASS: source installation, rollback of new header, and drift rejection.')
