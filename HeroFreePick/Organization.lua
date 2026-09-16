local A=HeroFreePick
A.view='browse';A.ownership='All';A.spec='All'
function A.VisibleEntries(kind)
    local out={}
    for _,e in ipairs(A.Results())do
        local talent=e.kind=='Talent' or e.kind=='TalentAbility'
        local planned=(HeroFreePickPlans.entries[e.id] or 0)>0
        if (kind=='talent' and talent or kind=='ability' and not talent)
            and (A.ownership=='All' or A.ownership=='Planned' and planned or A.ownership=='Not planned' and not planned)then
            out[#out+1]=e
        end
    end
    table.sort(out,function(a,b)
        if a.level~=b.level then return a.level<b.level end
        local ac=(HeroFreePickLayout[a.id]or{}).column or 0
        local bc=(HeroFreePickLayout[b.id]or{}).column or 0
        if kind=='talent' and ac~=bc then return ac<bc end
        if a.name~=b.name then return a.name<b.name end
        return a.id<b.id
    end)
    return out
end
function A.PlannedEntries()
    local out={}
    for id,rank in pairs(HeroFreePickPlans.entries)do
        local e=A.byID[id]
        if e and rank>0 then out[#out+1]=e end
    end
    table.sort(out,function(a,b)if a.level~=b.level then return a.level<b.level end;if a.class~=b.class then return a.class<b.class end;return a.id<b.id end)
    return out
end
-- Reference-level grouping is presentation, not an enforced leveling sequence.
function A.LevelGroups(entries)
    local groups={}
    for _,e in ipairs(entries)do
        local last=groups[#groups]
        if not last or last.level~=e.level then last={level=e.level,entries={}};groups[#groups+1]=last end
        last.entries[#last.entries+1]=e
    end
    return groups
end
