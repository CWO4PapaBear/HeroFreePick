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
    # Every profile and server mode is independently downloadable.
    components=[('Classic-addon', [addon]),('server-foundation',[ROOT/'server/mod-hero-advancement'])]
    for mode,folder in [('ClassPlus','mod-hero-classplus'),('Hybrid','mod-hero-hybrid'),('Hero','mod-hero-freepick')]:
        components.append((mode+'-preview-addon',[ROOT/'profiles'/('HeroAdvancement_'+mode)]))
        components.append((mode+'-server-policy',[ROOT/'server'/folder]))
    components.append(('Area52-talent-importer',[ROOT/'tools/talents']))
    components.append(('ClassPlus-enrollment-runtime',[ROOT/'server/mod-hero-starting-path',ROOT/'profiles/HeroStartingPathTest',ROOT/'profiles/HeroClassPlusCommitTest']))
    components.append(('complete-development-bundle',[addon,*sorted((ROOT/'profiles').iterdir()),*sorted(p for p in (ROOT/'server').iterdir()if p.name.startswith('mod-'))]))
    for label,folders in components:
        package=out/f'HeroAdvancement-{label}-{version}.zip'
        with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED)as z:
            for folder in folders:
                for p in sorted(folder.rglob('*')):
                    if p.is_file()and '__pycache__'not in p.parts and p.suffix not in ('.pyc','.pyo'):z.write(p,Path(folder.name)/p.relative_to(folder))
            z.write(ROOT/'docs/MODULES.md','INSTALL-MODULES.md')
        print(package.name)
if __name__=='__main__':main()
