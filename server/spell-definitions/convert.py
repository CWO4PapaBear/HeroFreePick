#!/usr/bin/env python3
"""Offline Ascension Spell.dbc -> reviewed AzerothCore spell_dbc SQL. No DB connection."""
import argparse, copy, hashlib, json, math, re, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDED = {901018}
FLOAT_FIELDS = {47, *range(77,80), *range(101,104), *range(119,122), *range(216,219), *range(229,232)}
SIGNED_FIELDS = {0,13,15,41,*range(52,71),*range(74,77),*range(80,83),*range(110,116),224,228}
TEXT_FIELDS = {*range(136,152),*range(153,169),*range(170,186),*range(187,203)}

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def field_index(column, ordinal):
    match = re.fullmatch(r'EffectSpellClassMask([ABC])_([123])', column)
    if match:
        return 122 + 3*(int(match[2])-1) + 'ABC'.index(match[1])
    return ordinal

def convert(record, columns):
    raw = record['rawUInt32Fields']
    if len(raw) != 234 or any(type(x) is not int or not 0 <= x < 2**32 for x in raw):
        raise ValueError('Invalid raw spell row')
    if record['id'] != raw[0] or record['id'] in EXCLUDED:
        raise ValueError('Excluded or mismatched spell ID')
    result = {}
    for ordinal, column in enumerate(columns):
        i = field_index(column['name'], ordinal)
        value = raw[i]
        if i in TEXT_FIELDS:
            value = record['localizedStrings'][str(i)]
            if not isinstance(value,str): raise ValueError('Invalid localized string')
            limit = column.get('maxLength')
            if limit and len(value) > limit:
                raise ValueError(f"{record['id']} {column['name']} exceeds {limit} characters; source retained without truncation")
        elif i in FLOAT_FIELDS:
            value = struct.unpack('<f',struct.pack('<I',value))[0]
            if not math.isfinite(value): raise ValueError('Non-finite float')
        elif i in SIGNED_FIELDS and value >= 2**31:
            value -= 2**32
        result[column['name']] = value
    return result

def literal(value):
    # Hex UTF-8 is independent of NO_BACKSLASH_ESCAPES and preserves newlines/quotes.
    if isinstance(value,str):
        return "CONVERT(X'" + value.encode('utf-8').hex() + "' USING utf8mb4)"
    if isinstance(value,float): return format(value,'.17g')
    return str(value)

def schema_guard(columns):
    conditions=[]
    for c in columns:
        condition=f"COLUMN_NAME='{c['name']}' AND DATA_TYPE='{c['dataType']}'"
        if c['dataType'] in ('int','bigint'):
            condition += " AND (LOCATE('unsigned',COLUMN_TYPE)>0)=" + str(int(c['unsigned']))
        if c.get('maxLength'): condition += ' AND CHARACTER_MAXIMUM_LENGTH='+str(c['maxLength'])
        conditions.append('('+condition+')')
    return """  IF (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='spell_dbc') <> 234
     OR (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='spell_dbc' AND ("""+' OR '.join(conditions)+""")) <> 234 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='spell_dbc schema differs from packaged mapping';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='spell_dbc' AND ENGINE='InnoDB') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='InnoDB spell_dbc required for atomic import';
  END IF;
"""

def compatibility_issues(rows):
    issues=[]
    for row in rows:
        bad={}
        for prefix,limit in [('Effect_',165),('EffectAura_',317),('ImplicitTargetA_',111),('ImplicitTargetB_',111)]:
            for slot in range(1,4):
                name=prefix+str(slot)
                if row[name] >= limit:bad[name]=row[name]
        if bad:issues.append({'id':row['ID'],'name':row['Name_Lang_enUS'],'outOfRangeFields':bad})
    return issues

def compatible_selection(source):
    """Conservative closure: tooltip links can also exclude a root; never claim gameplay readiness."""
    records={r['id']:r for r in source['records']}
    blocked={i for i,r in records.items() if any(v>=165 for v in r['rawUInt32Fields'][71:74]) or any(v>=317 for v in r['rawUInt32Fields'][95:98]) or any(v>=111 for v in r['rawUInt32Fields'][86:92])}
    direct=set(blocked)
    while True:
        more={i for i,r in records.items() if any(d['id'] in blocked or (not d['presentInBaseline'] and d['id'] not in records) for d in r['dependencies'])}-blocked
        if not more: break
        blocked.update(more)
    roots=set(source['rootIDs'])-blocked
    selected=set(roots);queue=list(roots)
    while queue:
        r=records[queue.pop()]
        for d in r['dependencies']:
            if not d['presentInBaseline'] and d['id'] not in selected:
                selected.add(d['id']);queue.append(d['id'])
    report={'selectedRoots':sorted(roots),'selectedRecords':sorted(selected),'excludedRoots':[{'id':i,'name':records[i]['name'],'reason':'unsupported enum' if i in direct else 'reference dependency blocked'} for i in sorted(set(source['rootIDs'])&blocked)],'note':'Conservative trigger/aura/tooltip closure. Auxiliary DBC references and runtime effects remain unverified.'}
    return [records[i] for i in sorted(selected)],report

def generate_sql(rows, columns, batch):
    names=','.join('`'+c['name']+'`' for c in columns)
    ids=','.join(str(r['ID']) for r in rows)
    receipt='hf_spell_receipt_'+batch
    apply='hf_spell_apply_'+batch
    undo='hf_spell_undo_'+batch
    header="-- Generated definition candidates only. See README before applying.\n-- Use mysql on the selected WORLD database; never --force. Back up first.\nSET NAMES utf8mb4;\nSET SESSION sql_mode = CONCAT_WS(',', @@sql_mode, 'STRICT_ALL_TABLES');\n"
    body=header+f'DROP PROCEDURE IF EXISTS `{apply}`;\nDELIMITER //\nCREATE PROCEDURE `{apply}`()\nBEGIN\n  DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;\n'
    issues=compatibility_issues(rows)
    if issues:
        body+="  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Unsupported source effect/aura/target IDs; adapt before installation';\n"
    body+=schema_guard(columns)
    # DDL precedes transaction. An empty receipt can remain after a failed attempt.
    body+=f'  CREATE TABLE IF NOT EXISTS `{receipt}` LIKE `spell_dbc`;\n  START TRANSACTION;\n'
    body+=f"  IF EXISTS (SELECT 1 FROM `{receipt}`) OR EXISTS (SELECT 1 FROM `spell_dbc` WHERE ID IN ({ids})) THEN\n    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Import collision or existing receipt; no spell rows changed';\n  END IF;\n"
    body+='  INSERT INTO `spell_dbc` ('+names+') VALUES\n'+',\n'.join('('+','.join(literal(r[c['name']]) for c in columns)+')' for r in rows)+';\n'
    body+=f'  INSERT INTO `{receipt}` ({names}) SELECT {names} FROM `spell_dbc` WHERE ID IN ({ids});\n  COMMIT;\nEND//\nCALL `{apply}`()//\nDROP PROCEDURE `{apply}`//\nDELIMITER ;\n'
    comparisons=[]
    for c in columns:
        n='`'+c['name']+'`'
        comparisons.append(f'BINARY s.{n} <=> BINARY r.{n}' if c['dataType'] in ('varchar','text') else f's.{n} <=> r.{n}')
    equal=' AND '.join('('+x+')' for x in comparisons)
    rollback=header+f'DROP PROCEDURE IF EXISTS `{undo}`;\nDELIMITER //\nCREATE PROCEDURE `{undo}`()\nBEGIN\n  DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;\n'
    rollback+=schema_guard(columns)
    rollback+=f"  START TRANSACTION;\n  SELECT s.ID FROM `spell_dbc` s JOIN `{receipt}` r ON s.ID=r.ID FOR UPDATE;\n  IF (SELECT COUNT(*) FROM `{receipt}`) <> {len(rows)} OR (SELECT COUNT(*) FROM `spell_dbc` s JOIN `{receipt}` r ON s.ID=r.ID WHERE {equal}) <> {len(rows)} THEN\n    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Receipt missing or imported rows changed; rollback refused';\n  END IF;\n  DELETE s FROM `spell_dbc` s JOIN `{receipt}` r ON s.ID=r.ID;\n  DELETE FROM `{receipt}`;\n  COMMIT;\nEND//\nCALL `{undo}`()//\nDROP PROCEDURE `{undo}`//\nDELIMITER ;\n"
    return body,rollback

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,default=ROOT/'data')
    p.add_argument('--output',type=Path,default=ROOT/'generated')
    p.add_argument('--include-dependencies',action='store_true',help='Also convert preserved non-stock reference dependencies (review required)')
    p.add_argument('--compatible-only',action='store_true',help='Exclude unsupported enums and roots referencing them; include remaining reference closure')
    p.add_argument('--server-spell-dbc',type=Path,help='Optional installer Spell.dbc for fresh ID collision detection')
    a=p.parse_args()
    manifest=read_json(a.data/'manifest.json')
    for filename,digest in manifest['files'].items():
        if hashlib.sha256((a.data/filename).read_bytes()).hexdigest()!=digest:
            raise ValueError('Reference checksum mismatch: '+filename)
    source=read_json(a.data/'spells.json');columns=read_json(a.data/'schema.json')['columns']
    if len(columns)!=234 or len({c['name'] for c in columns})!=234: raise ValueError('Expected 234 unique columns')
    records=source['records'] if a.include_dependencies else [r for r in source['records'] if r['id'] in source['rootIDs']]
    selection=None
    if a.compatible_only: records,selection=compatible_selection(source)
    if not records: raise ValueError('No records selected')
    records=sorted(records,key=lambda r:r['id'])
    if len({r['id'] for r in records})!=len(records):raise ValueError('Duplicate spell IDs')
    if a.server_spell_dbc:
        b=a.server_spell_dbc.read_bytes();magic,n,fields,stride,strings=struct.unpack_from('<4s4I',b)
        if magic!=b'WDBC' or stride!=936 or len(b)!=20+n*stride+strings:raise ValueError('Invalid server Spell.dbc')
        existing={struct.unpack_from('<I',b,20+i*stride)[0] for i in range(n)}
        collision=existing&{r['id'] for r in records}
        if collision:raise ValueError('Server DBC ID collisions: '+str(sorted(collision)))
    original_columns=copy.deepcopy(columns)
    widened=[]
    for c in columns:
        if not c.get('maxLength'): continue
        required=max(len(r['localizedStrings'][str(c['sourceField'])]) for r in records)
        if required > c['maxLength']:
            widened.append({'name':c['name'],'oldLength':c['maxLength'],'newLength':required})
            c['maxLength']=required
    rows=[convert(r,columns) for r in records]
    payload=json.dumps(rows,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    batch=hashlib.sha256(payload.encode()).hexdigest()[:16]
    apply,rollback=generate_sql(rows,columns,batch)
    a.output.mkdir(parents=True,exist_ok=True)
    for name,text in [('rows.json',payload),('apply.review.sql',apply),('rollback.sql',rollback)]:
        (a.output/name).write_text(text,encoding='utf-8',newline='\n')
    for name in ['schema-required.review.sql','schema-restore.review.sql']:
        (a.output/name).write_text('-- No schema adjustment required for this selection.\n',encoding='utf-8')
    if widened:
        widen_name='hf_spell_widen_'+batch
        widen="-- Separate prerequisite: expands text storage without truncating source text.\nDELIMITER //\nCREATE PROCEDURE `"+widen_name+"`()\nBEGIN\n"+schema_guard(original_columns)
        for c in widened:
            widen+=f"  ALTER TABLE `spell_dbc` MODIFY COLUMN `{c['name']}` varchar({c['newLength']}) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;\n"
        widen+=f"END//\nCALL `{widen_name}`()//\nDROP PROCEDURE `{widen_name}`//\nDELIMITER ;\n"
        (a.output/'schema-required.review.sql').write_text(widen,encoding='utf-8',newline='\n')
        restore_name='hf_spell_restore_'+batch
        restore="-- Optional AFTER successful row rollback; refuses to truncate other data.\nDELIMITER //\nCREATE PROCEDURE `"+restore_name+"`()\nBEGIN\n"+schema_guard(columns)
        for c in widened:
            restore+=f"  IF EXISTS (SELECT 1 FROM `spell_dbc` WHERE CHAR_LENGTH(`{c['name']}`)>{c['oldLength']}) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Text exceeds original capacity; schema restore refused'; END IF;\n"
        for c in widened:
            restore+=f"  ALTER TABLE `spell_dbc` MODIFY COLUMN `{c['name']}` varchar({c['oldLength']}) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;\n"
        restore+=f"END//\nCALL `{restore_name}`()//\nDROP PROCEDURE `{restore_name}`//\nDELIMITER ;\n"
        (a.output/'schema-restore.review.sql').write_text(restore,encoding='utf-8',newline='\n')
    issues=compatibility_issues(rows)
    (a.output/'compatibility.json').write_text(json.dumps({'unsupportedEnumRecords':issues,'limits':{'effects':165,'auras':317,'targets':111},'note':'In-range values are not proof of implemented behavior. All spell effects/dependencies still require testing.'},indent=2)+'\n',encoding='utf-8')
    if selection:
        (a.output/'selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
    summary={'compatibleOnly':a.compatible_only,'unsupportedEnumRecords':len(issues),'schemaWidening':widened,'batch':batch,'rootCount':len(source['rootIDs']),'selectedCount':len(rows),'excludedIDs':sorted(EXCLUDED),'dependenciesIncluded':a.include_dependencies,'serverDBCCollisionChecked':bool(a.server_spell_dbc),'sourceManifest':manifest,'status':'Definition candidates. Not deployed or gameplay validated.'}
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(f"Converted {len(rows)} definitions into {a.output}. No server changes made.")

if __name__=='__main__':main()
