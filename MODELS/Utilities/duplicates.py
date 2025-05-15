import pandas as pd
import os

class RemoverDuplicadas:
    def __init__(self, excel_file, type_table):
        self.excel_file = excel_file
        self.type_table = type_table
        self.df = None
        self.df_no_dup = None
        self.df_dup = None
        self.no_dup_file = None

    def remover(self):
        if not self.excel_file:
            print("❌ Nenhum arquivo selecionado")
        
        try:
            # Gera o caminho de saída com base no nome do arquivo original
            base_nome = os.path.splitext(os.path.basename(self.excel_file))[0]
            self.no_dup_file = os.path.join(os.path.dirname(self.excel_file), f"No_dup_{base_nome}.xlsx")

            # Lê a planilha de entrada
            self.df = pd.read_excel(self.excel_file, engine='openpyxl')

            for col in self.df.select_dtypes(include=["object"]).columns:
                self.df[col] = self.df[col].str.replace(r"http\S+", "", regex=True)

            colunas_exp = [
                "university_id",
                "campus_id", 
                "name_from_university",
                "level",
                "kind",
                "shift",
                "enrollment_semester",
                "max_payments",
                "full_price"
            ]

            colunas_msp = [
                "ID do Campus",
                "Nome do Curso",
                "Grau",
                "Modalidade",
                "Turno",
                "Duração do Curso",
                "Mensalidade sem desconto"
            ]

            if self.type_table == "msp":
                colunas_para_comparacao = colunas_msp
            elif self.type_table == "exp":
                colunas_para_comparacao = colunas_exp
            else:
                print("❌ Tipo de tabela não reconhecido.")
                return

            # Cria a coluna de chave única concatenada
            self.df['SKU'] = self.df[colunas_para_comparacao].astype(str).apply(
                lambda row: '_'.join(row.values), axis=1
            )

            # Cria o df csó com as linhas duplicatas
            self.df_dup= self.df[self.df.duplicated(subset='SKU', keep=False)]

            # Cria um novo df removendo as duplicatas 
            self.df_no_dup = self.df.drop_duplicates(subset='SKU', keep='first')

            # Remove a coluna auxiliar da tabela modelo 'exp'
            if self.type_table =='exp':
                self.df_no_dup = self.df_no_dup.drop(columns=['SKU'])
                self.df_dup = self.df_dup.drop(columns=['SKU'])

            # Salvar o Df sem duplicadas na tabela original e cria uma nova aba 'Duplicados' para salvar os valores Duplicados
            try:
                with pd.ExcelWriter(self.no_dup_file, engine='openpyxl') as writer:
                    self.df_no_dup.to_excel(writer, index=False)
                    self.df_dup.to_excel(writer, index=False, sheet_name='Duplicados')
                    print(f"📁 Arquivo Excel salvo: {self.no_dup_file}")
            except Exception as e:
                print(f"⚠️ Erro ao salvar o arquivo Excel: {e}")
        
        except Exception as e:
            print(f"❌ Ocorreu um erro durante o processamento: {e}")
            return