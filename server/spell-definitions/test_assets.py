import importlib.util,json,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def module(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
icons=module('stage_icon_dbc');visual=module('stage_visual_dbc')
class AssetTests(unittest.TestCase):
 def test_icon_collision_and_preservation(self):
  b=struct.pack('<4s4I',b'WDBC',1,2,8,5)+struct.pack('<II',1,1)+b'\0old\0'
  after,ids=icons.build(b,{'2':{'dbcPath':'new'}});self.assertEqual(ids,[2]);self.assertEqual(after[20:28],b[20:28])
  with self.assertRaises(ValueError):icons.build(b,{'1':{'dbcPath':'different'}})
 def test_packaged_icon_integrity(self):
  import hashlib
  for r in json.loads((ROOT/'data/resolved-icons.json').read_text()).values():
   b=(ROOT/'icon-assets'/r['file']).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),r['sha256']);self.assertIn(b[:4],[b'BLP1',b'BLP2'])
 def test_visual_clone_string_rebasing_and_namespace(self):
  ref={t:{}for t in visual.TABLES};ref['SpellVisual']={'100':[100]+[0]*31};ref['SpellVisual']['100'][2]=10
  ref['SpellVisualKit']={'10':[10]+[0]*37};ref['SpellVisualKit']['10'][17:21]=[0xffffffff]*4;ref['SpellVisualKit']['10'][6]=20
  ref['SpellVisualEffectName']={'20':{'rawFields':[20,1,1,0,0,0,0],'name':'effect','model':''}}
  widths={'SpellVisual':128,'SpellVisualKit':152,'SpellVisualEffectName':28,'SpellVisualKitModelAttach':40,'SpellMissileMotion':20,'SoundEntries':120,'SoundEntriesAdvanced':96,'SpellChainEffects':177}
  baselines={}
  for t,z in widths.items():
   row=struct.pack('<I',1)+b'\0'*(z-4);baselines[t]=struct.pack('<4s4I',b'WDBC',1,48 if z==177 else z//4,z,1)+row+b'\0'
  out,report=visual.build(ref,baselines,{'spells/test.blp':b'BLP2test'})
  self.assertIn('HeroAdvancement/spells/test.blp',out)
  for t,z in widths.items():self.assertEqual(out['DBFilesClient/'+t+'.dbc'][20:20+z],baselines[t][20:20+z])
  v=visual.dbc(out['DBFilesClient/SpellVisual.dbc'])[2][100]
  self.assertEqual(struct.unpack_from('<I',v,8)[0],report['SpellVisualKit']['mapping'][10])
  bad=dict(baselines);bad['SpellVisual']=out['DBFilesClient/SpellVisual.dbc']
  with self.assertRaises(ValueError):visual.build(ref,bad,{})
if __name__=='__main__':unittest.main()
