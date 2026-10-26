Procedure Posting(Cancel, Mode)
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
