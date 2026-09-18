#include "../mod-hero-advancement/src/ClassTrainerPolicy.h"
#include <cassert>
#include <initializer_list>
int main(){using namespace HeroTrainer;
 for(auto mode:{Mode::ClassPlus,Mode::Hybrid,Mode::Hero,Mode::Pending}){
  assert(BlockPurchase(mode,0));for(unsigned type=1;type<=3;++type)assert(!BlockPurchase(mode,type));
 }
 for(unsigned type=0;type<=3;++type)assert(!BlockPurchase(Mode::Classic,type));
}
