import importlib.util,json,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('stage',ROOT/'stage_auxiliary_dbc.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PatchTests(unittest.TestCase):
 def test_real_reference_rows_and_string_rebasing(self):
  source=json.loads((ROOT/'data/auxiliary-additions.json').read_text())
  for table,ref in source['tables'].items():
   width=40 if table=='SpellRange' else 4
   stock=[1]+[0]*(width-1);strings=b'\0existing name\0'
   blob=struct.pack('<4s4I',b'WDBC',1,width,width*4,len(strings))+struct.pack('<'+'I'*width,*stock)+strings
   patched,ids=m.patch(blob,table,ref);_,_,rows,text=m.parse(patched)
   self.assertEqual(rows[0],stock);self.assertEqual(text[:len(strings)],strings)
   self.assertEqual(ids,sorted(map(int,ref['rows'])))
   if table=='SpellRange':
    for row in rows[1:]:
     for i in list(range(6,22))+list(range(23,39)):
      self.assertEqual(text[row[i]:text.index(b'\0',row[i])].decode(),ref['localizedStrings'][str(row[0])][str(i)])
   with self.assertRaises(ValueError):m.patch(patched,table,ref)
 def test_malformed_input_rejected(self):
  with self.assertRaises((ValueError,struct.error)):m.parse(b'bad')
if __name__=='__main__':unittest.main()
