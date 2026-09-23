from pathlib import Path
import os,subprocess,shlex,tempfile
HERE=Path(__file__).resolve().parent
holder=None
if os.environ.get('HERO_TEST_DIR'):
 out=Path(os.environ['HERO_TEST_DIR']);out.mkdir(parents=True,exist_ok=True)
else:
 holder=tempfile.TemporaryDirectory();out=Path(holder.name)
# The fixture is extracted from the actual staged grant functions.
overlay=HERE/'overlay/modules/mod-hero-starting-path/src/StartingPath.cpp'
if overlay.exists():
 s=overlay.read_text();start=s.index('void KeepHybridEquipment');end=s.index('bool Sync(Player*',start)
 assert s[start:end]==(HERE/'grant-test-fixture.h').read_text()
text=(HERE/'test-stub.h').read_text()+(HERE/'grant-test-fixture.h').read_text()+(HERE/'policy-test.cpp').read_text()
(out/'test.cpp').write_text(text)
command=shlex.split(os.environ.get('CXX','c++'))
subprocess.run(command+['-std=c++17','-I'+str(HERE),str(out/'test.cpp'),'-o',str(out/'test.exe')],check=True)
subprocess.run([str(out/'test.exe')],check=True)
print('PASS: all 90 class pairs, level gates, actual grant functions, progression and Classic/profession isolation.')
