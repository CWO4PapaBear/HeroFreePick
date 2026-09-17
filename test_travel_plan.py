"""Validate the integration specification; this does not test server travel."""
from pathlib import Path
import json

policy=json.loads((Path(__file__).resolve().parent/'docs/hero-travel-destinations.json').read_text())
rows={row['id']:row for row in policy['destinations']}
assert set(rows)==set(range(2,162))
assert len(policy['masteries'])==2
assert {m['kind'] for m in policy['masteries']}=={'portal','teleport'}
assert all(m['abilityPoints']==2 and m['uncommonGems']==1 for m in policy['masteries'])
assert rows[18]['level']==rows[90]['level']==25
assert rows[102]['level']==62 and rows[37]['level']==72
races={'Human':'Alliance','Dwarf':'Alliance','Gnome':'Alliance','NightElf':'Alliance','Draenei':'Alliance',
       'Orc':'Horde','Troll':'Horde','Tauren':'Horde','Scourge':'Horde','BloodElf':'Horde'}
for race,faction in races.items():
    for level in range(1,81):
        eligible=[d for d in rows.values() if d['enabled'] and d['faction'] in (faction,'Neutral')
                  and level >= (10 if race in d['racialCapitalRaces'] else d['level'])]
        assert all(d['faction'] in (faction,'Neutral') for d in eligible)
        if level<10: assert not eligible
        if 10<=level<15: assert len(eligible)==1 and race in eligible[0]['racialCapitalRaces']
        if level>=15: assert sum(bool(d['racialCapitalRaces']) for d in eligible)==4
assert rows[23]['accessConditions']=={'questStartedOrRewarded':12905}
assert rows[36]['accessConditions']=={'questRewarded':13141}
assert rows[43]['accessConditions']=={'anyOf':[{'questStartedOrRewarded':12924},{'questRewarded':12967}]}
assert rows[129]['accessConditions']=={'questRewardedByFaction':{'Alliance':12896,'Horde':12897}}
assert policy['reagentRule']['consume'] is False
assert policy['reagentRule']['teleportRewardItem']==17031
assert policy['reagentRule']['portalRewardItem']==17032
assert policy['reagentRule']['quantity']==1
print('PASS: 160 destinations, Acherus excluded, ten races across levels 1–80, faction/capital gates, independent mastery costs and reward item specification.')
