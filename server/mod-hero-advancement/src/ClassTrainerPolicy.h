#pragma once
#include <cstdint>
namespace HeroTrainer {
enum class Mode { Classic, ClassPlus, Hybrid, Hero, Pending };
inline bool Custom(Mode mode) { return mode!=Mode::Classic; }
inline bool BlockPurchase(Mode mode, unsigned trainerType) { return Custom(mode)&&trainerType==0; }
}
