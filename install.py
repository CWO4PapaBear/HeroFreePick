#!/usr/bin/env python3
"""Install into an explicitly selected WoW client, preserving a backup."""
from pathlib import Path
import argparse,datetime,hashlib,json,shutil
HERE=Path(__file__).resolve().parent

def hashes(root):return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--client',required=True,type=Path,help='WoW client directory containing Wow.exe');a=p.parse_args()
    client=a.client.resolve()
    if not (client/'Wow.exe').is_file():raise SystemExit('Selected directory does not contain Wow.exe')
    source=HERE/'HeroFreePick';expected=json.loads((HERE/'addon-manifest.json').read_text())
    if hashes(source)!=expected:raise SystemExit('Package differs from manifest. Run python build.py after intentional edits.')
    parent=client/'Interface'/'AddOns';parent.mkdir(parents=True,exist_ok=True);target=parent/'HeroFreePick'
    if target.is_symlink() or not target.resolve().is_relative_to(client):raise SystemExit('Redirected target is not supported')
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    staging=parent/('HeroFreePick-staging-'+stamp);shutil.copytree(source,staging)
    if hashes(staging)!=expected:raise SystemExit('Staging verification failed; installed addon unchanged')
    backup=client/'HeroFreePickBackups'/stamp
    if target.exists():
        backup.mkdir(parents=True);target.rename(backup/'HeroFreePick')
    try:staging.rename(target)
    except BaseException:
        if (backup/'HeroFreePick').exists():(backup/'HeroFreePick').rename(target)
        raise
    print('Installed:',target)
    print('Previous addon backup:',backup if backup.exists() else 'First installation')
    print('Restart the client when adding addon files; otherwise /reload. SavedVariables are unchanged.')
if __name__=='__main__':main()
