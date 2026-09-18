#pragma once
#include <cstdint>
#include <string>
namespace HeroStartingPath {
// Reviewed stock level-one active class spells. Never infer this list from all
// known spells: that would also remove racial abilities and core proficiencies.
struct Starter { std::uint8_t klass; std::uint32_t spell; char const* name; };
constexpr Starter Starters[] = {
    {1,78,"Heroic Strike"}, {1,2457,"Battle Stance"},
    {2,635,"Holy Light"}, {2,21084,"Seal of Righteousness"},
    {3,2973,"Raptor Strike"}, {3,75,"Auto Shot"},
    {4,1752,"Sinister Strike"}, {4,2098,"Eviscerate"},
    {5,2050,"Lesser Heal"}, {5,585,"Smite"},
    {7,331,"Healing Wave"}, {7,403,"Lightning Bolt"},
    {8,168,"Frost Armor"}, {8,133,"Fireball"},
    {9,687,"Demon Skin"}, {9,686,"Shadow Bolt"},
    {11,5185,"Healing Touch"}, {11,5176,"Wrath"},
    {6,45902,"Blood Strike"}, {6,48266,"Blood Presence"}, {6,45477,"Icy Touch"},
    {6,56816,"Rune Strike"}, {6,45462,"Plague Strike"}, {6,47541,"Death Coil"}, {6,49576,"Death Grip"}
};
inline bool Gated(std::uint8_t klass, std::uint32_t spell) {
    for (auto const& s : Starters) if (s.klass==klass && s.spell==spell) return true;
    return false;
}
inline bool Eligible(std::string const& /*name*/, std::uint8_t klass, std::uint8_t level) {
    if (level!=(klass==6?55:1)) return false;
    for (auto const& s : Starters) if (s.klass==klass) return true;
    return false;
}
// Pending=0, Classic=1, ClassPlus=2. Switching is allowed only at level one.
inline bool CanChoose(unsigned level, unsigned phase, unsigned klass) { return level==(klass==6?55u:1u) && (phase==1 || phase==2); }
}
