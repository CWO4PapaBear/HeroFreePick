bool HeroShouldSkipSavedStarter(Player* p,uint32 spell){
 if(!p||!HeroStartingPath::Gated(p->getClass(),spell))return false;
 auto snapshot=Read(p);
 if(snapshot.phase!=0&&snapshot.phase!=2)return false;
 bool held=false;for(auto const& s:snapshot.spells)if(s.id==spell&&s.held)held=true;
 if(!held)return false;
 if(snapshot.phase==0)return true;
 auto build=LoadBuild(p);HeroBuild::Build wanted;
 // Do not delete saved rows when ownership cannot be verified or migration is pending.
 if(!build.valid||build.rebuild||build.migrating||!Desired(p,build.roots,wanted))return false;
 return !wanted.count(spell);
}
