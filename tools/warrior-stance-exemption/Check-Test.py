"""Run only the Warrior stance preflight; never activate."""
from pathlib import Path
import runpy,sys
path=Path(__file__).with_name('Activate-Test.py')
sys.argv=[str(path),'--check']
runpy.run_path(str(path),run_name='__main__')
