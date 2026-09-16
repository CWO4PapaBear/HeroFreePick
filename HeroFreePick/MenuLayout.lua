HeroMenuLayout={frames={},defaults={},overrides=HeroMenuLayoutOverrides or {}}
local L=HeroMenuLayout
L.defaults['window']={parent='',x=0,y=0,w=1180,h=620}
L.defaults['header']={parent='window',x=48,y=7,w=1124,h=29}
L.defaults['close']={parent='window',x=1143,y=7,w=29,h=29}
L.defaults['info']={parent='window',x=1114,y=7,w=29,h=29}
L.defaults['abilities']={parent='window',x=25,y=135,w=451,h=433}
L.defaults['talents']={parent='window',x=483,y=135,w=334,h=433}
L.defaults['side']={parent='window',x=828,y=106,w=326,h=462}
L.defaults['abilitiesTitle']={parent='abilities',x=14,y=13,w=340,h=20}
L.defaults['talentsTitle']={parent='talents',x=14,y=13,w=306,h=20}
L.defaults['abilitiesScroll']={parent='abilities',x=10,y=39,w=409,h=373}
L.defaults['talentsScroll']={parent='talents',x=8,y=39,w=292,h=373}
L.defaults['talentsBar']={parent='talents',x=308,y=55,w=16,h=341}
L.defaults['learnedScroll']={parent='side',x=12,y=152,w=274,h=164}
L.defaults['primaryTitle']={parent='side',x=14,y=44,w=292,h=18}
L.defaults['searchBox']={parent='side',x=12,y=120,w=192,h=25}
L.defaults['filter']={parent='side',x=208,y=120,w=104,h=25}
L.defaults['points']={parent='window',x=25,y=573,w=265,h=30}
L.defaults['talentPoints']={parent='window',x=640,y=573,w=177,h=30}
L.defaults['rarityToggle']={parent='window',x=838,y=575,w=306,h=25}
L.defaults['resetAbilities']={parent='window',x=297,y=575,w=167,h=25}
L.defaults['resetTalents']={parent='window',x=468,y=575,w=167,h=25}
L.defaults['bottomHero']={parent='window',x=20,y=615,w=195,h=32}
L.defaults['bottomBuilder']={parent='window',x=207,y=615,w=195,h=32}
L.defaults['spec1']={parent='window',x=483,y=106,w=110,h=31}
L.defaults['spec2']={parent='window',x=595,y=106,w=110,h=31}
L.defaults['spec3']={parent='window',x=707,y=106,w=110,h=31}
L.defaults['spec4']={parent='window',x=25,y=106,w=150,h=31}
L.defaults['sideTab1']={parent='side',x=10,y=8,w=99,h=26}
L.defaults['sideTab2']={parent='side',x=111,y=8,w=99,h=26}
L.defaults['sideTab3']={parent='side',x=212,y=8,w=99,h=26}
L.defaults['statStrength']={parent='side',x=35,y=69,w=36,h=36}
L.defaults['statAgility']={parent='side',x=102,y=69,w=36,h=36}
L.defaults['statIntellect']={parent='side',x=169,y=69,w=36,h=36}
L.defaults['statSpirit']={parent='side',x=236,y=69,w=36,h=36}
L.defaults['rarityLegendary']={parent='side',x=10,y=329,w=302,h=28}
L.defaults['rarityEpic']={parent='side',x=10,y=358,w=302,h=28}
L.defaults['rarityRare']={parent='side',x=10,y=387,w=302,h=28}
L.defaults['rarityUncommon']={parent='side',x=10,y=416,w=302,h=28}
L.defaults['class1']={parent='window',x=25,y=43,w=100,h=63}
L.defaults['class2']={parent='window',x=127,y=43,w=100,h=63}
L.defaults['class3']={parent='window',x=229,y=43,w=100,h=63}
L.defaults['class4']={parent='window',x=331,y=43,w=100,h=63}
L.defaults['class5']={parent='window',x=433,y=43,w=100,h=63}
L.defaults['class6']={parent='window',x=535,y=43,w=100,h=63}
L.defaults['class7']={parent='window',x=637,y=43,w=100,h=63}
L.defaults['class8']={parent='window',x=739,y=43,w=100,h=63}
L.defaults['class9']={parent='window',x=841,y=43,w=100,h=63}
L.defaults['class10']={parent='window',x=943,y=43,w=100,h=63}
L.defaults['class11']={parent='window',x=1045,y=43,w=100,h=63}
function L.Bind(id,frame)if frame then L.frames[id]=frame end end
function L.Apply()
 for id,v in pairs(L.overrides)do
  local frame=L.frames[id];local d=L.defaults[id]
  if frame and d and type(v)=='table' then
   if id=='window' then frame:SetSize(v.w or d.w,v.h or d.h)
   else
    local parent=L.frames[d.parent]
    if parent then
     frame:ClearAllPoints();frame:SetPoint('TOPLEFT',parent,'TOPLEFT',v.x or d.x,-(v.y or d.y))
     frame:SetSize(v.w or d.w,v.h or d.h)
    end
   end
  end
 end
 if L.AfterApply then L.AfterApply()end
end
