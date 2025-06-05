import MODELS.excel_file as ef
import pandas as pd
import openpyxl

class tecnicoCruzeiro:
    def __init__(self,file_ies,file_campus):
        file_msp = file_ies
        file_campus = file_campus
        self.sheet_process(file_msp,file_campus)
        self.treatment_name_ies()
        self.nursing_treatment()
        self.create_columns_search()
        self.fill_in_campus_id()
        self.names_treatment()
        self.fill_in_msp()

    def sheet_process(self,file_msp,file_campus):
        dtype_campus = {
            'id' : str,
            'metadata_code' : str
        }
        dtype_msp = {
            'ID_POLO' : str,
            'COD_CURSO' : str
        }
        self.msp = ef.new_dataframe(file_msp,"Modelo Sem Parar")
        self.port_tec = ef.new_dataframe(file_msp,"Polo X Portfólio Técnico",dtype= dtype_msp)
        self.tec_nursing = ef.new_dataframe(file_msp,"Polo X Portfólio Tec Enfermagem",dtype= dtype_msp)
        self.campus = ef.new_dataframe(file_campus,"Sheet 1",dtype=dtype_campus)
        self.campus_brazcubas =ef.new_filtered_dataframe(self.campus,"Brazcubas","university_name")
        self.campus_cruzeiro =ef.new_filtered_dataframe(self.campus,"UNICSUL - Cruzeiro do Sul","university_name")
        self.campus = ef.concat_dataframes(self.campus_cruzeiro,self.campus_brazcubas)
        self.pending,self.pending_nursing,self.pending_msp = None,None,None

    def treatment_name_ies(self):
        self.port_tec = ef.replace_pd(self.port_tec,"NOM_FILI","BRAZ CUBAS - TECNICO EAD","BRAZ CUBAS")
        self.port_tec = ef.replace_pd(self.port_tec,"NOM_FILI","CRUZEIRO DO SUL - TECNICO EAD","CRUZEIRO")

    def nursing_treatment(self):
        ef.xlookup_pd(self.tec_nursing,self.campus_brazcubas,'ID_POLO','metadata_code','id','campus_id')
        if ef.verify_nas(self.tec_nursing['campus_id']):
            self.pending_nursing = ef.get_nulls_in_dataframe(self.tec_nursing,'campus_id')
            self.tec_nursing = ef.remove_nas_dataframe(self.tec_nursing,'campus_id')
        else:
            self.pending_nursing = pd.DataFrame([["sem pendências"]])
        self.tec_nursing['concat'] = ef.concat_pd([self.tec_nursing['campus_id'],self.tec_nursing['ID_POLO']],";campus_code:")
        self.nursing_txt_join = ef.textjoin_pd(self.tec_nursing['concat'])

    def create_columns_search(self):
        ef.xlookup_pd(self.port_tec,self.msp,'NOM_FILI','Nome da IES','ID da IES','university_id')
        self.port_tec['concat'] = ef.concat_pd([self.port_tec['university_id'],self.port_tec['ID_POLO']])
        self.port_tec['concat2'] = ef.concat_pd([self.port_tec['university_id'],self.port_tec['NOME_POL']])
        self.campus['concat'] = ef.concat_pd([self.campus['university_id'],self.campus['metadata_code']])
        self.campus['concat2'] = ef.concat_pd([self.campus['university_id'],self.campus['name_from_university']])

    def fill_in_campus_id(self):
        ef.xlookup_pd(self.port_tec,self.campus,'concat','concat','id','campus_id')
        if ef.verify_nas(self.port_tec['campus_id']):
            nulls = ef.get_nulls_in_dataframe(self.port_tec,'campus_id')
            nulls = ef.delete_column_dataframe(nulls,'campus_id')
            self.port_tec = ef.remove_nas_dataframe(self.port_tec,'campus_id')
            ef.xlookup_pd(nulls,self.campus,'concat2','concat2','id','campus_id')
            if ef.verify_nas(nulls['campus_id']):
                self.pending = ef.get_nulls_in_dataframe(nulls,'campus_id')
                nulls = ef.remove_nas_dataframe(nulls,'campus_id')
            else:
                self.pending = pd.DataFrame([["sem pendências"]])
            self.port_tec = ef.concat_dataframes(self.port_tec,nulls)

    def names_treatment(self):
        self.port_tec = ef.replace_pd(self.port_tec,'DES_CURS'," ","")
        self.port_tec = ef.replace_pd(self.port_tec,'DES_CURS',".","")
        self.msp = ef.replace_pd(self.msp,'Semestre de Ingresso',",",".")
        self.msp['cursos'] = self.msp['Nome do Curso']
        self.msp = ef.replace_pd(self.msp,'cursos'," ","")
        self.port_tec['concat_curso'] = ef.concat_pd([self.port_tec['campus_id'],self.port_tec['DES_CURS']], "-")
        self.port_tec = ef.remove_duplicates_pd(self.port_tec,'concat_curso')

    def fill_in_msp(self):
        self.port_tec['ids_concatenados'] = ef.concat_pd([self.port_tec['campus_id'],self.port_tec['ID_POLO']], ";campus_code:")
        ids_campus = []
        for index,row in self.msp.iterrows():
            tec_university = self.port_tec['university_id'].astype(str)
            row_university = str(row['ID da IES'])
            tec_course = self.port_tec['DES_CURS'].astype(str)
            row_course = str(row['cursos'])
            filter = (tec_university == row_university ) & (tec_course == row_course)
            filtereds = self.port_tec.loc[filter,'ids_concatenados']
            result = ef.textjoin_pd(filtereds)
            if result == '':
                result = None
            if row['cursos'] == 'TÉCNICOEMENFERMAGEM':
                ids_campus.append(self.nursing_txt_join)
            else:
                ids_campus.append(result)     
        self.msp['ID do Campus'] = ids_campus
        if ef.verify_nas(self.msp['ID do Campus']):
            self.pending_msp = ef.get_nulls_in_dataframe(self.msp,'ID do Campus')
            self.msp = ef.remove_nas_dataframe(self.msp,'ID do Campus')
        else:
            self.pending_msp = pd.DataFrame([["sem pendências"]])

    def saving_and_separing_pendings(self,path):
        ef.save_multiple_dfs(path,[self.msp,self.pending,self.pending_nursing,self.pending_msp],['Modelo Sem Parar','Pendencias portfolio','Pendencias enfermagem','Pendencias MSP'])

