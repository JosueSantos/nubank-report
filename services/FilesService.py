import pandas as pd
from pathlib import Path


class FilesService():
    
    NUBANK_FILES = "nubank-"

    def load_and_process_data(folder_path):
        all_dataframes = []
        folder = Path(folder_path)
        files = folder.glob('*.csv')
        
        for file in files:
            df = pd.read_csv(file)

            filename = file.stem
            _, year, month = filename.split('-')
            df['month_ref'] = month + "/" + year

            all_dataframes.append(df)
            
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_df['date'] = pd.to_datetime(combined_df['date'])

        combined_df = combined_df[combined_df['category'] != 'payment']

        combined_df = combined_df.sort_values(by='date')
        
        return combined_df
    
    def filter_and_sum_by_month(dataframe):
        monthly_summary = dataframe.groupby(
            ['year', 'month', 'category']
        )['amount'].sum().reset_index()

        monthly_summary.columns = ['year', 'month', 'category', 'total_amount']

        return monthly_summary