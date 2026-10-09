&AtClientProcedure ТоварыКоличествоOnChange(Item)    CurrentRow = Items.Товары.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;EndProcedure





	
&AtClientProcedure ТоварыЦенаOnChange(Item)    CurrentRow = Items.Товары.CurrentData;    CurrentRow.Сумма =        CurrentRow.Количество * CurrentRow.Цена;EndProcedure