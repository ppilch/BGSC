import inspect

class DataTableOperations():
    
    def delete_rows(self, table_name):
        print(inspect.currentframe().f_code.co_name)
        list_len = len(table_name.row_data)
        for i in range(list_len):
            #Just remove first item - as many times as many items in the list
            table_name.remove_row(table_name.row_data[0])

    def add_row_to_table(self, table_name, col1, col2):
        print(inspect.currentframe().f_code.co_name)
        if col2 == None:
            table_name.add_row((str(col1)))
        else:
            table_name.add_row((str(col1), str(col2)))

    def get_rows_from_table(self, table_name):
        print(inspect.currentframe().f_code.co_name)
        return table_name.row_data
