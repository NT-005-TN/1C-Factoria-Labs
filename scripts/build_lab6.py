from pathlib import Path
import shutil, uuid, re
ROOT=Path(__file__).resolve().parents[1]; base=ROOT/'source/Lab6'
shutil.copytree(ROOT/'source/Lab5',base,dirs_exist_ok=True)
def uid(): return str(uuid.uuid4())
header=(base/'Documents/РасходнаяНакладная.xml').read_text(encoding='utf-8-sig').split('<Document ')[0]
def save(path,body):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(header+body+'</MetaDataObject>',encoding='utf-8')
def syn(s): return f'<Synonym><v8:item><v8:lang>en</v8:lang><v8:content>{s}</v8:content></v8:item></Synonym>'
name='ОтчетПоПродажам'
internal=''.join(f'<xr:GeneratedType name="Report{t}.{name}" category="{t}"><xr:TypeId>{uid()}</xr:TypeId><xr:ValueId>{uid()}</xr:ValueId></xr:GeneratedType>' for t in ['Object','Manager'])
save(base/f'Reports/{name}.xml',f'''<Report uuid="{uid()}"><InternalInfo>{internal}</InternalInfo><Properties><Name>{name}</Name>{syn('Отчёт по продажам')}<UseStandardCommands>true</UseStandardCommands><DefaultForm/><MainDataCompositionSchema>Report.{name}.Template.ОсновнаяСхемаКомпоновкиДанных</MainDataCompositionSchema><DefaultSettingsForm/><DefaultVariantForm/><IncludeHelpInContents>true</IncludeHelpInContents></Properties><ChildObjects><Template>ОсновнаяСхемаКомпоновкиДанных</Template></ChildObjects></Report>''')
save(base/f'Reports/{name}/Templates/ОсновнаяСхемаКомпоновкиДанных.xml',f'''<Template uuid="{uid()}"><Properties><Name>ОсновнаяСхемаКомпоновкиДанных</Name>{syn('Основная схема компоновки данных')}<TemplateType>DataCompositionSchema</TemplateType></Properties></Template>''')
p=base/'Configuration.xml'; s=p.read_text(encoding='utf-8-sig').replace('</ChildObjects>',f'<Report>{name}</Report></ChildObjects>'); p.write_text(s,encoding='utf-8')
p=base/'Subsystems/Продажи.xml'; s=p.read_text().replace('</Content>',f'<xr:Item xsi:type="xr:MDObjectRef">Report.{name}</xr:Item></Content>'); p.write_text(s,encoding='utf-8')
ns='http://v8.1c.ru/8.1/data-composition-system'
fields=''
for n in ['Номенклатура','Контрагент','Количество','Сумма']:
    fields+=f'<field xsi:type="DataSetFieldField"><dataPath>{n}</dataPath><field>{n}</field><title xsi:type="v8:LocalStringType"><v8:item><v8:lang>en</v8:lang><v8:content>{n}</v8:content></v8:item></title></field>'
params=''
for n,typ,expr in [('НачалоПериода','xs:dateTime','&amp;Период.StartDate'),('КонецПериода','xs:dateTime','EndOfPeriod(&amp;Период.EndDate, &quot;Day&quot;)'),('Период','v8:StandardPeriod',''),('Номенклатура','cfg:CatalogRef.СписокНоменклатуры','')]:
    params+=f'<parameter><name>{n}</name><title xsi:type="v8:LocalStringType"><v8:item><v8:lang>en</v8:lang><v8:content>{n}</v8:content></v8:item></title><valueType><v8:Type>{typ}</v8:Type></valueType>'
    if n=='Номенклатура': params+='<value xsi:type="cfg:CatalogRef.СписокНоменклатуры">00000000-0000-0000-0000-000000000000</value>'
    if n=='Период': params+='<value xsi:type="v8:StandardPeriod"><v8:variant xsi:type="v8:StandardPeriodVariant">Custom</v8:variant><v8:startDate>0001-01-01T00:00:00</v8:startDate><v8:endDate>0001-01-01T00:00:00</v8:endDate></value>'
    params+='<useRestriction>false</useRestriction>'
    if expr: params+=f'<expression>{expr}</expression>'
    params+='</parameter>'
xml=f'''<?xml version="1.0" encoding="UTF-8"?>
<DataCompositionSchema xmlns="{ns}/schema" xmlns:dcsset="{ns}/settings" xmlns:dcscor="{ns}/core" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dataSource><name>ИсточникДанных1</name><dataSourceType>Local</dataSourceType></dataSource>
<dataSet xsi:type="DataSetQuery"><name>Продажи</name>{fields}<dataSource>ИсточникДанных1</dataSource><query>ВЫБРАТЬ
 ПродажиОбороты.Номенклатура КАК Номенклатура,
 ПродажиОбороты.Контрагент КАК Контрагент,
 ПродажиОбороты.КоличествоОборот КАК Количество,
 ПродажиОбороты.СуммаОборот КАК Сумма
ИЗ РегистрНакопления.Продажи.Обороты(&amp;НачалоПериода, &amp;КонецПериода, , ) КАК ПродажиОбороты
ГДЕ (&amp;Номенклатура = ЗНАЧЕНИЕ(Справочник.СписокНоменклатуры.ПустаяСсылка)
 ИЛИ ПродажиОбороты.Номенклатура = &amp;Номенклатура)</query></dataSet>
<totalField><dataPath>Количество</dataPath><expression>Sum(Количество)</expression></totalField>
<totalField><dataPath>Сумма</dataPath><expression>Sum(Сумма)</expression></totalField>
{params}
<settingsVariant><dcsset:name>Основной</dcsset:name><dcsset:presentation xsi:type="v8:LocalStringType"><v8:item><v8:lang>en</v8:lang><v8:content>Продажи по номенклатуре и контрагентам</v8:content></v8:item></dcsset:presentation>
<dcsset:settings><dcsset:selection><dcsset:item xsi:type="dcsset:SelectedItemField"><dcsset:field>Номенклатура</dcsset:field></dcsset:item><dcsset:item xsi:type="dcsset:SelectedItemField"><dcsset:field>Контрагент</dcsset:field></dcsset:item><dcsset:item xsi:type="dcsset:SelectedItemField"><dcsset:field>Количество</dcsset:field></dcsset:item><dcsset:item xsi:type="dcsset:SelectedItemField"><dcsset:field>Сумма</dcsset:field></dcsset:item></dcsset:selection>
<dcsset:structure><dcsset:item xsi:type="dcsset:StructureItemGroup"><dcsset:groupItems><dcsset:item xsi:type="dcsset:GroupItemField"><dcsset:field>Номенклатура</dcsset:field><dcsset:groupType>Items</dcsset:groupType></dcsset:item></dcsset:groupItems><dcsset:structure><dcsset:item xsi:type="dcsset:StructureItemGroup"><dcsset:groupItems><dcsset:item xsi:type="dcsset:GroupItemField"><dcsset:field>Контрагент</dcsset:field><dcsset:groupType>Items</dcsset:groupType></dcsset:item></dcsset:groupItems></dcsset:item></dcsset:structure></dcsset:item></dcsset:structure>
</dcsset:settings></settingsVariant></DataCompositionSchema>'''
xml=xml.replace('<dcsset:structure>','').replace('</dcsset:structure>','')
xml=xml.replace('</dcsset:selection>','''</dcsset:selection><dcsset:dataParameters>
<dcscor:item xsi:type="dcsset:SettingsParameterValue"><dcscor:parameter>Период</dcscor:parameter><dcscor:value xsi:type="v8:StandardPeriod"><v8:variant xsi:type="v8:StandardPeriodVariant">ThisMonth</v8:variant></dcscor:value><dcsset:use>true</dcsset:use><dcsset:userSettingID>681272fa-a09f-4319-9a60-87cf3d9e6601</dcsset:userSettingID></dcscor:item>
<dcscor:item xsi:type="dcsset:SettingsParameterValue"><dcscor:parameter>Номенклатура</dcscor:parameter><dcscor:value xsi:type="cfg:CatalogRef.СписокНоменклатуры">00000000-0000-0000-0000-000000000000</dcscor:value><dcsset:use>true</dcsset:use><dcsset:userSettingID>681272fa-a09f-4319-9a60-87cf3d9e6602</dcsset:userSettingID></dcscor:item>
</dcsset:dataParameters>''',1)
xml=xml.replace('</dcsset:groupItems>','</dcsset:groupItems><dcsset:selection><dcsset:item xsi:type="dcsset:SelectedItemAuto"/></dcsset:selection>')
xml=re.sub(r'<dcsset:use>.*?</dcsset:use>','',xml)
xml=xml.replace('</dcsset:dataParameters>','''</dcsset:dataParameters><dcsset:outputParameters><dcscor:item xsi:type="dcsset:SettingsParameterValue"><dcscor:parameter>ВертикальноеРасположениеОбщихИтогов</dcscor:parameter><dcscor:value xsi:type="dcscor:DataCompositionTotalPlacement">End</dcscor:value></dcscor:item><dcscor:item xsi:type="dcsset:SettingsParameterValue"><dcscor:parameter>МакетОформления</dcscor:parameter><dcscor:value xsi:type="xs:string">Море</dcscor:value></dcscor:item></dcsset:outputParameters>''')
p=base/f'Reports/{name}/Templates/ОсновнаяСхемаКомпоновкиДанных/Ext/Template.xml'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(xml,encoding='utf-8')
print('Lab6 source prepared')
