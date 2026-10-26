from pathlib import Path
from xml.dom import minidom as D
import shutil, uuid, re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source'
def uid(): return str(uuid.uuid4())
def read(p): return D.parse(str(p))
def child(n, tag): return next(x for x in n.childNodes if x.nodeType == x.ELEMENT_NODE and x.tagName == tag)
def children(n): return [x for x in n.childNodes if x.nodeType == x.ELEMENT_NODE]
def value(n): return ''.join(x.data for x in n.childNodes if x.nodeType == x.TEXT_NODE)
def setval(n, v):
    for x in list(n.childNodes): n.removeChild(x)
    if v: n.appendChild(n.ownerDocument.createTextNode(v))
def write(p, doc):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc.toxml(), encoding='utf-8')
def fragment(n, xml):
    wrapper = D.parseString('<root xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:app="http://v8.1c.ru/8.2/managed-application/core">'+xml+'</root>')
    for x in children(wrapper.documentElement): n.appendChild(n.ownerDocument.importNode(x, True))
def props(doc): return child(children(doc.documentElement)[0], 'Properties')
def fresh(text): return re.sub(r'[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}', lambda m: uid(), text)
def addconfig(base, tag, name):
    p=base/'Configuration.xml'; d=read(p); c=child(children(d.documentElement)[0],'ChildObjects'); fragment(c,f'<{tag}>{name}</{tag}>'); write(p,d)
def subsystem(base, name, content):
    d=D.parseString(fresh((base/'Subsystems/Фактория.xml').read_text(encoding='utf-8-sig'))); p=props(d)
    setval(child(p,'Name'),name)
    for x in child(p,'Synonym').getElementsByTagName('v8:content'): setval(x,name)
    c=child(p,'Content'); setval(c,'')
    for s in content: fragment(c,f'<xr:Item xsi:type="xr:MDObjectRef">{s}</xr:Item>')
    write(base/f'Subsystems/{name}.xml',d); addconfig(base,'Subsystem',name)
def clonebase(name, previous):
    target=SRC/name
    if target.exists(): raise RuntimeError(f'Already exists: {target}')
    shutil.copytree(SRC/previous,target)
    (target/'ConfigDumpInfo.xml').unlink(missing_ok=True)
    return target

b=clonebase('Lab4','Lab3-final')
p=b/'Documents/ПриходнаяНакладная.xml'; d=read(p)
fragment(child(props(d),'BasedOn'),'<xr:Item xsi:type="xr:MDObjectRef">Document.ЗаказПоставщику</xr:Item>'); write(p,d)
p=b/'Documents/ПриходнаяНакладная/Ext/ObjectModule.bsl'; p.parent.mkdir(parents=True,exist_ok=True)
p.write_text('''Procedure Filling(FillingData, StandardProcessing)
    If TypeOf(FillingData) = Type("DocumentRef.ЗаказПоставщику") Then
        StandardProcessing = False;
        Поставщик = FillingData.Поставщик;
        Договор = FillingData.Договор;
        Материалы.Load(FillingData.Материалы.Unload());
        Расходники.Load(FillingData.Расходники.Unload());
    EndIf;
EndProcedure
''',encoding='utf-8')

d=D.parseString(fresh((b/'Documents/ПриходнаяНакладная.xml').read_text(encoding='utf-8-sig')).replace('ПриходнаяНакладная','ПроизводствоПродукции').replace('Приходная накладная','Производство продукции'))
p=props(d)
for name in ['BasedOn','DefaultObjectForm']: setval(child(p,name),'')
c=child(children(d.documentElement)[0],'ChildObjects')
for x in list(children(c)):
    if x.tagName != 'TabularSection': c.removeChild(x)
tables=children(c)
for i,t in enumerate(tables):
    tp=child(t,'Properties'); old=value(child(tp,'Name')); new=['Материалы','Товары'][i]
    setval(child(tp,'Name'),new)
    for x in child(tp,'Synonym').getElementsByTagName('v8:content'): setval(x,new)
    for x in t.getElementsByTagName('xr:GeneratedType'): x.setAttribute('name',x.getAttribute('name').replace(old,new))
    ac=child(t,'ChildObjects')
    for a in list(children(ac)):
        ap=child(a,'Properties'); an=value(child(ap,'Name'))
        if an in ['Цена','Сумма']: ac.removeChild(a); continue
        if an=='Количество':
            for x in ap.getElementsByTagName('v8:FractionDigits'): setval(x,'3')
        else:
            setval(child(ap,'Name'),'Номенклатура')
            for x in child(ap,'Synonym').getElementsByTagName('v8:content'): setval(x,'Номенклатура')
            ch=child(ap,'ChoiceParameters'); setval(ch,'')
            if i==0:
                fragment(ch,'<app:item name="Filter.ВидНоменклатуры"><app:value xsi:type="v8:FixedArray"><v8:Value xmlns:v8="http://v8.1c.ru/8.1/data/core" xsi:type="xr:DesignTimeRef">Enum.ВидыНоменклатуры.EnumValue.Материал</v8:Value><v8:Value xmlns:v8="http://v8.1c.ru/8.1/data/core" xsi:type="xr:DesignTimeRef">Enum.ВидыНоменклатуры.EnumValue.РасходныйМатериал</v8:Value></app:value></app:item>')
            else:
                fragment(ch,'<app:item name="Filter.ВидНоменклатуры"><app:value xsi:type="xr:DesignTimeRef">Enum.ВидыНоменклатуры.EnumValue.Товар</app:value></app:item>')
write(b/'Documents/ПроизводствоПродукции.xml',d)
addconfig(b,'Document','ПроизводствоПродукции')
subsystem(b,'Производство',['Document.ПроизводствоПродукции','Catalog.СписокНоменклатуры'])

# Form totals must be initialized when opening saved or filled documents.
for p in (b/'Documents').glob('*/Forms/*/Ext/Form.xml'):
    d=read(p); root=d.documentElement
    events=next((x for x in children(root) if x.tagName=='Events'),None)
    if events is None:
        events=d.createElement('Events'); root.appendChild(events)
    fragment(events,'<Event name="OnOpen">ПриОткрытииИтоги</Event>')
    write(p,d)
    mod=p.parent/'Form/Module.bsl'
    with mod.open('a',encoding='utf-8') as f: f.write('\n&AtClient\nProcedure ПриОткрытииИтоги(Cancel)\n    ПересчитатьИтоги();\nEndProcedure\n')

print('Lab4 source prepared')
