import pandas as pd
from pathlib import Path


class FilesService():
    
    NUBANK_FILES = "Nubank_"

    def load_and_process_data(folder_path):
        all_dataframes = []
        folder = Path(folder_path)
        files = folder.glob('*.csv')
        
        for file in files:
            df = pd.read_csv(file)

            filename = file.stem
            year, month, _ = filename.split('_')[1].split('-')
            df['month_ref'] = month + "/" + year

            all_dataframes.append(df)
            
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_df['date'] = pd.to_datetime(combined_df['date'])

        combined_df = combined_df[combined_df['title'] != 'Pagamento recebido']

        combined_df = combined_df.sort_values(by='date')
        
        return combined_df
    