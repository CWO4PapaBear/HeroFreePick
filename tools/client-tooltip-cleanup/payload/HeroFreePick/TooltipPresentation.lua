local A=HeroFreePick
-- Sentence spacing for Hero Advancement only. Decimal numbers and IDs are
-- untouched; color escapes remain attached to their text.
function A.TooltipParagraphs(text)
 if type(text)~='string'then return text end
 text=text:gsub('\r\n','\n')
 text=text:gsub('([.!?])(|r)[ \t\n]+','%1%2\n\n')
 text=text:gsub('([.!?])[ \t\n]+','%1\n\n')
 return text
end
function A.ShowAdvancementTooltip(tip)
 local name=tip:GetName()
 if name then
  for i=2,tip:NumLines()do
   for _,side in ipairs({'Left','Right'})do
    local line=_G[name..'Text'..side..i]
    if line and line:GetText()then
     local text=A.TooltipParagraphs(line:GetText())
     -- A following tooltip line starts on the next line already; one trailing
     -- newline leaves the requested blank line after a complete sentence.
     text=text:gsub('\n+$','')
     local plain=text:gsub('|c%x%x%x%x%x%x%x%x',''):gsub('|r','')
     if i<tip:NumLines()and plain:match('[.!?]$')then text=text..'\n'end
     line:SetText(text)
    end
   end
  end
 end
 tip:Show()
end
