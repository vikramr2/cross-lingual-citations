import pandas as pd
import os
from tqdm import tqdm

# Directory containing the CSV files
directory = 'oc_citations_zips/'

# Initialize an empty list to hold DataFrames
dataframes = []

dirs = os.listdir(directory)

# Iterate over the files in the directory
for filename in tqdm(dirs):
    if filename.endswith('.csv'):
        # Construct the full file path
        filepath = os.path.join(directory, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)
        # Append the DataFrame to the list
        dataframes.append(df)

# Concatenate all the DataFrames in the list
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('oc_citation_events_lats_5yrs.csv', index=False)
