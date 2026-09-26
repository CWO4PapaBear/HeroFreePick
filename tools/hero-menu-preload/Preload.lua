-- Warm immutable art only. Never render menus or change preparation state.
do
 local worker=CreateFrame('Frame',nil,UIParent)
 worker:SetSize(1,1);worker:SetPoint('TOPLEFT',UIParent,'TOPLEFT',0,0)
 worker:SetAlpha(0);worker:EnableMouse(false)
 local seen,textures={},{}
 local status={loaded=0,complete=false};A.MenuPreloadStatus=status
 local function warm(path)
  if type(path)~='string' or path=='' or seen[path]then return end
  seen[path]=true
  local texture=worker:CreateTexture(nil,'BACKGROUND')
  texture:SetAllPoints(worker);texture:SetTexture(path)
  textures[#textures+1]=texture;status.loaded=#textures
  coroutine.yield()
 end
 local function load()
  -- Tree backgrounds are large and unique to each specialization.
  for _,base in pairs(nativeBackgrounds)do
   for _,part in ipairs({'TopLeft','TopRight','BottomLeft','BottomRight'})do
    warm('Interface\\TalentFrame\\'..base..'-'..part)
   end
  end
  for _,e in ipairs(HeroFreePickCatalog or {})do
   warm(icon(e))
   -- Also warm custom-mode art before the player has chosen a mode.
   warm(e.referenceIcon)
   if e.catalogOnly and e.icon then warm('Interface\\Icons\\'..e.icon)end
   if e.spells and e.spells[1]then
    warm(A.PackageSpellIcons and A.PackageSpellIcons[e.spells[1]])
   end
   -- Bound traversal even when many entries share a texture.
   coroutine.yield()
  end
  status.complete=true
 end
 local job,delay
 worker:RegisterEvent('PLAYER_ENTERING_WORLD');worker:RegisterEvent('PLAYER_LEAVING_WORLD')
 worker:SetScript('OnEvent',function(self,event)
  if event=='PLAYER_LEAVING_WORLD'then self:Hide();return end
  if status.complete or status.error then return end
  job=job or coroutine.create(load);delay=.5;self:Show()
 end)
 worker:SetScript('OnUpdate',function(self,elapsed)
  if not job or (InCombatLockdown and InCombatLockdown())then return end
  delay=delay-elapsed;if delay>0 then return end
  local start=debugprofilestop and debugprofilestop()
  -- At most two work units per frame; stop sooner at a 1ms soft budget.
  for i=1,2 do
   local ok,err=coroutine.resume(job)
   if not ok then status.error=tostring(err);self:SetScript('OnUpdate',nil);return end
   if coroutine.status(job)=='dead'then self:SetScript('OnUpdate',nil);return end
   if start and debugprofilestop()-start>=1 then return end
  end
 end)
 worker:Hide()
end
