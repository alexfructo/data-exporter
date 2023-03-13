import pandas as pd

class CentralDataProcessor():
    def __init__(self, config=None):
        # Inicialização da classe com o atributo config e atributos específicos para cada tipo de dados
        self.config = config
        self.attendance_config = config.get('data').get('central').get('attendance') if config else None
        self.activity_config = config.get('data').get('central').get('activity') if config else None
    
    def process_data_attendance(self, data) -> pd.DataFrame:
        attendance_data = data

        # Aplicação da configuração específica para os dados de attendance, se existir
        if self.attendance_config:
            columns = self.attendance_config.get('columns')
            rename_columns = self.attendance_config.get('rename_columns')
            
            # Filtragem das colunas, se a configuração existir
            if columns:
                attendance_data = attendance_data[columns]
            
            # Renomeação das colunas, se a configuração existir
            if rename_columns:
                attendance_data = attendance_data.rename(columns=rename_columns)
        
        # Normalização dos dados em um dataframe
        return pd.json_normalize(attendance_data)

    def process_data_activity(self, data) -> pd.DataFrame:
        activity_data = data

        # Aplicação da configuração específica para os dados de activity, se existir
        if self.activity_config:
            columns = self.activity_config.get('columns')
            rename_columns = self.activity_config.get('rename_columns')
            
            # Filtragem das colunas, se a configuração existir
            if columns:
                activity_data = activity_data[columns]
            
            # Renomeação das colunas, se a configuração existir
            if rename_columns:
                activity_data = activity_data.rename(columns=rename_columns)
        
        # Normalização dos dados em um dataframe
        return pd.json_normalize(activity_data)
