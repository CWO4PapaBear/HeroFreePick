#pragma once
#include <cstdint>
class Player;

// Optional module callbacks. With no provider installed, stock behavior is unchanged.
// Register once during script initialization, before sessions begin.
namespace HeroGrapplingHooks
{
using Resolver = uint32_t (*)(Player*, uint32_t);
inline Resolver& CastResolver() { static Resolver value = nullptr; return value; }
inline Resolver& ActionResolver() { static Resolver value = nullptr; return value; }
inline uint32_t Cast(Player* player, uint32_t spell)
{
    return CastResolver() ? CastResolver()(player, spell) : spell;
}
inline uint32_t Action(Player* player, uint32_t spell)
{
    return ActionResolver() ? ActionResolver()(player, spell) : spell;
}
}
