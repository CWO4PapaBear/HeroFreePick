"""Install only the two reviewed Warrior MPQs, with backups and rollback."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def closed():
 if os.name!='nt':raise RuntimeError('Run this installer with Windows Python.')
 p=subprocess.run(['powershell.exe','-NoProfile','-Command',"if (Get-Process Wow -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"],capture_output=True)
 if p.returncode:raise RuntimeError('Close WoW before installing.')
def install(root,source,manifest,backup,guard=closed):
 assert set(manifest)=={'Data/patch-Z.MPQ','Data/enUS/patch-enUS-Z.MPQ'}
 for rel,h in manifest.items():
  assert sha(source/rel)==h['after'],'Candidate differs: '+rel
  assert sha(root/rel) in (h['before'],h['after']),'Client changed: '+rel
 guard();changed=[]
 try:
  for rel,h in manifest.items():
   target=root/rel
   if sha(target)==h['after']:continue
   guard();old=backup/rel;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,old)
   assert sha(old)==h['before'] and sha(target)==h['before']
   temp=target.with_name(target.name+'.warrior-new')
   try:
    shutil.copy2(source/rel,temp);assert sha(temp)==h['after']
    guard();assert sha(target)==h['before'];temp.replace(target);changed.append(rel)
   finally:temp.unlink(missing_ok=True)
   assert sha(target)==h['after']
 except BaseException:
  for rel in reversed(changed):shutil.copy2(backup/rel,root/rel)
  raise
 return changed
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 m=json.loads((HERE/'client-manifest.json').read_text())
 for rel,h in m.items():assert sha(HERE/'client-candidate'/rel)==h['after'] and sha(CLIENT/rel) in (h['before'],h['after']),rel
 closed()
 if a.check:print('CLIENT PREFLIGHT PASSED: closed and hashes match. No installation.');return
 backup=HERE/'client-backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
 changes=install(CLIENT,HERE/'client-candidate',m,backup)
 (HERE/'client-install.json').write_text(json.dumps(dict(status='installed',backup=str(backup),changed=changes,files=m),indent=2)+'\n')
 print('CLIENT INSTALLED: Warrior stance patch; both archives verified. Backup:',backup)
if __name__=='__main__':main()
