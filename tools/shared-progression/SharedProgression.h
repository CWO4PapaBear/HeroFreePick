#pragma once
#include "SharedProgressionCurve.h"
class Player;
struct PlayerLevelInfo;
struct PlayerClassLevelInfo;
void HeroSharedProgressionLoad();
bool HeroSharedProgressionApply(Player const*, unsigned, PlayerLevelInfo&, PlayerClassLevelInfo&);
bool HeroSharedProgressionRefresh(Player*);
