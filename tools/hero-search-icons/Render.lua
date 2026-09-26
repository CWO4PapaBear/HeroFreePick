-- SearchResults already sorts by level, then name and ID. Keep that order.
local function renderSearchIcons(entries)
 local size,step=34,40
 local columns=math.max(1,math.floor((allScroll:GetWidth()-12)/step))
 for i,e in ipairs(entries)do
  local b=allButtons[i]
  if not b then
   b=CreateFrame('Button',nil,allContent);b:SetSize(size,size)
   b:RegisterForClicks('LeftButtonUp','RightButtonUp')
   b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints(b)
   b:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square')
   b:SetScript('OnEnter',tooltip);b:SetScript('OnLeave',leaveEntryTooltip)
   b:SetScript('OnClick',function(self,mouse)A.AdjustPending(self.entry,mouse=='RightButton'and -1 or 1)end)
   allButtons[i]=b
  end
  if not rawget(b,'classBadge')then
   b.classBadge=b:CreateTexture(nil,'OVERLAY');b.classBadge:SetSize(16,16)
   b.classBadge:SetPoint('BOTTOMRIGHT',b,'BOTTOMRIGHT',4,-4)
   b.classRing=b:CreateTexture(nil,'OVERLAY',nil,1)
   b.classRing:SetTexture('Interface\\AddOns\\HeroFreePick\\Art\\ClassRing')
   b.classRing:SetSize(20,20);b.classRing:SetPoint('CENTER',b.classBadge,'CENTER',0,0)
  end
  local path='Interface\\Icons\\'..(badges[e.class]or'INV_Misc_QuestionMark')
  if SetPortraitToTexture then SetPortraitToTexture(b.classBadge,path)else b.classBadge:SetTexture(path)end
  b.entry=e;b.icon:SetTexture(icon(e));updateMasteryBadge(b,e)
  b.icon:SetDesaturated(A.OtherClass(e.class)or UnitLevel('player')<(A.AbilityDisplayLevel(e)or 1))
  b:ClearAllPoints();b:SetPoint('TOPLEFT',6+((i-1)%columns)*step,-6-math.floor((i-1)/columns)*step);b:Show()
 end
 if #entries==0 then browseEmpty:Show()end
 allContent:SetHeight(math.max(417,12+math.ceil(#entries/columns)*step))
end

