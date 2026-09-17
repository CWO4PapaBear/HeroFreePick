local A=HeroFreePick
local window=HeroFreePickFrame
local dialog=CreateFrame('Frame','HeroPendingChangesDialog',UIParent)
A.PendingDialog=dialog
-- Full-window mouse shield keeps the review modal while preserving the pending menu.
dialog:SetAllPoints(UIParent);dialog:SetFrameStrata('FULLSCREEN_DIALOG');dialog:SetFrameLevel(500);dialog:EnableMouse(true)
local box=CreateFrame('Frame',nil,dialog);box:SetSize(650,440);box:SetPoint('CENTER');box:EnableMouse(true)
box:SetBackdrop({bgFile='Interface\\DialogFrame\\UI-DialogBox-Background',edgeFile='Interface\\DialogFrame\\UI-DialogBox-Border',tile=true,tileSize=32,edgeSize=32,insets={left=11,right=11,top=11,bottom=11}})
local title=box:CreateFontString(nil,'OVERLAY','GameFontNormalLarge');title:SetPoint('TOP',0,-24);title:SetText('Pending Hero Advancement Changes')
local body=box:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');body:SetPoint('TOPLEFT',26,-58);body:SetSize(598,295);body:SetJustifyH('LEFT');body:SetJustifyV('TOP')
local message=box:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');message:SetPoint('BOTTOMLEFT',26,65);message:SetSize(598,38);message:SetTextColor(1,.65,.2);message:SetJustifyH('LEFT')
local function button(text,x,fn)
 local b=CreateFrame('Button',nil,box,'UIPanelButtonTemplate');b:SetSize(185,26);b:SetPoint('BOTTOMLEFT',x,26);b:SetText(text);b:SetScript('OnClick',fn);return b
end
local closing=false
local function finish()
 closing=true;dialog:Hide();window:Hide();closing=false
end
function A.ShowPendingReview()
 local lines={'Review the proposed resources below. No changes have been learned.',''}
 for _,section in ipairs(A.PendingSummary())do
  lines[#lines+1]=(section.key=='entries'and 'Archetype draft'or 'Hero Advancement')..': +'..section.added..' / -'..section.removed..' ranks'
  for _,q in ipairs({'AP','TP','Uncommon','Rare','Epic','Legendary'})do
   local before=section.before[q];local after=section.after[q];local delta=after-before
   lines[#lines+1]=(q=='AP'and 'Ability Points'or q=='TP'and 'Talent Points'or q)..': '..before..' -> '..after..' ('..(delta>=0 and '+'or '')..delta..')'
  end
  lines[#lines+1]=''
 end
 local base=HeroFreePickPlans.pendingBaseline
 if base and base.primaryStat~=HeroFreePickPlans.primaryStat then lines[#lines+1]='Primary stat: '..tostring(base.primaryStat or 'None')..' -> '..tostring(HeroFreePickPlans.primaryStat or 'None')end
 body:SetText(table.concat(lines,'\n'))
 message:SetText('Server committing is not available yet. Accept will retain these pending changes.')
 dialog:Show()
end
function A.RequestClose()
 if A.HasPendingChanges()then A.ShowPendingReview();return false end
 if HeroFreePickPlans then HeroFreePickPlans.pendingBaseline=nil end
 finish();return true
end
A.PendingAcceptButton=button('Accept Changes',27,function()
 local ok,reason=A.AcceptPreparation()
 if ok then finish()else message:SetText(reason)end
end)
A.PendingBackButton=button('Go Back',232,function()dialog:Hide();window:Show()end)
A.PendingCancelButton=button('Cancel Changes',437,function()A.CancelPreparation();A.Refresh();finish()end)
if HeroFreePickFrameClose then HeroFreePickFrameClose:SetScript('OnClick',A.RequestClose)end
-- Escape and inherited close actions use Hide directly; intercept them as well.
window:SetScript('OnHide',function()
 if closing then return end
 if A.HasPendingChanges()then window:Show();A.ShowPendingReview()
 elseif HeroFreePickPlans then HeroFreePickPlans.pendingBaseline=nil end
end)
dialog:Hide()
