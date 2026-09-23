
#pragma once
#include <array>
#include <vector>
#include <memory>
#include <cstdint>
#include <algorithm>
using int16=std::int16_t; using uint8=std::uint8_t;
enum Stats { STR, AGI, STA, INT, SPI }; enum Powers { POWER_MANA };
struct PlayerLevelInfo { unsigned stats[5]{}; };
struct PlayerClassLevelInfo { unsigned basehealth=0,basemana=0; };
namespace HeroTrainer { enum class Mode {Classic,ClassPlus,Hybrid,Hero,Pending}; }
class Player {
public:
 HeroTrainer::Mode mode=HeroTrainer::Mode::Hero;
 unsigned level=1,race=1, health=25,mana=30,maxhealth=100,maxmana=100,basehealth=0,basemana=0,updates=0;
 unsigned stats[5]{}; unsigned gear=17;
 unsigned GetLevel()const{return level;} unsigned getRace(bool)const{return race;}
 unsigned GetCreateStat(Stats s)const{return stats[s];} void SetCreateStat(Stats s,unsigned n){stats[s]=n;}
 unsigned GetCreateHealth()const{return basehealth;} unsigned GetCreateMana()const{return basemana;}
 void SetCreateHealth(unsigned n){basehealth=n;} void SetCreateMana(unsigned n){basemana=n;}
 unsigned GetHealth()const{return health;} unsigned GetPower(Powers)const{return mana;}
 unsigned GetMaxHealth()const{return maxhealth;} unsigned GetMaxPower(Powers)const{return maxmana;}
 void SetHealth(unsigned n){health=n;} void SetPower(Powers,unsigned n){mana=n;}
 void UpdateAllStats(){++updates;maxhealth=basehealth+20+10*(stats[STA]-20)+gear;maxmana=basemana+20+15*(stats[INT]-20)+gear;}
};
namespace HeroTrainer { inline Mode Current(Player const* p){return p->mode;} }
struct Field {int n;template<class T>T Get()const{return T(n);}};
struct Result {std::vector<std::array<Field,6>> rows;unsigned index=0;Field* Fetch(){return rows[index].data();}bool NextRow(){return ++index<rows.size();}};
inline bool missingRace=false;
struct DB {std::shared_ptr<Result> Query(char const*){auto r=std::make_shared<Result>();for(int id:{1,2,3,4,5,6,7,8,10,11})if(!missingRace||id!=11)r->rows.push_back({Field{id},Field{1},Field{-2},Field{3},Field{0},Field{4}});return r;}};
inline DB WorldDatabase;
#define LOG_INFO(...) ((void)0)
#define LOG_ERROR(...) ((void)0)
