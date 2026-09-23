from pathlib import Path
import sys, tempfile, shutil, subprocess, json, hashlib
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
HERE=Path(__file__).resolve().parent
l=LuaRuntime()
for p in (HERE/'payload').glob('*.lua'):
    l.execute('assert(loadstring(...))',p.read_text())
l.execute('''
frames={};combat=false;buttons={};sent={};local methods={}
function methods:SetScript(k,v)self.scripts[k]=v end
function methods:GetScript(k)return self.scripts[k]end
function methods:HookScript(k,fn)local old=self.scripts[k];self.scripts[k]=function(...)if old then old(...)end;fn(...)end end
function methods:SetAttribute(k,v)self[k]=v end
function methods:GetEffectiveScale()return self.scale or 1 end
function methods:GetLeft()return 40 end
function methods:GetTop()return 150 end
function methods:GetHeight()return 200 end
function methods:SetPoint(...)self.point={...}end
function methods:StartMoving()self.moving=true end
function methods:StopMovingOrSizing()self.moving=false end
function CreateFrame(_,name)
 local f=setmetatable({scripts={}},{__index=function(t,k)
  if methods[k]then return methods[k]end
  if k:match('^Set')or k:match('^Register')or k:match('^Clear')then return function()end end
 end});frames[#frames+1]=f;if name then _G[name]=f end;return f
end
UIParent=CreateFrame('Frame');HeroIntegratedResourceTest=CreateFrame('Frame')
HeroLivePet1=CreateFrame('Frame');HeroLivePet2=CreateFrame('Frame');TargetFrame=CreateFrame('Frame')
FocusFrame=CreateFrame('Frame');TargetFrameHealthBar=CreateFrame('Frame');TargetFrameManaBar=CreateFrame('Frame');FocusFrameHealthBar=CreateFrame('Frame');FocusFrameManaBar=CreateFrame('Frame')
HeroFreePick={mode='Classic'}
function SecureUnitButton_OnLoad(self,unit,fn)self:SetAttribute('*type1','target');self:SetAttribute('*type2','menu');self:SetAttribute('unit',unit);self.menu=fn end
function FocusFrameDropDown_Initialize()lastMenu={'FOCUS','focus'}end
function InCombatLockdown()return combat end
function UIDropDownMenu_CreateInfo()return {} end
function UIDropDownMenu_AddButton(b)buttons[#buttons+1]=b end
function UIDropDownMenu_Initialize(f,fn)f.init=fn end
function ToggleDropDownMenu(_,__,f)buttons={};f.init(f,1)end
function UnitPopup_ShowMenu(_,kind,unit)lastMenu={kind,unit}end
function TargetFrameDropDown_Initialize()lastMenu={'TARGET','target'}end
function SendChatMessage(s)sent[#sent+1]=s end
''')
source=(HERE/'payload/AdditionalResources.lua').read_text()
# Exercise the actual player drag helper and secure setup, without rendering.
l.execute(source.split('local panel=',1)[0] + '\nHeroTestDrag=playerDrag')
l.execute("SecureUnitButton_OnLoad(HeroLivePet1,'pet',function()end)")
l.execute((HERE/'payload/PortraitControls.lua').read_text())
l.execute('''
local event=frames[#frames]
event.scripts.OnEvent();assert(not HeroPlayerPortraitDropDown)
HeroFreePick.mode='Hybrid';event.scripts.OnUpdate(event,1.1)
assert(HeroPortraitSettings.player.locked and HeroPortraitSettings.target.locked)
assert(HeroIntegratedResourceTest.point[4]==3 and HeroIntegratedResourceTest.point[5]==-2)
HeroLivePet1.menu();assert(lastMenu[1]=='PET'and lastMenu[2]=='pet')
HeroLivePet2.scripts.OnMouseUp(HeroLivePet2,'RightButton');buttons[#buttons].func()
assert(sent[1]=='.demon dismiss')
TargetFrame.scripts.OnDragStart(TargetFrame);assert(not TargetFrame.moving)
TargetFrame.menu();assert(lastMenu[1]=='TARGET');buttons[#buttons].func()
assert(not HeroPortraitSettings.target.locked)
TargetFrame.scripts.OnDragStart(TargetFrame);assert(TargetFrame.moving)
TargetFrame.scale=.8;TargetFrame.scripts.OnDragStop(TargetFrame)
assert(HeroPortraitSettings.target.x==32 and HeroPortraitSettings.target.y==-80)
event.scripts.OnEvent();assert(TargetFrame.point[4]==40 and TargetFrame.point[5]==-100)
assert(HeroIntegratedResourceTest['*type2']=='menu'and HeroLivePet1['*type2']=='menu')
FocusFrame.scripts.OnDragStart(FocusFrame);assert(not FocusFrame.moving)
FocusFrame.menu();assert(lastMenu[1]=='FOCUS');buttons[#buttons].func()
FocusFrameHealthBar.scripts.OnDragStart();assert(FocusFrame.moving)
FocusFrameHealthBar.scripts.OnDragStop();assert(HeroPortraitSettings.focus.x==40)
TargetFrameManaBar.scripts.OnDragStart();assert(TargetFrame.moving);TargetFrameManaBar.scripts.OnDragStop()
HeroIntegratedResourceTest.menu();buttons[#buttons].func()
HeroIntegratedResourceTest.scripts.OnDragStart();assert(HeroIntegratedResourceTest.moving)
HeroIntegratedResourceTest.scripts.OnDragStop();assert(HeroPortraitSettings.player.x==40)
local resourceBar=CreateFrame('Frame');HeroTestDrag(resourceBar)
resourceBar.scripts.OnDragStart();assert(HeroIntegratedResourceTest.moving);resourceBar.scripts.OnDragStop()
combat=true;resourceBar.scripts.OnDragStart();assert(not HeroIntegratedResourceTest.moving)
FocusFrameManaBar.scripts.OnDragStart();assert(not FocusFrame.moving)
TargetFrame.scripts.OnDragStart(TargetFrame);assert(not TargetFrame.moving)
HeroIntegratedResourceTest.menu();assert(buttons[#buttons].disabled)
''')
# Exercise the real installer in a temporary client, with a reviewed synthetic baseline.
from contextlib import nullcontext
import uuid
with nullcontext(HERE / ('test-output-' + uuid.uuid4().hex)) as tmp:
    t=Path(tmp);pkg=t/'package';shutil.copytree(HERE/'payload',pkg/'payload')
    shutil.copy2(HERE/'Install-Client.py',pkg/'Install-Client.py')
    addon=t/'client/Interface/AddOns/HeroClassPlusCommitTest';addon.mkdir(parents=True)
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,h in manifest.items():
        (addon/name).write_text('prior version')
        h['before']=hashlib.sha256((addon/name).read_bytes()).hexdigest()
    (pkg/'manifest.json').write_text(json.dumps(manifest))
    args=[sys.executable,str(pkg/'Install-Client.py'),'--client',str(t/'client'),'--wow-closed']
    subprocess.run(args,check=True,capture_output=True)
    for name,h in manifest.items():assert hashlib.sha256((addon/name).read_bytes()).hexdigest()==h['after']
    assert 'ALREADY INSTALLED' in subprocess.check_output(args,text=True)
    (addon/'PortraitControls.lua').write_text('independent edit')
    assert subprocess.run(args,capture_output=True).returncode!=0
    assert (addon/'PortraitControls.lua').read_text()=='independent edit'
source=(HERE/'payload/AdditionalResources.lua').read_text()
assert 'RuneFrame:SetParent(stockRuneHolder)'in source and 'RuneFrame:SetParent(stockRuneParent)'in source
assert 'b:SetSize(143,11)'in source and 'HeroSavePortraitPosition' in source
assert "SecureUnitButton_OnLoad(card,'pet',card.menu)" in source and 'togglemenu' not in source
assert 'playerDrag(b)' in source and 'playerDrag(header)' in source
toc=(HERE/'payload/HeroClassPlusCommitTest.toc').read_text()
assert toc.index('AdditionalResources.lua')<toc.index('PortraitControls.lua')
assert '## SavedVariablesPerCharacter: HeroPortraitSettings' in toc
print('PASS: Lua 5.1 syntax, delayed custom-mode setup, native pet menu, secondary commands, locks, combat guard, scaled position persistence; installer hashes, backups, idempotence and drift rejection.')


