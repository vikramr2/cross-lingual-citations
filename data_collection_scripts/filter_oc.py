import pandas as pd
import os
from datetime import datetime, timedelta
from tqdm import tqdm

# Set the path to the directory containing the CSV files
directory_path = 'oc_meta_dump/'

# Get data starting from 2019
date_string = '2019-01-01'
five_years_ago = datetime.strptime(date_string, '%Y-%m-%d')

# Initialize an empty list to store dataframes
dfs = []

# Loop through each file in the directory
for filename in tqdm(os.listdir(directory_path)):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory_path, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Filter rows where 'pub-date' is within the last 5 years
        # Convert 'pub-date' to datetime, errors='coerce' handles different date formats
        df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce')
        
        # Keep only the rows with 'pub-date' in the last 5 years
        df_filtered = df[df['pub_date'] >= five_years_ago]
        
        # Append the filtered dataframe to the list
        dfs.append(df_filtered)

# Concatenate all dataframes in the list
concatenated_df = pd.concat(dfs, ignore_index=True)

# Save the concatenated dataframe to a new CSV file
concatenated_df.to_csv('concatenated_last_5_years.csv', index=False)
