import pandas as pd
import os
import glob

df = pd.read_csv('integer_doi_mapping.csv')

# Read all csvs from ../data/unprocessed/openalex_first_sweep/ and concatenate them into a single DataFrame
path = '../data/unprocessed/openalex_first_sweep/'
all_files = glob.glob(os.path.join(path, "*.csv"))

fetched_df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# Get all entries in df whos ids are not in fetched_df
df = df[~df['id'].isin(fetched_df['id'])]

# Save the remaining entries to a new csv
df.to_csv('remaining_dois.csv', index=False)
