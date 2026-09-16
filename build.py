#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parent

def main():
    addon=ROOT/'HeroFreePick'
    version=re.search(r'^## Version: (.+)$',(addon/'HeroFreePick.toc').read_text(),re.M).group(1).strip()
    files=sorted(p for p in addon.rglob('*') if p.is_file())
    manifest={p.relative_to(addon).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (ROOT/'addon-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    out=ROOT/'dist';out.mkdir(exist_ok=True)
    package=out/f'HeroFreePick-{version}.zip'
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.relative_to(ROOT))
    print(package)
if __name__=='__main__':main()
