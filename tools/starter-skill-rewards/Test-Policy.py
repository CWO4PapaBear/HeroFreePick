from pathlib import Path
import subprocess,os,shlex
p=Path(__file__).resolve().parent
out=Path(os.environ.get('HERO_TEST_DIR',str(p/'test-output')));out.mkdir(parents=True,exist_ok=True)
helper=(p/'starter-policy-fixture.h').read_text()
overlay=p/'overlay/modules/mod-hero-starting-path/src/StartingPath.cpp'
if overlay.exists():assert helper in overlay.read_text()
branch=(p/'grant-branch-fixture.h').read_text()
core=p/'overlay/src/server/game/Entities/Player/Player.cpp'
if core.exists():assert branch in core.read_text()
source=r"""
#include <cassert>
#include <set>
#include <vector>
using uint32=unsigned;
struct Player{unsigned getClass(){return 4;} bool world=false;int grants=0;bool IsInWorld(){return world;}void addSpell(unsigned,int,bool,bool){++grants;}void learnSpell(unsigned,bool,bool){++grants;}void reward(unsigned);};
constexpr int SPEC_MASK_ALL=255;
struct Spell{unsigned id;bool held;};
struct Snapshot{int phase=2;std::vector<Spell> spells={{1752,true},{2098,true},{674,false}};} snapshot;
namespace HeroBuild{using Build=std::set<unsigned>;}
namespace HeroStartingPath{bool Gated(unsigned,unsigned spell){return spell==1752||spell==2098;}}
struct Saved{bool valid=true,rebuild=false,migrating=false;HeroBuild::Build roots;} saved;
bool desiredOK=true;
Snapshot Read(Player*){return snapshot;}
Saved LoadBuild(Player*){return saved;}
bool Desired(Player*,HeroBuild::Build const& roots,HeroBuild::Build& wanted){wanted=roots;return desiredOK;}
"""+helper+"\nvoid Player::reward(unsigned spell){struct Ability{unsigned Spell;} ability{spell};auto pAbility=&ability;for(int once=0;once<1;++once){\n"+branch+"\n}}\n"+r"""
int main(){
 Player player;auto p=&player;
 // No saved spell rows involved: both consecutive default-skill passes must be blocked.
 p->reward(1752);p->reward(2098);p->reward(1752);p->reward(2098);assert(p->grants==0);
 p->reward(674);assert(p->grants==1);
 saved.roots.insert(1752);p->reward(1752);assert(p->grants==2);saved.roots.clear();
 snapshot.phase=1;p->reward(2098);assert(p->grants==3);snapshot.phase=2;
 p->world=true;p->reward(2098);assert(p->grants==4);p->world=false;

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
print('PASS: actual pre-world grant branch and ownership filter; repeated logins, purchased starters, Classic and unchanged in-world routing.')
