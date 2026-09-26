"""Guarded PTR Warrior stance activation; no SQL writes or client installation."""
from pathlib import Path
import argparse,copy,hashlib,json,os,shutil,subprocess,time
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/dml/games/wow-server-classless-test')
WORLD='classless-test-worldserver';DB='classless-test-database'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def save(p,data):p.write_text(json.dumps(data,indent=2)+'\n');os.chmod(p,0o600)
def run(args):
 p=subprocess.run(args,capture_output=True,timeout=180)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
 return p.stdout.decode(errors='replace')
def inspect():return json.loads(run(['docker','inspect',WORLD]))[0]
def query(sql,database='acore_world'):
 return run(['docker','exec','-i',DB,'sh','-c','MYSQL_PWD="${MYSQL_ROOT_PASSWORD:-$MARIADB_ROOT_PASSWORD}" mysql -uroot --default-character-set=utf8mb4 --batch --skip-column-names "$1" -e "$2"','warrior-read',database,sql]).strip()
def compose(path):run(['docker','compose','-p','classless-test','-f',str(path),'up','-d','--no-deps','--no-build','--force-recreate','ac-worldserver'])
def ready(image,new,label):
 deadline=time.monotonic()+600
 while time.monotonic()<deadline:
  w=inspect();p=subprocess.run(['docker','logs',WORLD],capture_output=True,timeout=30)
  logs=(p.stdout+p.stderr).decode(errors='replace');(HERE/(label+'.log')).write_text(logs)
  assert w['Image']==image and w['State']['Running'],'Unexpected world state; review '+label+'.log'
  if any(('validation failed' in line.lower() or 'baseline mismatch' in line.lower() or 'must rollback' in line.lower()) and ('HERO_' in line or 'MORE_MINIONS' in line) for line in logs.splitlines()):raise RuntimeError('Module validation failed; review '+label+'.log')
  markers=['HERO_STARTING_PATH ready','HERO_SHARED_PROGRESSION v1 ready','HERO_MARTIAL_FLUIDITY v1 ready','Adaptive Auto Attack: module loaded']
  if new:markers.append('HERO_WARRIOR_STANCES v1 ready; 12 ranks;')
  if all(m in logs for m in markers):
   p=subprocess.run(['docker','exec',WORLD,'bash','-c','exec 3<>/dev/tcp/127.0.0.1/8085'],capture_output=True)
   if p.returncode==0:return
  print('Waiting for PTR readiness...',flush=True);time.sleep(5)
 raise RuntimeError('Startup timed out; review '+label+'.log')
def main():
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--check',action='store_true');g.add_argument('--activate',action='store_true');g.add_argument('--rollback',action='store_true')
 p.add_argument('--maintenance',action='store_true');p.add_argument('--client-ready',action='store_true');a=p.parse_args()
 if os.name!='posix' or os.geteuid()!=0:p.error('Run with sudo python3 in WSL.')
 if not a.check and not a.maintenance:p.error('Arrange maintenance and supply --maintenance.')
 if a.activate and not a.client_ready:p.error('Install the matching client for testing, then supply --client-ready.')
 import fcntl
 lock=(ROOT/'.hero-upcoming-build.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 s=json.loads((HERE/'build-state.json').read_text());work=Path(s['work'])
 assert work.resolve().is_relative_to(ROOT/'backups') and not s['sourceRestorationErrors'] and s['status']=='compiled-not-activated'
 w=inspect();assert w['Config']['Labels'].get('com.docker.compose.project')=='classless-test'
 assert s['files']==json.loads((HERE/'source-manifest.json').read_text()),'C++ changed: rebuild required'
 for rel,h in s['files'].items():
  assert sha(work/'before'/rel)==h['before'] and sha(work/'after'/rel)==h['after'] and sha(HERE/'candidate'/rel)==h['after'],rel
 def sources(version):
  for rel,h in s['files'].items():assert sha(ROOT/rel) in (h['before'],h['after']),'Source independently changed: '+rel
  for rel,h in s['files'].items():
   if h[version] is None:(ROOT/rel).unlink(missing_ok=True)
   else:shutil.copy2(work/version/rel,ROOT/rel)
 def rollback():
  assert inspect()['Image'] in (s['previousImage'],s['builtImage'])
  old=work/'warrior-rollback.json';assert old.exists()
  run(['docker','stop',WORLD]);sources('before');compose(old);ready(s['previousImage'],False,'rollback')
  assert inspect()['HostConfig']['PortBindings']==s['ports']
  save(HERE/'activation.json',dict(phase='rolled-back',image=s['previousImage']))
  print('ROLLBACK COMPLETE: previous PTR image, source and DBC mounts restored.')
 if a.rollback:
  assert query('SELECT COUNT(*) FROM characters WHERE online=1;','acore_characters')=='0','Players online'
  rollback();return
 assert w['Image']==s['previousImage'],'PTR image changed; review before activation'
 assert w['HostConfig']['PortBindings']==s['ports'],'PTR ports changed'
 assert w['Config']['Labels']['com.docker.compose.project.config_files']==s['activeConfig'],'Compose changed; review before activation'
 for rel,h in s['files'].items():assert sha(ROOT/rel)==h['before'],'Source changed: '+rel
 assert run(['docker','image','inspect','--format','{{.Id}}',s['tag']]).strip()==s['builtImage']
 # Recheck live SQL collisions, including overrides introduced after the snapshot.
 ids='100,6178,11578,6343,8198,8204,8205,11580,11581,25264,47501,47502,9905301'
 assert query('SELECT COUNT(*) FROM spell_dbc WHERE ID IN ('+ids+');')=='0','Spell override collision'
 assert query('SELECT COUNT(*) FROM spell_script_names WHERE ABS(spell_id)=9905301;')=='0','Spell binding collision'
 assert query('SELECT COUNT(*) FROM spell_dbc WHERE SpellClassSet=4 AND ((SpellClassMask_3 | EffectSpellClassMaskC_1 | EffectSpellClassMaskC_2 | EffectSpellClassMaskC_3) & 536870912)<>0;')=='0','SQL family-mask collision'
 run(['docker','cp',WORLD+':/azerothcore/env/dist/data/dbc/Spell.dbc',str(work/'Spell-current.dbc')])
 m=json.loads((HERE/'candidate/manifest.json').read_text())
 assert sha(work/'Spell-current.dbc')==m['spellBefore']==s['spellBefore'],'Live DBC changed'
 assert sha(HERE/'candidate/Spell.dbc')==m['spellAfter']
 # Data is separately staged from compilation. Pin the final reviewed DBC now;
 # the C++ manifest must still exactly match the compiled source above.
 shutil.copy2(HERE/'candidate/Spell.dbc',work/'Spell-activation.dbc');os.chmod(work/'Spell-activation.dbc',0o644)
 old=json.loads(run(['docker','compose','-p','classless-test','-f',s['activeConfig'],'config','--format','json']))
 old['services']['ac-worldserver'].pop('build',None);old['services']['ac-worldserver']['image']=s['previousImage']
 new=copy.deepcopy(old);service=new['services']['ac-worldserver'];service['image']=s['builtImage']
 target='/azerothcore/env/dist/data/dbc/Spell.dbc'
 assert not any(v.get('target')==target for v in service.get('volumes',[])),'Existing per-file DBC mount requires reconciliation'
 service.setdefault('volumes',[]).append(dict(type='bind',source=str(work/'Spell-activation.dbc'),target=target,read_only=True))
 private=copy.deepcopy(new);private['services']['ac-worldserver']['ports']=[]
 for name,config in (('rollback',old),('private',private),('active',new)):
  path=work/('warrior-'+name+'.json');save(path,config);run(['docker','compose','-p','classless-test','-f',str(path),'config','--quiet'])
 save(HERE/'activation-preflight.json',dict(status='passed',image=s['builtImage'],spellHash=m['spellAfter']))
 if a.check:print('ACTIVATION CHECK PASSED. Image/source/DBC/SQL collisions verified; no restart or live writes.');return
 client=Path('/mnt/d/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
 client_manifest=json.loads((HERE/'client-manifest.json').read_text())
 assert set(client_manifest)=={'Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'}
 for rel,h in client_manifest.items():assert sha(client/rel)==h['after'],'Matching local client not installed: '+rel
 assert query('SELECT COUNT(*) FROM characters WHERE online=1;','acore_characters')=='0','Players online; arrange maintenance'
 try:
  run(['docker','stop',WORLD]);sources('after')
  compose(work/'warrior-private.json');ready(s['builtImage'],True,'private-startup')
  assert not inspect()['HostConfig']['PortBindings'],'Private validation exposed ports'
  compose(work/'warrior-active.json');ready(s['builtImage'],True,'startup')
  assert inspect()['HostConfig']['PortBindings']==s['ports']
 except BaseException:rollback();raise
 save(HERE/'activation.json',dict(phase='active',image=s['builtImage'],previousImage=s['previousImage'],spellHash=m['spellAfter']))
 print('ACTIVATION COMPLETE: Charge/Thunder Clap stance exemption for Class+, Hybrid and Hero. Classic unchanged. No SQL migration. Previous image and DBC mounts retained for rollback.')
if __name__=='__main__':main()
