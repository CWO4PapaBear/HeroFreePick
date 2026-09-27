"""Install the reviewed local Grappling Hook client payload with verified backups."""
from pathlib import Path
import ctypes,datetime,hashlib,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def main():
    assert os.name=='nt','Run using Windows Python'
    running=json.loads(subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process Wow -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id) | ConvertTo-Json -Compress"],capture_output=True,text=True,check=True).stdout or '[]')
    assert not running,'Close WoW before installing'
    manifest=json.loads((HERE/'client-manifest.json').read_text())
    for rel,h in manifest.items():
        assert (CLIENT/rel).resolve().is_relative_to(CLIENT.resolve())
        assert sha(CLIENT/rel)==h['before'],'Client changed; reconcile: '+rel
        assert sha(HERE/'client-candidate'/rel)==h['after'],'Payload changed: '+rel
    backup=HERE/'client-backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup.mkdir(parents=True,exist_ok=False)
    for rel,h in manifest.items():
        if h['before'] is not None:
            dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(CLIENT/rel,dst)
            assert sha(dst)==h['before']
    (backup/'manifest.json').write_text(json.dumps(manifest,indent=2))
    written=[]
    try:
        for rel,h in manifest.items():
            dst=CLIENT/rel;dst.parent.mkdir(parents=True,exist_ok=True);written.append(rel)
            shutil.copy2(HERE/'client-candidate'/rel,dst)
            assert sha(dst)==h['after']
    except BaseException:
        for rel in reversed(written):
            if manifest[rel]['before'] is None:(CLIENT/rel).unlink(missing_ok=True)
            else:shutil.copy2(backup/rel,CLIENT/rel)
        raise
    (HERE/'client-install.json').write_text(json.dumps(dict(status='installed',backup=str(backup),files=manifest),indent=2))
    print('LOCAL CLIENT INSTALL COMPLETE. Four files verified; backups: '+str(backup))
if __name__=='__main__':main()
