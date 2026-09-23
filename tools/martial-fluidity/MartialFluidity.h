#pragma once
class Player;
class Unit;
bool HeroMartialFluidityEnabled(Unit const*);
void HeroMartialFluiditySend(Unit*);
void HeroMartialFluidityLogin(Player*);
void HeroMartialFluidityLoad();
void AddHeroMartialFluidityScripts();
