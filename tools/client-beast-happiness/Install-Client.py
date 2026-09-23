"""Install only the reviewed More Minions stable compatibility. Close WoW first."""
import argparse, datetime, hashlib, json, shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--wow-closed',action='store_true')
    p.add_argument('--client',type=Path,default=Path('/mnt/d/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test'))
    a=p.parse_args()
    if not a.wow_closed:p.error('Close WoW completely, then supply --wow-closed.')
    addon=a.client/'Interface/AddOns'
    if not addon.is_dir():p.error('Client addon folder not found; use --client with the WoW folder.')
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,h in manifest.items():
        assert sha(HERE/'payload'/name)==h['after'],'Package differs: '+name
        assert sha(addon/name) in (h['before'],h['after']),'Client changed since review: '+name
    pending=[n for n,h in manifest.items() if sha(addon/n)!=h['after']]
    if not pending:
        print('STABLE PET PORTRAIT ALREADY INSTALLED. No changes.');return
    backup=HERE/'backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True)
    for name in pending:
        if (addon/name).exists():
            (backup/name).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(addon/name,backup/name)
    changed=[]
    try:
        for name in pending:
            tmp=addon/(name+'.tooltip-new')
            shutil.copy2(HERE/'payload'/name,tmp)
            changed.append(name);tmp.replace(addon/name)
            assert sha(addon/name)==manifest[name]['after']
    except BaseException:
        for name in reversed(changed):
            if (backup/name).exists():shutil.copy2(backup/name,addon/name)
            else:(addon/name).unlink(missing_ok=True)
        raise
    (backup/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (HERE/'installation.json').write_text(json.dumps({'status':'installed','backup':str(backup)},indent=2)+'\n')
    print('STABLE PET PORTRAIT COMPLETE. Live primary pet portrait replaces the fallback whistle icon.')
    print('Backup:',backup)
    print('No server, spellbook, MPQ or launcher publication changes.')
if __name__=='__main__':main()
