"""Build reviewed Warrior stance module against the captured PTR; restore source afterward."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/dml/games/wow-server-classless-test');WORLD='classless-test-worldserver'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()
def save(p,data):p.write_text(json.dumps(data,indent=2)+'\n');os.chmod(p,0o600)
def main():
 if os.name!='posix' or os.geteuid()!=0:raise RuntimeError('Run with sudo python3 in WSL.')
 import fcntl
 lock=(ROOT/'.hero-upcoming-build.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 baseline=HERE/json.loads((HERE/'latest-baseline.json').read_text())['path'];m=json.loads((baseline/'manifest.json').read_text())
 files=json.loads((HERE/'source-manifest.json').read_text());candidate=HERE/'candidate'
 world=json.loads(run(['docker','inspect',WORLD]))[0];labels=world['Config']['Labels']
 assert labels.get('com.docker.compose.project')=='classless-test'
 assert world['Image']==m['image'] and world['HostConfig']['PortBindings']==m['ports'],'PTR changed since snapshot'
 assert labels['com.docker.compose.project.config_files']==m['activeConfig'],'Active compose changed'
 for rel,h in m['files'].items():
  assert sha(baseline/rel)==h,'Snapshot changed: '+rel
  if rel.startswith(('src/','modules/')):assert sha(ROOT/rel)==h,'Live source changed: '+rel
 for rel,h in files.items():
  assert sha(candidate/rel)==h['after'] and sha(ROOT/rel)==h['before'],rel
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
 work=ROOT/'backups'/('warrior-stances-build-'+stamp);work.mkdir(parents=True,mode=0o700)
 for rel,h in files.items():
  for version in ('before','after'):(work/version/rel).parent.mkdir(parents=True,exist_ok=True)
  if h['before'] is not None:shutil.copy2(ROOT/rel,work/'before'/rel)
  shutil.copy2(candidate/rel,work/'after'/rel)
 run(['docker','cp',WORLD+':/azerothcore/env/dist/data/dbc/Spell.dbc',str(work/'Spell-before.dbc')])
 spells=json.loads((candidate/'manifest.json').read_text())
 assert sha(work/'Spell-before.dbc')==spells['spellBefore'] and sha(candidate/'Spell.dbc')==spells['spellAfter']
 shutil.copy2(candidate/'Spell.dbc',work/'Spell-after.dbc');os.chmod(work/'Spell-after.dbc',0o644)
 active=Path(m['activeConfig']);assert active.resolve().is_relative_to(ROOT)
 config=json.loads(run(['docker','compose','-p','classless-test','-f',str(active),'config','--format','json']))
 build=json.loads((ROOT/'compose.no-core-build.json').read_text())['services']['ac-worldserver']['build']
 assert Path(build['context']).resolve()==ROOT
 tag='local/classless-test-worldserver:warrior-stances-'+stamp
 config['services']['ac-worldserver'].update(build=build,image=tag);save(work/'build.json',config)
 command=['docker','compose','-p','classless-test','-f',str(work/'build.json')]
 subprocess.run(command+['config','--quiet'],check=True)
 state=dict(status='building',previousImage=world['Image'],ports=m['ports'],activeConfig=str(active),tag=tag,work=str(work),files=files,spellBefore=spells['spellBefore'],spellAfter=spells['spellAfter'])
 save(HERE/'build-state.json',state);changed=[]
 try:
  for rel,h in files.items():
   assert sha(ROOT/rel)==h['before'];shutil.copy2(work/'after'/rel,ROOT/rel);changed.append(rel)
  with (HERE/'build.log').open('w') as log:
   proc=subprocess.Popen(command+['build','ac-worldserver'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   for line in proc.stdout:print(line,end='',flush=True);log.write(line);log.flush()
   if proc.wait():raise RuntimeError('BUILD FAILED. Review build.log; no activation performed.')
  state.update(status='compiled-not-activated',builtImage=run(['docker','image','inspect','--format','{{.Id}}',tag]))
 except BaseException:state['status']='failed';raise
 finally:
  errors=[]
  for rel in reversed(changed):
   try:
    assert sha(ROOT/rel)==files[rel]['after'],'Source independently changed: '+rel
    if files[rel]['before'] is None:(ROOT/rel).unlink()
    else:shutil.copy2(work/'before'/rel,ROOT/rel)
   except Exception as e:errors.append(str(e))
  state['sourceRestorationErrors']=errors;save(HERE/'build-state.json',state)
  if errors:raise RuntimeError('Source restoration needs review: '+str(errors))
 now=json.loads(run(['docker','inspect',WORLD]))[0]
 assert now['Image']==world['Image'] and now['HostConfig']['PortBindings']==world['HostConfig']['PortBindings']
 print('BUILD COMPLETE. Source restored. No restart, database writes or client installation. Return for activation review.')
if __name__=='__main__':main()
