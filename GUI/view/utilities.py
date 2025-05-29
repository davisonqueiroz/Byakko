from GUI.content_area import *
from GUI.widgets.cards import *
from MODELS.Cruzeiro_do_Sul.pos_grad_ead import *
from MODELS.Cruzeiro_do_Sul.tecnico import *
from MODELS.Utilities.duplicates import *
from MODELS.Utilities.divisor import *


class Utilities(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)

        self.card_divisor = Card("divisor_table","#FF7E29")
        self.card_divisor.create_front_card("Dividir tabela","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_divisor.create_back_card("#FF7E29","1.Selecione em quantas tabelas deseja dividir a planilhazn2.Selecione o arquivo.\n3.Clique em 'Gerar'\n4.Selecione onde deseja salvar(todos os arquivos serão gerados no diretório selecionado)")
        cb_box_divisor = self.card_divisor.create_combobox(["2","3","4","5","6","7","8"])
        self.card_divisor.add_component_card(cb_box_divisor,"combobox")
        self.card_divisor.set_action_btn("btn_generate", self.create_division)

        self.card_exp_msp = Card("exp_msp","#FF7E29")
        self.card_exp_msp.create_front_card("Exp para MSP","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_exp_msp.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_exp_msp.set_action_btn("btn_generate", self.process_files)   
        
        self.card_duplicates = Card("duplicates","#FF7E29")
        self.card_duplicates.create_front_card("Remover Duplicadas","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_duplicates.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        cb_box_duplicates = self.card_duplicates.create_combobox(["MSP", "EXP"])
        self.card_duplicates.add_component_card(cb_box_duplicates,"combobox")
        self.card_duplicates.set_action_btn("btn_generate", self.process_dup)
        
        self.card_csv = Card("csvtoxlsx","#FF7E29")
        self.card_csv.create_front_card("CSV para Excel","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_csv.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_csv.set_action_btn("btn_generate", self.process_files)

        self.card_fix_cities = Card("fix_cities","#FF7E29")
        self.card_fix_cities.create_front_card("Corrigir Cidades","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.card_fix_cities.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_fix_cities.set_action_btn("btn_generate", self.process_files)        
        
        self.add_card(self.card_exp_msp,"TOP")
        self.add_card(self.card_duplicates,"TOP")
        self.add_card(self.card_csv,"TOP")
        self.add_card(self.card_fix_cities,"BOTTOM")
        self.add_card(self.card_divisor,"BOTTOM")


    def process_files(self):
            if self.card_tecnico.paths["btn_option1"] and self.card_tecnico.paths["btn_option2"]:
                msp = self.card_tecnico.paths["btn_option2"]
                exp = self.card_tecnico.paths["btn_option1"]
                tecnico = tecnicoCruzeiro(msp,exp)
                self.card_tecnico.set_save_manager("btn_generate")
                path_save = self.card_tecnico.paths["save"]
                tecnico.saving_and_separing_pendings(path_save)
                self.card_tecnico.set_text_btns(["btn_option1","btn_option2"],"Selecione o arquivo")

    def process_dup(self):
        print('entrou no process')
        selected = self.card_duplicates.get_selected_text()
        path = self.card_duplicates.paths["btn_option1"]
        print(selected)
        print(path)
        if path and selected:
            print('Entrou if')
            dup = RemoverDuplicadas(path,selected)
            dup.remover()
            self.card_duplicates.set_text_btns(["btn_option1"])

    
    def create_division(self):
        selected = self.card_divisor.get_selected_text()
        if self.card_divisor.paths["btn_option1"] and selected:
             file = self.card_divisor.paths["btn_option1"]
             div = TableDivisor(file,selected)
             self.card_divisor.set_directory("btn_generate")
             path_save = self.card_divisor.paths["save"]
             div.create_files(path_save)
             self.card_divisor.set_text_btns(["btn_option1"])

         
