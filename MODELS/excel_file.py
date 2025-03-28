import xlwings as xw
import os 
import pandas as pd

class excel_file:
    def __init__(self,path = None,visibility = True, filtered = False):
        if path:
            self.path = path
            self.visibility = visibility
            self.filtered = filtered
            self.book = xw.Book(self.path)
        else:
            self.book = xw.Book()
            self.path = None
            self.visibility = visibility
            self.filtered = filtered

    #file manipulation

    def new_workbook(self,directory,name):
        file_path = os.path.join(directory,name)
        self.save_workbook(file_path)

    def close_workbook(self):
        self.book.close()
    
    def save_workbook(self,path):
        self.book.save(path)

    def quit_whitout_saving(self):
        self.book.app.quit()

     #sheets manipulation

    def new_sheet(self,sheet_name):
        self.book.sheets.add(sheet_name)

    def get_sheet(self,sheet_name):
        return self.book.sheets[f'{sheet_name}']
    
    def get_first_sheet(self):
        return self.book.sheets[0]
    
    def delete_sheet(self,sheet_name):
        sheet_delete = self.get_sheet(sheet_name)
        sheet_delete.delete()

    def move_sheet_to_beginning(self,sheet_name):
        sheet_name.api.Move(Before = self.book.sheets[0].api)

    def rename_sheet(self,current_name,new_name):
        sheet = self.get_sheet(current_name)
        sheet.name = new_name

        #rows manipulation

    def get_header_position(self,sheet,value_search):
        header = sheet.range("A1").expand("right").value
        position, message=[], []
        for value in value_search:
            if value in header:
                position_header = header.index(value) + 1
                position.append(xw.utils.col_name(position_header))
            else:
                message.append(value)

            if not message:
                pass
                #message box => value não encontrado

        return position_header

    def get_last_row(self,sheet,column_position,row_position = 1):
        return sheet.cells(row_position,column_position).end('down').row
    
    def get_end_row_up(self,sheet,row_position,column_position = 2):
        return sheet.cells(row_position,column_position).end('up').row
    
    def new_row(self,sheet,row_position,column_position = 1):
        sheet.cells(row_position,column_position).api.EntireRow.Insert()

    def clear_contents_rows(self,sheet,clear_range):
        clear_cells = sheet.range(clear_range)
        clear_cells.clear_contents()
    
    def delete_row(self,sheet,row_position,column_position):
        sheet.cells(row_position,column_position).api.EntireRow.Delete()

    def delete_rows_in_range(self,sheet,delete_range):
        delete_cells = sheet.range(delete_range)
        delete_cells.api.EntireRow.Delete()

        #columns manipulation
    
    def new_column(self,sheet,column_position,row_position = 1):
        sheet.cells(row_position,column_position).api.EntireColumn.Insert()

    def name_header(self,sheet,name,column_position,row_position = 1):
        sheet.cells(row_position,column_position).value = name

    def delete_column(self,sheet,column_position,row_position = 1):
        sheet.cells(row_position,column_position).api.EntireColumn.Delete()

        #use of formulas

    def apply_formula(self,sheet,apply_range,formula_apply):
        sheet.range(apply_range).formula = formula_apply

    def apply_text_join(self,sheet,range_formula,apply_cell,delimiter = ","):
        formula_textjoin = f'=TEXTJOIN({delimiter},,{range_formula})'
        self.apply_formula(sheet,apply_cell,formula_textjoin)


    def apply_concat(self,sheet,first_cell,second_cell,apply_range):
        formula_concat = f'=CONCAT({first_cell},"-",{second_cell})'
        self.apply_formula(sheet,apply_range,formula_concat)
        self.transform_to_value(apply_range,sheet)

    def transform_to_value(self,apply_range,sheet):
        range_transform = sheet.range(apply_range)
        values = range_transform.value
        range_transform.value = [[val] for val in values]

    def apply_xlookup(self,sheet,search_value,search_array,return_array,apply_range):
        formula_xlookup = f'=XLOOKUP({search_value},{search_array},{return_array})'
        self.apply_formula(sheet,apply_range,formula_xlookup)
        self.transform_to_value(apply_range,sheet)

        #other methods

    def replace(self,sheet,replace_range,original_value,new_value):
        to_replace= sheet.range(replace_range)
        to_replace.api.Replace(original_value,new_value)

    def turn_in_text(self,sheet,column_range,column_cell):
        conversion = sheet.range(f'{column_range}2:{column_range}{self.get_last_row(sheet,column_cell)}')
        conversion.api.TextToColumns(Destination= conversion.api,
                                     DataType= 1,
                                     Semicolon = False)
    
    def fill_with_value(self,sheet,cell_to_fill,value):
        sheet.range(cell_to_fill).value = value
    
    #creating and manipulation dataframes

def new_dataframe(path,type = True,delimiter=None,encoding=None): #se True sera arquivo xlsx, false para arquivo csv
    if type == True:
        df = pd.read_excel(path)
        return df
    else:
        df = pd.read_csv(path,delimiter,encoding)
        return df

def new_dataframe_from_variable(path,sheet_variable_wkbook):
    sheet = sheet_variable_wkbook.name
    df = pd.read_excel(path,sheet_name = sheet)

def remove_nas_dataframe(data_frame,header_column):
    data_frame[data_frame[header_column].notna()]
    
def get_nulls_in_dataframe(data_frame,header_column):
    data_frame[data_frame[header_column].isnull()]

def create_column_dataframe(dataframe,new_column,content):
    dataframe[new_column] = content

def new_filtered_dataframe(dataframe,filter,column_filter):
    dataframe.loc[dataframe[column_filter] == filter]

def concat_dataframes(dataframe_top,dataframe_down):
    pd.concat([dataframe_top,dataframe_down],ignore_index=True)