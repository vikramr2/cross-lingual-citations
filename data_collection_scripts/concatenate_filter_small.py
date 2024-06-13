from sys import argv
import os
import pandas as pd
from tqdm import tqdm


folder = argv[1]

print(f"starting {folder}")

# Initialize an empty list to store individual dataframes
df_list = []

for file in os.listdir(folder):
    file_path = f'{folder}/{file}'

    # Read each CSV file
    temp_df = pd.read_csv(file_path, \
        usecols=['citing', 'cited', 'creation'], \
        dtype={'citing': str, 'cited': str, 'creation': str})

    # Convert the "creation" column to datetime
    temp_df['creation'] = pd.to_datetime(temp_df['creation'], errors='coerce')

    # Filter rows where "creation" is after January 1, 2019
    filtered_df = temp_df[temp_df['creation'] >= '2019-01-01']

    # Append the dataframe to the list
    df_list.append(filtered_df)

# Concatenate all dataframes into one
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv(f'{folder}.csv', index=False)

print(f"finishing {folder}")
