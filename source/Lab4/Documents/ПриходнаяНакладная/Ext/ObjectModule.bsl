Procedure Filling(FillingData, StandardProcessing)
    If TypeOf(FillingData) = Type("DocumentRef.ЗаказПоставщику") Then
        StandardProcessing = False;
        Поставщик = FillingData.Поставщик;
        Договор = FillingData.Договор;
        Материалы.Load(FillingData.Материалы.Unload());
        Расходники.Load(FillingData.Расходники.Unload());
    EndIf;
EndProcedure
