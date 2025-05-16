import os
import pandas as pd
import numpy as np
from Byakko.MODELS.Utilities.dicionarios import lista_cidades


class CorrigirCidades:
    def __init__(self, xlsx_file):
        self.xlsx_file = xlsx_file
        self.lista_cidades = lista_cidades
        self.df = None
        self.fixed_file = None
    
    def carregar_arquivo(self):
        if not self.xlsx_file:
            return False
        try:
            self.df = pd.read_excel(self.xlsx_file)
            base_nome = os.path.splitext(self.xlsx_file[0])
            self.fixed_file = f"fixed_cities_{base_nome}.xlsx"
            return True
        except Exception as e:
            print(f"⚠️ Erro ao ler o arquivo Excel: {e}")
            return False

    def levenshtein_distance(self, s1, s2):
        len_s1, len_s2 = len(s1), len(s2)
        dp = np.zeros((len_s1 + 1, len_s2 + 1), dtype=int)

        # Inicializa a matriz
        for i in range(len_s1 + 1):
            dp[i][0] = i
        for j in range(len_s2 + 1):
            dp[0][j] = j

        # Preenche a matriz
        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                if s1[i - 1] == s2[j - 1]:  
                    cost = 0  
                else:
                    cost = 1  
                
                dp[i][j] = min(dp[i - 1][j] + 1,        # Remoção
                            dp[i][j - 1] + 1,           # Inserção
                            dp[i - 1][j - 1] + cost)    # Substituição
        
        return dp[len_s1, len_s2]
    
    def encontrar_correspondente(self, word, word_list):
        if word in word_list:
            return word
        closest_word = min(word_list, key = lambda x: self.levenshtein_distance(word.lower(), x.lower()))
        return closest_word if closest_word.lower()!=word.lower() else word

    def fix_cities(self):
        if self.df is None:
            print("⚠️ Dados não carregados.")
            return
        for idx, row in self.df.iterrows():
            cidade, estado = row["city"], row["state"]
            cidades_estado = self.lista_cidades(estado)
            if cidades_estado:
                cidade_corrigida = self.encontrar_correspondente(cidade, cidades_estado)
                self.df.at[idx, "city"] = cidade_corrigida

    def salvar_arquivo(self):
        try:
            self.df.to_excel(self.fixed_file, index=False, engine='openpyxl')
            print(f"✅ Arquivo salvo como: {self.fixed_file}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar o arquivo Excel: {e}")

    def executar(self):
        if self.carregar_arquivo():
            self.corrigir_cidades()
            self.salvar_arquivo()
    