from GUI.content_area import *
from GUI.widgets.cards import *
from MODELS.Utilities.duplicates import *
from MODELS.Utilities.csv_converter import *
from MODELS.Utilities.fix_cities import *
from MODELS.Utilities.divisor import *
from MODELS.Utilities.exp_msp import *

class Utilities(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)

        self.card_divisor = Card("divisor_table","#FF7E29")
        self.card_divisor.create_front_card("Dividir tabela","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_divisor.create_back_card("#FF7E29","1.Selecione em quantas tabelas deseja dividir a planilha\n2.Selecione o arquivo.\n3.Clique em 'Gerar'\n4.Selecione onde deseja salvar(todos os arquivos serão gerados no diretório selecionado)")
        cb_box_divisor = self.card_divisor.create_combobox(["2","3","4","5","6","7","8"])
        self.card_divisor.add_component_card(cb_box_divisor,"combobox")
        self.card_divisor.set_action_btn("btn_generate", self.create_division)

        self.card_exp_msp = Card("exp_msp","#FF7E29")
        self.card_exp_msp.create_front_card("Exp para MSP","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_exp_msp.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha EXP. \n2.Clique em 'Gerar'\n\nIMPORTANTE: O arquivo será salvo na pasta original com 'MSP_' na frente do nome")
        self.card_exp_msp.set_action_btn("btn_generate", self.process_exp_msp)   
        
        self.card_duplicates = Card("duplicates","#FF7E29")
        self.card_duplicates.create_front_card("Remover Duplicadas","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_duplicates.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione o modelo da planilha. \n2. Selecione a planilha no modelo correto.\n3.Clique em 'Gerar'\n\nIMPORTANTE: O arquivo é salvo na pasta original com 'no_dup_' na frente do nome")
        cb_box_duplicates = self.card_duplicates.create_combobox(["MSP", "EXP"])
        self.card_duplicates.add_component_card(cb_box_duplicates,"combobox")
        self.card_duplicates.set_action_btn("btn_generate", self.process_dup)
        
        self.card_csv = Card("csvtoxlsx","#FF7E29")
        self.card_csv.create_front_card("CSV para Excel","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_csv.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha CSV. \n2.Clique em 'Gerar'\n\nIMPORTANTE: O arquivo será salvo na pasta original com 'xlsx_' na frente do nome")
        self.card_csv.set_action_btn("btn_generate", self.process_csv_converter)

        self.card_fix_cities = Card("fix_cities","#FF7E29")
        self.card_fix_cities.create_front_card("Corrigir Cidades","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_fix_cities.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP de Campus. \n2.Clique em 'Gerar'\n\nIMPORTANTE: O arquivo será salvo na pasta original com 'fixed_cities_' na frente do nome")
        self.card_fix_cities.set_action_btn("btn_generate", self.process_fix_cities)        
        
        self.add_card(self.card_exp_msp,"TOP")
        self.add_card(self.card_duplicates,"TOP")
        self.add_card(self.card_csv,"TOP")
        self.add_card(self.card_fix_cities,"BOTTOM")
        self.add_card(self.card_divisor,"BOTTOM")


    def process_exp_msp(self):
        path = self.card_exp_msp.paths["btn_option1"]
        if path:
            exp_converter = MSPConverter(path)
            exp_converter.convert()
            self.card_exp_msp.set_text_btns(["btn_option1"])

    def process_dup(self):
        selected = self.card_duplicates.get_selected_text()
        path = self.card_duplicates.paths["btn_option1"]
        if path and selected:
            dup = RemoverDuplicadas(path,selected)
            dup.remover()
            self.card_duplicates.set_text_btns(["btn_option1"])

    def process_csv_converter(self):
        path = self.card_csv.paths["btn_option1"]
        if path:
            csv_converter = CSVConverter(path)
            csv_converter.converter_para_excel()
            self.card_csv.set_text_btns(["btn_option1"])

    def process_fix_cities(self):
        path = self.card_fix_cities.paths["btn_option1"]
        if path:
            fix_cities = CorrigirCidades(path)
            fix_cities.executar()
            self.card_fix_cities.set_text_btns(["btn_option1"])

    
    def create_division(self):
        selected = self.card_divisor.get_selected_text()
        if self.card_divisor.paths["btn_option1"] and selected:
             file = self.card_divisor.paths["btn_option1"]
             div = TableDivisor(file,selected)
             self.card_divisor.set_directory("btn_generate")
             path_save = self.card_divisor.paths["save"]
             div.create_files(path_save)
             self.card_divisor.set_text_btns(["btn_option1"])

         
