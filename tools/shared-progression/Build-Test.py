"""Build the Hero shared progression; does not activate."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent;ROOT=Path('/home/dml/games/wow-server-classless-test');WORLD='classless-test-worldserver'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,indent=2));os.chmod(p,0o600)
def main():
 if os.name!='posix' or os.geteuid()!=0:raise RuntimeError('Run with sudo python3 in WSL.')
 import fcntl
 lock=(ROOT/'.hero-upcoming-build.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 w=json.loads(run(['docker','inspect',WORLD]))[0];labels=w['Config']['Labels'];assert labels.get('com.docker.compose.project')=='classless-test'
 active=Path(labels['com.docker.compose.project.config_files']);assert ',' not in str(active) and active.resolve().is_relative_to(ROOT)
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S-%f');work=ROOT/'backups'/('shared-progression-build-'+stamp);work.mkdir(parents=True,mode=0o700)
 spec=importlib.util.spec_from_file_location('stage',HERE/'Stage-Server.py');stage=importlib.util.module_from_spec(spec);spec.loader.exec_module(stage)
 files={}
 for rel,ids in stage.FILES.items():
  before=work/'before'/rel;after=work/'after'/rel;before.parent.mkdir(parents=True,exist_ok=True);after.parent.mkdir(parents=True,exist_ok=True)
  if (ROOT/rel).is_file():shutil.copy2(ROOT/rel,before)
  after.write_text(stage.patch(before.read_text() if before.exists() else None,ids));files[rel]={'before':sha(before) if before.exists() else None,'after':sha(after)}
 config=json.loads(run(['docker','compose','-p','classless-test','-f',str(active),'config','--format','json']))
 build=json.loads((ROOT/'compose.no-core-build.json').read_text())['services']['ac-worldserver']['build'];assert Path(build['context']).resolve()==ROOT
 tag='local/classless-test-worldserver:shared-progression-'+stamp;config['services']['ac-worldserver'].update(build=build,image=tag);save(work/'build.json',config)
 command=['docker','compose','-p','classless-test','-f',str(work/'build.json')];subprocess.run(command+['config','--quiet'],check=True)
 state={'status':'building','previousImage':w['Image'],'ports':w['HostConfig']['PortBindings'],'activeConfig':str(active),'tag':tag,'work':str(work),'files':files};save(HERE/'build-state.json',state);changed=[]
 try:
  for rel,h in files.items():
   assert (sha(ROOT/rel) if (ROOT/rel).is_file() else None)==h['before'];shutil.copy2(work/'after'/rel,ROOT/rel);changed.append(rel)
  with (HERE/'build.log').open('w') as log:
   proc=subprocess.Popen(command+['build','ac-worldserver'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   for line in proc.stdout:print(line,end='',flush=True);log.write(line);log.flush()
   if proc.wait():raise RuntimeError('BUILD FAILED. Send build.log; no activation performed.')
  state['builtImage']=run(['docker','image','inspect','--format','{{.Id}}',tag]);state['status']='compiled-not-activated'
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
 now=json.loads(run(['docker','inspect',WORLD]))[0];assert now['Image']==w['Image'] and now['HostConfig']['PortBindings']==w['HostConfig']['PortBindings']
 print('BUILD COMPLETE. Source restored. No restart, database writes or client installation. Return for activation review.')
if __name__=='__main__':main()
