from pathlib import Path
import argparse,shlex,subprocess
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True,help='Patched Player.cpp')
p.add_argument('--cxx',default='c++',help='C++ compiler command')
p.add_argument('--output',type=Path,required=True,help='Directory for generated test source and executable')
a=p.parse_args()
source=a.source.read_text()
assert 'cd <= m_regenTimer && getClass() != CLASS_DEATH_KNIGHT && HeroResourcesNeedsRunes(this)' in source
start=source.index('    // Runes act as cooldowns',source.index('void Player::RegenerateAll()'))
end=source.index('    if (m_regenTimerCount >= 2000)',start)
body=source[start:end]
cpp=r'''
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <vector>
using uint8=uint8_t;using uint32=uint32_t;using int32=int32_t;
constexpr int CLASS_DEATH_KNIGHT=6,CLASS_CONTEXT_ABILITY=0,MAX_RUNES=6,RUNE_GRACE_PERIOD=2500;
struct Player;bool HeroResourcesNeedsRunes(Player const*);
struct Player {
 int native=4;bool eligible=true,combat=true;uint32 m_regenTimer=100;
 uint32 cooldown[6]={},grace[6]={};std::vector<int> notifications;
 bool IsClass(int,int){return native==6||eligible;}int getClass(){return native;}
 uint32 GetRuneCooldown(int i){return cooldown[i];}
 void SetRuneCooldown(int i,uint32 v){cooldown[i]=v;}
 bool IsInCombat(){return combat;}uint32 GetGracePeriod(int i){return grace[i];}
 void SetGracePeriod(int i,uint32 v){grace[i]=v;}
 void AddRunePower(int i){assert(cooldown[i]==0);notifications.push_back(i);}
 void tick(){ BODY }
};
bool HeroResourcesNeedsRunes(Player const* p){return p->eligible;}
int main(){
 Player p;p.cooldown[0]=10000;p.cooldown[2]=10001;
 for(int i=0;i<99;++i)p.tick();assert(p.notifications.empty());
 p.tick();assert(p.cooldown[0]==0&&p.cooldown[2]==1);
 assert(p.notifications==std::vector<int>{0});p.tick();assert((p.notifications==std::vector<int>{0,2}));
 for(int i=0;i<100;++i)p.tick();assert(p.notifications.size()==2);
 p.cooldown[0]=100;p.tick();assert(p.notifications.size()==3);
 Player native;native.native=6;native.cooldown[0]=100;native.tick();assert(native.cooldown[0]==0&&native.notifications.empty());
 Player denied;denied.eligible=false;denied.cooldown[0]=100;denied.tick();assert(denied.cooldown[0]==100&&denied.notifications.empty());
 Player idle;idle.combat=false;idle.cooldown[5]=1;idle.tick();assert(idle.notifications==std::vector<int>{5});assert(idle.grace[5]==0);
 Player early;early.cooldown[1]=0;early.tick();assert(early.notifications.empty());
 Player death;death.cooldown[3]=50;death.tick();assert(death.notifications==std::vector<int>{3});
}
'''.replace('BODY',body)

out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
(out/'test.cpp').write_text(cpp)
subprocess.run(shlex.split(a.cxx)+['-std=c++17',str(out/'test.cpp'),'-o',str(out/'test.exe')],check=True)
subprocess.run([str(out/'test.exe')],check=True)
print('PASS: actual regeneration block readiness notification tests')
