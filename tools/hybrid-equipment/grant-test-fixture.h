void KeepHybridEquipment(Player* p,HeroBuild::Build& keep){
 auto mask=HeroEquipmentClassMask(p);if(mask==p->getClassMask())return;
 for(auto const& profile:HeroEquipment::Proficiencies){
  if(!HeroEquipment::Available(profile,mask,p->GetLevel()))continue;
  keep.insert(profile.spell);
 }
}
bool VerifyHybridEquipment(Player* p){
 auto mask=HeroEquipmentClassMask(p);if(mask==p->getClassMask())return true;
 for(auto const& profile:HeroEquipment::Proficiencies){
  if(!HeroEquipment::Available(profile,mask,p->GetLevel()))continue;
  if(!p->HasSpell(profile.spell))return false;
  // Do not reset trained skill or award max skill just for choosing a class.
  auto value=p->GetPureSkillValue(profile.skill);
  unsigned cap=profile.weapon?p->GetMaxSkillValueForLevel():1;
  if(!value)p->SetSkill(profile.skill,0,1,cap);
  else if(profile.weapon&&p->GetPureMaxSkillValue(profile.skill)<cap)p->SetSkill(profile.skill,0,value,cap);
  if(!p->HasSkill(profile.skill))return false;
 }
 return true;
}
