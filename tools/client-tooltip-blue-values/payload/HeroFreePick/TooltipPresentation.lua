local A=HeroFreePick
-- Light blue distinguishes resolved values from yellow implementation warnings.
function A.TooltipValueColors(text)
 if A.mode=='Classic'or type(text)~='string'or text:find('|T',1,true)or text:find('|H',1,true)or text:find('Spell ID',1,true)or text:find('Character Advancement ID',1,true)then return text end
 local out={};local start=1;local colored=false
 local function append(chunk)
  if not colored then
   chunk=chunk:gsub('(%d[%d,]*%.?%d*%%?)',function(value)
    local punctuation=''
    if value:sub(-1)=='.'then value=value:sub(1,-2);punctuation='.'end
    return '|cff80cfff'..value..'|r'..punctuation
   end)
  end
  out[#out+1]=chunk
 end
 while start<=#text do
  local first,last,code=text:find('(|c%x%x%x%x%x%x%x%x)',start)
  local resetFirst,resetLast=text:find('|r',start,true)
  if resetFirst and(not first or resetFirst<first)then first,last,code=resetFirst,resetLast,'|r'end
  if not first then append(text:sub(start));break end
  append(text:sub(start,first-1));out[#out+1]=code
  colored=code~='|r';start=last+1
 end
 return table.concat(out)
end
-- Sentence spacing for Hero Advancement only. Decimal numbers and IDs are
-- untouched; color escapes remain attached to their text.
function A.TooltipParagraphs(text,keepColor)
 if type(text)~='string'then return text end
 text=text:gsub('\r\n','\n')
 text=text:gsub('([.!?])(|r)[ \t\n]+','%1%2\n\n')
 text=text:gsub('([.!?])[ \t\n]+','%1\n\n')
 return keepColor and text or A.TooltipValueColors(text)
end
function A.ShowAdvancementTooltip(tip)
 local name=tip:GetName()
 if name then
  for i=2,tip:NumLines()do
   for _,side in ipairs({'Left','Right'})do
    local line=_G[name..'Text'..side..i]
    if line and line:GetText()then
     local r,g,b=line:GetTextColor()
     -- Respect warning/requirement lines colored through the FontString itself.
     local keepColor=r and(r>0.8 and g>0.45 and b<0.5)
     local text=A.TooltipParagraphs(line:GetText(),keepColor)
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
