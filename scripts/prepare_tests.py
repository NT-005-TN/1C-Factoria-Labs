from pathlib import Path
import shutil,re,uuid
R=Path(__file__).resolve().parents[1]; b=Path('/private/tmp/factoria456-testsource')
shutil.copytree(R/'source/Lab6',b,dirs_exist_ok=True)
p=b/'CommonModules/УКЗ_ВызовСервера.xml'; text=p.read_text(encoding='utf-8-sig').replace('УКЗ_ВызовСервера','LabTests')
text=re.sub(r'[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}',lambda m:str(uuid.uuid4()),text)
(b/'CommonModules/LabTests.xml').write_text(text,encoding='utf-8')
p=b/'Configuration.xml'; text=p.read_text().replace('</ChildObjects>','<CommonModule>LabTests</CommonModule></ChildObjects>'); p.write_text(text)
p=b/'Ext/ManagedApplicationModule.bsl'; p.write_text('''Procedure OnStart()
    LabTests.Run();
    Exit(False);
EndProcedure
''',encoding='utf-8')
p=b/'CommonModules/LabTests/Ext/Module.bsl'; p.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(R/'tests/LabTests.bsl',p)
print(b)
