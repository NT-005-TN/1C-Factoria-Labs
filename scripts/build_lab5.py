from pathlib import Path
import shutil, uuid
from xml.dom import minidom as D
ROOT=Path(__file__).resolve().parents[1]; base=ROOT/'source/Lab5'
shutil.copytree(ROOT/'source/Lab4',base,dirs_exist_ok=True)
def uid(): return str(uuid.uuid4())
header=(base/'Documents/РасходнаяНакладная.xml').read_text(encoding='utf-8-sig').split('<Document ')[0]
def save(path, body):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(header+body+'</MetaDataObject>',encoding='utf-8')
def syn(s): return f'<Synonym><v8:item><v8:lang>en</v8:lang><v8:content>{s}</v8:content></v8:item></Synonym>'
def num(d,f): return f'<Type><v8:Type>xs:decimal</v8:Type><v8:NumberQualifiers><v8:Digits>{d}</v8:Digits><v8:FractionDigits>{f}</v8:FractionDigits><v8:AllowedSign>Any</v8:AllowedSign></v8:NumberQualifiers></Type>'
internal=''.join(f'<xr:GeneratedType name="AccumulationRegister{t}.Продажи" category="{t}"><xr:TypeId>{uid()}</xr:TypeId><xr:ValueId>{uid()}</xr:ValueId></xr:GeneratedType>' for t in ['Record','Manager','Selection','List','RecordSet','RecordKey'])
save(base/'AccumulationRegisters/Продажи.xml',f'''<AccumulationRegister uuid="{uid()}"><InternalInfo>{internal}</InternalInfo>
<Properties><Name>Продажи</Name>{syn('Продажи')}<Comment/><UseStandardCommands>true</UseStandardCommands><RegisterType>Turnovers</RegisterType><DefaultListForm/><AuxiliaryListForm/><IncludeHelpInContents>false</IncludeHelpInContents><DataLockControlMode>Managed</DataLockControlMode><EnableTotalsSplitting>true</EnableTotalsSplitting></Properties>
<ChildObjects>
<Dimension uuid="{uid()}"><Properties><Name>Номенклатура</Name>{syn('Номенклатура')}<Type><v8:Type>cfg:CatalogRef.СписокНоменклатуры</v8:Type></Type><FillChecking>ShowError</FillChecking><DenyIncompleteValues>true</DenyIncompleteValues><UseInTotals>true</UseInTotals></Properties></Dimension>
<Dimension uuid="{uid()}"><Properties><Name>Контрагент</Name>{syn('Контрагент')}<Type><v8:Type>cfg:CatalogRef.Поставщики</v8:Type></Type><FillChecking>ShowError</FillChecking><DenyIncompleteValues>true</DenyIncompleteValues><UseInTotals>true</UseInTotals></Properties></Dimension>
<Resource uuid="{uid()}"><Properties><Name>Количество</Name>{syn('Количество')}{num(10,3)}</Properties></Resource>
<Resource uuid="{uid()}"><Properties><Name>Сумма</Name>{syn('Сумма')}{num(15,2)}</Properties></Resource>
</ChildObjects></AccumulationRegister>''')
p=base/'Configuration.xml'; s=p.read_text(encoding='utf-8-sig'); s=s.replace('</ChildObjects>','<AccumulationRegister>Продажи</AccumulationRegister><Subsystem>Продажи</Subsystem></ChildObjects>'); p.write_text(s,encoding='utf-8')
save(base/'Subsystems/Продажи.xml',f'''<Subsystem uuid="{uid()}"><Properties><Name>Продажи</Name>{syn('Продажи')}<IncludeHelpInContents>true</IncludeHelpInContents><IncludeInCommandInterface>true</IncludeInCommandInterface><UseOneCommand>false</UseOneCommand><Content><xr:Item xsi:type="xr:MDObjectRef">Document.РасходнаяНакладная</xr:Item><xr:Item xsi:type="xr:MDObjectRef">AccumulationRegister.Продажи</xr:Item><xr:Item xsi:type="xr:MDObjectRef">Catalog.СписокНоменклатуры</xr:Item></Content></Properties><ChildObjects/></Subsystem>''')
p=base/'Documents/РасходнаяНакладная.xml'; s=p.read_text(encoding='utf-8-sig'); s=s.replace('<RegisterRecords/>','<RegisterRecords><xr:Item xsi:type="xr:MDObjectRef">AccumulationRegister.Продажи</xr:Item></RegisterRecords>'); p.write_text(s,encoding='utf-8')
p=base/'Documents/РасходнаяНакладная/Ext/ObjectModule.bsl'; p.parent.mkdir(parents=True,exist_ok=True)
p.write_text('''Procedure Posting(Cancel, Mode)
    RegisterRecords.Продажи.Write = True;
    RegisterRecords.Продажи.Clear();
    For Each Row In Товары Do
        Movement = RegisterRecords.Продажи.Add();
        Movement.Period = Date;
        Movement.Контрагент = Поставщик;
        Movement.Номенклатура = Row.Товар;
        Movement.Количество = Row.Количество;
        Movement.Сумма = Row.Сумма;
    EndDo;
    For Each Row In Услуги Do
        Movement = RegisterRecords.Продажи.Add();
        Movement.Period = Date;
        Movement.Контрагент = Поставщик;
        Movement.Номенклатура = Row.Услуга;
        Movement.Количество = 1;
        Movement.Сумма = Row.Сумма;
    EndDo;
EndProcedure
''',encoding='utf-8')
print('Lab5 source prepared')
