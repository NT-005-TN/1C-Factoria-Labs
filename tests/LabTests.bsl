Procedure Check(Condition, Message)
    If Not Condition Then Raise Message; EndIf;
EndProcedure

Function Item(Name, Kind)
    O = Catalogs.СписокНоменклатуры.CreateItem();
    O.Description = Name;
    O.ВидНоменклатуры = Kind;
    O.Write();
    Return O.Ref;
EndFunction

Function Totals(Recorder)
    Q = New Query("SELECT SUM(Количество) AS Qty, SUM(Сумма) AS Amount FROM AccumulationRegister.Продажи WHERE Recorder = &Recorder");
    Q.SetParameter("Recorder",Recorder);
    S = Q.Execute().Select(); S.Next();
    Return New Structure("Qty,Amount",S.Qty,S.Amount);
EndFunction

Procedure Run() Export
    Log = New TextDocument;
    Try
        Counterparty = Catalogs.Поставщики.CreateItem();
        Counterparty.Description = "ТЕСТ ЛР4–6"; Counterparty.Write();
        Contract = Catalogs.Договоры.CreateItem(); Contract.Owner = Counterparty.Ref;
        Contract.Description = "Тестовый договор"; Contract.Write();
        Material = Item("ТЕСТ Материал",Enums.ВидыНоменклатуры.Материал);
        Supply = Item("ТЕСТ Расходник",Enums.ВидыНоменклатуры.РасходныйМатериал);
        Product = Item("ТЕСТ Товар",Enums.ВидыНоменклатуры.Товар);
        Service = Item("ТЕСТ Услуга",Enums.ВидыНоменклатуры.Услуга);
        Order = Documents.ЗаказПоставщику.CreateDocument(); Order.Date = CurrentDate();
        Order.Поставщик = Counterparty.Ref; Order.Договор = Contract.Ref;
        R = Order.Материалы.Add(); R.Материал = Material; R.Количество = 2; R.Цена = 100; R.Сумма = 200;
        R = Order.Расходники.Add(); R.Расходник = Supply; R.Количество = 3; R.Цена = 10; R.Сумма = 30;
        Order.Write();
        Receipt = Documents.ПриходнаяНакладная.CreateDocument(); Receipt.Fill(Order.Ref);
        Check(Receipt.Поставщик = Counterparty.Ref, "Supplier transfer failed");
        Check(Receipt.Договор = Contract.Ref, "Contract transfer failed");
        Check(Receipt.Материалы.Count() = 1 And Receipt.Материалы[0].Сумма = 200, "Material transfer failed");
        Check(Receipt.Расходники.Count() = 1 And Receipt.Расходники[0].Сумма = 30, "Supply transfer failed");
        Log.AddLine("PASS: order -> receipt supplier, contract and both tables");
        Filter = Metadata.Documents.ПроизводствоПродукции.TabularSections.Материалы.Attributes.Номенклатура.ChoiceParameters[0].Value;
        Log.AddLine("Filter type: " + String(TypeOf(Filter)) + ", count: " + String(Filter.Count()));
        Check(TypeOf(Filter) = Type("FixedArray") And Filter.Count() = 2, "FixedArray filter failed");
        Log.AddLine("PASS: production materials FixedArray has two kinds");
        Production = Documents.ПроизводствоПродукции.CreateDocument(); Production.Date = CurrentDate();
        R = Production.Материалы.Add(); R.Номенклатура = Material; R.Количество = 1.5;
        R = Production.Товары.Add(); R.Номенклатура = Product; R.Количество = 1;
        Production.Write();
        Check(Production.Материалы[0].Количество = 1.5,"Production fraction lost");
        Log.AddLine("PASS: production document saved with fractional quantity");
        Sale = Documents.РасходнаяНакладная.CreateDocument(); Sale.Date = CurrentDate();
        Sale.Поставщик = Counterparty.Ref; Sale.Договор = Contract.Ref;
        R = Sale.Товары.Add(); R.Товар = Product; R.Количество = 2; R.Цена = 100; R.Сумма = 200;
        R = Sale.Услуги.Add(); R.Услуга = Service; R.Сумма = 500;
        Sale.Write(DocumentWriteMode.Posting);
        T = Totals(Sale.Ref); Check(T.Qty = 3 And T.Amount = 700,"Sales totals wrong");
        Log.AddLine("PASS: posting produces quantity 3 and amount 700 (service quantity 1)");
        Sale.Write(DocumentWriteMode.Posting); T = Totals(Sale.Ref);
        Check(T.Qty = 3 And T.Amount = 700,"Reposting duplicates records");
        Log.AddLine("PASS: reposting does not duplicate records");
        Schema = Reports.ОтчетПоПродажам.GetTemplate("ОсновнаяСхемаКомпоновкиДанных");
        Settings = Schema.DefaultSettings;
        For Each P In Settings.DataParameters.Items Do
            Check(ValueIsFilled(P.UserSettingID), "Report parameter is not exposed to the user");
        EndDo;
        Settings.DataParameters.SetParameterValue("Период", New StandardPeriod(StandardPeriodVariant.ThisMonth));
        Settings.DataParameters.SetParameterValue("Номенклатура", Product);
        Writer = New XMLWriter; Writer.OpenFile("/private/tmp/factoria456-settings.xml"); XDTOSerializer.WriteXML(Writer,Settings); Writer.Close();
        Layout = New DataCompositionTemplateComposer;
        Template = Layout.Execute(Schema, Settings);
        Processor = New DataCompositionProcessor; Processor.Initialize(Template);
        Result = New SpreadsheetDocument;
        Output = New ПроцессорВыводаРезультатаКомпоновкиДанныхВТабличныйДокумент;
        Output.УстановитьДокумент(Result); Output.Вывести(Processor);
        Check(Result.TableHeight > 0, "Report empty");
        Found = False;
        For I = 1 To Result.TableHeight Do
            For J = 1 To Result.TableWidth Do
                If StrFind(Result.Area(I,J).Text,"200") > 0 Then Found = True; EndIf;
            EndDo;
        EndDo;
        Check(Found,"Report has no product amount 200");
        Log.AddLine("PASS: DCS query, period expression, template and report output executed");
        Sale.Write(DocumentWriteMode.UndoPosting);
        Q = New Query("SELECT COUNT(*) AS N FROM AccumulationRegister.Продажи WHERE Recorder = &Recorder"); Q.SetParameter("Recorder",Sale.Ref); S = Q.Execute().Select(); S.Next();
        Check(S.N = 0,"Unposting left records");
        Log.AddLine("PASS: unposting removes register records");
        Log.AddLine("ALL TESTS PASSED");
    Except
        Log.AddLine("FAIL: " + ErrorDescription());
    EndTry;
    Log.Write("/private/tmp/factoria456-tests.txt");
EndProcedure
