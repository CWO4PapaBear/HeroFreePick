from pathlib import Path
import runpy, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    context=runpy.run_path(str(Path(__file__).with_name('test_ui.py')))
lua=context['lua'];root=context['root']
lua.execute((root/'TrainerGate.lua').read_text())
lua.execute("""
local A=HeroFreePick
local seen={};local n=0
for _,e in ipairs(A.AscensionAbilities)do
 n=n+1;assert(not seen[e.id]);seen[e.id]=true
 assert(e.ae>0 and e.te==0 and e.level>=1 and e.level<=80)
 assert(e.referenceDescription and #e.referenceDescription>0 and not e.referenceDescription:find('$',1,true))
 assert(e.referenceIcon:find('Art',1,true) and e.serverPending)
 assert(HeroRarityCosts[e.id]==e.rarityCost)
 A.mode='Classic';assert(not A.EntryAvailableInMode(e))
 for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
  A.mode=mode;assert(A.EntryAvailableInMode(e));assert(A.EntryIcon(e)==e.referenceIcon)
 end
end
assert(n==65)
local e=A.byID[26001189];assert(e.name=='Brilliance Aura' and e.ae==2 and e.level==1 and e.rarityCost==2 and e.quality=='Rare')
local key='N';GetBindingKey=function()return key end;GetBindingText=function(k)return k end
assert(A.ClassTrainerDialogueText():find('(N)',1,true))
key='CTRL-N';assert(A.ClassTrainerDialogueText():find('(CTRL-N)',1,true))
key=nil;assert(A.ClassTrainerDialogueText():find('No keyboard shortcut',1,true))
local closed=0;CloseTrainer=function()closed=closed+1 end
ClassTrainerFrame={};HideUIPanel=function()end
local greeting='Profession Trainer';GetTrainerGreetingText=function()return greeting end
for _,mode in ipairs({'ClassPlus','Hybrid','Hero'})do
 A.mode=mode;A.TrainerDialogue:Hide()
 HeroAdvancementTrainerEvents.scripts.OnEvent(nil,'TRAINER_SHOW');assert(not A.TrainerDialogue:IsShown())
 greeting='HF_CLASS_TRAINER: message';HeroAdvancementTrainerEvents.scripts.OnEvent(nil,'TRAINER_SHOW');assert(A.TrainerDialogue:IsShown())
 greeting='Profession Trainer'
end
A.mode='Classic';A.TrainerDialogue:Hide();greeting='HF_CLASS_TRAINER: message'
HeroAdvancementTrainerEvents.scripts.OnEvent(nil,'TRAINER_SHOW');assert(not A.TrainerDialogue:IsShown());assert(not A.ShowClassTrainerDialogue())
assert(closed==3)
print('PASS: 65 unique custom previews, costs/descriptions/icons, Classic isolation; class/profession trainer routing and rebound/unbound hotkeys.')
""")
for e in lua.globals().HeroFreePick.AscensionAbilities.values():
    rel=e['referenceIcon'].split('HeroFreePick\\',1)[1].replace('\\','/')+'.blp'
    assert (root/rel).is_file(),rel
