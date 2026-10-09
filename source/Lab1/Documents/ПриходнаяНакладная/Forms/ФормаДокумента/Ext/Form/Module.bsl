&AtClientProcedure МатериалыКоличествоOnChange(Item)    CurrentRow = Items.Материалы.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;EndProcedure
	
	
&AtClientProcedure МатериалыЦенаOnChange(Item)    CurrentRow = Items.Материалы.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;EndProcedure
	
	
&AtClientProcedure РасходникиКоличествоOnChange(Item)    CurrentRow = Items.Расходники.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;EndProcedure
	
	
&AtClientProcedure РасходникиЦенаOnChange(Item)    CurrentRow = Items.Расходники.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;EndProcedure