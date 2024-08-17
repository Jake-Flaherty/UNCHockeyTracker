import os
import datetime
import csv
import pandas as pd
from shorthand import countingWords, split_and_edit

def save_team_as_csv(dataframe, tab_name=None):
    # Format the date without the time
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    fileName = f'{date_str}_team_stats'
    
    if tab_name:
        fileName += f'_{tab_name.replace(" ", "_")}'
    
    dataframe.to_csv(fileName + '.csv', index=False)

def save_indiv_as_csv(dataframe, tab_name=None):
    # Format the date without the time
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    fileName = f'{date_str}_indiv_stats'
    
    if tab_name:
        fileName += f'_{tab_name.replace(" ", "_")}'
    
    dataframe.to_csv(fileName + '.csv', index=False)

def combine_csvs(tab_names, output_file_name):
    # Initialize an empty DataFrame with the same columns as the data
    aggregated_df = pd.DataFrame(columns=['FaceoffAttempts', 'FaceoffWins', 'Hits', 'Shots', 'ShotsFromHouse', 'TOO', 'TON', 'TOD', 'PEN', 'PIM', 'PK', 'PP', 'Saves', 'HitsOpp'])

    for tab_name in tab_names:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f'{date_str}_team_stats_{tab_name.replace(" ", "_")}.csv'
        
        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            
            # Aggregate the DataFrame
            for column in aggregated_df.columns:
                if column in df.columns:
                    if aggregated_df.empty:
                        aggregated_df[column] = df[column]
                    else:
                        aggregated_df[column] = aggregated_df[column].add(df[column].fillna(0), fill_value=0)
    
    if not aggregated_df.empty:
        aggregated_df.to_csv(output_file_name + '.csv', index=False)
    else:
        print("No data to combine.")