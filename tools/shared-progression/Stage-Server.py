from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
FILES=json.loads((HERE/'source-manifest.json').read_text())
def patch(source,record):
 actual=hashlib.sha256(source.encode()).hexdigest() if source is not None else None
 if actual!=record['before']:raise ValueError('Source differs from reviewed shared progression baseline')
 rel=next(rel for rel,h in FILES.items() if h==record)
 data=(HERE/'overlay'/rel).read_bytes()
 if hashlib.sha256(data).hexdigest()!=record['after']:raise ValueError('Staged shared progression source changed')
 return data.decode()
