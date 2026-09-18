"""Read-only live evidence collection. Run in WSL with access to Docker.
No restarts, writes to databases, learning or build changes are performed.
"""
from pathlib import Path
import argparse,json,subprocess,datetime

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--database-container',default='classless-test-database');p.add_argument('--world-container',default='classless-test-worldserver');p.add_argument('--ids',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 ids=json.loads(Path(a.ids).read_text());assert isinstance(ids,list)and all(isinstance(i,int)and 0<i<2**32 for i in ids)
 def sql(query):
  assert query.startswith('SELECT ')
  command=['docker','exec',a.database_container,'sh','-c','MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot -B acore_world -e "$1"','audit',query]
  raw=subprocess.run(command,check=True,capture_output=True,text=True).stdout.splitlines()
  if not raw:return []
  fields=raw[0].split('\t');return [dict(zip(fields,line.split('\t')))for line in raw[1:]]
 report={'collectedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'readOnly':True,'tables':{},'notes':[]}
 proc=subprocess.run(['docker','inspect','--format','{{.Image}}',a.world_container],capture_output=True,text=True)
 report['worldImage']=proc.stdout.strip()if proc.returncode==0 else None
 schemas=sql("SELECT TABLE_NAME,COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE()")
 tables={}
 for row in schemas:tables.setdefault(row['TABLE_NAME'],{})[row['COLUMN_NAME'].lower()]=row['COLUMN_NAME']
 wanted={'spell_dbc':['id'],'spell_script_names':['spell_id'],'spell_proc':['spellid'],'spell_ranks':['spell_id','first_spell_id'],'spell_learn_spell':['entry','spellid'],'spell_linked_spell':['spell_trigger','spell_effect']}
 for table,columns in wanted.items():
  available=tables.get(table,{})
  actual=[available[c]for c in columns if c in available]
  if not actual:report['notes'].append('Table/ID columns unavailable: '+table);continue
  rows=[]
  for start in range(0,len(ids),300):
   values=','.join(map(str,ids[start:start+300]));where=' OR '.join('ABS(`'+col+'`) IN ('+values+')'for col in actual)
   rows+=sql('SELECT * FROM `'+table+'` WHERE '+where)
  unique={json.dumps(row,sort_keys=True):row for row in rows};report['tables'][table]=list(unique.values())
 report['notes'].append('Database presence/bindings are not proof of runtime effects. Verify core SpellMgr and gameplay separately. Rank rows may reference further spells outside the initial requested ID set.')
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print('Saved read-only evidence to',out)
if __name__=='__main__':main()
