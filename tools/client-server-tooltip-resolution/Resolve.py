"""Audit installed tooltip placeholders against exported PTR spell records.

Never connects to or modifies a server. Unknown expressions remain yellow.
"""
from pathlib import Path
import ast, hashlib, importlib.util, json, re, struct, sys

HERE=Path(__file__).resolve().parent
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'work/regalia/libs'))
from lupa.lua51 import LuaRuntime

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

imp=module('reference_renderer',ROOT/'outputs/HeroFreePick-GitHub/tools/talents/import_area52_talents.py')
conv=module('spell_columns',ROOT/'outputs/HeroFreePick-GitHub/server/spell-definitions/convert.py')
BASE=ROOT/'outputs/Hero_Abomination_Test/npc-audit-3'
CLIENT=Path('D:/DML WOTLK Client Side/WoW-3.3.5a - HeroFreePick - Classic Test/Interface/AddOns/HeroFreePick')

def mysql_text(s):
    return re.sub(r'\\([0nrtbZ\\])',lambda m:{'0':'\0','n':'\n','r':'\r','t':'\t','b':'\b','Z':'\x1a','\\':'\\'}[m[1]],s)

def load():
    db=imp.DBC(BASE/'Spell.dbc',234);strings=bytearray(db.strings)
    lines=(BASE/'spell-overrides.tsv').read_bytes().decode('utf-8').split('\n')
    columns=lines[0].split('\t');overrides=set()
    for line in lines[1:]:
        if not line:continue
        values=line.split('\t');assert len(values)==len(columns)
        row=[0]*234
        for ordinal,(name,value) in enumerate(zip(columns,values)):
            i=conv.field_index(name,ordinal)
            if i in conv.TEXT_FIELDS:
                row[i]=len(strings);strings.extend((mysql_text(value) if value!='NULL' else '').encode()+b'\0')
            elif i in conv.FLOAT_FIELDS:row[i]=struct.unpack('<I',struct.pack('<f',float(value) if value!='NULL' else 0))[0]
            else:row[i]=int(value if value!='NULL' else 0)&0xffffffff
        db.rows[row[0]]=tuple(row);overrides.add(row[0])
    db.strings=bytes(strings)
    tables={'SpellDuration':imp.DBC(BASE/'SpellDuration.dbc').rows}
    for name in ('SpellRadius','SpellRange'):
        tables[name]=imp.DBC(ROOT/'outputs/Hero_Abomination_Test/live-baseline'/f'{name}.dbc').rows
    return db,tables,overrides

def expression_tree(expression):
    def convert(n):
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):return n.value
        if isinstance(n,ast.Name) and n.id in ('AP','RAP','SPI'):return n.id
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            return ['*',-1 if isinstance(n.op,ast.USub) else 1,convert(n.operand)]
        if isinstance(n,ast.BinOp) and type(n.op) in (ast.Add,ast.Sub,ast.Mult,ast.Div):
            return [{ast.Add:'+',ast.Sub:'-',ast.Mult:'*',ast.Div:'/'}[type(n.op)],convert(n.left),convert(n.right)]
        raise ValueError('Unsupported formula')
    if len(expression)>300:raise ValueError('Formula too long')
    return convert(ast.parse(expression,mode='eval').body)

def constant(tree):
    if isinstance(tree,(float,int)):return tree
    if isinstance(tree,str):raise ValueError('Character stat required')
    op,a,b=tree;a=constant(a);b=constant(b)
    if op=='+':return a+b
    if op=='-':return a-b
    if op=='*':return a*b
    return a/b

def resolve(db,tables,sid):
    row=db.rows[sid];text=db.text(row[170]) or db.text(row[187])
    formulas={};unresolved=[]
    def field(match,numeric=False):
        q=db.rows.get(int(match[1]) if match[1] else sid)
        k=match[2];i=int(match[3] or 1)-1
        if not q or not 0<=i<3:return match[0]
        # Signed values are essential inside formulas (e.g. cooldown reductions).
        if k in ('m','M','s','S'):
            die=imp.signed(q[74+i]);bp=imp.signed(q[80+i])
            value=bp+(die if k=='M' else min(1,die) if die else 0)
            if k in ('s','S') and die>1:
                if numeric:return match[0] # random ranges cannot be one formula operand
                return '%g to %g'%(abs(bp+1),abs(bp+die))
            if not numeric:value=abs(value)
        elif k in ('d','D'):
            d=tables['SpellDuration'].get(q[40])
            if not d or imp.signed(d[2])!=0 or imp.signed(d[1])<0:return match[0]
            value=imp.signed(d[1])/1000
            return '%g'%value if numeric else '%g sec'%value
        elif k in ('t','T'):value=q[98+i]/1000
        elif k=='x':value=q[104+i]
        elif k=='e':value=imp.float32(q[101+i])
        elif k=='b':value=imp.float32(q[119+i])
        elif k=='q':value=imp.signed(q[110+i])
        elif k=='o':
            d=tables['SpellDuration'].get(q[40]);period=q[98+i]
            if not d or d[2]!=0 or imp.signed(d[1])<0 or not period or imp.signed(q[74+i])>1:return match[0]
            value=(imp.signed(q[80+i])+(1 if q[74+i] else 0))*(imp.signed(d[1])//period)
        else:return match[0]
        return '%g'%value
    pattern=r'\$(\d*)([mMsSdDtTxeoqb])([123]?)(?![a-zA-Z0-9])'
    def formula(m):
        body=re.sub(pattern,lambda t:field(t,True),m[1])
        body=re.sub(r'\$(RAP|AP|SPI)\b',r'\1',body)
        try:
            tree=expression_tree(body)
            try:return '%g'%constant(tree)
            except ValueError:
                key='HFVALUE%dX'%(len(formulas)+1);formulas[key]=tree;return key
        except (ValueError,SyntaxError,ZeroDivisionError):return m[0]
    text=re.sub(r'\$\{([^{}]+)\}(?:\.\d+)?',formula,text)
    # Protect unsupported formulas from partial substitutions and whitespace truncation.
    protected={}
    def protect(m):
        key='HFUNKNOWN%dX'%len(protected);protected[key]=m[0];return key
    text=re.sub(r'\$\{[^{}]+\}(?:\.\d+)?',protect,text)
    def arithmetic(m):
        candidate='${$'+m[3]+m[4]+m[5]+m[1]+m[2]+'}'
        return re.sub(r'\$\{([^{}]+)\}',formula,candidate)
    text=re.sub(r'\$([/*])([\d.]+);(\d*)([omtTsS])([123])',arithmetic,text)
    text=re.sub(pattern,field,text)
    text=re.sub(r'\$[gG]([^:;]+):([^;]+);',lambda m:'their' if m[1].lower()=='his' else 'themself' if m[1].lower()=='himself' else m[1],text)
    text=re.sub(r'\$[lL]([^:;]+):([^;]+);',r'\2',text)
    # Existing renderer handles cross references and labelled conditional branches.
    strings=db.strings;original=db.rows[sid];tmp=list(original);tmp[170]=len(strings)
    db.strings+=text.encode()+b'\0';db.rows[sid]=tuple(tmp)
    try:text,_=imp.render(db,sid,tables)
    finally:db.strings=strings;db.rows[sid]=original
    for key,value in protected.items():text=text.replace(key,value)
    text=re.sub(r'(?<!\n)When ([^\n]+?) is active:',r'\nWhen \1 is active:',text)
    # Entire expressions, not just the first whitespace-delimited fragment.
    unknown=re.compile(r'\$\{[^{}]*\}(?:\.\d+)?|\$<[^>]+>|\$[^\s,.;%]+|@[a-zA-Z]+:[^@]*@')
    unresolved=sorted(set(unknown.findall(text)))
    for token in sorted(unresolved,key=len,reverse=True):text=text.replace(token,'[value pending]')
    return {'text':text,'unresolved':unresolved,'formulas':formulas}

def main():
    db,tables,overrides=load();l=LuaRuntime();l.execute((CLIENT/'ServerSpellDescriptions.lua').read_text(encoding='utf-8'))
    current=l.globals().HeroServerSpellDescriptions;result={};audit=[]
    for sid,item in current.items():
        sid=int(sid)
        if not len(item['unresolved']) and not re.search(r'\[value (?:pending|unavailable)\]|\$|@learns:',item['text']):continue
        if sid not in db.rows:
            audit.append({'spell':sid,'status':'missing server definition'});continue
        new=resolve(db,tables,sid);result[sid]=new
        audit.append({'spell':sid,'name':db.text(db.rows[sid][136]),'before':item['text'],**new,'source':'spell_dbc' if sid in overrides else 'Spell.dbc'})
    out=HERE/'payload/HeroFreePick';out.mkdir(parents=True,exist_ok=True)
    (out/'ResolvedServerTooltips.lua').write_text('-- Generated from exported PTR definitions. Runtime formulas are restricted arithmetic trees.\nHeroResolvedServerTooltips='+imp.lua(result)+'\n',encoding='utf-8')
    sources=[BASE/'Spell.dbc',BASE/'SpellDuration.dbc',BASE/'spell-overrides.tsv',CLIENT/'ServerSpellDescriptions.lua']
    report={'reviewedDescriptions':len(list(current.items())),'affected':len(audit),'fullyResolved':sum(not v.get('unresolved',[1]) for v in audit),'stillUnresolved':sum(bool(v.get('unresolved',[1])) for v in audit),'sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'entries':audit}
    (HERE/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print({k:v for k,v in report.items() if k not in ('sources','entries')})

if __name__=='__main__':main()
