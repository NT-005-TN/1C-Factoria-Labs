&AtClientProcedure МатериалыЦенаOnChange(Item)    CurrentRow = Items.Материалы.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;		
	ПересчитатьИтоги();	
		EndProcedure&AtClientProcedure РасходникиКоличествоOnChange(Item)    CurrentRow = Items.Расходники.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;		
	ПересчитатьИтоги();	
		EndProcedure             
	
	
	
&AtClientProcedure МатериалыКоличествоOnChange(Item)    CurrentRow = Items.Материалы.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;		
	ПересчитатьИтоги();	
	EndProcedure&AtClientProcedure РасходникиЦенаOnChange(Item)    CurrentRow = Items.Расходники.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;  
		
	ПересчитатьИтоги();EndProcedure
	



	
&AtClientProcedure ПересчитатьИтоги()    ИтогМатериалы = 0;    For Each CurrentRow In Object.Материалы Do        ИтогМатериалы = ИтогМатериалы + CurrentRow.Сумма;    EndDo;    ИтогРасходники = 0;    For Each CurrentRow In Object.Расходники Do        ИтогРасходники = ИтогРасходники + CurrentRow.Сумма;    EndDo;EndProcedure