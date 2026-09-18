#!/usr/bin/env python3
import copy,importlib.util,json,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('convert',ROOT/'convert.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ConversionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=m.read_json(ROOT/'data/spells.json');cls.cols=m.read_json(ROOT/'data/schema.json')['columns']
    def test_all_records_roundtrip(self):
        cols=copy.deepcopy(self.cols)
        for c in cols:
            if c.get('maxLength'): c['maxLength']=max(c['maxLength'],max(len(r['localizedStrings'][str(c['sourceField'])]) for r in self.source['records']))
        self.assertEqual(len(self.source['rootIDs']),179)
        self.assertNotIn(901018,[r['id'] for r in self.source['records']])
        for record in self.source['records']:
            row=m.convert(record,cols);self.assertEqual(len(row),234)
            for c in cols:
                i=c['sourceField'];v=row[c['name']]
                if i in m.TEXT_FIELDS:self.assertEqual(v,record['localizedStrings'][str(i)])
                elif i in m.FLOAT_FIELDS:self.assertEqual(struct.unpack('<I',struct.pack('<f',v))[0],record['rawUInt32Fields'][i])
                else:self.assertEqual(v & 0xffffffff,record['rawUInt32Fields'][i])
    def test_effect_mask_transpose(self):
        expected={'EffectSpellClassMaskA_1':122,'EffectSpellClassMaskB_1':123,'EffectSpellClassMaskC_1':124,'EffectSpellClassMaskA_2':125,'EffectSpellClassMaskB_2':126,'EffectSpellClassMaskC_2':127,'EffectSpellClassMaskA_3':128,'EffectSpellClassMaskB_3':129,'EffectSpellClassMaskC_3':130}
        for name,index in expected.items():self.assertEqual(m.field_index(name,999),index)
    def test_signed_float_and_unicode(self):
        r=copy.deepcopy(self.source['records'][0]);r['rawUInt32Fields'][68]=0xffffffff;r['rawUInt32Fields'][47]=0x3fc00000;r['localizedStrings']['136']="Mage's \\ spell\nÉ"
        row=m.convert(r,self.cols);self.assertEqual(row['EquippedItemClass'],-1);self.assertEqual(row['Speed'],1.5)
        lit=m.literal(row['Name_Lang_enUS']);self.assertNotIn("Mage's",lit);self.assertIn(r['localizedStrings']['136'].encode().hex(),lit)
    def test_fail_closed(self):
        r=copy.deepcopy(self.source['records'][0]);r['id']=901018;r['rawUInt32Fields'][0]=901018
        with self.assertRaises(ValueError):m.convert(r,self.cols)
        r=copy.deepcopy(self.source['records'][0]);r['rawUInt32Fields'][47]=0x7f800000
        with self.assertRaises(ValueError):m.convert(r,self.cols)
        r=copy.deepcopy(self.source['records'][0]);r['localizedStrings']['136']='a'*101
        with self.assertRaises(ValueError):m.convert(r,self.cols)
    def test_filtered_closure(self):
        records,report=m.compatible_selection(self.source)
        ids={r['id'] for r in records}
        self.assertEqual(len(report['selectedRoots']),156)
        self.assertEqual(len(report['excludedRoots']),23)
        for r in records:
            for d in r['dependencies']:
                self.assertTrue(d['presentInBaseline'] or d['id'] in ids)
            self.assertLess(max(r['rawUInt32Fields'][71:74]),165)
            self.assertLess(max(r['rawUInt32Fields'][95:98]),317)
    def test_unsupported_enums_block_apply(self):
        row=m.convert(self.source['records'][0],self.cols);row['Effect_2']=184
        issues=m.compatibility_issues([row]);self.assertEqual(issues[0]['outOfRangeFields']['Effect_2'],184)
        sql,_=m.generate_sql([row],self.cols,'blocked')
        self.assertLess(sql.index('Unsupported source effect'),sql.index('CREATE TABLE'))
    def test_sql_guards_and_receipt(self):
        row=m.convert(self.source['records'][0],self.cols);a,b=m.generate_sql([row],self.cols,'test')
        self.assertIn('ROLLBACK; RESIGNAL',a);self.assertIn('Import collision',a);self.assertIn('INSERT INTO `hf_spell_receipt_test`',a)
        self.assertNotIn('REPLACE INTO',a);self.assertNotIn('INSERT IGNORE',a);self.assertIn('FOR UPDATE',b);self.assertIn('rollback refused',b);self.assertIn('BINARY s.',b)
        self.assertIn('STRICT_ALL_TABLES',a);self.assertIn("ENGINE='InnoDB'",a)

if __name__=='__main__':unittest.main()
