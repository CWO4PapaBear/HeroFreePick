"""Activate the reviewed Starter skill rewards image. No SQL, DBC, MPQ or addon installation."""
from pathlib import Path
import argparse,copy,hashlib,json,os,shutil,subprocess,time
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/dml/games/wow-server-classless-test');WORLD='classless-test-worldserver';DB='classless-test-database'
def run(args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=180)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def save(p,data):p.write_text(json.dumps(data,indent=2));os.chmod(p,0o600)
def inspect():return json.loads(run(['docker','inspect',WORLD]))[0]
def sql(query):return run(['docker','exec',DB,'sh','-c','MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot --batch --skip-column-names acore_characters -e "$1"','starter-skill-rewards-read',query])
def compose(config):run(['docker','compose','-p','classless-test','-f',str(config),'up','-d','--no-deps','--no-build','--force-recreate','ac-worldserver'])
def ready(image,path):
 build=json.loads((HERE/'build-state.json').read_text())
 marker='Adaptive Auto Attack: module loaded (0.2.1 spell opener;' if image==build['builtImage'] else 'Adaptive Auto Attack: module loaded'
 for i in range(180):
  w=inspect();logs=run(['docker','logs',WORLD]);path.write_text(logs)
  if not w['State']['Running'] or w['Image']!=image:raise RuntimeError('Unexpected world state; see startup log')
  if any(('validation failed' in line.lower() or 'baseline mismatch' in line.lower() or 'must rollback' in line.lower()) and any(tag in line for tag in ('HERO_','MORE_MINIONS')) for line in logs.splitlines()):raise RuntimeError('Module validation failed; see startup log')
  if marker in logs and all(marker in logs for marker in ('HERO_STARTING_PATH ready v6.7;', 'HERO_DK_SCALING v1 ready;', 'MORE_MINIONS v0.2 staged handlers ready; shared Hunter stable', 'MORE_MINIONS independent Demon Mastery ready (native stable slot preserved)', 'HERO_PROJECTILES v0.4 loaded;')):
   test=subprocess.run(['docker','exec',WORLD,'bash','-c','exec 3<>/dev/tcp/127.0.0.1/8085'],capture_output=True)
   if test.returncode==0:return
  if i%6==0:print('Waiting for world startup...',flush=True)
  time.sleep(5)
 raise RuntimeError('World startup timeout; see '+str(path))
def restore_sources(root,work,files,version):
 if version not in ('before','after'):raise ValueError('Invalid source version')
 # Validate the entire set before changing any file, including rollback's new header.
 for rel,h in files.items():
  target=root/rel
  if not target.resolve().is_relative_to(root.resolve()):raise RuntimeError('Source outside root')
  if sha(target) not in (h['before'],h['after']):raise RuntimeError('Source independently changed: '+rel)
  if sha(work/version/rel)!=h[version]:raise RuntimeError('Backup differs: '+rel)
 for rel,h in files.items():
  target=root/rel
  if h[version] is None:
   if target.exists():target.unlink()
  else:shutil.copy2(work/version/rel,target)

def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--check',action='store_true');g.add_argument('--activate',action='store_true');g.add_argument('--rollback',action='store_true');p.add_argument('--maintenance',action='store_true');a=p.parse_args()
 if os.name!='posix' or os.geteuid()!=0:p.error('Run with sudo python3 in WSL.')
 if not a.check and not a.maintenance:p.error('Arrange downtime and supply --maintenance.')
 import fcntl
 lock=(ROOT/'.hero-upcoming-build.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 s=json.loads((HERE/'build-state.json').read_text());work=Path(s['work']);assert work.resolve().is_relative_to(ROOT/'backups')
 w=inspect();assert w['Config']['Labels'].get('com.docker.compose.project')=='classless-test'
 assert not s['sourceRestorationErrors'] and s['status']=='compiled-not-activated'
 expected={'src/server/game/Entities/Player/Player.cpp'}
 assert set(s['files'])==expected,'Unexpected source scope'
 assert s['files']==json.loads((HERE/'source-manifest.json').read_text()),'Build differs from reviewed source manifest'
 for rel,h in s['files'].items():
  assert sha(work/'before'/rel)==h['before'] and sha(work/'after'/rel)==h['after'],'Build backup differs: '+rel
 def copy_source(version):restore_sources(ROOT,work,s['files'],version)
 def rollback():
  assert inspect()['Image'] in (s['previousImage'],s['builtImage'])
  for rel,h in s['files'].items():assert sha(ROOT/rel) in (h['before'],h['after'])
  run(['docker','stop',WORLD]);copy_source('before');compose(work/'starter-skill-rewards-rollback.json')
  ready(s['previousImage'],HERE/'rollback.log');assert inspect()['HostConfig']['PortBindings']==s['ports']
  save(HERE/'activation.json',{'phase':'rolled-back','image':s['previousImage']});print('ROLLBACK COMPLETE. Previous image/source restored; normal player progression and any reconciled spell rows are retained.')
 if a.rollback:
  assert sql('SELECT COUNT(*) FROM characters WHERE online=1;')=='0','Players online; arrange maintenance first'
  rollback();return
 if w['Image']==s['builtImage']:
  assert w['HostConfig']['PortBindings']==s['ports'],'Installed image has unexpected ports; stop for review'
  for rel,h in s['files'].items():assert sha(ROOT/rel)==h['after'],'Installed image source differs: '+rel
  assert w['Config']['Labels']['com.docker.compose.project.config_files']==str(work/'starter-skill-rewards-active.json'),'Installed image uses an unexpected compose configuration'
  ready(s['builtImage'],HERE/'already-active-check.log')
  print('ALREADY ACTIVE: Starter skill rewards image, source, ports and readiness verified. No restart or changes performed.')
  return
 assert w['Image']==s['previousImage'],'Live image changed since build; neither previous nor Starter skill rewards image is running. Stop for review.'
 assert w['HostConfig']['PortBindings']==s['ports'],'Live ports changed since build'
 for rel,h in s['files'].items():assert sha(ROOT/rel)==h['before'],'Live source changed since build: '+rel
 assert run(['docker','image','inspect','--format','{{.Id}}',s['tag']])==s['builtImage']
 live_config=w['Config']['Labels']['com.docker.compose.project.config_files']
 config=json.loads(run(['docker','compose','-p','classless-test','-f',s['activeConfig'],'config','--format','json']))
 old=copy.deepcopy(config);old['services']['ac-worldserver'].pop('build',None);old['services']['ac-worldserver']['image']=s['previousImage']
 if live_config!=s['activeConfig']:
  assert live_config==str(work/'starter-skill-rewards-rollback.json'),'Unexpected recovery configuration'
  recovery=json.loads((HERE/'activation.json').read_text())
  assert recovery.get('phase')=='rolled-back' and recovery.get('image')==s['previousImage']
  assert json.loads(run(['docker','compose','-p','classless-test','-f',live_config,'config','--format','json']))==old,'Recovery configuration changed'
 new=copy.deepcopy(old);new['services']['ac-worldserver']['image']=s['builtImage']
 private=copy.deepcopy(new);private['services']['ac-worldserver']['ports']=[]
 for name,data in [('rollback',old),('active',new),('private',private)]:
  path=work/('starter-skill-rewards-'+name+'.json');save(path,data);run(['docker','compose','-p','classless-test','-f',str(path),'config','--quiet'])
 if a.check:print('ACTIVATION CHECK PASSED. Image/source/ports verified. Server unchanged.');return
 assert sql('SELECT COUNT(*) FROM characters WHERE online=1;')=='0','Players online; log them out before activation'
 try:
  run(['docker','stop',WORLD]);copy_source('after')
  save(HERE/'activation.json',{'phase':'private-validation','image':s['builtImage']})
  compose(work/'starter-skill-rewards-private.json');ready(s['builtImage'],HERE/'private-startup.log')
  assert not inspect()['HostConfig']['PortBindings'],'Private startup unexpectedly published ports'
  compose(work/'starter-skill-rewards-active.json');ready(s['builtImage'],HERE/'startup.log')
  assert inspect()['HostConfig']['PortBindings']==s['ports'],'Published ports differ'
 except BaseException:
  rollback();raise
 save(HERE/'activation.json',{'phase':'active','image':s['builtImage'],'previousImage':s['previousImage'],'work':str(work)})
 print('ACTIVATION COMPLETE: Starter skill rewards temporary starter skill reward filter installed. No SQL migration or client installation. Obsolete saved starters will be reconciled on login. Previous image retained.')
if __name__=='__main__':main()
