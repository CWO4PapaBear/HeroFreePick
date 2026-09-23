from pathlib import Path
import subprocess,os,shlex
p=Path(__file__).resolve().parent
out=Path(os.environ.get('HERO_TEST_DIR',str(p/'test-output')));out.mkdir(parents=True,exist_ok=True)
helper=(p/'starter-policy-fixture.h').read_text()
overlay=p/'overlay/modules/mod-hero-starting-path/src/StartingPath.cpp'
if overlay.exists():assert helper in overlay.read_text()
source=r"""
#include <cassert>
#include <set>
#include <vector>
using uint32=unsigned;
struct Player{unsigned getClass(){return 4;}};
struct Spell{unsigned id;bool held;};
struct Snapshot{int phase=2;std::vector<Spell> spells={{1752,true},{2098,true},{674,false}};} snapshot;
namespace HeroBuild{using Build=std::set<unsigned>;}
namespace HeroStartingPath{bool Gated(unsigned,unsigned spell){return spell==1752||spell==2098;}}
struct Saved{bool valid=true,rebuild=false,migrating=false;HeroBuild::Build roots;} saved;
bool desiredOK=true;
Snapshot Read(Player*){return snapshot;}
Saved LoadBuild(Player*){return saved;}
bool Desired(Player*,HeroBuild::Build const& roots,HeroBuild::Build& wanted){wanted=roots;return desiredOK;}
"""+helper+r"""
int main(){
 Player player;auto p=&player;
 assert(HeroShouldSkipSavedStarter(p,1752));assert(HeroShouldSkipSavedStarter(p,2098));
 assert(!HeroShouldSkipSavedStarter(p,674));assert(!HeroShouldSkipSavedStarter(nullptr,1752));
 saved.roots.insert(1752);assert(!HeroShouldSkipSavedStarter(p,1752));assert(HeroShouldSkipSavedStarter(p,2098));
 for(int phase:{-2,-1,1}){snapshot.phase=phase;assert(!HeroShouldSkipSavedStarter(p,2098));}
 snapshot.phase=0;assert(HeroShouldSkipSavedStarter(p,1752));snapshot.phase=2;
 saved.valid=false;assert(!HeroShouldSkipSavedStarter(p,2098));saved.valid=true;
 saved.rebuild=true;assert(!HeroShouldSkipSavedStarter(p,2098));saved.rebuild=false;
 saved.migrating=true;assert(!HeroShouldSkipSavedStarter(p,2098));saved.migrating=false;
 desiredOK=false;assert(!HeroShouldSkipSavedStarter(p,2098));desiredOK=true;
 snapshot.spells.clear();assert(!HeroShouldSkipSavedStarter(p,2098));
}
"""
(out/'test.cpp').write_text(source)
subprocess.run(shlex.split(os.environ.get('CXX','c++'))+['-std=c++17',str(out/'test.cpp'),'-o',str(out/'test.exe')],check=True)
subprocess.run([str(out/'test.exe')],check=True)
print('PASS: actual starter ownership filter; purchased, Classic, unavailable data and migration cases.')
